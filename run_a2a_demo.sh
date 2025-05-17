#!/bin/bash

# This script runs the A2A Protocol demonstration for Coherence Weaver,
# showing how the agent can communicate with other agents using the
# Agent-to-Agent (A2A) Protocol

# Change to the project root directory
cd "$(dirname "$0")"

# Ensure the script can find the module
export PYTHONPATH=$PYTHONPATH:$(pwd)/..

# Display a header
echo "=========================================="
echo "   Running A2A Protocol Demonstration"
echo "=========================================="
echo
echo "This demonstration shows how Coherence Weaver:"
echo "  - Creates and publishes A2A-compliant Agent Cards"
echo "  - Discovers other A2A-compliant agents"
echo "  - Communicates with other agents using the A2A Protocol"
echo "  - Coordinates conversations between multiple agents"
echo

# Run the demo
python3 examples/a2a_protocol_demo.py

# Check if the demo was successful
if [ $? -eq 0 ]; then
    echo
    echo "=========================================="
    echo "   A2A Protocol Demo completed successfully"
    echo "=========================================="
else
    echo
    echo "=========================================="
    echo "   Error: A2A Protocol Demo failed"
    echo "=========================================="
    exit 1
fi

# Display information about the demo
echo
echo "The demo has created a sample Agent Card at:"
echo "$(pwd)/data/agent_cards/coherence_weaver_card.json"
echo
echo "For more information about the A2A Protocol, see:"
echo "$(pwd)/docs/a2a_protocol.md"
echo
echo "To run a real A2A server, use:"
echo "./start_a2a_server.sh"
echo
echo "To interact with other A2A agents, use the A2A client:"
echo "python3 -m coherence_weaver.src.a2a_client --url http://remote-agent-url/a2a --token your_token"
