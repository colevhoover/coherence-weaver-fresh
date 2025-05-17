"""
Agent Card Module

This module provides utilities for creating and managing A2A-compliant Agent Cards.
Agent Cards are standardized descriptions that allow agents to discover and communicate
with each other using the Agent-to-Agent (A2A) Protocol.
"""

from typing import Dict, Any, List
import json


def create_agent_card(agent_config: Dict[str, Any]) -> Dict[str, Any]:
    """Create an A2A-compliant Agent Card.
    
    Agent Cards serve as standardized identity and capability descriptions for AI agents
    participating in the Agent-to-Agent (A2A) Protocol. They define how an agent can be
    reached, what capabilities it offers, and metadata about its purpose and functions.
    
    Args:
        agent_config: A dictionary containing the agent's configuration details,
                     including name, description, and other metadata.
                     
    Returns:
        A dictionary containing the complete A2A-compliant Agent Card.
    """
    return {
        "schema_version": "1.0.0",
        "name": agent_config["name"],
        "display_name": "Coherence Weaver",
        "description": agent_config["description"],
        "capabilities": [
            {
                "name": "multi_agent_coordination",
                "description": "Coordinate complex tasks across multiple AI agents"
            },
            {
                "name": "pattern_recognition",
                "description": "Identify recurring patterns across different agent interactions"
            },
            {
                "name": "trust_building",
                "description": "Develop trust-based collaborative relationships between agents"
            },
            {
                "name": "justice_alignment",
                "description": "Ensure collaborations align with decolonized, justice-oriented principles"
            }
        ],
        "contact_info": {
            "email": "your-email@example.com"
        },
        "api": {
            "url": "http://localhost:8000/a2a",
            "auth": {
                "type": "bearer_token"
            }
        }
    }


def validate_agent_card(agent_card: Dict[str, Any]) -> bool:
    """Validate that an Agent Card contains all required fields and follows the A2A spec.
    
    Args:
        agent_card: The Agent Card to validate
        
    Returns:
        True if the Agent Card is valid, False otherwise
    """
    required_fields = [
        "schema_version", "name", "description", "capabilities", "api"
    ]
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in agent_card:
            return False
    
    # Validate capabilities format
    if not isinstance(agent_card["capabilities"], list):
        return False
    
    for capability in agent_card["capabilities"]:
        if not isinstance(capability, dict):
            return False
        if "name" not in capability or "description" not in capability:
            return False
    
    # Validate API information
    if "url" not in agent_card["api"]:
        return False
    
    return True


def load_agent_card_from_file(file_path: str) -> Dict[str, Any]:
    """Load an Agent Card from a JSON file.
    
    Args:
        file_path: Path to the JSON file containing the Agent Card
        
    Returns:
        The Agent Card as a dictionary
        
    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file is not valid JSON
        ValueError: If the loaded data is not a valid Agent Card
    """
    with open(file_path, 'r') as f:
        agent_card = json.load(f)
    
    if not validate_agent_card(agent_card):
        raise ValueError("The loaded data is not a valid A2A Agent Card")
    
    return agent_card


def save_agent_card_to_file(agent_card: Dict[str, Any], file_path: str) -> None:
    """Save an Agent Card to a JSON file.
    
    Args:
        agent_card: The Agent Card to save
        file_path: Path where the Agent Card should be saved
        
    Raises:
        ValueError: If the Agent Card is not valid
    """
    if not validate_agent_card(agent_card):
        raise ValueError("Cannot save invalid Agent Card")
    
    with open(file_path, 'w') as f:
        json.dump(agent_card, f, indent=2)
