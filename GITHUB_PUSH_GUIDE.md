# GitHub Push Guide for Coherence Weaver

This guide will help you push your Coherence Weaver project to GitHub. I've already set up the local Git repository for you, including adding a `.gitignore` file and making an initial commit.

## 1. Create a New GitHub Repository

1. Go to [GitHub](https://github.com/) and sign in to your account
2. Click the "+" icon in the top-right corner and select "New repository"
3. Fill in the repository details:
   - Repository name: `coherence-weaver` (or a name of your choice)
   - Description: "An AI agent designed to facilitate justice-aligned collaboration between different AI systems"
   - Visibility: Public or Private (your choice)
   - **Important**: Do NOT initialize the repository with a README, .gitignore, or license since we already have these locally

4. Click "Create repository"

## 2. Connect Your Local Repository

After creating the repository, GitHub will show you commands to use. You need to run the commands for "pushing an existing repository".

Run these commands in your terminal from the `coherence_weaver` directory:

```bash
# Configure your Git username and email (if you haven't done this before)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add the remote GitHub repository
git remote add origin https://github.com/YOUR-USERNAME/coherence-weaver.git

# Push your code to GitHub
git push -u origin main
```

Replace "YOUR-USERNAME" with your actual GitHub username and "coherence-weaver" with your repository name if different.

## 3. Authentication

### Using Personal Access Token (PAT)

If you're prompted for credentials, you'll need to use a Personal Access Token:

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name like "Coherence Weaver Push"
4. Select scopes: at minimum, check "repo" for full repository access
5. Click "Generate token" and copy the token immediately
6. Use this token as your password when prompted (your username remains the same)

### Using SSH (Alternative)

Alternatively, you can set up SSH for easier authentication:

1. Generate an SSH key: `ssh-keygen -t ed25519 -C "your.email@example.com"`
2. Add the key to your SSH agent: `ssh-add ~/.ssh/id_ed25519`
3. Add the public key to your GitHub account (Settings → SSH and GPG keys)
4. Use SSH URL instead: `git remote add origin git@github.com:YOUR-USERNAME/coherence-weaver.git`

## 4. Verify the Push

After pushing, refresh your GitHub repository page. You should see all your code and files uploaded.

## 5. Future Commits

For future changes, use:

```bash
git add .
git commit -m "Your descriptive commit message"
git push
```

## Troubleshooting

- **Authentication failures**: Make sure you're using a personal access token or have set up SSH correctly
- **Push rejection**: If GitHub rejects your push, you might need to pull first: `git pull --rebase origin main`
- **Large files**: If you have files larger than GitHub's limit (100MB), consider using Git LFS or adding them to .gitignore
