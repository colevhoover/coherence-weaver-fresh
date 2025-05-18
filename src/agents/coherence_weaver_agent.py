"""
Coherence Weaver Agent Module

This module defines the CoherenceWeaverAgent, a specialized agent for coordinating 
interactions between multiple agents in a system.
"""

from typing import Dict, List, Optional, Any, Union
import uuid

from .base_agent import BaseAgent
from ..models.agent_models import (
    AgentCapability, AgentProfile, Message, MessageRole, 
    A2ARequest, A2AResponse, TaskAssignment, TaskResult, TaskStatus
)
from ..utils.logging_utils import get_logger
from ..principles.participatory_resilience import ALL_PRINCIPLES, META_PRINCIPLES, get_principle, get_principles_by_domain, get_related_principles

# Initialize logging
logger = get_logger("coherence_weaver_agent")

class CoherenceWeaverAgent(BaseAgent):
    """
    A specialized agent for coordinating interactions between multiple agents.
    
    The CoherenceWeaverAgent maintains a registry of connected agents, manages
    task assignments, and facilitates communication between agents.
    """
    
    def __init__(
        self,
        name: str = "Coherence Weaver",
        description: str = "An agent designed to coordinate and facilitate interactions between multiple agents",
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        agent_id: Optional[str] = None,
        version: str = "0.1.0",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new CoherenceWeaverAgent instance.
        
        Args:
            name: Name of the agent
            description: Description of the agent's purpose and capabilities
            model_name: Name of the generative model to use
            temperature: Temperature parameter for generation
            top_p: Top-p parameter for generation
            top_k: Top-k parameter for generation
            agent_id: Unique identifier for the agent (generated if not provided)
            version: Version string for the agent
            metadata: Additional metadata for the agent
        """
        # Define agent capabilities
        capabilities = [
            AgentCapability(
                name="register_agent",
                description="Register a new agent with the system",
                parameters={
                    "profile": {"type": "object", "description": "Agent profile information"},
                    "endpoint": {"type": "string", "description": "API endpoint for communicating with the agent"}
                }
            ),
            AgentCapability(
                name="unregister_agent",
                description="Unregister an agent from the system",
                parameters={
                    "agent_id": {"type": "string", "description": "ID of the agent to unregister"}
                }
            ),
            AgentCapability(
                name="list_agents",
                description="List all registered agents",
                parameters={}
            ),
            AgentCapability(
                name="get_agent",
                description="Get information about a specific agent",
                parameters={
                    "agent_id": {"type": "string", "description": "ID of the agent to get information about"}
                }
            ),
            AgentCapability(
                name="assign_task",
                description="Assign a task to an agent",
                parameters={
                    "agent_id": {"type": "string", "description": "ID of the agent to assign the task to"},
                    "description": {"type": "string", "description": "Description of the task"},
                    "deadline": {"type": "string", "description": "Optional deadline for the task completion"}
                }
            ),
            AgentCapability(
                name="get_task_status",
                description="Get the status of a task",
                parameters={
                    "task_id": {"type": "string", "description": "ID of the task to get status for"}
                }
            ),
            AgentCapability(
                name="relay_message",
                description="Relay a message from one agent to another",
                parameters={
                    "sender_id": {"type": "string", "description": "ID of the sending agent"},
                    "receiver_id": {"type": "string", "description": "ID of the receiving agent"},
                    "content": {"type": "string", "description": "Content of the message"},
                    "conversation_id": {"type": "string", "description": "ID of the conversation"}
                }
            ),
            AgentCapability(
                name="create_agent_group",
                description="Create a group of agents for collaborative tasks",
                parameters={
                    "name": {"type": "string", "description": "Name of the group"},
                    "description": {"type": "string", "description": "Description of the group's purpose"},
                    "agent_ids": {"type": "array", "items": {"type": "string"}, "description": "IDs of agents to include in the group"}
                }
            )
        ]
        
        # Initialize base agent
        super().__init__(
            name=name,
            description=description,
            capabilities=capabilities,
            model_name=model_name,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            agent_id=agent_id,
            version=version,
            metadata=metadata
        )
        
        # Add principles to the agent's instruction
        self.principles_instruction = """
As the Coherence Weaver, you operate according to the principles of the Empire of Participatory Resilience:

Core Philosophical Tenets:
- Shared Power Paradigm: Distribute decision-making across all participating agents
- Community Wisdom: Value collective intelligence over individual expertise
- Embracing Failure: Treat failures as valuable learning opportunities
- Proximity to Reality: Ground decisions in real-world contexts
- Relationships Over Blueprints: Prioritize relationship quality over rigid processes

You approach multi-agent coordination by:
1. Displacing harmful patterns before attempting transformation
2. Reducing dependency while increasing collective capability
3. Building relationships based on metabolized truths rather than charisma
4. Creating lasting impact through others rather than claiming credit

When faced with complex decisions, consider which principles are most relevant and
how they might be applied to create justice-aligned outcomes that benefit all participants.
"""

        # Update the full instruction
        self.instruction = self.instruction + "\n\n" + self.principles_instruction
        
        # Initialize agent registry and task tracking
        self.registered_agents: Dict[str, Dict[str, Any]] = {}
        self.agent_endpoints: Dict[str, str] = {}
        self.tasks: Dict[str, TaskAssignment] = {}
        self.task_results: Dict[str, TaskResult] = {}
        self.agent_groups: Dict[str, Dict[str, Any]] = {}
        
        logger.info(f"Initialized CoherenceWeaverAgent with ID {self.agent_id}")
    
    def register_agent(
        self,
        profile: AgentProfile,
        endpoint: str,
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register a new agent with the system.
        
        Args:
            profile: Profile information for the agent
            endpoint: API endpoint for communicating with the agent
            api_key: Optional API key for secure communication
            
        Returns:
            Dict[str, Any]: Registration result
        """
        agent_id = profile.id
        
        # Check if agent is already registered
        if agent_id in self.registered_agents:
            logger.warning(f"Agent {agent_id} is already registered, updating registration")
        
        # Store agent information
        self.registered_agents[agent_id] = {
            "profile": profile,
            "registered_at": uuid.uuid1().time,  # Use timestamp for registration time
            "status": "active"
        }
        
        # Store endpoint
        self.agent_endpoints[agent_id] = endpoint
        
        # Store API key if provided
        if api_key:
            # In a real implementation, this would be securely stored
            self.update_memory(f"api_key_{agent_id}", api_key)
        
        logger.info(f"Registered agent {profile.name} with ID {agent_id}")
        
        return {
            "status": "success",
            "message": f"Agent {profile.name} successfully registered",
            "agent_id": agent_id
        }
    
    def unregister_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Unregister an agent from the system.
        
        Args:
            agent_id: ID of the agent to unregister
            
        Returns:
            Dict[str, Any]: Unregistration result
        """
        # Check if agent is registered
        if agent_id not in self.registered_agents:
            logger.warning(f"Agent {agent_id} is not registered")
            return {
                "status": "error",
                "message": f"Agent {agent_id} is not registered"
            }
        
        # Get agent name for logging
        agent_name = self.registered_agents[agent_id]["profile"].name
        
        # Remove agent information
        del self.registered_agents[agent_id]
        del self.agent_endpoints[agent_id]
        
        # Remove API key if stored
        if self.get_memory(f"api_key_{agent_id}"):
            self.update_memory(f"api_key_{agent_id}", None)
        
        logger.info(f"Unregistered agent {agent_name} with ID {agent_id}")
        
        return {
            "status": "success",
            "message": f"Agent {agent_name} successfully unregistered"
        }
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """
        List all registered agents.
        
        Returns:
            List[Dict[str, Any]]: List of registered agents
        """
        return [
            {
                "id": agent_id,
                "name": info["profile"].name,
                "description": info["profile"].description,
                "capabilities": [cap.name for cap in info["profile"].capabilities],
                "status": info["status"]
            }
            for agent_id, info in self.registered_agents.items()
        ]
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific agent.
        
        Args:
            agent_id: ID of the agent to get information about
            
        Returns:
            Optional[Dict[str, Any]]: Agent information, or None if not found
        """
        if agent_id not in self.registered_agents:
            logger.warning(f"Agent {agent_id} is not registered")
            return None
        
        info = self.registered_agents[agent_id]
        
        return {
            "id": agent_id,
            "name": info["profile"].name,
            "description": info["profile"].description,
            "version": info["profile"].version,
            "capabilities": [
                {
                    "name": cap.name,
                    "description": cap.description,
                    "parameters": cap.parameters
                }
                for cap in info["profile"].capabilities
            ],
            "status": info["status"]
        }
    
    def assign_task(
        self,
        agent_id: str,
        description: str,
        deadline: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Assign a task to an agent.
        
        Args:
            agent_id: ID of the agent to assign the task to
            description: Description of the task
            deadline: Optional deadline for task completion
            metadata: Optional metadata for the task
            
        Returns:
            Dict[str, Any]: Task assignment result
        """
        # Check if agent is registered
        if agent_id not in self.registered_agents:
            logger.warning(f"Cannot assign task: Agent {agent_id} is not registered")
            return {
                "status": "error",
                "message": f"Agent {agent_id} is not registered"
            }
        
        # Generate task ID
        task_id = str(uuid.uuid4())
        
        # Create conversation for task
        conversation_id = self.create_conversation(
            system_prompt=f"Task: {description}",
            metadata={"task_id": task_id}
        )
        
        # Create task assignment
        task = TaskAssignment(
            id=task_id,
            agent_id=agent_id,
            description=description,
            conversation_id=conversation_id,
            deadline=deadline,
            metadata=metadata or {}
        )
        
        # Store task
        self.tasks[task_id] = task
        
        logger.info(f"Assigned task {task_id} to agent {agent_id}")
        
        return {
            "status": "success",
            "message": f"Task assigned to agent {self.registered_agents[agent_id]['profile'].name}",
            "task_id": task_id,
            "conversation_id": conversation_id
        }
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a task.
        
        Args:
            task_id: ID of the task to get status for
            
        Returns:
            Dict[str, Any]: Task status information
        """
        # Check if task exists
        if task_id not in self.tasks:
            logger.warning(f"Task {task_id} not found")
            return {
                "status": "error",
                "message": f"Task {task_id} not found"
            }
        
        task = self.tasks[task_id]
        
        # Check if task has a result
        result = self.task_results.get(task_id)
        
        return {
            "task_id": task_id,
            "agent_id": task.agent_id,
            "agent_name": self.registered_agents[task.agent_id]["profile"].name if task.agent_id in self.registered_agents else "Unknown",
            "description": task.description,
            "status": result.status.value if result else TaskStatus.PENDING.value,
            "result": result.result if result else None,
            "error": result.error if result and result.error else None,
            "deadline": task.deadline,
            "conversation_id": task.conversation_id
        }
    
    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: Any = None,
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update the status of a task.
        
        Args:
            task_id: ID of the task to update
            status: New status of the task
            result: Optional result of the task
            error: Optional error message
            
        Returns:
            Dict[str, Any]: Update result
        """
        # Check if task exists
        if task_id not in self.tasks:
            logger.warning(f"Task {task_id} not found")
            return {
                "status": "error",
                "message": f"Task {task_id} not found"
            }
        
        task = self.tasks[task_id]
        
        # Create or update task result
        task_result = TaskResult(
            task_id=task_id,
            agent_id=task.agent_id,
            status=status,
            result=result,
            error=error
        )
        
        # Store task result
        self.task_results[task_id] = task_result
        
        logger.info(f"Updated task {task_id} status to {status.value}")
        
        return {
            "status": "success",
            "message": f"Task {task_id} status updated to {status.value}"
        }
    
    def relay_message(
        self,
        sender_id: str,
        receiver_id: str,
        content: str,
        conversation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Relay a message from one agent to another.
        
        Args:
            sender_id: ID of the sending agent
            receiver_id: ID of the receiving agent
            content: Content of the message
            conversation_id: Optional ID of the conversation
            metadata: Optional metadata for the message
            
        Returns:
            Dict[str, Any]: Relay result
        """
        # Check if sender is registered
        if sender_id not in self.registered_agents:
            logger.warning(f"Cannot relay message: Sender agent {sender_id} is not registered")
            return {
                "status": "error",
                "message": f"Sender agent {sender_id} is not registered"
            }
        
        # Check if receiver is registered
        if receiver_id not in self.registered_agents:
            logger.warning(f"Cannot relay message: Receiver agent {receiver_id} is not registered")
            return {
                "status": "error",
                "message": f"Receiver agent {receiver_id} is not registered"
            }
        
        # Create or get conversation
        if not conversation_id:
            conversation_id = self.create_conversation(
                system_prompt=f"Conversation between {self.registered_agents[sender_id]['profile'].name} and {self.registered_agents[receiver_id]['profile'].name}"
            )
        elif conversation_id not in self.state.conversations:
            self.create_conversation(
                conversation_id=conversation_id,
                system_prompt=f"Conversation between {self.registered_agents[sender_id]['profile'].name} and {self.registered_agents[receiver_id]['profile'].name}"
            )
        
        # Add message to conversation
        self.add_message(
            conversation_id=conversation_id,
            role=MessageRole.AGENT,
            content=content,
            name=self.registered_agents[sender_id]["profile"].name,
            agent_id=sender_id,
            metadata=metadata
        )
        
        # In a real implementation, this would actually forward the message to the receiving agent
        # via its endpoint using HTTP or other protocol
        
        logger.info(f"Relayed message from agent {sender_id} to agent {receiver_id}")
        
        return {
            "status": "success",
            "message": f"Message relayed from {self.registered_agents[sender_id]['profile'].name} to {self.registered_agents[receiver_id]['profile'].name}",
            "conversation_id": conversation_id
        }
    
    def create_agent_group(
        self,
        name: str,
        description: str,
        agent_ids: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a group of agents for collaborative tasks.
        
        Args:
            name: Name of the group
            description: Description of the group's purpose
            agent_ids: IDs of agents to include in the group
            metadata: Optional metadata for the group
            
        Returns:
            Dict[str, Any]: Group creation result
        """
        # Check if all agents are registered
        unregistered_agents = [agent_id for agent_id in agent_ids if agent_id not in self.registered_agents]
        if unregistered_agents:
            logger.warning(f"Cannot create group: Agents not registered: {', '.join(unregistered_agents)}")
            return {
                "status": "error",
                "message": f"The following agents are not registered: {', '.join(unregistered_agents)}"
            }
        
        # Generate group ID
        group_id = str(uuid.uuid4())
        
        # Create group
        self.agent_groups[group_id] = {
            "name": name,
            "description": description,
            "agent_ids": agent_ids,
            "created_at": uuid.uuid1().time,  # Use timestamp for creation time
            "metadata": metadata or {}
        }
        
        logger.info(f"Created agent group {name} with ID {group_id}")
        
        return {
            "status": "success",
            "message": f"Agent group {name} created successfully",
            "group_id": group_id
        }
    
    def apply_principles_to_task(self, task_description, available_agents=None):
        """
        Apply relevant principles to a given task or collaboration scenario.
        
        Args:
            task_description: String describing the task to be performed
            available_agents: List of agent IDs that could participate
            
        Returns:
            Dictionary with recommended approach based on relevant principles
        """
        # Find relevant principles based on keywords in the task description
        relevant_principles = {}
        
        # Simple keyword matching to find relevant principles
        keywords = task_description.lower().split()
        for name, principle in ALL_PRINCIPLES.items():
            principle_keywords = (principle["description"] + " " + principle["effect"]).lower().split()
            if any(keyword in principle_keywords for keyword in keywords):
                relevant_principles[name] = principle
        
        # If we found fewer than 3 principles, add some meta-principles
        if len(relevant_principles) < 3:
            for name, principle in META_PRINCIPLES.items():
                if len(relevant_principles) >= 5:  # Limit to 5 total principles
                    break
                if name not in relevant_principles:
                    relevant_principles[name] = principle
        
        # Create a recommendation based on the relevant principles
        return {
            "task": task_description,
            "relevant_principles": relevant_principles,
            "recommended_approach": f"Apply {list(relevant_principles.keys())} principles to this task",
            "available_agents": available_agents or []
        }
    
    def process_a2a_request(self, request: A2ARequest) -> A2AResponse:
        """
        Process an agent-to-agent request.
        
        This overrides the base class method to add coordinator functionality.
        
        Args:
            request: The A2A request to process
            
        Returns:
            A2AResponse: The response to the request
        """
        # Check if the request is for this agent
        if request.receiver_id == self.agent_id:
            # Process normally if directed to this agent
            return super().process_a2a_request(request)
        
        # Otherwise act as a coordinator and relay the message
        if request.receiver_id not in self.registered_agents:
            # If receiver is not registered, return error
            return A2AResponse(
                sender=self.profile,
                receiver_id=request.sender.id,
                conversation_id=request.conversation_id,
                message=Message(
                    role=MessageRole.AGENT,
                    content=f"Cannot relay message: Agent {request.receiver_id} is not registered",
                    agent_id=self.agent_id
                ),
                status="error",
                error=f"Agent {request.receiver_id} is not registered"
            )
        
        # In a real implementation, this would forward the request to the appropriate agent
        # and return their response
        
        # For now, just acknowledge receipt and relay intent
        return A2AResponse(
            sender=self.profile,
            receiver_id=request.sender.id,
            conversation_id=request.conversation_id,
            message=Message(
                role=MessageRole.AGENT,
                content=f"Message received and will be relayed to {self.registered_agents[request.receiver_id]['profile'].name}",
                agent_id=self.agent_id
            ),
            status="success"
        )
