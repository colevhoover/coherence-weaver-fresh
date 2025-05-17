#!/bin/bash
# Final push script - non-interactive direct push to GitHub

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    Final Direct Push to GitHub         ${NC}"
echo -e "${BLUE}========================================${NC}"

# Repository details
GITHUB_USERNAME="colevhoover"
REPO_NAME="coherenceweaver"
BRANCH="main"
GITHUB_TOKEN="<GITHUB_TOKEN>"

# Configure Git
git config user.name "Cole Hoover"
git config user.email "colevhoover@gmail.com"

# Initialize Git if needed
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing Git repository...${NC}"
    git init
    
    # Make sure we're using main branch
    git checkout -b main
fi

# Update .gitignore
echo -e "${YELLOW}Updating .gitignore...${NC}"
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

# Security - scripts with tokens should be deleted
*token*_push.sh
final_push.sh
EOL

# Add all files
echo -e "${YELLOW}Adding files to Git...${NC}"
git add .

# Commit if there are changes
git diff --cached --quiet || git commit -m "Coherence Weaver Agent: Final commit for GitHub push"

# Create GitHub repository directly
echo -e "${YELLOW}Ensuring GitHub repository exists...${NC}"
curl -s -o /dev/null -H "Authorization: token $GITHUB_TOKEN" \
     -d "{\"name\":\"$REPO_NAME\",\"description\":\"Coherence Weaver: An AI agent for justice-aligned collaboration\"}" \
     https://api.github.com/user/repos

# Set up URL with token embedded
echo -e "${YELLOW}Setting up Git remote with token...${NC}"
REPO_URL="https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Configure remote
if git remote | grep -q "^origin$"; then
    git remote remove origin
fi

git remote add origin "$REPO_URL"

# Push with force if needed to ensure it works
echo -e "${YELLOW}Pushing to GitHub (force push)...${NC}"
git push -u origin $BRANCH --force

RESULT=$?

# Clean up - remove token from remote URL
git remote remove origin
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

if [ $RESULT -eq 0 ]; then
    echo -e "${GREEN}Successfully pushed to GitHub!${NC}"
    echo -e "${GREEN}Your repository is now available at: https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
    
    echo -e "${RED}IMPORTANT: Remember to delete this script as it contains your token${NC}"
    echo -e "${RED}Run: rm final_push.sh${NC}"
else
    echo -e "${RED}Push failed with error code: $RESULT${NC}"
    echo -e "${YELLOW}Check error messages above for details.${NC}"
fi

echo -e "${BLUE}========================================${NC}"
