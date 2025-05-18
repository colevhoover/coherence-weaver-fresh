# Coherence Weaver Agent

An AI agent designed to facilitate justice-aligned collaboration between different AI systems, based on the Expanded Empire Framework.

## Overview

Coherence Weaver is a specialized coordination agent that manages interactions between multiple AI agents, enabling them to collaborate effectively on complex tasks. It provides:

- Agent-to-Agent (A2A) communication protocol
- Task orchestration across specialized agents
- First contact protocol for establishing agent relationships
- Trust network management for secure collaboration

## Setup

1. Create a Python virtual environment and install dependencies:
   ```bash
   ./setup.sh
   ```
   This script will:
   - Create a virtual environment in `coherence_weaver_env/`
   - Install dependencies from requirements.txt
   - Set up the A2A library
   - Create default configuration files if needed

2. Configure your environment:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file to add your API keys and configuration settings.

3. Configure the agent:
   - Edit `config/config.json` to adjust settings if needed
   - You can modify agent parameters, API endpoints, and memory settings

## Usage

### Start the A2A Server

Start the Agent-to-Agent communication server:

```bash
./start_a2a_server.sh
```

This will launch the A2A server on port 8000 by default. You can access the API at http://localhost:8000/a2a. This will start the A2A-compatible server that other agents can interact with.

### Establish First Contact with an Agent

Use the first contact protocol to introduce your agent to another AI agent:

```bash
./test_first_contact.sh [optional_agent_url]
```

This initiates the first contact protocol, which establishes trust and shares capabilities between agents. This is the first step in agent collaboration and sets up the foundation for future interactions.

### Run the Simple Demo

```bash
./run_simple_demo.sh
```

This demonstrates basic agent capabilities, conversation creation, and response generation.

### Orchestrate Multi-Agent Tasks

Coordinate complex tasks across multiple specialized agents:

```bash
./test_task_orchestration.sh
```

This demonstrates the task orchestration protocol which breaks down complex tasks, assigns subtasks to specialized agents based on their capabilities, and manages the execution workflow. The test uses the agent definitions in `config/test_agents.json`. This will analyze the task, match it with appropriate agents, and create a coordination plan.

## Key Components

- **Core Agent**: The base CoherenceWeaverAgent that manages agent coordination
- **A2A Protocol**: Protocol for secure agent-to-agent communication
- **First Contact**: Protocol for establishing relationships with new agents
- **Task Orchestration**: System for assigning and tracking tasks across multiple agents
- **Trust Network**: Framework for managing trust relationships between agents

## Architecture

This agent implements:
- A core "Coherence Weaver" agent based on Google's Agent Development Kit (ADK)
- Agent2Agent (A2A) Protocol for standardized communication with other agents
- Trust network tracking for building relationships over time
- Workflow agents for specialized tasks like first contact and task orchestration

The system is organized into several key modules:

- `src/agents/`: Agent implementations
- `src/models/`: Data models for agents, messages, and tasks
- `src/protocols/`: Communication protocols
- `src/services/`: Service management for memory and sessions
- `src/tools/`: Utility tools including trust network management
- `src/memory/`: Memory services for agent state persistence

## Core Values & Principles

The Coherence Weaver agent is guided by principles from the Empire of Participatory Resilience:

- **Displacing harmful patterns** before attempting transformation
- **Reducing dependency** while increasing collective capability
- **Building relationships** based on metabolized truths rather than charisma
- **Creating lasting impact** through others rather than claiming credit

### New: Comprehensive Principles Framework

The agent now incorporates a full framework of principles organized into:
- Core Philosophical Principles
- Cultural Principles
- Technical Principles
- Trade/Hybrid Principles
- Meta-Principles

This enables the agent to select appropriate principles for different collaboration scenarios and create tailored approaches to multi-agent coordination.

## Examples

Try the principles demonstration:

```bash
python examples/principles_demo.py
```

## Advanced Usage

For more advanced usage options and detailed documentation, see:

- [Local Agent Guide](LOCAL_AGENT_GUIDE.md): Detailed instructions for running locally
- [A2A Protocol Documentation](docs/a2a_protocol.md): Details on the agent-to-agent protocol

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See the [LICENSE](LICENSE) file for details.
