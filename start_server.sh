#!/bin/bash

# Start Server Script
# This script starts the Coherence Weaver server with the new configuration system

# Set the directory to the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ -d "coherence_weaver_env" ]; then
    echo "Activating virtual environment..."
    source coherence_weaver_env/bin/activate
fi

# Process command line arguments
ENV_ONLY=false
DEBUG=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --env-only) ENV_ONLY=true ;;
        --debug) DEBUG=true ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Run the server
echo "Starting Coherence Weaver server..."

# Set environment variables based on arguments
if [ "$ENV_ONLY" = true ]; then
    export SKIP_JSON_CONFIG=True
    echo "Using environment variables only (JSON configs disabled)"
fi

if [ "$DEBUG" = true ]; then
    export DEBUG=True
    echo "Debug mode enabled"
fi

# Start the server
python -m src.main

# Deactivate virtual environment if we activated it
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Deactivating virtual environment..."
    deactivate
fi
