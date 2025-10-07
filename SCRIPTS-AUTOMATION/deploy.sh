#!/bin/bash

# 🚀 Deployment Script
# Ultra Advanced AI Agent System

set -e

ENVIRONMENT=${1:-production}

echo "🚀 Deploying Ultra Advanced AI Agent System to $ENVIRONMENT..."
echo "================================================================"

# Load environment variables
if [ -f ".env.$ENVIRONMENT" ]; then
    echo "📝 Loading environment variables from .env.$ENVIRONMENT..."
    export $(cat .env.$ENVIRONMENT | grep -v '^#' | xargs)
else
    echo "⚠️  .env.$ENVIRONMENT not found, using .env..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Build Docker images
echo "🐳 Building Docker images..."
docker-compose build

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Start containers
echo "▶️  Starting containers..."
if [ "$ENVIRONMENT" = "production" ]; then
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
else
    docker-compose up -d
fi

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check health
echo "🏥 Checking service health..."
curl -f http://localhost:8000/health || echo "⚠️  API Gateway health check failed"
curl -f http://localhost:8001/health || echo "⚠️  AI Engine health check failed"

echo ""
echo "================================================================"
echo "✅ Deployment to $ENVIRONMENT completed!"
echo ""
echo "📊 Service URLs:"
echo "   - Frontend: http://localhost:3000"
echo "   - API Gateway: http://localhost:8000"
echo "   - AI Engine: http://localhost:8001/docs"
echo "   - Prometheus: http://localhost:9090"
echo "   - Grafana: http://localhost:3001"
echo ""
echo "📝 View logs with: docker-compose logs -f"
echo "🛑 Stop services with: docker-compose down"
echo "================================================================"