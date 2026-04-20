# Instrumentation Examples

This directory contains examples demonstrating automatic instrumentation of agent frameworks with the IoC CFN MAS Client.

## A2A (Agent-to-Agent) Instrumentation

The `a2a/` directory shows how to automatically instrument Google A2A agents using monkey patching.

### Prerequisites

**Requires Python >= 3.10** (a2a-sdk constraint)

```bash
pip install ioc_cfn_mas_client_lib
pip install a2a-sdk[http-server]  # Latest: 0.3.26
```

### Running the Multi-Agent Example

This example demonstrates two agents communicating via A2A protocol, with automatic CFN instrumentation on both sides:

**Terminal 1** - Start Agent B (Trend Analyzer Server):

```bash
uv run python examples/instrumentation/a2a/multi_agent_example.py --server
```

**Terminal 2** - Run Agent A (Query Client):

```bash
uv run python examples/instrumentation/a2a/multi_agent_example.py --client
```

### What Gets Instrumented

- **Agent A (Client)**: Input queries and final outputs are logged
- **Agent B (Server)**: Incoming messages and task completions are logged

Both agents will print `[CFN]` log messages showing:

- `Query from shared memory` - when reading input
- `Update to shared memory` - when writing output

These logs demonstrate where the actual CFN API calls would occur in production (currently using mock endpoints for testing).

### How It Works

The instrumentation uses monkey patching to automatically wrap `AgentExecutor.execute()` methods:

```python
from ioc_cfn_mas_client import Client, A2AInstrumentor

# Initialize CFN client
cfn_client = Client(cfn_url="http://localhost:9002")

# Apply instrumentation (monkey patching)
instrumentor = A2AInstrumentor(
    client=cfn_client,
    workspace_id="demo-workspace",
    mas_id="my-mas-id",
)
instrumentor.instrument()

# Now all AgentExecutor.execute() calls are automatically tracked!
```

No decorators required - all agents inheriting from `AgentExecutor` are automatically instrumented after calling `instrumentor.instrument()`.
