# IoC CFN MAS Client Library - Repository Specification

## Project Overview

**Purpose**: Python SDK client library for IoC CFN MAS (Multi-Agent System)

**Type**: Python library/SDK (not a service or application)

**Package Name**: `ioc_cfn_mas_client_lib`

**Python Version**: 3.9+ (tested on 3.9, 3.10, 3.11, 3.12)

**Package Manager**: `uv` (modern, fast Python package manager)

## Repository Structure

```
.
├── src/
│   ├── ioc_cfn_mas_client/        # User-facing SDK wrapper
│   │   └── client.py              # Main Client class (EDIT THIS)
│   └── generated/                 # OpenAPI-generated code (DO NOT EDIT)
│       ├── api/
│       │   ├── shared_memories_api.py
│       │   ├── memory_operations_api.py
│       │   └── semantic_negotiation_api.py
│       ├── models/
│       ├── api_client.py
│       └── configuration.py
├── examples/
│   └── example.py                 # Usage examples for all APIs
├── tests/                         # Pytest test files
├── scripts/
│   └── unit-test.sh               # Run pytest with coverage
├── openapi/
│   ├── public-api-v1.0.yaml       # OpenAPI spec (copied from ioc-cfn-svc)
│   └── openapi.json               # (Deprecated) Old spec
├── .github/workflows/
│   └── ci.yaml                    # GitHub Actions CI (lint, test, build)
├── pyproject.toml                 # Python project configuration
├── Makefile                       # OpenAPI generation tasks (Docker-based)
└── README.md                      # User documentation
```

## Key Architecture Decisions

### 1. **Generated Code Location**
- **Path**: `src/generated/` (NOT `src/ioc_cfn_mas_client/generated/`)
- **Why**: Keeps generated code separate from hand-written code
- **Rule**: NEVER manually edit files in `src/generated/` - regenerate instead

### 2. **OpenAPI Spec Source of Truth**
- **Authoritative Source**: [ioc-cfn-svc/docs/public-api/public-api-v1.0.yaml](https://github.com/cisco-eti/ioc-cfn-svc/blob/main/docs/public-api/public-api-v1.0.yaml)
- **Local Copy**: `openapi/public-api-v1.0.yaml`
- **Rule**: DO NOT edit local copy - changes must be made in ioc-cfn-svc
- **Naming**: Follows Python PEP 8 conventions (snake_case methods/fields, PascalCase classes)

### 3. **Client Wrapper Pattern**
- **File**: `src/ioc_cfn_mas_client/client.py`
- **Purpose**: User-friendly wrapper around OpenAPI-generated client
- **Design Philosophy**: Provide intuitive, well-documented methods that hide complexity
- **Responsibilities**:
  - Centralize configuration (base_url, timeout)
  - Provide clean methods (e.g., `create_shared_memories()`, `query_shared_memories()`)
  - Return Pydantic response models
  - Expose underlying generated API for advanced usage via properties

### 4. **Import Pattern**
- Generated code is imported as: `from generated.api.shared_memories_api import SharedMemoriesApi`
- This works because `src/` is in the Python path during development

### 5. **No Docker/Kubernetes**
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
uv run python examples/example.py
```

#### Regenerate OpenAPI Client
```bash
# Prerequisites: Docker
docker pull openapitools/openapi-generator-cli
# Or: make pull-openapi-generator

# Generate SDK
make gen-openapi
```

This command:
1. Reads `openapi/public-api-v1.0.yaml`
2. Uses Docker with `openapitools/openapi-generator-cli`
3. Generates Python client code into `src/generated/`
4. Package name: `generated`

#### Update OpenAPI Spec
```bash
# 1. Copy latest spec from ioc-cfn-svc
cp /path/to/ioc-cfn-svc/docs/public-api/public-api-v1.0.yaml openapi/

# 2. Regenerate SDK
make gen-openapi

# 3. Update client.py if API surface changed

# 4. Test
./scripts/unit-test.sh
uv run python examples/example.py
```

### File Editing Guidelines

**ALWAYS EDIT**:
- `src/ioc_cfn_mas_client/client.py` - Main SDK interface
- `examples/*.py` - Usage examples
- `tests/*.py` - Test files
- `README.md` - User documentation
- `pyproject.toml` - Dependencies and config

**NEVER EDIT**:
- `src/generated/**` - Auto-generated from OpenAPI spec
- Regenerate instead using `make gen-openapi`

**EDIT WITH CAUTION**:
- `openapi/public-api-v1.0.yaml` - **DO NOT EDIT** - changes must be made in ioc-cfn-svc
- `.github/workflows/ci.yaml` - CI pipeline
- `Makefile` - Build automation

## API Structure

### Current APIs

#### 1. Shared Memories API
**User-friendly methods**:
- `client.create_shared_memories(workspace_id, mas_id, data, format, agent_id)` - Create/update from trace data
- `client.query_shared_memories(workspace_id, mas_id, intent, agent_id)` - Query using natural language

**Generated methods**:
- `client.shared_memories_api.create_or_update_shared_memories(workspace_id, mas_id, create_or_update_request)`
- `client.shared_memories_api.fetch_shared_memories(workspace_id, mas_id, query_request)`
- `client.shared_memories_api.onboard_vector_store(workspace_id, onboard_vector_store_request)`

#### 2. Memory Operations API
**User-friendly methods**:
- `client.memory_operation(workspace_id, mas_id, agent_id, http_method, http_url, http_body)` - Proxy to remote memory providers

**Generated methods**:
- `client.memory_operations_api.memory_operations(workspace_id, mas_id, agent_id, memory_operation_request)`

#### 3. Semantic Negotiation API
**User-friendly methods**:
- `client.start_negotiation(workspace_id, mas_id, session_id, agents, content_text, n_steps)` - Start negotiation
- `client.advance_negotiation(workspace_id, mas_id, session_id, agent_replies)` - Advance with agent replies

**Generated methods**:
- `client.semantic_negotiation_api.start_semantic_negotiation(workspace_id, mas_id, start_request)`
- `client.semantic_negotiation_api.decide_semantic_negotiation(workspace_id, mas_id, decide_request)`

### Response Models

All methods return Pydantic models with proper attributes:
- `CreateOrUpdateResponse`: `.status`, `.response_id`, `.message`
- `QueryResponse`: `.response_id`, `.message`
- `MemoryOperationResponse`: `.http_status`, `.http_response_body`, `.http_headers`
- `NegotiationResponse`: `.status`, `.message`, `.result`

### Advanced Access (for power users)
Direct access to generated APIs:
- `client.shared_memories_api` - SharedMemoriesApi
- `client.memory_operations_api` - MemoryOperationsApi
- `client.semantic_negotiation_api` - SemanticNegotiationApi
- `client.api_client` - ApiClient
- `client.configuration` - Configuration

### Adding New APIs
When the OpenAPI spec is updated with new endpoints:
1. Update spec in [ioc-cfn-svc repository](https://github.com/cisco-eti/ioc-cfn-svc)
2. Copy updated spec: `cp /path/to/ioc-cfn-svc/docs/public-api/public-api-v1.0.yaml openapi/`
3. Run `make gen-openapi`
4. Update `src/ioc_cfn_mas_client/client.py` to expose new methods
5. Add examples in `examples/`
6. Update `README.md` with usage documentation

## Configuration

### Client Constructor Parameters
- `base_url` (required): API endpoint (e.g., `http://localhost:9010`)
- `timeout` (optional): Request timeout in seconds
- `configuration` (optional): Pre-configured Configuration object
- `api_client` (optional): Pre-configured ApiClient object

### Environment Variables
- `CFN_BASE_URL`: API base URL (used in examples, defaults to `http://localhost:9010`)

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
- `pydantic>=2.5` - Data validation (used by generated code)
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
- `tests/` directory

### Testing Approach
- Unit tests for `Client` class
- Integration tests for API calls (may require mocking)
- Coverage target: Aim for >80% on hand-written code (not generated)

### Running Tests
```bash
uv run pytest tests/ -v --cov=ioc_cfn_mas_client --cov-report=term-missing
```

## Common Patterns

### Creating a Client
```python
from ioc_cfn_mas_client.client import Client

client = Client(base_url="http://localhost:9010")
```

### Using the User-Friendly API

#### Create Shared Memories from Trace Data
```python
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
    workspace_id="workspace_id",
    mas_id="mas_id",
    data=trace_data,
    format="observe-sdk-otel",
    agent_id="agent1",
)

print(response.status)
print(response.response_id)
print(response.message)
```

#### Query Shared Memories
```python
response = client.query_shared_memories(
    workspace_id="workspace_id",
    mas_id="mas_id",
    intent="Find information about user login events",
    agent_id="agent1",
    additional_context=[{"context": "authentication patterns"}],
)

print(response.response_id)
print(response.message)
```

#### Memory Operations (Proxy)
```python
# GET from remote provider
response = client.memory_operation(
    workspace_id="ws1",
    mas_id="sys1",
    agent_id="agent1",
    http_method="GET",
    http_url="v1/memories/?user_id=test-user",
)

print(response.http_status)
print(response.http_response_body)
```

#### Semantic Negotiation
```python
# Start negotiation
response = client.start_negotiation(
    workspace_id="ws1",
    mas_id="sys1",
    session_id="session-123",
    agents=[
        {"id": "agent1", "name": "Planner Agent"},
        {"id": "agent2", "name": "Executor Agent"}
    ],
    content_text="Plan a deployment strategy",
    n_steps=10,
)

print(response.status)
print(response.message)
if response.result:
    print(response.result)
```

### Advanced Usage - Direct API Access
For power users needing full control:
```python
# Access the underlying generated API
api = client.shared_memories_api

# Use generated method directly
from generated.models.create_or_update_request import CreateOrUpdateRequest
from generated.models.header import Header
from generated.models.extraction_payload import ExtractionPayload

request = CreateOrUpdateRequest(
    header=Header(agent_id="agent1"),
    payload=ExtractionPayload(data=data, metadata=metadata)
)

response = api.create_or_update_shared_memories(
    workspace_id="ws1",
    mas_id="sys1",
    create_or_update_request=request,
)
```

### Adding New User-Friendly Methods
When adding new operations, follow this pattern in `Client` class:
1. Use clear, descriptive method names (verbs + nouns)
2. Add comprehensive docstrings with examples
3. Use explicit parameters (not generic `body` dicts)
4. Return Pydantic models (not HTTP info tuples)
5. Keep the underlying generated API accessible for advanced usage

Example:
```python
def create_shared_memories(
    self,
    workspace_id: str,
    mas_id: str,
    data: Dict[str, Any],
    format: str,
    agent_id: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Any:
    """Create or update shared memories from trace or OpenClaw output.

    Args:
        workspace_id: The workspace identifier
        mas_id: The multi-agent system identifier
        data: The extraction payload data
        format: Data format ("observe-sdk-otel" or "openclaw")
        agent_id: Optional agent identifier
        request_id: Optional request identifier

    Returns:
        CreateOrUpdateResponse with status and message

    Example:
        >>> response = client.create_shared_memories(
        ...     workspace_id="ws1",
        ...     mas_id="sys1",
        ...     data=[{"TraceId": "...", "SpanId": "..."}],
        ...     format="observe-sdk-otel",
        ...     agent_id="agent1"
        ... )
    """
    metadata = ExtractionPayloadMetadata(format=format)
    payload = ExtractionPayload(data=data, metadata=metadata)
    header = Header(agent_id=agent_id) if agent_id else None

    request = CreateOrUpdateRequest(
        header=header,
        payload=payload,
        request_id=request_id
    )

    return self._shared_memories_api.create_or_update_shared_memories(
        workspace_id=workspace_id,
        mas_id=mas_id,
        create_or_update_request=request,
    )
```

## Troubleshooting

### Import Errors
- Ensure `uv pip install -e ".[dev]"` was run
- Check that you're in the activated virtual environment
- Verify `src/` is in Python path

### OpenAPI Generation Issues
- Ensure Docker is installed: `docker --version`
- Pull generator image: `make pull-openapi-generator`
- Check `openapi/public-api-v1.0.yaml` is valid YAML

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
- **OpenAPI Spec**: Maintained in [ioc-cfn-svc](https://github.com/cisco-eti/ioc-cfn-svc/tree/main/docs/public-api)
- **Issues**: Report in GitHub Issues

## Quick Reference for Claude

When helping with this repository:
1. **This is a library, not a service** - No Docker/K8s deployment
2. **Don't edit `src/generated/`** - Regenerate from OpenAPI spec using Docker
3. **Main file to edit**: `src/ioc_cfn_mas_client/client.py`
4. **Use `uv` commands** for package management
5. **Environment variable**: `CFN_BASE_URL` (not `IoC_BASE_URL`)
6. **Generated code location**: `src/generated/` (not `src/ioc_cfn_mas_client/generated/`)
7. **OpenAPI spec source**: [ioc-cfn-svc/docs/public-api/public-api-v1.0.yaml](https://github.com/cisco-eti/ioc-cfn-svc/blob/main/docs/public-api/public-api-v1.0.yaml)
8. **SDK generation**: Docker-based, not local brew install
9. **Naming conventions**: PEP 8 (snake_case methods, PascalCase classes)
10. **Response types**: Pydantic models with direct attribute access
11. **CI runs**: unit tests on Python 3.9 via scripts/unit-test.sh
12. **Git commits**: Do NOT include `Co-Authored-By: Claude` lines
