#!/bin/bash
set -e

CLUSTER_NAME="a2a-demo"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "=========================================="
echo "A2A Sidecar Demo Setup"
echo "=========================================="

# Step 1: Create kind cluster
echo ""
echo "Step 1: Creating kind cluster..."
if kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
    echo "Cluster ${CLUSTER_NAME} already exists. Deleting..."
    kind delete cluster --name ${CLUSTER_NAME}
fi

kind create cluster --name ${CLUSTER_NAME} --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
EOF

# Step 2: Install Istio
echo ""
echo "Step 2: Installing Istio..."
if ! command -v istioctl &> /dev/null; then
    echo "ERROR: istioctl not found. Please install Istio CLI first:"
    echo "  curl -L https://istio.io/downloadIstio | sh -"
    echo "  cd istio-*/bin && export PATH=\$PWD:\$PATH"
    exit 1
fi

istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled

# Step 3: Build Docker images
echo ""
echo "Step 3: Building Docker images..."

cd "${REPO_ROOT}"

# Build sidecar image
echo "Building a2a-sidecar..."
docker build -t a2a-sidecar:latest -f sidecar/envoy/Dockerfile .

# Build demo images
cd examples/sidecar
echo "Building mock-cfn..."
docker build -t mock-cfn:latest -f Dockerfile.mock_cfn .
echo "Building agent-b..."
docker build -t agent-b:latest -f Dockerfile.agent_b .
echo "Building agent-a..."
docker build -t agent-a:latest -f Dockerfile.agent_a .

# Step 4: Load images into kind
echo ""
echo "Step 4: Loading images into kind..."
kind load docker-image a2a-sidecar:latest --name ${CLUSTER_NAME}
kind load docker-image mock-cfn:latest --name ${CLUSTER_NAME}
kind load docker-image agent-b:latest --name ${CLUSTER_NAME}
kind load docker-image agent-a:latest --name ${CLUSTER_NAME}

# Step 5: Deploy to k8s
echo ""
echo "Step 5: Deploying to Kubernetes..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/mock-cfn.yaml
kubectl apply -f k8s/agent-b.yaml

echo "Waiting for Agent B to be ready..."
kubectl wait --for=condition=ready pod -l app=agent-b -n a2a-demo --timeout=120s

echo "Deploying Agent A..."
kubectl apply -f k8s/agent-a.yaml

# Step 6: Show logs
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Watch logs:"
echo "  Mock CFN API:  kubectl logs -f -n a2a-demo deployment/mock-cfn"
echo "  Agent B:       kubectl logs -f -n a2a-demo deployment/agent-b -c agent-b"
echo "  Agent B Sidecar: kubectl logs -f -n a2a-demo deployment/agent-b -c a2a-sidecar"
echo "  Agent A:       kubectl logs -f -n a2a-demo pod/agent-a -c agent-a"
echo "  Agent A Sidecar: kubectl logs -f -n a2a-demo pod/agent-a -c a2a-sidecar"
echo ""
echo "Cleanup:"
echo "  kind delete cluster --name ${CLUSTER_NAME}"
echo ""
