#!/usr/bin/env python3
"""Agent A - Simple A2A client (NO sidecar awareness)."""

import logging
import time
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AGENT_B_URL = "http://agent-b:8000"


def send_a2a_request(message: str):
    """Send A2A JSON-RPC request to Agent B."""
    request = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tasks/send",
        "params": {
            "message": message,
        },
    }

    logger.info(f"Agent A sending request to Agent B: {message}")

    try:
        response = httpx.post(
            AGENT_B_URL,
            json=request,
            headers={"Content-Type": "application/json"},
            timeout=10.0,
        )
        response.raise_for_status()
        result = response.json()
        logger.info(f"Agent A received response: {result}")
        return result
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return None


if __name__ == "__main__":
    logger.info("Starting Agent A (A2A client) - NO sidecar awareness!")

    # Wait for Agent B to be ready
    logger.info("Waiting for Agent B to be ready...")
    time.sleep(5)

    # Send test messages
    messages = [
        "Hello from Agent A",
        "Process this task please",
        "Final test message",
    ]

    for msg in messages:
        logger.info(f"\n{'='*60}")
        send_a2a_request(msg)
        logger.info(f"{'='*60}\n")
        time.sleep(2)

    logger.info("Agent A finished sending requests")
