# ioc-cfn-mas-client-lib

Python SDK client library for IOC CFN MAS Multi-Agent System.

## Overview

This SDK provides:
- **CFN Service Client**: Shared memories and agent coordination
- **Management Plane Functions**: List workspaces and multi-agentic systems

## Installation

```bash
pip install ioc-cfn-mas-client-lib
```

## Configuration

The library accepts configuration through parameters - no environment variables required. You pass settings directly to the client:

```python
from ioc_cfn_mas_client import Client

client = Client(
    base_url="http://localhost:9010",
    api_key="your-api-key"  # Optional
)
```

**For examples and convenience**, you can optionally use `.env` files with `python-dotenv`. See [`examples/README.md`](examples/README.md) for details.

## Quick Start

### CFN Service (Shared Memories)

```python
import os
from ioc_cfn_mas_client import Client

# Create CFN client
client = Client(
    base_url=os.getenv("CFN_BASE_URL", "http://localhost:9010"),
    api_key=os.getenv("CFN_API_KEY"),  # Optional
)

# Upsert shared memories
memories = [
    {"id": "m1", "content": "User prefers dark mode"},
    {"id": "m2", "content": "Last login: 2024-01-15"},
]

response = client.upsert_shared_memories(
    workspace_id="your_workspace_id",
    system_id="your_system_id",
    memories=memories,
)

# Query shared memories
results = client.query_shared_memories(
    workspace_id="your_workspace_id",
    system_id="your_system_id",
    query="user preferences",
    top_k=5,
)
```

### Management Plane (List Workspaces & MAS)

```python
from ioc_cfn_mas_client import list_workspaces, list_mas

# List all workspaces
workspaces = list_workspaces(
    mgmt_base_url="http://localhost:8080",
    api_key="your-api-key"
)

for workspace in workspaces['workspaces']:
    print(f"{workspace['name']}: {workspace['id']}")

# List multi-agentic systems in a workspace
systems = list_mas(
    mgmt_base_url="http://localhost:8080",
    api_key="your-api-key",
    workspace_id="workspace-uuid"
)

for mas in systems['systems']:
    print(f"{mas['name']}: {mas['id']}")
```

## Complete Example

```python
from ioc_cfn_mas_client import Client, list_workspaces, list_mas

# Get workspace and MAS info from Management Plane
workspaces = list_workspaces("http://localhost:8080", "your-api-key")
workspace_id = workspaces['workspaces'][0]['id']

systems = list_mas("http://localhost:8080", "your-api-key", workspace_id)
mas_id = systems['systems'][0]['id']

# Use CFN client for shared memories
cfn = Client(base_url="http://localhost:9010")

memories = [{"id": "m1", "content": "System initialized"}]
cfn.upsert_shared_memories(workspace_id, mas_id, memories)

results = cfn.query_shared_memories(workspace_id, mas_id, "system", top_k=5)
```

## API Reference

### CFN Client

#### `Client(base_url, api_key=None, **kwargs)`

Main client for CFN service operations.

**Parameters:**
- `base_url` (str, required): CFN API base URL (e.g., `"http://localhost:9010"`)
- `api_key` (str, optional): API key for authentication
- `api_key_name` (str, optional): Header name (default: `"Authorization"`)
- `api_key_prefix` (str, optional): Token prefix (default: `"Bearer"`)
- `timeout` (float, optional): Request timeout in seconds
- `debug` (bool, optional): Enable debug logging

**Methods:**
- `upsert_shared_memories(workspace_id, system_id, memories)`: Upsert memories
- `query_shared_memories(workspace_id, system_id, query, top_k=5)`: Query memories

### Management Plane Functions

#### `list_workspaces(mgmt_base_url, api_key, timeout=None)`

List all workspaces.

**Parameters:**
- `mgmt_base_url` (str): Management Plane base URL (e.g., `"http://localhost:8080"`)
- `api_key` (str): API key for X-API-Key header authentication
- `timeout` (float, optional): Request timeout in seconds

**Returns:** Dict with `'workspaces'` list and `'total'` count

#### `list_mas(mgmt_base_url, api_key, workspace_id, timeout=None)`

List multi-agentic systems in a workspace.

**Parameters:**
- `mgmt_base_url` (str): Management Plane base URL
- `api_key` (str): API key for X-API-Key header authentication
- `workspace_id` (str): UUID of the workspace
- `timeout` (float, optional): Request timeout in seconds

**Returns:** Dict with `'systems'` list and `'total'` count


## Examples

See the [`examples/`](examples/) directory for complete examples with setup instructions:
- [`example.py`](examples/example.py) - CFN service usage
- [`simple_mgmt_example.py`](examples/simple_mgmt_example.py) - Management Plane functions

**Running examples:**
```bash
# See examples/README.md for setup
cd examples
cp .env.example .env  # Configure your settings
cd ..
python examples/example.py
```

## Development

### Setup (macOS)

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install -e ".[dev,examples]"  # Include 'examples' for python-dotenv

# Configure examples (see examples/README.md for details)
cd examples && cp .env.example .env && cd ..
# Edit examples/.env with your configuration

# Run examples
python examples/example.py
python examples/simple_mgmt_example.py
```

### Running Tests

```bash
./scripts/unit-test.sh
```

## OpenAPI Code Generation

The CFN client is generated from OpenAPI specifications.

### Prerequisites (macOS)

```bash
brew install openapi-generator
```

### Generate Clients

```bash
# Generate both CFN and Management Plane clients
make gen-openapi

# Or generate individually
make gen-cfn
make gen-management-plane
```

**OpenAPI specs:**
- CFN: `openapi/cfn.json`
- Management Plane: `openapi/management-plane.json`

**Generated output:**
- `src/generated/cfn/`
- `src/generated/management_plane/`

## Architecture

```
┌─────────────────────────────────────────────┐
│         ioc_cfn_mas_client Package          │
├─────────────────────────────────────────────┤
│                                             │
│  Client (CFN Service)                       │
│  └─ Shared Memories API                     │
│     ├─ upsert_shared_memories()             │
│     └─ query_shared_memories()              │
│                                             │
│  Management Plane Functions                 │
│  ├─ list_workspaces()                       │
│  └─ list_mas()                              │
│                                             │
└─────────────────────────────────────────────┘
```

**Design Philosophy:**
- **Simple**: Two simple functions for Management Plane
- **No dependencies**: Uses Python stdlib only
- **Clean separation**: CFN client and Management Plane functions are independent
- **Easy to use**: Import what you need, when you need it

## License

See [LICENSE](LICENSE) file for details.
