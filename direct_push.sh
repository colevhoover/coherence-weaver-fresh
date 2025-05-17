#!/bin/bash
# Non-interactive script to push the Coherence Weaver project to GitHub

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    Direct Push to GitHub Repository    ${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: Git is not installed. Please install Git first.${NC}"
    exit 1
fi

# Verify we're in the coherence_weaver directory
if [ ! -f "README.md" ] || [ ! -d "src" ]; then
    echo -e "${RED}Error: Please run this script from the coherence_weaver directory.${NC}"
    exit 1
fi

# User and repository details
GIT_NAME="Cole Hoover"
GIT_EMAIL="colevhoover@gmail.com"
REPO_URL="https://github.com/colevhoover/coherenceweaver.git"

# Initialize Git if needed
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing Git repository...${NC}"
    git init
fi

# Configure Git
echo -e "${YELLOW}Configuring Git...${NC}"
git config user.name "$GIT_NAME"
git config user.email "$GIT_EMAIL"

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo -e "${YELLOW}Creating .gitignore file...${NC}"
    cat > .gitignore << EOL
# Python virtual environment
coherence_weaver_env/
venv/
env/
ENV/

# Environment variables
.env

# Python cache files
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.coverage
htmlcov/

# Distribution / packaging
dist/
build/
*.egg-info/

# Logs
*.log
logs/

# OS specific files
.DS_Store
.idea/
.vscode/
*.swp
*~

# Local configuration
instance/
.webassets-cache

# Database
*.sqlite
*.db

# Jupyter Notebook
.ipynb_checkpoints
EOL
fi

# Add all files
echo -e "${YELLOW}Adding files to Git...${NC}"
git add .

# Make initial commit if needed
COMMIT_COUNT=$(git rev-list --all --count 2>/dev/null || echo "0")
if [ "$COMMIT_COUNT" -eq "0" ]; then
    echo -e "${YELLOW}Making initial commit...${NC}"
    git commit -m "Initial commit: Coherence Weaver Agent project"
fi

# Set remote
echo -e "${YELLOW}Setting up remote repository...${NC}"
if git remote | grep -q "^origin$"; then
    git remote remove origin
fi
git remote add origin "$REPO_URL"
echo -e "${GREEN}Remote 'origin' set to $REPO_URL${NC}"

echo -e "${BLUE}----------------------------------------${NC}"
echo -e "${YELLOW}Next steps to complete the GitHub push:${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
echo -e "${YELLOW}1. Create the GitHub repository at: https://github.com/new${NC}"
echo -e "${YELLOW}   - Name it 'coherenceweaver'${NC}"
echo -e "${YELLOW}   - Do NOT initialize it with any files${NC}"
echo -e ""
echo -e "${YELLOW}2. Create a personal access token at: https://github.com/settings/tokens${NC}"
echo -e "${YELLOW}   - Select at least the 'repo' scope${NC}"
echo -e "${YELLOW}   - Copy the token securely${NC}"
echo -e ""
echo -e "${YELLOW}3. Run the following command to push to GitHub:${NC}"
echo -e "${GREEN}   git push -u origin main${NC}"
echo -e ""
echo -e "${YELLOW}4. When prompted for your password, use the personal access token${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Repository is ready for pushing to GitHub.${NC}"
echo -e "${BLUE}========================================${NC}"
