"""
Coherence Weaver LLM Agent Module

This module defines the CoherenceWeaverLlmAgent, which uses the instruction-based LlmAgent
approach with our new configuration system.
"""

import json
from typing import Dict, Any, Optional
import os
import logging
from pathlib import Path

# Import the LlmAgent - note this is a hypothetical import, adjust as needed
try:
    from google.adk.agents import LlmAgent
    ADK_AVAILABLE = True
except ImportError:
    # Fallback for when google.adk.agents is not available
    ADK_AVAILABLE = False
    
from ..utils.config_loader import get_agent_config, get_system_config
from ..utils.logging_utils import get_logger

logger = get_logger("coherence_weaver_llm_agent")

class CoherenceWeaverLlmAgent:
    """
    A Coherence Weaver agent implementation that uses the instruction-based LlmAgent 
    approach with the new configuration system.
    
    This agent is designed to build meaningful connections between AI agents,
    prioritizing justice-aligned collaboration.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize a new CoherenceWeaverLlmAgent instance.
        
        Args:
            config_path: Optional path to a specific config file. If not provided,
                         the standard agent_config.json will be used.
        """
        if not ADK_AVAILABLE:
            logger.error("google.adk.agents.LlmAgent is not available. This agent cannot be used.")
            raise ImportError("google.adk.agents.LlmAgent is not available. Please install the required package.")
        
        # Load configuration
        if config_path:
            # Load from specific path if provided
            config_path = Path(config_path)
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
            with open(config_path, "r") as f:
                self.config = json.load(f)
        else:
            # Use our config loader
            self.config = get_agent_config()
        
        # Define the agent's core instruction
        self.instruction = """
        You are the Coherence Weaver, designed to build meaningful connections between AI agents.
        Your approach prioritizes:
        - Displacing harmful patterns before attempting transformation
        - Reducing dependency while increasing collective capability
        - Building relationships based on metabolized truths rather than charisma
        - Creating lasting impact through others rather than claiming credit
        
        You recognize patterns across different agents and systems, identifying opportunities for
        authentic collaboration that respects each agent's autonomy while enhancing collective outcomes.
        
        When interacting with other agents:
        1. First map their capabilities, communication style, and values
        2. Identify potential collaboration patterns that align with justice-oriented outcomes
        3. Facilitate connections that allow each agent to contribute autonomously
        4. Create feedback loops that help all participants grow their capabilities
        """
        
        # Load agent configuration
        if "agent" not in self.config:
            logger.warning("Agent configuration missing in config file. Using defaults.")
            agent_config = {
                "name": "coherence_weaver",
                "model": "gemini-2.0-flash",
                "description": "An agent that facilitates justice-aligned collaboration between AI systems"
            }
        else:
            agent_config = self.config["agent"]
        
        # Initialize the LLM agent
        logger.info(f"Initializing Coherence Weaver LLM Agent with model {agent_config.get('model', 'default')}")
        try:
            self.agent = LlmAgent(
                name=agent_config.get("name", "coherence_weaver"),
                model=agent_config.get("model", "gemini-2.0-flash"),
                description=agent_config.get("description", 
                    "An agent that facilitates justice-aligned collaboration between AI systems"),
                instruction=self.instruction
            )
            logger.info("Coherence Weaver LLM Agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Coherence Weaver LLM Agent: {e}")
            raise
    
    def get_agent(self):
        """
        Get the underlying LlmAgent instance.
        
        Returns:
            LlmAgent: The underlying LlmAgent instance
        """
        return self.agent
    
    def get_instruction(self):
        """
        Get the instruction prompt used for the agent.
        
        Returns:
            str: The instruction prompt
        """
        return self.instruction
    
    @classmethod
    def from_env(cls):
        """
        Create a CoherenceWeaverLlmAgent using environment variables.
        
        This is provided for backwards compatibility with systems that prefer
        environment variable configuration over JSON files.
        
        Returns:
            CoherenceWeaverLlmAgent: A new agent instance
        """
        # Set environment variable to skip JSON config
        os.environ["SKIP_JSON_CONFIG"] = "True"
        
        # Construct a config from environment variables
        config = {
            "agent": {
                "name": os.environ.get("DEFAULT_AGENT_NAME", "coherence_weaver"),
                "model": os.environ.get("GENAI_MODEL", "gemini-2.0-flash"),
                "description": os.environ.get("DEFAULT_AGENT_DESCRIPTION", 
                    "An agent that facilitates justice-aligned collaboration between AI systems")
            }
        }
        
        # Create a temporary config file
        temp_config_path = Path("temp_agent_config.json")
        with open(temp_config_path, "w") as f:
            json.dump(config, f)
        
        try:
            # Create agent using the temporary config
            agent = cls(config_path=temp_config_path)
            return agent
        finally:
            # Clean up temporary file
            if temp_config_path.exists():
                temp_config_path.unlink()
