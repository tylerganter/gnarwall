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

## GitHub App Setup (One-Time)

A GitHub App is used so you can approve PRs created by the AI. The app has its own identity, so PRs it creates can be approved by you (GitHub doesn't allow approving your own PRs).

1. Create a GitHub App at https://github.com/settings/apps/new with these permissions:
   - **Contents**: Read and write
   - **Pull requests**: Read and write
   - **Issues**: Read and write
   - **Metadata**: Read-only (automatically included)
2. Generate and download a private key (.pem file)
3. Install the app on this repository
4. Run `gh-setup` inside the container—it will configure authentication using your app credentials

## GitHub Setup

Run `gh-setup` inside the container. It will prompt for your App ID, Installation ID, and private key path.

### Security Model

Access control is split between two complementary mechanisms:

| Layer | Controls | Set Where |
|-------|----------|-----------|
| **GitHub App** | Which repositories and permissions | App installation settings |
| **Branch Protection** | Which branches can be modified and how | GitHub repo settings |

**GitHub App Installation** restricts access to only the repositories where the app is installed. The app is configured with specific permissions (Contents, PRs, Issues) and cannot access other repositories or perform admin actions.

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

### App Permissions

The GitHub App needs these permissions:

| Permission | Access Level | Enables |
|------------|--------------|---------|
| **Contents** | Read and write | Push/pull code, create branches |
| **Issues** | Read and write | Create, comment, close, label issues |
| **Pull requests** | Read and write | Create PRs, comment, review, request reviews |
| **Metadata** | Read-only | Required base permission (automatic) |

Permissions we explicitly **omit** for security:
- **Administration** — cannot change repo settings or rulesets
- **Actions/Workflows** — cannot modify CI/CD pipelines

### Credential Persistence

GitHub App credentials are stored in `.devcontainer/.gh-app/` (gitignored). This includes:
- `private-key.pem` — the app's private key
- `app-id` and `installation-id` — app identifiers

GitHub CLI session data is stored in the Docker volume `gnarwall-gh-config` at `~/.config/gh/`.

To manually clear credentials:
```bash
# Inside container
gh auth logout

# Or from host, delete the volume
docker volume rm gnarwall-gh-config
```

### Token Refresh

GitHub App tokens expire after 1 hour but are automatically refreshed. If you see authentication errors, run:
```bash
gh-setup
```

## Notes

- The container includes network restrictions via iptables (see `init-firewall.sh`)
- Your `ANTHROPIC_API_KEY` environment variable needs to be available to the container
- Working directory inside the container is `/workspace`
