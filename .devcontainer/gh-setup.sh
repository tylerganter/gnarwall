#!/bin/bash
# GitHub CLI setup helper for gnarwall devcontainer
# Uses fine-grained PAT for repo-restricted access

echo "=== GitHub CLI Setup (Fine-Grained PAT) ==="
echo ""

# Check if already authenticated
if gh auth status &>/dev/null; then
    echo "Already authenticated:"
    gh auth status
    echo ""
    read -p "Re-authenticate? (y/N): " confirm
    [[ "$confirm" != "y" && "$confirm" != "Y" ]] && exit 0
fi

echo "This will set up GitHub CLI with a fine-grained Personal Access Token"
echo "restricted to only the gnarwall repository."
echo ""
echo "Steps:"
echo "  1. Go to: https://github.com/settings/tokens?type=beta"
echo "  2. Click 'Generate new token'"
echo "  3. Set token name (e.g., 'gnarwall-devcontainer')"
echo "  4. Set expiration (e.g., 90 days)"
echo "  5. Under 'Repository access', select 'Only select repositories'"
echo "     and choose 'tylerganter/gnarwall'"
echo "  6. Under 'Permissions' > 'Repository permissions', set:"
echo "     - Contents: Read and write (push/pull code)"
echo "     - Issues: Read and write (create/comment/close issues)"
echo "     - Pull requests: Read and write (create/review PRs)"
echo "     - Metadata: Read-only (required, usually auto-selected)"
echo "  7. Click 'Generate token' and copy it"
echo ""
echo "See DEVCONTAINER.md for security details and branch protection setup."
echo ""
read -p "Press Enter when you have your token ready..."
echo ""

echo "Paste your token below (input is hidden):"
read -s token
echo ""

if [ -z "$token" ]; then
    echo "No token provided. Run 'gh-setup' to try again."
    exit 1
fi

echo "$token" | gh auth login --with-token

echo ""
if gh auth status &>/dev/null; then
    echo "GitHub CLI configured successfully!"
    echo ""
    echo "Note: This token only has access to the gnarwall repository."

    # Configure git to use gh for authentication
    echo "Setting up git credential helper..."
    gh auth setup-git
    echo "Git credential helper configured."

    # Convert SSH remote to HTTPS if needed
    if git rev-parse --git-dir &>/dev/null; then
        remote_url=$(git remote get-url origin 2>/dev/null || true)
        if [[ "$remote_url" == git@github.com:* ]]; then
            # Convert git@github.com:user/repo.git to https://github.com/user/repo.git
            https_url=$(echo "$remote_url" | sed 's|git@github.com:|https://github.com/|')
            git remote set-url origin "$https_url"
            echo "Converted origin remote from SSH to HTTPS."
        fi
    fi

    # Prompt for git identity if not configured
    if [ -z "$(git config --global user.name)" ]; then
        echo ""
        echo "=== Git Identity Setup ==="
        read -p "Enter your name for git commits: " git_name
        read -p "Enter your email for git commits: " git_email
        git config --global user.name "$git_name"
        git config --global user.email "$git_email"
        echo "Git identity configured."
    fi

    echo ""
    echo "You can now use 'gh' commands and git push/pull for gnarwall."
else
    echo "Authentication failed. Run 'gh-setup' to try again."
    exit 1
fi
