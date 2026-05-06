#!/usr/bin/env python3
"""CFN API server - validates L9 messages."""

import logging
from fastapi import FastAPI, Request
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/v1/l9/validate")
async def validate_l9(request: Request):
    """CFN L9 validation endpoint - receives L9-formatted messages from sidecars."""
    l9_message = await request.json()

    header = l9_message.get("header", {})
    payload = l9_message.get("payload", {})

    # Extract direction and format symbols
    direction = header.get('direction', 'unknown')
    direction_symbol = "→" if direction == "outbound" else "←" if direction == "inbound" else "?"

    # Extract source and destination
    source = header.get('source', 'unknown')
    dest = header.get('destination', 'unknown')
    sidecar_id = header.get('sidecar_id', 'unknown')

    logger.info("=" * 80)
    logger.info(f"🎯 CFN RECEIVED L9 MESSAGE")
    logger.info(f"Direction: {direction.upper()} {direction_symbol}")
    logger.info(f"Intercepted by: {sidecar_id}")
    logger.info(f"Source: {source} {direction_symbol} Dest: {dest}")
    logger.info(f"Actor ID: {header.get('actor_id')}")
    logger.info(f"Timestamp: {header.get('timestamp')}")

    # Log protocol-specific payload
    if "a2a" in payload:
        a2a_payload = payload['a2a']
        msg_id = a2a_payload.get('id', 'N/A')
        method = a2a_payload.get('method', 'N/A')
        params = a2a_payload.get('params', {})
        message = params.get('message', 'N/A') if isinstance(params, dict) else 'N/A'
        logger.info(f"A2A Message: [{msg_id}] {method} - {message}")
    elif "mcp" in payload:
        logger.info(f"MCP payload: {payload['mcp']}")

    logger.info("=" * 80)

    # TODO: Add actual policy validation logic here
    # For now, always allow
    return {"status": "ok", "allow": True}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    logger.info("Starting CFN API server with L9 validation endpoint...")
    logger.info("Listening on: http://0.0.0.0:9002")
    logger.info("Endpoint: POST /v1/l9/validate")
    uvicorn.run(app, host="0.0.0.0", port=9002)
