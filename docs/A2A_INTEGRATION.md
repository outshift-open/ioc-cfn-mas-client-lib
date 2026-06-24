# Google A2A Protocol Integration with CFN

This document describes how to use `A2AInstrumentor` to automatically integrate Google's Agent-to-Agent (A2A) protocol with CFN's shared memory system using monkey patching.

## Overview

The `A2AInstrumentor` automatically instruments all A2A agents to publish their interactions to CFN shared memory. No decorators or code changes needed - just call `instrument()` once and all agents are tracked.

## Architecture

```
┌─────────────┐         ┌─────────────┐
│   Agent A   │         │   Agent B   │
│  (A2A SDK)  │         │  (A2A SDK)  │
└──────┬──────┘         └──────┬──────┘
       │                       │
       │  Auto-instrumented    │  Auto-instrumented
       │  (monkey patched)     │  (monkey patched)
       │                       │
       ▼                       ▼
┌─────────────────────────────────────┐
│     CFN Shared Memory API           │
│  (format="openclaw" with A2A data)  │
└─────────────────────────────────────┘
```

### How It Works

1. **Monkey Patching**: `A2AInstrumentor` replaces `AgentExecutor.execute()` with an instrumented version
2. **Transparent**: Your agent code doesn't change - instrumentation happens automatically
3. **Global**: All `AgentExecutor` subclasses are automatically tracked
4. **Reversible**: Call `uninstrument()` to restore original behavior

### Communication Pattern

- **Asynchronous Knowledge Sharing**: Agents publish messages to shared memory
- **Protocol Preservation**: A2A protocol structure is preserved in CFN storage
- **Zero Code Changes**: Works with any existing A2A agent
- **No Direct Coupling**: Agents don't need to know about each other

## Installation

**Requirements:**
- Python >= 3.10

```bash
pip install ioc-cfn-mas-client-lib
```

## Usage

### Basic Example

```python
from ioc_cfn_mas_client import Client, A2AInstrumentor
from a2a.server.agent_execution import AgentExecutor

# Initialize CFN client
client = Client(cfn_url="http://localhost:9002")

# One-time setup - instrument ALL AgentExecutor classes
instrumentor = A2AInstrumentor(
    client=client,
    workspace_id="my-workspace",
    mas_id="my-mas",
    publish_input=True,   # Publish incoming messages
    publish_output=True,  # Publish results
)
instrumentor.instrument()

# Now all agents are automatically tracked - no changes needed!
class MyAgent(AgentExecutor):
    async def execute(self, context, event_queue):
        """Your A2A agent logic here - automatically published to CFN!"""
        message_text = context.message.parts[0].text
        result = f"Processed: {message_text}"
        return result
```

### Multiple Agents Example

```python
# Instrument once at startup
instrumentor = A2AInstrumentor(
    client=client,
    workspace_id="production-workspace",
    mas_id="multi-agent-system",
    publish_input=True,
    publish_output=True,
)
instrumentor.instrument()

# All these agents are automatically tracked!
class TrendAnalyzer(AgentExecutor):
    async def execute(self, context, event_queue):
        return "Analyzing trends..."

class SentimentAnalyzer(AgentExecutor):
    async def execute(self, context, event_queue):
        return "Analyzing sentiment..."

class RecommendationEngine(AgentExecutor):
    async def execute(self, context, event_queue):
        return "Generating recommendations..."

# All interactions automatically published to CFN - zero changes needed!
```

## Data Format

### Storage Format in CFN

Messages are stored using `format="openclaw"` with the following structure:

```json
{
  "protocol": "google-a2a",
  "version": "0.3.0",
  "agent_id": "TrendAnalyzer",
  "message_id": "msg-abc123",
  "task_id": "task-xyz789",
  "context_id": "ctx-456",
  "timestamp": "2026-04-17T12:34:56.789Z",
  "direction": "input",
  "type": "message",
  "data": {
    "role": "ROLE_USER",
    "parts": [
      {
        "text": "What are the trending topics today?"
      }
    ],
    "metadata": {}
  }
}
```

### Message Types

The instrumentor publishes two types of data:

1. **Message** (`type: "message"`) - Incoming A2A messages
2. **Task Completion** (`type: "task_completion"`) - Agent results

## Configuration

### A2AInstrumentor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `client` | `Client` | Required | CFN MAS client instance |
| `workspace_id` | `str` | Required | Workspace identifier |
| `mas_id` | `str` | Required | Multi-agent system identifier |
| `publish_input` | `bool` | `True` | Publish incoming messages |
| `publish_output` | `bool` | `True` | Publish task results |

### Example: Custom Configuration

```python
# Only publish outputs (not inputs)
instrumentor = A2AInstrumentor(
    client=client,
    workspace_id="ws1",
    mas_id="mas1",
    publish_input=False,   # Don't publish inputs
    publish_output=True,   # Only publish outputs
)
instrumentor.instrument()
```

## Advanced Usage

### Uninstrumentation

```python
# Apply instrumentation
instrumentor.instrument()

# ... your agent code runs ...

# Restore original behavior (optional)
instrumentor.uninstrument()
```

### Multiple Workspaces

```python
# Instrument different workspace per environment
import os

environment = os.getenv("ENVIRONMENT", "dev")

instrumentor = A2AInstrumentor(
    client=client,
    workspace_id=f"{environment}-workspace",
    mas_id=f"{environment}-mas",
)
instrumentor.instrument()
```

## Best Practices

### 1. Instrument Early

```python
# Instrument at application startup, before creating agents
def main():
    client = Client(base_url=os.getenv("CFN_URL"))
    instrumentor = A2AInstrumentor(client, "ws1", "mas1")
    instrumentor.instrument()  # Do this first!

    # Now create and run agents
    run_agents()
```

### 2. Use Environment Variables

```python
# Configuration from environment
client = Client(cfn_url=os.getenv("CFN_URL"))

instrumentor = A2AInstrumentor(
    client=client,
    workspace_id=os.getenv("CFN_WORKSPACE_ID"),
    mas_id=os.getenv("CFN_MAS_ID"),
)
instrumentor.instrument()
```

### 3. Single Instrumentor Instance

```python
# Create once and reuse
_instrumentor = None

def get_instrumentor():
    global _instrumentor
    if _instrumentor is None:
        client = Client(base_url=os.getenv("CFN_URL"))
        _instrumentor = A2AInstrumentor(client, "ws1", "mas1")
        _instrumentor.instrument()
    return _instrumentor
```

## Comparison with Observe Library

The `A2AInstrumentor` follows the same pattern as [Observe SDK](https://github.com/agntcy/observe):

| Feature | Observe SDK | CFN A2AInstrumentor |
|---------|-------------|---------------------|
| **Technology** | OpenTelemetry spans | CFN shared memory |
| **Method** | Monkey patching | Monkey patching |
| **Auto-instrument** | ✅ Yes | ✅ Yes |
| **Zero code changes** | ✅ Yes | ✅ Yes |
| **Backend** | OTLP exporters | CFN HTTP API |

## Troubleshooting

### "A2A SDK not found"

```bash
# Install the SDK (includes A2A dependencies)
pip install ioc-cfn-mas-client-lib
```

### "Already instrumented"

```python
# Only call instrument() once
instrumentor = A2AInstrumentor(...)
instrumentor.instrument()  # First call: OK
instrumentor.instrument()  # Second call: Prints warning and skips
```

### Messages Not Appearing in CFN

1. Verify CFN server is running
2. Verify workspace and MAS exist
3. Check client CFN URL is correct
4. Look for error messages in console output

### Restore Original Behavior

```python
# Uninstrument to restore original AgentExecutor.execute()
instrumentor.uninstrument()
```

## Related Resources

- [Google A2A Protocol Specification](https://github.com/a2aproject/A2A)
- [A2A Python SDK](https://github.com/a2aproject/a2a-python)
- [A2A Samples](https://github.com/a2aproject/a2a-samples)
- [Observe SDK (Similar Approach)](https://github.com/agntcy/observe)
- [CFN API Documentation](./REPOSITORY_SPEC.md)

## Example

See [examples/instrumentation/a2a/multi_agent_example.py](../examples/instrumentation/a2a/multi_agent_example.py) for a complete working example showing:
- Agent B running as an A2A HTTP server
- Agent A calling Agent B
- Automatic CFN instrumentation via monkey patching on both sides
- Real agent-to-agent communication

For more details, see the [examples/instrumentation/README.md](../examples/instrumentation/README.md).

Usage:
```bash
# Terminal 1 - Start Agent B server
python examples/instrumentation/a2a/multi_agent_example.py --server

# Terminal 2 - Run Agent A client
python examples/instrumentation/a2a/multi_agent_example.py --client
```

## Support

For issues or questions:
- SDK Issues: [ioc-cfn-mas-client-lib GitHub Issues](https://github.com/outshift-open/ioc-cfn-mas-client-lib/issues)
- A2A Protocol: [A2A Project Discussions](https://github.com/a2aproject/A2A/discussions)
