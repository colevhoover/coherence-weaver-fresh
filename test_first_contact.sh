#!/bin/bash
# Script to test the first contact protocol

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

# Get the agent URL from first argument or use default
AGENT_URL=${1:-"http://localhost:8000/a2a"}

# Test the first contact protocol
echo "Testing first contact protocol with agent at $AGENT_URL..."
python -m src.main contact \
    --agent-url "$AGENT_URL" \
    --message "Hello, I'm an AI assistant specializing in data analysis. I'd like to explore collaboration opportunities."

echo "First contact test completed."
