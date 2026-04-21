# MCP Client Integration

Use the MCP (Model Context Protocol) client to interact with MCP servers for tool discovery and execution:

```python
from ioc_cfn_mas_client.mcp import new_client, connect, list_tools, call_tool

# Define MCP server URL
MCP_SERVER_URL = "http://localhost:9001"

# Create and connect to MCP server
client = new_client("my-mcp-client", "1.0.0")
session = await connect(client, MCP_SERVER_URL)

# Discover available tools
tools = await list_tools(session)
for tool in tools:
    print(f"Tool: {tool.name} - {tool.description}")

# Call a specific tool (retain/recall)
result = await call_tool(session, "retain", {
    "workspace_id": "my-workspace",
    "mas_id": "my-mas",
    "payload": {"data": "example"}
})

# Clean up
await session.close()
```

**Key Features:**

- **HTTP+SSE Protocol** - Compatible with Go MCP servers using `mcp.NewStreamableHTTPHandler()`
- **Tool Discovery** - Automatically list available tools from MCP server
- **Tool Execution** - Call tools with structured parameters and get results
- **Session Management** - Proper initialization and cleanup with UUID-based request IDs
- **Error Handling** - Comprehensive JSON-RPC error management

**Examples:**

```bash
# List all available tools
uv run python -m src.ioc_cfn_mas_client.mcp.mcp_client_sample --operation list_tools

# Test retain tool with complex payload
uv run python -m src.ioc_cfn_mas_client.mcp.mcp_client_sample --operation retain

# Test recall tool with semantic search
uv run python -m src.ioc_cfn_mas_client.mcp.mcp_client_sample --operation recall
```

## Files in this Directory

- **`mcp_client.py`** - Core MCP client implementation with HTTP+SSE support
- **`mcp_client_sample.py`** - Command-line sample demonstrating MCP operations
- **`README.md`** - This documentation file

## Server Requirements

The MCP client is designed to work with servers that implement:

- **Protocol Version**: 2024-11-05
- **Transport**: HTTP with Server-Sent Events (SSE)
- **Message Format**: JSON-RPC 2.0
- **Content-Type**: text/event-stream (primary) or application/json (fallback)
- **Session Management**: Uses Mcp-Session-Id headers for session tracking
- **Connection**: Persistent HTTP connections with keep-alive support

## Compatible Servers

- Go MCP servers using `mcp.NewStreamableHTTPHandler()`
- Any MCP server implementing the HTTP+SSE transport layer
- Servers exposing tools via the MCP protocol specification

For complete examples and implementation details, see the files in this directory.