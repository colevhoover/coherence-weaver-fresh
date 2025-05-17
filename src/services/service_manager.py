"""
Service Manager Module

This module provides the ServiceManager class for initializing and managing
memory and session services based on configuration.
"""

from typing import Dict, Any, Optional
import os
import logging

# Import memory services from Google ADK (if available)
try:
    from google.adk.memory import InMemoryMemoryService, VertexAiRagMemoryService
    MEMORY_SERVICES_AVAILABLE = True
except ImportError:
    MEMORY_SERVICES_AVAILABLE = False
    
# Import session services from Google ADK (if available)
try:
    from google.adk.sessions import InMemorySessionService, DatabaseSessionService
    SESSION_SERVICES_AVAILABLE = True
except ImportError:
    SESSION_SERVICES_AVAILABLE = False

from ..utils.config_loader import get_memory_config, get_memory_system_config
from ..utils.logging_utils import get_logger

logger = get_logger("service_manager")


# Mock classes for when Google ADK is not available
class MockInMemoryMemoryService:
    """Mock implementation of InMemoryMemoryService for demonstration."""
    def __init__(self):
        self.storage = {}
        logger.info("Initialized MockInMemoryMemoryService")
    
    def store(self, key, data):
        self.storage[key] = data
        return True
    
    def retrieve(self, key):
        return self.storage.get(key)
    
    def search(self, query, limit=5):
        return []


class MockVertexAiRagMemoryService:
    """Mock implementation of VertexAiRagMemoryService for demonstration."""
    def __init__(self, rag_corpus, similarity_top_k=7):
        self.rag_corpus = rag_corpus
        self.similarity_top_k = similarity_top_k
        self.storage = {}
        logger.info(f"Initialized MockVertexAiRagMemoryService with corpus {rag_corpus}")
    
    def store(self, key, data):
        self.storage[key] = data
        return True
    
    def retrieve(self, key):
        return self.storage.get(key)
    
    def search(self, query, limit=5):
        return []


class MockInMemorySessionService:
    """Mock implementation of InMemorySessionService for demonstration."""
    def __init__(self):
        self.sessions = {}
        logger.info("Initialized MockInMemorySessionService")
    
    def create_session(self, session_id, data):
        self.sessions[session_id] = data
        return True
    
    def get_session(self, session_id):
        return self.sessions.get(session_id)
    
    def update_session(self, session_id, data):
        if session_id not in self.sessions:
            return False
        self.sessions[session_id] = data
        return True
    
    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False


class MockDatabaseSessionService:
    """Mock implementation of DatabaseSessionService for demonstration."""
    def __init__(self, db_url):
        self.db_url = db_url
        self.sessions = {}
        logger.info(f"Initialized MockDatabaseSessionService with URL {db_url}")
    
    def create_session(self, session_id, data):
        self.sessions[session_id] = data
        return True
    
    def get_session(self, session_id):
        return self.sessions.get(session_id)
    
    def update_session(self, session_id, data):
        if session_id not in self.sessions:
            return False
        self.sessions[session_id] = data
        return True
    
    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False


class ServiceManager:
    """
    A manager for memory and session services based on configuration.
    
    This class initializes and provides access to memory and session
    services based on the provided configuration.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize a new ServiceManager with the specified configuration.
        
        Args:
            config: Optional dictionary containing memory and session configuration
                   If not provided, it will be loaded from the configuration files
        """
        self.config = config or get_memory_config()
        self.memory_service = self._initialize_memory_service()
        self.session_service = self._initialize_session_service()
        logger.info("Service manager initialized")
    
    def _initialize_memory_service(self):
        """
        Initialize the memory service based on configuration.
        
        Returns:
            The initialized memory service
        """
        memory_config = self.config.get("memory", {})
        memory_type = memory_config.get("type", "in_memory")
        
        logger.info(f"Initializing memory service of type '{memory_type}'")
        
        if not MEMORY_SERVICES_AVAILABLE:
            logger.warning("Google ADK memory services not available, using mock implementations")
            if memory_type == "vertex_ai" and "alternatives" in memory_config:
                vertex_config = memory_config.get("alternatives", {}).get("vertex_ai", {})
                return MockVertexAiRagMemoryService(
                    rag_corpus=vertex_config.get("corpus_name", ""),
                    similarity_top_k=vertex_config.get("similarity_top_k", 7)
                )
            else:
                return MockInMemoryMemoryService()
        
        # If Google ADK is available, use the actual implementations
        if memory_type == "in_memory":
            return InMemoryMemoryService()
        elif memory_type == "vertex_ai" and "alternatives" in memory_config:
            vertex_config = memory_config.get("alternatives", {}).get("vertex_ai", {})
            return VertexAiRagMemoryService(
                rag_corpus=vertex_config.get("corpus_name", ""),
                similarity_top_k=vertex_config.get("similarity_top_k", 7)
            )
        else:
            # Default to in-memory
            logger.warning(f"Unsupported memory type '{memory_type}', using in-memory")
            return InMemoryMemoryService()
    
    def _initialize_session_service(self):
        """
        Initialize the session service based on configuration.
        
        Returns:
            The initialized session service
        """
        session_config = self.config.get("session", {})
        session_type = session_config.get("type", "in_memory")
        
        logger.info(f"Initializing session service of type '{session_type}'")
        
        if not SESSION_SERVICES_AVAILABLE:
            logger.warning("Google ADK session services not available, using mock implementations")
            if session_type == "database" and "alternatives" in session_config:
                db_config = session_config.get("alternatives", {}).get("database", {})
                return MockDatabaseSessionService(db_url=db_config.get("db_url", ""))
            else:
                return MockInMemorySessionService()
        
        # If Google ADK is available, use the actual implementations
        if session_type == "in_memory":
            return InMemorySessionService()
        elif session_type == "database" and "alternatives" in session_config:
            db_config = session_config.get("alternatives", {}).get("database", {})
            return DatabaseSessionService(db_url=db_config.get("db_url", ""))
        else:
            # Default to in-memory
            logger.warning(f"Unsupported session type '{session_type}', using in-memory")
            return InMemorySessionService()
    
    def get_memory_service(self):
        """
        Get the memory service.
        
        Returns:
            The initialized memory service
        """
        return self.memory_service
    
    def get_session_service(self):
        """
        Get the session service.
        
        Returns:
            The initialized session service
        """
        return self.session_service
    
    @classmethod
    def from_config_model(cls):
        """
        Create a ServiceManager using the strongly-typed configuration model.
        
        This method loads the configuration using the MemorySystemConfig model
        for stronger type validation.
        
        Returns:
            ServiceManager: A new service manager instance
        """
        # Get the typed configuration model
        memory_system_config = get_memory_system_config()
        
        # Convert to dictionary for compatibility
        config = {
            "memory": {
                "type": memory_system_config.memory.type,
                "alternatives": memory_system_config.memory.alternatives
            },
            "session": {
                "type": memory_system_config.session.type,
                "alternatives": memory_system_config.session.alternatives
            }
        }
        
        return cls(config)


# Singleton instance for easy access
_service_manager_instance = None


def get_service_manager() -> ServiceManager:
    """
    Get the global service manager instance.
    
    Returns:
        ServiceManager: The service manager instance
    """
    global _service_manager_instance
    if _service_manager_instance is None:
        _service_manager_instance = ServiceManager()
    return _service_manager_instance


def initialize_services() -> None:
    """
    Initialize the service system.
    This should be called during application startup.
    """
    global _service_manager_instance
    _service_manager_instance = ServiceManager()
    logger.info("Service system initialized")
