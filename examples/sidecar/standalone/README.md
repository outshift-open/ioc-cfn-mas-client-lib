# Sidecar Standalone Demo (Kubernetes without Istio)

This demo shows **transparent traffic interception with iptables and UID-based exclusions** in Kubernetes **without requiring Istio**. It uses init containers to set up iptables rules for dual-boundary interception.

**One command setup:** `./setup.sh` creates everything!

## Key Feature: UID-Based iptables Exclusions

This demo solves the "traffic loop problem" using the same approach as Istio:

- **Agent containers run as UID 1000** (regular user)
- **Sidecar containers run as UID 1337** (Envoy)
- **iptables excludes UID 1337** from interception

This prevents Envoy's own traffic from being intercepted, eliminating infinite loops.

## Architecture

```
┌─────────────────────────────────────────┐
│  Pod: agent-a (network namespace)       │
│  ┌────────────────────────────────────┐ │
│  │ Init Container: init-iptables      │ │
│  │ - Sets up iptables rules           │ │
│  │ - Excludes UID 1337 from redirect  │ │
│  └────────────────────────────────────┘ │
│  ┌──────────┐  ┌───────────────────┐  │
│  │ Sidecar  │  │ Agent A           │  │
│  │ UID 1337 │  │ UID 1000          │  │
│  └──────────┘  └───────────────────┘  │
│         Pod IP: 10.244.0.x             │
└─────────────────────────────────────────┘
                 ↕ veth interface
            Kubernetes Network
                 ↕
┌─────────────────────────────────────────┐
│  Pod: agent-b (network namespace)       │
│  ┌────────────────────────────────────┐ │
│  │ Init Container: init-iptables      │ │
│  └────────────────────────────────────┘ │
│  ┌──────────┐  ┌───────────────────┐  │
│  │ Sidecar  │  │ Agent B           │  │
│  │ UID 1337 │  │ UID 1000          │  │
│  └──────────┘  └───────────────────┘  │
│         Pod IP: 10.244.0.y             │
└─────────────────────────────────────────┘
```

## How It Works

### 1. Init Container Sets Up iptables with UID Exclusion

Before the main containers start, an init container runs `init-iptables.sh`:

```bash
# CRITICAL: Exclude Envoy's traffic (UID 1337) from interception
iptables -t nat -A OUTPUT -m owner --uid-owner 1337 -j RETURN

# OUTBOUND: Redirect egress traffic to Envoy port 15002
iptables -t nat -A OUTPUT -p tcp -j REDIRECT --to-port 15002

# INBOUND: Redirect ingress traffic to Envoy port 15001
iptables -t nat -A PREROUTING -p tcp --dport 8000,8001 -j REDIRECT --to-port 15001
```

### 2. Containers Run with Different UIDs

**K8s Security Context:**
```yaml
containers:
- name: agent
  securityContext:
    runAsUser: 1000  # Agent UID
    runAsNonRoot: true

- name: sidecar
  securityContext:
    runAsUser: 1337  # Envoy UID
    runAsNonRoot: true
```

### 3. Traffic Flow

**Agent A → Agent B:**

1. **OUTBOUND** (Agent A's sidecar):
   - Agent A (UID 1000) calls `http://agent-b:8000`
   - OUTPUT chain intercepts (UID 1000 ≠ 1337)
   - Redirects to Envoy (port 15002)
   - Envoy's ext_authz logs A2A message to CFN (OUTBOUND)
   - Envoy (UID 1337) forwards to Agent B
   - Envoy's traffic bypasses iptables (UID exclusion)

2. **INBOUND** (Agent B's sidecar):
   - Traffic arrives at Agent B's pod via veth interface
   - PREROUTING chain redirects to Envoy (port 15001)
   - Envoy's ext_authz logs A2A message to CFN (INBOUND)
   - Envoy forwards to Agent B's app (port 8000)

### 4. Why This Works

✅ **App traffic intercepted** - UID 1000 goes through iptables
✅ **Envoy traffic bypassed** - UID 1337 excluded by iptables
✅ **No loops** - Envoy can forward without being intercepted
✅ **Dual-boundary** - Both sender and receiver sidecars see the message

## Prerequisites

- Kubernetes cluster (kind, minikube, or cloud)
- kubectl configured
- Docker for building images

## Quick Start

```bash
# Creates kind cluster, builds images, and deploys everything
./setup.sh
```

This will:
- ✅ Create a local kind cluster (or use existing one)
- ✅ Build all Docker images
- ✅ Load images to the cluster
- ✅ Deploy all services
- ✅ Wait for pods to be ready

### Watch the Demo

```bash
# Watch CFN logs (dual-boundary validation)
kubectl logs -f -l app=cfn

# Watch Agent A (sender) logs
kubectl logs -f -l app=agent-a -c agent

# Watch Agent B (receiver) logs
kubectl logs -f -l app=agent-b -c agent

# Watch sidecar logs
kubectl logs -f -l app=agent-a -c sidecar
kubectl logs -f -l app=agent-b -c sidecar

# Verify iptables rules
kubectl exec deploy/agent-a -c sidecar -- iptables -t nat -L -n -v

# Verify UIDs
kubectl exec deploy/agent-a -c agent -- id
kubectl exec deploy/agent-a -c sidecar -- id
```

## Expected Output

CFN logs should show both OUTBOUND and INBOUND interceptions:

```
===========================================================
[14:23:15] Direction: OUTBOUND →
===========================================================
Intercepted by: agent-a-sidecar
Workspace: demo-workspace
A2A Message:
  - ID: 1
  - Type: tasks/send
  - Path: /tasks/send
  - Content: Message #1 from Agent A
===========================================================

===========================================================
[14:23:15] Direction: INBOUND ←
===========================================================
Intercepted by: agent-b-sidecar
Workspace: demo-workspace
A2A Message:
  - ID: 1
  - Type: tasks/send
  - Path: /tasks/send
  - Content: Message #1 from Agent A
===========================================================
```

## Manual Deployment

```bash
# Build images
docker build -t sidecar-standalone-cfn:latest -f ../sidecar/Dockerfile.cfn ../sidecar
docker build -t sidecar-standalone-agent-a:latest -f ../sidecar/Dockerfile.agent_a ../sidecar
docker build -t sidecar-standalone-agent-b:latest -f ../sidecar/Dockerfile.agent_b ../sidecar
docker build -t sidecar-standalone-sidecar:latest -f Dockerfile.sidecar ../..

# Load to kind (if using kind)
kind load docker-image sidecar-standalone-cfn:latest
kind load docker-image sidecar-standalone-agent-a:latest
kind load docker-image sidecar-standalone-agent-b:latest
kind load docker-image sidecar-standalone-sidecar:latest

# Deploy
kubectl apply -f k8s/cfn.yaml
kubectl apply -f k8s/agent-a.yaml
kubectl apply -f k8s/agent-b.yaml

# Check status
kubectl get pods
kubectl wait --for=condition=ready pod -l app=agent-a
```

## Cleanup

```bash
kubectl delete -f k8s/
# Or delete the entire cluster
kind delete cluster --name sidecar-demo
```

## Comparison with Istio

| Feature | Standalone (This Demo) | Istio Demo |
|---------|----------------------|------------|
| Istio Required | ❌ No | ✅ Yes |
| Service Mesh | ❌ No | ✅ Yes |
| Sidecar Injection | Manual (manifests) | Automatic |
| iptables Setup | Init container | Istio CNI / init container |
| UID-Based Exclusions | ✅ Manual | ✅ Automatic |
| Dual-Boundary | ✅ Yes | ✅ Yes |
| Traffic Loops | ✅ Prevented | ✅ Prevented |
| Production Ready | ✅ Yes (VMs/K8s) | ✅ Yes (K8s only) |

## Production Deployment

This pattern works for:

### 1. **Kubernetes without Istio**
Use these manifests as-is. Add resource limits, health checks, etc.

### 2. **Virtual Machines**
The same iptables approach works on VMs:

```bash
# On VM startup (as root):
/path/to/init-iptables.sh

# Start sidecar as UID 1337:
sudo -u envoy /path/to/sidecar-entrypoint.sh &

# Start app as UID 1000:
sudo -u appuser ./your-app
```

### 3. **Bare Metal**
Same as VMs - iptables rules apply to the host's network namespace.

## Troubleshooting

### No INBOUND traffic intercepted?
```bash
# Check if init container ran
kubectl logs -l app=agent-a -c init-iptables

# Verify iptables rules
kubectl exec deploy/agent-a -c sidecar -- iptables -t nat -L PREROUTING -n -v
# Should show redirect to port 15001
```

### No OUTBOUND traffic intercepted?
```bash
# Check OUTPUT chain
kubectl exec deploy/agent-a -c sidecar -- iptables -t nat -L OUTPUT -n -v
# Should show:
# 1. RETURN for UID 1337 (first rule)
# 2. REDIRECT for all other traffic
```

### Traffic loop / connection failures?
```bash
# Verify UIDs are correct
kubectl exec deploy/agent-a -c agent -- id
# Should show: uid=1000

kubectl exec deploy/agent-a -c sidecar -- id
# Should show: uid=1337

# Check iptables UID exclusion
kubectl exec deploy/agent-a -c sidecar -- iptables -t nat -L OUTPUT -n -v | grep 1337
# Should show: RETURN rule for owner UID match 1337
```

### Direction detection wrong?
```bash
# Check local IP detection
kubectl logs -l app=agent-a -c sidecar | grep "Local container IP"
# Should match pod IP

kubectl get pods -o wide
# Compare with pod IPs
```

## Technical Details

### Init Container Security

The init container needs `NET_ADMIN` capability to modify iptables:

```yaml
securityContext:
  capabilities:
    add: ["NET_ADMIN"]
  privileged: false  # Not needed!
  runAsUser: 0  # Must be root for iptables
```

### Container UIDs

**Why UID 1337?**
Istio convention - makes it easy to recognize Envoy containers.

**Why UID 1000?**
Standard non-root user UID - common default in Docker.

### Envoy Listeners

- **Port 15001:** Inbound listener (PREROUTING → here)
- **Port 15002:** Outbound listener (OUTPUT → here)
- **Port 9001:** ext_authz gRPC service

### Direction Detection

The sidecar detects traffic direction by:
1. Checking if destination IP matches local pod IP → INBOUND
2. Checking if source IP matches local pod IP → OUTBOUND
3. Fallback: port-based heuristics

## Why UID-Based Exclusions Work

The Linux kernel tracks which process (UID) initiated each network connection. The iptables `-m owner --uid-owner` module can match on this:

```bash
# Traffic from UID 1337 (Envoy) → RETURN (skip interception)
iptables -t nat -A OUTPUT -m owner --uid-owner 1337 -j RETURN

# Traffic from UID 1000 (Agent) → REDIRECT (intercept)
iptables -t nat -A OUTPUT -p tcp -j REDIRECT --to-port 15002
```

**Result:**
- Agent makes request → intercepted → sent to Envoy
- Envoy forwards request → bypassed → sent to destination
- No loop, dual-boundary interception works! ✅

## Next Steps

- Add TLS/mTLS between sidecars
- Implement policy enforcement (block/allow rules)
- Add rate limiting and circuit breaking
- Deploy to production VMs or K8s cluster
