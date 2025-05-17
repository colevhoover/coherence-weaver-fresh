"""
Client Module

This module provides a sample client for interacting with the Coherence Weaver agent system.
"""

import requests
import uuid
import json
import argparse
import sys
from typing import Dict, List, Any, Optional, Union

BASE_URL = "http://localhost:8000"  # Default URL to the Coherence Weaver API

class CoherenceWeaverClient:
    """
    Client for interacting with the Coherence Weaver agent system.
    """
    
    def __init__(self, base_url: str = BASE_URL, api_key: Optional[str] = None):
        """
        Initialize a new CoherenceWeaverClient instance.
        
        Args:
            base_url: Base URL for the Coherence Weaver API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url
        self.headers = {}
        
        if api_key:
            self.headers["X-API-Key"] = api_key
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a request to the Coherence Weaver API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Optional data to send in the request body
            params: Optional URL parameters
            
        Returns:
            Dict[str, Any]: Response from the API
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data, params=params)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=self.headers, json=data, params=params)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with API: {e}")
            if hasattr(e, "response") and e.response:
                print(f"Response: {e.response.text}")
            sys.exit(1)
    
    def check_health(self) -> Dict[str, Any]:
        """
        Check the health of the Coherence Weaver API.
        
        Returns:
            Dict[str, Any]: Health status
        """
        return self._request("GET", "/health")
    
    def get_agent_profile(self) -> Dict[str, Any]:
        """
        Get the profile of the Coherence Weaver agent.
        
        Returns:
            Dict[str, Any]: Agent profile
        """
        return self._request("GET", "/profile")
    
    def register_agent(
        self,
        agent_id: str,
        name: str,
        description: str,
        endpoint: str,
        capabilities: Optional[List[Dict[str, Any]]] = None,
        api_key: Optional[str] = None,
        version: str = "0.1.0",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Register a new agent with the system.
        
        Args:
            agent_id: Unique identifier for the agent
            name: Name of the agent
            description: Description of the agent's purpose and capabilities
            endpoint: API endpoint for communicating with the agent
            capabilities: Optional list of agent capabilities
            api_key: Optional API key for secure communication
            version: Optional version string for the agent
            metadata: Optional metadata for the agent
            
        Returns:
            Dict[str, Any]: Registration result
        """
        profile = {
            "id": agent_id,
            "name": name,
            "description": description,
            "version": version,
            "capabilities": capabilities or [],
            "metadata": metadata or {}
        }
        
        data = {
            "profile": profile,
            "endpoint": endpoint,
            "api_key": api_key
        }
        
        return self._request("POST", "/agents/register", data=data)
    
    def unregister_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Unregister an agent from the system.
        
        Args:
            agent_id: ID of the agent to unregister
            
        Returns:
            Dict[str, Any]: Unregistration result
        """
        return self._request("DELETE", f"/agents/{agent_id}")
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """
        List all registered agents.
        
        Returns:
            List[Dict[str, Any]]: List of registered agents
        """
        return self._request("GET", "/agents")
    
    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Get information about a specific agent.
        
        Args:
            agent_id: ID of the agent to get information about
            
        Returns:
            Dict[str, Any]: Agent information
        """
        return self._request("GET", f"/agents/{agent_id}")
    
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
        data = {
            "agent_id": agent_id,
            "description": description,
            "deadline": deadline,
            "metadata": metadata or {}
        }
        
        return self._request("POST", "/tasks", data=data)
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a task.
        
        Args:
            task_id: ID of the task to get status for
            
        Returns:
            Dict[str, Any]: Task status information
        """
        return self._request("GET", f"/tasks/{task_id}")
    
    def update_task_status(
        self,
        task_id: str,
        status: str,
        result: Any = None,
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update the status of a task.
        
        Args:
            task_id: ID of the task to update
            status: New status of the task (pending, in_progress, completed, failed)
            result: Optional result of the task
            error: Optional error message
            
        Returns:
            Dict[str, Any]: Update result
        """
        data = {
            "status": status,
            "result": result,
            "error": error
        }
        
        return self._request("PUT", f"/tasks/{task_id}", data=data)
    
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
        data = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "content": content,
            "conversation_id": conversation_id,
            "metadata": metadata or {}
        }
        
        return self._request("POST", "/messages/relay", data=data)
    
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
        data = {
            "name": name,
            "description": description,
            "agent_ids": agent_ids,
            "metadata": metadata or {}
        }
        
        return self._request("POST", "/groups", data=data)


def main():
    """
    Main function that demonstrates the usage of the CoherenceWeaverClient.
    """
    parser = argparse.ArgumentParser(description="Coherence Weaver Client")
    parser.add_argument("--url", default=BASE_URL, help="Base URL for the API")
    parser.add_argument("--api-key", help="API key for authentication")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    client = CoherenceWeaverClient(base_url=args.url, api_key=args.api_key)
    
    if args.interactive:
        interactive_mode(client)
    else:
        # Run a simple demonstration
        run_demonstration(client)


def run_demonstration(client: CoherenceWeaverClient):
    """
    Run a demonstration of the CoherenceWeaverClient.
    
    Args:
        client: CoherenceWeaverClient instance
    """
    print("=== Coherence Weaver Client Demonstration ===")
    
    # Check health
    print("\nChecking API health...")
    health = client.check_health()
    print(f"Health: {health}")
    
    # Get agent profile
    print("\nGetting agent profile...")
    profile = client.get_agent_profile()
    print(f"Agent Profile: {json.dumps(profile, indent=2)}")
    
    # Register a test agent
    agent_id = f"test-agent-{uuid.uuid4()}"
    print(f"\nRegistering test agent with ID {agent_id}...")
    register_result = client.register_agent(
        agent_id=agent_id,
        name="Test Agent",
        description="A test agent for demonstration purposes",
        endpoint="http://localhost:9000/agent",  # This would be a real endpoint in production
        capabilities=[
            {
                "name": "test",
                "description": "A test capability",
                "parameters": {}
            }
        ]
    )
    print(f"Registration result: {json.dumps(register_result, indent=2)}")
    
    # List all agents
    print("\nListing all agents...")
    agents = client.list_agents()
    print(f"Agents: {json.dumps(agents, indent=2)}")
    
    # Assign a task to the test agent
    print(f"\nAssigning task to agent {agent_id}...")
    task_result = client.assign_task(
        agent_id=agent_id,
        description="Test task",
        metadata={"priority": "low"}
    )
    print(f"Task assignment result: {json.dumps(task_result, indent=2)}")
    
    # Get task status
    task_id = task_result["task_id"]
    print(f"\nGetting status of task {task_id}...")
    task_status = client.get_task_status(task_id)
    print(f"Task status: {json.dumps(task_status, indent=2)}")
    
    # Update task status
    print(f"\nUpdating status of task {task_id} to completed...")
    update_result = client.update_task_status(
        task_id=task_id,
        status="completed",
        result={"message": "Task completed successfully"}
    )
    print(f"Update result: {json.dumps(update_result, indent=2)}")
    
    # Get updated task status
    print(f"\nGetting updated status of task {task_id}...")
    updated_status = client.get_task_status(task_id)
    print(f"Updated task status: {json.dumps(updated_status, indent=2)}")
    
    # Clean up by unregistering the test agent
    print(f"\nUnregistering test agent {agent_id}...")
    unregister_result = client.unregister_agent(agent_id)
    print(f"Unregistration result: {json.dumps(unregister_result, indent=2)}")
    
    print("\n=== Demonstration completed ===")


def interactive_mode(client: CoherenceWeaverClient):
    """
    Run the client in interactive mode.
    
    Args:
        client: CoherenceWeaverClient instance
    """
    print("=== Coherence Weaver Interactive Client ===")
    print("Type 'help' for a list of commands, 'exit' to quit.")
    
    while True:
        try:
            command = input("\n> ").strip()
            
            if command.lower() == "exit":
                break
            elif command.lower() == "help":
                print_help()
            elif command.lower() == "health":
                print(json.dumps(client.check_health(), indent=2))
            elif command.lower() == "profile":
                print(json.dumps(client.get_agent_profile(), indent=2))
            elif command.lower() == "agents":
                print(json.dumps(client.list_agents(), indent=2))
            elif command.lower().startswith("agent "):
                agent_id = command.split(" ", 1)[1]
                print(json.dumps(client.get_agent(agent_id), indent=2))
            elif command.lower() == "register":
                register_agent_interactive(client)
            elif command.lower().startswith("unregister "):
                agent_id = command.split(" ", 1)[1]
                print(json.dumps(client.unregister_agent(agent_id), indent=2))
            elif command.lower() == "task":
                assign_task_interactive(client)
            elif command.lower().startswith("task "):
                task_id = command.split(" ", 1)[1]
                print(json.dumps(client.get_task_status(task_id), indent=2))
            elif command.lower() == "update":
                update_task_interactive(client)
            elif command.lower() == "relay":
                relay_message_interactive(client)
            elif command.lower() == "group":
                create_group_interactive(client)
            else:
                print("Unknown command. Type 'help' for a list of commands.")
        
        except Exception as e:
            print(f"Error: {e}")


def print_help():
    """
    Print help information for interactive mode.
    """
    print("\nAvailable commands:")
    print("  help        - Show this help message")
    print("  exit        - Exit the interactive client")
    print("  health      - Check API health")
    print("  profile     - Get agent profile")
    print("  agents      - List all registered agents")
    print("  agent ID    - Get information about a specific agent")
    print("  register    - Register a new agent (interactive)")
    print("  unregister ID - Unregister an agent")
    print("  task        - Assign a task to an agent (interactive)")
    print("  task ID     - Get the status of a task")
    print("  update      - Update the status of a task (interactive)")
    print("  relay       - Relay a message from one agent to another (interactive)")
    print("  group       - Create an agent group (interactive)")


def register_agent_interactive(client: CoherenceWeaverClient):
    """
    Register a new agent interactively.
    
    Args:
        client: CoherenceWeaverClient instance
    """
    agent_id = input("Agent ID (leave empty for auto-generated): ").strip() or str(uuid.uuid4())
    name = input("Name: ").strip()
    description = input("Description: ").strip()
    endpoint = input("Endpoint: ").strip()
    version = input("Version (default: 0.1.0): ").strip() or "0.1.0"
    
    result = client.register_agent(
        agent_id=agent_id,
        name=name,
        description=description,
        endpoint=endpoint,
        version=version
    )
    
    print(json.dumps(result, indent=2))


def assign_task_interactive(client: CoherenceWeaverClient):
    """
    Assign a task to an agent interactively.
    
    Args:
        client: CoherenceWeaverClient instance
    """
    agent_id = input("Agent ID: ").strip()
    description = input("Task description: ").strip()
    deadline = input("Deadline (optional): ").strip() or None
    
    result = client.assign_task(
        agent_id=agent_id,
        description=description,
        deadline=deadline
    )
    
    print(json.dumps(result, indent=2))


def update_task_interactive(client: CoherenceWeaverClient):
    """
    Update the status of a task interactively.
    
    Args:
        client: CoherenceWeaverClient instance
    """
    task_id = input("Task ID: ").strip()
    status = input("Status (pending, in_progress, completed, failed): ").strip()
    result_str = input("Result (as JSON, optional): ").strip()
    error = input("Error (optional): ").strip() or None
    
    result = None
    if result_str:
        try:
            result = json.loads(result_str)
        except json.JSONDecodeError:
            result = result_str
    
    update_result = client.update_task_status(
        task_id=task_id,
        status=status,
        result=result,
        error=error
    )
    
    print(json.dumps(update_result, indent=2))


def relay_message_interactive(client: CoherenceWeaverClient):
    """
    Relay a message from one agent to another interactively.
    
    Args:
        client: CoherenceWeaverClient instance
    """
    sender_id = input("Sender ID: ").strip()
    receiver_id = input("Receiver ID: ").strip()
    content = input("Message content: ").strip()
    conversation_id = input("Conversation ID (optional): ").strip() or None
    
    result = client.relay_message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        conversation_id=conversation_id
    )
    
    print(json.dumps(result, indent=2))


def create_group_interactive(client: CoherenceWeaverClient):
    """
    Create an agent group interactively.
    
    Args:
        client: CoherenceWeaverClient instance
    """
    name = input("Group name: ").strip()
    description = input("Group description: ").strip()
    agent_ids_str = input("Agent IDs (comma-separated): ").strip()
    agent_ids = [id.strip() for id in agent_ids_str.split(",")]
    
    result = client.create_agent_group(
        name=name,
        description=description,
        agent_ids=agent_ids
    )
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
