# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

#!/usr/bin/env python3
"""IOC CFN L9 service for A2A traffic interception.

This service integrates with Envoy's external authorization API to intercept
HTTP traffic at the L8 (A2A) layer, parse A2A messages, convert them to L9
format, and send them to CFN for semantic alignment and validation.

The service operates in fail-open mode to ensure traffic continues flowing
even if errors occur.
"""

import asyncio
import json
import logging
from typing import Optional

import grpc
import httpx
from grpc import aio
from envoy.service.auth.v3 import external_auth_pb2, external_auth_pb2_grpc
from google.rpc import code_pb2, status_pb2

from sidecar.shared.config import ProxyConfig
from sidecar.shared.l9_converter import a2a_to_l9
from sidecar.shared.logger import log_a2a_message
from sidecar.shared.message_parser import A2AMessage, A2AMessageParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IocCfnL9Service(external_auth_pb2_grpc.AuthorizationServicer):
    """IOC CFN L9 service: intercepts L8 (A2A) messages, converts to L9, and sends to CFN."""

    def __init__(self, config: ProxyConfig):
        self.config = config
        logger.info(f"CFN L9 validation endpoint: {config.cfn_url}/v1/l9/validate")
        logger.info("IOC CFN L9 service initialized (A2A → L9 conversion mode)")

    def _detect_direction(self, request: external_auth_pb2.CheckRequest) -> str:
        """
        Detect traffic direction using a clear priority order.

        Returns:
            "outbound" if traffic is app → external service
            "inbound" if traffic is external → app

        Detection strategy (in order):
        1. Localhost source = OUTBOUND (app making request)
        2. Service IP destination = OUTBOUND (calling another service)
        3. Istio metadata = use explicitly set direction
        4. App port destination = INBOUND (receiving on app port)
        5. Default = OUTBOUND
        """
        source_addr = request.attributes.source.address.socket_address
        dest_addr = request.attributes.destination.address.socket_address
        source_ip = source_addr.address
        dest_ip = dest_addr.address
        dest_port = dest_addr.port_value

        # 1. Localhost source → app is making the request (OUTBOUND)
        if source_ip.startswith("127.") or source_ip == "::1":
            logger.debug(f"OUTBOUND: source={source_ip} (localhost)")
            return "outbound"

        # 2. Service IP destination → calling another service (OUTBOUND)
        if self.config.network.is_service_ip(dest_ip):
            logger.debug(f"OUTBOUND: dest={dest_ip} (service IP)")
            return "outbound"

        # 3. Check Istio/Envoy metadata for explicit direction
        try:
            metadata_context = request.attributes.metadata_context
            if metadata_context and metadata_context.filter_metadata:
                if "istio_authn" in metadata_context.filter_metadata:
                    logger.debug("INBOUND: istio_authn metadata present")
                    return "inbound"

                conn_mgr_metadata = metadata_context.filter_metadata.get(
                    "envoy.filters.network.http_connection_manager"
                )
                if conn_mgr_metadata and "direction" in conn_mgr_metadata.fields:
                    direction = conn_mgr_metadata.fields["direction"].string_value
                    if direction in ["INBOUND", "OUTBOUND"]:
                        logger.debug(f"{direction}: from Envoy metadata")
                        return direction.lower()
        except Exception as e:
            logger.debug(f"No metadata available: {e}")

        # 4. App port destination → receiving request on app (INBOUND)
        if dest_port in self.config.network.app_ports:
            logger.debug(f"INBOUND: dest_port={dest_port} (app port)")
            return "inbound"

        # 5. Default to OUTBOUND (safer for fail-open)
        logger.debug(f"OUTBOUND: default fallback (source={source_ip}, dest={dest_ip}:{dest_port})")
        return "outbound"

    async def Check(
        self,
        request: external_auth_pb2.CheckRequest,
        context: grpc.ServicerContext,
    ) -> external_auth_pb2.CheckResponse:
        try:
            http_req = request.attributes.request.http
            source_addr = request.attributes.source.address.socket_address
            dest_addr = request.attributes.destination.address.socket_address
            source = f"{source_addr.address}:{source_addr.port_value}"
            dest = f"{dest_addr.address}:{dest_addr.port_value}"

            # Detect direction from Envoy's filter metadata (set by EnvoyFilter context)
            direction = self._detect_direction(request)

            logger.info(f"Intercepted: {source} → {dest}, direction={direction}")

            # Debug: Log request details
            logger.info(f"  Method: {http_req.method}, Path: {http_req.path}")
            logger.info(f"  Body length: {len(http_req.body) if http_req.body else 0}")

            # Parse body first for accurate A2A detection
            parsed_body = None
            if http_req.body:
                try:
                    parsed_body = json.loads(http_req.body)
                    logger.info(f"  Parsed body keys: {list(parsed_body.keys()) if parsed_body else 'none'}")
                    if 'method' in parsed_body:
                        logger.info(f"  JSON-RPC method: {parsed_body.get('method')}")
                except (json.JSONDecodeError, ValueError):
                    logger.info(f"  Body parse failed (not JSON)")

            is_a2a = A2AMessageParser.is_a2a_message(http_req.method, http_req.path, dict(http_req.headers), parsed_body)
            logger.info(f"  Is A2A: {is_a2a}")

            if is_a2a:
                msg = A2AMessageParser.parse_message(
                    method=http_req.method,
                    path=http_req.path,
                    headers=dict(http_req.headers),
                    body=http_req.body.encode() if http_req.body else b"",
                    direction=direction,  # Use detected direction
                )

                if msg:
                    log_a2a_message(msg, source, http_req.host or "unknown")
                    # Send to CFN in background - don't block proxy decision
                    try:
                        await self._send_to_cfn(msg, direction, source=source, dest=dest)
                    except Exception as e:
                        logger.error(f"Failed to send to CFN (non-blocking): {e}")

            # Always allow traffic through - interception is transparent
            return external_auth_pb2.CheckResponse(
                status=status_pb2.Status(code=code_pb2.OK),
                ok_response=external_auth_pb2.OkHttpResponse(),
            )

        except Exception as e:
            logger.error(f"Error in L9 service Check: {e}", exc_info=True)
            # Fail open - allow traffic even on error to avoid breaking the pod
            return external_auth_pb2.CheckResponse(
                status=status_pb2.Status(code=code_pb2.OK),
                ok_response=external_auth_pb2.OkHttpResponse(),
            )

    async def _send_to_cfn(self, message: A2AMessage, direction: str, source: str = None, dest: str = None):
        """Convert A2A to L9 and validate with CFN."""
        try:
            # Convert A2A → L9
            l9_message = a2a_to_l9(
                a2a_body=message.body or {},
                direction=direction,  # Use detected direction (inbound/outbound)
                actor_id=message.agent_card_url or "unknown",
                source=source,
                destination=dest,
                sidecar_id=self.config.sidecar_id
            )

            logger.info(f"🔄 Converted to L9: direction={direction}, task={message.task_id}")

            # Call CFN L9 validation endpoint
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.config.cfn_url}/v1/l9/validate",
                    json=l9_message,
                    headers={"Content-Type": "application/json"},
                    timeout=self.config.cfn_timeout_seconds
                )

                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"✅ CFN allowed: direction={direction}, task={message.task_id}, allow={result.get('allow')}")
                else:
                    logger.warning(f"❌ CFN denied: direction={direction}, status={response.status_code}, body={response.text}")

        except httpx.TimeoutException:
            logger.error(f"CFN timeout after {self.config.cfn_timeout_seconds}s")
        except Exception as e:
            logger.error(f"Failed to validate with CFN: {e}")


async def serve(config: Optional[ProxyConfig] = None):
    if config is None:
        config = ProxyConfig.from_env()

    server = aio.server()
    external_auth_pb2_grpc.add_AuthorizationServicer_to_server(
        IocCfnL9Service(config), server
    )

    listen_addr = f"0.0.0.0:{config.network.ext_authz_port}"
    server.add_insecure_port(listen_addr)
    logger.info(f"Starting IOC CFN L9 service on {listen_addr}")
    await server.start()

    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        await server.stop(grace=5)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfn-url", required=True, help="CFN API endpoint URL")
    parser.add_argument("--workspace-id", required=True, help="CFN workspace ID")
    parser.add_argument("--mas-id", required=True, help="CFN MAS ID")
    args = parser.parse_args()

    config = ProxyConfig(
        cfn_url=args.cfn_url,
        workspace_id=args.workspace_id,
        mas_id=args.mas_id,
    )

    asyncio.run(serve(config))


if __name__ == "__main__":
    main()
