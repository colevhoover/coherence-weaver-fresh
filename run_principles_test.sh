#!/bin/bash

# Run script for testing the participatory resilience principles

# Ensure we're in the project root directory
cd "$(dirname "$0")"

# Activate the virtual environment if it exists
if [ -d "coherence_weaver_env" ]; then
    echo "Activating virtual environment..."
    source coherence_weaver_env/bin/activate
fi

# Run the test script
echo "Running participatory resilience principles test..."
python tests/test_participatory_resilience.py

# Check if we should create a sample task with principle guidance
if [ "$1" == "--create-task" ]; then
    echo "Creating a sample task with principle guidance..."
    
    # Simple interactive task creation (future enhancement)
    echo "This feature will be implemented in a future version."
fi

# If running with --interactive flag, provide a menu of options
if [ "$1" == "--interactive" ]; then
    echo "Interactive mode:"
    echo "1. Run tests"
    echo "2. Explore principles by domain"
    echo "3. Generate guidance for a specific task"
    echo "4. Exit"
    
    read -p "Enter option (1-4): " option
    
    case $option in
        1)
            python tests/test_participatory_resilience.py
            ;;
        2)
            python -c "
import sys
from pathlib import Path
sys.path.append('src')
from participatory_resilience import get_principles_by_domain

domains = ['Culture', 'Tech', 'Trade']
print('\\nExploring principles by domain:\\n')

for domain in domains:
    principles = get_principles_by_domain(domain)
    print(f'\\n{domain} Domain: {len(principles)} principles')
    for name, principle in principles.items():
        print(f'  - {name}: {principle[\"description\"]}')
"
            ;;
        3)
            read -p "Enter task description: " task_description
            python -c "
import sys
from pathlib import Path
sys.path.append('src')
from participatory_resilience import create_principle_guidance

task_description = '$task_description'
guidance = create_principle_guidance(task_description)

print(f'\\nGuidance for task: \"{task_description}\"\\n')
print(f'Primary principles ({len(guidance[\"primary_principles\"])}):')
for p in guidance['primary_principles']:
    print(f'  - {p[\"name\"]} ({p[\"domain\"]}): {p[\"description\"]}')
    
print(f'\\nSupporting principles ({len(guidance[\"supporting_principles\"])}):')
for p in guidance['supporting_principles']:
    print(f'  - {p[\"name\"]} ({p[\"domain\"]}): {p[\"description\"]}')
    
print(f'\\nMeta principles ({len(guidance[\"meta_principles\"])}):')
for p in guidance['meta_principles']:
    print(f'  - {p[\"name\"]} ({p[\"domain\"]}): {p[\"description\"]}')
"
            ;;
        4)
            echo "Exiting."
            exit 0
            ;;
        *)
            echo "Invalid option."
            ;;
    esac
fi

echo "Done."
