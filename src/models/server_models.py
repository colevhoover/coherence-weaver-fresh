"""
Server Models Module

This module defines the data models used for server configuration.
"""

from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field


class LogLevel(str, Enum):
    """Enumeration of standard logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ServerConfig(BaseModel):
    """Server configuration settings."""
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    debug: bool = Field(default=False)


class ApiConfig(BaseModel):
    """API configuration settings."""
    genai_model: str = Field(default="gemini-2.0-flash")
    timeout: int = Field(default=30)
    google_api_key: Optional[str] = None


class A2AConfig(BaseModel):
    """Agent-to-Agent protocol configuration."""
    protocol_version: str = Field(default="0.1")
    coordination_strategy: str = Field(default="centralized")
    endpoint_timeout: int = Field(default=10)


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: LogLevel = Field(default=LogLevel.INFO)
    file: Optional[str] = None
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console: bool = Field(default=True)
    
    class Config:
        use_enum_values = True


class SystemConfig(BaseModel):
    """Overall system configuration."""
    server: ServerConfig
    api: ApiConfig
    a2a: A2AConfig
    logging: LoggingConfig
    
    @classmethod
    def from_config_dict(cls, config_dict: Dict[str, Any]) -> "SystemConfig":
        """
        Create a SystemConfig from a configuration dictionary.
        
        Args:
            config_dict: Dictionary containing system configuration
            
        Returns:
            SystemConfig instance
        """
        server_dict = config_dict.get("server", {})
        server_config = ServerConfig(
            host=server_dict.get("host", "0.0.0.0"),
            port=server_dict.get("port", 8000),
            debug=server_dict.get("debug", False)
        )
        
        api_dict = config_dict.get("api", {})
        api_config = ApiConfig(
            genai_model=api_dict.get("genai_model", "gemini-2.0-flash"),
            timeout=api_dict.get("timeout", 30),
            google_api_key=api_dict.get("google_api_key")
        )
        
        a2a_dict = config_dict.get("a2a", {})
        a2a_config = A2AConfig(
            protocol_version=a2a_dict.get("protocol_version", "0.1"),
            coordination_strategy=a2a_dict.get("coordination_strategy", "centralized"),
            endpoint_timeout=a2a_dict.get("endpoint_timeout", 10)
        )
        
        logging_dict = config_dict.get("logging", {})
        logging_config = LoggingConfig(
            level=logging_dict.get("level", "INFO"),
            file=logging_dict.get("file"),
            format=logging_dict.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            console=logging_dict.get("console", True)
        )
        
        return cls(
            server=server_config,
            api=api_config,
            a2a=a2a_config,
            logging=logging_config
        )
