"""
Base Agent Module

This module defines the BaseAgent class, which provides core functionality for all agent types.
"""

import uuid
import google.generativeai as genai
from typing import Dict, List, Optional, Any, Union
import time

from ..models.agent_models import (
    AgentProfile, AgentState, AgentCapability, Message, 
    Conversation, MessageRole, A2ARequest, A2AResponse
)
from ..utils.logging_utils import get_logger
from ..config import GOOGLE_API_KEY, GENAI_MODEL, AGENT_TEMPERATURE, AGENT_TOP_P, AGENT_TOP_K

# Initialize logging
logger = get_logger("base_agent")

class BaseAgent:
    """
    Base agent class that provides core functionality for all agent types.
    
    This class handles agent state management, conversation tracking, and 
    interaction with the Google Generative AI API.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        capabilities: Optional[List[AgentCapability]] = None,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        agent_id: Optional[str] = None,
        version: str = "0.1.0",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new BaseAgent instance.
        
        Args:
            name: Name of the agent
            description: Description of the agent's purpose and capabilities
            capabilities: List of capabilities this agent has
            model_name: Name of the generative model to use
            temperature: Temperature parameter for generation
            top_p: Top-p parameter for generation
            top_k: Top-k parameter for generation
            agent_id: Unique identifier for the agent (generated if not provided)
            version: Version string for the agent
            metadata: Additional metadata for the agent
        """
        # Initialize Google GenerativeAI
        if GOOGLE_API_KEY:
            genai.configure(api_key=GOOGLE_API_KEY)
        else:
            logger.warning("GOOGLE_API_KEY not set. Agent will not be able to use generative AI capabilities.")
        
        # Set up agent profile
        self.agent_id = agent_id or str(uuid.uuid4())
        self.capabilities = capabilities or []
        
        self.profile = AgentProfile(
            id=self.agent_id,
            name=name,
            description=description,
            version=version,
            capabilities=self.capabilities,
            metadata=metadata or {}
        )
        
        # Set up agent state
        self.state = AgentState(
            id=self.agent_id,
            profile=self.profile,
            conversations={},
            memory={},
            metadata={}
        )
        
        # Set up generation parameters
        self.model_name = model_name or GENAI_MODEL
        self.temperature = temperature or AGENT_TEMPERATURE
        self.top_p = top_p or AGENT_TOP_P
        self.top_k = top_k or AGENT_TOP_K
        
        # Initialize generative model
        if GOOGLE_API_KEY:
            try:
                self.model = genai.GenerativeModel(
                    model_name=self.model_name,
                    generation_config={
                        "temperature": self.temperature,
                        "top_p": self.top_p,
                        "top_k": self.top_k
                    }
                )
                logger.info(f"Successfully initialized agent '{name}' with model '{self.model_name}'")
            except Exception as e:
                logger.error(f"Failed to initialize generative model: {e}")
                self.model = None
        else:
            self.model = None
    
    def get_profile(self) -> AgentProfile:
        """
        Get the agent's profile.
        
        Returns:
            AgentProfile: The agent's profile information
        """
        return self.profile
    
    def create_conversation(
        self,
        system_prompt: Optional[str] = None,
        conversation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new conversation for the agent.
        
        Args:
            system_prompt: Optional system prompt to initialize the conversation
            conversation_id: Optional ID for the conversation (generated if not provided)
            metadata: Optional metadata for the conversation
            
        Returns:
            str: The conversation ID
        """
        # Generate conversation ID if not provided
        conversation_id = conversation_id or str(uuid.uuid4())
        
        # Create conversation object
        conversation = Conversation(
            id=conversation_id,
            messages=[],
            metadata=metadata or {}
        )
        
        # Add system prompt if provided
        if system_prompt:
            system_message = Message(
                role=MessageRole.SYSTEM,
                content=system_prompt
            )
            conversation.messages.append(system_message)
        
        # Store conversation in agent state
        self.state.conversations[conversation_id] = conversation
        logger.info(f"Created conversation {conversation_id}")
        
        return conversation_id
    
    def add_message(
        self,
        conversation_id: str,
        role: MessageRole,
        content: Union[str, List[Dict[str, Any]]],
        name: Optional[str] = None,
        agent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Message]:
        """
        Add a message to a conversation.
        
        Args:
            conversation_id: ID of the conversation to add the message to
            role: Role of the message sender
            content: Content of the message
            name: Optional name of the sender
            agent_id: Optional ID of the agent sending the message
            metadata: Optional metadata for the message
            
        Returns:
            Optional[Message]: The added message, or None if the conversation ID is invalid
        """
        # Check if conversation exists
        if conversation_id not in self.state.conversations:
            logger.error(f"Conversation {conversation_id} not found")
            return None
        
        # Create message
        message = Message(
            role=role,
            content=content,
            name=name,
            agent_id=agent_id,
            metadata=metadata or {}
        )
        
        # Add message to conversation
        self.state.conversations[conversation_id].messages.append(message)
        
        return message
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """
        Get a conversation by ID.
        
        Args:
            conversation_id: ID of the conversation to get
            
        Returns:
            Optional[Conversation]: The conversation, or None if not found
        """
        return self.state.conversations.get(conversation_id)
    
    def get_messages(self, conversation_id: str) -> Optional[List[Message]]:
        """
        Get all messages in a conversation.
        
        Args:
            conversation_id: ID of the conversation to get messages from
            
        Returns:
            Optional[List[Message]]: List of messages, or None if conversation not found
        """
        conversation = self.get_conversation(conversation_id)
        return conversation.messages if conversation else None
    
    def generate_response(
        self,
        conversation_id: str,
        add_to_conversation: bool = True
    ) -> Optional[str]:
        """
        Generate a response using the generative AI model.
        
        Args:
            conversation_id: ID of the conversation to generate a response for
            add_to_conversation: Whether to add the generated response to the conversation
            
        Returns:
            Optional[str]: The generated response, or None if generation failed
        """
        if not self.model:
            logger.error("Cannot generate response: generative model not initialized")
            return None
        
        # Check if conversation exists
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            logger.error(f"Conversation {conversation_id} not found")
            return None
        
        try:
            # Convert conversation messages to chat format
            messages = []
            for msg in conversation.messages:
                messages.append({
                    "role": msg.role.value,
                    "parts": [msg.content] if isinstance(msg.content, str) else msg.content
                })
            
            # Generate response
            chat = self.model.start_chat(history=messages)
            response = chat.send_message("")
            
            # Extract text from response
            response_text = response.text
            
            # Add to conversation if requested
            if add_to_conversation and response_text:
                self.add_message(
                    conversation_id=conversation_id,
                    role=MessageRole.ASSISTANT,
                    content=response_text,
                    name=self.profile.name,
                    agent_id=self.agent_id
                )
            
            return response_text
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return None
    
    def process_a2a_request(self, request: A2ARequest) -> A2AResponse:
        """
        Process an agent-to-agent request.
        
        Args:
            request: The A2A request to process
            
        Returns:
            A2AResponse: The response to the request
        """
        # Check if the request is directed to this agent
        if request.receiver_id != self.agent_id:
            return A2AResponse(
                sender=self.profile,
                receiver_id=request.sender.id,
                conversation_id=request.conversation_id,
                message=Message(
                    role=MessageRole.AGENT,
                    content="Request rejected: incorrect receiver",
                    agent_id=self.agent_id
                ),
                status="error",
                error="Request not directed to this agent"
            )
        
        # Check if the conversation exists, create it if not
        if request.conversation_id not in self.state.conversations:
            self.create_conversation(conversation_id=request.conversation_id)
        
        # Add the incoming message to the conversation
        self.add_message(
            conversation_id=request.conversation_id,
            role=MessageRole.AGENT,
            content=request.message.content,
            name=request.sender.name,
            agent_id=request.sender.id,
            metadata=request.message.metadata
        )
        
        # Generate a response
        response_text = self.generate_response(request.conversation_id, add_to_conversation=False)
        
        # Create response message
        response_message = Message(
            role=MessageRole.AGENT,
            content=response_text or "Failed to generate response",
            name=self.profile.name,
            agent_id=self.agent_id
        )
        
        # Add response to conversation
        self.add_message(
            conversation_id=request.conversation_id,
            role=MessageRole.AGENT,
            content=response_text or "Failed to generate response",
            name=self.profile.name,
            agent_id=self.agent_id
        )
        
        # Create and return A2A response
        return A2AResponse(
            sender=self.profile,
            receiver_id=request.sender.id,
            conversation_id=request.conversation_id,
            message=response_message,
            status="success" if response_text else "error",
            error=None if response_text else "Failed to generate response"
        )
    
    def send_a2a_request(
        self,
        receiver_id: str,
        content: str,
        conversation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> A2ARequest:
        """
        Create an agent-to-agent request.
        
        Note: This method only creates the request object, it does not actually send it.
        The request object must be sent through an appropriate communication channel.
        
        Args:
            receiver_id: ID of the receiving agent
            content: Content of the message
            conversation_id: Optional ID of the conversation (created if not provided)
            metadata: Optional metadata for the request
            
        Returns:
            A2ARequest: The created A2A request
        """
        # Create or get conversation ID
        if not conversation_id:
            conversation_id = self.create_conversation()
        elif conversation_id not in self.state.conversations:
            self.create_conversation(conversation_id=conversation_id)
        
        # Create message
        message = Message(
            role=MessageRole.AGENT,
            content=content,
            name=self.profile.name,
            agent_id=self.agent_id
        )
        
        # Add message to conversation
        self.add_message(
            conversation_id=conversation_id,
            role=MessageRole.AGENT,
            content=content,
            name=self.profile.name,
            agent_id=self.agent_id
        )
        
        # Create and return A2A request
        return A2ARequest(
            sender=self.profile,
            receiver_id=receiver_id,
            conversation_id=conversation_id,
            message=message,
            metadata=metadata or {}
        )
    
    def update_memory(self, key: str, value: Any) -> None:
        """
        Update the agent's memory.
        
        Args:
            key: Memory key
            value: Memory value
        """
        self.state.memory[key] = value
    
    def get_memory(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the agent's memory.
        
        Args:
            key: Memory key
            default: Default value to return if key not found
            
        Returns:
            Any: The memory value, or default if not found
        """
        return self.state.memory.get(key, default)
