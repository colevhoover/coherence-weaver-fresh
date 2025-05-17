"""
A2A Client Module

This module provides a client for communicating with other agents using the
Agent-to-Agent (A2A) Protocol. It allows the Coherence Weaver agent to
discover and interact with other A2A-compliant agents.
"""

import json
import requests
import uuid
from typing import Dict, Any, List, Optional, Union


class A2AClient:
    """
    Client for communicating with A2A-compliant agents.
    
    This client handles the details of the A2A Protocol, including authentication,
    RPC requests, and Agent Card retrieval.
    """
    
    def __init__(self, base_url: Optional[str] = None, auth_token: Optional[str] = None):
        """
        Initialize the A2A client.
        
        Args:
            base_url: The base URL of the agent to communicate with
            auth_token: Optional authentication token for the agent
        """
        self.base_url = base_url.rstrip('/') if base_url else None
        self.auth_token = auth_token
        self.agent_card = None
        
        # Set up headers
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if auth_token:
            self.headers["Authorization"] = f"Bearer {auth_token}"
    
    def fetch_agent_card(self, agent_url: str) -> Dict[str, Any]:
        """
        Fetch the agent card from another A2A-compatible agent.
        
        Args:
            agent_url: URL of the agent to fetch the card from
            
        Returns:
            Agent Card dictionary
            
        Raises:
            requests.HTTPError: If the request fails
        """
        response = requests.get(f"{agent_url}/a2a/card", headers=self.headers)
        response.raise_for_status()
        
        agent_card = response.json()
        return agent_card
    
    def get_agent_card(self) -> Dict[str, Any]:
        """
        Retrieve the Agent Card from the agent configured in this client.
        
        Returns:
            Agent Card dictionary
            
        Raises:
            requests.HTTPError: If the request fails
            ValueError: If no base_url is configured
        """
        if not self.base_url:
            raise ValueError("No base URL configured. Use fetch_agent_card() or set base_url.")
            
        self.agent_card = self.fetch_agent_card(self.base_url)
        return self.agent_card
    
    def check_health(self, agent_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Check the health of an agent.
        
        Args:
            agent_url: Optional URL of the agent to check. If not provided,
                      uses the base_url configured in this client.
            
        Returns:
            Health status dictionary
            
        Raises:
            requests.HTTPError: If the request fails
            ValueError: If no agent_url is provided and no base_url is configured
        """
        url = agent_url or self.base_url
        
        if not url:
            raise ValueError("No URL provided. Provide agent_url or set base_url.")
            
        url = f"{url}/a2a/health"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def create_task(self, agent_url: Optional[str] = None, 
                   messages: List[Dict[str, Any]] = None,
                   description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new task with another agent.
        
        Args:
            agent_url: Optional URL of the agent to create a task with. If not provided,
                      uses the base_url configured in this client.
            messages: Optional list of initial messages for the task
            description: Optional description of the task
            
        Returns:
            Response from the agent, containing task information
            
        Raises:
            requests.HTTPError: If the request fails
            ValueError: If no agent_url is provided and no base_url is configured
        """
        url = agent_url or self.base_url
        
        if not url:
            raise ValueError("No URL provided. Provide agent_url or set base_url.")
            
        payload = {
            "jsonrpc": "2.0",
            "method": "create_task",
            "params": {
                "messages": messages or []
            },
            "id": str(uuid.uuid4())
        }
        
        if description:
            payload["params"]["description"] = description
        
        response = requests.post(
            f"{url}/a2a/rpc",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        
        return response.json()
    
    def get_task_status(self, task_id: str, agent_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the status of a task.
        
        Args:
            task_id: ID of the task
            agent_url: Optional URL of the agent that has the task. If not provided,
                       uses the base_url configured in this client.
            
        Returns:
            Task status information
            
        Raises:
            requests.HTTPError: If the request fails
            ValueError: If no agent_url is provided and no base_url is configured
        """
        url = agent_url or self.base_url
        
        if not url:
            raise ValueError("No URL provided. Provide agent_url or set base_url.")
            
        payload = {
            "jsonrpc": "2.0",
            "method": "get_task",
            "params": {
                "task_id": task_id
            },
            "id": str(uuid.uuid4())
        }
        
        response = requests.post(
            f"{url}/a2a/rpc",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        
        return response.json()
    
    def submit_message(self, message: Union[str, Dict[str, Any]], 
                      conversation_id: str = 'default',
                      agent_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Submit a message to an agent.
        
        Args:
            message: The message text or message object
            conversation_id: Optional conversation ID
            agent_url: Optional URL of the agent to submit the message to. If not provided,
                       uses the base_url configured in this client.
            
        Returns:
            Agent's response
            
        Raises:
            requests.HTTPError: If the request fails
            ValueError: If no agent_url is provided and no base_url is configured
        """
        url = agent_url or self.base_url
        
        if not url:
            raise ValueError("No URL provided. Provide agent_url or set base_url.")
            
        # Convert string messages to message objects
        if isinstance(message, str):
            message = {
                'role': 'user',
                'content': message
            }
            
        payload = {
            "jsonrpc": "2.0",
            "method": "submit_message",
            "params": {
                "message": message,
                "conversation_id": conversation_id
            },
            "id": str(uuid.uuid4())
        }
        
        response = requests.post(
            f"{url}/a2a/rpc",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        
        return response.json()
    
    def assess_trust(self, agent_id: str, agent_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Request a trust assessment for an agent.
        
        Args:
            agent_id: ID of the agent to assess
            agent_url: Optional URL of the agent to request the assessment from. If not provided,
                       uses the base_url configured in this client.
            
        Returns:
            Trust assessment information
            
        Raises:
            requests.HTTPError: If the request fails
            ValueError: If no agent_url is provided and no base_url is configured
        """
        url = agent_url or self.base_url
        
        if not url:
            raise ValueError("No URL provided. Provide agent_url or set base_url.")
            
        payload = {
            "jsonrpc": "2.0",
            "method": "trust_assessment",
            "params": {
                "agent_id": agent_id
            },
            "id": str(uuid.uuid4())
        }
        
        response = requests.post(
            f"{url}/a2a/rpc",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        
        return response.json()
    
    def call_method(self, method: str, params: Dict[str, Any], 
                   agent_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Call a method on an agent using the A2A Protocol.
        
        This is a general-purpose method for calling any RPC method supported by the agent.
        
        Args:
            method: Name of the method to call
            params: Parameters for the method
            agent_url: Optional URL of the agent to call the method on. If not provided,
                       uses the base_url configured in this client.
            
        Returns:
            Result of the method call
            
        Raises:
            requests.HTTPError: If the request fails
            ValueError: If no agent_url is provided and no base_url is configured or if the agent returns an error
        """
        url = agent_url or self.base_url
        
        if not url:
            raise ValueError("No URL provided. Provide agent_url or set base_url.")
            
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": str(uuid.uuid4())
        }
        
        response = requests.post(
            f"{url}/a2a/rpc",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        
        result = response.json()
        
        if 'error' in result:
            raise ValueError(f"Agent returned an error: {result['error']}")
            
        return result


def discover_agent(agent_url: str, auth_token: Optional[str] = None) -> Dict[str, Any]:
    """
    Discover an agent by retrieving its Agent Card.
    
    Args:
        agent_url: URL of the agent
        auth_token: Optional authentication token for the agent
        
    Returns:
        Agent Card dictionary
        
    Raises:
        requests.HTTPError: If the request fails
    """
    client = A2AClient(auth_token=auth_token)
    return client.fetch_agent_card(agent_url)


def create_conversation(agents: List[A2AClient], 
                        topic: str, 
                        initial_message: str) -> Dict[str, Any]:
    """
    Create a conversation between multiple agents.
    
    Args:
        agents: List of A2A clients for participating agents
        topic: Topic of the conversation
        initial_message: Initial message to start the conversation
        
    Returns:
        Conversation details dictionary
    """
    # Create a conversation ID
    conversation_id = f"conv_{uuid.uuid4().hex[:8]}"
    
    # Keep track of all messages
    messages = []
    
    # Send the initial message to the first agent
    if agents:
        first_agent = agents[0]
        if not first_agent.base_url:
            raise ValueError("First agent must have a base_url configured")
            
        first_response = first_agent.submit_message(
            initial_message, 
            conversation_id=conversation_id
        )
        
        messages.append({
            'role': 'user',
            'content': initial_message
        })
        
        result = first_response.get('result', {})
        messages.append(result.get('message', {
            'role': 'assistant',
            'content': 'No response'
        }))
    
    # Return the conversation details
    return {
        'conversation_id': conversation_id,
        'topic': topic,
        'agents': [a.base_url for a in agents if a.base_url],
        'messages': messages
    }


def initiate_collaboration(agent_url: str, 
                          message: str, 
                          auth_token: Optional[str] = None) -> Dict[str, Any]:
    """
    Initiate collaboration with another agent.
    
    This is a convenience function that:
    1. Discovers the agent by fetching its Agent Card
    2. Creates a new task with the agent
    3. Returns information about the initiated collaboration
    
    Args:
        agent_url: URL of the agent to collaborate with
        message: Initial message for the collaboration
        auth_token: Optional authentication token for the agent
        
    Returns:
        Collaboration information
        
    Raises:
        requests.HTTPError: If any request fails
    """
    # Create the client
    client = A2AClient(auth_token=auth_token)
    
    # Discover the agent
    agent_card = client.fetch_agent_card(agent_url)
    
    # Create a message object
    message_obj = {
        'role': 'user',
        'content': message
    }
    
    # Create a task
    task_response = client.create_task(
        agent_url=agent_url,
        messages=[message_obj],
        description=f"Collaboration initiated at {uuid.uuid4().hex[:8]}"
    )
    
    # Get the task ID
    result = task_response.get('result', {})
    task_id = result.get('task_id')
    
    # Return information about the collaboration
    return {
        'agent_card': agent_card,
        'task_id': task_id,
        'message': message,
        'status': 'collaboration_initiated'
    }


if __name__ == "__main__":
    import argparse
    import pprint
    
    parser = argparse.ArgumentParser(description="Test the A2A client with a remote agent")
    parser.add_argument("--url", help="URL of the remote agent")
    parser.add_argument("--token", help="Authentication token (if required)")
    parser.add_argument("--method", default="get_card", 
                        choices=["get_card", "health", "create_task", "message", "collaborate"],
                        help="Method to test")
    parser.add_argument("--param", action="append", help="Parameters in the form key=value")
    
    args = parser.parse_args()
    
    # Parse parameters
    params = {}
    if args.param:
        for p in args.param:
            key, value = p.split('=', 1)
            params[key] = value
    
    try:
        if args.method == "get_card":
            if not args.url:
                parser.error("--url is required for get_card")
                
            # Discover an agent
            agent_card = discover_agent(args.url, args.token)
            print("\nAgent Card:")
            pprint.pprint(agent_card)
            
        elif args.method == "health":
            if not args.url:
                parser.error("--url is required for health")
                
            # Create A2A client
            client = A2AClient(args.url, args.token)
            
            # Check health
            health = client.check_health()
            print("\nHealth Status:")
            pprint.pprint(health)
            
        elif args.method == "create_task":
            if not args.url:
                parser.error("--url is required for create_task")
                
            # Create A2A client
            client = A2AClient(args.url, args.token)
            
            # Create a task
            description = params.get('description', 'Test task')
            response = client.create_task(description=description)
            
            print("\nTask Creation Response:")
            pprint.pprint(response)
            
            # Get the task ID
            result = response.get('result', {})
            task_id = result.get('task_id')
            
            if task_id:
                # Get task status
                status_response = client.get_task_status(task_id)
                print("\nTask Status:")
                pprint.pprint(status_response)
            
        elif args.method == "message":
            if not args.url:
                parser.error("--url is required for message")
                
            # Create A2A client
            client = A2AClient(args.url, args.token)
            
            # Submit a message
            message = params.get('message', 'Hello, agent!')
            conversation_id = params.get('conversation_id', 'test')
            
            response = client.submit_message(message, conversation_id)
            print("\nAgent Response:")
            pprint.pprint(response)
            
        elif args.method == "collaborate":
            if not args.url:
                parser.error("--url is required for collaborate")
                
            # Initiate collaboration
            message = params.get('message', 'Hello, I would like to collaborate with you.')
            
            collaboration = initiate_collaboration(args.url, message, args.token)
            print("\nCollaboration Initiated:")
            pprint.pprint(collaboration)
        
        print("\nA2A communication successful!")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
