#!/bin/bash

# This script runs the First Contact Protocol demonstration for Coherence Weaver,
# showing how the agent can discover, analyze, and establish relationships with 
# previously unknown agents.

# Change to the project root directory
cd "$(dirname "$0")"

# Ensure the script can find the module
export PYTHONPATH=$PYTHONPATH:$(pwd)/..

# Display a header
echo "=========================================="
echo "   Running First Contact Protocol Demo"
echo "=========================================="
echo
echo "This demonstration shows how Coherence Weaver:"
echo "  - Discovers new agents and analyzes their capabilities"
echo "  - Builds relationship strategies based on capability assessments"
echo "  - Initiates contact with tailored collaboration proposals"
echo "  - Establishes foundations for ongoing agent-to-agent relationships"
echo

# Run the demo
python3 examples/first_contact_demo.py

# Check if the demo was successful
if [ $? -eq 0 ]; then
    echo
    echo "=========================================="
    echo "   First Contact Protocol Demo completed successfully"
    echo "=========================================="
else
    echo
    echo "=========================================="
    echo "   Error: First Contact Protocol Demo failed"
    echo "=========================================="
    exit 1
fi

# Display information about the First Contact Protocol
echo
echo "The First Contact Protocol enables Coherence Weaver to establish"
echo "effective relationships with previously unknown agents by:"
echo
echo "1. Mapping agent capabilities through communication analysis"
echo "2. Building relationship strategies focused on mutual benefit"
echo "3. Creating foundations for long-term collaborative interactions"
echo
echo "This protocol builds on the A2A Protocol, using Agent Cards and"
echo "standardized communication methods with a focus on understanding"
echo "the unique capabilities and interaction patterns of each agent."
