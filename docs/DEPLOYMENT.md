# Production Deployment Guide

This guide covers production deployment patterns for agents using the IOC CFN MAS Client Library.

## Table of Contents

- [Deployment Options](#deployment-options)
- [A2A Sidecar Proxy Pattern (Production)](#a2a-sidecar-proxy-pattern-production)
- [Comparison: Sidecar vs Monkey-Patching](#comparison-sidecar-vs-monkey-patching)

## Deployment Options

There are two primary approaches for instrumenting agents with CFN:

1. **Envoy Sidecar (Production)** - Zero Trust Architecture with Istio service mesh
2. **Monkey-Patching (Development)** - Python-only instrumentation approach

This guide focuses on the production-ready sidecar approach.

## A2A Sidecar Proxy Pattern (Production)

For production deployments, use the **Envoy-based sidecar** following the **ZTA (Zero Trust Architecture)** pattern with **Istio service mesh**. This provides **truly transparent** interception with zero agent configuration.

**Prerequisites:** Istio must be installed in your Kubernetes cluster.

### Architecture

```
┌──────────────────────────────────────┐
│        Kubernetes Pod                │
│                                      │
│  Agent (UNCHANGED) → Istio/iptables  │
│         ↓                            │
│      Envoy Proxy                     │
│         ↓                            │
│   ext_authz (A2A Parser)             │
│         ↓                            │
│   Logs/CFN API                       │
└──────────────────────────────────────┘
```

**Components:**

- **Istio**: Automatic sidecar injection and traffic interception
- **Envoy Proxy**: C++ high-performance proxy for traffic interception
- **ext_authz Service**: Python gRPC service for A2A message parsing

### Quick Start

```bash
# 1. Build ext-authz image (Istio approach)
docker build -t ext-authz-only:latest -f sidecar/istio/Dockerfile .

# 2. Apply EnvoyFilter to Kubernetes (requires Istio)
kubectl apply -f sidecar/istio/envoy-filter.yaml

# 3. Deploy your agent with ext-authz sidecar container
# See examples/sidecar/k8s/ for complete manifests

# 4. That's it! Agent is completely agnostic - no changes needed!
```

### Key Features

- **✅ Truly agnostic** - zero code changes, zero configuration changes
- **✅ Istio-based** - automatic sidecar injection and iptables setup
- **✅ Production-ready** - uses Istio service mesh
- **✅ Language agnostic** - works with any HTTP client (Python, Go, Node.js, Java, Rust, etc.)
- **✅ High performance** - Envoy proxy (50K+ req/s)
- **✅ Protocol-aware** - parses A2A messages (JSON-RPC 2.0)

### Additional Documentation

For detailed implementation guides, see:

- [Sidecar README](../sidecar/README.md) - Complete implementation guide
- [Working Demo](../examples/sidecar/) - End-to-end example with Istio
- [ZTA Implementation Summary](ZTA_IMPLEMENTATION_SUMMARY.md) - Architecture details
- [Transparent Interception Guide](TRANSPARENT_INTERCEPTION.md) - How iptables works

## Comparison: Sidecar vs Monkey-Patching

| Feature | Envoy Sidecar (ZTA) | Monkey-Patching |
|---------|---------------------|-----------------|
| **Agent Code** | ✅ Unchanged | ⚠️ One instrumentation call |
| **Agent Config** | ✅ Unchanged | ✅ Unchanged |
| **Languages** | Any (Python, Go, Node.js, Java, etc.) | Python only |
| **Performance** | 50K+ req/s | Minimal overhead |
| **Production** | ✅ Recommended | Development only |
| **Platform** | Kubernetes | Any |
| **Isolation** | Strong (separate process) | Weak (same process) |

### Recommendation

- **Production**: Use **Envoy sidecar** (truly agnostic, language-independent)
- **Development/Testing**: Use **monkey-patching** (quick setup, Python-only)

For monkey-patching approach details, see the [A2A Integration Guide](A2A_INTEGRATION.md).

## License

Copyright (c) 2024-2026 Cisco Systems, Inc. and its affiliates. All rights reserved.

Licensed under the Apache License, Version 2.0. See [LICENSE.md](../LICENSE.md) for details.
