"""
Memory Factory Module

This module provides a factory for creating memory and session instances based on configuration.
"""

import logging
from typing import Tuple, Dict, Any, Optional

from ..models.memory_models import MemorySystemConfig, MemoryType, SessionType
from ..utils.config_loader import get_memory_system_config
from .base_memory import BaseMemory, BaseSession
from .in_memory import InMemoryMemory, InMemorySession

# Import other implementations as they are added
# from .vertex_ai import VertexAIMemory
# from .database import DatabaseSession

logger = logging.getLogger(__name__)


class MemoryFactory:
    """
    Factory for creating memory and session instances based on configuration.
    """
    
    @staticmethod
    def create_memory_system() -> Tuple[BaseMemory, BaseSession]:
        """
        Create memory and session instances based on the current configuration.
        
        Returns:
            Tuple[BaseMemory, BaseSession]: A tuple containing the memory and session instances
        """
        try:
            config = get_memory_system_config()
            return MemoryFactory._create_from_config(config)
        except Exception as e:
            logger.error(f"Error creating memory system from config, using defaults: {e}")
            logger.info("Falling back to in-memory implementation")
            return InMemoryMemory(), InMemorySession()
    
    @staticmethod
    def _create_from_config(config: MemorySystemConfig) -> Tuple[BaseMemory, BaseSession]:
        """
        Create memory and session instances from a specific configuration.
        
        Args:
            config: The memory system configuration
            
        Returns:
            Tuple[BaseMemory, BaseSession]: A tuple containing the memory and session instances
        """
        memory = MemoryFactory._create_memory(config.memory.type, config.memory.alternatives)
        session = MemoryFactory._create_session(config.session.type, config.session.alternatives)
        
        logger.info(f"Created memory system with {config.memory.type} memory and {config.session.type} session")
        
        return memory, session
    
    @staticmethod
    def _create_memory(memory_type: str, alternatives: Optional[Dict[str, Dict[str, Any]]] = None) -> BaseMemory:
        """
        Create a memory instance of the specified type.
        
        Args:
            memory_type: The type of memory to create
            alternatives: Alternative configurations for fallback
            
        Returns:
            BaseMemory: The created memory instance
            
        Raises:
            ValueError: If the memory type is not supported
        """
        if memory_type == MemoryType.IN_MEMORY:
            return InMemoryMemory()
        
        # Add more implementations as they are added
        # elif memory_type == MemoryType.VERTEX_AI:
        #     if alternatives and "vertex_ai" in alternatives:
        #         config = alternatives["vertex_ai"]
        #         return VertexAIMemory(
        #             corpus_name=config.get("corpus_name"),
        #             similarity_top_k=config.get("similarity_top_k", 7)
        #         )
        
        # If we get here, the type is not supported or not implemented yet
        logger.warning(f"Memory type {memory_type} not supported, falling back to in-memory")
        return InMemoryMemory()
    
    @staticmethod
    def _create_session(session_type: str, alternatives: Optional[Dict[str, Dict[str, Any]]] = None) -> BaseSession:
        """
        Create a session instance of the specified type.
        
        Args:
            session_type: The type of session to create
            alternatives: Alternative configurations for fallback
            
        Returns:
            BaseSession: The created session instance
            
        Raises:
            ValueError: If the session type is not supported
        """
        if session_type == SessionType.IN_MEMORY:
            return InMemorySession()
        
        # Add more implementations as they are added
        # elif session_type == SessionType.DATABASE:
        #     if alternatives and "database" in alternatives:
        #         config = alternatives["database"]
        #         return DatabaseSession(
        #             db_url=config.get("db_url"),
        #             table_name=config.get("table_name")
        #         )
        
        # If we get here, the type is not supported or not implemented yet
        logger.warning(f"Session type {session_type} not supported, falling back to in-memory")
        return InMemorySession()


# Singleton instance for easy access
_memory_instance = None
_session_instance = None


def get_memory() -> BaseMemory:
    """
    Get the global memory instance.
    
    Returns:
        BaseMemory: The memory instance
    """
    global _memory_instance
    if _memory_instance is None:
        _memory_instance, _ = MemoryFactory.create_memory_system()
    return _memory_instance


def get_session() -> BaseSession:
    """
    Get the global session instance.
    
    Returns:
        BaseSession: The session instance
    """
    global _session_instance
    if _session_instance is None:
        _, _session_instance = MemoryFactory.create_memory_system()
    return _session_instance


def initialize_memory_system() -> None:
    """
    Initialize the memory system.
    This should be called during application startup.
    """
    global _memory_instance, _session_instance
    _memory_instance, _session_instance = MemoryFactory.create_memory_system()
    logger.info("Memory system initialized")
