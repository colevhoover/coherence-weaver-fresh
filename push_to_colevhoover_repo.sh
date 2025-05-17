#!/bin/bash
# Script to push the Coherence Weaver project to Cole Hoover's GitHub repository

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    Pushing to colevhoover's GitHub     ${NC}"
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
fi

# Configure Git with the provided information
echo -e "${YELLOW}Configuring Git with colevhoover's information...${NC}"
git config user.name "Cole Hoover"
git config user.email "colevhoover@gmail.com"

# Add all files
echo -e "${YELLOW}Adding files to Git...${NC}"
git add .

# Make initial commit if needed
COMMIT_COUNT=$(git rev-list --all --count 2>/dev/null || echo "0")
if [ "$COMMIT_COUNT" -eq "0" ]; then
    echo -e "${YELLOW}Making initial commit...${NC}"
    git commit -m "Initial commit: Coherence Weaver Agent project"
fi

# Set remote to the provided URL
echo -e "${YELLOW}Setting up remote repository...${NC}"
if git remote | grep -q "^origin$"; then
    git remote remove origin
fi
git remote add origin "https://github.com/colevhoover/coherenceweaver.git"
echo -e "${GREEN}Remote 'origin' set to https://github.com/colevhoover/coherenceweaver.git${NC}"

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
        echo -e "${GREEN}Your repository is now available at: https://github.com/colevhoover/coherenceweaver${NC}"
    else
        echo -e "${RED}Push failed. Please check your credentials and try again.${NC}"
        echo -e "${YELLOW}Make sure you're using a Personal Access Token and not your password.${NC}"
        echo -e "${YELLOW}You can manually push using: git push -u origin $DEFAULT_BRANCH${NC}"
    fi
else
    echo -e "${YELLOW}You can push later using: git push -u origin $DEFAULT_BRANCH${NC}"
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}GitHub setup complete.${NC}"
echo -e "${BLUE}========================================${NC}"
