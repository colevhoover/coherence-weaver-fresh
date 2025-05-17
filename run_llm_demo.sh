#!/bin/bash

# Run LLM Agent Demo Script
# This script runs the Coherence Weaver LLM Agent demo

# Set the directory to the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ -d "coherence_weaver_env" ]; then
    echo "Activating virtual environment..."
    source coherence_weaver_env/bin/activate
fi

# Process command line arguments
USE_ENV=false
CUSTOM_CONFIG=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --env) USE_ENV=true ;;
        --config) CUSTOM_CONFIG="$2"; shift ;;
        --help) 
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --env                Use environment variables for configuration"
            echo "  --config FILE        Use a custom configuration file"
            echo "  --help               Show this help message"
            exit 0 ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

echo "========================================"
echo "Coherence Weaver LLM Agent Demo"
echo "========================================"
echo ""
echo "First, let's test our configuration system:"
echo ""

# Run the configuration test first
./test_config.sh

echo ""
echo "Now, let's run the LLM Agent demo:"
echo ""

# Build the command with any options
CMD="python -m examples.llm_agent_demo"
if [ "$USE_ENV" = true ]; then
    CMD="$CMD --env"
fi
if [ -n "$CUSTOM_CONFIG" ]; then
    CMD="$CMD --config $CUSTOM_CONFIG"
fi

# Run the demo
$CMD

# Deactivate virtual environment if we activated it
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Deactivating virtual environment..."
    deactivate
fi

echo ""
echo "Demo completed successfully!"
echo "========================================"
