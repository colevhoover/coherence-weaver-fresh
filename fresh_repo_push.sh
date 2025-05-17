#!/bin/bash
# Script to create a fresh repository with no history and push to GitHub

echo "Creating and pushing a fresh repository with no history..."

# Create a temporary directory
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Copy all files except .git directory to temp directory
echo "Copying files to temporary directory..."
rsync -av --exclude='.git' --exclude='A2A/.git' . "$TEMP_DIR/"

# Navigate to temporary directory
cd "$TEMP_DIR"

# Initialize a new Git repository
echo "Initializing fresh Git repository..."
git init

# Add .gitignore for the new repository
echo "Adding all files to Git..."
git add .

# Commit files
echo "Committing files..."
git commit -m "Initial commit of Coherence Weaver"

# Set up the main branch
echo "Setting up main branch..."
git branch -M main

# Add GitHub as remote
echo "Adding GitHub remote..."
git remote add origin https://github.com/colevhoover/coherenceweaver.git

# Push to GitHub
echo "Pushing to GitHub..."
echo "You'll be prompted for your GitHub username and personal access token"
git push -f -u origin main

# Clean up
echo "Cleaning up..."
cd -

echo "Process completed! Check https://github.com/colevhoover/coherenceweaver to see if it was successful."
