# A2A Sidecar Integration Test

Demonstrates transparent A2A protocol interception with **zero agent code changes**.

## Architecture

```
Agent A ──A2A──> Agent B
   │               │
 [Sidecar]     [Sidecar]
   │               │
   └──> Mock CFN API <──┘
```

## What Gets Intercepted

- A2A JSON-RPC requests (tasks/send)
- Transparent via Envoy + iptables + Istio
- Agents have ZERO awareness of sidecar

## Prerequisites

```bash
# Install kind
brew install kind

# Install Istio CLI
curl -L https://istio.io/downloadIstio | sh -
cd istio-*/bin && export PATH=$PWD:$PATH
```

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

# See Agent A sending requests
kubectl logs -f -n a2a-demo pod/agent-a -c agent-a

# See Agent B receiving requests
kubectl logs -f -n a2a-demo deployment/agent-b -c agent-b

# See sidecar intercepting traffic
kubectl logs -f -n a2a-demo deployment/agent-b -c a2a-sidecar
```

## Verify Zero Code Changes

Check [agent_a.py](agent_a.py) and [agent_b.py](agent_b.py) - no sidecar imports, no configuration, just pure A2A protocol.

## Cleanup

```bash
kind delete cluster --name a2a-demo
```
