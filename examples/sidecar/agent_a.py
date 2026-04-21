#!/usr/bin/env python3
"""Agent A - A2A server + client (NO sidecar awareness)."""

import asyncio
import logging
import httpx
from fastapi import FastAPI
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

AGENT_B_URL = "http://agent-b:8000"
MESSAGE_INTERVAL = 5  # seconds


@app.post("/")
async def handle_a2a_request(request: dict):
    """Handle incoming A2A JSON-RPC request."""
    logger.info(f"Agent A received request: {request.get('params', {}).get('message', 'N/A')}")

    if request.get("jsonrpc") == "2.0":
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "status": "completed",
                "message": "Agent A processed your request",
            },
        }

    return {"error": "Invalid A2A request"}


@app.get("/.well-known/agent.json")
async def agent_card():
    """Agent card (A2A protocol)."""
    return {
        "name": "Agent A",
        "description": "Simple A2A agent",
        "url": "http://agent-a:8001",
    }


async def send_periodic_messages():
    """Periodically send messages to Agent B."""
    await asyncio.sleep(10)  # Wait for services to be ready

    counter = 0
    while True:
        try:
            counter += 1
            message = f"Message #{counter} from Agent A"

            request = {
                "jsonrpc": "2.0",
                "id": str(counter),
                "method": "tasks/send",
                "params": {"message": message},
            }

            logger.info(f"Agent A sending to Agent B: {message}")

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    AGENT_B_URL,
                    json=request,
                    headers={"Content-Type": "application/json"},
                    timeout=10.0,
                )
                result = response.json()
                logger.info(f"Agent A received response from Agent B: {result.get('result', {}).get('message', 'N/A')}")

        except Exception as e:
            logger.error(f"Agent A failed to send message: {e}")

        await asyncio.sleep(MESSAGE_INTERVAL)


async def run_server():
    """Run FastAPI server."""
    config = uvicorn.Config(app, host="0.0.0.0", port=8001, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    """Run both server and periodic client."""
    logger.info("Starting Agent A (server + client) - NO sidecar awareness!")

    # Run server and periodic sender concurrently
    await asyncio.gather(
        run_server(),
        send_periodic_messages(),
    )


if __name__ == "__main__":
    asyncio.run(main())
