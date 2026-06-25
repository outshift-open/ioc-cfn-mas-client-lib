# Copyright 2026 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

#!/bin/bash
# Complete setup script for sidecar standalone demo
# Creates kind cluster, builds images, and deploys

set -e

CLUSTER_NAME="sidecar-demo"

echo "==========================================="
echo "Sidecar Standalone Demo - Complete Setup"
echo "==========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."
MISSING_DEPS=()

if ! command -v docker &> /dev/null; then
    MISSING_DEPS+=("docker")
fi

if ! command -v kubectl &> /dev/null; then
    MISSING_DEPS+=("kubectl")
fi

if ! command -v kind &> /dev/null; then
    MISSING_DEPS+=("kind")
fi

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo "❌ Missing dependencies: ${MISSING_DEPS[*]}"
    echo ""
    echo "Install them:"
    echo "  - Docker: https://docs.docker.com/get-docker/"
    echo "  - kubectl: https://kubernetes.io/docs/tasks/tools/"
    echo "  - kind: https://kind.sigs.k8s.io/docs/user/quick-start/#installation"
    exit 1
fi

echo "✅ All prerequisites installed"
echo ""

# Check if kind cluster exists
if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    echo "ℹ️  Kind cluster '${CLUSTER_NAME}' already exists"
    read -p "   Delete and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Deleting existing cluster..."
        kind delete cluster --name ${CLUSTER_NAME}
    else
        echo "Using existing cluster"
    fi
fi

# Create kind cluster if it doesn't exist
if ! kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    echo "Creating kind cluster '${CLUSTER_NAME}'..."
    kind create cluster --name ${CLUSTER_NAME}
    echo "✅ Cluster created"
else
    echo "✅ Using existing cluster"
fi

echo ""

# Set kubectl context
echo "Setting kubectl context..."
kubectl config use-context kind-${CLUSTER_NAME}
echo "✅ Context set"
echo ""

# Build Docker images
EXAMPLE_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "${EXAMPLE_DIR}/../../.." && pwd)"

echo "Building Docker images..."

echo "  Building CFN image..."
docker build -t sidecar-standalone-cfn:latest -f "${EXAMPLE_DIR}/demo-apps/Dockerfile.cfn" "${EXAMPLE_DIR}/demo-apps"

echo "  Building Agent A image..."
docker build -t sidecar-standalone-agent-a:latest -f "${EXAMPLE_DIR}/demo-apps/Dockerfile.agent_a" "${EXAMPLE_DIR}/demo-apps"

echo "  Building Agent B image..."
docker build -t sidecar-standalone-agent-b:latest -f "${EXAMPLE_DIR}/demo-apps/Dockerfile.agent_b" "${EXAMPLE_DIR}/demo-apps"

echo "  Building Sidecar image..."
docker build -t sidecar-standalone-sidecar:latest -f "${REPO_ROOT}/sidecar/standalone/Dockerfile" "${REPO_ROOT}"

echo "✅ Images built"
echo ""

# Load images to kind cluster
echo "Loading images to kind cluster..."
kind load docker-image sidecar-standalone-cfn:latest --name ${CLUSTER_NAME}
kind load docker-image sidecar-standalone-agent-a:latest --name ${CLUSTER_NAME}
kind load docker-image sidecar-standalone-agent-b:latest --name ${CLUSTER_NAME}
kind load docker-image sidecar-standalone-sidecar:latest --name ${CLUSTER_NAME}
echo "✅ Images loaded"
echo ""

# Deploy to Kubernetes
echo "Deploying to Kubernetes..."
kubectl apply -f k8s/cfn.yaml
kubectl apply -f k8s/agent-a.yaml
kubectl apply -f k8s/agent-b.yaml
echo "✅ Manifests applied"
echo ""

# Wait for pods to be ready
echo "Waiting for pods to be ready (this may take 1-2 minutes)..."
echo ""

echo "Waiting for CFN..."
kubectl wait --for=condition=ready pod -l app=cfn --timeout=120s 2>/dev/null || {
    echo "⚠️  CFN pod taking longer than expected, checking status..."
    kubectl get pods -l app=cfn
}

echo "Waiting for Agent A..."
kubectl wait --for=condition=ready pod -l app=agent-a --timeout=120s 2>/dev/null || {
    echo "⚠️  Agent A pod taking longer than expected, checking status..."
    kubectl get pods -l app=agent-a
}

echo "Waiting for Agent B..."
kubectl wait --for=condition=ready pod -l app=agent-b --timeout=120s 2>/dev/null || {
    echo "⚠️  Agent B pod taking longer than expected, checking status..."
    kubectl get pods -l app=agent-b
}

echo ""
echo "==========================================="
echo "✅ Setup Complete!"
echo "==========================================="
echo ""
echo "Current status:"
kubectl get pods
echo ""
echo "📋 Useful commands:"
echo ""
echo "  # Watch dual-boundary interception logs:"
echo "  kubectl logs -f -l app=cfn"
echo ""
echo "  # Watch Agent A logs (sender):"
echo "  kubectl logs -f -l app=agent-a -c agent"
echo ""
echo "  # Watch Agent B logs (receiver):"
echo "  kubectl logs -f -l app=agent-b -c agent"
echo ""
echo "  # Watch sidecar logs:"
echo "  kubectl logs -f -l app=agent-a -c sidecar"
echo "  kubectl logs -f -l app=agent-b -c sidecar"
echo ""
echo "  # Check iptables rules:"
echo "  kubectl exec deploy/agent-a -c sidecar -- iptables -t nat -L -n -v"
echo ""
echo "  # Check init container logs:"
echo "  kubectl logs -l app=agent-a -c init-iptables"
echo ""
echo "  # Verify UIDs:"
echo "  kubectl exec deploy/agent-a -c agent -- id"
echo "  kubectl exec deploy/agent-a -c sidecar -- id"
echo ""
echo "  # Cleanup:"
echo "  kubectl delete -f k8s/"
echo "  kind delete cluster --name ${CLUSTER_NAME}"
echo ""
