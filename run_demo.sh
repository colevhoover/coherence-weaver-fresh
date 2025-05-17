#!/bin/bash
# Script to run the Coherence Weaver demo

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

# Check if the first argument is --help or -h
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    echo "Coherence Weaver Demo Runner"
    echo
    echo "Usage: ./run_demo.sh [OPTION]"
    echo
    echo "Options:"
    echo "  --server        Start the Coherence Weaver server"
    echo "  --client        Run the client demo"
    echo "  --interactive   Run the client in interactive mode"
    echo "  --custom-agent  Run the custom agent demo"
    echo "  --all           Start the server and run the client demo in a separate terminal"
    echo "  --help, -h      Show this help message"
    echo
    exit 0
fi

# Function to start the server
start_server() {
    echo "Starting Coherence Weaver server..."
    python -m src.main
}

# Function to run the client demo
run_client() {
    echo "Running client demo..."
    python -m src.client
}

# Function to run the client in interactive mode
run_interactive_client() {
    echo "Running client in interactive mode..."
    python -m src.client --interactive
}

# Function to run the custom agent demo
run_custom_agent_demo() {
    echo "Running custom agent demo..."
    python examples/custom_agent_demo.py
}

# Process command line arguments
case "$1" in
    --server)
        start_server
        ;;
    --client)
        run_client
        ;;
    --interactive)
        run_interactive_client
        ;;
    --custom-agent)
        run_custom_agent_demo
        ;;
    --all)
        # Start the server in a new terminal and run the client demo
        echo "Starting server and client in separate processes..."
        
        # Detect operating system for the correct terminal command
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            osascript -e 'tell app "Terminal" to do script "cd \"'$PWD'\" && source coherence_weaver_env/bin/activate && python -m src.main"'
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux with x-terminal-emulator
            if command -v x-terminal-emulator &> /dev/null; then
                x-terminal-emulator -e "bash -c 'cd \"$PWD\" && source coherence_weaver_env/bin/activate && python -m src.main; exec bash'" &
            # Try gnome-terminal
            elif command -v gnome-terminal &> /dev/null; then
                gnome-terminal -- bash -c "cd \"$PWD\" && source coherence_weaver_env/bin/activate && python -m src.main; exec bash"
            # Try xterm
            elif command -v xterm &> /dev/null; then
                xterm -e "bash -c 'cd \"$PWD\" && source coherence_weaver_env/bin/activate && python -m src.main; exec bash'" &
            else
                echo "Could not find a suitable terminal emulator. Please start the server manually."
                exit 1
            fi
        elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            # Windows
            start cmd /k "cd /d \"%CD%\" && coherence_weaver_env\Scripts\activate && python -m src.main"
        else
            echo "Unsupported operating system. Please start the server manually."
            exit 1
        fi
        
        # Wait for the server to start
        echo "Waiting for server to start..."
        sleep 5
        
        # Run the client demo
        run_client
        ;;
    *)
        # Default to showing help
        echo "No option specified. Use --help to see available options."
        echo "Starting the server by default..."
        start_server
        ;;
esac

exit 0
