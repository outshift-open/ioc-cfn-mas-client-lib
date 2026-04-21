"""MCP client.

This client is designed to work with MCP (Model Context Protocol) servers that implement:

SERVER CONFIGURATION REQUIREMENTS:
- Protocol Version: 2024-11-05
- Transport: HTTP with Server-Sent Events (SSE)
- Message Format: JSON-RPC 2.0
- Content-Type: text/event-stream (primary) or application/json (fallback)
- Session Management: Uses Mcp-Session-Id headers for session tracking
- Connection: Persistent HTTP connections with keep-alive support

PROTOCOL IMPLEMENTATION:
- Session Initialization: Requires 'initialize' method call before other operations
- Tool Discovery: 'tools/list' method to enumerate available tools
- Tool Execution: 'tools/call' method with structured parameters
- Response Format: SSE events with 'data: {json-rpc-response}' format
- Error Handling: Standard JSON-RPC error responses

COMPATIBLE SERVERS:
- Go MCP servers using mcp.NewStreamableHTTPHandler()
- Any MCP server implementing the HTTP+SSE transport layer
- Servers exposing tools via the MCP protocol specification

NETWORK REQUIREMENTS:
- HTTP/1.1 or HTTP/2 support
- Server-Sent Events (EventSource) compatibility
- JSON-RPC 2.0 message parsing
- Persistent connection handling
"""

import logging
from typing import Any, Dict, List, Optional
import threading
import json
import aiohttp
import uuid

class Tool:
    def __init__(self, name: str, description: str = "", **kwargs):
        self.name = name
        self.description = description
        for k, v in kwargs.items():
            setattr(self, k, v)

class CallToolResult:
    def __init__(self, content=None):
        self.content = content or []

class CallToolParams:
    def __init__(self, name: str, arguments: Dict[str, Any]):
        self.name = name
        self.arguments = arguments

class TextContent:
    def __init__(self, text: str):
        self.text = text

class ClientSession:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session_initialized = False
        self.http_session = None
        self.mcp_session_id = None
        self.connector = None
    
    async def _send_request(self, method: str, params: Dict[str, Any] = None, request_id: int = None):
        """Send a JSON-RPC request to the MCP server and handle streaming response."""
        if not self.http_session:
            # Create connector that keeps connections alive
            self.connector = aiohttp.TCPConnector(keepalive_timeout=300, enable_cleanup_closed=True)
            self.http_session = aiohttp.ClientSession(connector=self.connector)
        
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {}
        }
        
        if request_id is not None:
            payload["id"] = request_id
        
        headers = {'Content-Type': 'application/json'}
        if self.mcp_session_id:
            headers['Mcp-Session-Id'] = self.mcp_session_id
        
        async with self.http_session.post(self.base_url, json=payload, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                raise RuntimeError(f"HTTP {response.status}: {text}")
            
            # Capture session ID from response headers
            if 'Mcp-Session-Id' in response.headers and not self.mcp_session_id:
                self.mcp_session_id = response.headers['Mcp-Session-Id']
            
            # Handle streaming response
            content_type = response.headers.get('content-type', '')
            if content_type.startswith('text/event-stream'):
                # Parse Server-Sent Events
                async for line in response.content:
                    line_str = line.decode().strip()
                    if line_str.startswith('data: '):
                        try:
                            data = json.loads(line_str[6:])  # Remove 'data: ' prefix
                            if "error" in data:
                                raise RuntimeError(f"MCP error: {data['error']}")
                            return data
                        except json.JSONDecodeError:
                            continue
            elif content_type.startswith('application/json'):
                # Handle regular JSON response
                data = await response.json()
                if "error" in data:
                    raise RuntimeError(f"MCP error: {data['error']}")
                return data
            else:
                # Handle plain text or other content types
                text = await response.text()
                return {"result": {"text": text}}
    
    async def _initialize_session(self):
        """Initialize MCP session if not already done."""
        if self.session_initialized:
            return
        
        # Send initialize request
        response = await self._send_request(
            method="initialize",
            params={
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "mcp-test-client",
                    "version": "1.0.0"
                }
            },
            request_id=str(uuid.uuid4())
        )
        
        # Check if initialization was successful
        if response.get("result"):
            self.session_initialized = True
        else:
            raise RuntimeError("MCP initialization failed")
    
    async def list_tools(self, params=None):
        """List tools via MCP session."""
        await self._initialize_session()
        
        response = await self._send_request(
            method="tools/list",
            params=params or {},
            request_id=str(uuid.uuid4())
        )
        
        tools_data = response.get("result", {}).get("tools", [])
        tools = []
        for t in tools_data:
            # Extract known fields and pass the rest as kwargs
            tool_kwargs = dict(t)
            name = tool_kwargs.pop("name", "")
            description = tool_kwargs.pop("description", "")
            tools.append(Tool(name=name, description=description, **tool_kwargs))
        
        # Return tools directly wrapped in a simple object
        class ToolsResult:
            def __init__(self, tools):
                self.tools = tools
        
        return ToolsResult(tools)
    
    async def call_tool(self, params: 'CallToolParams'):
        """Call tool via MCP session."""
        await self._initialize_session()
        
        response = await self._send_request(
            method="tools/call",
            params={
                "name": params.name,
                "arguments": params.arguments
            },
            request_id=str(uuid.uuid4())
        )
        
        result_data = response.get("result", {})
        content = []
        
        # Handle different response formats
        if "content" in result_data:
            for item in result_data["content"]:
                if item.get("type") == "text":
                    content.append(TextContent(item.get("text", "")))
        elif "text" in result_data:
            content.append(TextContent(result_data["text"]))
        elif isinstance(result_data, str):
            content.append(TextContent(result_data))
        
        return CallToolResult(content)
    
    async def close(self):
        """Close the HTTP session and connector."""
        if self.http_session:
            await self.http_session.close()
            self.http_session = None
        if self.connector:
            await self.connector.close()
            self.connector = None
        self.session_initialized = False
        self.mcp_session_id = None

class StreamableClientTransport:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

class Implementation:
    """Client implementation metadata for MCP protocol identification.
    
    This class stores client identification information that gets sent to the MCP server
    during the initialization handshake as part of the 'clientInfo' field.
    """
    def __init__(self, name: str, version: str):
        self.name = name      # Client name (e.g., "mcp-test-client")
        self.version = version # Client version (e.g., "1.0.0")

class Client:
    def __init__(self, implementation, options=None):
        self.implementation = implementation
        self.options = options
    
    async def connect(self, transport, options):
        return ClientSession(transport.endpoint)


# Module logger following repository standard pattern
logger = logging.getLogger(__name__)


def get_logger() -> logging.Logger:
    """Get the module logger for MCP operations."""
    return logger


def new_client(name: str, version: str) -> Client:
    """Create an MCP client."""
    implementation = Implementation(name=name, version=version)
    return Client(implementation, None)


async def connect(client: Client, url: str) -> ClientSession:
    """Establish a connection to an MCP server."""
    transport = StreamableClientTransport(endpoint=url)
    return await client.connect(transport, None)


async def list_tools(session: ClientSession) -> List[Tool]:
    """Return available tools from the server."""
    result = await session.list_tools(None)
    return result.tools


async def call_tool(session: ClientSession, name: str, args: Dict[str, Any]) -> CallToolResult:
    """Invoke a tool on the server."""
    params = CallToolParams(name=name, arguments=args)
    return await session.call_tool(params)


def print_tool_result(result: CallToolResult) -> None:
    """Log text content from a tool result."""
    log = get_logger()
    
    for content in result.content:
        if isinstance(content, TextContent):
            log.info(content.text)