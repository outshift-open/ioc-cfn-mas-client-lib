# Claude Code Instructions

## Project Type
This is a **Python SDK library** for IoC CFN MAS Multi-Agent System. It is NOT a service - no Docker, Helm, or K8s deployments.

## Critical Rules

### ⚠️ DO NOT EDIT
- **`src/generated/`** - OpenAPI-generated code. Regenerate with `make gen-openapi` instead.

### ✅ DO EDIT
- **`src/ioc_cfn_mas_client/client.py`** - Main SDK interface
- **`examples/*.py`** - Usage examples
- **`tests/*.py`** - Test files
- **`README.md`** - User documentation

## Quick Reference

### Repository Structure
```
src/ioc_cfn_mas_client/client.py   # Main Client class (hand-written)
src/generated/                      # OpenAPI-generated code (auto-generated)
examples/example.py                 # Usage examples
openapi/public-api-v1.0.yaml        # API spec (copied from ioc-cfn-svc)
```

### Key Facts
- **Package Manager**: `uv` (not pip/poetry)
- **Python Versions**: 3.9, 3.10, 3.11, 3.12
- **Environment Variable**: `CFN_BASE_URL` (NOT `IoC_BASE_URL`)
- **Generated Code Path**: `src/generated/` (NOT `src/ioc_cfn_mas_client/generated/`)
- **Import Pattern**: `from generated.api.shared_memories_api import ...`
- **OpenAPI Source**: [ioc-cfn-svc/docs/public-api/public-api-v1.0.yaml](https://github.com/cisco-eti/ioc-cfn-svc/blob/main/docs/public-api/public-api-v1.0.yaml)

### Common Commands
```bash
# Setup
uv venv && source .venv/bin/activate && uv pip install -e ".[dev]"

# Test
./scripts/unit-test.sh

# Regenerate OpenAPI client (requires Docker)
make gen-openapi

# Pull OpenAPI generator Docker image
make pull-openapi-generator

# Run example
uv run python examples/example.py
```

### CI Pipeline
- **Test**: pytest on Python 3.9 with coverage via scripts/unit-test.sh
- **Runners**: Standard GitHub `ubuntu-latest`

### OpenAPI Spec Important Notes
- **Source of Truth**: The spec in [ioc-cfn-svc](https://github.com/cisco-eti/ioc-cfn-svc/blob/main/docs/public-api/public-api-v1.0.yaml) is authoritative
- **Local Copy**: `openapi/public-api-v1.0.yaml` is copied from ioc-cfn-svc for SDK generation
- **DO NOT** edit `openapi/public-api-v1.0.yaml` directly - changes must be made in ioc-cfn-svc
- **Naming Conventions**: The spec follows Python PEP 8 conventions (snake_case methods/fields, PascalCase classes)
- **SDK Generation**: Uses Docker with `openapitools/openapi-generator-cli` (not local brew install)

### Git Commits
- **DO NOT** include `Co-Authored-By: Claude` lines in commit messages
- Keep commit messages clean and conventional

## Architecture

The `Client` class in `src/ioc_cfn_mas_client/client.py` is a user-friendly wrapper that:
1. Centralizes configuration (base_url, timeout, optional api_key)
2. Provides clean, intuitive methods for common operations
3. Exposes underlying generated API for advanced usage

Example:
```python
from ioc_cfn_mas_client.client import Client

client = Client(base_url="http://localhost:9010")

# User-friendly methods
client.create_shared_memories(workspace_id, mas_id, data=data, format="observe-sdk-otel")
client.query_shared_memories(workspace_id, mas_id, intent="Find user preferences", agent_id="agent1")

# Advanced: direct API access
client.shared_memories_api.create_or_update_shared_memories(...)
client.shared_memories_api.fetch_shared_memories(...)
```

## Documentation
For detailed documentation, see [docs/claude/REPOSITORY_SPEC.md](docs/claude/REPOSITORY_SPEC.md)
