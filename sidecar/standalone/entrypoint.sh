# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

#!/bin/bash
# Entrypoint script for A2A sidecar container (standalone mode)
# Starts both Envoy proxy and ext_authz service
# Note: iptables setup is handled by init container

set -e

echo "========================================="
echo "A2A Sidecar (Standalone - No Istio)"
echo "========================================="

# Start IOC CFN L9 gRPC service in background
# This service intercepts L8 (A2A) messages, converts to L9, and sends to CFN
# Envoy calls this service via gRPC for authorization decisions on each request
echo "Starting IOC CFN L9 gRPC service..."
python -m sidecar.shared.ioc_cfn_l9_service \
    --cfn-url="${CFN_URL}" \
    --workspace-id="${WORKSPACE_ID}" \
    --mas-id="${MAS_ID}" &

CFN_L9_PID=$!

# Configuration (can be overridden via environment variables)
CFN_L9_PORT="${CFN_L9_PORT:-9001}"

# Wait for CFN L9 service to be ready (check gRPC port)
echo "Waiting for CFN L9 service to be ready on port ${CFN_L9_PORT}..."
for i in $(seq 1 30); do
    if nc -z 127.0.0.1 ${CFN_L9_PORT} 2>/dev/null; then
        echo "CFN L9 service is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "ERROR: CFN L9 service failed to start within 30 seconds"
        kill $CFN_L9_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Start Envoy proxy (running as envoy user UID 1337 via securityContext)
echo "Starting Envoy proxy..."
exec envoy -c /etc/envoy/envoy.yaml

# If Envoy exits, kill CFN L9 service
kill $CFN_L9_PID 2>/dev/null || true
