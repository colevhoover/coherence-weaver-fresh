#!/bin/bash
# Manual push script following GitHub's recommendations

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}  MANUAL PUSH TO GITHUB REPOSITORY ${NC}"
echo -e "${BLUE}==================================${NC}"

# Make sure we're in the coherence_weaver directory
if [ ! -d "src" ]; then
    echo -e "${RED}Please run this script from the coherence_weaver directory${NC}"
    exit 1
fi

# Initialize Git if needed
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing Git repository...${NC}"
    git init
fi

# Add a basic README.md file if it doesn't exist
if [ ! -f "README.md" ]; then
    echo -e "${YELLOW}Creating a README.md file...${NC}"
    echo "# Coherence Weaver" > README.md
    echo "An AI agent designed to facilitate justice-aligned collaboration between different AI systems" >> README.md
fi

# Configure Git
echo -e "${YELLOW}Configuring Git...${NC}"
git config user.name "Cole Hoover"
git config user.email "colevhoover@gmail.com"

# Add README.md first
echo -e "${YELLOW}Adding README.md...${NC}"
git add README.md

# Commit README
echo -e "${YELLOW}Committing README.md...${NC}"
git commit -m "first commit"

# Create main branch
echo -e "${YELLOW}Creating main branch...${NC}"
git branch -M main

# Set remote
echo -e "${YELLOW}Setting remote...${NC}"
git remote add origin https://github.com/colevhoover/coherenceweaver.git

# Push README first
echo -e "${YELLOW}Pushing README to GitHub...${NC}"
git push -u origin main

# Now add everything else
echo -e "${YELLOW}Adding remaining files...${NC}"
git add .

# Commit everything
echo -e "${YELLOW}Committing all files...${NC}"
git commit -m "Add complete Coherence Weaver project"

# Push everything
echo -e "${YELLOW}Pushing all files to GitHub...${NC}"
git push origin main

echo -e "${GREEN}Done! Your repository should now be populated with all files.${NC}"
echo -e "${GREEN}Check https://github.com/colevhoover/coherenceweaver${NC}"
