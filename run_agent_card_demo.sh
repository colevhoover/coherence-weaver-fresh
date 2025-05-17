#!/bin/bash

# This script runs the Agent Card Demo to demonstrate creating and managing
# A2A-compliant Agent Cards for the Coherence Weaver agent

# Change to the project root directory
cd "$(dirname "$0")"

# Ensure the script can find the module
export PYTHONPATH=$PYTHONPATH:$(pwd)/..

# Display a header
echo "=========================================="
echo "   Running Agent Card Demo"
echo "=========================================="
echo

# Run the demo
python3 examples/agent_card_demo.py

# Check if the demo was successful
if [ $? -eq 0 ]; then
    echo
    echo "=========================================="
    echo "   Agent Card Demo completed successfully"
    echo "=========================================="
else
    echo
    echo "=========================================="
    echo "   Error: Agent Card Demo failed"
    echo "=========================================="
    exit 1
fi

# Display information about the created files
echo
echo "Agent Card file is located at:"
echo "$(pwd)/data/agent_cards/coherence_weaver_card.json"
echo
echo "You can use this Agent Card for A2A Protocol communications"
echo "between Coherence Weaver and other A2A-compatible agents."
