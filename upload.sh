#!/bin/bash
# Super simple script to upload to GitHub

echo "Starting GitHub upload process..."

# Initialize Git repository
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit"

# Set the main branch
git branch -M main

# Connect to the GitHub repository
git remote add origin https://github.com/colevhoover/coherenceweaver.git

# Push code to GitHub (this will prompt for username and password)
echo "Pushing to GitHub... When prompted:"
echo "Username: colevhoover"
echo "Password: use your GitHub personal access token (<GITHUB_TOKEN>)"
git push -u origin main

echo "Done! Check https://github.com/colevhoover/coherenceweaver to see your files."
