# A2A Sidecar Demo

End-to-end demo showing **zero-code-change** A2A message interception.

## What This Demonstrates

```
Agent A ←─ A2A ─→ Agent B
   │                 │
[ext-authz]     [ext-authz]
   │                 │
   └──→ Mock CFN ←──┘
```

- Two agents exchange A2A messages every 5-7 seconds
- Sidecars intercept and forward to Mock CFN API
- **Agents have zero awareness of sidecars** (check `agent_a.py` and `agent_b.py`)

## Run Demo

```bash
# Prerequisites: Docker, kind
brew install kind

# Run setup (creates cluster, installs Istio, deploys everything)
./setup.sh
```

## Watch It Work

```bash
# See intercepted messages
kubectl logs -f -n a2a-demo deployment/mock-cfn

# See agents (unaware of interception)
kubectl logs -f -n a2a-demo deployment/agent-a -c agent-a
kubectl logs -f -n a2a-demo deployment/agent-b -c agent-b

# See sidecars doing the work
kubectl logs -f -n a2a-demo deployment/agent-a -c ext-authz
```

## How It Works

**Istio EnvoyFilter Approach:**
- Istio injects Envoy proxy into each pod automatically
- `EnvoyFilter` CRD configures Envoy to call ext-authz service
- ext-authz container (Python) detects A2A messages and sends to CFN
- Only pods with label `cfn/a2a-sidecar: enabled` are affected

**Why Mock CFN has no Istio injection:**
- Annotation `sidecar.istio.io/inject: "false"` prevents sidecar injection
- Avoids interception loop (sidecar → CFN would be intercepted again)

## Files

```
examples/sidecar/
├── setup.sh                   # One-command demo setup
├── agent_a.py                 # Agent A (no sidecar code!)
├── agent_b.py                 # Agent B (no sidecar code!)
├── mock_cfn_api.py            # Mock CFN API
└── k8s/
    ├── namespace.yaml         # Creates a2a-demo namespace
    ├── envoy-filter.yaml      # Configures Istio's Envoy
    ├── agent-a.yaml           # Agent A + ext-authz sidecar
    ├── agent-b.yaml           # Agent B + ext-authz sidecar
    └── mock-cfn.yaml          # Mock CFN (no sidecar)
```

## Cleanup

```bash
kind delete cluster --name a2a-demo
```

## Next Steps

See [sidecar/README.md](../../sidecar/README.md) for deploying to your own agents.
