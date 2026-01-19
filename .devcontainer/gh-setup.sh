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
echo "     - Contents: Read and write"
echo "     - Metadata: Read-only (required)"
echo "  7. Click 'Generate token' and copy it"
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
    echo "You can now use 'gh' commands and git push/pull for gnarwall."
    echo ""
    echo "Note: This token only has access to the gnarwall repository."
else
    echo "Authentication failed. Run 'gh-setup' to try again."
    exit 1
fi
