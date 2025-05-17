#!/bin/bash

# Coherence Weaver CLI Entry Point
# This script provides a convenient way to run the Coherence Weaver CLI commands

# Change to the project root directory
cd "$(dirname "$0")"

# Ensure the script can find the module
export PYTHONPATH=$PYTHONPATH:$(pwd)/..

# Display header if no arguments provided
if [ $# -eq 0 ]; then
    echo "=========================================="
    echo "   Coherence Weaver CLI"
    echo "=========================================="
    echo
    echo "Usage: ./coherence_weaver_cli.sh COMMAND [OPTIONS]"
    echo
    echo "Available commands:"
    echo "  server         Start the A2A server"
    echo "  contact        Establish first contact with an agent"
    echo "  orchestrate    Orchestrate a collaborative task"
    echo "  card           Generate or display an Agent Card"
    echo "  discover       Discover an agent by retrieving its Agent Card"
    echo
    echo "For command-specific help:"
    echo "  ./coherence_weaver_cli.sh COMMAND --help"
    echo
    exit 0
fi

# Run the Python CLI with all arguments
python3 -m coherence_weaver.src.main "$@"

# Check if the command was successful
if [ $? -eq 0 ]; then
    exit 0
else
    echo
    echo "Error: Command failed with an error."
    exit 1
fi
