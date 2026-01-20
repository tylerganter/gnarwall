# GitHub Setup for Gnarwall Devcontainer

This document explains how GitHub access is configured in the devcontainer and the security model that protects your repository.

## Quick Start

Run `gh-setup` inside the container and follow the prompts.

## Security Model

Access control is split between two complementary mechanisms:

| Layer | Controls | Set Where |
|-------|----------|-----------|
| **Fine-grained PAT** | Which repositories can be accessed | GitHub token settings |
| **Branch Protection** | Which branches can be modified and how | GitHub repo settings |

### Why This Is Secure

**Fine-grained Personal Access Tokens (PATs)** restrict access to specific repositories. The token created during setup only has access to the `tylerganter/gnarwall` repository—even if the token is compromised, it cannot access any other repositories in your account.

**Branch Protection Rules** enforce workflow requirements server-side. Even with valid repository access, no one (including AI assistants) can:
- Push directly to protected branches
- Merge pull requests without required approvals
- Bypass status checks

These protections are enforced by GitHub's servers and cannot be circumvented by any client, token, or tool.

## Setting Up Branch Protection

To protect the `main` branch:

1. Go to: `https://github.com/tylerganter/gnarwall/settings/branches`
2. Click **Add branch ruleset** or **Add rule**
3. Set **Branch name pattern**: `main`
4. Enable these protections:
   - **Require a pull request before merging** ✓
     - **Require approvals**: 1
   - **Do not allow bypassing the above settings** ✓

With this configuration, all changes to `main` must go through a pull request that you approve. The AI can create branches, push code, and open PRs, but cannot merge without your explicit approval.

## Token Permissions

The `gh-setup` script guides you through creating a fine-grained PAT with these permissions:

| Permission | Access Level | Enables |
|------------|--------------|---------|
| **Contents** | Read and write | Push/pull code, create branches |
| **Issues** | Read and write | Create, comment, close, label issues |
| **Pull requests** | Read and write | Create PRs, comment, review, request reviews |
| **Metadata** | Read-only | Required base permission for all tokens |

### Optional Permissions

Depending on your workflow, you may also want:

| Permission | Access Level | Enables |
|------------|--------------|---------|
| **Actions** | Read-only | View workflow run status and logs |
| **Workflows** | Read and write | Modify `.github/workflows/` files |

## Credential Persistence

GitHub credentials are stored in a Docker volume (`gnarwall-gh-config`) mounted at `~/.config/gh/`. This means:

- Credentials persist across container rebuilds
- You only need to run `gh-setup` once (unless the token expires)
- Deleting the volume will require re-authentication

To manually clear credentials:
```bash
# Inside container
gh auth logout

# Or from host, delete the volume
docker volume rm gnarwall-gh-config
```

## Token Expiration

Fine-grained PATs have a maximum lifetime of 1 year. When creating your token, choose an expiration that balances security and convenience (e.g., 90 days). The container will show an error when the token expires, at which point run `gh-setup` again with a new token.

## Comparison: OAuth vs Fine-Grained PAT

| Aspect | OAuth (browser flow) | Fine-Grained PAT |
|--------|---------------------|------------------|
| Repository scope | All repos you can access | Specific repos only |
| Permission granularity | Broad scopes | Per-permission control |
| Setup complexity | Simpler (browser click) | More steps (manual creation) |
| Security | Less restrictive | Least-privilege access |

This devcontainer uses fine-grained PATs for better security through least-privilege access.
