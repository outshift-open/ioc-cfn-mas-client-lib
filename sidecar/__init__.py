"""A2A Sidecar - Transparent A2A message interception.

This package provides production-ready sidecar deployment patterns for intercepting
A2A protocol messages using Envoy's ext_authz filter.

The sidecar runs as a separate container alongside your agent with zero
configuration changes needed in the agent application.

Architecture:
    Agent (unchanged) → Envoy (Istio or standalone) → ext_authz → CFN

Deployment Options:
    - istio/: Recommended for production - uses Istio EnvoyFilter (no port conflicts)
    - standalone/: For non-Istio environments - custom Envoy + ext_authz
    - shared/: Common Python code (ext_authz service, message parser, config)

For implementation details, see: sidecar/README.md
"""

__version__ = "1.0.0"
