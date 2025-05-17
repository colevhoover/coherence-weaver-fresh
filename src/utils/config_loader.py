"""
Configuration Loader

This module provides utilities for loading and using JSON configuration files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

from ..models.memory_models import MemorySystemConfig
from ..models.server_models import SystemConfig


def load_config_file(filename: str) -> Dict[str, Any]:
    """
    Load a configuration file from the config directory.
    
    Args:
        filename (str): Name of the configuration file to load
        
    Returns:
        Dict[str, Any]: Loaded configuration
        
    Raises:
        FileNotFoundError: If the configuration file does not exist
    """
    config_dir = Path(__file__).parent.parent.parent / "config"
    config_path = config_dir / filename
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, "r") as f:
        return json.load(f)


def get_agent_config() -> Dict[str, Any]:
    """
    Get the agent configuration.
    
    Returns:
        Dict[str, Any]: Agent configuration
    """
    return load_config_file("agent_config.json")


def get_memory_config() -> Dict[str, Any]:
    """
    Get the memory configuration.
    
    Returns:
        Dict[str, Any]: Memory configuration
    """
    return load_config_file("memory_config.json")


def get_server_config() -> Dict[str, Any]:
    """
    Get the server configuration.
    
    Returns:
        Dict[str, Any]: Server configuration
    """
    return load_config_file("server_config.json")


def get_memory_system_config() -> MemorySystemConfig:
    """
    Get the memory system configuration as a structured Pydantic model.
    
    Returns:
        MemorySystemConfig: The memory system configuration
    """
    memory_config_dict = get_memory_config()
    return MemorySystemConfig.from_config_dict(memory_config_dict)


def get_system_config() -> SystemConfig:
    """
    Get the server system configuration as a structured Pydantic model.
    
    Returns:
        SystemConfig: The server system configuration
    """
    server_config_dict = get_server_config()
    return SystemConfig.from_config_dict(server_config_dict)


def update_env_from_config():
    """
    Update environment variables based on the configuration files.
    This allows seamless integration with the existing config module.
    """
    # Skip if explicitly requested
    if os.environ.get("SKIP_JSON_CONFIG", "").lower() in ("true", "1", "t"):
        return "Skipping JSON configuration as requested"
    
    # Update from agent config
    try:
        agent_config = get_agent_config()
        if "agent" in agent_config:
            os.environ["GENAI_MODEL"] = agent_config["agent"].get("model", "gemini-2.0-flash")
    except FileNotFoundError:
        # If agent_config.json doesn't exist yet, that's okay
        pass
    
    # Update from memory config
    try:
        memory_config = get_memory_config()
        if "memory" in memory_config:
            memory_type = memory_config["memory"].get("type")
            if memory_type:
                os.environ["MEMORY_TYPE"] = memory_type
        
        if "session" in memory_config:
            session_type = memory_config["session"].get("type")
            if session_type:
                os.environ["SESSION_TYPE"] = session_type
                
            # If using database session, set the DB URL
            if session_type == "database" and "alternatives" in memory_config["session"]:
                db_config = memory_config["session"]["alternatives"].get("database", {})
                if "db_url" in db_config:
                    os.environ["DB_URL"] = db_config["db_url"]
    except FileNotFoundError:
        # If memory_config.json doesn't exist yet, that's okay
        pass
    
    # Update from server config
    try:
        server_config = get_server_config()
        if "server" in server_config:
            if "host" in server_config["server"]:
                os.environ["HOST"] = server_config["server"]["host"]
            if "port" in server_config["server"]:
                os.environ["PORT"] = str(server_config["server"]["port"])
            if "debug" in server_config["server"]:
                os.environ["DEBUG"] = str(server_config["server"]["debug"]).lower()
        
        if "api" in server_config:
            if "genai_model" in server_config["api"] and not os.environ.get("GENAI_MODEL"):
                os.environ["GENAI_MODEL"] = server_config["api"]["genai_model"]
        
        if "logging" in server_config:
            if "level" in server_config["logging"]:
                os.environ["LOG_LEVEL"] = server_config["logging"]["level"]
    except FileNotFoundError:
        # If server_config.json doesn't exist yet, that's okay
        pass


def initialize_config():
    """
    Initialize the configuration system.
    This should be called at application startup.
    """
    update_env_from_config()
    
    # Return success message
    return "Configuration initialized from JSON files"
