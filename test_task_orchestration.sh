#!/bin/bash
# Script to test the task orchestration protocol

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

# Test the task orchestration protocol
echo "Testing task orchestration protocol..."
python -m src.main orchestrate \
    --task "Analyze a large dataset of climate measurements to identify patterns and create visualization dashboards" \
    --agents-file "config/test_agents.json"

echo "Task orchestration test completed."
