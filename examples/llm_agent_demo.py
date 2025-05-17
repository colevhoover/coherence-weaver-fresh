#!/usr/bin/env python3
"""
Coherence Weaver LLM Agent Demo

This script demonstrates how to use the CoherenceWeaverLlmAgent with the new configuration system.
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path to allow imports
script_dir = Path(__file__).parent
parent_dir = script_dir.parent
sys.path.append(str(parent_dir))

# Import agent and configuration utilities
from src.agents.coherence_weaver_llm_agent import CoherenceWeaverLlmAgent, ADK_AVAILABLE
from src.utils.config_loader import initialize_config, get_agent_config
from src.utils.logging_utils import get_logger

# Initialize logging
logger = get_logger("llm_agent_demo")

def load_agent(use_env: bool = False, config_path: str = None):
    """
    Load the Coherence Weaver LLM Agent with the specified configuration method.
    
    Args:
        use_env: Whether to use environment variables for configuration
        config_path: Optional path to a specific configuration file
        
    Returns:
        CoherenceWeaverLlmAgent: The initialized agent
    """
    if not ADK_AVAILABLE:
        logger.error("google.adk.agents is not available. This agent cannot be used.")
        print("\nERROR: The CoherenceWeaverLlmAgent requires google.adk.agents.")
        print("This is a hypothetical import in this example.")
        print("\nIn a real implementation, you would need to:")
        print("1. Install the appropriate package")
        print("2. Adjust the import in src/agents/coherence_weaver_llm_agent.py")
        
        print("\nDemonstrating with mock implementation:")
        # Create a simple mock LlmAgent for demonstration
        class MockLlmAgent:
            def __init__(self, name, model, description, instruction):
                self.name = name
                self.model = model
                self.description = description
                self.instruction = instruction
            
            def __str__(self):
                return f"MockLlmAgent(name='{self.name}', model='{self.model}')"
        
        # Monkey-patch the module
        import src.agents.coherence_weaver_llm_agent as agent_module
        agent_module.LlmAgent = MockLlmAgent
        agent_module.ADK_AVAILABLE = True
    
    if use_env:
        logger.info("Loading agent from environment variables")
        agent = CoherenceWeaverLlmAgent.from_env()
    elif config_path:
        logger.info(f"Loading agent from custom config: {config_path}")
        agent = CoherenceWeaverLlmAgent(config_path=config_path)
    else:
        # Initialize configuration from JSON files
        initialize_config()
        logger.info("Loading agent from standard configuration")
        agent = CoherenceWeaverLlmAgent()
    
    return agent

def main():
    """Main function to run the demo."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Coherence Weaver LLM Agent Demo")
    parser.add_argument("--env", action="store_true", help="Use environment variables for configuration")
    parser.add_argument("--config", type=str, help="Path to custom configuration file")
    args = parser.parse_args()
    
    print("\n======================================")
    print("Coherence Weaver LLM Agent Demo")
    print("======================================\n")
    
    try:
        # Load the agent
        agent = load_agent(use_env=args.env, config_path=args.config)
        llm_agent = agent.get_agent()
        
        # Print agent information
        print(f"Agent Name: {llm_agent.name}")
        print(f"Agent Model: {llm_agent.model}")
        print(f"Agent Description: {llm_agent.description}")
        
        print("\nAgent Instruction:")
        print("-----------------------")
        print(agent.get_instruction())
        
        # Show configuration used
        config = get_agent_config()
        print("\nConfiguration Used:")
        print("-----------------------")
        print(json.dumps(config["agent"], indent=2))
        
        print("\nDemo Complete!")
        print("======================================\n")
        
    except Exception as e:
        logger.error(f"Error in demo: {e}")
        print(f"\nERROR: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
