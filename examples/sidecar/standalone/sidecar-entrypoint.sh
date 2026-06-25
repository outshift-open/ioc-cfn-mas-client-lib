# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

#!/bin/bash
# Entrypoint for sidecar container
# Starts IOC CFN L9 gRPC service and Envoy proxy

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

# Start IOC CFN L9 gRPC service in background
echo "Starting IOC CFN L9 gRPC service..."
python /app/sidecar/shared/ioc_cfn_l9_service.py \
    --cfn-url="${CFN_URL}" \
    --workspace-id="${WORKSPACE_ID}" \
    --mas-id="${MAS_ID}" &

CFN_L9_PID=$!

# Wait for CFN L9 service to be ready
echo "Waiting for CFN L9 service to be ready..."
for i in $(seq 1 30); do
    if nc -z 127.0.0.1 9001 2>/dev/null; then
        echo "✓ CFN L9 service is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "ERROR: CFN L9 service failed to start"
        kill $CFN_L9_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Start Envoy proxy (foreground)
echo "Starting Envoy proxy..."
echo "Config: /etc/envoy/envoy.yaml"
exec envoy -c /etc/envoy/envoy.yaml

# If Envoy exits, kill CFN L9 service
kill $CFN_L9_PID 2>/dev/null || true
