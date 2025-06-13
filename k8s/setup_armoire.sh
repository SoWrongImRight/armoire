#!/bin/bash

set -e

CLUSTER_NAME="armoire-dev"
NAMESPACE="armoire"
ARGOCD_NAMESPACE="argocd"

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

# Step 2: Create app namespace
echo "Creating namespace: $NAMESPACE..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
kubectl config set-context --current --namespace=$NAMESPACE

# Step 3: Load Docker images into Kind
echo "Loading Docker images into Kind..."
kind load docker-image armoire-backend --name $CLUSTER_NAME
kind load docker-image armoire-frontend --name $CLUSTER_NAME

# Step 4: Label node for ingress
echo "Labeling control-plane node for Ingress..."
kubectl label node ${CLUSTER_NAME}-control-plane ingress-ready=true --overwrite

# Step 5: Install Ingress-NGINX controller
echo "Installing Ingress NGINX controller..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/kind/deploy.yaml

echo "Waiting for Ingress NGINX controller to become ready..."
kubectl wait --namespace ingress-nginx \
  --for=condition=Ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=180s

# Step 6: Load POSTGRES_PASSWORD from ../.env
ENV_FILE="$(dirname "$0")/../.env"
echo "Checking for .env file..."
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: $ENV_FILE not found."
  exit 1
fi

POSTGRES_PASSWORD=$(grep -E '^POSTGRES_PASSWORD=' "$ENV_FILE" | cut -d '=' -f2- | tr -d '"')
if [ -z "$POSTGRES_PASSWORD" ]; then
  echo "Error: POSTGRES_PASSWORD not set in $ENV_FILE."
  exit 1
fi

echo "Creating Kubernetes secret for PostgreSQL..."
kubectl create secret generic postgres-secret \
  --from-literal=POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  -n $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Step 7: Install Argo CD
echo "Installing Argo CD..."
kubectl create namespace $ARGOCD_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

kubectl apply -n $ARGOCD_NAMESPACE -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo "Waiting for Argo CD server to become ready..."
kubectl wait deployment argocd-server -n $ARGOCD_NAMESPACE --for condition=Available=True --timeout=180s

# Expose Argo CD via port-forward or ingress (optional)
echo "Argo CD installed in namespace '$ARGOCD_NAMESPACE'."
echo "To access Argo CD UI, run:"
echo "  kubectl port-forward svc/argocd-server -n $ARGOCD_NAMESPACE 8080:443"
echo "Then open https://localhost:8080 in your browser."

echo "To get the initial admin password:"
echo "  kubectl -n $ARGOCD_NAMESPACE get secret argocd-initial-admin-secret -o jsonpath=\"{.data.password}\" | base64 -d && echo"

echo "✅ Cluster and Argo CD setup complete."
