#!/bin/bash
# GitHub CLI setup helper for gnarwall devcontainer
# Configures a bot account so the human can approve AI-created PRs

echo "=== GitHub CLI Setup (Bot Account) ==="
echo ""

# Check if already authenticated
if gh auth status &>/dev/null; then
    echo "Already authenticated:"
    gh auth status
    echo ""
    read -p "Re-authenticate? (y/N): " confirm
    [[ "$confirm" != "y" && "$confirm" != "Y" ]] && exit 0
fi

echo "This configures the container to use a bot account for GitHub operations."
echo "Using a bot account allows you to approve PRs created by the AI."
echo ""
echo "Prerequisites:"
echo "  1. Create a bot GitHub account (e.g., yourname+bot@gmail.com)"
echo "  2. Add the bot as a collaborator with Write access to this repo"
echo ""
echo "Create a fine-grained PAT for the bot account:"
echo "  1. Log in as the bot account"
echo "  2. Go to: https://github.com/settings/tokens?type=beta"
echo "  3. Click 'Generate new token'"
echo "  4. Set token name (e.g., 'gnarwall-devcontainer')"
echo "  5. Set expiration (e.g., 90 days)"
echo "  6. Under 'Repository access', select 'Only select repositories'"
echo "     and choose 'tylerganter/gnarwall'"
echo "  7. Under 'Permissions' > 'Repository permissions', set:"
echo "     - Contents: Read and write (push/pull code)"
echo "     - Issues: Read and write (create/comment/close issues)"
echo "     - Pull requests: Read and write (create/review PRs)"
echo "     - Metadata: Read-only (required, usually auto-selected)"
echo "  8. Click 'Generate token' and copy it"
echo ""
read -p "Press Enter when you have the bot's token ready..."
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

    # Prompt for git identity if not configured (use bot account info)
    if [ -z "$(git config --global user.name)" ]; then
        echo ""
        echo "=== Git Identity Setup (for bot account) ==="
        read -p "Enter the bot's name for git commits: " git_name
        read -p "Enter the bot's email for git commits: " git_email
        git config --global user.name "$git_name"
        git config --global user.email "$git_email"
        echo "Git identity configured."
    fi

    echo ""
    echo "Bot account configured. PRs created by the AI can now be approved by you."
else
    echo "Authentication failed. Run 'gh-setup' to try again."
    exit 1
fi
