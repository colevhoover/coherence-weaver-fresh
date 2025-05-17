#!/bin/bash

# This script runs the Task Orchestration Protocol demonstration for Coherence Weaver,
# showing how the agent can decompose complex tasks, match them to appropriate agents,
# and coordinate their execution across multiple agents.

# Change to the project root directory
cd "$(dirname "$0")"

# Ensure the script can find the module
export PYTHONPATH=$PYTHONPATH:$(pwd)/..

# Display a header
echo "=========================================="
echo "   Running Task Orchestration Protocol Demo"
echo "=========================================="
echo
echo "This demonstration shows how Coherence Weaver:"
echo "  - Analyzes complex tasks into component subtasks"
echo "  - Matches subtasks to the most appropriate agents based on capabilities"
echo "  - Creates coordination structures for multi-agent collaboration"
echo "  - Establishes communication protocols and feedback mechanisms"
echo

# Run the demo
python3 examples/task_orchestration_demo.py

# Check if the demo was successful
if [ $? -eq 0 ]; then
    echo
    echo "=========================================="
    echo "   Task Orchestration Protocol Demo completed successfully"
    echo "=========================================="
else
    echo
    echo "=========================================="
    echo "   Error: Task Orchestration Protocol Demo failed"
    echo "=========================================="
    exit 1
fi

# Display information about the Task Orchestration Protocol
echo
echo "The Task Orchestration Protocol enables Coherence Weaver to:"
echo
echo "1. Break down complex tasks into well-defined components with clear"
echo "   inputs, outputs, and capability requirements"
echo
echo "2. Match tasks with agents based on capability alignment, prior"
echo "   performance, and complementary strengths"
echo
echo "3. Create structured coordination plans with defined interfaces,"
echo "   communication protocols, and feedback mechanisms"
echo
echo "4. Provide continuous monitoring, risk management, and adaptive"
echo "   coordination throughout task execution"
echo
echo "This protocol complements the A2A Protocol and First Contact Protocol"
echo "by enabling effective collaboration once relationships are established."
