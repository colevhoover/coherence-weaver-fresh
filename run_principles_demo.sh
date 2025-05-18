#!/bin/bash

# Run script for the participatory resilience principles demonstration

# Ensure we're in the project root directory
cd "$(dirname "$0")"

# Activate the virtual environment if it exists
if [ -d "coherence_weaver_env" ]; then
    echo "Activating virtual environment..."
    source coherence_weaver_env/bin/activate
fi

# Run the principles demo
echo "Running participatory resilience principles demonstration..."
python examples/principles_demo.py

echo "Done."
