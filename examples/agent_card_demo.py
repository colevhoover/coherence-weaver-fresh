"""
Agent Card Demo

This example demonstrates how to create, validate, and manage A2A-compliant Agent Cards
for the Coherence Weaver agent using the agent_card utilities.
"""

import os
import json
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import from the src package
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from coherence_weaver.src.utils import (
    create_agent_card,
    validate_agent_card,
    save_agent_card_to_file,
    load_agent_card_from_file
)


def main():
    """Demonstrate the creation and management of an A2A Agent Card."""
    
    # Example agent configuration
    agent_config = {
        "name": "coherence-weaver",
        "description": "A specialized agent for coordinating interactions between multiple AI agents, identifying patterns, and building trust-based collaborative relationships that align with justice-oriented principles."
    }
    
    # Create an A2A-compliant Agent Card
    agent_card = create_agent_card(agent_config)
    
    # Validate the Agent Card
    is_valid = validate_agent_card(agent_card)
    print(f"Agent Card validation result: {is_valid}")
    
    # Create the output directory if it doesn't exist
    output_dir = Path(__file__).parent.parent / "data" / "agent_cards"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the Agent Card to a file
    output_file = output_dir / "coherence_weaver_card.json"
    save_agent_card_to_file(agent_card, output_file)
    print(f"Agent Card saved to: {output_file}")
    
    # Load the Agent Card from the file
    loaded_card = load_agent_card_from_file(output_file)
    
    # Print the Agent Card in a nicely formatted way
    print("\nLoaded Agent Card:")
    print(json.dumps(loaded_card, indent=2))
    
    print("\nA2A Protocol Agent Card is ready for use in agent-to-agent communications")


if __name__ == "__main__":
    main()
