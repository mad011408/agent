"""
🚀 FastAPI Main Application
High-performance AI API with multi-provider support
"""

import os
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from core_ai_engine.llm_engines import (
    get_orchestrator,
    AIProvider,
    ModelOrchestrator
)


# Pydantic Models
class ChatMessage(BaseModel):
    """Chat message model"""
    role: str = Field(..., description="Message role (system, user, assistant)")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Chat completion request"""
    messages: List[ChatMessage] = Field(..., description="Conversation messages")
    provider: Optional[str] = Field(None, description="AI provider (nvidia, sambanova, cerebras)")
    model: Optional[str] = Field(None, description="Specific model to use")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(4096, ge=1, le=32000, description="Maximum tokens to generate")
    stream: bool = Field(False, description="Stream the response")


class GenerateRequest(BaseModel):
    """Simple generation request"""
    prompt: str = Field(..., description="User prompt")
    provider: Optional[str] = Field(None, description="AI provider")
    model: Optional[str] = Field(None, description="Specific model")
    system_prompt: Optional[str] = Field(None, description="System prompt")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(4096, ge=1, le=32000)
    stream: bool = Field(False, description="Stream the response")


class SmartRouteRequest(BaseModel):
    """Smart routing request"""
    prompt: str = Field(..., description="User prompt")
    task_type: str = Field("general", description="Task type: general, code, reasoning, fast, advanced")
    system_prompt: Optional[str] = Field(None, description="System prompt")


class MultiProviderRequest(BaseModel):
    """Multi-provider request"""
    prompt: str = Field(..., description="User prompt")
    providers: Optional[List[str]] = Field(None, description="List of providers to use")
    system_prompt: Optional[str] = Field(None, description="System prompt")


class ChatResponse(BaseModel):
    """Chat completion response"""
    content: str = Field(..., description="Generated content")
    provider: str = Field(..., description="Provider used")
    model: Optional[str] = Field(None, description="Model used")
    usage: Dict[str, int] = Field(default_factory=dict, description="Token usage")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    providers: Dict[str, bool]
    metrics: Dict[str, Any]


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    # Startup
    print("🚀 Starting AI/ML Deep Learning Engine...")
    orchestrator = get_orchestrator()
    print(f"✅ Initialized with {len(orchestrator.providers)} providers")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down AI Engine...")
    await orchestrator.close()
    print("✅ Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="🌟 Ultra Advanced AI Agent System API",
    description="World's Most Advanced Autonomous AI Agent System with Multi-Provider Support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGIN", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "message": "🌟 Welcome to Ultra Advanced AI Agent System",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    orchestrator = get_orchestrator()
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        providers={
            provider.value: True for provider in orchestrator.providers.keys()
        },
        metrics=orchestrator.get_metrics()
    )


@app.post("/v1/chat/completions", tags=["AI"])
async def chat_completions(request: ChatRequest):
    """
    OpenAI-compatible chat completions endpoint
    Supports multiple AI providers with intelligent routing
    """
    orchestrator = get_orchestrator()
    
    try:
        # Convert messages
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Handle streaming
        if request.stream:
            provider_enum = AIProvider(request.provider) if request.provider else None
            
            async def generate_stream():
                async for chunk in orchestrator.stream_generate(
                    prompt=messages[-1]["content"],
                    provider=provider_enum,
                    model=request.model,
                    system_prompt=messages[0]["content"] if messages[0]["role"] == "system" else None,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens
                ):
                    yield f"data: {chunk}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(generate_stream(), media_type="text/event-stream")
        
        # Non-streaming response
        provider_enum = AIProvider(request.provider) if request.provider else None
        user_message = messages[-1]["content"]
        system_message = messages[0]["content"] if messages and messages[0]["role"] == "system" else None
        
        response = await orchestrator.generate(
            prompt=user_message,
            provider=provider_enum,
            model=request.model,
            system_prompt=system_message,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return ChatResponse(
            content=response,
            provider=request.provider or orchestrator.config.default_provider.value,
            model=request.model,
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/generate", tags=["AI"])
async def generate_text(request: GenerateRequest):
    """
    Simple text generation endpoint
    """
    orchestrator = get_orchestrator()
    
    try:
        if request.stream:
            provider_enum = AIProvider(request.provider) if request.provider else None
            
            async def generate_stream():
                async for chunk in orchestrator.stream_generate(
                    prompt=request.prompt,
                    provider=provider_enum,
                    model=request.model,
                    system_prompt=request.system_prompt,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens
                ):
                    yield chunk
            
            return StreamingResponse(generate_stream(), media_type="text/plain")
        
        provider_enum = AIProvider(request.provider) if request.provider else None
        
        response = await orchestrator.generate(
            prompt=request.prompt,
            provider=provider_enum,
            model=request.model,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return {"content": response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/smart-route", tags=["AI"])
async def smart_route(request: SmartRouteRequest):
    """
    Intelligent routing based on task type
    Task types: general, code, reasoning, fast, advanced
    """
    orchestrator = get_orchestrator()
    
    try:
        response = await orchestrator.smart_route(
            prompt=request.prompt,
            task_type=request.task_type,
            system_prompt=request.system_prompt
        )
        
        return {"content": response, "task_type": request.task_type}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/multi-provider", tags=["AI"])
async def multi_provider_generate(request: MultiProviderRequest):
    """
    Generate responses from multiple providers simultaneously
    Compare outputs from different AI models
    """
    orchestrator = get_orchestrator()
    
    try:
        providers = None
        if request.providers:
            providers = [AIProvider(p) for p in request.providers]
        
        responses = await orchestrator.multi_provider_generate(
            prompt=request.prompt,
            providers=providers,
            system_prompt=request.system_prompt
        )
        
        return {"responses": responses}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/providers", tags=["Info"])
async def list_providers():
    """List all available AI providers and their models"""
    orchestrator = get_orchestrator()
    
    from core_ai_engine.llm_engines.models.nvidia_wrapper import NVIDIAWrapper
    from core_ai_engine.llm_engines.models.sambanova_wrapper import SambaNovaWrapper
    from core_ai_engine.llm_engines.models.cerebras_wrapper import CerebrasWrapper
    
    return {
        "providers": {
            "nvidia": {
                "available": AIProvider.NVIDIA in orchestrator.providers,
                "models": NVIDIAWrapper.AVAILABLE_MODELS
            },
            "sambanova": {
                "available": AIProvider.SAMBANOVA in orchestrator.providers,
                "models": SambaNovaWrapper.AVAILABLE_MODELS
            },
            "cerebras": {
                "available": AIProvider.CEREBRAS in orchestrator.providers,
                "models": CerebrasWrapper.AVAILABLE_MODELS
            }
        }
    }


@app.get("/v1/metrics", tags=["Monitoring"])
async def get_metrics():
    """Get performance metrics"""
    orchestrator = get_orchestrator()
    return orchestrator.get_metrics()


@app.post("/v1/cache/clear", tags=["Admin"])
async def clear_cache():
    """Clear response cache"""
    orchestrator = get_orchestrator()
    orchestrator.clear_cache()
    return {"status": "cache cleared"}


# Run with: uvicorn api.main:app --reload --port 8001
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PYTHON_API_PORT", 8001)),
        reload=True
    )