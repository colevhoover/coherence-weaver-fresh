#!/bin/bash

# Run Service Demo Script
# This script runs the Service Manager Demo

# Set the directory to the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ -d "coherence_weaver_env" ]; then
    echo "Activating virtual environment..."
    source coherence_weaver_env/bin/activate
fi

# Process command line arguments
MEMORY_ONLY=false
SESSION_ONLY=false
LLM_ONLY=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --memory-only) MEMORY_ONLY=true ;;
        --session-only) SESSION_ONLY=true ;;
        --llm-only) LLM_ONLY=true ;;
        --help) 
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --memory-only        Run only memory service demo"
            echo "  --session-only       Run only session service demo"
            echo "  --llm-only           Run only LLM agent integration demo"
            echo "  --help               Show this help message"
            exit 0 ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

echo "========================================"
echo "Coherence Weaver Service Demo"
echo "========================================"
echo ""
echo "First, let's test our configuration system:"
echo ""

# Run the configuration test first
./test_config.sh

echo ""
echo "Now, let's run the Service Manager demo:"
echo ""

# Build the command with any options
CMD="python -m examples.service_demo"
if [ "$MEMORY_ONLY" = true ]; then
    CMD="$CMD --memory-only"
elif [ "$SESSION_ONLY" = true ]; then
    CMD="$CMD --session-only"
elif [ "$LLM_ONLY" = true ]; then
    CMD="$CMD --llm-only"
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
