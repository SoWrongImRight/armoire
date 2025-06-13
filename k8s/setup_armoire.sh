#!/bin/bash

set -e

CLUSTER_NAME="armoire-dev"
NAMESPACE="armoire"

# Step 1: Create kind cluster if not exists
if ! kind get clusters | grep -q "$CLUSTER_NAME"; then
  echo "Creating Kind cluster: $CLUSTER_NAME..."
  cat <<EOF | kind create cluster --name $CLUSTER_NAME --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 80
        hostPort: 80
      - containerPort: 443
        hostPort: 443
      - containerPort: 30080
        hostPort: 30080
      - containerPort: 30435
        hostPort: 30435
      - containerPort: 5432
        hostPort: 5432
EOF
else
  echo "Kind cluster '$CLUSTER_NAME' already exists."
fi

# Step 2: Create armoire namespace
echo "Creating namespace: $NAMESPACE..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
kubectl config set-context --current --namespace=armoire

# Step 3: Load Docker images into Kind
echo "Loading Docker images into Kind..."
kind load docker-image armoire-backend --name $CLUSTER_NAME
kind load docker-image armoire-frontend --name $CLUSTER_NAME

# Step 4: Label Node
echo "Labeling control-plane node for Ingress..."
kubectl label node armoire-dev-control-plane ingress-ready=true

# Step 5: Install Ingress-NGINX controller
echo "Installing Ingress NGINX controller..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/kind/deploy.yaml

echo "Waiting for Ingress NGINX controller to become ready..."
kubectl wait --namespace ingress-nginx \
  --for=condition=Ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=180s

# Step: 6 Load POSTGRES_PASSWORD from ../.env
echo "Checking for .env file in parent directory..."
ENV_FILE="../.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: $ENV_FILE not found."
  exit 1
fi

echo "Extracting POSTGRES_PASSWORD from $ENV_FILE..."
POSTGRES_PASSWORD=$(grep -E '^POSTGRES_PASSWORD=' "$ENV_FILE" | cut -d '=' -f2- | tr -d '"')

if [ -z "$POSTGRES_PASSWORD" ]; then
  echo "Error: POSTGRES_PASSWORD not set in $ENV_FILE."
  exit 1
fi

echo "Creating Kubernetes secret 'postgres-secret' in namespace $NAMESPACE..."
kubectl create secret generic postgres-secret \
  --from-literal=POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  -n $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -


echo "✅ Setup complete."
