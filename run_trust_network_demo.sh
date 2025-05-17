#!/bin/bash

# Run Trust Network Demo Script
# This script runs the Trust Network Tracking Tool demo

# Set the directory to the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ -d "coherence_weaver_env" ]; then
    echo "Activating virtual environment..."
    source coherence_weaver_env/bin/activate
fi

# Process command line arguments
API_ONLY=false
TOOLS_ONLY=false
INTEGRATION_ONLY=false
CLEAN_START=false
DATA_PATH=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --api-only) API_ONLY=true ;;
        --tools-only) TOOLS_ONLY=true ;;
        --integration-only) INTEGRATION_ONLY=true ;;
        --clean) CLEAN_START=true ;;
        --data-path) DATA_PATH="$2"; shift ;;
        --help) 
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --api-only            Run only the direct API demo"
            echo "  --tools-only          Run only the function tools demo"
            echo "  --integration-only    Show only the integration example"
            echo "  --clean               Start with a clean trust network"
            echo "  --data-path PATH      Custom path for trust network data file"
            echo "  --help                Show this help message"
            exit 0 ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

echo "========================================"
echo "Coherence Weaver Trust Network Demo"
echo "========================================"
echo ""

# Build the command with any options
CMD="python -m examples.trust_network_demo"
if [ "$API_ONLY" = true ]; then
    CMD="$CMD --api-only"
elif [ "$TOOLS_ONLY" = true ]; then
    CMD="$CMD --tools-only"
elif [ "$INTEGRATION_ONLY" = true ]; then
    CMD="$CMD --integration-only"
fi

if [ "$CLEAN_START" = true ]; then
    CMD="$CMD --clean"
fi

if [ -n "$DATA_PATH" ]; then
    CMD="$CMD --data-path $DATA_PATH"
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
