# IOC CFN MAS Client Library - Repository Specification

## Project Overview

**Purpose**: Python SDK client library for IOC CFN MAS (Multi-Agent System)

**Type**: Python library/SDK (not a service or application)

**Package Name**: `ioc_cfn_mas_client_lib`

**Python Version**: 3.9+ (tested on 3.9, 3.10, 3.11, 3.12)

**Package Manager**: `uv` (modern, fast Python package manager)

## Repository Structure

```
.
├── src/
│   ├── ioc_cfn_mas_client/        # User-facing SDK wrapper
│   │   ├── __init__.py            # Package exports
│   │   ├── client.py              # Main CFN Client class (EDIT THIS)
│   │   └── management_plane_client.py  # Management Plane functions (EDIT THIS)
│   └── generated/                 # OpenAPI-generated CFN client (DO NOT EDIT)
│       ├── api/
│       │   └── shared_memories_api.py
│       ├── models/
│       ├── api_client.py
│       └── configuration.py
├── examples/
│   ├── example.py                 # CFN service usage examples
│   └── simple_mgmt_example.py     # Management Plane functions examples
├── tests/                         # Pytest test files
├── scripts/
│   ├── unit-test.sh               # Run pytest with coverage
│   └── lint.sh                    # Run ruff and mypy
├── openapi/
│   └── openapi.json               # CFN API specification (source of truth)
├── .github/workflows/
│   └── ci.yaml                    # GitHub Actions CI (lint, test, build)
├── pyproject.toml                 # Python project configuration
├── Makefile                       # OpenAPI generation tasks
└── README.md                      # User documentation
```

## Key Architecture Decisions

### 1. **Generated Code Location**
- **Path**: `src/generated/` (NOT `src/ioc_cfn_mas_client/generated/`)
- **Why**: Keeps generated code separate from hand-written code
- **Rule**: NEVER manually edit files in `src/generated/` - regenerate instead
- **What's generated**: Only the CFN client - Management Plane functions are hand-written

### 2. **CFN Client Wrapper Pattern**
- **File**: `src/ioc_cfn_mas_client/client.py`
- **Purpose**: User-friendly wrapper around OpenAPI-generated CFN client
- **Design Philosophy**: Provide intuitive, well-documented methods that hide complexity
- **Responsibilities**:
  - Centralize configuration (base_url, api_key, timeout)
  - Provide clean methods with good parameter names (e.g., `upsert_shared_memories()`)
  - Return clean responses (data only, not HTTP info tuples)
  - Expose underlying generated API for advanced usage via properties

### 3. **Management Plane Functions (Simple Approach)**
- **File**: `src/ioc_cfn_mas_client/management_plane_client.py`
- **Purpose**: Two simple functions for listing workspaces and MAS
- **Design Philosophy**: KISS (Keep It Simple, Stupid)
  - No class wrapper - just pure functions
  - Uses Python stdlib only (`urllib.request`) - no external dependencies
  - Each function takes its own parameters (no shared state)
  - X-API-Key authentication via header
  - **NO generated code** - hand-written for simplicity
- **Functions**:
  - `list_workspaces(mgmt_base_url, api_key, timeout=None)`
  - `list_mas(mgmt_base_url, api_key, workspace_id, timeout=None)`
- **Why Simple?**: User only needs 2 basic listing operations - no need for full OpenAPI generation and class wrappers

### 4. **Clean Separation**
- **CFN Service**: For shared memories and agent coordination
- **Management Plane**: For workspace and MAS management
- **No dependencies between them**: Can use one without the other
- **Exported together**: `from ioc_cfn_mas_client import Client, list_workspaces, list_mas`

### 5. **Import Pattern**
- Generated CFN code: `from generated.api.shared_memories_api import SharedMemoriesApi`
- Management Plane functions: `from ioc_cfn_mas_client import list_workspaces, list_mas`
- This works because `src/` is in the Python path during development

### 6. **No Docker/Kubernetes**
- This is a **library**, not a service
- No Dockerfile, no Helm charts, no container deployment
- Distributed via PyPI (or private package registry)

## Development Workflow

### Setup
```bash
uv venv                          # Create virtual environment
source .venv/bin/activate        # Activate it
uv pip install -e ".[dev]"       # Install in editable mode with dev deps
```

### Common Tasks

#### Run Tests
```bash
./scripts/unit-test.sh
# Or manually:
uv run pytest tests/ -v --cov=ioc_cfn_mas_client --cov-report=term-missing
```

#### Run Examples
```bash
# CFN service example
uv run python examples/example.py

# Management Plane functions example
uv run python examples/simple_mgmt_example.py
```

#### Regenerate OpenAPI Client
```bash
# Prerequisites: brew install openapi-generator
make gen-openapi
```

This command:
1. Reads `openapi/openapi.json` (CFN API spec)
2. Generates Python CFN client code into `src/generated/`
3. Package name: `generated`

**Note**: Only the CFN client is generated. Management Plane functions are hand-written.

### File Editing Guidelines

**ALWAYS EDIT**:
- `src/ioc_cfn_mas_client/client.py` - CFN Client wrapper
- `src/ioc_cfn_mas_client/management_plane_client.py` - Management Plane functions
- `examples/*.py` - Usage examples
- `tests/*.py` - Test files
- `README.md` - User documentation
- `pyproject.toml` - Dependencies and config

**NEVER EDIT**:
- `src/generated/**` - Auto-generated CFN client from OpenAPI spec
- Regenerate instead using `make gen-openapi`

**EDIT WITH CAUTION**:
- `openapi/openapi.json` - Source of truth for API, coordinate with backend team
- `.github/workflows/ci.yaml` - CI pipeline
- `Makefile` - Build automation

## API Structure

### Current APIs

**CFN Service (Shared Memories)** - User-friendly methods via Client class:
- `client.upsert_shared_memories(workspace_id, system_id, memories)` - Upsert memory objects
- `client.query_shared_memories(workspace_id, system_id, query, top_k=5)` - Semantic search

**CFN Advanced Access** (for power users):
- `client.shared_memories_api` - Direct access to generated SharedMemoriesApi
  - `api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_post_with_http_info()`
  - `api_workspaces_workspace_id_multi_agentic_systems_system_id_shared_memories_query_post_with_http_info()`

**Management Plane Functions** - Simple standalone functions:
- `list_workspaces(mgmt_base_url, api_key, timeout=None)` - List all workspaces
- `list_mas(mgmt_base_url, api_key, workspace_id, timeout=None)` - List MAS in a workspace

**Design Note**: Management Plane uses simple functions (not class-based) because:
1. No shared state needed between calls
2. Simpler API surface for users
3. Uses Python stdlib only (no external HTTP library dependencies)

### Adding New APIs
When the OpenAPI spec is updated with new endpoints:
1. Update `openapi/openapi.json`
2. Run `make gen-openapi`
3. Update `src/ioc_cfn_mas_client/client.py` to expose the new API group
4. Add examples in `examples/`
5. Update `README.md` with usage documentation

## Configuration

### Client Constructor Parameters
- `base_url` (required): API endpoint (e.g., `http://localhost:9010`)
- `api_key` (optional): Authentication token
- `api_key_name` (optional): Header name, default `"Authorization"`
- `api_key_prefix` (optional): Token prefix, default `"Bearer"`
- `timeout` (optional): Request timeout in seconds
- `debug` (optional): Enable debug logging
- `configuration` (optional): Pre-configured `Configuration` object
- `api_client` (optional): Pre-configured `ApiClient` object

### Environment Variables
**CFN Service**:
- `CFN_BASE_URL`: CFN API base URL (used in examples, defaults to `http://localhost:9010`)
- `CFN_API_KEY`: Optional API key for CFN authentication

**Management Plane**:
- `MANAGEMENT_PLANE_BASE_URL`: Management Plane base URL (defaults to `http://localhost:8080`)
- `API_KEY`: API key for Management Plane X-API-Key header authentication

## CI/CD Pipeline

**GitHub Actions Workflow**: `.github/workflows/ci.yaml`

**Jobs**:
1. **Test**: Runs pytest with coverage on Python 3.9 via `scripts/unit-test.sh`
2. **CI Status**: Aggregates results for PR status checks

**Triggers**:
- Push to `main` branch
- Pull requests to `main`
- Manual workflow dispatch

**Runners**: Standard GitHub `ubuntu-latest` (no custom runners)

**Action Versions**: Uses version tags (e.g., `@v4`, `@v5`, `@v6`) instead of commit hashes for maintainability

## Dependencies

### Runtime Dependencies
- `pydantic>=2.5` - Data validation
- `urllib3>=1.26` - HTTP client
- `python-dateutil>=2.8` - Date/time utilities
- `typing-extensions>=4.7` - Type hints backport

### Development Dependencies
- `pytest>=7.4` - Testing framework
- `pytest-cov>=4.1` - Coverage reporting
- `ruff>=0.4` - Linting and formatting
- `mypy>=1.8` - Static type checking

## Testing Strategy

### Test Location
- `tests/` directory (currently exists but may need test files)

### Testing Approach
- Unit tests for `Client` class
- Integration tests for API calls (may require mocking)
- Coverage target: Aim for >80% on hand-written code (not generated)

### Running Tests
```bash
uv run pytest tests/ -v --cov=ioc_cfn_mas_client --cov-report=term-missing
```

## Common Patterns

### CFN Service - Creating a Client
```python
from ioc_cfn_mas_client import Client

client = Client(
    base_url="http://localhost:9010",
    api_key="your-api-key",  # Optional
)
```

### CFN Service - Using the User-Friendly API
```python
# Upsert memories - clean, intuitive interface
memories = [
    {"id": "m1", "content": "User prefers dark mode"},
    {"id": "m2", "content": "Last login: 2024-01-15"},
]
response = client.upsert_shared_memories(
    workspace_id="workspace_id",
    system_id="system_id",
    memories=memories,
)

# Query memories - semantic search
results = client.query_shared_memories(
    workspace_id="workspace_id",
    system_id="system_id",
    query="user preferences",
    top_k=5,
)
```

### Management Plane - List Workspaces and MAS
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

### Complete Workflow - Using Both Services
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

### Advanced Usage - Direct API Access
For power users needing full control:
```python
# Access the underlying generated API
api = client.shared_memories_api
response = api.api_workspaces_workspace_id_...(
    workspace_id="workspace_id",
    system_id="system_id",
    body={"key": "value"},
)
```

### Adding New User-Friendly Methods
When adding new operations, follow this pattern in `Client` class:
1. Use clear, descriptive method names (verbs + nouns)
2. Add comprehensive docstrings with examples
3. Use explicit parameters (not generic `body` dicts)
4. Return clean data (unwrap HTTP info tuples)
5. Keep the underlying generated API accessible for advanced usage

Example:
```python
def upsert_shared_memories(
    self,
    workspace_id: str,
    system_id: str,
    memories: List[Dict[str, Any]],
) -> Any:
    """Upsert (insert or update) shared memories.

    Args:
        workspace_id: The workspace identifier
        system_id: The multi-agent system identifier
        memories: List of memory objects with 'id' and 'content'

    Returns:
        API response with upsert results

    Example:
        >>> memories = [{"id": "m1", "content": "hello"}]
        >>> client.upsert_shared_memories("ws1", "sys1", memories)
    """
    body = {"memories": memories}
    response = self._shared_memories_api.api_workspaces_...(
        workspace_id=workspace_id,
        system_id=system_id,
        body=body,
    )
    return response[0]  # Return data only, not HTTP info
```

## Troubleshooting

### Import Errors
- Ensure `uv pip install -e ".[dev]"` was run
- Check that you're in the activated virtual environment
- Verify `src/` is in Python path

### OpenAPI Generation Issues
- Ensure `openapi-generator` is installed: `brew install openapi-generator`
- Set `OPENAPI_GENERATOR` env var if needed: `export OPENAPI_GENERATOR=/opt/homebrew/bin/openapi-generator`
- Check `openapi/openapi.json` is valid JSON

### Test Failures
- Ensure all dependencies installed: `uv pip install -e ".[dev]"`
- Check if tests require API server running (mock if needed)

## Git Workflow

### Commit Messages
- Keep commit messages clean and conventional
- **DO NOT** include `Co-Authored-By: Claude` lines in commit messages
- Follow conventional commit format when appropriate (e.g., `feat:`, `fix:`, `chore:`)

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` (if exists)
3. Run tests: `./scripts/unit-test.sh`
4. Build package: `uv run python -m build`
5. Publish to PyPI: `uv run twine upload dist/*` (if configured)

## Contact & Resources

- **Repository**: cisco-eti/ioc-cfn-mas-client-lib
- **Main Branch**: `main`
- **OpenAPI Spec**: Backend team maintains source of truth
- **Issues**: Report in GitHub Issues

## Quick Reference for Claude

When helping with this repository:
1. **This is a library, not a service** - No Docker/K8s needed
2. **Don't edit `src/generated/`** - Regenerate CFN client from OpenAPI spec
3. **Main files to edit**:
   - `src/ioc_cfn_mas_client/client.py` - CFN Client wrapper
   - `src/ioc_cfn_mas_client/management_plane_client.py` - Management Plane functions (hand-written, NOT generated)
4. **Two services, clean separation**:
   - CFN Service: For shared memories (class-based Client wrapping generated code)
   - Management Plane: For workspaces/MAS (simple hand-written functions)
5. **Use `uv` commands** for package management
6. **Environment variables**:
   - `CFN_BASE_URL` (not `IOC_BASE_URL`) for CFN service
   - `MANAGEMENT_PLANE_BASE_URL` and `API_KEY` for Management Plane
7. **Generated code location**: `src/generated/` (CFN only, not Management Plane)
8. **CI runs**: lint + unit tests on Python 3.9-3.12
9. **Git commits**: Do NOT include `Co-Authored-By: Claude` lines
10. **Design philosophy**: Keep Management Plane simple (no generation, no class, stdlib only)
