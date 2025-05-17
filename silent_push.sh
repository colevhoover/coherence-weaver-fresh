#!/bin/bash
# Silent script to push to GitHub without interactive prompts

echo "Starting non-interactive GitHub upload process..."

# Navigate to the coherence_weaver directory
cd "$(dirname "$0")"

# Check if .git directory exists, if not initialize it
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
fi

# Configure Git to save credentials temporarily (15 minutes)
git config --global credential.helper 'cache --timeout=900'

# Add all files
echo "Adding files to Git..."
git add .

# Commit changes
echo "Committing changes..."
git commit -m "Upload Coherence Weaver with cleaned token files"

# Set the main branch
echo "Setting up main branch..."
git branch -M main

# Remove origin if it exists
git remote remove origin 2>/dev/null

# Add the remote origin
echo "Setting up remote repository..."
git remote add origin https://github.com/colevhoover/coherenceweaver.git

# Allow unrelated histories
git config pull.rebase false

# Push with force flag (this is where you'll need to enter credentials)
echo "Force pushing to GitHub..."
echo "You will be prompted for your GitHub username and personal access token"
git push -f -u origin main

echo "Push attempt completed. Check https://github.com/colevhoover/coherenceweaver to see if it was successful."
echo "If the push failed, you can run this script again or try pushing manually with:"
echo "  git push -f origin main"
