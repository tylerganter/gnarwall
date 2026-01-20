# GitHub Configuration

This document explains how GitHub authentication and access control work in the dev container.

## The Problem

When an AI creates a pull request using your credentials, GitHub considers it "your" PR—and you can't approve your own PRs. We need a way for the AI to have its own identity.

## The Solution: GitHub App

A GitHub App provides:
- **Separate identity** — PRs created by the app can be approved by you
- **Granular permissions** — only the access needed, nothing more
- **Repository-scoped** — only works on repos where it's installed

## Setup

### 1. Create a GitHub App

Go to https://github.com/settings/apps/new and configure:

| Setting | Value |
|---------|-------|
| **App name** | Something like "My Dev Container" |
| **Homepage URL** | Can be your GitHub profile |
| **Webhook** | Uncheck "Active" (not needed) |

Under **Repository permissions**:
- **Contents**: Read and write
- **Pull requests**: Read and write
- **Issues**: Read and write
- **Metadata**: Read-only (automatic)

Leave all other permissions as "No access".

### 2. Generate a Private Key

After creating the app, scroll down and click **Generate a private key**. Save the `.pem` file.

### 3. Install the App

Go to **Install App** in the sidebar and install it on your repository.

### 4. Run Setup

Inside the container:
```bash
gh-setup
```

You'll need:
- **App ID** — from the app's settings page
- **Installation ID** — from the URL after clicking "Configure" on your installation
- **Private key path** — the `.pem` file you downloaded

## Security Model

Access control has two layers:

| Layer | What it controls |
|-------|------------------|
| **GitHub App** | Which repos can be accessed, what actions are allowed |
| **Branch Protection** | Which branches require PRs, approvals, etc. |

### Why Both Layers?

The GitHub App limits *what the AI can attempt*. Branch protection limits *what can actually happen*. Even if the app has write access, protected branches enforce PR requirements server-side.

### Setting Up Branch Protection

To protect the `main` branch:

1. Go to: `https://github.com/YOUR_USER/YOUR_REPO/settings/rules`
2. Click **New ruleset** → **New branch ruleset**
3. Configure:
   - **Ruleset name**: `main`
   - **Enforcement status**: **Active**
   - **Target branches**: Add target → Include default branch
4. Enable these rules:
   - **Require a pull request before merging** with 1 required approval
   - **Block force pushes**
5. Leave **Bypass list** empty
6. Click **Create**

## Permissions Reference

What the app **can** do:
- Push code to branches
- Create, update, and comment on PRs
- Create, update, and comment on issues

What the app **cannot** do:
- Change repository settings
- Modify branch protection rules
- Access other repositories
- Merge PRs (requires your approval)
- Push directly to protected branches

## Credentials

Credentials are stored in `.devcontainer/.gh-app/` (gitignored):
- `private-key.pem` — the app's private key
- `app-id` and `installation-id` — identifiers

GitHub CLI session data is in the Docker volume `gnarwall-gh-config`.

### Token Refresh

GitHub App tokens expire after 1 hour. To refresh:
```bash
.devcontainer/gh-app-token.sh | gh auth login --with-token
```

### Clear Credentials

```bash
# Inside container
gh auth logout

# Or from host, delete the volume
docker volume rm gnarwall-gh-config
```
