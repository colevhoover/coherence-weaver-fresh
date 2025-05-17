# GitHub Upload Guide for Coherence Weaver

This guide explains how to upload the Coherence Weaver project to GitHub using the provided scripts, specifically designed to avoid token limit issues that may occur when using AI assistants like Cline.

## Understanding the Token Limit Issue

When trying to upload large projects through AI assistants, you might encounter errors like:

```
400 {"type":"error","error":{"type":"invalid_request_error","message":"prompt is too long: 207342 tokens > 200000 maximum"}}
```

This happens because the conversation context becomes too large for the model to process. The scripts provided here solve this problem by:

1. Breaking down the upload process into smaller, manageable chunks
2. Avoiding loading the entire project into the conversation at once
3. Handling each step sequentially to minimize token usage

## Available Scripts

Three scripts have been created to facilitate the GitHub upload process:

1. **create_github_repo.sh**: Creates a new GitHub repository for your project
2. **github_upload.sh**: Uploads the code to GitHub in small, incremental commits
3. **github_quick_upload.sh**: A convenience wrapper that runs both scripts in sequence

## Prerequisites

Before starting, make sure you have:

1. A GitHub account
2. A Personal Access Token (PAT) with 'repo' permissions
   - Create one at https://github.com/settings/tokens
   - Select at least the "repo" scope when creating your token

## Step-by-Step Instructions

### Option 1: Using the Combined Script (Recommended)

For the simplest experience, use the combined script:

1. Navigate to the coherence_weaver directory:
   ```bash
   cd /path/to/coherence_weaver
   ```

2. Run the quick upload script:
   ```bash
   ./github_quick_upload.sh
   ```

3. When prompted, enter your GitHub Personal Access Token.

4. The script will automatically:
   - Clean sensitive data from the repository
   - Create a new repository on GitHub
   - Upload your code in manageable chunks
   - Provide a link to your new repository when complete

### Option 2: Running Scripts Individually

If you prefer more control over the process, you can run the scripts individually:

1. First, clean sensitive data:
   ```bash
   ./thorough_clean.sh
   ```

2. Create the GitHub repository:
   ```bash
   ./create_github_repo.sh
   ```
   Enter your GitHub Personal Access Token when prompted.

3. Upload the code:
   ```bash
   ./github_upload.sh
   ```

## How It Works

### Token Cleaning

The `thorough_clean.sh` script scans all text files in the project for GitHub tokens and replaces them with placeholders, ensuring no sensitive data is accidentally uploaded.

### Repository Creation

The `create_github_repo.sh` script:
- Uses GitHub's API to create a new repository
- Sets up the proper repository configuration
- Prepares the environment for the upload process

### Incremental Upload

The `github_upload.sh` script:
- Initializes a Git repository locally (if needed)
- Sets up Git configuration
- Adds the remote GitHub repository
- Commits and pushes files in logical chunks:
  - Core files first
  - Configuration files
  - Source code by module
  - Examples and documentation
  - Tests
  - Scripts
  - Any remaining files

This incremental approach prevents token limit issues by breaking the upload into smaller, manageable operations.

## Troubleshooting

### Authentication Issues
- Make sure your Personal Access Token has the 'repo' scope
- Ensure the token is correctly entered without extra spaces
- Check that the token hasn't expired

### Repository Already Exists
- If the repository already exists, the script will attempt to use it
- You may need to manually delete the repository on GitHub if you want to start fresh

### Permission Errors
- Ensure the scripts are executable: `chmod +x *.sh`
- Make sure you have write permissions in the directory

## After Upload

Once the upload is complete:
1. Visit the repository URL displayed in the terminal
2. Verify that all files were uploaded correctly
3. Add additional information such as:
   - More detailed README
   - Contributing guidelines
   - Issue templates

## Need Help?

If you encounter any issues not covered in this guide, please create an issue in the GitHub repository or contact the repository maintainer.
