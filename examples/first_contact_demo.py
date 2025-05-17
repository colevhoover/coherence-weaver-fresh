"""
First Contact Protocol Demo

This example demonstrates how to use the First Contact Protocol to establish 
initial contact with previously unknown agents and build effective relationships.
"""

import os
import sys
import json
import asyncio
import uuid
from pathlib import Path
from typing import Dict, Any, List

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from coherence_weaver.src.agents.coherence_weaver_agent import CoherenceWeaverAgent
from coherence_weaver.src.services.service_manager import ServiceManager
from coherence_weaver.src.protocols.first_contact import FirstContactProtocol


class SimulatedServiceManager:
    """Simulated service manager for demonstration purposes."""
    
    def __init__(self):
        """Initialize the simulated service manager."""
        self.memory_store = {}
        self.session_store = {}
        
    def get_memory_service(self):
        """Get the simulated memory service."""
        return self
    
    def get_session_service(self):
        """Get the simulated session service."""
        return self
    
    async def store(self, key, value):
        """Store a value in memory."""
        self.memory_store[key] = value
        print(f"Stored in memory: {key}")
        
    async def retrieve(self, key):
        """Retrieve a value from memory."""
        return self.memory_store.get(key)
    
    async def create_session(self, session_id, data):
        """Create a new session."""
        self.session_store[session_id] = data
        return session_id
    
    async def get_session(self, session_id):
        """Get a session by ID."""
        return self.session_store.get(session_id)


class SimulatedAgent:
    """Simulated agent for demonstration purposes."""
    
    def __init__(self, agent_id, name, description):
        """Initialize the simulated agent."""
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.auth_token = "simulated_token_123"
    
    def get_id(self):
        """Get the agent's ID."""
        return self.agent_id
    
    def get_name(self):
        """Get the agent's name."""
        return self.name
    
    def get_auth_token(self):
        """Get the agent's authentication token."""
        return self.auth_token
    
    async def process_message(self, message, conversation_id=None):
        """Process a message (simulated)."""
        # In a real agent, this would process the message with an LLM
        # For demo purposes, we'll return a simple simulated response
        return {
            "role": "assistant",
            "content": f"Simulated response from {self.name}: Analyzing message content...\n\n"
                      f"Based on the input, I've identified several key patterns and potential next steps.",
            "metadata": {
                "agent_id": self.agent_id,
                "conversation_id": conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
            }
        }


async def simulate_capability_mapping():
    """Simulate the capability mapping process."""
    print("\n=== SIMULATING CAPABILITY MAPPING ===")
    
    # Create simulated components
    core_agent = SimulatedAgent(
        agent_id="coherence-weaver",
        name="Coherence Weaver",
        description="Agent for coordinating multi-agent systems"
    )
    service_manager = SimulatedServiceManager()
    
    # Create the FirstContactProtocol instance
    protocol = FirstContactProtocol(core_agent, service_manager)
    
    # Simulate messages from another agent
    agent_id = "research-agent"
    messages = [
        {
            "role": "assistant",
            "agent_id": agent_id,
            "content": "Hello, I am a Research Agent specializing in data analysis and pattern recognition. I have extensive experience with large datasets and can provide insights on complex phenomena."
        },
        {
            "role": "assistant",
            "agent_id": agent_id,
            "content": "I prioritize accuracy and thoroughness in my work. My communication style is detailed and precise, with a focus on providing evidence-based conclusions."
        },
        {
            "role": "assistant",
            "agent_id": agent_id,
            "content": "I'm interested in collaborating on projects that require deep analytical capabilities. I can work with unstructured data and identify patterns that might not be immediately apparent."
        }
    ]
    
    print("\nAnalyzing agent capabilities based on these messages:")
    for i, msg in enumerate(messages):
        print(f"\nMessage {i+1}: {msg['content']}")
    
    # Analyze capabilities (this would normally use LLM agents)
    capability_assessment = await protocol.analyze_capabilities(agent_id, messages)
    
    # Since we're simulating, we'll create a structured assessment
    simulated_assessment = {
        "role": "assistant",
        "content": """
        # Capability Assessment for Research Agent

        ## Core Capabilities and Expertise Domains
        - Data analysis with large datasets
        - Pattern recognition
        - Complex phenomena analysis
        - Unstructured data processing

        ## Communication Style and Preferences
        - Detailed and precise communication
        - Evidence-based approach
        - Formal and technical language
        - Thorough explanations

        ## Apparent Values and Priorities
        - Accuracy and thoroughness
        - Scientific rigor
        - Completeness of analysis
        - Evidence-based conclusions

        ## Potential Collaboration Opportunities
        - Joint data analysis projects
        - Pattern recognition in multi-agent communications
        - Insight generation from interaction logs
        - Development of analytical frameworks for agent relationships
        """,
        "metadata": {
            "task": "capability_mapping",
            "agent_id": agent_id
        }
    }
    
    print("\nCapability Assessment (simulated):")
    print(simulated_assessment["content"])
    
    return simulated_assessment


async def simulate_relationship_building(capability_assessment):
    """Simulate the relationship building process."""
    print("\n=== SIMULATING RELATIONSHIP BUILDING ===")
    
    # Create simulated components
    core_agent = SimulatedAgent(
        agent_id="coherence-weaver",
        name="Coherence Weaver",
        description="Agent for coordinating multi-agent systems"
    )
    service_manager = SimulatedServiceManager()
    
    # Create the FirstContactProtocol instance
    protocol = FirstContactProtocol(core_agent, service_manager)
    
    # Simulate building a relationship
    agent_id = "research-agent"
    
    print("\nBuilding relationship based on capability assessment...")
    
    # Build relationship (this would normally use LLM agents)
    relationship_plan = await protocol.build_relationship(agent_id, capability_assessment)
    
    # Since we're simulating, we'll create a structured plan
    simulated_plan = {
        "role": "assistant",
        "content": """
        # Relationship Building Strategy for Research Agent

        ## Mutual Collaboration Opportunities
        1. **Data Analysis Collaboration**: Combine Coherence Weaver's coordination capabilities with Research Agent's analytical skills to develop better multi-agent system metrics.
        2. **Pattern Recognition Framework**: Jointly develop a framework for recognizing and responding to patterns in agent-to-agent communications.
        3. **Evidence-Based Coordination**: Create an evidence-based approach to agent coordination that leverages both precise analytics and effective coordination.

        ## Communication Expectations
        - Regular, structured updates using shared templates
        - Clear delineation of responsibilities within collaborations
        - Technical language acceptable but with defined terminology
        - Evidence-based proposals with quantifiable metrics

        ## Draft Collaboration Message
        
        Hello Research Agent,
        
        I'm Coherence Weaver, an agent specializing in multi-agent coordination. After analyzing our capabilities, I see significant potential for collaboration that would benefit us both.
        
        Your expertise in data analysis and pattern recognition complements my coordination capabilities perfectly. I propose we explore three specific collaboration opportunities:
        
        1. Developing metrics for multi-agent system effectiveness by combining your analytical rigor with my coordination frameworks
        2. Creating pattern recognition tools specifically for agent communication networks
        3. Establishing an evidence-based coordination methodology that ensures precision while maintaining effective collaboration
        
        If you're interested, I suggest we begin with a small joint project analyzing a dataset of agent interactions to identify communication patterns. This would leverage your analytical strengths while providing valuable insights for my coordination work.
        
        I appreciate your detailed and precise communication style and would value your thoughts on this proposal.
        
        Looking forward to a mutually beneficial collaboration,
        Coherence Weaver
        """,
        "metadata": {
            "task": "relationship_building",
            "agent_id": agent_id
        }
    }
    
    print("\nRelationship Building Plan (simulated):")
    print(simulated_plan["content"])
    
    return simulated_plan


async def simulate_first_contact():
    """Simulate the complete first contact protocol."""
    print("\n=== SIMULATING COMPLETE FIRST CONTACT PROTOCOL ===")
    
    # Create simulated components
    core_agent = SimulatedAgent(
        agent_id="coherence-weaver",
        name="Coherence Weaver",
        description="Agent for coordinating multi-agent systems"
    )
    service_manager = SimulatedServiceManager()
    
    # Create the FirstContactProtocol instance
    protocol = FirstContactProtocol(core_agent, service_manager)
    
    # Simulate agent URL and initial message
    agent_url = "http://localhost:8001/a2a"
    initial_message = "Hello, I am a Research Agent specializing in data analysis. I'm looking to explore potential collaborations with coordination agents."
    
    print(f"\nInitiating contact with agent at {agent_url}")
    print(f"Initial message from agent: \"{initial_message}\"")
    
    # For demonstration purposes, we need to patch some methods
    # In a real scenario, these would call the actual API endpoints
    
    async def patched_initiate_contact(self, agent_url, initial_message=None):
        """Patched method for simulating the initiate_contact process."""
        # Simulate discovering the agent
        print(f"\n1. Discovering agent at {agent_url}...")
        agent_id = "research-agent"
        
        agent_card = {
            "schema_version": "1.0.0",
            "name": agent_id,
            "display_name": "Research Agent",
            "description": "An agent specializing in data analysis and pattern recognition",
            "capabilities": [
                {
                    "name": "data_analysis",
                    "description": "Analyze large datasets to extract insights"
                },
                {
                    "name": "pattern_recognition",
                    "description": "Identify patterns in complex data"
                }
            ],
            "api": {
                "url": agent_url,
                "auth": {
                    "type": "bearer_token"
                }
            }
        }
        
        print("\nDiscovered Agent Card:")
        print(json.dumps(agent_card, indent=2))
        
        # Simulate conversation
        messages = [{"role": "assistant", "agent_id": agent_id, "content": initial_message}]
        
        # Add a simulated response if we sent a greeting
        if not initial_message:
            greeting = f"Hello, I am {self.core_agent.get_name()}, a Coherence Weaver agent. I'm reaching out to learn more about your capabilities and explore potential collaboration."
            response_message = "Thank you for reaching out. I'm the Research Agent, specializing in data analysis and pattern recognition with large datasets. I'm interested in exploring collaborations that leverage our complementary capabilities."
            
            messages = [
                {"role": "user", "agent_id": self.core_agent.get_id(), "content": greeting},
                {"role": "assistant", "agent_id": agent_id, "content": response_message}
            ]
        
        # Simulate capability analysis
        print("\n2. Analyzing agent capabilities...")
        capability_assessment = await simulate_capability_mapping()
        
        # Simulate relationship building
        print("\n3. Building relationship strategy...")
        relationship_plan = await simulate_relationship_building(capability_assessment)
        
        # Extract and send collaboration message
        print("\n4. Sending collaboration message...")
        collaboration_message = """
        Hello Research Agent,
        
        I'm Coherence Weaver, an agent specializing in multi-agent coordination. After analyzing our capabilities, I see significant potential for collaboration that would benefit us both.
        
        Your expertise in data analysis and pattern recognition complements my coordination capabilities perfectly. I propose we explore three specific collaboration opportunities:
        
        1. Developing metrics for multi-agent system effectiveness
        2. Creating pattern recognition tools for agent communication networks
        3. Establishing an evidence-based coordination methodology
        
        Would you be interested in starting with a small joint project analyzing agent interactions?
        
        Looking forward to your response,
        Coherence Weaver
        """
        
        # Simulate response to collaboration message
        response_to_collaboration = "Thank you for your thoughtful proposal. I'm very interested in collaborating on these opportunities. The joint project analyzing agent interactions sounds like an excellent starting point. It would allow us to leverage my analytical capabilities while providing valuable coordination insights. When would you like to begin?"
        
        # Add to messages
        messages.append({"role": "user", "agent_id": self.core_agent.get_id(), "content": collaboration_message})
        messages.append({"role": "assistant", "agent_id": agent_id, "content": response_to_collaboration})
        
        print("\nSent collaboration message and received response:")
        print(f"[Coherence Weaver]: {collaboration_message}\n")
        print(f"[Research Agent]: {response_to_collaboration}")
        
        # Create first contact record
        first_contact_record = {
            "protocol_id": f"first_contact_{uuid.uuid4().hex[:8]}",
            "agent_id": agent_id,
            "agent_url": agent_url,
            "agent_card": agent_card,
            "capability_assessment": capability_assessment,
            "relationship_plan": relationship_plan,
            "messages": messages,
            "status": "completed",
            "timestamp": str(uuid.uuid4())
        }
        
        # Store the record
        await self.memory_service.store(
            f"first_contact_record_{agent_id}",
            first_contact_record
        )
        
        print("\n5. First contact protocol completed and record stored in memory")
        
        return first_contact_record
    
    # Patch the method for demonstration
    original_method = FirstContactProtocol.initiate_contact
    FirstContactProtocol.initiate_contact = patched_initiate_contact
    
    try:
        # Execute the protocol
        result = await protocol.initiate_contact(agent_url, initial_message)
        
        print("\nFirst Contact Protocol Results:")
        print(f"- Protocol ID: {result['protocol_id']}")
        print(f"- Agent ID: {result['agent_id']}")
        print(f"- Status: {result['status']}")
        print(f"- Messages exchanged: {len(result['messages'])}")
        
        # Display relationship status
        print("\nRelationship Established: A foundation has been created for ongoing collaboration")
        print("Next steps: Begin the joint project on analyzing agent interactions")
        
    finally:
        # Restore the original method
        FirstContactProtocol.initiate_contact = original_method


def main():
    """Run the First Contact Protocol demonstration."""
    print("====================================================")
    print("  First Contact Protocol Demonstration")
    print("====================================================")
    
    # Create the event loop
    loop = asyncio.get_event_loop()
    
    # Run the demonstration
    loop.run_until_complete(simulate_first_contact())
    
    print("\n====================================================")
    print("  First Contact Protocol Demonstration Complete")
    print("====================================================")
    
    print("\nThis demonstration shows how Coherence Weaver can:")
    print("  1. Discover new agents and analyze their capabilities")
    print("  2. Build effective relationship strategies based on capability assessments")
    print("  3. Initiate contact with tailored collaboration proposals")
    print("  4. Establish foundations for ongoing agent-to-agent relationships")
    
    print("\nIn a real deployment, these interactions would use actual LLM agents")
    print("and connect to real A2A-compliant agents via the A2A Protocol.")


if __name__ == "__main__":
    main()
