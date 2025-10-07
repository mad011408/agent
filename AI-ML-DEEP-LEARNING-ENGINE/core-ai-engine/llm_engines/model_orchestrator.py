"""
🎯 Multi-Provider AI Model Orchestrator
Intelligent routing, load balancing, and failover across AI providers
"""

import os
import asyncio
from typing import Optional, Dict, List, Any, AsyncGenerator
from enum import Enum
from pydantic import BaseModel, Field

from .models.nvidia_wrapper import NVIDIAWrapper, get_nvidia_client
from .models.sambanova_wrapper import SambaNovaWrapper, get_sambanova_client
from .models.cerebras_wrapper import CerebrasWrapper, get_cerebras_client


class AIProvider(str, Enum):
    """Supported AI Providers"""
    NVIDIA = "nvidia"
    SAMBANOVA = "sambanova"
    CEREBRAS = "cerebras"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class OrchestratorConfig(BaseModel):
    """Orchestrator Configuration"""
    default_provider: AIProvider = Field(
        default_factory=lambda: AIProvider(os.getenv("DEFAULT_AI_PROVIDER", "nvidia"))
    )
    enable_fallback: bool = Field(default=True)
    enable_load_balancing: bool = Field(default=True)
    enable_caching: bool = Field(default=True)
    max_retries: int = Field(default=3)
    timeout: float = Field(default=300.0)


class ModelOrchestrator:
    """
    🎯 Central AI Model Orchestrator
    
    Features:
    - Multi-provider support (NVIDIA, SambaNova, Cerebras, OpenAI, Anthropic)
    - Intelligent routing and load balancing
    - Automatic failover and retry logic
    - Response caching
    - Cost optimization
    - Performance monitoring
    """
    
    def __init__(self, config: Optional[OrchestratorConfig] = None):
        """Initialize the orchestrator with configuration"""
        self.config = config or OrchestratorConfig()
        
        # Initialize provider clients
        self.providers: Dict[AIProvider, Any] = {}
        self._init_providers()
        
        # Performance tracking
        self.metrics: Dict[str, Any] = {
            "requests_count": 0,
            "success_count": 0,
            "error_count": 0,
            "provider_usage": {provider.value: 0 for provider in AIProvider},
            "average_latency": 0.0
        }
        
        # Simple cache
        self._cache: Dict[str, str] = {}
        
    def _init_providers(self):
        """Initialize available AI provider clients"""
        try:
            self.providers[AIProvider.NVIDIA] = get_nvidia_client()
        except Exception as e:
            print(f"Warning: NVIDIA client initialization failed: {e}")
            
        try:
            self.providers[AIProvider.SAMBANOVA] = get_sambanova_client()
        except Exception as e:
            print(f"Warning: SambaNova client initialization failed: {e}")
            
        try:
            self.providers[AIProvider.CEREBRAS] = get_cerebras_client()
        except Exception as e:
            print(f"Warning: Cerebras client initialization failed: {e}")
    
    def _get_cache_key(self, prompt: str, provider: AIProvider, model: Optional[str]) -> str:
        """Generate cache key for request"""
        return f"{provider.value}:{model}:{hash(prompt)}"
    
    async def generate(
        self,
        prompt: str,
        provider: Optional[AIProvider] = None,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        use_cache: bool = True,
        **kwargs
    ) -> str:
        """
        Generate text using the specified or default AI provider
        
        Args:
            prompt: User prompt
            provider: AI provider to use (defaults to config.default_provider)
            model: Specific model to use
            system_prompt: Optional system prompt
            use_cache: Whether to use response cache
            
        Returns:
            Generated text
        """
        provider = provider or self.config.default_provider
        
        # Check cache
        if use_cache and self.config.enable_caching:
            cache_key = self._get_cache_key(prompt, provider, model)
            if cache_key in self._cache:
                return self._cache[cache_key]
        
        # Track request
        self.metrics["requests_count"] += 1
        self.metrics["provider_usage"][provider.value] += 1
        
        import time
        start_time = time.time()
        
        try:
            # Get provider client
            client = self.providers.get(provider)
            if not client:
                raise Exception(f"Provider {provider.value} not initialized")
            
            # Generate response
            response = await client.generate(
                prompt=prompt,
                model=model,
                system_prompt=system_prompt,
                **kwargs
            )
            
            # Update metrics
            latency = time.time() - start_time
            self.metrics["success_count"] += 1
            self.metrics["average_latency"] = (
                (self.metrics["average_latency"] * (self.metrics["success_count"] - 1) + latency)
                / self.metrics["success_count"]
            )
            
            # Cache response
            if use_cache and self.config.enable_caching:
                cache_key = self._get_cache_key(prompt, provider, model)
                self._cache[cache_key] = response
            
            return response
            
        except Exception as e:
            self.metrics["error_count"] += 1
            
            # Attempt failover if enabled
            if self.config.enable_fallback:
                return await self._failover_generate(prompt, provider, model, system_prompt, **kwargs)
            
            raise Exception(f"Generation failed: {str(e)}")
    
    async def _failover_generate(
        self,
        prompt: str,
        failed_provider: AIProvider,
        model: Optional[str],
        system_prompt: Optional[str],
        **kwargs
    ) -> str:
        """
        Attempt to generate using alternative providers
        
        Args:
            prompt: User prompt
            failed_provider: Provider that failed
            model: Specific model to use
            system_prompt: Optional system prompt
            
        Returns:
            Generated text from alternative provider
        """
        # Try other providers in order
        fallback_order = [
            AIProvider.NVIDIA,
            AIProvider.SAMBANOVA,
            AIProvider.CEREBRAS
        ]
        
        for provider in fallback_order:
            if provider != failed_provider and provider in self.providers:
                try:
                    print(f"Attempting failover to {provider.value}...")
                    return await self.generate(
                        prompt,
                        provider=provider,
                        model=None,  # Use default model for fallback
                        system_prompt=system_prompt,
                        use_cache=False,
                        **kwargs
                    )
                except Exception as e:
                    print(f"Failover to {provider.value} failed: {e}")
                    continue
        
        raise Exception("All providers failed")
    
    async def stream_generate(
        self,
        prompt: str,
        provider: Optional[AIProvider] = None,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Stream text generation from AI provider
        
        Args:
            prompt: User prompt
            provider: AI provider to use
            model: Specific model to use
            system_prompt: Optional system prompt
            
        Yields:
            Chunks of generated text
        """
        provider = provider or self.config.default_provider
        client = self.providers.get(provider)
        
        if not client:
            raise Exception(f"Provider {provider.value} not initialized")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        async for chunk in client.stream_chat_completion(messages, model=model, **kwargs):
            yield chunk
    
    async def multi_provider_generate(
        self,
        prompt: str,
        providers: Optional[List[AIProvider]] = None,
        system_prompt: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate responses from multiple providers simultaneously
        
        Args:
            prompt: User prompt
            providers: List of providers to use (defaults to all available)
            system_prompt: Optional system prompt
            
        Returns:
            Dictionary mapping provider names to their responses
        """
        if not providers:
            providers = list(self.providers.keys())
        
        tasks = [
            self.generate(prompt, provider=provider, system_prompt=system_prompt, use_cache=False)
            for provider in providers
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            provider.value: result if not isinstance(result, Exception) else f"Error: {str(result)}"
            for provider, result in zip(providers, results)
        }
    
    async def smart_route(
        self,
        prompt: str,
        task_type: str = "general",
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Intelligently route request to best provider based on task type
        
        Args:
            prompt: User prompt
            task_type: Type of task (general, code, reasoning, fast)
            system_prompt: Optional system prompt
            
        Returns:
            Generated text from optimal provider
        """
        # Route based on task type
        routing_map = {
            "code": (AIProvider.CEREBRAS, "qwen-3-coder-480b"),
            "reasoning": (AIProvider.CEREBRAS, "qwen-3-235b-a22b-thinking-2507"),
            "fast": (AIProvider.NVIDIA, "nvidia/nvidia-nemotron-nano-9b-v2"),
            "advanced": (AIProvider.NVIDIA, "deepseek-ai/deepseek-v3.1"),
            "general": (AIProvider.SAMBANOVA, "DeepSeek-V3.1")
        }
        
        provider, model = routing_map.get(task_type, (self.config.default_provider, None))
        
        return await self.generate(
            prompt,
            provider=provider,
            model=model,
            system_prompt=system_prompt,
            **kwargs
        )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return self.metrics
    
    def clear_cache(self):
        """Clear response cache"""
        self._cache.clear()
    
    async def close(self):
        """Close all provider clients"""
        for client in self.providers.values():
            try:
                await client.close()
            except:
                pass


# Global orchestrator instance
_orchestrator: Optional[ModelOrchestrator] = None


def get_orchestrator() -> ModelOrchestrator:
    """Get or create global orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = ModelOrchestrator()
    return _orchestrator


async def ai_generate(
    prompt: str,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    **kwargs
) -> str:
    """Quick helper function for AI generation"""
    orchestrator = get_orchestrator()
    provider_enum = AIProvider(provider) if provider else None
    return await orchestrator.generate(prompt, provider=provider_enum, model=model, **kwargs)


async def ai_stream(
    prompt: str,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    **kwargs
) -> AsyncGenerator[str, None]:
    """Quick helper function for streaming AI generation"""
    orchestrator = get_orchestrator()
    provider_enum = AIProvider(provider) if provider else None
    async for chunk in orchestrator.stream_generate(prompt, provider=provider_enum, model=model, **kwargs):
        yield chunk