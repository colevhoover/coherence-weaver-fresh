# Running Coherence Weaver Agent Locally

This guide provides instructions for running the Coherence Weaver agent on your local machine.

## Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

## Setup

1. First, run the setup script to create a virtual environment and install required dependencies:

```bash
./setup.sh
```

This script will:
- Create a Python virtual environment in `coherence_weaver_env/`
- Install all required packages
- Set up the A2A (Agent-to-Agent) library
- Create a default configuration file if one doesn't exist

## Running the Agent Locally

You have several options for running and testing the Coherence Weaver agent:

### Option 1: Simple Agent Demo

The simplest way to test the agent is to run the simple demo script:

```bash
./run_simple_demo.sh
```

This script demonstrates:
- Initializing a CoherenceWeaverAgent
- Displaying agent capabilities
- Creating a conversation
- Adding a user message
- Generating an agent response

### Option 2: Dedicated Test Scripts

We've created dedicated scripts for testing specific agent functionality:

#### A2A Server
Start the Agent-to-Agent (A2A) server:
```bash
./start_a2a_server.sh
```

#### Testing First Contact Protocol
Test the first contact protocol with another agent:
```bash
./test_first_contact.sh [optional_agent_url]
```
Default URL is http://localhost:8000/a2a

#### Testing Task Orchestration
Test the task orchestration protocol with multiple specialized agents:
```bash
./test_task_orchestration.sh
```
This uses the agent definitions in `config/test_agents.json`

#### Testing Core Agent
Run the core agent test suite:
```bash
./run_core_test.sh
```

### Option 3: Using the Main Demo Script

For more options, use the main demo script:

```bash
./run_demo.sh --help
```

Available options:
- `--server`: Start the Coherence Weaver server
- `--client`: Run the client demo
- `--interactive`: Run the client in interactive mode
- `--custom-agent`: Run the custom agent demo
- `--all`: Start the server and run the client demo in a separate terminal

For example:
```bash
./run_demo.sh --custom-agent
```

### Option 4: Using Command-Line Interface

For advanced usage, you can use the CLI directly:

```bash
# Start the server
python -m src.main server --host 0.0.0.0 --port 8000

# Initialize first contact with another agent
python -m src.main contact --agent-url http://other-agent-url:8000/a2a --message "Hello"

# Orchestrate a task
python -m src.main orchestrate --task "Analyze financial data" --agents-file agents.json

# Generate an agent card
python -m src.main card --output agent_card.json
```

## Running Multiple Components

To fully test the system, you may need to run multiple components simultaneously:

1. **Start the A2A server** in one terminal:
   ```bash
   ./start_a2a_server.sh
   ```

2. **Test communication** in another terminal:
   ```bash
   ./test_first_contact.sh
   ```

3. **Orchestrate tasks** in another terminal:
   ```bash
   ./test_task_orchestration.sh
   ```

Each of these components can be run in separate terminal windows to test the full functionality of the system.

## Troubleshooting

### Module Not Found Errors

If you encounter `ModuleNotFoundError: No module named 'coherence_weaver'`, it means the import paths are incorrectly configured. Try modifying the imports in the affected file to use relative imports instead of absolute imports.

For example, change:
```python
from coherence_weaver.src.agents.coherence_weaver_agent import CoherenceWeaverAgent
```

To:
```python
from src.agents.coherence_weaver_agent import CoherenceWeaverAgent
```

### Virtual Environment Issues

If you encounter errors related to missing packages, ensure the virtual environment is activated:

```bash
source coherence_weaver_env/bin/activate  # On Unix/Linux/macOS
coherence_weaver_env\Scripts\activate     # On Windows
```

### API Key Configuration

For functionality that requires API keys (e.g., for LLM services), ensure you have:

1. Copied the `.env.example` file to `.env`
2. Updated the `.env` file with your actual API keys

### Port Conflicts

If you encounter port conflicts (e.g., "Address already in use"), you can:
- Stop the process using the port: `lsof -i :<port>` then `kill <PID>`
- Or specify a different port: `./start_a2a_server.sh --port 8001`
