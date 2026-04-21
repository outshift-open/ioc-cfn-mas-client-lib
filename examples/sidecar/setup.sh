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

# Download latest Istio
ISTIO_VERSION="${ISTIO_VERSION:-1.29.0}"
ISTIO_DIR="istio-${ISTIO_VERSION}"

if [ ! -d "${ISTIO_DIR}" ]; then
    echo "Downloading Istio ${ISTIO_VERSION}..."
    curl -L https://istio.io/downloadIstio | ISTIO_VERSION=${ISTIO_VERSION} sh -
else
    echo "Using existing Istio ${ISTIO_VERSION} in ${ISTIO_DIR}"
fi

ISTIOCTL="${ISTIO_DIR}/bin/istioctl"

if [ ! -x "${ISTIOCTL}" ]; then
    echo "ERROR: istioctl not found at ${ISTIOCTL}"
    exit 1
fi

${ISTIOCTL} install --set profile=demo -y
kubectl label namespace default istio-injection=enabled --overwrite

# Step 3: Build Docker images
echo ""
echo "Step 3: Building Docker images..."

cd "${REPO_ROOT}"

# Build ext-authz sidecar image (Istio approach)
echo "Building ext-authz-only..."
docker build -t ext-authz-only:latest -f sidecar/istio/Dockerfile .

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
kind load docker-image ext-authz-only:latest --name ${CLUSTER_NAME}
kind load docker-image mock-cfn:latest --name ${CLUSTER_NAME}
kind load docker-image agent-b:latest --name ${CLUSTER_NAME}
kind load docker-image agent-a:latest --name ${CLUSTER_NAME}

# Step 5: Deploy to k8s
echo ""
echo "Step 5: Deploying to Kubernetes..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/envoy-filter.yaml
kubectl apply -f k8s/mock-cfn.yaml
kubectl apply -f k8s/agent-a.yaml
kubectl apply -f k8s/agent-b.yaml

echo "Waiting for deployments to be ready..."
kubectl rollout status deployment/mock-cfn -n a2a-demo --timeout=120s
kubectl rollout status deployment/agent-a -n a2a-demo --timeout=120s
kubectl rollout status deployment/agent-b -n a2a-demo --timeout=120s

# Step 6: Show logs
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Agents are now sending messages back and forth every ~5-7 seconds."
echo ""
echo "Watch logs:"
echo "  Mock CFN API:    kubectl logs -f -n a2a-demo deployment/mock-cfn"
echo "  Agent A:         kubectl logs -f -n a2a-demo deployment/agent-a -c agent-a"
echo "  Agent A Sidecar: kubectl logs -f -n a2a-demo deployment/agent-a -c ext-authz"
echo "  Agent B:         kubectl logs -f -n a2a-demo deployment/agent-b -c agent-b"
echo "  Agent B Sidecar: kubectl logs -f -n a2a-demo deployment/agent-b -c ext-authz"
echo ""
echo "Cleanup:"
echo "  kind delete cluster --name ${CLUSTER_NAME}"
echo ""
