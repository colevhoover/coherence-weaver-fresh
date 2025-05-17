#!/bin/bash
# Script to run the core agent test

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

# Check if the test file exists
if [ -f "tests/test_core.py" ]; then
    TEST_FILE="tests/test_core.py"
elif [ -f "tests/test_core_agent.py" ]; then
    TEST_FILE="tests/test_core_agent.py"
else
    echo "Core agent test file not found. Please ensure either tests/test_core.py or tests/test_core_agent.py exists."
    exit 1
fi

# Run the core agent test
echo "Running core agent test: $TEST_FILE"
python3 "$TEST_FILE"

echo "Core agent test completed."
