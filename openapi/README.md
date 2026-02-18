# OpenAPI Specification

This directory contains the OpenAPI specification for the IoC CFN MAS API.

## Files

- **`openapi.json`**: OpenAPI 3.0 specification that defines the MAS API contract

## Purpose

The OpenAPI spec is the **source of truth** for generating the Python SDK client code in `src/generated/`. Any changes to the API should be made here first, then the SDK should be regenerated.

## Generating SDK Client

To regenerate the Python SDK from this spec:

```bash
make gen-openapi
```

This uses `openapi-generator` to create type-safe Python client code in `src/generated/`.

### Prerequisites (macOS)

```bash
brew install openapi-generator
```

If the generator binary is not found, set:

```bash
export OPENAPI_GENERATOR=/opt/homebrew/bin/openapi-generator
```

## Important Notes

### additionalProperties

For flexible object schemas (like `memories` and `relationships`), use:

```json
{
  "type": "object",
  "additionalProperties": true
}
```

**DO NOT** use `"additionalProperties": {}` as this causes Pydantic validation errors. The generator interprets `{}` as "only dict values allowed", which breaks properties with string/number/boolean values.

### Editing the Spec

When modifying `openapi.json`:

1. Make your changes to the spec
2. Run `make gen-openapi` to regenerate the SDK
3. Test the changes with `uv run python examples/example.py`
4. Update `src/ioc_cfn_mas_client/client.py` if the API surface changed

## Documentation

For the user-facing SDK documentation, see the main [README.md](../README.md).
