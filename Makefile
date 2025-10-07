# 🌟 Ultra Advanced AI Agent System - Makefile

.PHONY: help setup install build dev test clean docker-build docker-up docker-down deploy

help: ## Show this help message
	@echo '🌟 Ultra Advanced AI Agent System'
	@echo ''
	@echo 'Usage:'
	@echo '  make <target>'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Run initial setup
	@echo "🚀 Running setup..."
	@chmod +x SCRIPTS-AUTOMATION/setup.sh
	@./SCRIPTS-AUTOMATION/setup.sh

install: ## Install all dependencies
	@echo "📦 Installing dependencies..."
	@npm install
	@cd AI-ML-DEEP-LEARNING-ENGINE && pip install -r requirements.txt

build: ## Build all services
	@echo "🔨 Building services..."
	@npm run build

dev: ## Start development servers
	@echo "▶️  Starting development servers..."
	@npm run dev

test: ## Run all tests
	@echo "🧪 Running tests..."
	@npm run test

lint: ## Run linters
	@echo "🔍 Running linters..."
	@npm run lint

format: ## Format code
	@echo "✨ Formatting code..."
	@npm run format

docker-build: ## Build Docker images
	@echo "🐳 Building Docker images..."
	@docker-compose build

docker-up: ## Start Docker containers
	@echo "▶️  Starting Docker containers..."
	@docker-compose up -d

docker-down: ## Stop Docker containers
	@echo "🛑 Stopping Docker containers..."
	@docker-compose down

docker-logs: ## View Docker logs
	@docker-compose logs -f

deploy: ## Deploy to production
	@echo "🚀 Deploying to production..."
	@chmod +x SCRIPTS-AUTOMATION/deploy.sh
	@./SCRIPTS-AUTOMATION/deploy.sh production

clean: ## Clean build artifacts
	@echo "🧹 Cleaning..."
	@rm -rf node_modules
	@rm -rf dist
	@rm -rf build
	@rm -rf logs
	@rm -rf AI-ML-DEEP-LEARNING-ENGINE/__pycache__
	@rm -rf FRONTEND-ECOSYSTEM/ai-powered-ui/dist

status: ## Check service status
	@echo "📊 Service Status:"
	@docker-compose ps

health: ## Check service health
	@echo "🏥 Health Check:"
	@curl -f http://localhost:8000/health || echo "API Gateway: ❌"
	@curl -f http://localhost:8001/health || echo "AI Engine: ❌"

backup: ## Backup databases
	@echo "💾 Creating backup..."
	@chmod +x SCRIPTS-AUTOMATION/backup.sh
	@./SCRIPTS-AUTOMATION/backup.sh

restore: ## Restore databases
	@echo "♻️  Restoring backup..."
	@chmod +x SCRIPTS-AUTOMATION/restore.sh
	@./SCRIPTS-AUTOMATION/restore.sh