# ioc-cfn-mas-client-lib

Python SDK client library for IoC CFN MAS\.

## Overview

This repository contains:

- `src/ioc_cfn_mas_client/client.py`: a small, user\-facing `Client` wrapper\.
- `src/generated/`: OpenAPI\-generated code \(implementation detail\)\. Avoid editing generated files directly\.

## Installation

```bash
pip install ioc_cfn_mas_client_lib
```

**For A2A Instrumentation (requires Python >= 3.10):**
```bash
pip install a2a-sdk[http-server]  # Latest: 0.3.26
```

## Quick start

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

### Semantic Negotiation API

Run multi\-agent negotiation sessions:

```python
# Start a negotiation session
response = client.start_negotiation(
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

# Advance negotiation with agent replies
response = client.advance_negotiation(
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

### Advanced Usage

For power users who need direct access to the generated OpenAPI clients:

```python
# Access the underlying API clients
shared_memories_api = client.shared_memories_api
memory_operations_api = client.memory_operations_api
semantic_negotiation_api = client.semantic_negotiation_api

# Use generated methods directly
response = shared_memories_api.api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_post_with_http_info(...)
```

For a complete example, see `examples/example.py`\.

## Configuration

The `Client` constructor accepts the following parameters:

- `cfn_url` \(required\): CFN API endpoint URL \(e\.g\., `http://localhost:9002`\)
- `timeout` \(optional\): Request timeout in seconds
- `configuration` \(optional\): Pre\-configured Configuration object \(for advanced users\)
- `api_client` \(optional\): Pre\-configured ApiClient object \(for advanced users\)

### Environment variables

Optional environment variable:

- `CFN_URL`: CFN API endpoint URL \(defaults to `http://localhost:9002` if not set\)

## Development (macOS)

Using `uv`:

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Run examples
uv run python examples/example.py
```

## OpenAPI SDK generation

- **OpenAPI spec source**: [ioc-cfn-svc public-api-v1.0.yaml](https://github.com/cisco-eti/ioc-cfn-svc/blob/main/docs/public-api/public-api-v1.0.yaml)
- **Local spec**: `openapi/public-api-v1.0.yaml` (copied from source)
- **Generated output**: `src/generated/`

### Prerequisites

**Docker** (required):

```bash
docker pull openapitools/openapi-generator-cli
```

Or use the make target:

```bash
make pull-openapi-generator
```

### Generate

```bash
make gen-openapi
```

This regenerates `src/generated/` from `openapi/public-api-v1.0.yaml` using Docker.

**Note**: The spec follows Python naming conventions (snake_case for methods/fields, PascalCase for classes). See [ioc-cfn-svc public API docs](https://github.com/cisco-eti/ioc-cfn-svc/tree/main/docs/public-api) for details.

### Updating the spec

To update to a newer version:

1. Copy the latest spec from ioc-cfn-svc:

   ```bash
   cp /path/to/ioc-cfn-svc/docs/public-api/public-api-v1.0.yaml openapi/
   ```

2. Regenerate:

   ```bash
   make gen-openapi
   ```

3. Update `client.py` if the API surface changed\.
