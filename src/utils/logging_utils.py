"""
Logging Utilities Module

This module provides consistent logging functionality across the application.
"""

import logging
import sys
from typing import Optional
from ..config import LOG_LEVEL

# Define log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Set up and configure a logger instance.
    
    Args:
        name: Name of the logger
        level: Optional logging level to override the default
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Determine log level
    log_level_str = level if level else LOG_LEVEL
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Check if logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
    
    return logger

# Create default application logger
app_logger = setup_logger("coherence_weaver")

def get_logger(module_name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        module_name: Name of the module requesting a logger
        
    Returns:
        logging.Logger: Logger instance for the specified module
    """
    return setup_logger(f"coherence_weaver.{module_name}")
