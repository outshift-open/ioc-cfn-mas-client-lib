# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

#!/bin/bash
# Quick local test script (for development/debugging)
# This doesn't deploy to K8s, just shows what the setup will do

set -e

echo "==========================================="
echo "Pre-flight Check"
echo "==========================================="
echo ""

# Check all files exist
FILES=(
    "Dockerfile.sidecar"
    "init-iptables.sh"
    "sidecar-entrypoint.sh"
    "setup.sh"
    "k8s/cfn.yaml"
    "k8s/agent-a.yaml"
    "k8s/agent-b.yaml"
    "../sidecar/demo-apps/agent_a.py"
    "../sidecar/demo-apps/agent_b.py"
    "../sidecar/demo-apps/cfn_mock.py"
    "../sidecar/Dockerfile.cfn"
    "../sidecar/Dockerfile.agent_a"
    "../sidecar/Dockerfile.agent_b"
)

echo "Checking files..."
MISSING=0
for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "  ❌ Missing: $file"
        MISSING=1
    else
        echo "  ✅ Found: $file"
    fi
done

if [ $MISSING -eq 1 ]; then
    echo ""
    echo "❌ Some files are missing!"
    exit 1
fi

echo ""
echo "✅ All files present!"
echo ""

# Check Dockerfiles
echo "Checking Dockerfiles..."
for df in Dockerfile.sidecar ../sidecar/Dockerfile.cfn ../sidecar/Dockerfile.agent_a ../sidecar/Dockerfile.agent_b; do
    if grep -q "USER" "$df"; then
        echo "  ✅ $df has USER directive"
    else
        echo "  ⚠️  $df missing USER directive (may be intentional)"
    fi
done

echo ""

# Check K8s manifests for UID settings
echo "Checking K8s manifests for UID configuration..."
for manifest in k8s/agent-a.yaml k8s/agent-b.yaml; do
    if grep -q "runAsUser: 1000" "$manifest"; then
        echo "  ✅ $manifest: Agent runs as UID 1000"
    else
        echo "  ❌ $manifest: Missing runAsUser: 1000 for agent"
    fi

    if grep -q "runAsUser: 1337" "$manifest"; then
        echo "  ✅ $manifest: Sidecar runs as UID 1337"
    else
        echo "  ❌ $manifest: Missing runAsUser: 1337 for sidecar"
    fi
done

echo ""

# Check iptables script for UID exclusion
echo "Checking iptables script..."
if grep -q "uid-owner" init-iptables.sh && grep -q 'ENVOY_UID="1337"' init-iptables.sh; then
    echo "  ✅ iptables script has UID 1337 exclusion"
else
    echo "  ❌ iptables script missing UID 1337 exclusion"
fi

echo ""
echo "==========================================="
echo "✅ Pre-flight check complete!"
echo "==========================================="
echo ""
echo "Ready to run: ./setup.sh"
