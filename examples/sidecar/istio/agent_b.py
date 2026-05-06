#!/usr/bin/env python3
"""Agent B - A2A server + client (NO sidecar awareness)."""

import asyncio
import logging
import httpx
from fastapi import FastAPI
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

AGENT_A_URL = "http://agent-a:8001"
MESSAGE_INTERVAL = 20  # seconds (longer for easier demo observation, offset from Agent A)


@app.post("/")
async def handle_a2a_request(request: dict):
    """Handle incoming A2A JSON-RPC request."""
    logger.info(f"Agent B received request: {request.get('params', {}).get('message', 'N/A')}")

    if request.get("jsonrpc") == "2.0":
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "status": "completed",
                "message": "Agent B processed your request",
            },
        }

    return {"error": "Invalid A2A request"}


@app.get("/.well-known/agent.json")
async def agent_card():
    """Agent card (A2A protocol)."""
    return {
        "name": "Agent B",
        "description": "Simple A2A agent",
        "url": "http://agent-b:8000",
    }


async def send_periodic_messages():
    """Periodically send messages to Agent A."""
    await asyncio.sleep(12)  # Wait for services to be ready

    counter = 0
    while True:
        try:
            counter += 1
            message = f"Message #{counter} from Agent B"

            request = {
                "jsonrpc": "2.0",
                "id": str(counter),
                "method": "tasks/send",
                "params": {"message": message},
            }

            logger.info(f"Agent B sending to Agent A: {message}")

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    AGENT_A_URL,
                    json=request,
                    headers={"Content-Type": "application/json"},
                    timeout=10.0,
                )
                result = response.json()
                logger.info(f"Agent B received response from Agent A: {result.get('result', {}).get('message', 'N/A')}")

        except Exception as e:
            logger.error(f"Agent B failed to send message: {e}")

        await asyncio.sleep(MESSAGE_INTERVAL)


async def run_server():
    """Run FastAPI server."""
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    """Run both server and periodic client."""
    logger.info("Starting Agent B (server + client) - NO sidecar awareness!")

    # Run server and periodic sender concurrently
    await asyncio.gather(
        run_server(),
        send_periodic_messages(),
    )


if __name__ == "__main__":
    asyncio.run(main())
