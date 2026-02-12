# ioc-cfn-mas-client-lib

Python SDK client library for IOC CFN MAS\.

## Overview

This repository contains:

- `src/ioc_cfn_mas_client/client.py`: a small, user\-facing `Client` wrapper\.
- `src/ioc_cfn_mas_client/generated/`: OpenAPI\-generated code \(implementation detail\)\. Avoid editing generated files directly\.

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
    base_url=os.getenv("IOC_BASE_URL", "http://localhost:9010"),
    api_key=os.getenv("IOC_API_KEY"),
)
```

For additional usage examples, see `examples/example.py`\.

## Configuration

Supported environment variables:

- `IOC_BASE_URL`: API base URL \(for example, `http://localhost:8080`\)
- `IOC_API_KEY`: API key or token \(optional; required only if your deployment enforces auth\)
- `IOC_WORKSPACE_ID`: workspace ID used by examples \(optional\)
- `IOC_SYSTEM_ID`: system ID used by examples \(optional\)

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
- Generated output: `src/ioc_cfn_mas_client/generated/`

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

This regenerates `src/ioc_cfn_mas_client/generated/` from `openapi/openapi.json`\.