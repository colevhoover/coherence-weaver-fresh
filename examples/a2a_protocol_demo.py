"""
A2A Protocol Demo

This example demonstrates how to use the Agent-to-Agent (A2A) Protocol
for communication between Coherence Weaver and other agents.
"""

import os
import sys
import json
import time
import uuid
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from coherence_weaver.src.a2a_client import A2AClient, discover_agent, create_conversation
from coherence_weaver.src.utils.agent_card import create_agent_card, save_agent_card_to_file


def setup_demo_environment():
    """Set up the environment for the demo."""
    # Create output directory for agent cards
    output_dir = Path(__file__).parent.parent / "data" / "agent_cards"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load agent config
    config_path = Path(__file__).parent.parent / "config" / "agent_config.json"
    if not config_path.exists():
        print(f"Config file not found at {config_path}")
        print("Creating a sample config for the demo")
        
        config = {
            "name": "coherence-weaver",
            "description": "A specialized agent for coordinating interactions between multiple AI agents",
            "api": {
                "url": "http://localhost:8000/a2a",
                "auth_token": "demo_token_123"
            }
        }
        
        # Create config directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the sample config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
            
        print(f"Created sample config at {config_path}")
    else:
        # Load existing config
        with open(config_path, 'r') as f:
            config = json.load(f)
            
    return config


def demonstrate_agent_card(config):
    """Demonstrate creating and using an Agent Card."""
    print("\n=== AGENT CARD DEMONSTRATION ===")
    
    # Create an A2A-compliant Agent Card
    agent_card = create_agent_card(config)
    print("\nCreated Agent Card:")
    print(json.dumps(agent_card, indent=2))
    
    # Save the Agent Card to a file
    output_file = Path(__file__).parent.parent / "data" / "agent_cards" / "coherence_weaver_card.json"
    save_agent_card_to_file(agent_card, output_file)
    print(f"\nSaved Agent Card to: {output_file}")
    
    return agent_card


def demonstrate_agent_discovery(remote_url):
    """Demonstrate discovering another agent."""
    print("\n=== AGENT DISCOVERY DEMONSTRATION ===")
    
    print(f"\nAttempting to discover agent at: {remote_url}")
    try:
        # In a real scenario, this would fetch the real agent card
        # For demo purposes, we use the discover_agent function
        # but simulate the response
        
        # Simulate a successful discovery
        print(f"Connecting to {remote_url}...")
        
        # Create a simulated agent card for demonstration
        agent_card = {
            "schema_version": "1.0.0",
            "name": "remote-agent",
            "display_name": "Remote Test Agent",
            "description": "A test agent for A2A Protocol demonstration",
            "capabilities": [
                {
                    "name": "knowledge_retrieval",
                    "description": "Retrieve knowledge from various sources"
                }
            ],
            "api": {
                "url": remote_url,
                "auth": {
                    "type": "bearer_token"
                }
            }
        }
        
        print("\nDiscovered Agent Card:")
        print(json.dumps(agent_card, indent=2))
        
        return agent_card
    except Exception as e:
        print(f"\nError discovering agent: {str(e)}")
        print("Using simulated agent card for demonstration purposes")
        
        # Return a simulated agent card
        return {
            "schema_version": "1.0.0",
            "name": "simulated-agent",
            "display_name": "Simulated Agent",
            "description": "A simulated agent for demonstration purposes",
            "capabilities": [
                {
                    "name": "echo",
                    "description": "Echo back messages"
                }
            ],
            "api": {
                "url": remote_url,
                "auth": {
                    "type": "bearer_token"
                }
            }
        }


def demonstrate_agent_communication(remote_url, auth_token=None):
    """Demonstrate communication with another agent."""
    print("\n=== AGENT COMMUNICATION DEMONSTRATION ===")
    
    print(f"\nConnecting to agent at: {remote_url}")
    
    # Create A2A client
    client = A2AClient(base_url=remote_url, auth_token=auth_token)
    
    # For demo purposes, we'll simulate responses
    # In a real scenario, these would be actual API calls
    
    print("\nSubmitting message to agent...")
    message = "Hello, I am Coherence Weaver. I'd like to coordinate on a task."
    
    try:
        # In a real scenario, this would be a real API call
        # For demo purposes, we simulate the response
        
        # Simulate a response
        simulated_response = {
            "jsonrpc": "2.0",
            "result": {
                "message": {
                    "role": "assistant",
                    "content": "Hello, Coherence Weaver. I'm ready to collaborate. What task would you like to coordinate on?"
                }
            },
            "id": str(uuid.uuid4())
        }
        
        print("\nReceived response:")
        print(json.dumps(simulated_response, indent=2))
        
        # Create a task
        print("\nCreating a task...")
        task_description = "Analyze communication patterns between our agent teams"
        
        # Simulate task creation
        simulated_task_response = {
            "jsonrpc": "2.0",
            "result": {
                "task_id": f"task_{uuid.uuid4().hex[:8]}",
                "status": "created"
            },
            "id": str(uuid.uuid4())
        }
        
        task_id = simulated_task_response["result"]["task_id"]
        print(f"\nCreated task with ID: {task_id}")
        
        # Get task status
        print("\nChecking task status...")
        
        # Simulate task status
        simulated_status_response = {
            "jsonrpc": "2.0",
            "result": {
                "task_id": task_id,
                "status": "in_progress",
                "progress": 25,
                "message": "Analyzing communication patterns..."
            },
            "id": str(uuid.uuid4())
        }
        
        print("\nTask status:")
        print(json.dumps(simulated_status_response, indent=2))
        
        return {
            "task_id": task_id,
            "status": simulated_status_response["result"],
            "messages": [
                {"role": "user", "content": message},
                simulated_response["result"]["message"]
            ]
        }
        
    except Exception as e:
        print(f"\nError communicating with agent: {str(e)}")
        print("Using simulated responses for demonstration purposes")
        
        return {
            "task_id": f"simulated_task_{uuid.uuid4().hex[:8]}",
            "status": {
                "status": "simulated",
                "message": "This is a simulated task for demonstration purposes"
            },
            "messages": [
                {"role": "user", "content": message},
                {"role": "assistant", "content": "Simulated response for demonstration purposes"}
            ]
        }


def demonstrate_multi_agent_conversation():
    """Demonstrate a conversation between multiple agents."""
    print("\n=== MULTI-AGENT CONVERSATION DEMONSTRATION ===")
    
    # Create simulated agents
    agent1 = A2AClient(base_url="http://localhost:8001/a2a", auth_token="token1")  # Coherence Weaver
    agent2 = A2AClient(base_url="http://localhost:8002/a2a", auth_token="token2")  # Knowledge Agent
    agent3 = A2AClient(base_url="http://localhost:8003/a2a", auth_token="token3")  # Planning Agent
    
    agents = [agent1, agent2, agent3]
    agent_names = ["Coherence Weaver", "Knowledge Agent", "Planning Agent"]
    
    print(f"\nCreating a conversation between {len(agents)} agents:")
    for i, name in enumerate(agent_names):
        print(f"  {i+1}. {name} at {agents[i].base_url}")
    
    # Initial message
    initial_message = "Let's collaborate on analyzing the communication patterns in our organization."
    
    # Create a conversation
    print("\nIn a real scenario, we would call create_conversation() to start a multi-agent conversation")
    print("For demonstration purposes, we'll simulate the conversation flow")
    
    conversation_id = f"conv_{uuid.uuid4().hex[:8]}"
    print(f"\nCreated conversation with ID: {conversation_id}")
    
    # Simulate the conversation
    messages = [
        {"role": "user", "content": initial_message},
        {"role": "assistant", "from": "Coherence Weaver", "content": "I'll coordinate this analysis. Knowledge Agent, do you have data on our communication patterns?"},
        {"role": "assistant", "from": "Knowledge Agent", "content": "Yes, I have data from the last 3 months of team communications. The main patterns show clustering around project teams."},
        {"role": "assistant", "from": "Planning Agent", "content": "Based on that data, I can propose an optimized communication structure to improve collaboration."},
        {"role": "assistant", "from": "Coherence Weaver", "content": "Perfect. Let's analyze the data together and develop a comprehensive proposal for improving team communication."}
    ]
    
    # Display the conversation
    print("\nConversation:")
    for msg in messages:
        from_label = f" ({msg['from']})" if 'from' in msg else ""
        print(f"\n[{msg['role']}{from_label}]: {msg['content']}")
        time.sleep(0.5)  # Slight delay for readability
    
    print("\nThis demonstrates how Coherence Weaver can coordinate conversations between multiple agents.")
    
    return {
        "conversation_id": conversation_id,
        "agents": agent_names,
        "messages": messages
    }


def demonstrate_collaboration_initiation():
    """Demonstrate initiating collaboration with another agent."""
    print("\n=== COLLABORATION INITIATION DEMONSTRATION ===")
    
    remote_url = "http://localhost:8004/a2a"
    print(f"\nInitiating collaboration with agent at: {remote_url}")
    
    # In a real scenario, this would use the initiate_collaboration function
    # For demo purposes, we'll simulate the collaboration initiation
    
    message = "Hello, I'd like to collaborate on analyzing communication patterns in a multi-agent system."
    
    try:
        # Simulate the collaboration initiation process
        print(f"\n1. Discovering agent at {remote_url}...")
        
        # Simulate agent card discovery
        agent_card = {
            "schema_version": "1.0.0",
            "name": "ai-researcher",
            "display_name": "AI Research Agent",
            "description": "An agent specializing in AI communication research",
            "capabilities": [
                {
                    "name": "communication_analysis",
                    "description": "Analyze communication patterns between AI agents"
                }
            ],
            "api": {
                "url": remote_url,
                "auth": {
                    "type": "bearer_token"
                }
            }
        }
        
        print("\nDiscovered agent card:")
        print(json.dumps(agent_card, indent=2))
        
        # Simulate creating a task
        print("\n2. Creating a task with the agent...")
        
        task_id = f"collab_{uuid.uuid4().hex[:8]}"
        
        # Simulate collaboration response
        collaboration_info = {
            'agent_card': agent_card,
            'task_id': task_id,
            'message': message,
            'status': 'collaboration_initiated'
        }
        
        print(f"\nCollaboration initiated with task ID: {task_id}")
        
        return collaboration_info
        
    except Exception as e:
        print(f"\nError initiating collaboration: {str(e)}")
        print("Using simulated response for demonstration purposes")
        
        # Return simulated collaboration info
        return {
            'agent_card': {
                "name": "simulated-agent",
                "display_name": "Simulated Agent"
            },
            'task_id': f"simulated_{uuid.uuid4().hex[:8]}",
            'message': message,
            'status': 'simulated_collaboration'
        }


def main():
    """Run the A2A Protocol demonstration."""
    print("==================================================")
    print("  A2A Protocol Demonstration for Coherence Weaver")
    print("==================================================")
    
    # Set up the demo environment
    config = setup_demo_environment()
    
    # Demonstrate creating and using an Agent Card
    agent_card = demonstrate_agent_card(config)
    
    # Demonstrate discovering another agent
    remote_url = "http://localhost:8001/a2a"
    discovered_card = demonstrate_agent_discovery(remote_url)
    
    # Demonstrate communication with another agent
    communication_result = demonstrate_agent_communication(remote_url)
    
    # Demonstrate multi-agent conversation
    conversation_result = demonstrate_multi_agent_conversation()
    
    # Demonstrate collaboration initiation
    collaboration_result = demonstrate_collaboration_initiation()
    
    print("\n==================================================")
    print("  A2A Protocol Demonstration Complete")
    print("==================================================")
    print("\nThis demonstration shows how Coherence Weaver can:")
    print("  1. Create and publish A2A-compliant Agent Cards")
    print("  2. Discover other A2A-compliant agents")
    print("  3. Communicate with other agents using the A2A Protocol")
    print("  4. Coordinate conversations between multiple agents")
    print("  5. Initiate collaboration with other agents")
    
    print("\nIn a real deployment, these interactions would happen with actual A2A-compliant agents.")
    print("For more information, see the A2A Protocol documentation in docs/a2a_protocol.md")


if __name__ == "__main__":
    main()
