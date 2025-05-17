"""
Configuration Test Utility

This module provides functions for testing and displaying configuration settings.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

from ..utils.config_loader import get_agent_config, get_memory_config, get_server_config
from ..utils.config_loader import get_memory_system_config, get_system_config
from ..utils.config_loader import initialize_config
from ..utils.logging_utils import get_logger

logger = get_logger("config_test")


def display_config(config: Dict[str, Any], indent: int = 0) -> None:
    """
    Display a configuration dictionary in a readable format.
    
    Args:
        config: Configuration dictionary to display
        indent: Indentation level
    """
    indent_str = "  " * indent
    for key, value in config.items():
        if isinstance(value, dict):
            print(f"{indent_str}{key}:")
            display_config(value, indent + 1)
        else:
            if key == "google_api_key" and value:
                # Mask API key for security
                value = "***" + str(value)[-4:] if value else None
            print(f"{indent_str}{key}: {value}")


def test_agent_config() -> None:
    """Test loading the agent configuration."""
    try:
        config = get_agent_config()
        print("\n\033[1;32m=== Agent Configuration ===\033[0m")
        display_config(config)
    except Exception as e:
        print(f"\033[1;31mError loading agent configuration: {e}\033[0m")


def test_memory_config() -> None:
    """Test loading the memory configuration."""
    try:
        config = get_memory_config()
        print("\n\033[1;32m=== Memory Configuration ===\033[0m")
        display_config(config)
    except Exception as e:
        print(f"\033[1;31mError loading memory configuration: {e}\033[0m")


def test_server_config() -> None:
    """Test loading the server configuration."""
    try:
        config = get_server_config()
        print("\n\033[1;32m=== Server Configuration ===\033[0m")
        display_config(config)
    except Exception as e:
        print(f"\033[1;31mError loading server configuration: {e}\033[0m")


def test_model_loading() -> None:
    """Test loading configurations into structured models."""
    try:
        memory_config = get_memory_system_config()
        print("\n\033[1;32m=== Memory System Model ===\033[0m")
        print(f"Memory Type: {memory_config.memory.type}")
        print(f"Session Type: {memory_config.session.type}")
        
        system_config = get_system_config()
        print("\n\033[1;32m=== System Model ===\033[0m")
        print(f"Server Host: {system_config.server.host}")
        print(f"Server Port: {system_config.server.port}")
        print(f"Logging Level: {system_config.logging.level}")
    except Exception as e:
        print(f"\033[1;31mError loading models: {e}\033[0m")


def main():
    """Run configuration tests."""
    print("\033[1;34mInitializing configuration...\033[0m")
    initialize_config()
    
    # Test all configuration components
    test_agent_config()
    test_memory_config()
    test_server_config()
    test_model_loading()
    
    print("\n\033[1;34mConfiguration test completed.\033[0m")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test configuration loading")
    parser.add_argument("--env-only", action="store_true", help="Use only environment variables")
    args = parser.parse_args()
    
    if args.env_only:
        import os
        os.environ["SKIP_JSON_CONFIG"] = "True"
    
    main()
