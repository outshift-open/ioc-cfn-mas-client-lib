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
openapi/openapi.json                # API spec (source of truth)
```

### Key Facts
- **Package Manager**: `uv` (not pip/poetry)
- **Python Versions**: 3.9, 3.10, 3.11, 3.12
- **Environment Variable**: `CFN_BASE_URL` (NOT `IoC_BASE_URL`)
- **Generated Code Path**: `src/generated/` (NOT `src/ioc_cfn_mas_client/generated/`)
- **Import Pattern**: `from generated.api.shared_memories_api import ...`

### Common Commands
```bash
# Setup
uv venv && source .venv/bin/activate && uv pip install -e ".[dev]"

# Test
./scripts/unit-test.sh

# Regenerate OpenAPI client
make gen-openapi

# Run example
uv run python examples/example.py
```

### CI Pipeline
- **Test**: pytest on Python 3.9 with coverage via scripts/unit-test.sh
- **Runners**: Standard GitHub `ubuntu-latest`

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
client.upsert_memories(workspace_id, system_id, memories=memories, relationships=relationships)
client.search_memories(workspace_id, system_id, query, top_k=5)

# Advanced: direct API access
client.shared_memories_api.api_workspaces_...(...)
```

## Documentation
For detailed documentation, see [docs/claude/REPOSITORY_SPEC.md](docs/claude/REPOSITORY_SPEC.md)
