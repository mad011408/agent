# 🔌 API Examples

Complete examples for using the Ultra Advanced AI Agent System API.

## 📡 Base URLs

- **Development**: `http://localhost:8001`
- **Production**: `https://your-domain.com`

## 🔑 Authentication

Most endpoints are public for development. For production, include JWT token:

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8001/v1/generate
```

## 📚 API Endpoints

### 1. Simple Text Generation

**Endpoint**: `POST /v1/generate`

```bash
curl -X POST http://localhost:8001/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a haiku about AI",
    "provider": "nvidia",
    "model": "deepseek-ai/deepseek-v3.1",
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

**Response**:
```json
{
  "content": "Silicon dreams awake,\nNeural pathways learn and grow,\nFuture unfolds here."
}
```

### 2. Chat Completion (OpenAI Compatible)

**Endpoint**: `POST /v1/chat/completions`

```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful AI assistant."},
      {"role": "user", "content": "Explain machine learning"}
    ],
    "provider": "sambanova",
    "temperature": 0.7
  }'
```

**Response**:
```json
{
  "content": "Machine learning is a subset of AI...",
  "provider": "sambanova",
  "model": "DeepSeek-V3.1",
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 150,
    "total_tokens": 170
  }
}
```

### 3. Streaming Response

**Endpoint**: `POST /v1/generate` (with `stream: true`)

```bash
curl -X POST http://localhost:8001/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Tell me a story about AI",
    "provider": "cerebras",
    "stream": true
  }'
```

**Response** (Server-Sent Events):
```
data: Once
data:  upon
data:  a
data:  time
...
data: [DONE]
```

### 4. Smart Task Routing

**Endpoint**: `POST /v1/smart-route`

Automatically selects the best AI model based on task type.

#### Code Generation
```bash
curl -X POST http://localhost:8001/v1/smart-route \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to sort a list using quicksort",
    "task_type": "code"
  }'
```

Uses: **Cerebras qwen-3-coder-480b**

#### Reasoning Task
```bash
curl -X POST http://localhost:8001/v1/smart-route \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "If all roses are flowers and some flowers fade quickly, what can we conclude?",
    "task_type": "reasoning"
  }'
```

Uses: **Cerebras qwen-3-235b-a22b-thinking-2507**

#### Fast Response
```bash
curl -X POST http://localhost:8001/v1/smart-route \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is 2+2?",
    "task_type": "fast"
  }'
```

Uses: **NVIDIA nvidia-nemotron-nano-9b-v2**

### 5. Multi-Provider Comparison

**Endpoint**: `POST /v1/multi-provider`

Get responses from multiple AI providers simultaneously.

```bash
curl -X POST http://localhost:8001/v1/multi-provider \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is consciousness?",
    "providers": ["nvidia", "sambanova", "cerebras"],
    "system_prompt": "Answer philosophically"
  }'
```

**Response**:
```json
{
  "responses": {
    "nvidia": "Consciousness is the state of awareness...",
    "sambanova": "From a philosophical perspective...",
    "cerebras": "The nature of consciousness remains..."
  }
}
```

### 6. List Available Providers

**Endpoint**: `GET /v1/providers`

```bash
curl http://localhost:8001/v1/providers
```

**Response**:
```json
{
  "providers": {
    "nvidia": {
      "available": true,
      "models": [
        "deepseek-ai/deepseek-v3.1",
        "deepseek-ai/deepseek-r1",
        "meta/llama-3.1-405b-instruct",
        ...
      ]
    },
    "sambanova": {
      "available": true,
      "models": ["DeepSeek-V3.1", "DeepSeek-V3.1-Terminus"]
    },
    "cerebras": {
      "available": true,
      "models": [
        "qwen-3-235b-a22b-thinking-2507",
        "qwen-3-coder-480b",
        ...
      ]
    }
  }
}
```

### 7. Performance Metrics

**Endpoint**: `GET /v1/metrics`

```bash
curl http://localhost:8001/v1/metrics
```

**Response**:
```json
{
  "requests_count": 1523,
  "success_count": 1498,
  "error_count": 25,
  "provider_usage": {
    "nvidia": 650,
    "sambanova": 425,
    "cerebras": 423
  },
  "average_latency": 1.2
}
```

### 8. Health Check

**Endpoint**: `GET /health`

```bash
curl http://localhost:8001/health
```

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "providers": {
    "nvidia": true,
    "sambanova": true,
    "cerebras": true
  },
  "metrics": {
    "requests_count": 1523,
    "success_count": 1498,
    "average_latency": 1.2
  }
}
```

## 🐍 Python Examples

### Using Requests Library

```python
import requests
import json

# Simple generation
def generate_text(prompt, provider="nvidia"):
    response = requests.post(
        "http://localhost:8001/v1/generate",
        json={
            "prompt": prompt,
            "provider": provider,
            "temperature": 0.7
        }
    )
    return response.json()["content"]

# Smart routing
def smart_generate(prompt, task_type="general"):
    response = requests.post(
        "http://localhost:8001/v1/smart-route",
        json={
            "prompt": prompt,
            "task_type": task_type
        }
    )
    return response.json()["content"]

# Multi-provider comparison
def compare_providers(prompt):
    response = requests.post(
        "http://localhost:8001/v1/multi-provider",
        json={
            "prompt": prompt,
            "providers": ["nvidia", "sambanova", "cerebras"]
        }
    )
    return response.json()["responses"]

# Example usage
if __name__ == "__main__":
    # Generate text
    result = generate_text("Explain quantum entanglement")
    print(result)
    
    # Smart routing for code
    code = smart_generate("Write a binary search function", "code")
    print(code)
    
    # Compare providers
    comparisons = compare_providers("What is love?")
    for provider, response in comparisons.items():
        print(f"\n{provider}: {response}")
```

### Streaming Example

```python
import requests

def stream_generate(prompt):
    response = requests.post(
        "http://localhost:8001/v1/generate",
        json={
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            print(line.decode('utf-8'), end='', flush=True)

# Usage
stream_generate("Write a short story about AI")
```

## 🔧 JavaScript/Node.js Examples

```javascript
// Using axios
const axios = require('axios');

const API_URL = 'http://localhost:8001/v1';

// Simple generation
async function generateText(prompt, provider = 'nvidia') {
  const response = await axios.post(`${API_URL}/generate`, {
    prompt,
    provider,
    temperature: 0.7
  });
  return response.data.content;
}

// Smart routing
async function smartGenerate(prompt, taskType = 'general') {
  const response = await axios.post(`${API_URL}/smart-route`, {
    prompt,
    task_type: taskType
  });
  return response.data.content;
}

// Multi-provider
async function compareProviders(prompt) {
  const response = await axios.post(`${API_URL}/multi-provider`, {
    prompt,
    providers: ['nvidia', 'sambanova', 'cerebras']
  });
  return response.data.responses;
}

// Example usage
(async () => {
  try {
    // Generate text
    const result = await generateText('Explain blockchain technology');
    console.log(result);
    
    // Code generation with smart routing
    const code = await smartGenerate('Create a REST API endpoint', 'code');
    console.log(code);
    
    // Compare providers
    const comparisons = await compareProviders('What is the meaning of life?');
    console.log(comparisons);
  } catch (error) {
    console.error('Error:', error.message);
  }
})();
```

## 🎯 Advanced Use Cases

### 1. Code Review Agent

```bash
curl -X POST http://localhost:8001/v1/smart-route \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review this code:\n\ndef factorial(n):\n    if n == 0: return 1\n    return n * factorial(n-1)",
    "task_type": "code",
    "system_prompt": "You are a code review expert. Provide constructive feedback."
  }'
```

### 2. Research Assistant

```bash
curl -X POST http://localhost:8001/v1/smart-route \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Summarize recent advances in quantum computing",
    "task_type": "advanced"
  }'
```

### 3. Reasoning Engine

```bash
curl -X POST http://localhost:8001/v1/smart-route \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Three friends have different favorite colors. Alice doesn'\''t like red. Bob'\''s favorite is not blue. Charlie likes green. What are their favorites?",
    "task_type": "reasoning"
  }'
```

## 📊 Rate Limiting

Default rate limits:
- **100 requests per minute** per IP
- **1000 requests per hour** per user

## 🔒 Best Practices

1. **Use streaming** for long responses
2. **Cache responses** when appropriate
3. **Handle errors gracefully**
4. **Set appropriate timeouts**
5. **Monitor token usage**
6. **Use smart routing** for optimal performance

---

For more examples, see the [GitHub repository](https://github.com/your-repo) or [API Documentation](http://localhost:8001/docs).