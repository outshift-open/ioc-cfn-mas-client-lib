#!/usr/bin/env python3
"""Envoy ext_authz service for A2A traffic interception."""

import asyncio
import json
import logging
from typing import Optional

import grpc
from grpc import aio
from envoy.service.auth.v3 import external_auth_pb2, external_auth_pb2_grpc
from envoy.type.v3 import http_status_pb2
from google.rpc import status_pb2, code_pb2

from sidecar.shared.message_parser import A2AMessageParser, A2AMessage
from sidecar.shared.logger import log_a2a_message
from sidecar.shared.config import ProxyConfig
from sidecar.shared.l9_converter import a2a_to_l9
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class A2AExtAuthZService(external_auth_pb2_grpc.AuthorizationServicer):
    def __init__(self, config: ProxyConfig):
        self.config = config
        logger.info(f"CFN L9 validation endpoint: {config.cfn_url}/v1/l9/validate")
        logger.info("A2A ext_authz service initialized (L9 mode)")

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

            # Detect direction: inbound (dest is agent) vs outbound (source is agent)
            # Heuristic: if destination port is agent port (8000/8001), it's inbound
            is_inbound = dest_addr.port_value in [8000, 8001]
            direction = "inbound" if is_inbound else "outbound"

            logger.debug(f"Intercepted: {source} → {dest}, direction={direction}")

            # Parse body first for accurate A2A detection
            parsed_body = None
            if http_req.body:
                try:
                    parsed_body = json.loads(http_req.body)
                except (json.JSONDecodeError, ValueError):
                    pass

            if A2AMessageParser.is_a2a_message(http_req.method, http_req.path, dict(http_req.headers), parsed_body):
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
                        await self._send_to_cfn(msg, direction)
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

    async def _send_to_cfn(self, message: A2AMessage, direction: str):
        """Convert A2A to L9 and validate with CFN."""
        try:
            # Convert A2A → L9
            l9_message = a2a_to_l9(
                a2a_body=message.body or {},
                direction=direction,  # Use detected direction (inbound/outbound)
                actor_id=message.agent_card_url or "unknown"
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
