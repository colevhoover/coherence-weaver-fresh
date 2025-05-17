"""
Agent Models Module

This module defines the data models used for agent-to-agent communication
and internal state representation.
"""

from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """Enumeration of possible message roles in a conversation."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    AGENT = "agent"
    FUNCTION = "function"


class MessageContent(BaseModel):
    """Content of a message, which can be text or other types."""
    type: str = Field(default="text")
    text: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class Message(BaseModel):
    """A message in a conversation between agents."""
    role: MessageRole
    content: Union[str, List[MessageContent], List[Dict[str, Any]]]
    name: Optional[str] = None
    agent_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Conversation(BaseModel):
    """A conversation between agents."""
    id: str
    messages: List[Message] = []
    metadata: Optional[Dict[str, Any]] = None


class AgentCapability(BaseModel):
    """Describes a capability that an agent has."""
    name: str
    description: str
    parameters: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentProfile(BaseModel):
    """Profile information about an agent."""
    id: str
    name: str
    description: str
    version: str
    capabilities: List[AgentCapability] = []
    metadata: Optional[Dict[str, Any]] = None


class AgentState(BaseModel):
    """Internal state of an agent."""
    id: str
    profile: AgentProfile
    conversations: Dict[str, Conversation] = {}
    memory: Dict[str, Any] = {}
    metadata: Optional[Dict[str, Any]] = None


class A2ARequest(BaseModel):
    """A request from one agent to another."""
    sender: AgentProfile
    receiver_id: str
    conversation_id: str
    message: Message
    metadata: Optional[Dict[str, Any]] = None


class A2AResponse(BaseModel):
    """A response from one agent to another."""
    sender: AgentProfile
    receiver_id: str
    conversation_id: str
    message: Message
    status: str = "success"
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentRegistration(BaseModel):
    """Information for registering an agent with a coordinator."""
    profile: AgentProfile
    endpoint: str
    api_key: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class TaskAssignment(BaseModel):
    """A task assigned to an agent."""
    id: str
    agent_id: str
    description: str
    conversation_id: str
    deadline: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class TaskStatus(str, Enum):
    """Enumeration of possible task statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskResult(BaseModel):
    """Result of a completed task."""
    task_id: str
    agent_id: str
    status: TaskStatus
    result: Any
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
