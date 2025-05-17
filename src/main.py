"""
Coherence Weaver Main Application

This module provides the main entry point for the Coherence Weaver system,
offering a command-line interface for various operations such as starting
the A2A server, initiating first contact, and orchestrating tasks.
"""

import asyncio
import json
import argparse
import os
from pathlib import Path

from src.agents.coherence_weaver_agent import CoherenceWeaverAgent
from src.services.service_manager import ServiceManager
from src.protocols.first_contact import FirstContactProtocol
from src.protocols.task_orchestration import TaskOrchestration
from src.a2a_client import A2AClient, discover_agent
from src.tools.trust_network import TrustNetwork


def create_trust_network_tools():
    """Create tools for the trust network."""
    trust_network = TrustNetwork()
    return [
        trust_network.assess_trust_tool,
        trust_network.update_trust_tool,
        trust_network.get_trusted_agents_tool
    ]


async def main():
    """Main entry point for the Coherence Weaver application."""
    parser = argparse.ArgumentParser(description="Coherence Weaver Agent CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Start A2A server command
    server_parser = subparsers.add_parser("server", help="Start the A2A server")
    server_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    server_parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    server_parser.add_argument("--config", default="config/agent_config.json", help="Path to agent configuration file")
    
    # First contact command
    contact_parser = subparsers.add_parser("contact", help="Establish first contact with an agent")
    contact_parser.add_argument("--agent-url", required=True, help="URL of the agent to contact")
    contact_parser.add_argument("--message", help="Initial message to send")
    contact_parser.add_argument("--config", default="config/agent_config.json", help="Path to agent configuration file")
    
    # Orchestrate task command
    orchestrate_parser = subparsers.add_parser("orchestrate", help="Orchestrate a collaborative task")
    orchestrate_parser.add_argument("--task", required=True, help="Description of the task to orchestrate")
    orchestrate_parser.add_argument("--agents-file", required=True, help="Path to JSON file with available agents")
    orchestrate_parser.add_argument("--config", default="config/agent_config.json", help="Path to agent configuration file")
    
    # Agent card command
    card_parser = subparsers.add_parser("card", help="Generate or display an Agent Card")
    card_parser.add_argument("--output", help="Path to save the Agent Card as JSON")
    card_parser.add_argument("--config", default="config/agent_config.json", help="Path to agent configuration file")
    
    # Discover agent command
    discover_parser = subparsers.add_parser("discover", help="Discover an agent by retrieving its Agent Card")
    discover_parser.add_argument("--url", required=True, help="URL of the agent to discover")
    discover_parser.add_argument("--output", help="Path to save the discovered Agent Card as JSON")
    
    args = parser.parse_args()
    
    try:
        # Get project root directory
        project_root = Path(__file__).parent.parent
        
        # Ensure config path is relative to project root
        config_path = project_root / args.config if hasattr(args, 'config') else project_root / "config/agent_config.json"
        
        if not config_path.exists():
            print(f"Configuration file not found: {config_path}")
            print("Creating a default configuration...")
            
            # Ensure directory exists
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create a default configuration
            default_config = {
                "name": "coherence-weaver",
                "display_name": "Coherence Weaver",
                "description": "A specialized agent for coordinating interactions between multiple AI agents",
                "version": "1.0.0",
                "api": {
                    "url": "http://localhost:8000/a2a",
                    "auth_token": "default_token_123"
                },
                "memory": {
                    "type": "in_memory"
                },
                "services": {
                    "memory": {
                        "type": "in_memory"
                    },
                    "session": {
                        "type": "in_memory"
                    }
                }
            }
            
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
                
            print(f"Created default configuration at {config_path}")
        
        # Load configuration
        with open(config_path, "r") as f:
            config = json.load(f)
        
        if args.command == "server":
            # Import here to avoid circular imports
            from src.a2a_server import start_server
            print(f"Starting A2A server on {args.host}:{args.port}...")
            start_server(host=args.host, port=args.port, config_path=str(config_path))
            
        elif args.command == "contact":
            # Initialize components
            print("Initializing components...")
            
            # Initialize service manager
            service_manager = ServiceManager(config)
            
            # Initialize agent
            core_agent = CoherenceWeaverAgent(
                agent_id=config.get("name", "coherence-weaver"),
                name=config.get("display_name", "Coherence Weaver"),
                description=config.get("description", "A multi-agent coordination agent")
            )
            
            # Initialize first contact protocol
            first_contact_protocol = FirstContactProtocol(core_agent, service_manager)
            
            print(f"Establishing first contact with agent at {args.agent_url}...")
            result = await first_contact_protocol.initiate_contact(
                agent_url=args.agent_url,
                initial_message=args.message
            )
            
            print("\nFirst Contact Result:")
            print(f"Status: {result.get('status', 'unknown')}")
            print(f"Agent ID: {result.get('agent_id', 'unknown')}")
            
            # Display the first part of the capability assessment
            assessment = result.get('capability_assessment', {}).get('content', '')
            if assessment:
                print("\nCapability Assessment (excerpt):")
                print('\n'.join(assessment.split('\n')[:10]) + '\n...')
            
            # Display the plan summary
            relationship_plan = result.get('relationship_plan', {}).get('content', '')
            if relationship_plan:
                print("\nRelationship Plan Summary (excerpt):")
                print('\n'.join(relationship_plan.split('\n')[:10]) + '\n...')
            
            print(f"\nComplete record stored with ID: {result.get('protocol_id', 'unknown')}")
            
        elif args.command == "orchestrate":
            # Check if agents file exists
            agents_file_path = Path(args.agents_file)
            if not agents_file_path.exists():
                print(f"Agents file not found: {args.agents_file}")
                return
            
            # Load available agents
            with open(agents_file_path, "r") as f:
                available_agents = json.load(f)
            
            # Initialize components
            print("Initializing components...")
            
            # Initialize service manager
            service_manager = ServiceManager(config)
            
            # Initialize agent
            core_agent = CoherenceWeaverAgent(
                agent_id=config.get("name", "coherence-weaver"),
                name=config.get("display_name", "Coherence Weaver"),
                description=config.get("description", "A multi-agent coordination agent")
            )
            
            # Initialize A2A client
            a2a_client = A2AClient(auth_token=config.get("api", {}).get("auth_token", ""))
            
            # Initialize task orchestration protocol
            task_orchestration = TaskOrchestration(core_agent, service_manager, a2a_client)
            
            print(f"Orchestrating task across {len(available_agents)} agents...")
            print(f"Task: {args.task}")
            
            result = await task_orchestration.orchestrate_task(args.task, available_agents)
            
            print("\nTask Orchestration Result:")
            print(f"Status: {result.get('status', 'unknown')}")
            print(f"Orchestration ID: {result.get('orchestration_id', 'unknown')}")
            
            # Display analysis summary
            analysis = result.get('analysis', {}).get('analysis', {}).get('content', '')
            if analysis:
                print("\nTask Analysis Summary (excerpt):")
                print('\n'.join(analysis.split('\n')[:10]) + '\n...')
            
            print(f"\nComplete orchestration record stored with ID: {result.get('orchestration_id', 'unknown')}")
            
        elif args.command == "card":
            from src.utils.agent_card import create_agent_card, save_agent_card_to_file
            
            # Generate an Agent Card
            agent_card = create_agent_card(config)
            
            # Display the card
            print("\nGenerated Agent Card:")
            print(json.dumps(agent_card, indent=2))
            
            # Save to file if requested
            if args.output:
                output_path = Path(args.output)
                save_agent_card_to_file(agent_card, output_path)
                print(f"\nAgent Card saved to: {output_path}")
                
        elif args.command == "discover":
            # Discover an agent
            print(f"Discovering agent at {args.url}...")
            try:
                agent_card = discover_agent(args.url)
                
                # Display the card
                print("\nDiscovered Agent Card:")
                print(json.dumps(agent_card, indent=2))
                
                # Save to file if requested
                if args.output:
                    output_path = Path(args.output)
                    
                    # Ensure directory exists
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(output_path, 'w') as f:
                        json.dump(agent_card, f, indent=2)
                        
                    print(f"\nDiscovered Agent Card saved to: {output_path}")
                    
            except Exception as e:
                print(f"Error discovering agent: {str(e)}")
                
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
