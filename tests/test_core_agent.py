#!/usr/bin/env python3
"""
Test script for the Coherence Weaver Core Agent functionality.
"""

import asyncio
import sys
import os
import json

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.coherence_weaver_agent import CoherenceWeaverAgent
from src.services.service_manager import ServiceManager

# Import Google ADK runner if available
try:
    from google.adk.runners import Runner
    RUNNER_AVAILABLE = True
except ImportError:
    RUNNER_AVAILABLE = False
    print("Warning: google.adk.runners.Runner not available. Using mock implementation.")
    
    # Mock Runner implementation
    class Runner:
        """Mock implementation of Google ADK Runner."""
        def __init__(self, agent, session_service, memory_service):
            self.agent = agent
            self.session_service = session_service
            self.memory_service = memory_service
            print("Initialized Mock Runner")
            
        async def run_async(self, content, session):
            """Mock implementation of run_async method."""
            print(f"Mock runner executing: {content}")
            # Yield a sample response
            class Event:
                def __init__(self, text):
                    self.content = type('Content', (), {'parts': [type('Part', (), {'text': text})]})
            
            yield Event(f"This is a mock response from the Coherence Weaver Agent.\n\n")
            yield Event(f"To coordinate multiple AI agents with different capabilities for a complex data analysis task, I would:\n\n")
            yield Event(f"1. Identify the specific capabilities needed for the task\n")
            yield Event(f"2. Assign specialized roles to each agent based on their strengths\n")
            yield Event(f"3. Establish a clear communication protocol between agents\n")
            yield Event(f"4. Create a central coordination mechanism to manage workflow\n")
            yield Event(f"5. Implement feedback loops to ensure quality and consistency\n")
            yield Event(f"6. Design fallback mechanisms for handling edge cases\n")

async def test_core_agent():
    """Test the core agent's basic functionality."""
    print("Starting core agent test...\n")
    
    # Load configuration
    config_path = "config/config.json"
    if not os.path.exists(config_path):
        # Create a basic config for testing if not exists
        config = {
            "agent": {
                "name": "Coherence Weaver",
                "description": "An agent designed to coordinate and facilitate interactions between multiple agents",
                "version": "0.1.0"
            },
            "memory": {
                "type": "in_memory"
            },
            "session": {
                "type": "in_memory"
            }
        }
        # Save the test config
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
    else:
        # Load existing config
        with open(config_path, "r") as f:
            config = json.load(f)
    
    print(f"Using configuration: {json.dumps(config, indent=2)}\n")
    
    # Initialize components
    print("Initializing components...")
    agent_manager = CoherenceWeaverAgent(
        name=config.get("agent", {}).get("name", "Coherence Weaver"),
        description=config.get("agent", {}).get("description", "An agent for coordination"),
        version=config.get("agent", {}).get("version", "0.1.0")
    )
    core_agent = agent_manager  # In this case, the manager is the agent
    service_manager = ServiceManager(config)
    memory_service = service_manager.get_memory_service()
    session_service = service_manager.get_session_service()
    
    print("Initialized core agent and services\n")
    
    # Create a runner
    runner = Runner(
        agent=core_agent,
        session_service=session_service,
        memory_service=memory_service
    )
    
    print("Created runner\n")
    
    # Create a test session
    session = {
        "state": {
            "test_mode": True
        },
        "app_name": "coherence_weaver_test",
        "user_id": "test_user"
    }
    
    # Test the agent
    test_message = "How would you approach coordinating multiple AI agents with different capabilities to work on a complex data analysis task?"
    print(f"Test message: {test_message}")
    print("\nAgent response:")
    
    async for event in runner.run_async(content=test_message, session=session):
        if event.content and hasattr(event.content, 'parts'):
            for part in event.content.parts:
                if hasattr(part, 'text'):
                    print(part.text, end="", flush=True)
    
    print("\n\nTest completed.")

if __name__ == "__main__":
    asyncio.run(test_core_agent())
