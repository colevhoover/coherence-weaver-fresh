"""
Memory Models Module

This module defines the data models used for memory and session management configurations.
"""

from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    """Enumeration of supported memory types."""
    IN_MEMORY = "in_memory"
    VERTEX_AI = "vertex_ai"
    CUSTOM = "custom"


class SessionType(str, Enum):
    """Enumeration of supported session types."""
    IN_MEMORY = "in_memory"
    DATABASE = "database"
    CUSTOM = "custom"


class VertexAIMemoryConfig(BaseModel):
    """Configuration for Vertex AI-based memory."""
    corpus_name: str
    similarity_top_k: int = Field(default=7)
    project_id: Optional[str] = None
    location: str = Field(default="global")


class DatabaseSessionConfig(BaseModel):
    """Configuration for database-backed sessions."""
    db_url: str
    table_name: Optional[str] = None
    connection_pool_size: Optional[int] = None
    max_overflow: Optional[int] = None


class MemoryConfig(BaseModel):
    """Configuration for agent memory."""
    type: MemoryType
    alternatives: Optional[Dict[str, Dict[str, Any]]] = None
    vertex_ai: Optional[VertexAIMemoryConfig] = None
    custom_config: Optional[Dict[str, Any]] = None

    class Config:
        use_enum_values = True


class SessionConfig(BaseModel):
    """Configuration for agent sessions."""
    type: SessionType
    alternatives: Optional[Dict[str, Dict[str, Any]]] = None
    database: Optional[DatabaseSessionConfig] = None
    custom_config: Optional[Dict[str, Any]] = None
    
    class Config:
        use_enum_values = True


class MemorySystemConfig(BaseModel):
    """Overall memory system configuration."""
    memory: MemoryConfig
    session: SessionConfig
    
    @classmethod
    def from_config_dict(cls, config_dict: Dict[str, Any]) -> "MemorySystemConfig":
        """
        Create a MemorySystemConfig from a configuration dictionary.
        
        Args:
            config_dict: Dictionary containing memory and session configuration
            
        Returns:
            MemorySystemConfig instance
        """
        memory_dict = config_dict.get("memory", {})
        memory_type = memory_dict.get("type", "in_memory")
        
        # Extract and create VertexAIMemoryConfig if needed
        vertex_ai_config = None
        if memory_type == "vertex_ai" or (
            "alternatives" in memory_dict and "vertex_ai" in memory_dict["alternatives"]
        ):
            vertex_config = memory_dict.get("alternatives", {}).get("vertex_ai", {})
            if vertex_config:
                vertex_ai_config = VertexAIMemoryConfig(
                    corpus_name=vertex_config.get("corpus_name", ""),
                    similarity_top_k=vertex_config.get("similarity_top_k", 7),
                    project_id=vertex_config.get("project_id"),
                    location=vertex_config.get("location", "global")
                )
        
        # Create MemoryConfig
        memory_config = MemoryConfig(
            type=memory_type,
            alternatives=memory_dict.get("alternatives"),
            vertex_ai=vertex_ai_config,
            custom_config=memory_dict.get("custom_config")
        )
        
        session_dict = config_dict.get("session", {})
        session_type = session_dict.get("type", "in_memory")
        
        # Extract and create DatabaseSessionConfig if needed
        db_config = None
        if session_type == "database" or (
            "alternatives" in session_dict and "database" in session_dict["alternatives"]
        ):
            db_dict = session_dict.get("alternatives", {}).get("database", {})
            if db_dict:
                db_config = DatabaseSessionConfig(
                    db_url=db_dict.get("db_url", ""),
                    table_name=db_dict.get("table_name"),
                    connection_pool_size=db_dict.get("connection_pool_size"),
                    max_overflow=db_dict.get("max_overflow")
                )
        
        # Create SessionConfig
        session_config = SessionConfig(
            type=session_type,
            alternatives=session_dict.get("alternatives"),
            database=db_config,
            custom_config=session_dict.get("custom_config")
        )
        
        return cls(memory=memory_config, session=session_config)
