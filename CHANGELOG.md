# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-07-15

### Added
- L9 protocol message routing support (CFN API v0.2.1)
- `forward_l9_message()` method for L9 protocol messages
- Compatibility table in README showing API version mapping
- PyPI publishing infrastructure
- Automated release workflow via GitHub Actions
- Build and test Makefile targets
- RELEASING.md with maintainer documentation

### Removed
- A2A instrumentation (monkey-patching approach) - deprecated
- A2A sidecar proxy examples and deployment code
- a2a-sdk dependency (was causing version conflicts)

### Changed
- **Version scheme**: Client library uses independent versioning
- Version `0.3.0` supports CFN Public API v0.2.1
- OpenAPI spec updated from v1.2 to v0.2.1

## [0.2.2] - 2026-07-10

### Changed
- Updated PyPI package description
- Documentation improvements

## [0.1.0] - 2026-06-24

### Added
- Initial alpha release to PyPI
- Python SDK for IoC Cognition Fabric Node MAS
- Shared Memories API support
- Memory Operations API support (proxy to remote providers)
- Semantic Alignment API support
- MCP (Model Context Protocol) integration
- OpenAPI-generated API clients
- Comprehensive examples and documentation
- Support for Python 3.10, 3.11, and 3.12

### Documentation
- README with quick start guide
- API documentation
- Examples for all major features
- MCP integration guide

[Unreleased]: https://github.com/outshift-open/ioc-cfn-mas-client-lib/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/outshift-open/ioc-cfn-mas-client-lib/compare/v0.2.2...v0.3.0
[0.2.2]: https://github.com/outshift-open/ioc-cfn-mas-client-lib/compare/v0.1.0...v0.2.2
[0.1.0]: https://github.com/outshift-open/ioc-cfn-mas-client-lib/releases/tag/v0.1.0
