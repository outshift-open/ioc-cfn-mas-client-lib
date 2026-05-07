# Implementation Details: UID-Based iptables for Traffic Interception

## Problem Solved

**Traffic Loop Issue**: When using iptables REDIRECT for transparent traffic interception, Envoy's own outbound traffic gets intercepted, creating infinite loops.

## Solution

Use **UID-based iptables exclusions** (same approach as Istio):
- Run agent as UID 1000
- Run Envoy sidecar as UID 1337
- Exclude UID 1337 from iptables interception

## Key Files

### 1. `init-iptables.sh`
```bash
ENVOY_UID="1337"

# CRITICAL: Exclude Envoy's traffic from interception
iptables -t nat -A OUTPUT -m owner --uid-owner ${ENVOY_UID} -j RETURN

# Then intercept all other traffic
iptables -t nat -A OUTPUT -p tcp -j REDIRECT --to-port 15002
iptables -t nat -A PREROUTING -p tcp --dport 8000,8001 -j REDIRECT --to-port 15001
```

**Result**: App traffic (UID 1000) → intercepted, Envoy traffic (UID 1337) → bypassed

### 2. K8s Manifests (`k8s/agent-*.yaml`)

**Init Container** (runs as root to set up iptables):
```yaml
initContainers:
- name: init-iptables
  image: sidecar-standalone-sidecar:latest
  command: ["/init-iptables.sh"]
  securityContext:
    capabilities:
      add: ["NET_ADMIN"]
    runAsUser: 0  # Root for iptables
```

**Agent Container** (runs as UID 1000):
```yaml
containers:
- name: agent
  securityContext:
    runAsUser: 1000
    runAsNonRoot: true
```

**Sidecar Container** (runs as UID 1337):
```yaml
- name: sidecar
  securityContext:
    runAsUser: 1337
    runAsNonRoot: true
```

### 3. Dockerfiles

**Sidecar**: Creates envoy user with UID 1337
```dockerfile
RUN useradd -u 1337 -m -s /bin/bash envoy
# Don't set USER here - K8s securityContext handles it
```

**Agent**: Creates appuser with UID 1000
```dockerfile
RUN useradd -u 1000 -m appuser
USER appuser
```

## How It Works

### Traffic Flow: Agent A → Agent B

1. **Agent A makes request** (running as UID 1000)
   ```
   Agent A (UID 1000) → http://agent-b:8000
   ```

2. **iptables OUTPUT chain checks UID**
   ```
   Rule 1: UID 1337? → RETURN (skip)
   Rule 2: Other UID? → REDIRECT to port 15002
   ```
   **Match Rule 2** → Traffic redirected to Envoy

3. **Envoy receives and processes**
   ```
   Port 15002 → ext_authz logs (OUTBOUND) → forward to agent-b:8000
   ```

4. **Envoy forwards** (running as UID 1337)
   ```
   Envoy (UID 1337) → http://agent-b:8000
   ```

5. **iptables OUTPUT chain checks UID again**
   ```
   Rule 1: UID 1337? → RETURN (skip)
   ```
   **Match Rule 1** → Traffic bypasses interception, goes directly to agent-b

6. **Traffic arrives at Agent B pod**
   ```
   veth interface → PREROUTING chain → REDIRECT to port 15001
   ```

7. **Agent B's Envoy receives**
   ```
   Port 15001 → ext_authz logs (INBOUND) → forward to localhost:8000
   ```

8. **Agent B receives request** ✅

## Why This Prevents Loops

**Without UID exclusion:**
```
App → iptables → Envoy → iptables → Envoy → iptables → ∞
```

**With UID exclusion:**
```
App (UID 1000) → iptables intercepts → Envoy (UID 1337)
Envoy (UID 1337) → iptables skips → Destination ✅
```

## Security Considerations

### Capabilities
- **Init container**: Needs `NET_ADMIN` for iptables (root)
- **Agent/Sidecar**: No special capabilities needed

### Non-privileged
- No containers need `privileged: true`
- All main containers run as non-root

### Least Privilege
- Init container runs, sets up iptables, exits
- Main containers run with minimal permissions

## Testing

### Pre-flight Check
```bash
./test-local.sh
```
Verifies:
- All files present
- UIDs configured correctly
- iptables exclusion in place

### Full Deployment
```bash
./setup.sh
```
Deploys to kind cluster and runs integration test.

### Manual Verification
```bash
# Check UIDs
kubectl exec deploy/agent-a -c agent -- id
kubectl exec deploy/agent-a -c sidecar -- id

# Check iptables rules
kubectl exec deploy/agent-a -c sidecar -- iptables -t nat -L OUTPUT -n -v

# Watch logs
kubectl logs -f -l app=cfn
```

## Comparison: Before vs After

| Aspect | Before (No UID Exclusion) | After (With UID Exclusion) |
|--------|---------------------------|----------------------------|
| Traffic Loops | ✗ Infinite loops | ✅ No loops |
| Dual-Boundary | ✗ Can't work | ✅ Works perfectly |
| Agent Code | No changes | No changes |
| Deployment | Simple manifests | +securityContext |
| Production Ready | ❌ No | ✅ Yes |

## Production Checklist

- [ ] Set resource limits on all containers
- [ ] Add liveness/readiness probes
- [ ] Configure proper logging
- [ ] Set up monitoring/alerting
- [ ] Test failure scenarios
- [ ] Document runbook for operators
- [ ] Implement mTLS between sidecars
- [ ] Add policy enforcement

## References

- Istio uses the same UID 1337 for Envoy
- iptables owner module: `man iptables-extensions`
- K8s security context: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
