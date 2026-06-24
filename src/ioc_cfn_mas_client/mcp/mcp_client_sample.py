# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""Sample MCP client usage demonstrating connection, tool listing, and tool calling."""

import asyncio
import logging
import argparse
import json
from typing import Dict, Any

from .mcp_client import new_client, connect, list_tools, call_tool, print_tool_result

# Commands:
# uv run python -m src.ioc_cfn_mas_client.mcp.mcp_client_sample --operation list_tools
# uv run python -m src.ioc_cfn_mas_client.mcp.mcp_client_sample --operation retain
# uv run python -m src.ioc_cfn_mas_client.mcp.mcp_client_sample --operation recall

# Constants
TOOL_NAME_RETAIN = "retain"
TOOL_NAME_RECALL = "recall"
MCP_SERVER_PORT = 9001


async def list_tools_operation(session, logger):
    """List all available tools from the MCP server."""
    tools = await list_tools(session)
    
    logger.info(f"Retrieved {len(tools)} tools from server:")
    for i, tool in enumerate(tools):
        logger.info(f"  Tool {i}: {tool.name if hasattr(tool, 'name') else 'Unknown'}")
        if hasattr(tool, 'description'):
            logger.info(f"    Description: {tool.description}")
        if hasattr(tool, 'inputSchema'):
            logger.info(f"    Input Schema: {tool.inputSchema}")
    
    return tools


async def retain_operation(session, logger):
    """Demonstrate retain tool functionality."""
    # Test calling the retain tool with complex payload
    tool_args: Dict[str, Any] = {
        "workspace_id": "7f136aa0-143c-46a6-82f2-249eac489e52",
        "mas_id": "223e4567-e89b-12d3-a456-426614174001",
        "request_id": "test-request-retain-123",
        "header": {
            "agent_id": "test-agent-retain",
        },
        "payload": {
            "metadata": {
                "format": "openclaw",
            },
            "data": [
                {
                    "schema": "openclaw-conversation-v1",
                    "extractedAt": "2026-02-25T20:32:24.376Z",
                    "session": {
                        "agentId": "main",
                        "sessionId": "906630a9-bf57-48d8-bbae-9d41e7639d29",
                        "sessionKey": "agent:main:matrix:channel:!ltghwkqehwwjyjyrhf:local",
                        "channel": "matrix",
                        "cwd": "/home/node/.openclaw/workspace",
                    },
                    "stats": {
                        "totalEntries": 8,
                        "turns": 1,
                        "toolCallCount": 1,
                        "thinkingTurnCount": 0,
                        "totalCost": 0,
                    },
                    "turns": [
                        {
                            "index": 0,
                            "timestamp": "2026-02-25T20:32:14.783Z",
                            "model": "bedrock/global.anthropic.claude-haiku-4-5-20251001-v1:0",
                            "stopReason": "stop",
                            "usage": {
                                "input": 9,
                                "output": 469,
                                "cacheRead": 13531,
                                "cacheWrite": 14906,
                                "totalTokens": 28915,
                                "cost": {
                                    "input": 0,
                                    "output": 0,
                                    "cacheRead": 0,
                                    "cacheWrite": 0,
                                    "total": 0,
                                },
                            },
                            "userMessage": "Test message for MCP retain operation",
                            "thinking": None,
                            "toolCalls": [
                                {
                                    "id": "toolu_test_retain_123",
                                    "name": "read",
                                    "input": {
                                        "path": "/test/path",
                                    },
                                    "result": "Test result for retain",
                                    "isError": False,
                                },
                            ],
                            "response": "Test response from agent for retain operation",
                        },
                    ],
                },
            ],
        },
    }
    
    logger.info(f"Calling {TOOL_NAME_RETAIN} tool...")
    logger.info(f"Tool arguments:\n{json.dumps(tool_args, indent=2)}")
    result = await call_tool(session, TOOL_NAME_RETAIN, tool_args)
    
    if result is None or not hasattr(result, 'content') or len(result.content) == 0:
        raise RuntimeError("expected result content, but got none")
    
    print_tool_result(result)
    logger.info("Retain tool call completed successfully")


async def recall_operation(session, logger):
    """Demonstrate recall tool functionality."""
    # Test calling the recall tool with semantic graph traversal
    intent = "Tell me something about Q2 budget planning"
    tool_args: Dict[str, Any] = {
        "workspace_id": "7f136aa0-143c-46a6-82f2-249eac489e52",
        "mas_id": "223e4567-e89b-12d3-a456-426614174001",
        "intent": intent,
        "search_strategy": "semantic_graph_traversal",
        "request_id": "test-request-recall-123",
        "header": {
            "agent_id": "test-agent-recall",
        },
    }
    
    logger.info(f"Calling {TOOL_NAME_RECALL} tool with intent: '{intent}'")
    logger.info(f"Tool arguments:\n{json.dumps(tool_args, indent=2)}")
    result = await call_tool(session, TOOL_NAME_RECALL, tool_args)
    
    if result is None or not hasattr(result, 'content') or len(result.content) == 0:
        raise RuntimeError("expected result content, but got none")
    
    print_tool_result(result)
    logger.info("Recall tool call completed successfully")


async def main():
    """Main function demonstrating MCP client usage."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='MCP Client Sample')
    parser.add_argument('--operation', 
                       choices=['list_tools', 'retain', 'recall'], 
                       default='list_tools',
                       help='Operation to perform (default: list_tools)')
    args = parser.parse_args()
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    session = None
    try:
        # Create client and connect
        client = new_client("mcp-test-client", "1.0.0")
        mcp_server_url = f"http://localhost:{MCP_SERVER_PORT}"
        session = await connect(client, mcp_server_url)
        
        logger.info(f"Connected to mcpserver at {mcp_server_url}")
        
        # Execute the requested operation
        if args.operation == 'list_tools':
            await list_tools_operation(session, logger)
        elif args.operation == 'retain':
            # First check if retain tool is available
            tools = await list_tools_operation(session, logger)
            retain_available = any(getattr(t, 'name', '') == TOOL_NAME_RETAIN for t in tools)
            if not retain_available:
                raise RuntimeError(f"retain tool not found in registered tools")
            await retain_operation(session, logger)
        elif args.operation == 'recall':
            # First check if recall tool is available
            tools = await list_tools_operation(session, logger)
            recall_available = any(getattr(t, 'name', '') == TOOL_NAME_RECALL for t in tools)
            if not recall_available:
                raise RuntimeError(f"recall tool not found in registered tools")
            await recall_operation(session, logger)
        
    except Exception as e:
        logger.error(f"MCP client sample failed: {e}")
        raise
    finally:
        # Ensure proper cleanup of HTTP session
        if session and hasattr(session, 'close'):
            try:
                await session.close()
                logger.debug("HTTP session closed successfully")
            except Exception as cleanup_error:
                logger.warning(f"Error during session cleanup: {cleanup_error}")


if __name__ == "__main__":
    asyncio.run(main())