#!/bin/bash

# Test Configuration Script
# This script runs the configuration test utility

# Set the directory to the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ -d "coherence_weaver_env" ]; then
    echo "Activating virtual environment..."
    source coherence_weaver_env/bin/activate
fi

# Run the configuration test
echo "Running configuration test..."
python -m src.utils.config_test "$@"

# Deactivate virtual environment if we activated it
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Deactivating virtual environment..."
    deactivate
fi

echo "Configuration test completed."
