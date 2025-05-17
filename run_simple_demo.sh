#!/bin/bash
# Script to run the simple Coherence Weaver agent demo

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

# Run the simple agent demo
echo "Running simple agent demo..."
python3 simple_agent_demo.py

echo "Demo completed"
