#!/bin/bash
# Script to create a GitHub repository via GitHub API
# Must run this before running github_upload.sh

set -e  # Exit on error

REPO_NAME="coherenceweaver"
GITHUB_USERNAME="colevhoover"
REPO_DESCRIPTION="An AI agent designed to facilitate justice-aligned collaboration between different AI systems"
REPO_VISIBILITY="public"  # or "private"

echo "This script will create a new GitHub repository: $GITHUB_USERNAME/$REPO_NAME"
echo "Please provide your GitHub Personal Access Token (PAT)"
echo "You can create one at: https://github.com/settings/tokens"
echo "Make sure it has 'repo' permissions"
echo ""
read -p "GitHub Personal Access Token: " GITHUB_TOKEN

if [ -z "$GITHUB_TOKEN" ]; then
  echo "Error: GitHub token is required"
  exit 1
fi

# Create the repository using GitHub API
echo "Creating GitHub repository..."

# Prepare JSON payload
JSON_PAYLOAD=$(cat << EOF
{
  "name": "$REPO_NAME",
  "description": "$REPO_DESCRIPTION",
  "private": $([ "$REPO_VISIBILITY" = "private" ] && echo "true" || echo "false"),
  "auto_init": false
}
EOF
)

# Create repository using GitHub API
RESPONSE=$(curl -s -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d "$JSON_PAYLOAD" \
  "https://api.github.com/user/repos")

# Check if repository was created successfully
if echo "$RESPONSE" | grep -q "\"name\":\"$REPO_NAME\""; then
  echo "Repository created successfully!"
  echo "URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
  
  # Update the git configuration for the upload script
  echo "Configuring local git settings..."
  
  # Save the token temporarily for git push (will be used by github_upload.sh)
  # The token is stored in an environment variable
  export GITHUB_TOKEN
  
  # Setting the remote URL with authentication embedded
  REMOTE_URL="https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com/$GITHUB_USERNAME/$REPO_NAME.git"
  
  echo "GitHub repository is ready for upload."
  echo "Now you can run: ./github_upload.sh"
  echo ""
  echo "IMPORTANT: For security, this script does not save your token permanently."
  echo "You'll need to provide it again if you restart your session."
  
else
  echo "Failed to create repository. API response:"
  echo "$RESPONSE"
  exit 1
fi
