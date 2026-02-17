# ioc-cfn-mas-client-lib

Python SDK client library for IOC CFN MAS\.

## Overview

This repository contains:

- `src/ioc_cfn_mas_client/client.py`: a small, user\-facing `Client` wrapper\.
- `src/generated/`: OpenAPI\-generated code \(implementation detail\)\. Avoid editing generated files directly\.

## Installation

```bash
pip install ioc_cfn_mas_client_lib
```

## Quick start

Create a client using the base URL \(and optionally an API key\):

```python
import os
from ioc_cfn_mas_client.client import Client

client = Client(
    base_url=os.getenv("CFN_BASE_URL", "http://localhost:9010"),
    api_key=os.getenv("CFN_API_KEY"),  # Optional
)
```

### Using the Shared Memories API

```python
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

### Advanced Usage

For power users who need direct access to the generated OpenAPI client:

```python
# Access the underlying API client
api = client.shared_memories_api
response = api.api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_post_with_http_info(...)
```

For a complete example, see `examples/example.py`\.

## Configuration

The `Client` constructor accepts the following parameters:

- `base_url` \(required\): API base URL \(e\.g\., `http://localhost:9010`\)
- `api_key` \(optional\): API key or token \(required only if your deployment enforces auth\)
- `api_key_name` \(optional\): Header name for API key \(default: `"Authorization"`\)
- `api_key_prefix` \(optional\): Prefix for API key value \(default: `"Bearer"`\)
- `timeout` \(optional\): Request timeout in seconds
- `debug` \(optional\): Enable debug mode \(default: `False`\)
- `configuration` \(optional\): Pre\-configured `Configuration` object from generated client
- `api_client` \(optional\): Pre\-configured `ApiClient` object from generated client

### Environment variables

The example code uses:

- `CFN_BASE_URL`: API base URL \(defaults to `http://localhost:9010` if not set\)

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

- OpenAPI spec: `openapi/openapi.json`
- Generated output: `src/generated/`

### Prerequisites (macOS)

```bash
brew update
brew install openapi-generator
openapi-generator version
```

If `make gen-openapi` cannot locate the binary:

```bash
export OPENAPI_GENERATOR=/opt/homebrew/bin/openapi-generator
```

### Generate

```bash
make gen-openapi
```

This regenerates `src/generated/` from `openapi/openapi.json`\.