# Internet of Cognition (IOC) - Cognition Fabric Node (CFN) MAS Client Library

[![PyPI version](https://badge.fury.io/py/ioc-cfn-mas-client-lib.svg)](https://badge.fury.io/py/ioc-cfn-mas-client-lib)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Python SDK client library for the Internet of Cognition (IoC) Cognition Fabric Node.

## Overview

This library provides a Python client for interacting with the CFN (Cognition Fabric Node) service, enabling:

- **Shared Memories API**: Create and query shared memories from trace data
- **Memory Operations API**: Proxy memory operations to remote providers (Mem0, Graphiti)
- **Semantic Alignment API**: Run multi-agent alignment sessions
- **MCP Integration**: Retain and recall memories using Model Context Protocol
- **A2A Instrumentation**: Automatic tracking of Google A2A protocol agents

## Installation

**Requires Python >= 3.10**

```bash
pip install ioc-cfn-mas-client-lib
```

## Quick Start

Create a client using the CFN URL:

```python
from ioc_cfn_mas_client.client import Client

client = Client(cfn_url="http://localhost:9002")
```

### Shared Memories API

#### Create or update shared memories from trace data

```python
# Create memories from trace data (e.g., OpenTelemetry traces)
trace_data = [
    {
        "TraceId": "trace-001",
        "SpanId": "span-001",
        "SpanName": "user_login",
        "ServiceName": "auth-service",
        "SpanAttributes": {"user_id": "user123"},
        "Duration": 150
    }
]

response = client.create_shared_memories(
    workspace_id="your_workspace_id",
    mas_id="your_mas_id",
    data=trace_data,
    format="observe-sdk-otel",  # or "openclaw"
    agent_id="your_agent_id",  # Optional
)
```

#### Query shared memories with natural language

```python
# Query memories using natural language intent
results = client.query_shared_memories(
    workspace_id="your_workspace_id",
    mas_id="your_mas_id",
    intent="Find information about user login events",
    agent_id="your_agent_id",
    additional_context=[{"context": "prior conversation"}],  # Optional
)
```

### Memory Operations API (Proxy to Remote Providers)

Forward memory operations to remote providers like Mem0 or Graphiti:

```python
# GET memories from remote provider
response = client.memory_operation(
    workspace_id="your_workspace_id",
    mas_id="your_mas_id",
    agent_id="your_agent_id",
    http_method="GET",
    http_url="v1/memories/?user_id=test-user",
)

# POST memories to remote provider
response = client.memory_operation(
    workspace_id="your_workspace_id",
    mas_id="your_mas_id",
    agent_id="your_agent_id",
    http_method="POST",
    http_url="/v1/memories/",
    http_body={
        "messages": [{"role": "user", "content": "I prefer dark mode"}],
        "user_id": "test-user"
    },
)
```

### Semantic Alignment API

Run multi-agent alignment sessions:

```python
# Start a alignment session
response = client.start_alignment(
    workspace_id="your_workspace_id",
    mas_id="your_mas_id",
    session_id="session-123",
    agents=[
        {"id": "agent1", "name": "Planner Agent"},
        {"id": "agent2", "name": "Executor Agent"}
    ],
    content_text="Plan a deployment strategy",
    n_steps=10,  # Optional, defaults to 20
)

# Advance alignment with agent replies
response = client.advance_alignment(
    workspace_id="your_workspace_id",
    mas_id="your_mas_id",
    session_id="session-123",
    agent_replies=[
        {
            "agent_id": "agent1",
            "action": "counter_offer",
            "offer": {"strategy": "blue-green deployment"}
        },
        {
            "agent_id": "agent2",
            "action": "accept"
        }
    ],
)
```

### Google A2A Protocol Integration

Use `A2AInstrumentor` to automatically track all A2A agents without decorators (monkey patching approach):

```python
from ioc_cfn_mas_client import Client, A2AInstrumentor
from a2a.server.agent_execution import AgentExecutor

client = Client(cfn_url="http://localhost:9002")

# One-time setup - instruments ALL AgentExecutor classes automatically
instrumentor = A2AInstrumentor(
    client=client,
    workspace_id="my-workspace",
    mas_id="my-mas",
    publish_input=True,   # Publish incoming A2A messages
    publish_output=True,  # Publish task results
)
instrumentor.instrument()

# Now ALL agents are automatically tracked - no decorators needed!
class MyA2AAgent(AgentExecutor):
    async def execute(self, context, event_queue):
        """Execute agent - automatically published to CFN."""
        # Your A2A agent logic here
        # All interactions automatically saved to CFN shared memory
        pass
```

**Key Features:**

- **Zero code changes** - works with any A2A agent
- Automatic publishing of A2A messages to CFN shared memory
- Uses monkey patching (similar to OpenTelemetry auto-instrumentation)
- Preserves A2A protocol structure (messages, tasks, artifacts)
- Can be enabled/disabled globally with `uninstrument()`

For detailed documentation, see [docs/A2A_INTEGRATION.md](docs/A2A_INTEGRATION.md).

**Example:**

```bash
# Terminal 1 - Start Agent B server
uv run python examples/instrumentation/a2a/multi_agent_example.py --server

# Terminal 2 - Run Agent A client
uv run python examples/instrumentation/a2a/multi_agent_example.py --client
```

See [examples/instrumentation/a2a/multi_agent_example.py](examples/instrumentation/a2a/multi_agent_example.py) for the complete code, and [examples/instrumentation/README.md](examples/instrumentation/README.md) for more details.

### MCP Client Integration

Use the MCP (Model Context Protocol) client methods integrated into the main Client class:

```python
from ioc_cfn_mas_client import Client

# Initialize client with MCP server URL
client = Client(cfn_url="http://localhost:9001")

# Retain shared memories using MCP-style interface
result = await client.retain(
    workspace_id="my-workspace",
    mas_id="my-mas",
    payload={
        "metadata": {"format": "openclaw"},
        "data": [{"example": "conversation data"}]
    },
    agent_id="my-agent"
)
print(f"Retain result: {result['status']}")

# Recall shared memories using natural language intent
result = await client.recall(
    workspace_id="my-workspace",
    mas_id="my-mas",
    intent="Find information about user preferences",
    search_strategy="semantic_graph_traversal",
    agent_id="my-agent"
)
print(f"Recall result: {result['message']}")
```

**Key Features:**

- **Integrated MCP Methods** - `retain()` and `recall()` methods built into the main Client class
- **Mock Responses** - Returns structured mock data for testing without live MCP server
- **OpenClaw Format** - Supports conversation data for retain operations
- **Natural Language Queries** - Use intent-based queries for recall operations
- **Semantic Search** - Built-in semantic graph traversal for memory retrieval

**Examples:**

```bash
# Run the MCP client example demonstrating retain/recall methods
uv run python examples/mcp/client_example.py

# For direct MCP protocol testing (advanced users):
uv run python -m src.ioc_cfn_mas_client.mcp.mcp_client_sample --operation list_tools
uv run python -m src.ioc_cfn_mas_client.mcp.mcp_client_sample --operation retain
uv run python -m src.ioc_cfn_mas_client.mcp.mcp_client_sample --operation recall
```

For complete examples and implementation details, see [examples/mcp/client_example.py](examples/mcp/client_example.py) and [src/ioc_cfn_mas_client/mcp/](src/ioc_cfn_mas_client/mcp/).

### Advanced Usage

For power users who need direct access to the generated OpenAPI clients:

```python
# Access the underlying API clients
shared_memories_api = client.shared_memories_api
memory_operations_api = client.memory_operations_api
semantic_alignment_api = client.semantic_alignment_api

# Use generated methods directly
response = shared_memories_api.api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_post_with_http_info(...)
```

For a complete example, see `examples/example.py`.

## Configuration

The `Client` constructor accepts the following parameters:

- `cfn_url` (required): CFN API endpoint URL (e.g., `http://localhost:9002`)
- `timeout` (optional): Request timeout in seconds
- `configuration` (optional): Pre-configured Configuration object (for advanced users)
- `api_client` (optional): Pre-configured ApiClient object (for advanced users)

### Environment Variables

Optional environment variable:

- `CFN_URL`: CFN API endpoint URL (defaults to `http://localhost:9002` if not set)

## Contributing

For development setup, OpenAPI code generation, and contribution guidelines, see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE.md](LICENSE.md) file for full details.

Copyright (c) 2024-2026 Cisco Systems, Inc. and its affiliates. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
