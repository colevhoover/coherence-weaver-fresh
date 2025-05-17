#!/bin/bash

# Run the core agent test script
echo "Running core agent test..."
cd "$(dirname "$0")"
python3 tests/test_core_agent.py
