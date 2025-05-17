# Simple Steps to Put Your Project on GitHub

This is a straightforward guide to get your Coherence Weaver project on GitHub in just a few steps.

## Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com/) and sign in
2. Click the "+" icon in the top-right corner and select "New repository"
3. Name it "coherenceweaver"
4. Leave the description blank or add a simple description
5. Keep it Public (or Private if you prefer)
6. Do NOT initialize with README, .gitignore, or license
7. Click "Create repository"

## Step 2: Open Terminal and Run These Commands

Open Terminal and copy-paste these commands one by one:

```bash
# 1. Go to your project directory
cd /Users/colehoover/Documents/Cline/Svalbard\ 1/Svalbard/coherence_weaver

# 2. Initialize Git repository
git init

# 3. Add all your files
git add .

# 4. Make your first commit
git commit -m "Initial commit"

# 5. Set the main branch
git branch -M main

# 6. Connect to your GitHub repository
git remote add origin https://github.com/colevhoover/coherenceweaver.git

# 7. Push your code to GitHub
git push -u origin main
```

When prompted for your GitHub username and password, enter:
- Username: colevhoover
- Password: your GitHub personal access token (<GITHUB_TOKEN>)

## Step 3: Verify Your Code is on GitHub

1. Go to https://github.com/colevhoover/coherenceweaver
2. You should see all your files and folders

That's it! Your project is now on GitHub and can be shared with others.
