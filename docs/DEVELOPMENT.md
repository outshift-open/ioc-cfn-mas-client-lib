# Development Guide

This guide covers the development workflow for contributors to the IOC CFN MAS Client Library.

## Table of Contents

- [Setup](#setup)
- [OpenAPI SDK Generation](#openapi-sdk-generation)
- [Testing](#testing)
- [Building and Publishing](#building-and-publishing)

## Setup

### Development Environment (macOS)

Using `uv`:

```bash
# Create virtual environment
uv venv

# Activate the environment
source .venv/bin/activate

# Install package with dev dependencies
uv pip install -e ".[dev]"
```

### Running Tests

```bash
# Run test suite
uv run pytest

# Run with coverage
uv run pytest --cov
```

### Running Examples

```bash
# Basic client example
uv run python examples/example.py

# L9 protocol message example
uv run python examples/l9_example.py
```

## OpenAPI SDK Generation

The client library code in `src/generated/` is auto-generated from the CFN service's OpenAPI specification.

### Architecture

- **OpenAPI spec source**: [ioc-cfn-svc public-api-v1.2.yaml](https://github.com/outshift-open/ioc-cfn-svc/blob/main/docs/public-api/public-api-v1.2.yaml)
- **Local spec**: `openapi/public-api-v1.2.yaml` (copied from source)
- **Generated output**: `src/generated/`
- **User-facing wrapper**: `src/ioc_cfn_mas_client/client.py`

The spec follows Python naming conventions (snake_case for methods/fields, PascalCase for classes). See [ioc-cfn-svc public API docs](https://github.com/outshift-open/ioc-cfn-svc/tree/main/docs/public-api) for details.

### Prerequisites

**Docker** is required for OpenAPI code generation:

```bash
docker pull openapitools/openapi-generator-cli
```

Or use the make target:

```bash
make pull-openapi-generator
```

### Generating the Client

To regenerate the client code from the OpenAPI spec:

```bash
make gen-openapi
```

This regenerates `src/generated/` from `openapi/public-api-v1.2.yaml` using Docker.

Copyright/license headers are automatically added to generated files as part of the `make gen-openapi` process.

### Updating the OpenAPI Spec

To update to a newer version of the CFN service API:

1. **Copy the latest spec** from ioc-cfn-svc:

   ```bash
   cp /path/to/ioc-cfn-svc/docs/public-api/public-api-v1.2.yaml openapi/
   ```

2. **Regenerate the client**:

   ```bash
   make gen-openapi
   ```

3. **Update `client.py`** if the API surface changed:
   - Check for new endpoints
   - Add convenience methods as needed
   - Update method signatures if parameters changed

4. **Update tests** to cover new functionality

5. **Update examples** if API usage patterns changed

### Working with Generated Code

**Do not edit files in `src/generated/` directly** - they will be overwritten on the next regeneration.

Instead:
- Add convenience methods to `src/ioc_cfn_mas_client/client.py`
- Create helper utilities in separate modules
- Use composition and wrappers to extend functionality

### Advanced Usage

For power users who need direct access to the generated OpenAPI clients:

```python
from ioc_cfn_mas_client.client import Client

client = Client(cfn_url="http://localhost:9002")

# Access the underlying API clients
shared_memories_api = client.shared_memories_api
memory_operations_api = client.memory_operations_api
semantic_alignment_api = client.semantic_alignment_api

# Use generated methods directly
response = shared_memories_api.api_workspaces_workspace_id_multi_agentic_systems_mas_id_shared_memories_post_with_http_info(...)
```

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_client.py

# Run with verbose output
uv run pytest -v

# Run with coverage report
uv run pytest --cov=ioc_cfn_mas_client --cov-report=html
```

### Test Structure

```
tests/
└── test_client.py          # Client wrapper tests
```

## Building and Publishing

### Building the Package

```bash
# Install build tools
pip install build twine

# Build distribution packages
python -m build
```

This creates:
- `dist/ioc_cfn_mas_client_lib-*.whl` (wheel)
- `dist/ioc_cfn_mas_client_lib-*.tar.gz` (source distribution)

### Publishing to PyPI

```bash
# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Publish to PyPI
twine upload dist/*
```

See `.github/workflows/publish.yml` for the automated CI/CD pipeline.

## Code Quality

### Linting

```bash
# Run ruff linter
ruff check .

# Auto-fix issues
ruff check --fix .
```

### Type Checking

```bash
# Run mypy type checker
mypy src/ioc_cfn_mas_client
```

Note: Generated code in `src/generated/` is excluded from linting and type checking.

## Project Structure

```
ioc-cfn-mas-client-lib/
├── src/
│   ├── ioc_cfn_mas_client/
│   │   └── client.py           # Main user-facing Client wrapper
│   └── generated/              # Auto-generated OpenAPI code (DO NOT EDIT)
├── openapi/
│   └── public-api-v1.2.yaml   # OpenAPI spec (copied from ioc-cfn-svc)
├── examples/
│   ├── example.py              # Basic usage example
│   └── l9_example.py          # L9 protocol message example
├── tests/                      # Test suite
├── docs/                       # Documentation
├── pyproject.toml             # Package configuration
└── Makefile                   # Development tasks
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

Copyright (c) 2024-2026 Cisco Systems, Inc. and its affiliates. All rights reserved.

Licensed under the Apache License, Version 2.0. See [LICENSE.md](../LICENSE.md) for details.
