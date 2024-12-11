#!/bin/bash

# Variabel untuk konfigurasi
PROJECT_NAME=${1:-belanak}
DOMAIN=${2:-green-prd-belanak-ext.kiriminaja.com}
NEG="ingress-nginx-neg-controller"
NEG_ZONE="asia-southeast2-a"
MAX_RATE=100

if [ -z "$PROJECT_NAME" ]; then
  echo "Error: PROJECT_NAME is required!"
  echo "Usage: $0 <PROJECT_NAME>"
  exit 1
fi

# Step 1: Check if the Backend Service exists
echo "Checking if Backend Service $PROJECT_NAME-backend exists..."
BACKEND_SERVICE=$(gcloud compute backend-services list --filter="name:$PROJECT_NAME" | grep $PROJECT_NAME )

if [ "$BACKEND_SERVICE" == "$PROJECT_NAME" ]; then
  echo "Backend Service $PROJECT_NAME already exists. Exiting without error."
  exit 0
fi

# Step 1: Create Backend Service
echo "Creating Backend Service for $PROJECT_NAME..."
gcloud compute backend-services create "$PROJECT_NAME" \
    --protocol=HTTP \
    --health-checks=kaj-ingress-healthz \
    --timeout=300 \
    --security-policy="kaj-monitoring" \
    --custom-request-header="X-Real-IP:{client_ip_address}" \
    --custom-request-header="X-Forwarder-For:{client_ip_address}" \
    --global

# Step 2: Add security Policy (For Green)
gcloud compute backend-services update "$PROJECT_NAME" \
    --security-policy=kaj-monitoring \
    --global

# Step 3: Add Backend to Backend Service
echo "Adding Backend to Backend Service..."
gcloud compute backend-services add-backend "$PROJECT_NAME" \
    --network-endpoint-group=$NEG \
    --network-endpoint-group-zone=$NEG_ZONE \
    --balancing-mode=RATE \
    --max-rate-per-endpoint=$MAX_RATE \
    --global


# Step 4: Add Path Matcher to URL Map
echo "Adding Path Matcher to URL Map..."
gcloud compute url-maps add-path-matcher kaj-prd-alb \
    --path-matcher-name="$PROJECT_NAME-path-matcher" \
    --default-service="$PROJECT_NAME-backend" \
    --path-rules="/*=$PROJECT_NAME-backend" \
    --new-hosts="$DOMAIN" \
    --global

# Step 5: Update load balancer
gcloud compute forwarding-rules set-target kaj-prd-frontend-https \
  --target-http-proxy=kaj-prd-alb-target-proxy \
  --global