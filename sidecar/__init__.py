"""A2A Sidecar - Envoy-based transparent proxy (ZTA Pattern).

This package provides a production-ready sidecar that intercepts A2A traffic
using Envoy proxy + ext_authz + iptables for truly transparent operation.

The sidecar runs as a separate container alongside your agent with zero
configuration changes needed in the agent application.

Architecture:
    Agent (unchanged) → iptables → Envoy → ext_authz → Parse & Log → CFN

Components:
    - Envoy proxy: Traffic interception and routing
    - ext_authz: gRPC service for A2A message parsing and CFN integration
    - iptables: Transparent traffic redirection
    - Shared utilities: Message parser, logger, config (in envoy/ folder)

For implementation details, see: sidecar/envoy/README.md
"""

__version__ = "1.0.0"

# All implementation is in sidecar/envoy/
# No exports from this package - use the ext_authz service directly
