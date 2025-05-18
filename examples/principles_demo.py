"""
Demonstrates how the Coherence Weaver agent applies participatory resilience principles.
"""
import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.core_agent import CoherenceWeaverAgent
from src.models.services import ServiceManager
from src.principles.participatory_resilience import get_principles_by_domain, get_related_principles
from google.adk.runners import Runner
import json

async def demonstrate_principles_application():
    """Demonstrate how the agent applies principles to different scenarios."""
    # Load configuration
    with open("config/config.json", "r") as f:
        config = json.load(f)
    
    # Initialize components
    agent_manager = CoherenceWeaverAgent(config_path="config/config.json")
    core_agent = agent_manager.get_agent()
    service_manager = ServiceManager(config)
    memory_service = service_manager.get_memory_service()
    session_service = service_manager.get_session_service()
    
    # Create a runner
    runner = Runner(
        agent=core_agent,
        session_service=session_service,
        memory_service=memory_service
    )
    
    # Create a test session
    session = {
        "state": {
            "cultural_principles": get_principles_by_domain("Culture"),
            "technical_principles": get_principles_by_domain("Tech"),
            "trade_principles": get_principles_by_domain("Trade"),
            "meta_principles": get_related_principles("principle_cascading"),
            "related_to_shared_power": get_related_principles("shared_power_paradigm")
        },
        "app_name": "coherence_weaver_principles_demo",
        "user_id": "test_user"
    }
    
    # Test scenarios
    scenarios = [
        "How would you coordinate multiple AI agents with different expertise to analyze a large dataset on climate change?",
        "What principles would guide your approach to resolving a conflict between two AI agents with different priorities?",
        "How would you design a system where multiple specialized AI agents can contribute to a complex creative writing task?"
    ]
    
    print("Demonstrating Coherence Weaver Agent with Participatory Resilience Principles\n")
    
    for i, scenario in enumerate(scenarios):
        print(f"\n\nScenario {i+1}: {scenario}\n")
        print("Agent response:")
        
        # Create a clean response accumulator for each scenario
        full_response = ""
        
        async for event in runner.run_async(content=scenario, session=session):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end="", flush=True)
                        full_response += part.text
        
        print("\n\n" + "="*80)
    
    print("\nPrinciples demonstration completed.")

if __name__ == "__main__":
    asyncio.run(demonstrate_principles_application())
