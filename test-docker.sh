#!/bin/bash
echo "🔍 Testing Docker configuration..."

# 1. Check Dockerfile syntax
echo "1. Checking Dockerfile..."
docker build -t test-app .

# 2. Check compose file syntax
echo "2. Checking compose.yaml..."
docker compose config

# 3. Test build
echo "3. Building image..."
docker compose build

# 4. Test startup
echo "4. Testing startup..."
timeout 30s docker compose up || true

# 5. Check running containers
echo "5. Checking containers..."
docker compose ps

echo "✅ Docker test completed!"