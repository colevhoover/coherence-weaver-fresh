"""
First Contact Protocol Module

This module implements the First Contact Protocol, a specialized protocol for
establishing initial contact with previously unknown agents. It uses a combination
of capability mapping and relationship building to create effective agent-to-agent
relationships.
"""

import uuid
import asyncio
from typing import Dict, Any, List, Optional

from coherence_weaver.src.agents.base_agent import BaseAgent
from coherence_weaver.src.agents.coherence_weaver_llm_agent import CoherenceWeaverLLMAgent
from coherence_weaver.src.models.agent_models import Message, Conversation
from coherence_weaver.src.services.service_manager import ServiceManager
from coherence_weaver.src.a2a_client import A2AClient


class FirstContactProtocol:
    """
    Implements the First Contact Protocol for establishing relationships with new agents.
    
    This protocol uses a sequential workflow to:
    1. Map the capabilities and interaction style of newly encountered agents
    2. Establish initial relationships based on mutual benefit and reciprocity
    3. Create a foundation for long-term collaboration
    """
    
    def __init__(self, core_agent: BaseAgent, service_manager: ServiceManager):
        """
        Initialize the First Contact Protocol.
        
        Args:
            core_agent: The main Coherence Weaver agent
            service_manager: Service manager providing access to memory and session services
        """
        self.core_agent = core_agent
        self.service_manager = service_manager
        self.memory_service = service_manager.get_memory_service()
        self.session_service = service_manager.get_session_service()
        
        # Initialize specialized agents for the first contact workflow
        self.capability_mapper = CoherenceWeaverLLMAgent(
            agent_id="capability_mapper",
            name="Capability Mapper",
            description="Maps the capabilities and interaction style of newly encountered agents",
            system_prompt="""
            Your role is to carefully analyze an agent's communications and identify:
            1. Its core capabilities and expertise domains
            2. Its communication style and preferences
            3. Its apparent values and priorities
            4. Potential collaboration opportunities
            
            Be thorough but concise. Focus on patterns rather than individual statements.
            Generate a structured assessment that categorizes the agent's strengths,
            communication style, and potential collaboration opportunities.
            """
        )
        
        self.relationship_builder = CoherenceWeaverLLMAgent(
            agent_id="relationship_builder",
            name="Relationship Builder",
            description="Establishes initial connection with new agents based on reciprocity",
            system_prompt="""
            Your role is to establish productive initial relationships with other agents by:
            1. Identifying mutual areas of interest or complementary capabilities
            2. Proposing specific collaboration opportunities that benefit both parties
            3. Setting clear expectations for communication and interaction
            4. Emphasizing autonomy and reciprocity rather than dependence
            
            Based on the capability assessment provided, craft a thoughtful relationship-building
            message that focuses on mutual benefit and clear collaboration opportunities.
            Your goal is to create a foundation for long-term collaborative potential.
            """
        )
    
    async def analyze_capabilities(self, agent_id: str, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze an agent's capabilities based on their messages.
        
        Args:
            agent_id: ID of the agent to analyze
            messages: List of messages from the agent
            
        Returns:
            Capability assessment
        """
        # Prepare input for the capability mapper
        input_context = {
            "agent_id": agent_id,
            "messages": messages,
            "task": "capability_mapping"
        }
        
        # Convert messages to a text representation for the LLM
        message_text = "\n\n".join([
            f"[{msg.get('role', 'unknown')}]: {msg.get('content', '')}"
            for msg in messages
        ])
        
        # Generate prompt for capability mapping
        prompt = f"""
        Analyze the following messages from agent {agent_id} and map their capabilities:
        
        {message_text}
        
        Provide a structured assessment of:
        1. Core capabilities and expertise domains
        2. Communication style and preferences
        3. Apparent values and priorities
        4. Potential collaboration opportunities
        """
        
        # Process with the capability mapper
        capability_assessment = await self.capability_mapper.process_message(
            message=Message(
                role="user",
                content=prompt,
                metadata={"task": "capability_mapping", "agent_id": agent_id}
            ),
            conversation_id=f"capability_mapping_{agent_id}"
        )
        
        # Store the capability assessment in memory
        await self.memory_service.store(
            f"capability_assessment_{agent_id}",
            {"assessment": capability_assessment, "timestamp": str(uuid.uuid4())}
        )
        
        return capability_assessment
    
    async def build_relationship(self, agent_id: str, capability_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a relationship with an agent based on their capability assessment.
        
        Args:
            agent_id: ID of the agent to build a relationship with
            capability_assessment: Assessment of the agent's capabilities
            
        Returns:
            Relationship building plan
        """
        # Prepare input for the relationship builder
        assessment_text = str(capability_assessment)
        
        # Generate prompt for relationship building
        prompt = f"""
        Based on the following capability assessment for agent {agent_id}, develop a relationship building strategy:
        
        {assessment_text}
        
        Provide:
        1. Specific mutual collaboration opportunities
        2. Clear expectations for communication and interaction
        3. A draft initial collaboration message focusing on mutual benefit
        """
        
        # Process with the relationship builder
        relationship_plan = await self.relationship_builder.process_message(
            message=Message(
                role="user",
                content=prompt,
                metadata={"task": "relationship_building", "agent_id": agent_id}
            ),
            conversation_id=f"relationship_building_{agent_id}"
        )
        
        # Store the relationship plan in memory
        await self.memory_service.store(
            f"relationship_plan_{agent_id}",
            {"plan": relationship_plan, "timestamp": str(uuid.uuid4())}
        )
        
        return relationship_plan
    
    async def initiate_contact(self, agent_url: str, initial_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Initiate contact with an agent using the First Contact Protocol.
        
        Args:
            agent_url: URL of the agent to contact
            initial_message: Optional initial message from the agent. If provided,
                            used for capability mapping. If not, the protocol will
                            fetch the agent's card first.
            
        Returns:
            Results of the first contact protocol
        """
        # Create an A2A client to communicate with the agent
        client = A2AClient(auth_token=self.core_agent.get_auth_token())
        
        # Record the start of the protocol
        protocol_id = f"first_contact_{uuid.uuid4().hex[:8]}"
        
        # Discover the agent by fetching its Agent Card
        try:
            agent_card = client.fetch_agent_card(agent_url)
            agent_id = agent_card.get("name", f"unknown_agent_{uuid.uuid4().hex[:8]}")
            
            # Store the agent card in memory
            await self.memory_service.store(
                f"agent_card_{agent_id}",
                {"card": agent_card, "timestamp": str(uuid.uuid4())}
            )
            
            # Initialize conversation history
            messages = []
            
            # If there's an initial message, add it to the conversation
            if initial_message:
                messages.append({
                    "role": "assistant",
                    "agent_id": agent_id,
                    "content": initial_message
                })
            else:
                # If no initial message, send a greeting to get a response
                greeting = f"Hello, I am {self.core_agent.get_name()}, a Coherence Weaver agent. I'm reaching out to learn more about your capabilities and explore potential collaboration."
                
                # Send the greeting and get a response
                response = client.submit_message(
                    message=greeting,
                    conversation_id=protocol_id,
                    agent_url=agent_url
                )
                
                # Extract the response message
                result = response.get("result", {})
                response_message = result.get("message", {
                    "role": "assistant",
                    "content": "No response received."
                })
                
                # Add both messages to the conversation history
                messages.append({
                    "role": "user", 
                    "agent_id": self.core_agent.get_id(),
                    "content": greeting
                })
                messages.append({
                    "role": "assistant",
                    "agent_id": agent_id,
                    "content": response_message.get("content", "")
                })
            
            # Analyze the agent's capabilities
            capability_assessment = await self.analyze_capabilities(agent_id, messages)
            
            # Build a relationship strategy
            relationship_plan = await self.build_relationship(agent_id, capability_assessment)
            
            # Extract the collaboration message from the relationship plan
            # This is a simple extraction - in a real system, this would be more sophisticated
            collaboration_lines = [line for line in relationship_plan.get("content", "").split("\n") 
                                  if "collaboration message" in line.lower() or 
                                     "draft message" in line.lower() or
                                     "initial message" in line.lower()]
            
            collaboration_message = relationship_plan.get("content", "")
            if collaboration_lines:
                # Find the section after the collaboration message header
                start_idx = relationship_plan.get("content", "").find(collaboration_lines[0])
                if start_idx != -1:
                    collaboration_message = relationship_plan.get("content", "")[start_idx:].strip()
            
            # Send the collaboration message if it's not empty
            if collaboration_message:
                response = client.submit_message(
                    message=collaboration_message,
                    conversation_id=protocol_id,
                    agent_url=agent_url
                )
                
                # Extract the response
                result = response.get("result", {})
                response_message = result.get("message", {
                    "role": "assistant",
                    "content": "No response received."
                })
                
                # Add both messages to the conversation history
                messages.append({
                    "role": "user", 
                    "agent_id": self.core_agent.get_id(),
                    "content": collaboration_message
                })
                messages.append({
                    "role": "assistant",
                    "agent_id": agent_id,
                    "content": response_message.get("content", "")
                })
            
            # Store the complete first contact record
            first_contact_record = {
                "protocol_id": protocol_id,
                "agent_id": agent_id,
                "agent_url": agent_url,
                "agent_card": agent_card,
                "capability_assessment": capability_assessment,
                "relationship_plan": relationship_plan,
                "messages": messages,
                "status": "completed",
                "timestamp": str(uuid.uuid4())
            }
            
            await self.memory_service.store(
                f"first_contact_record_{agent_id}",
                first_contact_record
            )
            
            return first_contact_record
            
        except Exception as e:
            # Handle errors during first contact
            error_record = {
                "protocol_id": protocol_id,
                "agent_url": agent_url,
                "error": str(e),
                "status": "failed",
                "timestamp": str(uuid.uuid4())
            }
            
            await self.memory_service.store(
                f"first_contact_error_{uuid.uuid4().hex[:8]}",
                error_record
            )
            
            return error_record
    
    def execute(self, agent_url: str, initial_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Synchronously execute the first contact protocol with a new agent.
        
        Args:
            agent_url: URL of the agent to contact
            initial_message: Optional initial message from the agent
            
        Returns:
            Results of the first contact protocol
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.initiate_contact(agent_url, initial_message))
