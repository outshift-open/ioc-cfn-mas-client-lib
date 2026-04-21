# A2A Message Interception Sidecar

Transparent interception of A2A protocol messages using Envoy's ext_authz filter. Messages are forwarded to the CFN (Cognition Federation Network) API for storage and analysis.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Components](#components)
- [Deployment Options](#deployment-options)
- [How It Works](#how-it-works)
- [Quick Start](#quick-start)
- [Configuration](#configuration)

---

## Overview

This sidecar enables **zero-code-change** A2A message interception by:
- Using Envoy's ext_authz filter to inspect outbound HTTP traffic
- Detecting A2A JSON-RPC 2.0 messages (per [A2A Protocol v0.3.0](https://www.a2aprotocol.org))
- Forwarding intercepted messages to CFN API
- Allowing all traffic through transparently (fail-open)

**Key Features:**
- ✅ **Non-blocking** - Uses async SDK calls to avoid blocking event loop
- ✅ **Fail open** - Traffic continues even if sidecar crashes
- ✅ **A2A spec compliant** - Validates `jsonrpc == "2.0"` to avoid false positives
- ✅ **Zero agent changes** - Agents remain completely unaware of interception

---

## Architecture

```
┌─────────────────────────────────────────────┐
│ Kubernetes Pod                              │
│                                             │
│  ┌──────────────┐                          │
│  │ Agent        │ (Your application)       │
│  │ Container    │                          │
│  └──────┬───────┘                          │
│         │ HTTP traffic                     │
│         ↓                                   │
│  ┌──────────────┐      gRPC (ext_authz)   │
│  │ Istio Proxy  ├────────────────────────┐ │
│  │ (Envoy)      │                        │ │
│  └──────────────┘                        ↓ │
│                            ┌──────────────┐ │
│                            │ ext-authz    │ │
│                            │ (Python)     │ │
│                            └──────┬───────┘ │
└────────────────────────────────────┼────────┘
                                     │
                                     ↓
                        ┌────────────────────┐
                        │  CFN API           │
                        │  (Shared Memory)   │
                        └────────────────────┘
```

**Traffic Flow:**
1. Agent sends HTTP request (e.g., A2A message to another agent)
2. Istio's Envoy proxy intercepts via iptables
3. Envoy calls ext-authz service via gRPC (configured by EnvoyFilter)
4. ext-authz checks if request is A2A message
5. If A2A: sends copy to CFN API asynchronously
6. ext-authz returns OK → traffic proceeds normally

---

## Components

### 1. **shared/** - Common Python Code

Shared by both deployment patterns (Istio and standalone).

#### Files:
- **`ext_authz_service.py`** - gRPC server implementing Envoy's ext_authz protocol
  - Listens on port 9001
  - Receives HTTP request metadata from Envoy
  - Calls `message_parser` to detect A2A messages
  - Sends to CFN API using async SDK method
  - Always returns OK (fail-open)

- **`message_parser.py`** - A2A protocol detection
  - Validates `jsonrpc == "2.0"` field to avoid false positives
  - Checks for A2A methods: `tasks/send`, `tasks/cancel`, `tasks/verify`, etc.
  - Parses HTTP body before detection

- **`config.py`** - Configuration management
  - Environment variables: `CFN_URL`, `WORKSPACE_ID`, `MAS_ID`
  - Command-line argument parsing

- **`logger.py`** - Logging utilities
  - Formats A2A messages for debugging
  - Structured logging for production

### 2. **istio/** - Istio EnvoyFilter Approach ✅ **RECOMMENDED**

**Use this for production deployments with Istio.**

#### Files:
- **`Dockerfile`** - Builds `ext-authz-only` image (Python service only, no Envoy binary)
- **`envoy-filter.yaml`** - Kubernetes EnvoyFilter CRD to configure Istio's proxy

#### Benefits:
- ✅ **No port collision** - Only one Envoy running (Istio's)
- ✅ **Istio-native** - Uses official Istio API
- ✅ **Simpler** - No custom Envoy binary
- ✅ **Lighter image** - ~100MB smaller
- ✅ **Production-ready** - Follows Istio best practices

#### How It Works:
1. EnvoyFilter CRD patches Istio's Envoy proxy configuration
2. Adds ext_authz HTTP filter to SIDECAR_OUTBOUND listener
3. Adds ext_authz_cluster pointing to localhost:9001
4. Only affects pods with label `cfn/a2a-sidecar: enabled`

#### Requirements:
- Istio must be installed in your Kubernetes cluster

#### Usage:
```bash
# Build image
docker build -t ext-authz-only:latest -f sidecar/istio/Dockerfile .

# Apply EnvoyFilter
kubectl apply -f sidecar/istio/envoy-filter.yaml

# Deploy your app with:
# - annotation: sidecar.istio.io/inject: "true"
# - label: cfn/a2a-sidecar: enabled
# - ext-authz container (image: ext-authz-only:latest)
```

See [examples/sidecar/k8s/](../examples/sidecar/k8s/) for complete deployment manifests.

### 3. **standalone/** - Custom Envoy Approach

**Use this for non-Istio environments or local testing.**

#### Files:
- **`Dockerfile`** - Builds `a2a-sidecar` image (Envoy binary + ext_authz service)
- **`envoy.yaml`** - Custom Envoy proxy configuration with ext_authz filter
- **`entrypoint.sh`** - Starts ext_authz service, waits for readiness, then starts Envoy

#### Use Cases:
- **Non-Istio environments** - When service mesh is not available
- **Development/testing** - Quick local testing without Istio
- **Full control** - Need complete control over Envoy configuration

#### Limitations:
- ⚠️ **Port collision** - If using with Istio injection, creates conflicts (15001/15002)
- ⚠️ **Larger image** - Includes full Envoy binary (~150MB more)
- ⚠️ **More complex** - Manages both Envoy and ext_authz lifecycle

#### Usage:
```bash
# Build image
docker build -t a2a-sidecar:latest -f sidecar/standalone/Dockerfile .

# Deploy your app with:
# - annotation: sidecar.istio.io/inject: "false" (to avoid port conflicts)
# - a2a-sidecar container
# - iptables init container (if not using Istio)
```

---

## Deployment Options

### Option 1: Istio EnvoyFilter (Recommended)

**Best for:** Production Istio deployments

**Pros:**
- Native Istio integration
- No port conflicts
- Simpler configuration
- Lighter images

**Cons:**
- Requires Istio installed

**Files needed:**
- `sidecar/istio/Dockerfile` → build ext-authz-only image
- `sidecar/istio/envoy-filter.yaml` → apply EnvoyFilter
- Pod spec: add `ext-authz` container

### Option 2: Standalone Custom Envoy

**Best for:** Non-Istio environments, local testing

**Pros:**
- Works without Istio
- Full control over Envoy config

**Cons:**
- Port conflicts if Istio injection enabled
- Larger image
- More complex lifecycle management

**Files needed:**
- `sidecar/standalone/Dockerfile` → build a2a-sidecar image
- Pod spec: add `a2a-sidecar` container
- (Optional) iptables init container for traffic redirection

---

## How It Works

### 1. Traffic Interception

**Istio approach:**
- Istio automatically injects Envoy proxy into pods
- iptables rules redirect outbound traffic → Envoy (port 15001)
- No manual configuration needed

**Standalone approach:**
- Custom iptables init container redirects traffic → custom Envoy
- Must disable Istio injection to avoid conflicts

### 2. ext_authz Protocol

Envoy's ext_authz filter is a standard Envoy extension that calls an external gRPC service for authorization decisions.

**Request flow:**
1. Envoy receives HTTP request from agent
2. Envoy calls ext_authz gRPC service with request metadata (method, path, headers, body)
3. ext_authz service inspects request:
   - Parse JSON body
   - Check if `jsonrpc == "2.0"` and `method` in A2A methods
   - If A2A: send to CFN API asynchronously
4. ext_authz returns `OK` response (always allows traffic)
5. Envoy forwards original request to destination

**gRPC API:**
- Service: `envoy.service.auth.v3.Authorization`
- Method: `Check(CheckRequest) → CheckResponse`
- See: [Envoy ext_authz docs](https://www.envoyproxy.io/docs/envoy/latest/api-v3/service/auth/v3/external_auth.proto)

### 3. A2A Message Detection

Per [A2A Protocol v0.3.0](https://www.a2aprotocol.org/en/docs/json-rpc-2-0):
- All A2A messages are JSON-RPC 2.0
- Must have `jsonrpc: "2.0"` field
- Must have `method` field with A2A method name

**Detection logic:**
```python
def is_a2a_message(method: str, path: str, headers: Dict[str, str], body: Optional[dict]) -> bool:
    # If body is already parsed, check jsonrpc field to avoid false positives
    if body and isinstance(body, dict):
        return body.get("jsonrpc") == "2.0" and body.get("method") in A2A_METHODS

    # Fall back to content-type only if body not yet parsed
    content_type = headers.get("content-type", "").lower()
    return "application/json" in content_type
```

This prevents false positives from other JSON APIs.

### 4. CFN Integration

Once A2A message is detected:
1. Call `cfn_client.create_shared_memories_async()` (non-blocking)
2. Send message with metadata:
   - `workspace_id` - CFN workspace
   - `mas_id` - Multi-Agent System ID
   - `agent_id` - Source agent identifier
   - `format: "a2a"` - Message format
3. Fire-and-forget (don't block agent traffic)

**Error handling:**
- If CFN API call fails → log error and return OK (fail-open)
- Agent traffic always proceeds regardless of sidecar state

---

## Quick Start

See [examples/sidecar/](../examples/sidecar/) for a complete working demo.

```bash
cd examples/sidecar
./setup.sh
```

This will:
1. Create kind cluster with Istio
2. Build images (ext-authz-only, agent-a, agent-b, mock-cfn)
3. Deploy agents with sidecar interception
4. Show logs of intercepted messages

**Watch interception:**
```bash
# See intercepted messages
kubectl logs -f -n a2a-demo deployment/mock-cfn

# See agents (unaware of interception)
kubectl logs -f -n a2a-demo deployment/agent-a -c agent-a
kubectl logs -f -n a2a-demo deployment/agent-b -c agent-b

# See ext-authz sidecar logs
kubectl logs -f -n a2a-demo deployment/agent-a -c ext-authz
```

---

## Configuration

### Environment Variables

**Required:**
- `CFN_URL` - CFN API endpoint (e.g., `http://cfn-api.default.svc.cluster.local:8080`)
- `WORKSPACE_ID` - CFN workspace identifier
- `MAS_ID` - Multi-Agent System identifier

**Optional:**
- `LOG_LEVEL` - Logging level (default: `INFO`)

### Command-line Arguments

When running ext_authz_service.py directly:
```bash
python ext_authz_service.py \
  --cfn-url="http://cfn-api:8080" \
  --workspace-id="my-workspace" \
  --mas-id="my-mas"
```

### Kubernetes Example

```yaml
containers:
- name: ext-authz
  image: ext-authz-only:latest
  env:
  - name: CFN_URL
    value: "http://cfn-api.default.svc.cluster.local:8080"
  - name: WORKSPACE_ID
    value: "my-workspace"
  - name: MAS_ID
    value: "my-mas"
  ports:
  - name: ext-authz
    containerPort: 9001
    protocol: TCP
  livenessProbe:
    tcpSocket:
      port: 9001
    initialDelaySeconds: 10
    periodSeconds: 10
  readinessProbe:
    tcpSocket:
      port: 9001
    initialDelaySeconds: 5
    periodSeconds: 5
```

---

## Troubleshooting

### ext-authz not receiving requests

1. **Check EnvoyFilter is applied:**
   ```bash
   kubectl get envoyfilter -n a2a-demo
   kubectl describe envoyfilter a2a-ext-authz -n a2a-demo
   ```

2. **Check pod has correct label:**
   ```bash
   kubectl get pod -n a2a-demo -l cfn/a2a-sidecar=enabled
   ```

3. **Check Istio sidecar is injected:**
   ```bash
   kubectl get pod -n a2a-demo -o jsonpath='{.items[*].spec.containers[*].name}'
   # Should include: istio-proxy
   ```

4. **Check ext-authz service is running:**
   ```bash
   kubectl logs -n a2a-demo deployment/agent-a -c ext-authz
   # Should see: "Starting ext_authz gRPC service on 0.0.0.0:9001..."
   ```

### Messages not reaching CFN

1. **Check CFN_URL is correct:**
   ```bash
   kubectl get pod -n a2a-demo -o jsonpath='{.items[0].spec.containers[?(@.name=="ext-authz")].env}'
   ```

2. **Check CFN API is reachable:**
   ```bash
   kubectl exec -n a2a-demo deployment/agent-a -c agent-a -- curl -v $CFN_URL/health
   ```

3. **Check ext-authz logs for errors:**
   ```bash
   kubectl logs -n a2a-demo deployment/agent-a -c ext-authz | grep ERROR
   ```

### Port conflicts (standalone mode)

If using standalone Envoy with Istio injection enabled:
- **Symptom:** Both proxies racing for ports 15001/15002
- **Solution:** Disable Istio injection: `sidecar.istio.io/inject: "false"`
- **Better solution:** Use Istio EnvoyFilter approach instead

---

## Development

### Running locally

```bash
# Terminal 1 - Start ext_authz service
cd sidecar/shared
python ext_authz_service.py \
  --cfn-url="http://localhost:9002" \
  --workspace-id="local-workspace" \
  --mas-id="local-mas"

# Terminal 2 - Test with curl (via Envoy)
curl -X POST http://localhost:15001/tasks/send \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"tasks/send","params":{"message":"test"}}'
```

### Building images

```bash
# From repository root

# Istio approach
docker build -t ext-authz-only:latest -f sidecar/istio/Dockerfile .

# Standalone approach
docker build -t a2a-sidecar:latest -f sidecar/standalone/Dockerfile .
```

### Testing

See [examples/sidecar/](../examples/sidecar/) for end-to-end integration tests with kind + Istio.

---

## References

- [A2A Protocol v0.3.0](https://www.a2aprotocol.org)
- [Envoy ext_authz Filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_authz_filter)
- [Istio EnvoyFilter](https://istio.io/latest/docs/reference/config/networking/envoy-filter/)
- [CFN Shared Memory API](https://github.com/cisco-eti/ioc-knowledge-memory-svc)
