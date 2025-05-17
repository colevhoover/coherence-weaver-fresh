#!/bin/bash
# Final safe script to upload to GitHub with tokens cleaned

echo "Starting final GitHub upload process..."

# Navigate to the coherence_weaver directory
cd "$(dirname "$0")"

# Add all the cleaned files
echo "Adding cleaned files to Git..."
git add .

# Commit the changes
echo "Committing token cleanup changes..."
git commit -m "Clean tokens and prepare for GitHub upload"

# Push code to GitHub with force flag
echo "Pushing to GitHub... When prompted:"
echo "Username: colevhoover"
echo "Password: use your GitHub personal access token"
echo "Using force push to overwrite any existing content on GitHub"
git push -f -u origin main

echo "Done! Check https://github.com/colevhoover/coherenceweaver to see your files."
