#!/usr/bin/env python3
"""CFN API server - logs intercepted A2A messages."""

import logging
from datetime import datetime
from fastapi import FastAPI, Request
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/api/workspaces/{workspace_id}/multi-agentic-systems/{mas_id}/shared-memories")
async def create_shared_memories(workspace_id: str, mas_id: str, request: Request):
    """CFN shared memory creation endpoint."""
    body = await request.json()

    logger.info("=" * 80)
    logger.info("🎯 INTERCEPTED A2A MESSAGE")
    logger.info(f"Workspace: {workspace_id}")
    logger.info(f"MAS: {mas_id}")
    logger.info(f"Data: {body}")
    logger.info("=" * 80)

    return {"status": "ok", "message": "CFN API received message"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9002)
