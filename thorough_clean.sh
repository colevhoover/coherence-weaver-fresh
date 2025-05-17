#!/bin/bash
# Thoroughly clean all GitHub tokens from all files

echo "Thoroughly cleaning all potential token references..."

# Find all text files and clean any GitHub tokens
find . -type f -not -path "*/\.*" -not -path "*/node_modules/*" -not -path "*/__pycache__/*" | \
while read file; do
  # Skip binary files and .git directory
  if [[ -f "$file" && "$file" != "./.git/"* && "$file" != "./A2A/.git/"* ]]; then
    # Check if file is binary
    if file "$file" | grep -q "text"; then
      echo "Cleaning $file..."
      # Replace any GitHub tokens with placeholder
      sed -i.bak 's/<GITHUB_TOKEN>[a-zA-Z0-9]*/<GITHUB_TOKEN>/g' "$file"
      # Remove backup files
      rm -f "$file.bak"
    fi
  fi
done

echo "Token cleaning completed!"
