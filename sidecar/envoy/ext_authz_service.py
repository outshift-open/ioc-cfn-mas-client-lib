#!/usr/bin/env python3
"""Envoy ext_authz service for A2A traffic interception."""

import asyncio
import logging
import sys
import os
from typing import Optional

import grpc
from grpc import aio
from envoy.service.auth.v3 import external_auth_pb2, external_auth_pb2_grpc
from envoy.type.v3 import http_status_pb2
from google.rpc import status_pb2, code_pb2

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from message_parser import A2AMessageParser, A2AMessage
from logger import log_a2a_message
from config import ProxyConfig
from ioc_cfn_mas_client import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class A2AExtAuthZService(external_auth_pb2_grpc.AuthorizationServicer):
    def __init__(self, config: ProxyConfig):
        self.config = config
        self.cfn_client: Optional[Client] = None

        if config.cfn_url and config.workspace_id and config.mas_id:
            try:
                self.cfn_client = Client(cfn_url=config.cfn_url)
                logger.info(f"CFN client initialized: {config.cfn_url}")
            except Exception as e:
                logger.error(f"Failed to initialize CFN client: {e}")

        logger.info("A2A ext_authz service initialized")

    async def Check(
        self,
        request: external_auth_pb2.CheckRequest,
        context: grpc.ServicerContext,
    ) -> external_auth_pb2.CheckResponse:
        try:
            http_req = request.attributes.request.http
            source_addr = request.attributes.source.address.socket_address
            source = f"{source_addr.address}:{source_addr.port_value}"

            if A2AMessageParser.is_a2a_message(http_req.method, http_req.path, dict(http_req.headers)):
                msg = A2AMessageParser.parse_message(
                    method=http_req.method,
                    path=http_req.path,
                    headers=dict(http_req.headers),
                    body=http_req.body.encode() if http_req.body else b"",
                    direction="request",
                )

                if msg:
                    log_a2a_message(msg, source, http_req.host or "unknown")
                    if self.cfn_client:
                        await self._send_to_cfn(msg)

            return external_auth_pb2.CheckResponse(
                status=status_pb2.Status(code=code_pb2.OK),
                ok_response=external_auth_pb2.OkHttpResponse(),
            )

        except Exception as e:
            logger.error(f"Error in ext_authz Check: {e}", exc_info=True)
            return external_auth_pb2.CheckResponse(
                status=status_pb2.Status(code=code_pb2.UNAUTHENTICATED),
                denied_response=external_auth_pb2.DeniedHttpResponse(
                    status=http_status_pb2.HttpStatus(code=http_status_pb2.Forbidden)
                ),
            )

    async def _send_to_cfn(self, message: A2AMessage):
        if not self.cfn_client:
            return

        try:
            self.cfn_client.create_shared_memories(
                workspace_id=self.config.workspace_id,
                mas_id=self.config.mas_id,
                data=[{
                    "protocol": message.protocol_type.value,
                    "method": message.method,
                    "path": message.path,
                    "direction": message.direction,
                    "task_id": message.task_id,
                    "message_id": message.message_id,
                    "agent_card_url": message.agent_card_url,
                    "body": message.body,
                }],
                format="a2a-protocol",
                agent_id=message.agent_card_url or "unknown",
            )
            logger.info(f"Sent to CFN: task={message.task_id}, msg={message.message_id}")
        except Exception as e:
            logger.error(f"Failed to send to CFN: {e}")


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
    parser.add_argument("--cfn-url")
    parser.add_argument("--workspace-id")
    parser.add_argument("--mas-id")
    args = parser.parse_args()

    config = ProxyConfig(
        cfn_url=args.cfn_url,
        workspace_id=args.workspace_id,
        mas_id=args.mas_id,
    )

    asyncio.run(serve(config))


if __name__ == "__main__":
    main()
