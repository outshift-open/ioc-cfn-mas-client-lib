# MCP (Model Context Protocol) Integration with CFN

This document describes the supported MCP functionality for interacting with CFN's shared memory system.

## Architecture

```
┌─────────────────┐  JSON-RPC 2.0   ┌─────────────────┐
│   MCP Client    │  over HTTP+SSE  │   ioc-cfn-svc   │
│ (HTTP+SSE)      │◄──────────────►│   MCP Server    │
└─────────────────┘                 └─────────────────┘
                                             │
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │ CFN Shared      │
                                    │ Memory System   │
                                    └─────────────────┘
```

**Note**: The current `Client.retain()` and `Client.recall()` methods return mock responses and do not use the JSON-RPC protocol. For actual MCP protocol communication, use the direct MCP client commands shown in the examples below in [MCP Client Source](../src/ioc_cfn_mas_client/mcp/) as part of the `Client.retain()` and `Client.recall()` methods.

## Supported Functionality

The MCP client provides the following capabilities:

- **Retain Operations** - Store conversation data in OpenClaw format
- **Recall Operations** - Query stored memories using natural language intents
- **Mock Responses** - Returns structured test data without requiring live MCP server
- **Session Management** - Proper initialization and cleanup with UUID-based request IDs

## Installation

```bash
pip install ioc-cfn-mas-client-lib
```

## Usage

### Integrated Client Methods

```python
import asyncio
from ioc_cfn_mas_client import Client

async def main():
    client = Client(cfn_url="http://localhost:9001")
    
    # Retain shared memories
    result = await client.retain(
        workspace_id="my-workspace",
        mas_id="my-mas",
        payload={
            "metadata": {"format": "openclaw"},
            "data": [{"example": "conversation"}]
        }
    )
    print(f"Retain result: {result['status']}")
    
    # Recall shared memories
    result = await client.recall(
        workspace_id="my-workspace",
        mas_id="my-mas",
        intent="Find information about user preferences"
    )
    print(f"Recall result: {result['message']}")

asyncio.run(main())
```

### Command-Line Usage

```bash
# Run comprehensive example
uv run python examples/mcp/client_example.py

# Direct MCP protocol testing (advanced)
uv run python -m src.ioc_cfn_mas_client.mcp.mcp_client_sample --operation list_tools
uv run python -m src.ioc_cfn_mas_client.mcp.mcp_client_sample --operation retain
uv run python -m src.ioc_cfn_mas_client.mcp.mcp_client_sample --operation recall
```

## Related Resources

- [Example Implementation](../examples/mcp/client_example.py)
- [MCP Client Source](../src/ioc_cfn_mas_client/mcp/)
