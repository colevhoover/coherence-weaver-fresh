#!/bin/bash
# Combined script that runs both the repository creation and upload steps
# This script helps avoid the "prompt is too long" token limit issue by
# breaking the process into smaller steps

set -e  # Exit on error

echo "====================================================="
echo "GitHub Quick Upload for Coherence Weaver Project"
echo "====================================================="
echo 
echo "This script will:"
echo "1. Clean any sensitive data from the repository"
echo "2. Create a new GitHub repository if it doesn't exist"
echo "3. Upload the code in smaller chunks to avoid token limits"
echo
echo "Note: You'll need a GitHub Personal Access Token with 'repo' permissions"
echo "You can create one at: https://github.com/settings/tokens"
echo

# First run the cleaner script to remove any sensitive data
echo "Step 1: Cleaning repository files..."
cd "$(dirname "$0")"  # Make sure we're in the coherence_weaver directory
./thorough_clean.sh

# Create the GitHub repository
echo
echo "Step 2: Creating GitHub repository..."
./create_github_repo.sh

# Upload the code in chunks
echo
echo "Step 3: Uploading code to GitHub..."
./github_upload.sh

echo
echo "Process complete!"
echo "Your repository should now be available at: https://github.com/colevhoover/coherenceweaver"
