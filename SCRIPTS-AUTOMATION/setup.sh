#!/bin/bash

# 🚀 Ultra Advanced AI Agent System - Setup Script

set -e

echo "🌟 Starting Ultra Advanced AI Agent System Setup..."
echo "=================================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys and configuration"
    echo ""
fi

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
if command -v npm &> /dev/null; then
    npm install
    echo "✅ Node.js dependencies installed"
else
    echo "❌ npm not found. Please install Node.js first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if command -v python3 &> /dev/null; then
    cd AI-ML-DEEP-LEARNING-ENGINE
    pip install -r requirements.txt
    cd ..
    echo "✅ Python dependencies installed"
else
    echo "❌ Python not found. Please install Python 3.11+ first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p LOGS
mkdir -p AI-ML-DEEP-LEARNING-ENGINE/models
mkdir -p BACKEND-MICROSERVICES-ECOSYSTEM/api-gateway-service/logs
echo "✅ Directories created"

# Check Docker
echo "🐳 Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed"
    docker --version
else
    echo "⚠️  Docker not found. Please install Docker to use containerized deployment."
fi

# Check Docker Compose
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose is installed"
    docker-compose --version
else
    echo "⚠️  Docker Compose not found."
fi

echo ""
echo "=================================================="
echo "✅ Setup completed successfully!"
echo ""
echo "📚 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Start services with: npm run dev (development) or docker-compose up (production)"
echo "3. Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - API Gateway: http://localhost:8000"
echo "   - AI Engine: http://localhost:8001"
echo "   - API Docs: http://localhost:8001/docs"
echo ""
echo "🌟 Welcome to the World's Most Advanced AI Agent System!"
echo "=================================================="