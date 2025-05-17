#!/usr/bin/env python3
"""
A simple demonstration of the Coherence Weaver agent functionality.
"""

import os
import sys
import json
from src.agents.coherence_weaver_agent import CoherenceWeaverAgent
from src.models.agent_models import MessageRole, Message

def main():
    """Run a simple demonstration of the Coherence Weaver agent."""
    print("\n=== Coherence Weaver Simple Agent Demo ===\n")
    
    # Initialize the agent
    agent = CoherenceWeaverAgent(
        name="Demo Agent",
        description="A demonstration of the Coherence Weaver agent"
    )
    
    print(f"Agent initialized with ID: {agent.agent_id}")
    print(f"Name: {agent.name}")
    print(f"Description: {agent.description}")
    print(f"Version: {agent.version}")
    print(f"Capabilities: {len(agent.capabilities)}")
    
    for i, capability in enumerate(agent.capabilities):
        print(f"\nCapability {i+1}: {capability.name}")
        print(f"Description: {capability.description}")
        if capability.parameters:
            print("Parameters:")
            for param, details in capability.parameters.items():
                print(f"  - {param}: {details.get('description', 'No description')}")
    
    # Create a conversation
    conversation_id = agent.create_conversation(
        system_prompt="This is a test conversation with the Coherence Weaver agent."
    )
    print(f"\nCreated conversation with ID: {conversation_id}")
    
    # Add a message to the conversation
    agent.add_message(
        conversation_id=conversation_id,
        role=MessageRole.USER,
        content="Hello, can you help me coordinate a group of specialized AI agents for data analysis?"
    )
    print("Added user message to conversation")
    
    # Generate a response
    response = agent.generate_response(conversation_id)
    print("\nAgent response:")
    print(response.content)
    
    print("\n=== Demo completed successfully ===")

if __name__ == "__main__":
    main()
