#!/bin/bash
# GitHub CLI setup helper for gnarwall devcontainer

echo "=== GitHub CLI Setup ==="
echo ""

# Check if already authenticated
if gh auth status &>/dev/null; then
    echo "Already authenticated:"
    gh auth status
    echo ""
    read -p "Re-authenticate? (y/N): " confirm
    [[ "$confirm" != "y" && "$confirm" != "Y" ]] && exit 0
fi

echo "Steps:"
echo "  1. You'll get a one-time code below"
echo "  2. Open https://github.com/login/device in your browser"
echo "  3. Enter the code to authenticate"
echo ""
echo "(Ignore the 'Failed opening a web browser' warning - expected in containers)"
echo ""
read -p "Press Enter to continue..."
echo ""

gh auth login --hostname github.com --git-protocol https --web

echo ""
if gh auth status &>/dev/null; then
    echo "GitHub CLI configured successfully!"
    echo "You can now use 'gh' commands and git push/pull."
else
    echo "Authentication failed. Run 'gh-setup' to try again."
fi
