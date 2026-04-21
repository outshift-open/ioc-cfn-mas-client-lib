#!/bin/bash
# Entrypoint script for A2A sidecar container
# Starts both Envoy proxy and ext_authz service
# Note: iptables setup is handled by Istio

set -e

echo "========================================="
echo "A2A Sidecar (ZTA Pattern with Istio)"
echo "========================================="

# Start ext_authz service in background
echo "Starting ext_authz gRPC service..."
python ext_authz_service.py \
    --cfn-url="${CFN_URL}" \
    --workspace-id="${WORKSPACE_ID}" \
    --mas-id="${MAS_ID}" &

EXT_AUTHZ_PID=$!

# Wait for ext_authz to be ready
sleep 2

# Start Envoy proxy (as envoy user)
echo "Starting Envoy proxy..."
su envoy -c "envoy -c /etc/envoy/envoy.yaml"

# If Envoy exits, kill ext_authz
kill $EXT_AUTHZ_PID 2>/dev/null || true
