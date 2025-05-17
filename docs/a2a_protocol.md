# Agent-to-Agent (A2A) Protocol Integration

This document describes how Coherence Weaver implements the Agent-to-Agent (A2A) Protocol to enable standardized communication and collaboration with other AI agents.

## What is the A2A Protocol?

The Agent-to-Agent (A2A) Protocol is a standardized communication framework that allows AI agents to discover, communicate with, and collaborate with each other. It defines how agents identify themselves, describe their capabilities, and exchange messages in a structured format.

## Agent Cards

At the core of the A2A Protocol is the concept of an "Agent Card" - a standardized identity and capability description that enables agents to discover and interact with each other. The Agent Card serves as a machine-readable profile that describes:

- Who the agent is
- What capabilities it offers
- How it can be contacted
- Authentication requirements

### Coherence Weaver's Agent Card

Coherence Weaver implements an A2A-compliant Agent Card with the following key capabilities:

1. **Multi-Agent Coordination**: Ability to coordinate complex tasks across multiple AI agents
2. **Pattern Recognition**: Ability to identify recurring patterns across different agent interactions
3. **Trust Building**: Ability to develop trust-based collaborative relationships between agents
4. **Justice Alignment**: Ability to ensure collaborations align with decolonized, justice-oriented principles

## A2A Integration Components

Coherence Weaver's A2A Protocol integration includes the following components:

### 1. Agent Card Utilities

Located in `src/utils/agent_card.py`, these utilities provide functions for:

- Creating A2A-compliant Agent Cards
- Validating Agent Cards against the A2A specification
- Loading Agent Cards from JSON files
- Saving Agent Cards to JSON files

### 2. Request/Response Models

Located in `src/models/agent_models.py`, these Pydantic models define the structure of:

- A2A requests from other agents
- A2A responses to other agents
- Agent profiles and capabilities
- Conversations and messages between agents

### 3. A2A Endpoint

Coherence Weaver exposes an A2A endpoint at `/a2a` which other agents can use to:

- Discover Coherence Weaver's capabilities
- Send messages and requests
- Initiate collaboration
- Exchange information

## Using the A2A Protocol

### Creating an Agent Card

```python
from coherence_weaver.src.utils import create_agent_card

# Define basic agent information
agent_config = {
    "name": "coherence-weaver",
    "description": "A specialized agent for coordinating multi-agent interactions"
}

# Create an A2A-compliant Agent Card
agent_card = create_agent_card(agent_config)
```

### Validating an Agent Card

```python
from coherence_weaver.src.utils import validate_agent_card

# Validate that an Agent Card follows the A2A specification
is_valid = validate_agent_card(agent_card)
```

### Saving and Loading Agent Cards

```python
from coherence_weaver.src.utils import save_agent_card_to_file, load_agent_card_from_file

# Save the Agent Card to a file
save_agent_card_to_file(agent_card, "coherence_weaver_card.json")

# Load the Agent Card from a file
loaded_card = load_agent_card_from_file("coherence_weaver_card.json")
```

## Running the A2A Demo

Coherence Weaver includes an Agent Card demo that demonstrates how to create, validate, and manage A2A-compliant Agent Cards:

```bash
./run_agent_card_demo.sh
```

This script creates an Agent Card for Coherence Weaver and saves it to `data/agent_cards/coherence_weaver_card.json`.

## A2A Communication Flow

1. **Discovery**: Other agents discover Coherence Weaver through its published Agent Card
2. **Connection**: Agents connect to Coherence Weaver's A2A endpoint using the information in the Agent Card
3. **Authentication**: Agents authenticate using the specified authentication method (bearer token)
4. **Capability Exploration**: Agents can query Coherence Weaver's capabilities
5. **Message Exchange**: Agents exchange structured messages according to the A2A Protocol
6. **Collaboration**: Agents work together on tasks, leveraging each other's capabilities

## Security Considerations

- All A2A communications are authenticated using bearer tokens
- Agent identities should be verified before engaging in sensitive operations
- Rate limiting is applied to prevent abuse
- Message validation ensures protocol compliance

## Future Enhancements

- Support for additional authentication methods
- Implementation of capability negotiation
- Enhanced trust mechanisms
- Federation with agent directories
- Support for standardized workflows and task delegation
