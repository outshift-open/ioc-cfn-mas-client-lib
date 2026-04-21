#!/usr/bin/env python3
"""Agent B - Simple A2A server (NO sidecar awareness)."""

import logging
from fastapi import FastAPI
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/")
async def handle_a2a_request(request: dict):
    """Handle A2A JSON-RPC request."""
    logger.info(f"Agent B received request: {request}")

    if request.get("jsonrpc") == "2.0":
        method = request.get("method")
        params = request.get("params", {})

        if method == "tasks/send":
            message = params.get("message", "")
            logger.info(f"Processing task: {message}")

            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "status": "completed",
                    "message": f"Agent B processed: {message}",
                },
            }

    return {"error": "Invalid A2A request"}


@app.get("/.well-known/agent.json")
async def agent_card():
    """Agent card (A2A protocol)."""
    return {
        "name": "Agent B",
        "description": "Simple A2A server",
        "url": "http://agent-b:8000",
    }


if __name__ == "__main__":
    logger.info("Starting Agent B (A2A server) - NO sidecar awareness!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
