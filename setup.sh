#!/bin/bash
# Setup script for Coherence Weaver

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is required but could not be found. Please install Python 3 and try again."
    exit 1
fi

echo "=== Setting up Coherence Weaver ==="
echo

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv coherence_weaver_env

# Determine the OS to activate the environment correctly
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "Activating virtual environment (Windows)..."
    source coherence_weaver_env/Scripts/activate
else
    # Unix-like systems (macOS, Linux)
    echo "Activating virtual environment (Unix)..."
    source coherence_weaver_env/bin/activate
fi

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if A2A directory already exists
if [ ! -d "A2A" ]; then
    echo "Cloning A2A repository..."
    git clone https://github.com/google/A2A.git
    if [ $? -ne 0 ]; then
        echo "Failed to clone A2A repository. Please check your internet connection and try again."
        exit 1
    fi
fi

# Install A2A in development mode
echo "Installing A2A in development mode..."
cd A2A
pip install -e .
cd ..

# Create examples directory if it doesn't exist
if [ ! -d "examples" ]; then
    echo "Creating examples directory..."
    mkdir -p examples
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "NOTE: Please edit .env file to add your Google API key and other settings."
fi

echo
echo "=== Setup completed successfully ==="
echo
echo "To activate the virtual environment:"
echo "  - On Windows: coherence_weaver_env\\Scripts\\activate"
echo "  - On macOS/Linux: source coherence_weaver_env/bin/activate"
echo
echo "To run the server:"
echo "  python -m src.main"
echo
echo "To run the demo client:"
echo "  python -m src.client"
echo
