"""
Base Memory Management

This module defines the base interfaces for memory and session management.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseMemory(ABC):
    """
    Base interface for memory implementations.
    """
    
    @abstractmethod
    def store(self, key: str, data: Any) -> bool:
        """
        Store data in memory.
        
        Args:
            key: The key to store the data under
            data: The data to store
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def retrieve(self, key: str) -> Optional[Any]:
        """
        Retrieve data from memory.
        
        Args:
            key: The key to retrieve
            
        Returns:
            Optional[Any]: The retrieved data, or None if not found
        """
        pass
    
    @abstractmethod
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search memory for relevant data.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of matches, each with 'data' and 'score' fields
        """
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        Delete data from memory.
        
        Args:
            key: The key to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        """
        Clear all data from memory.
        
        Returns:
            bool: True if successful, False otherwise
        """
        pass


class BaseSession(ABC):
    """
    Base interface for session management implementations.
    """
    
    @abstractmethod
    def create_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """
        Create a new session.
        
        Args:
            session_id: The session identifier
            data: Initial session data
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an existing session.
        
        Args:
            session_id: The session identifier
            
        Returns:
            Optional[Dict[str, Any]]: The session data, or None if not found
        """
        pass
    
    @abstractmethod
    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """
        Update an existing session.
        
        Args:
            session_id: The session identifier
            data: New session data
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: The session identifier
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_sessions(self) -> List[str]:
        """
        List all session identifiers.
        
        Returns:
            List[str]: List of session identifiers
        """
        pass
