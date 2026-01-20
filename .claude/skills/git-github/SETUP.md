# GitHub Authentication Setup

This guide covers one-time setup for GitHub access in the gnarwall devcontainer.

## Quick Start

Authenticate using the `gh-setup` command:

```bash
gh-setup
```

This configures a **fine-grained Personal Access Token (PAT)** with repository-scoped access. The token is stored in a persistent Docker volume at `~/.config/gh/`.

## Token Permissions

The standard setup includes:

| Permission | Access | Purpose |
|------------|--------|---------|
| Contents | Read/Write | Push/pull code, create branches |
| Issues | Read/Write | Create, comment, close issues |
| Pull requests | Read/Write | Create PRs, comment, review |
| Metadata | Read-only | Required base permission |

Optional: Add **Actions** (read-only) for workflow status or **Workflows** (read/write) for modifying `.github/workflows/`.

## Security Model

### Two-Layer Protection

Access control is split between two complementary mechanisms:

1. **Fine-grained PAT**: Restricts access to specific repositories only (not all repos in the account)
2. **Branch Protection**: Server-side rules that cannot be bypassed

### Branch Protection Rules

The `main` branch should be protected with:
- Require pull request before merging
- Require at least 1 approval
- Do not allow bypassing settings

**Important**: Even with valid credentials, direct pushes to protected branches will fail. All changes must go through PRs.

## Credential Management

### Token Persistence

Credentials persist across container rebuilds via Docker volume. Re-run `gh-setup` only when:
- Token expires (max 1 year, recommend 90 days)
- Permissions need updating

### Clear Credentials

```bash
# Inside container
gh auth logout

# Or from host, delete the volume
docker volume rm gnarwall-gh-config
```

## Troubleshooting

### "Permission denied" on push
- Check `gh auth status` - token may be expired
- Verify token has Contents write permission
- If pushing to main, you must use a PR (branch protection)

### "Repository not found"
- Fine-grained PAT may not include this repository
- Create a new token with the correct repository scope

### Token expired
Run `gh-setup` again and create a new fine-grained PAT.
