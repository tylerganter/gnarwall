# GitHub Authentication Setup

Quick reference for GitHub access in the gnarwall devcontainer.

## Quick Start

```bash
gh-setup
```

The script prompts for App ID, Installation ID, and private key path.

For detailed setup instructions, see [.devcontainer/GITHUB.md](../../../.devcontainer/GITHUB.md).

## Token Refresh

GitHub App tokens expire after 1 hour. To refresh:

```bash
.devcontainer/gh-app-token.sh | gh auth login --with-token
```

## Troubleshooting

### "Permission denied" on push
- Check `gh auth status` — token may need refresh
- Verify app has Contents write permission
- If pushing to main, you must use a PR (branch protection)

### "Repository not found"
- App may not be installed on this repository
- Check installation at https://github.com/settings/installations

### Authentication errors
Run `gh-setup` again to reconfigure credentials.
