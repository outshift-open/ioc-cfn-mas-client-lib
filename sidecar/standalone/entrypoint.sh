#!/bin/bash
# Entrypoint script for A2A sidecar container (standalone mode)
# Starts both Envoy proxy and ext_authz service
# Note: iptables setup is handled by init container

set -e

echo "========================================="
echo "A2A Sidecar (Standalone - No Istio)"
echo "========================================="

# Start ext_authz gRPC service in background
# This service handles A2A message interception and CFN integration
# Envoy calls this service via gRPC for authorization decisions on each request
echo "Starting ext_authz gRPC service..."
python -m sidecar.shared.ext_authz_service \
    --cfn-url="${CFN_URL}" \
    --workspace-id="${WORKSPACE_ID}" \
    --mas-id="${MAS_ID}" &

EXT_AUTHZ_PID=$!

# Wait for ext_authz to be ready (check gRPC port 9001)
echo "Waiting for ext_authz service to be ready..."
for i in $(seq 1 30); do
    if nc -z 127.0.0.1 9001 2>/dev/null; then
        echo "ext_authz service is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "ERROR: ext_authz service failed to start within 30 seconds"
        kill $EXT_AUTHZ_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Start Envoy proxy (running as envoy user UID 1337 via securityContext)
echo "Starting Envoy proxy..."
exec envoy -c /etc/envoy/envoy.yaml

# If Envoy exits, kill ext_authz
kill $EXT_AUTHZ_PID 2>/dev/null || true
