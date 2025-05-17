#!/bin/bash
# Script to start the A2A server

# Ensure the virtual environment is activated
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "Activating virtual environment..."
    
    # Detect operating system
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        if [ -f "coherence_weaver_env/Scripts/activate" ]; then
            source coherence_weaver_env/Scripts/activate
        else
            echo "Virtual environment not found. Please run setup.sh first."
            exit 1
        fi
    else
        # Unix-like systems
        if [ -f "coherence_weaver_env/bin/activate" ]; then
            source coherence_weaver_env/bin/activate
        else
            echo "Virtual environment not found. Please run setup.sh first."
            exit 1
        fi
    fi
fi

# Start the A2A server
echo "Starting A2A server on port 8000..."
python -m src.main server --port 8000

echo "Server terminated."
