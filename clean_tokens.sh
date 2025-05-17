#!/bin/bash
# Script to clean personal access tokens from files

echo "Cleaning personal access tokens from files..."

# List of files that GitHub flagged
FILES=(
  "auth_push.sh"
  "final_push.sh"
  "manual_commands.txt"
  "simple_github_steps.md"
  "upload.sh"
)

# Clean each file
for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "Cleaning $file..."
    # Replace tokens with placeholder text
    sed -i '' 's/<GITHUB_TOKEN>[a-zA-Z0-9]*/<GITHUB_TOKEN>/g' "$file"
  fi
done

echo "Files cleaned. Now you can try pushing again."
