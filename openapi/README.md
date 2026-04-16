# OpenAPI Specification

This directory contains the OpenAPI specification for the IoC CFN MAS API.

## Files

- **`public-api-v1.0.yaml`**: Official OpenAPI 3.0 spec from [ioc-cfn-svc](https://github.com/cisco-eti/ioc-cfn-svc/blob/main/docs/public-api/public-api-v1.0.yaml)

## Source of Truth

**The spec in ioc-cfn-svc is the authoritative source.** This copy is used for local SDK generation.

- **Upstream source**: https://github.com/cisco-eti/ioc-cfn-svc/tree/main/docs/public-api
- **Local copy**: `public-api-v1.0.yaml`

## Generating SDK Client

To regenerate the Python SDK from this spec:

```bash
make gen-openapi
```

This uses Docker with `openapitools/openapi-generator-cli` to create type-safe Python client code in `src/generated/`.

### Prerequisites

Pull the Docker image:

```bash
docker pull openapitools/openapi-generator-cli
```

Or use the make target:

```bash
make pull-openapi-generator
```

## Updating the Spec

**DO NOT edit `public-api-v1.0.yaml` directly.** Changes must be made in the [ioc-cfn-svc repository](https://github.com/cisco-eti/ioc-cfn-svc).

To update to a newer version:

1. Copy the latest spec from ioc-cfn-svc:
   ```bash
   cp /path/to/ioc-cfn-svc/docs/public-api/public-api-v1.0.yaml .
   ```

2. Regenerate the SDK:
   ```bash
   make gen-openapi
   ```

3. Update `src/ioc_cfn_mas_client/client.py` if the API surface changed

4. Test the changes:
   ```bash
   uv run python examples/example.py
   ./scripts/unit-test.sh
   ```

## Naming Conventions

The spec follows **Python PEP 8** conventions automatically:

- **Package**: `generated`
- **Classes**: `SharedMemoriesApi`, `CreateOrUpdateRequest`
- **Methods**: `create_or_update_shared_memories()`, `fetch_shared_memories()`
- **Fields**: `workspace_id`, `mas_id`, `agent_id`

This resolves the snake_case vs camelCase inconsistencies from the old spec.

## Documentation

For the user-facing SDK documentation, see the main [README.md](../README.md).
