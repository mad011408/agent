"""
⚙️ Configuration Manager
Centralized configuration management
"""

import os
import json
from typing import Any, Dict, Optional
from pathlib import Path


class ConfigManager:
    """
    Configuration Manager
    
    Manages application configuration from environment variables and files
    """
    
    def __init__(self, config_file: Optional[str] = None):
        self.config: Dict[str, Any] = {}
        
        if config_file:
            self.load_from_file(config_file)
        
        # Load environment variables
        self._load_env_vars()
    
    def load_from_file(self, file_path: str) -> None:
        """Load configuration from JSON file"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")
        
        with open(path, 'r') as f:
            self.config = json.load(f)
    
    def _load_env_vars(self) -> None:
        """Load configuration from environment variables"""
        env_config = {
            # AI Providers
            "nvidia_api_key": os.getenv("NVIDIA_API_KEY", ""),
            "nvidia_base_url": os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"),
            "sambanova_api_key": os.getenv("SAMBANOVA_API_KEY", ""),
            "sambanova_base_url": os.getenv("SAMBANOVA_BASE_URL", ""),
            "cerebras_api_key": os.getenv("CEREBRAS_API_KEY", ""),
            "cerebras_base_url": os.getenv("CEREBRAS_BASE_URL", ""),
            
            # Database
            "postgres_host": os.getenv("POSTGRES_HOST", "localhost"),
            "postgres_port": int(os.getenv("POSTGRES_PORT", "5432")),
            "postgres_user": os.getenv("POSTGRES_USER", ""),
            "postgres_password": os.getenv("POSTGRES_PASSWORD", ""),
            "postgres_db": os.getenv("POSTGRES_DB", ""),
            
            "mongodb_uri": os.getenv("MONGODB_URI", ""),
            "redis_host": os.getenv("REDIS_HOST", "localhost"),
            "redis_port": int(os.getenv("REDIS_PORT", "6379")),
            
            # Application
            "default_ai_provider": os.getenv("DEFAULT_AI_PROVIDER", "nvidia"),
            "max_tokens": int(os.getenv("MAX_TOKENS", "4096")),
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
        }
        
        self.config.update(env_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self.config.copy()
    
    def save_to_file(self, file_path: str) -> None:
        """Save configuration to file"""
        with open(file_path, 'w') as f:
            json.dump(self.config, f, indent=2)


# Global config instance
config = ConfigManager()