#!/bin/bash
# Script to push the Coherence Weaver project to GitHub

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    Coherence Weaver GitHub Push Tool   ${NC}"
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

# Check if repository is already initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing Git repository...${NC}"
    git init
    
    # Create .gitignore file if it doesn't exist
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

# Prompt for GitHub information
echo -e "${BLUE}----------------------------------------${NC}"
echo -e "${BLUE}GitHub Repository Configuration${NC}"
echo -e "${BLUE}----------------------------------------${NC}"

# Git configuration
if [ -z "$(git config --get user.name)" ]; then
    echo -e "${YELLOW}Please enter your name for Git:${NC}"
    read GIT_NAME
    git config --global user.name "$GIT_NAME"
fi

if [ -z "$(git config --get user.email)" ]; then
    echo -e "${YELLOW}Please enter your email for Git:${NC}"
    read GIT_EMAIL
    git config --global user.email "$GIT_EMAIL"
fi

# GitHub configuration
echo -e "${YELLOW}Please enter your GitHub username:${NC}"
read GITHUB_USERNAME

echo -e "${YELLOW}Please enter your repository name (default: coherence-weaver):${NC}"
read REPO_NAME
REPO_NAME=${REPO_NAME:-coherence-weaver}

# Check if remote already exists
if git remote | grep -q "^origin$"; then
    echo -e "${YELLOW}Remote 'origin' already exists. Do you want to update it? (y/n)${NC}"
    read UPDATE_REMOTE
    if [[ $UPDATE_REMOTE =~ ^[Yy]$ ]]; then
        git remote remove origin
        git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
        echo -e "${GREEN}Remote 'origin' updated.${NC}"
    fi
else
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo -e "${GREEN}Remote 'origin' added.${NC}"
fi

# Inform about authentication
echo -e "${BLUE}----------------------------------------${NC}"
echo -e "${YELLOW}When prompted for password, use a Personal Access Token instead of your GitHub password.${NC}"
echo -e "${YELLOW}You can create a token at: https://github.com/settings/tokens${NC}"
echo -e "${BLUE}----------------------------------------${NC}"

# Push to GitHub
echo -e "${YELLOW}Do you want to push to GitHub now? (y/n)${NC}"
read PUSH_NOW
if [[ $PUSH_NOW =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Pushing to GitHub...${NC}"
    # Try to determine the default branch name
    DEFAULT_BRANCH=$(git branch --show-current)
    if [ -z "$DEFAULT_BRANCH" ]; then
        DEFAULT_BRANCH="main" # Use main as default if no branch exists yet
    fi
    
    git push -u origin $DEFAULT_BRANCH
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Successfully pushed to GitHub!${NC}"
        echo -e "${GREEN}Your repository is now available at: https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
    else
        echo -e "${RED}Push failed. Please check your credentials and try again.${NC}"
        echo -e "${YELLOW}You can manually push using: git push -u origin $DEFAULT_BRANCH${NC}"
    fi
else
    echo -e "${YELLOW}You can push later using: git push -u origin main${NC}"
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}GitHub setup complete.${NC}"
echo -e "${YELLOW}For more detailed instructions, see GITHUB_PUSH_GUIDE.md${NC}"
echo -e "${BLUE}========================================${NC}"
