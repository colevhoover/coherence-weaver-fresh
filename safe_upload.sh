#!/bin/bash
# Safe script to upload to GitHub with force push to overwrite remote content

echo "Starting GitHub upload process..."

# Navigate to the coherence_weaver directory
cd "$(dirname "$0")"

# Check if .git directory exists, if so remove it to start fresh
if [ -d ".git" ]; then
    echo "Removing existing Git repository..."
    rm -rf .git
fi

# Initialize a new Git repository
echo "Initializing Git repository..."
git init

# Add all files
echo "Adding all files to Git..."
git add .

# Commit the files
echo "Committing files..."
git commit -m "Initial commit of Coherence Weaver"

# Set the main branch
echo "Setting up main branch..."
git branch -M main

# Remove origin if it exists
git remote remove origin 2>/dev/null

# Connect to the GitHub repository
echo "Connecting to GitHub repository..."
git remote add origin https://github.com/colevhoover/coherenceweaver.git

# Push code to GitHub with force flag
echo "Pushing to GitHub... When prompted:"
echo "Username: colevhoover"
echo "Password: use your GitHub personal access token"
echo "Using force push to overwrite any existing content on GitHub"
git push -f -u origin main

echo "Done! Check https://github.com/colevhoover/coherenceweaver to see your files."
