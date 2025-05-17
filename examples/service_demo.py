#!/usr/bin/env python3
"""
Service Manager Demo

This script demonstrates how to use the ServiceManager with the CoherenceWeaverLlmAgent.
"""

import os
import sys
import json
import uuid
import argparse
from pathlib import Path

# Add parent directory to path to allow imports
script_dir = Path(__file__).parent
parent_dir = script_dir.parent
sys.path.append(str(parent_dir))

# Import required components
from src.utils.config_loader import initialize_config, get_memory_config
from src.utils.logging_utils import get_logger
from src.services.service_manager import (
    ServiceManager, get_service_manager, initialize_services, 
    MEMORY_SERVICES_AVAILABLE, SESSION_SERVICES_AVAILABLE
)
from src.agents.coherence_weaver_llm_agent import CoherenceWeaverLlmAgent, ADK_AVAILABLE

# Initialize logging
logger = get_logger("service_demo")


def create_mock_data():
    """Create mock data for the demo."""
    return {
        "user_id": str(uuid.uuid4()),
        "interactions": [
            {"timestamp": "2025-05-16T12:00:00", "content": "Hello, how can I help?"},
            {"timestamp": "2025-05-16T12:01:15", "content": "I need information about AI collaboration."},
            {"timestamp": "2025-05-16T12:02:30", "content": "Here are some resources on AI collaboration..."}
        ],
        "preferences": {
            "theme": "dark",
            "notification_frequency": "daily",
            "language": "en-US"
        },
        "session_data": {
            "last_active": "2025-05-16T12:05:45",
            "browser": "Chrome",
            "platform": "macOS"
        }
    }


def run_memory_service_demo(service_manager):
    """
    Demonstrate using the memory service.
    
    Args:
        service_manager: The initialized ServiceManager
    """
    print("\n=== Memory Service Demo ===")
    memory_service = service_manager.get_memory_service()
    
    # Get service type
    service_type = memory_service.__class__.__name__
    print(f"Using memory service: {service_type}")
    
    # Create some test data
    test_data = create_mock_data()
    test_key = f"user_data_{test_data['user_id']}"
    
    # Store data
    print(f"\nStoring data with key: {test_key}")
    success = memory_service.store(test_key, test_data)
    print(f"Storage success: {success}")
    
    # Retrieve data
    print("\nRetrieving data...")
    retrieved_data = memory_service.retrieve(test_key)
    if retrieved_data:
        print(f"Retrieved user ID: {retrieved_data['user_id']}")
        print(f"Retrieved {len(retrieved_data['interactions'])} interactions")
    else:
        print("Failed to retrieve data")
    
    # Perform search (may not be meaningful in mock implementation)
    print("\nPerforming search...")
    search_results = memory_service.search("collaboration")
    print(f"Found {len(search_results)} results")
    
    print("Memory service demo completed")


def run_session_service_demo(service_manager):
    """
    Demonstrate using the session service.
    
    Args:
        service_manager: The initialized ServiceManager
    """
    print("\n=== Session Service Demo ===")
    session_service = service_manager.get_session_service()
    
    # Get service type
    service_type = session_service.__class__.__name__
    print(f"Using session service: {service_type}")
    
    # Create a session
    session_id = str(uuid.uuid4())
    session_data = create_mock_data()["session_data"]
    
    print(f"\nCreating session with ID: {session_id}")
    success = session_service.create_session(session_id, session_data)
    print(f"Session creation success: {success}")
    
    # Get session
    print("\nRetrieving session...")
    retrieved_session = session_service.get_session(session_id)
    if retrieved_session:
        print(f"Retrieved session last active: {retrieved_session['last_active']}")
        print(f"Retrieved session browser: {retrieved_session['browser']}")
    else:
        print("Failed to retrieve session")
    
    # Update session
    print("\nUpdating session...")
    session_data["last_active"] = "2025-05-16T13:00:00"
    session_data["new_field"] = "New value"
    success = session_service.update_session(session_id, session_data)
    print(f"Session update success: {success}")
    
    # Get updated session
    updated_session = session_service.get_session(session_id)
    if updated_session:
        print(f"Updated session last active: {updated_session['last_active']}")
        print(f"Updated session new field: {updated_session.get('new_field')}")
    
    # Delete session
    print("\nDeleting session...")
    success = session_service.delete_session(session_id)
    print(f"Session deletion success: {success}")
    
    # Verify deletion
    if not session_service.get_session(session_id):
        print("Session successfully deleted")
    else:
        print("Session still exists")
    
    print("Session service demo completed")


def integrate_with_llm_agent():
    """
    Demonstrate how to integrate the service manager with the LLM agent.
    """
    print("\n=== LLM Agent Integration Demo ===")
    
    if not ADK_AVAILABLE:
        print("LLM Agent is not available (ADK not imported)")
        print("This is a conceptual demonstration only")
    
    # Initialize configuration
    initialize_config()
    
    # Create service manager
    service_manager = ServiceManager()
    
    # Get services
    memory_service = service_manager.get_memory_service()
    session_service = service_manager.get_session_service()
    
    # Create LLM Agent (or mock)
    try:
        agent = CoherenceWeaverLlmAgent()
        print(f"Created agent with model: {agent.config['agent']['model']}")
    except Exception as e:
        print(f"Could not create agent: {e}")
        print("Using conceptual integration only")
    
    # Conceptual integration example
    print("\nConceptual Agent-Service Integration:")
    print("1. Initialize agent with configuration")
    print("2. Pass memory_service to agent for persistent memory")
    print("3. Pass session_service to agent for user session management")
    print("4. Agent uses memory_service.store() to save important information")
    print("5. Agent uses memory_service.search() to find relevant past interactions")
    print("6. Agent uses session_service to maintain conversation context")
    
    # Example of how the integration would work in actual code
    print("\nPseudo-code for integration:")
    print("```python")
    print("def process_user_input(user_id, session_id, input_text):")
    print("    # Get services")
    print("    memory_service = service_manager.get_memory_service()")
    print("    session_service = service_manager.get_session_service()")
    print("    ")
    print("    # Get or create session")
    print("    session = session_service.get_session(session_id) or {}")
    print("    ")
    print("    # Get user history from memory")
    print("    user_data = memory_service.retrieve(f'user_{user_id}') or {")
    print("        'interactions': []")
    print("    }")
    print("    ")
    print("    # Use LLM agent to process input with context")
    print("    agent = get_configured_agent()")
    print("    response = agent.process(")
    print("        input_text,")
    print("        context={")
    print("            'user_history': user_data['interactions'],")
    print("            'session': session")
    print("        }")
    print("    )")
    print("    ")
    print("    # Update memory and session")
    print("    user_data['interactions'].append({")
    print("        'timestamp': current_time(),")
    print("        'input': input_text,")
    print("        'response': response")
    print("    })")
    print("    memory_service.store(f'user_{user_id}', user_data)")
    print("    ")
    print("    # Update session")
    print("    session['last_interaction'] = current_time()")
    print("    session_service.update_session(session_id, session)")
    print("    ")
    print("    return response")
    print("```")


def main():
    """Main function to run the demo."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Service Manager Demo")
    parser.add_argument("--memory-only", action="store_true", help="Run only memory service demo")
    parser.add_argument("--session-only", action="store_true", help="Run only session service demo")
    parser.add_argument("--llm-only", action="store_true", help="Run only LLM integration demo")
    args = parser.parse_args()
    
    print("\n======================================")
    print("Coherence Weaver Service Manager Demo")
    print("======================================\n")
    
    # Print availability of services
    print("Service Availability:")
    print(f"  - Memory Services: {'Available' if MEMORY_SERVICES_AVAILABLE else 'Not Available'}")
    print(f"  - Session Services: {'Available' if SESSION_SERVICES_AVAILABLE else 'Not Available'}")
    print(f"  - LLM Agent: {'Available' if ADK_AVAILABLE else 'Not Available'}\n")
    
    try:
        # Initialize configuration
        initialize_config()
        
        # Initialize the service manager
        initialize_services()
        service_manager = get_service_manager()
        
        # Run demos based on arguments
        if args.memory_only:
            run_memory_service_demo(service_manager)
        elif args.session_only:
            run_session_service_demo(service_manager)
        elif args.llm_only:
            integrate_with_llm_agent()
        else:
            # Run all demos
            run_memory_service_demo(service_manager)
            run_session_service_demo(service_manager)
            integrate_with_llm_agent()
        
        print("\nDemo completed successfully!")
        print("======================================\n")
        
    except Exception as e:
        logger.error(f"Error in demo: {e}")
        print(f"\nERROR: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
