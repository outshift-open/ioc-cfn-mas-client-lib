# A2A Sidecar Integration Test

Demonstrates transparent A2A protocol interception with **zero agent code changes**.

## Architecture

```
Agent A ←──A2A──→ Agent B
   │                 │
 [Sidecar]       [Sidecar]
   │                 │
   └──> Mock CFN API <─┘
```

Both agents act as **server + client**, sending messages back and forth every 5-7 seconds.

## What Gets Intercepted

- **Bidirectional** A2A JSON-RPC requests (tasks/send)
- Transparent via Envoy + iptables + Istio
- Agents have ZERO awareness of sidecar
- Continuous message exchange for realistic demo

## Important Setup Notes

### Architecture

This demo uses the **Istio EnvoyFilter approach**:
- Istio's Envoy proxy is configured via `EnvoyFilter` CRD
- Only the **ext-authz** Python service runs as a sidecar container
- No custom Envoy binary needed
- No port conflicts

### Istio Injection Configuration

**Agent Pods** (Agent A & Agent B):
- Have Istio sidecar injection **enabled** via namespace label: `istio-injection: enabled`
- Have label `cfn/a2a-sidecar: enabled` (matched by EnvoyFilter)
- Each pod has the **ext-authz** container for A2A interception
- Traffic between agents is intercepted transparently

**Mock CFN API**:
- Has Istio sidecar injection **disabled**: `sidecar.istio.io/inject: "false"`
- This prevents interception loops (sidecar → CFN would be intercepted again)
- Receives data directly from agent sidecars without additional proxying

This configuration ensures:
1. A2A traffic between agents is intercepted
2. Sidecar → CFN API traffic is NOT intercepted (avoids 403 Forbidden)
3. Backend services remain accessible without interference

## Prerequisites

```bash
# Install kind
brew install kind
```

Note: Istio will be automatically downloaded by the setup script.

## Run E2E Test

```bash
./setup.sh
```

This will:
1. Create kind cluster
2. Install Istio
3. Build all images
4. Deploy everything
5. Show log commands

## Watch Interception

```bash
# See intercepted messages in Mock CFN API
kubectl logs -f -n a2a-demo deployment/mock-cfn

# See Agent A (sends to B every 5s, receives from B)
kubectl logs -f -n a2a-demo deployment/agent-a -c agent-a

# See Agent B (sends to A every 7s, receives from A)
kubectl logs -f -n a2a-demo deployment/agent-b -c agent-b

# See ext-authz sidecars intercepting traffic
kubectl logs -f -n a2a-demo deployment/agent-a -c ext-authz
kubectl logs -f -n a2a-demo deployment/agent-b -c ext-authz
```

## Verify Zero Code Changes

Check [agent_a.py](agent_a.py) and [agent_b.py](agent_b.py) - no sidecar imports, no configuration, just pure A2A protocol.

## Cleanup

```bash
kind delete cluster --name a2a-demo
```
