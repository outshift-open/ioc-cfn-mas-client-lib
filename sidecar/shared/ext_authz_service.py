#!/usr/bin/env python3
"""Envoy ext_authz service for A2A traffic interception.

This service integrates with Envoy's external authorization API to intercept
HTTP traffic, parse A2A messages, convert them to L9 format, and send them to
CFN for validation. The service operates in fail-open mode to ensure traffic
continues flowing even if errors occur.
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


class A2AExtAuthZService(external_auth_pb2_grpc.AuthorizationServicer):
    def __init__(self, config: ProxyConfig):
        self.config = config
        logger.info(f"CFN L9 validation endpoint: {config.cfn_url}/v1/l9/validate")
        logger.info("A2A ext_authz service initialized (L9 mode)")

    def _detect_direction_from_metadata(self, request: external_auth_pb2.CheckRequest) -> str:
        """
        Detect traffic direction from Envoy metadata and headers.

        Strategy:
        1. Check for source IP: if it's localhost/127.x.x.x, it's OUTBOUND (app → sidecar → external)
        2. Check Istio/Envoy metadata for direction hints
        3. Check destination: if local pod, it's INBOUND
        4. Fallback to port-based heuristic
        """
        source_addr = request.attributes.source.address.socket_address
        dest_addr = request.attributes.destination.address.socket_address
        source_ip = source_addr.address
        dest_ip = dest_addr.address

        # Strategy 1: Service IP detection (most reliable for Kubernetes)
        # - Outbound: destination is a Kubernetes service ClusterIP (10.96.x.x range)
        #   App calls service name → resolves to ClusterIP → Envoy intercepts outbound
        # - Inbound: destination is pod IP (10.244.x.x range) or localhost
        #   External → Envoy intercepts inbound → forwards to local app

        # Check if destination is a service ClusterIP (typically 10.96.x.x in default k8s)
        if dest_ip.startswith("10.96."):
            logger.info(f"OUTBOUND detected: dest={dest_ip} (service ClusterIP)")
            return "outbound"

        # Check localhost patterns
        if source_ip.startswith("127.") or source_ip == "::1":
            logger.info(f"OUTBOUND detected: source={source_ip} (localhost)")
            return "outbound"

        if dest_ip.startswith("127.") or dest_ip == "::1":
            logger.info(f"INBOUND detected: dest={dest_ip} (localhost)")
            return "inbound"

        # Strategy 2: Check Istio metadata
        try:
            metadata_context = request.attributes.metadata_context
            if metadata_context and metadata_context.filter_metadata:
                # Istio sets 'istio_authn' metadata with source principal for inbound
                if "istio_authn" in metadata_context.filter_metadata:
                    return "inbound"

                # Check for listener metadata
                if "envoy.filters.network.http_connection_manager" in metadata_context.filter_metadata:
                    listener_metadata = metadata_context.filter_metadata[
                        "envoy.filters.network.http_connection_manager"
                    ]
                    if listener_metadata and "direction" in listener_metadata.fields:
                        direction_value = listener_metadata.fields["direction"].string_value
                        if direction_value in ["INBOUND", "OUTBOUND"]:
                            return direction_value.lower()
        except Exception as e:
            logger.debug(f"Could not extract direction from metadata: {e}")

        # Fallback: Use port-based heuristic
        is_inbound = dest_addr.port_value in [8000, 8001]
        direction = "inbound" if is_inbound else "outbound"
        logger.debug(f"Using port-based fallback: dest_port={dest_addr.port_value} → {direction}")
        return direction

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
            direction = self._detect_direction_from_metadata(request)

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
            logger.error(f"Error in ext_authz Check: {e}", exc_info=True)
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
                    timeout=1.0
                )

                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"✅ CFN allowed: direction={direction}, task={message.task_id}, allow={result.get('allow')}")
                else:
                    logger.warning(f"❌ CFN denied: direction={direction}, status={response.status_code}, body={response.text}")

        except httpx.TimeoutException:
            logger.error(f"CFN timeout after 1s")
        except Exception as e:
            logger.error(f"Failed to validate with CFN: {e}")


async def serve(config: Optional[ProxyConfig] = None):
    if config is None:
        config = ProxyConfig.from_env()

    server = aio.server()
    external_auth_pb2_grpc.add_AuthorizationServicer_to_server(
        A2AExtAuthZService(config), server
    )

    listen_addr = "0.0.0.0:9001"
    server.add_insecure_port(listen_addr)
    logger.info(f"Starting ext_authz service on {listen_addr}")
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
