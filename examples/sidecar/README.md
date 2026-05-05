# IoC Sidecar Demo: Dual-Boundary L9 Validation

Demonstrates IoC sidecar with **dual-boundary interception** (OUTBOUND + INBOUND) and **L9 protocol conversion**.

## Architecture Flow

Agent A periodically sends A2A messages to Agent B every 5 seconds. The flow:

```
Agent A (sends A2A message)
   ↓
Sidecar A intercepts (OUTBOUND)
   ↓ converts A2A → L9
   ↓
CFN API validates L9 → returns {"allow": true}
   ↓
Sidecar A forwards original A2A message
   ↓ (wire: A2A unchanged)
   ↓
Sidecar B intercepts (INBOUND)
   ↓ converts A2A → L9
   ↓
CFN API validates L9 → returns {"allow": true}
   ↓
Agent B receives A2A message
```

**Every message is validated twice** (sender + receiver boundaries).

## Run Demo

```bash
# Prerequisites: Docker, kind
brew install kind

# Deploy everything (creates cluster, installs Istio, deploys agents + CFN)
./setup.sh

# Watch CFN logs - you'll see 2 L9 messages per communication
kubectl logs -f -n a2a-demo deployment/cfn
```

**Expected output:**

```
🎯 CFN RECEIVED L9 MESSAGE
Direction: outbound
Actor ID: unknown
Timestamp: 2026-05-05T10:15:30.123Z
A2A payload: {'jsonrpc': '2.0', 'method': 'tasks/send', ...}

🎯 CFN RECEIVED L9 MESSAGE
Direction: inbound
Actor ID: unknown
Timestamp: 2026-05-05T10:15:30.456Z
A2A payload: {'jsonrpc': '2.0', 'method': 'tasks/send', ...}
```

## What Happens

1. **Agent A** sends A2A messages to Agent B every 5 seconds
2. **Sidecar A** (OUTBOUND):
   - Intercepts outbound traffic via Envoy ext_authz
   - Converts A2A → L9 format
   - Sends L9 to CFN API for validation
   - Forwards original A2A if CFN allows
3. **Sidecar B** (INBOUND):
   - Intercepts inbound traffic via Envoy ext_authz
   - Converts A2A → L9 format
   - Sends L9 to CFN API for validation
   - Forwards to Agent B if CFN allows

**Agents have zero awareness of sidecars** - no code changes required.

## L9 Message Format

```json
{
  "header": {
    "direction": "outbound",
    "actor_id": "unknown",
    "timestamp": "2026-05-05T10:15:30.123Z"
  },
  "payload": {
    "a2a": {
      "jsonrpc": "2.0",
      "method": "tasks/send",
      "params": {"message": "Hello"}
    }
  }
}
```

## Key Files

```
examples/sidecar/
├── setup.sh                              # One-command setup
├── cfn_api.py                            # CFN API (validates L9)
├── agent_a.py                            # Agent A (sender)
├── agent_b.py                            # Agent B (receiver)
├── sidecar/shared/ext_authz_service.py   # Sidecar logic (A2A→L9)
├── sidecar/shared/l9_converter.py        # L8→L9 conversion
└── k8s/envoy-filter.yaml                 # Dual-boundary config
```

## Cleanup

```bash
kind delete cluster --name a2a-demo
```
