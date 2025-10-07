# 🚀 Quick Start Guide

## Welcome to the World's Most Advanced AI Agent System!

This guide will get you up and running in minutes.

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ **Node.js 20+** ([Download](https://nodejs.org/))
- ✅ **Python 3.11+** ([Download](https://www.python.org/))
- ✅ **Docker & Docker Compose** ([Download](https://www.docker.com/))
- ✅ **Git** ([Download](https://git-scm.com/))

## 🎯 Installation Steps

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd ultra-advanced-autonomous-ai-agent-system
```

### Step 2: Run Setup Script

```bash
chmod +x SCRIPTS-AUTOMATION/setup.sh
./SCRIPTS-AUTOMATION/setup.sh
```

This will:
- Create `.env` file from template
- Install Node.js dependencies
- Install Python dependencies
- Create necessary directories

### Step 3: Configure API Keys

Edit the `.env` file with your API credentials:

```bash
# NVIDIA AI (Already configured!)
NVIDIA_API_KEY=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
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1

# SambaNova AI (Already configured!)
SAMBANOVA_API_KEY=29083607-49c3-46fd-a2db-4f5a6b97e41c
SAMBANOVA_BASE_URL=https://api.sambanova.ai/v1/chat/completions

# Cerebras AI (Already configured!)
CEREBRAS_API_KEY=csk-4jrn9fn53mnejw3exk5vpj2tr36k33evjnj99d2t4kthj929
CEREBRAS_BASE_URL=https://api.cerebras.ai/v1/chat/completions
```

**Note**: The API keys are already configured! You can start using the system immediately.

## 🚀 Running the System

### Option 1: Docker (Recommended for Production)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: Development Mode

```bash
# Start all services in development mode
npm run dev
```

This will start:
- 🎨 Frontend (React) on http://localhost:3000
- 🔧 API Gateway (Node.js) on http://localhost:8000
- 🧠 AI Engine (Python/FastAPI) on http://localhost:8001

## 🌐 Access Points

Once running, access the system through:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main web interface |
| **API Gateway** | http://localhost:8000 | API entry point |
| **AI Engine** | http://localhost:8001 | AI/ML backend |
| **API Docs** | http://localhost:8001/docs | Interactive API documentation |
| **Prometheus** | http://localhost:9090 | Metrics & monitoring |
| **Grafana** | http://localhost:3001 | Dashboards (admin/api) |

## 🧪 Quick Test

### Test the AI Engine

```bash
curl -X POST http://localhost:8001/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing in simple terms",
    "provider": "nvidia"
  }'
```

### Test Smart Routing (Code Generation)

```bash
curl -X POST http://localhost:8001/v1/smart-route \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to calculate fibonacci numbers",
    "task_type": "code"
  }'
```

### Test Multi-Provider Comparison

```bash
curl -X POST http://localhost:8001/v1/multi-provider \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the future of artificial intelligence?",
    "providers": ["nvidia", "sambanova", "cerebras"]
  }'
```

## 📊 Available AI Models

### NVIDIA Models
- `deepseek-ai/deepseek-v3.1` (Default)
- `deepseek-ai/deepseek-r1` (Reasoning)
- `qwen/qwen3-next-80b-a3b-thinking`
- `meta/llama-3.1-405b-instruct`
- `nvidia/nvidia-nemotron-nano-9b-v2`
- And 6+ more models!

### SambaNova Models
- `DeepSeek-V3.1` (Default)
- `DeepSeek-V3.1-Terminus`

### Cerebras Models
- `qwen-3-235b-a22b-thinking-2507` (Default - Reasoning)
- `qwen-3-coder-480b` (Code Generation)
- `qwen-3-32b` (Fast)
- `gpt-oss-120b`

## 🎯 Smart Task Routing

The system automatically routes tasks to the best AI model:

| Task Type | Best Provider | Best Model |
|-----------|--------------|------------|
| `code` | Cerebras | qwen-3-coder-480b |
| `reasoning` | Cerebras | qwen-3-235b-a22b-thinking-2507 |
| `fast` | NVIDIA | nvidia-nemotron-nano-9b-v2 |
| `advanced` | NVIDIA | deepseek-v3.1 |
| `general` | SambaNova | DeepSeek-V3.1 |

## 🛠️ Development Commands

```bash
# Start development servers
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Lint code
npm run lint

# Format code
npm run format

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart ai-engine

# Check service health
make health

# View system status
make status
```

## 📚 Next Steps

1. **Explore the API Docs**: http://localhost:8001/docs
2. **Read the Architecture Guide**: `DOCUMENTATION/ARCHITECTURE.md`
3. **Check out Examples**: Try different AI providers and tasks
4. **Monitor Performance**: Visit Grafana dashboards
5. **Customize Agents**: Modify agent configurations

## 🆘 Troubleshooting

### Services won't start?

```bash
# Check if ports are available
lsof -i :3000
lsof -i :8000
lsof -i :8001

# Clean and restart
docker-compose down
docker-compose up --build
```

### Python dependencies error?

```bash
cd AI-ML-DEEP-LEARNING-ENGINE
pip install --upgrade pip
pip install -r requirements.txt
```

### Node.js dependencies error?

```bash
rm -rf node_modules package-lock.json
npm install
```

## 📞 Get Help

- 📖 **Documentation**: `/DOCUMENTATION/`
- 🐛 **Issues**: Report bugs on GitHub
- 💬 **Community**: Join our Discord
- 📧 **Email**: support@aiagent.com

## 🎉 You're All Set!

Your Ultra Advanced AI Agent System is now running!

Start building amazing AI-powered applications! 🚀

---

**Made with ❤️ by the AI Agent System Team**