# Dev Container Setup

## Prerequisites
- Docker Desktop running
- VS Code with Dev Containers extension, or `devcontainer` CLI

## Option 1: VS Code

1. Open this repo in VS Code
2. Press `Cmd+Shift+P` and select "Dev Containers: Reopen in Container"
3. Wait for the container to build

## Option 2: CLI

```bash
# Build and start the container
devcontainer up --workspace-folder .

# Open a shell in the container
devcontainer exec --workspace-folder . bash
```

## Using Claude

Once inside the container:

```bash
# Normal mode (with permission prompts)
claude

# Permissive mode (no prompts)
claude-yolo
```

## Bot Account Setup (One-Time)

A separate GitHub "bot" account is used so you can approve PRs created by the AI (GitHub doesn't allow approving your own PRs).

1. Create a GitHub account with an email alias (e.g., `yourname+bot@gmail.com`)
2. Add the bot as a collaborator with **Write** access to this repo
3. Run `gh-setup` inside the container—it will walk you through creating a fine-grained PAT for the bot account

## GitHub Setup

Run `gh-setup` inside the container. It provides a step-by-step walkthrough for creating the bot's fine-grained PAT and configuring GitHub CLI.

### Security Model

Access control is split between two complementary mechanisms:

| Layer | Controls | Set Where |
|-------|----------|-----------|
| **Fine-grained PAT** | Which repositories can be accessed | GitHub token settings |
| **Branch Protection** | Which branches can be modified and how | GitHub repo settings |

**Fine-grained Personal Access Tokens (PATs)** restrict access to specific repositories. The token created during setup only has access to the `tylerganter/gnarwall` repository—even if the token is compromised, it cannot access any other repositories in your account.

**Branch Protection Rules** enforce workflow requirements server-side. Even with valid repository access, no one (including AI assistants) can:
- Push directly to protected branches
- Merge pull requests without required approvals
- Bypass status checks

These protections are enforced by GitHub's servers and cannot be circumvented by any client, token, or tool.

### Setting Up Branch Protection

To protect the `main` branch using GitHub Rulesets:

1. Go to: `https://github.com/tylerganter/gnarwall/settings/rules`
2. Click **New ruleset** → **New branch ruleset**
3. Configure the ruleset:
   - **Ruleset name**: `main` (or any descriptive name)
   - **Enforcement status**: **Active** (critical—disabled rulesets don't protect anything)
   - **Target branches**: Click **Add target** → **Include default branch**
4. Under **Rules**, enable:
   - **Require a pull request before merging** ✓
     - **Required approvals**: 1
   - **Block force pushes** ✓
5. Ensure **Bypass list** is empty (or contains only trusted admins)
6. Click **Create**

With this configuration, all changes to `main` must go through a pull request that you approve. The AI can create branches, push code, and open PRs, but cannot merge without your explicit approval.

### Token Permissions

The bot account's fine-grained PAT needs these permissions (scoped to this repo only):

| Permission | Access Level | Enables |
|------------|--------------|---------|
| **Contents** | Read and write | Push/pull code, create branches |
| **Issues** | Read and write | Create, comment, close, label issues |
| **Pull requests** | Read and write | Create PRs, comment, review, request reviews |
| **Metadata** | Read-only | Required base permission for all tokens |

Optional permissions depending on your workflow:

| Permission | Access Level | Enables |
|------------|--------------|---------|
| **Actions** | Read-only | View workflow run status and logs |
| **Workflows** | Read and write | Modify `.github/workflows/` files |

### Credential Persistence

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

### Token Expiration

Fine-grained PATs have a maximum lifetime of 1 year. When creating your token, choose an expiration that balances security and convenience (e.g., 90 days). The container will show an error when the token expires, at which point run `gh-setup` again with a new token.

## Notes

- The container includes network restrictions via iptables (see `init-firewall.sh`)
- Your `ANTHROPIC_API_KEY` environment variable needs to be available to the container
- Working directory inside the container is `/workspace`
