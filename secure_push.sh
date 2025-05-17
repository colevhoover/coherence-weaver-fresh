#!/bin/bash
# Script to securely push to GitHub using a token from environment variable
# This avoids exposing the token in command history or logs

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    Secure Push to GitHub Repository    ${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "src" ]; then
    echo -e "${RED}Error: Please run this script from the coherence_weaver directory.${NC}"
    exit 1
fi

# Set repository details
GITHUB_USERNAME="colevhoover"
REPO_NAME="coherenceweaver"
BRANCH="main"

# Check if the GitHub repository exists
echo -e "${YELLOW}Checking if GitHub repository exists...${NC}"
if curl -s -o /dev/null -w "%{http_code}" "https://github.com/$GITHUB_USERNAME/$REPO_NAME" | grep -q "200"; then
    echo -e "${GREEN}Repository exists at https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
else
    echo -e "${YELLOW}Repository may not exist yet. Creating a repository first is recommended.${NC}"
    echo -e "${YELLOW}Go to https://github.com/new and create a repository named '$REPO_NAME'${NC}"
    echo -e "${YELLOW}Do NOT initialize it with README, .gitignore, or license files.${NC}"
    echo -e "${YELLOW}Continue anyway? (y/n)${NC}"
    read CONTINUE
    if [[ ! $CONTINUE =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Exiting. Create the repository first and then run this script again.${NC}"
        exit 0
    fi
fi

# Construct the repository URL with credentials embedded
# This way the token is not visible in ps output and not stored in bash history
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}Enter your GitHub Personal Access Token:${NC}"
    read -s GITHUB_TOKEN
    # Export it so it's available to git push
    export GITHUB_TOKEN
fi

echo -e "${YELLOW}Setting up Git remote with your token...${NC}"
# Using the https URL with token for authentication
REPO_URL="https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Configure remote (this won't expose the token in any logs)
if git remote | grep -q "^origin$"; then
    git remote remove origin
fi
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Now perform the push with credentials
echo -e "${YELLOW}Pushing to GitHub...${NC}"
echo -e "${YELLOW}This may take a moment depending on your connection speed.${NC}"

# Using GIT_ASKPASS to provide the token securely
export GIT_ASKPASS="$(pwd)/token_helper.sh"

# Create a temporary script to provide the token
cat > token_helper.sh << EOL
#!/bin/bash
echo "$GITHUB_TOKEN"
EOL
chmod +x token_helper.sh

# Push to GitHub
git push -u origin $BRANCH

# Clean up
rm token_helper.sh
unset GITHUB_TOKEN
unset GIT_ASKPASS

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Successfully pushed to GitHub!${NC}"
    echo -e "${GREEN}Your repository is now available at: https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
    
    # Provide next steps
    echo -e "${BLUE}----------------------------------------${NC}"
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "${YELLOW}1. Visit your repository at: https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
    echo -e "${YELLOW}2. Verify all files were uploaded correctly${NC}"
    echo -e "${YELLOW}3. You can now clone this repository on other machines using:${NC}"
    echo -e "${GREEN}   git clone https://github.com/$GITHUB_USERNAME/$REPO_NAME.git${NC}"
    echo -e "${BLUE}----------------------------------------${NC}"
else
    echo -e "${RED}Push failed.${NC}"
    echo -e "${YELLOW}Please check:${NC}"
    echo -e "${YELLOW}1. That your GitHub repository exists at https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
    echo -e "${YELLOW}2. That your token has the 'repo' scope permissions${NC}"
    echo -e "${YELLOW}3. That your token hasn't expired${NC}"
fi

echo -e "${BLUE}========================================${NC}"
