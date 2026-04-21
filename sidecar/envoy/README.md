# A2A Sidecar - Envoy + ext_authz (ZTA Pattern with Istio)

**Truly transparent A2A traffic interception - NO agent configuration changes needed!**

This implementation follows the **ZTA (Zero Trust Architecture)** pattern using:
1. **Istio service mesh** - automatic sidecar injection and iptables setup
2. **Envoy proxy** - handles traffic interception
3. **ext_authz gRPC service** - parses and logs A2A messages

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Kubernetes Pod                        │
│                                                          │
│  ┌────────────────┐                                     │
│  │  Agent App     │  (COMPLETELY UNCHANGED!)            │
│  │  - No config   │                                     │
│  │  - No HTTP     │                                     │
│  │    _PROXY      │                                     │
│  └────────┬───────┘                                     │
│           │                                              │
│           │ (thinks it's going directly to target)      │
│           ▼                                              │
│  ┌──────────────────────────────────────────┐           │
│  │         iptables rules                   │           │
│  │  (automatically set up by Istio)         │           │
│  │  redirect :8000 → :15002 (outbound)      │           │
│  │  redirect *:* → :15001 (inbound)         │           │
│  └────────────┬─────────────────────────────┘           │
│               │                                          │
│               ▼                                          │
│  ┌──────────────────────────────────────────┐           │
│  │         Envoy Proxy                      │           │
│  │  - Inbound listener: :15001              │           │
│  │  - Outbound listener: :15002             │           │
│  │  - Admin interface: :9901                │           │
│  └────────────┬─────────────────────────────┘           │
│               │ (gRPC call to ext_authz)                │
│               ▼                                          │
│  ┌──────────────────────────────────────────┐           │
│  │    ext_authz gRPC Service (Python)       │           │
│  │  - Parse A2A messages                    │           │
│  │  - Log to file                           │           │
│  │  - Send to CFN API (future)              │           │
│  │  - Allow/Deny requests                   │           │
│  └──────────────────────────────────────────┘           │
└──────────────────────────────────────────────────────────┘
```

## Prerequisites

- **Istio service mesh** must be installed in your Kubernetes cluster
- Follow [Istio installation guide](https://istio.io/latest/docs/setup/install/)

## Key Features

✅ **Zero agent configuration** - agents are completely agnostic
✅ **Transparent interception** - Istio handles iptables automatically
✅ **Language agnostic** - works with any HTTP client
✅ **Production-ready** - based on ZTA/Istio patterns
✅ **Protocol-aware** - parses A2A messages (JSON-RPC 2.0)

## Quick Start

### 1. Build the Sidecar Image

```bash
cd /path/to/ioc-cfn-mas-client-lib
docker build -t a2a-sidecar:latest -f sidecar/envoy/Dockerfile .
```

### 2. Deploy to Kubernetes

**Note**: Ensure Istio is installed in your cluster first.

```bash
kubectl apply -f sidecar/envoy/kubernetes/agent-with-sidecar.yaml
```

The Pod uses the `sidecar.istio.io/inject: "true"` annotation to automatically:
- Inject Istio's Envoy sidecar
- Set up iptables rules for transparent traffic interception

### 3. Verify

```bash
# Check pod status
kubectl get pods

# Check sidecar logs
kubectl logs agent-with-a2a-sidecar -c a2a-sidecar

# Check agent logs
kubectl logs agent-with-a2a-sidecar -c agent
```

**That's it!** Your agent is now completely agnostic, and all A2A traffic is being intercepted and logged.

## Components

### 1. Envoy Configuration (`envoy.yaml`)

Configures two listeners:
- **Inbound listener** (:15001) - for incoming traffic
- **Outbound listener** (:15002) - for outgoing traffic

Both use ext_authz filter to call our parsing service.

### 2. ext_authz Service (`ext_authz_service.py`)

Python gRPC service that:
- Receives requests from Envoy
- Parses A2A protocol messages
- Logs to JSON file
- Allows/denies traffic
- (Future) Sends to CFN API

### 3. iptables Setup (`setup_iptables.sh`)

Bash script that sets up transparent redirection:
- Redirects outbound traffic to Envoy :15002
- Redirects inbound traffic to Envoy :15001
- Excludes Envoy's own traffic (to avoid loops)

### 4. Entrypoint (`entrypoint.sh`)

Starts both services:
1. Sets up iptables
2. Starts ext_authz gRPC service
3. Starts Envoy proxy

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CFN_URL` | CFN API endpoint | No |
| `WORKSPACE_ID` | CFN workspace ID | No |
| `MAS_ID` | CFN MAS ID | No |

### Kubernetes Deployment

```yaml
containers:
- name: agent
  image: my-agent:latest
  # NO configuration changes!

- name: a2a-sidecar
  image: a2a-sidecar:latest
  env:
  - name: CFN_URL
    value: "http://cfn-api:9002"
  - name: WORKSPACE_ID
    value: "my-workspace"
  - name: MAS_ID
    value: "my-mas"
```

### Docker Compose

```yaml
services:
  agent:
    image: my-agent:latest
    cap_add:
      - NET_ADMIN  # For iptables
    network_mode: "service:sidecar"

  sidecar:
    image: a2a-sidecar:latest
    environment:
      CFN_URL: "http://cfn-api:9002"
      WORKSPACE_ID: "my-workspace"
      MAS_ID: "my-mas"
    cap_add:
      - NET_ADMIN
```

## Agent Requirements

**NONE!** Agents need zero changes:

```python
# Agent code - COMPLETELY UNCHANGED
import httpx

async def main():
    client = httpx.AsyncClient()
    # This connection is TRANSPARENTLY intercepted
    response = await client.get("http://target-agent:8000/execute")
    print(response.text)

# NO HTTP_PROXY
# NO configuration
# NO awareness of sidecar
```

## Comparison: Envoy vs Python Proxy

| Feature | Envoy + ext_authz | Python HTTP Proxy |
|---------|-------------------|-------------------|
| **Agent Config** | None ✅ | HTTP_PROXY ⚠️ |
| **Performance** | High (50K+ req/s) | Medium (1-3K req/s) |
| **Complexity** | High | Low |
| **Setup** | Docker + K8s | Simple |
| **Platform** | Linux | Cross-platform |
| **Production** | ✅ Recommended | Development only |

## How It Works

### Traffic Flow

```
1. Agent makes HTTP request: GET http://target:8000/execute
   ↓
2. iptables intercepts and redirects to Envoy :15002
   ↓
3. Envoy receives request, calls ext_authz gRPC service
   ↓
4. ext_authz parses A2A message, logs it
   ↓
5. ext_authz returns ALLOW
   ↓
6. Envoy forwards request to original target (target:8000)
   ↓
7. Response flows back through the same chain
```

### iptables Rules

```bash
# Outbound redirection
iptables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner 1337 -j REDIRECT --to-port 15002

# Inbound redirection
iptables -t nat -A PREROUTING -p tcp -j REDIRECT --to-port 15001
```

## Logs

### ext_authz Logs (Console)

```
[2024-01-20 10:00:00] [A2A Sidecar] INFO - → A2A REQUEST: 10.244.1.5:54321 → target-agent:8000 | POST /execute | Protocol: jsonrpc
[2024-01-20 10:00:01] [A2A Sidecar] INFO - ← A2A RESPONSE: target-agent:8000 → 10.244.1.5:54321 | POST /execute | Protocol: jsonrpc
```

### ext_authz Logs (JSON File)

```bash
kubectl exec agent-with-a2a-sidecar -c a2a-sidecar -- cat /var/log/a2a/sidecar.log | jq .
```

```json
{
  "timestamp": "2024-01-20T10:00:00Z",
  "direction": "request",
  "protocol": "jsonrpc",
  "method": "POST",
  "path": "/execute",
  "task_id": "task-abc123",
  "body": {...}
}
```

### Envoy Admin Interface

```bash
# Port-forward admin interface
kubectl port-forward agent-with-a2a-sidecar 9901:9901

# View stats
curl http://localhost:9901/stats

# View config
curl http://localhost:9901/config_dump
```

## Troubleshooting

### No traffic being intercepted

```bash
# Check iptables rules
kubectl exec agent-with-a2a-sidecar -c a2a-sidecar -- iptables -t nat -L

# Should see A2A_INBOUND and A2A_OUTBOUND chains
```

### ext_authz not receiving requests

```bash
# Check ext_authz is running
kubectl exec agent-with-a2a-sidecar -c a2a-sidecar -- ps aux | grep ext_authz

# Check gRPC port
kubectl exec agent-with-a2a-sidecar -c a2a-sidecar -- netstat -tuln | grep 9001
```

### Envoy errors

```bash
# Check Envoy logs
kubectl logs agent-with-a2a-sidecar -c a2a-sidecar | grep envoy

# Check admin interface
kubectl port-forward agent-with-a2a-sidecar 9901:9901
curl http://localhost:9901/clusters
```

## Development

### Local Testing (Docker)

```bash
# Build image
docker build -t a2a-sidecar:latest -f sidecar/envoy/Dockerfile .

# Run with Docker (requires privileged for iptables)
docker run --privileged --rm \
  -e CFN_URL=http://localhost:9002 \
  -e WORKSPACE_ID=dev-workspace \
  -e MAS_ID=dev-mas \
  a2a-sidecar:latest
```

### Extending ext_authz

```python
# Custom ext_authz with CFN integration
class CustomExtAuthZ(A2AExtAuthZService):
    async def Check(self, request, context):
        response = await super().Check(request, context)

        # Add custom logic
        # e.g., send to CFN API, metrics, etc.

        return response
```

## Production Deployment

### 1. Use Init Container Pattern

```yaml
initContainers:
- name: iptables-init
  image: a2a-sidecar:latest
  command: ["/app/setup_iptables.sh"]
  securityContext:
    capabilities:
      add: [NET_ADMIN]
```

### 2. Resource Limits

```yaml
containers:
- name: a2a-sidecar
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"
```

### 3. Health Checks

```yaml
livenessProbe:
  httpGet:
    path: /ready
    port: 9901
  initialDelaySeconds: 10
  periodSeconds: 10
```

### 4. Monitoring

Add Prometheus metrics:
```bash
curl http://localhost:9901/stats/prometheus
```

## Next Steps

1. ✅ Test with your existing agents
2. ✅ Verify transparent interception
3. ⏩ Add CFN API integration in ext_authz
4. ⏩ Add metrics and monitoring
5. ⏩ Deploy to production

## References

- [ZTA Reference Implementation](https://github.com/zta)
- [Envoy ext_authz Documentation](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_authz_filter)
- [Istio Sidecar Pattern](https://istio.io/latest/docs/ops/deployment/architecture/)
- [Main README](../../../README.md)
