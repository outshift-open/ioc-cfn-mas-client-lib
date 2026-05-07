# Standalone A2A Sidecar (No Istio)

This directory contains a standalone implementation of the Agent-to-Agent (A2A) communication sidecar that operates **without** Istio service mesh. It provides transparent request/response interception using Envoy proxy and iptables.

## Architecture Overview

The sidecar consists of three main components:

```
┌─────────────────────────────────────────────────────┐
│                     Pod                              │
├─────────────────────────────────────────────────────┤
│  Init Container (runs first, as root)               │
│  ├─ init-iptables.sh                                │
│  └─ Sets up iptables rules for traffic interception │
├─────────────────────────────────────────────────────┤
│  Application Container (UID 1000)                   │
│  └─ Your agent application                          │
├─────────────────────────────────────────────────────┤
│  Sidecar Container (UID 1337)                       │
│  ├─ ioc_cfn_l9_service.py (gRPC service on :9001)    │
│  ├─ Envoy Proxy                                     │
│  │  ├─ Inbound listener (:15001)                    │
│  │  └─ Outbound listener (:15002)                   │
│  └─ entrypoint.sh (starts both services)            │
└─────────────────────────────────────────────────────┘
```

### Traffic Flow

#### Outbound Requests (Agent → External Service)
1. Agent makes HTTP request (e.g., `http://agent-b:8000`)
2. **iptables** redirects TCP traffic → Envoy outbound listener (`:15002`)
3. **Envoy** intercepts request, calls CFN L9 service via gRPC
4. **CFN L9 service** sends message to CFN, gets direction
5. Envoy forwards request to actual destination
6. Response flows back through Envoy → CFN L9 service → agent

#### Inbound Requests (External Service → Agent)
1. External request arrives on app port (e.g., `:8001`)
2. **iptables** redirects to Envoy inbound listener (`:15001`)
3. **Envoy** intercepts request, calls CFN L9 service via gRPC
4. **CFN L9 service** sends message to CFN, gets direction
5. Envoy forwards to agent application
6. Response flows back through Envoy → CFN L9 service → caller

## Components

### 1. init-iptables.sh
**Purpose**: Set up iptables rules for transparent traffic interception
**Runs**: As init container with root privileges (UID 0)
**What it does**:
- Creates custom iptables chains (`ENVOY_INBOUND`, `ENVOY_OUTPUT`)
- Redirects outbound TCP traffic to Envoy (`:15002`)
- Redirects inbound traffic on app ports to Envoy (`:15001`)
- Excludes Envoy's own traffic (UID 1337) to prevent loops
- Excludes localhost traffic

**Security**: Requires `NET_ADMIN` capability, runs before main containers

### 2. entrypoint.sh
**Purpose**: Start both CFN L9 service service and Envoy proxy
**Runs**: As main entrypoint for sidecar container (UID 1337)
**What it does**:
- Starts CFN L9 service gRPC service in background
- Waits for CFN L9 service to be ready (health check on `:9001`)
- Starts Envoy proxy as foreground process
- Uses `exec` so Envoy receives signals properly

**Environment Variables**:
- `CFN_URL`: URL of the CFN service (e.g., `http://cfn:9002`)
- `WORKSPACE_ID`: Workspace identifier for CFN
- `MAS_ID`: Unique identifier for this sidecar instance

### 3. envoy.yaml
**Purpose**: Envoy proxy configuration
**What it configures**:
- **Inbound Listener** (`:15001`): Handles incoming traffic to agent
- **Outbound Listener** (`:15002`): Handles outgoing traffic from agent
- **CFN L9 service Filter**: gRPC connection to CFN L9 service service (`:9001`)
- **Admin Interface** (`:9000`): Envoy admin/metrics endpoint

### 4. ioc_cfn_l9_service.py (in sidecar/shared/)
**Purpose**: gRPC service that handles authorization and CFN integration
**What it does**:
- Implements Envoy's CFN L9 service gRPC protocol
- Intercepts HTTP requests/responses
- Sends messages to CFN for semantic negotiation
- Applies direction from CFN to the traffic
- Returns authorization decision to Envoy

## Dockerfile

The Dockerfile builds a single image used by both init container and sidecar:

```dockerfile
FROM envoyproxy/envoy:v1.29-latest AS envoy
FROM python:3.10-slim

# Install Envoy, Python deps, MAS client library
# Copy scripts: entrypoint.sh, init-iptables.sh
# Scripts are copied to root: /entrypoint.sh, /init-iptables.sh
```

**Key Points**:
- Single image for both init and sidecar containers
- Init container runs `/init-iptables.sh` (as root)
- Sidecar container runs `/entrypoint.sh` (as UID 1337)
- Envoy user (UID 1337) created during build

## Deployment

See [examples/sidecar/standalone/](../../../examples/sidecar/standalone/) for:
- **k8s/**: Kubernetes deployment manifests for agent-a and agent-b
- **demo-apps/**: Sample agent applications
- **setup.sh**: Automated demo setup script

### Kubernetes Resources

Each agent pod requires:

1. **Init Container**: Runs `init-iptables.sh`
   - Must have `NET_ADMIN` capability
   - Runs as root (UID 0)

2. **Application Container**: Your agent
   - Runs as UID 1000 (non-root)
   - No special permissions needed

3. **Sidecar Container**: Runs `entrypoint.sh`
   - Runs as UID 1337 (envoy user)
   - No privilege escalation allowed

## Security Considerations

- **Least Privilege**: Only init container needs root and `NET_ADMIN`
- **Non-Root Execution**: Both app and sidecar run as non-root users
- **No Privilege Escalation**: Explicitly disabled in securityContext
- **UID Segregation**: Different UIDs prevent container interactions
  - App: UID 1000
  - Sidecar/Envoy: UID 1337
  - Init: UID 0 (required for iptables)

## Differences from Istio Mode

| Feature | Standalone Mode | Istio Mode |
|---------|----------------|------------|
| Service Mesh | None | Istio |
| Traffic Interception | iptables in init container | Istio's istio-init |
| Envoy Deployment | Explicit sidecar container | Injected by Istio |
| Configuration | envoy.yaml in image | Dynamic via xDS |
| Namespace Requirements | Any namespace | Istio injection enabled |
| Complexity | Lower | Higher |

## Troubleshooting

### Check CFN L9 service logs:
```bash
kubectl logs <pod-name> -c sidecar | grep CFN L9 service
```

### Check Envoy logs:
```bash
kubectl logs <pod-name> -c sidecar | grep Envoy
```

### Check iptables rules:
```bash
kubectl logs <pod-name> -c init-iptables
```

### Test connectivity:
```bash
kubectl exec <pod-name> -c agent -- curl -v http://agent-b:8000
```

### Check Envoy admin interface:
```bash
kubectl port-forward <pod-name> 9000:9000
curl http://localhost:9000/stats
```

## Development

To modify the sidecar:

1. **Edit scripts**: [entrypoint.sh](entrypoint.sh), [init-iptables.sh](init-iptables.sh)
2. **Update Envoy config**: [envoy.yaml](envoy.yaml)
3. **Modify CFN L9 service**: [../shared/ioc_cfn_l9_service.py](../shared/ioc_cfn_l9_service.py)
4. **Rebuild image**: `docker build -f Dockerfile -t sidecar-standalone-sidecar:latest ../../..`
5. **Test locally**: `cd ../../../examples/sidecar/standalone && ./setup.sh`

## Related Documentation

- [Standalone Example](../../../examples/sidecar/standalone/README.md) - Complete demo setup
- [ioc_cfn_l9_service.py](../shared/ioc_cfn_l9_service.py) - Authorization service implementation
- [MAS Client Library](../../../README.md) - Main project documentation
