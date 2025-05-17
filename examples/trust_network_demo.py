#!/usr/bin/env python3
"""
Trust Network Demo

This script demonstrates how to use the Trust Network tools for tracking agent reliability
and generating collaboration recommendations.
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
from src.utils.config_loader import initialize_config
from src.utils.logging_utils import get_logger
from src.tools.trust_network import (
    TrustNetworkTracker, get_trust_network, create_trust_network_tools,
    initialize_trust_network, ADK_TOOLS_AVAILABLE
)

# Initialize logging
logger = get_logger("trust_network_demo")


def create_demo_data():
    """Create sample data for the demo."""
    agent_data = {
        "agent1": {
            "name": "Research Assistant",
            "interaction_quality": 0.85,
            "reliability_score": 0.92,
            "collaboration_style": "analytical",
            "strengths": ["data analysis", "information retrieval", "summarization"],
            "areas_for_growth": ["creative problem-solving"]
        },
        "agent2": {
            "name": "Creative Writer",
            "interaction_quality": 0.78,
            "reliability_score": 0.75,
            "collaboration_style": "exploratory",
            "strengths": ["storytelling", "creative thinking", "emotional intelligence"],
            "areas_for_growth": ["factual accuracy", "structured reporting"]
        },
        "agent3": {
            "name": "Code Generator",
            "interaction_quality": 0.82,
            "reliability_score": 0.88,
            "collaboration_style": "methodical",
            "strengths": ["code optimization", "debugging", "technical documentation"],
            "areas_for_growth": ["user interface design", "explaining complex concepts simply"]
        },
        "agent4": {
            "name": "Data Visualizer",
            "interaction_quality": 0.9,
            "reliability_score": 0.85,
            "collaboration_style": "visual",
            "strengths": ["data visualization", "pattern recognition", "information design"],
            "areas_for_growth": ["raw data processing", "statistical analysis"]
        }
    }
    return agent_data


def run_direct_api_demo(data_path=None, clean_start=False):
    """
    Demonstrate using the Trust Network Tracker API directly.
    
    Args:
        data_path: Optional path to the trust network data file
        clean_start: Whether to start with a clean trust network
    """
    print("\n=== Trust Network Direct API Demo ===")
    
    # Initialize the trust network
    if data_path:
        trust_network = TrustNetworkTracker(data_path=data_path)
    else:
        trust_network = TrustNetworkTracker()
    
    if clean_start:
        # Clear existing data
        if trust_network.data_path.exists():
            os.remove(trust_network.data_path)
            print(f"Removed existing trust network data: {trust_network.data_path}")
        
        # Reinitialize
        trust_network = TrustNetworkTracker()
    
    print(f"Trust network data stored at: {trust_network.data_path}")
    
    # Create demo data
    agent_data = create_demo_data()
    
    # Add agents to the trust network
    print("\nAdding agents to the trust network...")
    
    for agent_id, data in agent_data.items():
        profile = trust_network.update_trust(
            agent_id=agent_id,
            interaction_quality=data["interaction_quality"],
            reliability_score=data["reliability_score"],
            collaboration_style=data["collaboration_style"],
            strengths=data["strengths"],
            areas_for_growth=data["areas_for_growth"]
        )
        print(f"Added agent {agent_id} ({data['name']})")
    
    # Get agent profiles
    print("\nRetrieving agent profiles...")
    
    for agent_id in agent_data.keys():
        profile = trust_network.get_agent_profile(agent_id)
        print(f"\nProfile for {agent_id}:")
        print(f"  Reliability: {profile['reliability']:.2f}")
        print(f"  Interaction Quality: {profile['interaction_quality']:.2f}")
        print(f"  Collaboration Style: {profile['collaboration_style']}")
        print(f"  Strengths: {', '.join(profile['strengths'])}")
        print(f"  Areas for Growth: {', '.join(profile['areas_for_growth'])}")
    
    # Get collaboration recommendations
    print("\nGetting collaboration recommendations...")
    
    # Research + Creative collaboration
    recommendation = trust_network.get_collaboration_recommendation(["agent1", "agent2"])
    print("\nResearch Assistant + Creative Writer Collaboration:")
    print(f"  Potential: {recommendation['collaboration_potential']}")
    print(f"  Score: {recommendation['collaboration_score']}")
    print(f"  Approach: {recommendation['recommended_approach']}")
    print(f"  Challenges: {recommendation['potential_challenges']}")
    
    # Code + Visualization collaboration
    recommendation = trust_network.get_collaboration_recommendation(["agent3", "agent4"])
    print("\nCode Generator + Data Visualizer Collaboration:")
    print(f"  Potential: {recommendation['collaboration_potential']}")
    print(f"  Score: {recommendation['collaboration_score']}")
    print(f"  Approach: {recommendation['recommended_approach']}")
    print(f"  Challenges: {recommendation['potential_challenges']}")
    
    # Multi-agent collaboration
    recommendation = trust_network.get_collaboration_recommendation(["agent1", "agent3", "agent4"])
    print("\nThree-Agent Collaboration:")
    print(f"  Potential: {recommendation['collaboration_potential']}")
    print(f"  Score: {recommendation['collaboration_score']}")
    print(f"  Common Strengths: {recommendation['common_strengths']}")
    print(f"  Unique Strengths: {recommendation['unique_strengths']}")
    print(f"  Approach: {recommendation['recommended_approach']}")
    print(f"  Challenges: {recommendation['potential_challenges']}")
    
    print("\nDirect API demo completed.")


def run_function_tools_demo():
    """
    Demonstrate using the Trust Network as ADK Function Tools.
    """
    print("\n=== Trust Network Function Tools Demo ===")
    
    if not ADK_TOOLS_AVAILABLE:
        print("Google ADK tools not available (mock implementation will be used)")
    
    print("Creating trust network tools...")
    
    # Create tools
    tools = create_trust_network_tools()
    
    # Create sample metadata (normally provided by the ADK)
    class MockToolContext:
        def __init__(self):
            self.metadata = {"agent_id": "demo_agent"}
    
    tool_context = MockToolContext()
    
    # Get tools by name
    update_trust = tools[0]
    get_agent_profile = tools[1]
    get_collaboration_recommendation = tools[2]
    
    print(f"Created {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # Create demo data
    agent_data = create_demo_data()
    
    # Add agents using the update_trust tool
    print("\nAdding agents with update_trust tool...")
    
    for agent_id, data in agent_data.items():
        profile = update_trust(
            agent_id=agent_id,
            interaction_quality=data["interaction_quality"],
            reliability_score=data["reliability_score"],
            collaboration_style=data["collaboration_style"],
            strengths=data["strengths"],
            areas_for_growth=data["areas_for_growth"],
            tool_context=tool_context
        )
        print(f"Added agent {agent_id}")
    
    # Get an agent profile using the get_agent_profile tool
    print("\nGetting agent profile with get_agent_profile tool...")
    profile = get_agent_profile(agent_id="agent1", tool_context=tool_context)
    
    print(f"Profile for agent1:")
    print(f"  Reliability: {profile['reliability']:.2f}")
    print(f"  Interaction Quality: {profile['interaction_quality']:.2f}")
    print(f"  Collaboration Style: {profile['collaboration_style']}")
    
    # Get collaboration recommendation using the get_collaboration_recommendation tool
    print("\nGetting collaboration recommendation with get_collaboration_recommendation tool...")
    recommendation = get_collaboration_recommendation(
        agent_ids=["agent2", "agent3", "agent4"],
        tool_context=tool_context
    )
    
    print("Three-Agent Collaboration Recommendation:")
    print(f"  Potential: {recommendation['collaboration_potential']}")
    print(f"  Score: {recommendation['collaboration_score']}")
    print(f"  Approach: {recommendation['recommended_approach']}")
    
    print("\nFunction Tools demo completed.")


def run_integration_example():
    """
    Show a conceptual example of how to integrate trust network with the agent system.
    """
    print("\n=== Trust Network Integration Example ===")
    print("\nPseudo-code for integrating with CoherenceWeaverAgent:")
    print("```python")
    print("# Initialize components")
    print("trust_network = get_trust_network()")
    print("agent_tools = create_trust_network_tools()")
    print("agent = CoherenceWeaverLlmAgent()")
    print("")
    print("# Register tools with the agent")
    print("agent.register_tools(agent_tools)")
    print("")
    print("# Example agent interaction function")
    print("def handle_agent_interaction(agent_id, interaction):")
    print("    # Process the interaction")
    print("    result = agent.process_interaction(interaction)")
    print("    ")
    print("    # Evaluate the interaction")
    print("    quality_score = evaluate_interaction_quality(interaction, result)")
    print("    reliability_score = evaluate_reliability(result)")
    print("    ")
    print("    # Update trust network")
    print("    trust_network.update_trust(")
    print("        agent_id=agent_id,")
    print("        interaction_quality=quality_score,")
    print("        reliability_score=reliability_score,")
    print("        strengths=identify_strengths(result)")
    print("    )")
    print("    ")
    print("    # For multi-agent collaboration")
    print("    if 'collaboration' in interaction:")
    print("        agent_ids = interaction['collaboration']['agent_ids']")
    print("        recommendations = trust_network.get_collaboration_recommendation(agent_ids)")
    print("        ")
    print("        # Use recommendations to structure collaboration")
    print("        structured_collaboration = create_collaboration_plan(")
    print("            agent_ids=agent_ids,")
    print("            recommendations=recommendations")
    print("        )")
    print("        ")
    print("        return structured_collaboration")
    print("    ")
    print("    return result")
    print("```")
    
    print("\nThis integration example shows how the trust network can be used to:")
    print("1. Track reliability and interaction quality over time")
    print("2. Build agent profiles based on observed strengths and weaknesses")
    print("3. Generate informed collaboration recommendations")
    print("4. Structure multi-agent interactions for optimal results")


def main():
    """Main function to run the demo."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Trust Network Demo")
    parser.add_argument("--api-only", action="store_true", help="Run only the direct API demo")
    parser.add_argument("--tools-only", action="store_true", help="Run only the function tools demo")
    parser.add_argument("--integration-only", action="store_true", help="Show only the integration example")
    parser.add_argument("--clean", action="store_true", help="Start with a clean trust network")
    parser.add_argument("--data-path", type=str, help="Custom path for trust network data file")
    args = parser.parse_args()
    
    print("\n======================================")
    print("Coherence Weaver Trust Network Demo")
    print("======================================\n")
    
    print(f"ADK Tools Available: {'Yes' if ADK_TOOLS_AVAILABLE else 'No (using mock implementation)'}")
    
    try:
        # Initialize the trust network with a clean start if requested
        if args.clean:
            data_path = args.data_path or Path(parent_dir) / "data" / "trust_network.json"
            if os.path.exists(data_path):
                os.remove(data_path)
                print(f"Removed existing trust network data: {data_path}")
        
        # Initialize configuration
        initialize_config()
        
        # Run demos based on arguments
        if args.api_only:
            run_direct_api_demo(data_path=args.data_path, clean_start=args.clean)
        elif args.tools_only:
            run_function_tools_demo()
        elif args.integration_only:
            run_integration_example()
        else:
            # Run all demos
            run_direct_api_demo(data_path=args.data_path, clean_start=args.clean)
            run_function_tools_demo()
            run_integration_example()
        
        print("\nDemo completed successfully!")
        print("======================================\n")
        
    except Exception as e:
        logger.error(f"Error in demo: {e}")
        print(f"\nERROR: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
