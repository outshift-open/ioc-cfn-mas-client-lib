#!/bin/bash
# Entrypoint for sidecar container
# Starts ext_authz gRPC service and Envoy proxy

set -e

echo "==========================================="
echo "A2A Sidecar (Transparent Interception)"
echo "==========================================="
echo "UID: $(id -u)"
echo "User: $(whoami)"
echo ""

# Detect local container IP
LOCAL_IP=$(hostname -i | awk '{print $1}')
echo "Local container IP: ${LOCAL_IP}"
export LOCAL_IP

# Start ext_authz gRPC service in background
echo "Starting ext_authz gRPC service..."
python /app/sidecar/shared/ext_authz_service.py \
    --cfn-url="${CFN_URL}" \
    --workspace-id="${WORKSPACE_ID}" \
    --mas-id="${MAS_ID}" &

EXT_AUTHZ_PID=$!

# Wait for ext_authz to be ready
echo "Waiting for ext_authz service to be ready..."
for i in $(seq 1 30); do
    if nc -z 127.0.0.1 9001 2>/dev/null; then
        echo "✓ ext_authz service is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "ERROR: ext_authz service failed to start"
        kill $EXT_AUTHZ_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Start Envoy proxy (foreground)
echo "Starting Envoy proxy..."
echo "Config: /etc/envoy/envoy.yaml"
exec envoy -c /etc/envoy/envoy.yaml

# If Envoy exits, kill ext_authz
kill $EXT_AUTHZ_PID 2>/dev/null || true
