#!/bin/bash
# GitHub CLI setup helper for gnarwall devcontainer
# Configures a GitHub App for authentication so the human can approve AI-created PRs

set -e

# Find the repo root to store credentials in .devcontainer/.gh-app
# This works whether the script is run directly or via symlink in /usr/local/bin
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "/workspace")"
SCRIPT_DIR="$REPO_ROOT/.devcontainer"
CREDENTIALS_DIR="$SCRIPT_DIR/.gh-app"

echo "=== GitHub CLI Setup (GitHub App) ==="
echo ""

# Check if already authenticated
if gh auth status &>/dev/null; then
    echo "Already authenticated:"
    gh auth status
    echo ""
    read -p "Re-authenticate? (y/N): " confirm
    [[ "$confirm" != "y" && "$confirm" != "Y" ]] && exit 0
fi

echo "This configures the container to use a GitHub App for authentication."
echo "Using a GitHub App allows you to approve PRs created by the AI."
echo ""

# Check if private key is pre-placed
PEM_FILE="$CREDENTIALS_DIR/private-key.pem"
if [ -f "$PEM_FILE" ]; then
    echo "Found private key at: $PEM_FILE"
    key_preplaced=true
else
    echo "You'll need:"
    echo "  1. Your GitHub App ID (from the app's settings page)"
    echo "  2. Your Installation ID (from the URL after installing the app)"
    echo "  3. Your private key file (.pem downloaded when you created the app)"
    echo ""
    echo "TIP: To skip the private key prompt, place your .pem file at:"
    echo "     .devcontainer/.gh-app/private-key.pem"
    echo "     (This directory is gitignored and won't be committed)"
    echo ""
    key_preplaced=false
fi

# Get App ID
read -p "Enter your GitHub App ID: " app_id
if [ -z "$app_id" ]; then
    echo "No App ID provided. Run 'gh-setup' to try again."
    exit 1
fi

# Get Installation ID
echo ""
echo "To find your Installation ID:"
echo "  Go to: https://github.com/settings/installations"
echo "  Click 'Configure' on your app"
echo "  The ID is in the URL: github.com/settings/installations/INSTALLATION_ID"
echo ""
read -p "Enter your Installation ID: " installation_id
if [ -z "$installation_id" ]; then
    echo "No Installation ID provided. Run 'gh-setup' to try again."
    exit 1
fi

# Get private key (skip if pre-placed)
if [ "$key_preplaced" = false ]; then
    echo ""
    read -p "Enter path to your private key (.pem file): " key_path
    key_path="${key_path/#\~/$HOME}"  # Expand ~
    if [ ! -f "$key_path" ]; then
        echo "Private key file not found: $key_path"
        exit 1
    fi

    # Create credentials directory
    mkdir -p "$CREDENTIALS_DIR"
    chmod 700 "$CREDENTIALS_DIR"

    # Copy private key to credentials directory
    cp "$key_path" "$CREDENTIALS_DIR/private-key.pem"
    chmod 600 "$CREDENTIALS_DIR/private-key.pem"
else
    # Ensure correct permissions on pre-placed key and directory
    chmod 700 "$CREDENTIALS_DIR"
    chmod 600 "$PEM_FILE"
fi

# Save App ID and Installation ID
echo "$app_id" > "$CREDENTIALS_DIR/app-id"
echo "$installation_id" > "$CREDENTIALS_DIR/installation-id"

echo ""
echo "Generating installation access token..."

# Generate token using the helper script
token=$("$SCRIPT_DIR/gh-app-token.sh")

if [ -z "$token" ]; then
    echo "Failed to generate token. Check your credentials."
    exit 1
fi

# Authenticate gh CLI with the token
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

    # Get the app's bot identity for git commits
    echo ""
    echo "=== Git Identity Setup ==="
    # GitHub Apps have a bot identity: app-name[bot]
    # The email format is: {app-id}+{app-slug}[bot]@users.noreply.github.com
    app_slug=$(gh api /app --jq '.slug' 2>/dev/null || echo "")
    if [ -n "$app_slug" ]; then
        bot_name="${app_slug}[bot]"
        bot_email="${app_id}+${app_slug}[bot]@users.noreply.github.com"
        git config --global user.name "$bot_name"
        git config --global user.email "$bot_email"
        echo "Git identity configured as: $bot_name <$bot_email>"
    else
        echo "Could not auto-detect app identity."
        read -p "Enter name for git commits: " git_name
        read -p "Enter email for git commits: " git_email
        git config --global user.name "$git_name"
        git config --global user.email "$git_email"
        echo "Git identity configured."
    fi

    echo ""
    echo "GitHub App configured! PRs created by the AI can now be approved by you."
    echo ""
    echo "Note: GitHub App tokens expire after 1 hour."
    echo "Run 'gh-app-token.sh' to refresh your token, or run 'gh-setup' again."
else
    echo "Authentication failed. Run 'gh-setup' to try again."
    exit 1
fi
