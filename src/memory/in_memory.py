"""
In-Memory Implementation

This module provides in-memory implementations of the memory and session interfaces.
"""

import time
from typing import Dict, List, Any, Optional
import logging

from .base_memory import BaseMemory, BaseSession

logger = logging.getLogger(__name__)


class InMemoryMemory(BaseMemory):
    """
    In-memory implementation of the BaseMemory interface.
    
    This implementation stores data in a dictionary in memory.
    It's suitable for development and testing, but not for production
    as data is lost when the application restarts.
    """
    
    def __init__(self):
        """Initialize the in-memory storage."""
        self._storage = {}
        self._metadata = {}
        logger.info("Initialized in-memory memory storage")
    
    def store(self, key: str, data: Any) -> bool:
        """
        Store data in memory.
        
        Args:
            key: The key to store the data under
            data: The data to store
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._storage[key] = data
            self._metadata[key] = {
                "timestamp": time.time(),
                "type": type(data).__name__
            }
            return True
        except Exception as e:
            logger.error(f"Error storing data: {e}")
            return False
    
    def retrieve(self, key: str) -> Optional[Any]:
        """
        Retrieve data from memory.
        
        Args:
            key: The key to retrieve
            
        Returns:
            Optional[Any]: The retrieved data, or None if not found
        """
        return self._storage.get(key)
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search memory for relevant data.
        
        This simple implementation just does a substring search on keys.
        A more sophisticated implementation would use vector embeddings.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of matches with 'key', 'data', and 'score' fields
        """
        results = []
        
        # Simple substring search
        for key, data in self._storage.items():
            if query.lower() in key.lower():
                score = 1.0  # Simple match score
                results.append({
                    "key": key,
                    "data": data,
                    "score": score,
                    "metadata": self._metadata.get(key, {})
                })
                
        # Sort by score and limit results
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
    
    def delete(self, key: str) -> bool:
        """
        Delete data from memory.
        
        Args:
            key: The key to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        if key in self._storage:
            del self._storage[key]
            if key in self._metadata:
                del self._metadata[key]
            return True
        return False
    
    def clear(self) -> bool:
        """
        Clear all data from memory.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._storage.clear()
            self._metadata.clear()
            return True
        except Exception as e:
            logger.error(f"Error clearing memory: {e}")
            return False


class InMemorySession(BaseSession):
    """
    In-memory implementation of the BaseSession interface.
    
    This implementation stores sessions in a dictionary in memory.
    It's suitable for development and testing, but not for production
    as data is lost when the application restarts.
    """
    
    def __init__(self):
        """Initialize the in-memory session storage."""
        self._sessions = {}
        self._metadata = {}
        logger.info("Initialized in-memory session storage")
    
    def create_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """
        Create a new session.
        
        Args:
            session_id: The session identifier
            data: Initial session data
            
        Returns:
            bool: True if successful, False otherwise
        """
        if session_id in self._sessions:
            logger.warning(f"Session {session_id} already exists, overwriting")
            
        try:
            self._sessions[session_id] = data.copy()
            self._metadata[session_id] = {
                "created_at": time.time(),
                "updated_at": time.time()
            }
            return True
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            return False
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an existing session.
        
        Args:
            session_id: The session identifier
            
        Returns:
            Optional[Dict[str, Any]]: The session data, or None if not found
        """
        session_data = self._sessions.get(session_id)
        if session_data is not None:
            # Return a copy to prevent unintended modifications
            return session_data.copy()
        return None
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """
        Update an existing session.
        
        Args:
            session_id: The session identifier
            data: New session data
            
        Returns:
            bool: True if successful, False otherwise
        """
        if session_id not in self._sessions:
            logger.warning(f"Session {session_id} does not exist, cannot update")
            return False
            
        try:
            self._sessions[session_id] = data.copy()
            if session_id in self._metadata:
                self._metadata[session_id]["updated_at"] = time.time()
            return True
        except Exception as e:
            logger.error(f"Error updating session: {e}")
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: The session identifier
            
        Returns:
            bool: True if successful, False otherwise
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            if session_id in self._metadata:
                del self._metadata[session_id]
            return True
        return False
    
    def list_sessions(self) -> List[str]:
        """
        List all session identifiers.
        
        Returns:
            List[str]: List of session identifiers
        """
        return list(self._sessions.keys())
