"""
Server Module

This module defines the FastAPI server that exposes the agent functionality
through HTTP endpoints.
"""

import uuid
from typing import Dict, List, Optional, Any, Union
from fastapi import FastAPI, HTTPException, Depends, Header, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import json

from .config import HOST, PORT, DEBUG
from .models.agent_models import (
    AgentProfile, AgentRegistration, A2ARequest, A2AResponse,
    Message, MessageRole, TaskStatus
)
from .agents.coherence_weaver_agent import CoherenceWeaverAgent
from .utils.logging_utils import get_logger

# Initialize logging
logger = get_logger("server")

# Initialize FastAPI app
app = FastAPI(
    title="Coherence Weaver API",
    description="API for interacting with the Coherence Weaver agent system",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize CoherenceWeaverAgent
coherence_weaver = CoherenceWeaverAgent()

# Helper function to get the agent
def get_agent():
    return coherence_weaver

# Authentication middleware (simple API key-based auth for demo purposes)
async def verify_api_key(request: Request, x_api_key: Optional[str] = Header(None)):
    # This is a simple example. In production, use a more secure authentication method.
    # For now, we'll accept any API key or none at all since this is just a demo.
    return True


@app.get("/")
async def root():
    """
    Root endpoint that provides basic information about the API.
    """
    return {
        "name": "Coherence Weaver API",
        "version": "0.1.0",
        "description": "API for interacting with the Coherence Weaver agent system",
        "documentation": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {
        "status": "ok",
        "timestamp": uuid.uuid1().time
    }


@app.get("/profile")
async def get_agent_profile(agent=Depends(get_agent)):
    """
    Get the profile of the Coherence Weaver agent.
    """
    return agent.get_profile()


@app.post("/agents/register")
async def register_agent(
    registration: AgentRegistration,
    agent=Depends(get_agent),
    authenticated: bool = Depends(verify_api_key)
):
    """
    Register a new agent with the system.
    """
    if not authenticated:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    result = agent.register_agent(
        profile=registration.profile,
        endpoint=registration.endpoint,
        api_key=registration.api_key
    )
    
    return result


@app.delete("/agents/{agent_id}")
async def unregister_agent(
    agent_id: str,
    agent=Depends(get_agent),
    authenticated: bool = Depends(verify_api_key)
):
    """
    Unregister an agent from the system.
    """
    if not authenticated:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    result = agent.unregister_agent(agent_id=agent_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result


@app.get("/agents")
async def list_agents(
    agent=Depends(get_agent),
    authenticated: bool = Depends(verify_api_key)
):
    """
    List all registered agents.
    """
    if not authenticated:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return agent.list_agents()


@app.get("/agents/{agent_id}")
async def get_agent_info(
    agent_id: str,
    agent=Depends(get_agent),
    authenticated: bool = Depends(verify_api_key)
):
    """
    Get information about a specific agent.
    """
    if not authenticated:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    result = agent.get_agent(agent_id=agent_id)
    
    if result is None:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    return result


@app.post("/tasks")
async def assign_task(
    task: Dict[str, Any],
    agent=Depends(get_agent),
    authenticated: bool = Depends(verify_api_key)
):
    """
    Assign a task to an agent.
    """
    if not authenticated:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    if "agent_id" not in task or "description" not in task:
        raise HTTPException(status_code=400, detail="agent_id and description are required")
    
    result = agent.assign_task(
        agent_id=task["agent_id"],
        description=task["description"],
        deadline=task.get("deadline"),
        metadata=task.get("metadata")
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result


@app.get("/tasks/{task_id}")
async def get_task_status(
    task_id: str,
    agent=Depends(get_agent),
    authenticated: bool = Depends(verify_api_key)
):
    """
    Get the status of a task.
    """
    if not authenticated:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    result = agent.get_task_status(task_id=task_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result


@app.put("/tasks/{task_id}")
async def update_task_status(
    task_id: str,
    update: Dict[str, Any],
    agent=Depends(get_agent),
    authenticated: bool = Depends(verify_api_key)
):
    """
    Update the status of a task.
    """
    if not authenticated:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    if "status" not in update:
        raise HTTPException(status_code=400, detail="status is required")
    
    try:
        status = TaskStatus(update["status"])
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {update['status']}")
    
    result = agent.update_task_status(
        task_id=task_id,
        status=status,
        result=update.get("result"),
        error=update.get("error")
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result


@app.post("/messages/relay")
async def relay_message(
    message: Dict[str, Any],
    agent=Depends(get_agent),
    authenticated: bool = Depends(verify_api_key)
):
    """
    Relay a message from one agent to another.
    """
    if not authenticated:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    required_fields = ["sender_id", "receiver_id", "content"]
    for field in required_fields:
        if field not in message:
            raise HTTPException(status_code=400, detail=f"{field} is required")
    
    result = agent.relay_message(
        sender_id=message["sender_id"],
        receiver_id=message["receiver_id"],
        content=message["content"],
        conversation_id=message.get("conversation_id"),
        metadata=message.get("metadata")
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result


@app.post("/a2a")
async def process_a2a_request(
    request: A2ARequest,
    agent=Depends(get_agent),
    authenticated: bool = Depends(verify_api_key)
):
    """
    Process an agent-to-agent request.
    """
    if not authenticated:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    response = agent.process_a2a_request(request=request)
    
    if response.status == "error":
        logger.warning(f"A2A request processing error: {response.error}")
    
    return response


@app.post("/groups")
async def create_agent_group(
    group: Dict[str, Any],
    agent=Depends(get_agent),
    authenticated: bool = Depends(verify_api_key)
):
    """
    Create a group of agents for collaborative tasks.
    """
    if not authenticated:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    required_fields = ["name", "description", "agent_ids"]
    for field in required_fields:
        if field not in group:
            raise HTTPException(status_code=400, detail=f"{field} is required")
    
    result = agent.create_agent_group(
        name=group["name"],
        description=group["description"],
        agent_ids=group["agent_ids"],
        metadata=group.get("metadata")
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result


def start_server():
    """
    Start the FastAPI server.
    """
    import uvicorn
    
    logger.info(f"Starting server on {HOST}:{PORT}")
    uvicorn.run(
        "src.server:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )


if __name__ == "__main__":
    start_server()
