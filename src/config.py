"""
Configuration Module

This module handles loading and validating configuration settings from environment variables.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path))

# Default values
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_GENAI_MODEL = "gemini-1.5-pro"
DEFAULT_AGENT_TEMPERATURE = 0.2
DEFAULT_AGENT_TOP_P = 0.95
DEFAULT_AGENT_TOP_K = 40
DEFAULT_A2A_PROTOCOL_VERSION = "0.1"

# Configuration values loaded from environment variables
HOST = os.getenv("HOST", DEFAULT_HOST)
PORT = int(os.getenv("PORT", DEFAULT_PORT))
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
LOG_LEVEL = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)

# Google API configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GENAI_MODEL = os.getenv("GENAI_MODEL", DEFAULT_GENAI_MODEL)

# Agent configuration
AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", DEFAULT_AGENT_TEMPERATURE))
AGENT_TOP_P = float(os.getenv("AGENT_TOP_P", DEFAULT_AGENT_TOP_P))
AGENT_TOP_K = int(os.getenv("AGENT_TOP_K", DEFAULT_AGENT_TOP_K))

# A2A configuration
A2A_PROTOCOL_VERSION = os.getenv("A2A_PROTOCOL_VERSION", DEFAULT_A2A_PROTOCOL_VERSION)
COORDINATION_STRATEGY = os.getenv("COORDINATION_STRATEGY", "centralized")


def validate_config() -> Optional[str]:
    """
    Validate the configuration settings.
    
    Returns:
        Optional[str]: Error message if configuration is invalid, None otherwise
    """
    # Check if PORT is a valid port number
    if not 1 <= PORT <= 65535:
        return f"Invalid PORT value: {PORT}. Must be between 1 and 65535."
    
    # Check if LOG_LEVEL is valid
    valid_log_levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    if LOG_LEVEL.upper() not in valid_log_levels:
        return f"Invalid LOG_LEVEL: {LOG_LEVEL}. Must be one of {valid_log_levels}."
    
    # Check if temperature is valid
    if not 0.0 <= AGENT_TEMPERATURE <= 1.0:
        return f"Invalid AGENT_TEMPERATURE: {AGENT_TEMPERATURE}. Must be between 0.0 and 1.0."
    
    # Check if top_p is valid
    if not 0.0 <= AGENT_TOP_P <= 1.0:
        return f"Invalid AGENT_TOP_P: {AGENT_TOP_P}. Must be between 0.0 and 1.0."
    
    # Check if top_k is valid
    if AGENT_TOP_K <= 0:
        return f"Invalid AGENT_TOP_K: {AGENT_TOP_K}. Must be greater than 0."
    
    # If using generative AI features, check if GOOGLE_API_KEY is provided
    # This is a soft validation since some features might not require the API key
    if not GOOGLE_API_KEY:
        print("WARNING: GOOGLE_API_KEY is not set. Generative AI features will not work.")
    
    return None


def get_config() -> Dict[str, Any]:
    """
    Get the current configuration settings.
    
    Returns:
        Dict[str, Any]: Dictionary of configuration settings
    """
    return {
        "server": {
            "host": HOST,
            "port": PORT,
            "debug": DEBUG
        },
        "logging": {
            "level": LOG_LEVEL
        },
        "api": {
            "google_api_key": GOOGLE_API_KEY,
            "genai_model": GENAI_MODEL
        },
        "agent": {
            "temperature": AGENT_TEMPERATURE,
            "top_p": AGENT_TOP_P,
            "top_k": AGENT_TOP_K
        },
        "a2a": {
            "protocol_version": A2A_PROTOCOL_VERSION,
            "coordination_strategy": COORDINATION_STRATEGY
        }
    }
