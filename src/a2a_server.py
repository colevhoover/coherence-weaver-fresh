"""
A2A Server Module

This module implements a FastAPI server that exposes endpoints for the
Agent-to-Agent (A2A) Protocol, allowing other agents to communicate with
the Coherence Weaver agent.
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import json
import uvicorn

# Import Coherence Weaver components
from coherence_weaver.src.agents.coherence_weaver_agent import CoherenceWeaverAgent
from coherence_weaver.src.services.service_manager import ServiceManager
from coherence_weaver.src.utils.agent_card import create_agent_card
from coherence_weaver.src.tools.trust_network import TrustNetwork


class A2ARequest(BaseModel):
    """Model for A2A Protocol JSON-RPC request."""
    jsonrpc: str = "2.0"
    method: str
    params: Dict[str, Any]
    id: Optional[str] = None


class A2AResponse(BaseModel):
    """Model for A2A Protocol JSON-RPC response."""
    jsonrpc: str = "2.0"
    result: Any
    id: Optional[str] = None


class A2AErrorResponse(BaseModel):
    """Model for A2A Protocol JSON-RPC error response."""
    jsonrpc: str = "2.0"
    error: Dict[str, Any]
    id: Optional[str] = None


def create_a2a_server(config_path: str = "config/agent_config.json"):
    """
    Create and configure a FastAPI application that implements the A2A Protocol.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        FastAPI application
    """
    # Load configuration
    with open(config_path, "r") as f:
        config = json.load(f)
    
    # Initialize components
    agent = CoherenceWeaverAgent(config)
    service_manager = ServiceManager(config)
    memory_service = service_manager.get_memory_service()
    trust_network = TrustNetwork()
    
    # Create FastAPI app
    app = FastAPI(
        title="Coherence Weaver A2A Server",
        description="Agent-to-Agent Protocol Server for Coherence Weaver",
        version="1.0.0"
    )
    
    def verify_token(authorization: str = Header(...)):
        """
        Verify the bearer token in the Authorization header.
        
        Args:
            authorization: The Authorization header value
            
        Returns:
            True if the token is valid
            
        Raises:
            HTTPException: If the token is invalid
        """
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        token = authorization.replace("Bearer ", "")
        
        # Simple token verification, can be expanded with more secure validation
        if token != config.get("api", {}).get("auth_token", ""):
            raise HTTPException(status_code=401, detail="Invalid token")
            
        return True
    
    @app.get("/a2a/card", tags=["A2A Protocol"])
    async def get_agent_card():
        """
        Return the Agent Card for this agent.
        
        The Agent Card follows the A2A Protocol specification and contains
        information about the agent's identity, capabilities, and API.
        
        Returns:
            Agent Card dictionary
        """
        return create_agent_card(config)
    
    @app.post("/a2a/rpc", tags=["A2A Protocol"])
    async def handle_rpc(request: A2ARequest, authorized: bool = Depends(verify_token)):
        """
        Handle JSON-RPC requests according to A2A protocol.
        
        This endpoint processes A2A protocol methods and returns appropriate responses.
        All requests must be authenticated with a valid bearer token.
        
        Args:
            request: The A2A request
            authorized: Authorization result from verify_token
            
        Returns:
            A2AResponse or A2AErrorResponse
        """
        try:
            # Handle different RPC methods
            if request.method == "create_task":
                # Create a new task
                task_id = agent.create_task(request.params)
                return A2AResponse(
                    jsonrpc="2.0",
                    result={"task_id": task_id, "status": "created"},
                    id=request.id
                )
                
            elif request.method == "get_task":
                # Get task status
                task_id = request.params.get("task_id")
                if not task_id:
                    raise ValueError("task_id is required")
                    
                task_status = agent.get_task_status(task_id)
                return A2AResponse(
                    jsonrpc="2.0",
                    result=task_status,
                    id=request.id
                )
                
            elif request.method == "submit_message":
                # Submit a message to the agent
                message = request.params.get("message")
                if not message:
                    raise ValueError("message is required")
                    
                conversation_id = request.params.get("conversation_id", "default")
                result = agent.process_message(message, conversation_id)
                return A2AResponse(
                    jsonrpc="2.0",
                    result=result,
                    id=request.id
                )
                
            elif request.method == "trust_assessment":
                # Perform trust assessment
                agent_id = request.params.get("agent_id")
                if not agent_id:
                    raise ValueError("agent_id is required")
                    
                assessment = trust_network.assess_trust(agent_id)
                return A2AResponse(
                    jsonrpc="2.0",
                    result=assessment,
                    id=request.id
                )
                
            else:
                # Method not found
                return A2AErrorResponse(
                    jsonrpc="2.0",
                    error={
                        "code": -32601, 
                        "message": f"Method '{request.method}' not found"
                    },
                    id=request.id
                )
                
        except Exception as e:
            # Internal error
            return A2AErrorResponse(
                jsonrpc="2.0",
                error={
                    "code": -32603, 
                    "message": str(e)
                },
                id=request.id
            )
    
    @app.get("/a2a/health", tags=["System"])
    async def health_check():
        """
        Health check endpoint.
        
        Returns:
            Dictionary with status information
        """
        return {"status": "healthy", "version": "1.0.0"}
    
    return app


def start_server(host: str = "0.0.0.0", port: int = 8000, 
                 config_path: str = "config/agent_config.json"):
    """
    Start the A2A server.
    
    Args:
        host: Host address to bind to
        port: Port to listen on
        config_path: Path to the configuration file
    """
    app = create_a2a_server(config_path)
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Start the A2A Protocol server for Coherence Weaver")
    parser.add_argument("--host", default="0.0.0.0", help="Host address to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    parser.add_argument("--config", default="config/agent_config.json", help="Path to configuration file")
    
    args = parser.parse_args()
    
    # Start the server with provided arguments
    start_server(host=args.host, port=args.port, config_path=args.config)
