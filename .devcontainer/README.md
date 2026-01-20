# Dev Container

A sandboxed environment for AI-assisted development with Claude Code.

## Prerequisites

- Docker Desktop running
- VS Code with Dev Containers extension, or `devcontainer` CLI

## Getting Started

### Option 1: VS Code

1. Open this repo in VS Code
2. Press `Cmd+Shift+P` and select "Dev Containers: Reopen in Container"
3. Wait for the container to build

### Option 2: CLI

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

## GitHub Setup

Run `gh-setup` to configure GitHub authentication. This is required for pushing code and creating PRs.

See [GITHUB.md](./GITHUB.md) for details on the authentication setup and security model.

## Notes

- The container includes network restrictions via iptables (see `init-firewall.sh`)
- Your `ANTHROPIC_API_KEY` environment variable needs to be available to the container
- Working directory inside the container is `/workspace`
