# A2A Sidecar for CFN

Transparently intercepts A2A protocol messages and forwards them to CFN Shared Memory API. **Zero code changes required** in your agents.

## Quick Start

```bash
cd examples/sidecar
./setup.sh  # Creates k8s cluster with working demo
```

See working agents exchange messages: `kubectl logs -f -n a2a-demo deployment/mock-cfn`

## What It Does

```
Agent → Istio Envoy → cfn-sidecar (detects A2A) → CFN API
        ↓
   Original traffic continues (transparent)
```

- Inspects outbound HTTP traffic via Envoy's ext_authz filter
- Detects A2A JSON-RPC 2.0 messages (`jsonrpc == "2.0"`)
- Sends copy to CFN API asynchronously
- **Always allows traffic through** (fail-open)

## Deployment Options

### Option 1: Istio (Recommended for Production)

Uses Istio's built-in Envoy proxy + lightweight Python sidecar.

**Structure:**
```
sidecar/
├── istio/
│   ├── Dockerfile          # cfn-sidecar Python service only
│   └── envoy-filter.yaml   # Configures Istio's Envoy
└── shared/                 # Common Python code
```

**Deploy:**
```bash
# 1. Build image
docker build -t cfn-sidecar:latest -f sidecar/istio/Dockerfile .

# 2. Apply EnvoyFilter (configures Istio's Envoy to call cfn-sidecar)
kubectl apply -f sidecar/istio/envoy-filter.yaml

# 3. Add to your pod spec:
# - annotation: sidecar.istio.io/inject: "true"
# - label: cfn/a2a-sidecar: enabled
# - cfn-sidecar container (see examples/sidecar/k8s/agent-a.yaml)
```

**Pros:** No port conflicts, lighter images, Istio-native
**Cons:** Requires Istio

### Option 2: Standalone (Non-Istio Environments)

Custom Envoy binary + cfn-sidecar service in one container.

**Structure:**
```
sidecar/
├── standalone/
│   ├── Dockerfile      # Envoy + cfn-sidecar together
│   ├── envoy.yaml      # Custom Envoy config
│   └── entrypoint.sh   # Starts both services
└── shared/             # Common Python code
```

**Deploy:**
```bash
docker build -t a2a-sidecar:latest -f sidecar/standalone/Dockerfile .
# Add a2a-sidecar container to your pod (disable Istio injection)
```

**Pros:** Works without Istio
**Cons:** Larger image, port conflicts if Istio enabled

## Configuration

Set these environment variables in the cfn-sidecar container:

```yaml
env:
- name: CFN_URL
  value: "http://cfn-api.default.svc.cluster.local:8080"
- name: WORKSPACE_ID
  value: "my-workspace"
- name: MAS_ID
  value: "my-mas"
```

## How It Works

1. **Traffic Interception:** Istio/Envoy intercepts outbound traffic via iptables
2. **ext_authz Call:** Before routing, Envoy calls cfn-sidecar gRPC service (port 9001)
3. **A2A Detection:** cfn-sidecar checks if `jsonrpc == "2.0"` + A2A method
4. **CFN Forward:** If A2A, sends to CFN API asynchronously (non-blocking)
5. **Traffic Continues:** cfn-sidecar returns OK, original request proceeds

**Key Files:**
- `shared/ext_authz_service.py` - gRPC server implementing Envoy ext_authz protocol
- `shared/message_parser.py` - A2A message detection logic
- `shared/config.py` - Env var configuration
- `istio/envoy-filter.yaml` - Configures Istio's Envoy to call cfn-sidecar

## Troubleshooting

**No messages intercepted?**
```bash
# Check EnvoyFilter is applied
kubectl get envoyfilter -n a2a-demo

# Check pod has label
kubectl get pod -n a2a-demo -l cfn/a2a-sidecar=enabled

# Check cfn-sidecar logs
kubectl logs -n a2a-demo deployment/agent-a -c cfn-sidecar
```

**Messages not reaching CFN?**
```bash
# Verify CFN_URL
kubectl get pod -n a2a-demo -o jsonpath='{.items[0].spec.containers[?(@.name=="cfn-sidecar")].env}'

# Test CFN connectivity
kubectl exec -n a2a-demo deployment/agent-a -c agent-a -- curl -v $CFN_URL/health
```

## References

- [A2A Protocol Spec](https://www.a2aprotocol.org)
- [Envoy ext_authz Docs](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_authz_filter)
- [Istio EnvoyFilter](https://istio.io/latest/docs/reference/config/networking/envoy-filter/)
- [Working Demo](../examples/sidecar/)
