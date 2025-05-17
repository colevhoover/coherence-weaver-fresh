#!/bin/bash
# Authenticated push script
# This script uses token authentication to push files to GitHub

# Define colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}  AUTHENTICATED GITHUB PUSH SCRIPT ${NC}"
echo -e "${BLUE}==================================${NC}"

# GitHub details
GITHUB_USERNAME="colevhoover"
REPO_NAME="coherenceweaver"
TOKEN="<GITHUB_TOKEN>"
AUTH_URL="https://$GITHUB_USERNAME:$TOKEN@github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Step 1: Clean start - remove any existing git directory
echo -e "${YELLOW}Step 1: Ensuring clean Git environment...${NC}"
rm -rf .git
echo -e "${GREEN}Removed existing Git configuration${NC}"

# Step 2: Initialize Git
echo -e "${YELLOW}Step 2: Initializing Git repository...${NC}"
git init
echo -e "${GREEN}Git repository initialized${NC}"

# Step 3: Configure Git
echo -e "${YELLOW}Step 3: Configuring Git identity...${NC}"
git config user.name "Cole Hoover"
git config user.email "colevhoover@gmail.com"
echo -e "${GREEN}Git user configured${NC}"

# Step 4: Add all files
echo -e "${YELLOW}Step 4: Adding all files to Git...${NC}"
git add .
echo -e "${GREEN}Files added${NC}"

# Step 5: Commit files
echo -e "${YELLOW}Step 5: Committing files...${NC}"
git commit -m "Initial commit"
echo -e "${GREEN}Files committed${NC}"

# Step 6: Create main branch
echo -e "${YELLOW}Step 6: Setting up main branch...${NC}"
git branch -M main
echo -e "${GREEN}Main branch created${NC}"

# Step 7: Set remote with authentication
echo -e "${YELLOW}Step 7: Setting remote with authentication...${NC}"
git remote add origin "$AUTH_URL"
echo -e "${GREEN}Remote added with authentication${NC}"

# Step 8: Push to GitHub
echo -e "${YELLOW}Step 8: Pushing to GitHub (this may take a moment)...${NC}"
git push -u origin main
PUSH_RESULT=$?

if [ $PUSH_RESULT -eq 0 ]; then
    echo -e "${GREEN}Successfully pushed to GitHub!${NC}"
    echo -e "${GREEN}Your repository is now available at: https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
else
    echo -e "${RED}Push failed with error code: $PUSH_RESULT${NC}"
    
    # Try with force push
    echo -e "${YELLOW}Trying with force push...${NC}"
    git push -f origin main
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Force push successful!${NC}"
        echo -e "${GREEN}Your repository is now available at: https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
    else
        echo -e "${RED}Force push also failed.${NC}"
        echo -e "${RED}Please check GitHub status and credentials.${NC}"
    fi
fi

# Clean up - remove sensitive information from Git config
git remote remove origin
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo -e "${YELLOW}IMPORTANT: Delete this script as it contains your GitHub token${NC}"
echo -e "${YELLOW}Run: rm auth_push.sh${NC}"

echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}           PUSH COMPLETE          ${NC}"
echo -e "${BLUE}==================================${NC}"
