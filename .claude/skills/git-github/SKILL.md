---
name: git-github
description: Git and GitHub workflows for the gnarwall devcontainer. Use when working with git operations, creating branches, committing code, pushing changes, opening PRs, managing issues, or setting up GitHub authentication. Activates automatically when code changes need to be committed or pushed.
allowed-tools: Bash, Read, Grep, Glob
---

# Git & GitHub Workflow for Gnarwall

This skill provides guidance for git and GitHub operations within the gnarwall devcontainer environment.

## Core Principle: Always Work on Feature Branches

**Never work directly on `main`.** The main branch is protected and requires PRs with approval. Always ensure you're on a feature branch before making changes.

### Proactive Behavior

When on a non-main branch, be **permissive and proactive** about:
- Committing changes frequently (after completing logical units of work)
- Pushing to remote to back up work
- Creating PRs when a feature or fix is ready for review

Don't wait to be asked—if you've made meaningful changes on a feature branch, commit and push them.

## GitHub Authentication Setup

Before using GitHub features, authenticate using the `gh-setup` command:

```bash
gh-setup
```

This configures a **fine-grained Personal Access Token (PAT)** with repository-scoped access. The token is stored in a persistent Docker volume at `~/.config/gh/`.

### Token Permissions

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

1. **Fine-grained PAT**: Restricts access to specific repositories only (not all repos in the account)
2. **Branch Protection**: Server-side rules that cannot be bypassed

### Branch Protection Rules

The `main` branch should be protected with:
- Require pull request before merging
- Require at least 1 approval
- Do not allow bypassing settings

**Important**: Even with valid credentials, direct pushes to protected branches will fail. All changes must go through PRs.

## Branch Management

### Before Starting Work

Always verify you're not on main:

```bash
git branch --show-current
```

If on main, create and switch to a feature branch immediately:

```bash
git checkout -b feature/descriptive-name
```

### Branch Naming Conventions

Use prefixes to indicate the type of work:
- `feature/` - New functionality
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code restructuring
- `chore/` - Maintenance tasks

### Switching Branches

```bash
# List all branches
git branch -a

# Switch to existing branch
git checkout branch-name

# Create and switch to new branch
git checkout -b new-branch-name
```

## Committing and Pushing Code

### When to Commit

Commit proactively when on a feature branch:
- After completing a logical unit of work
- Before switching contexts or tasks
- When you have working code worth preserving
- At natural stopping points

### How to Commit

```bash
# Stage all changes
git add -A

# Commit with descriptive message
git commit -m "Add user authentication endpoint

Implements JWT-based auth with refresh tokens.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Commit Message Guidelines

- First line: Brief summary (50 chars or less)
- Blank line, then details if needed
- Focus on "why" not "what"
- Always include the co-author line

### Pushing Changes

Push frequently to back up your work:

```bash
# First push of a new branch
git push -u origin $(git branch --show-current)

# Subsequent pushes
git push
```

### Complete Workflow: Commit and Push

```bash
# Verify not on main
git branch --show-current

# If on main, create feature branch first
# git checkout -b feature/my-feature

# Stage, commit, and push
git add -A && git commit -m "Description of changes

Co-Authored-By: Claude <noreply@anthropic.com>" && git push -u origin $(git branch --show-current)
```

## Creating Pull Requests

### When to Create a PR

Create a PR proactively when:
- A feature or fix is complete and ready for review
- You want feedback on work in progress (mark as draft)
- The branch has diverged significantly from main

### Creating a PR

```bash
gh pr create --title "Add feature X" --body "## Summary
- What this PR does
- Why it's needed

## Test plan
- How to verify the changes"
```

### Draft PRs for Work in Progress

```bash
gh pr create --draft --title "WIP: Feature X" --body "Work in progress, not ready for review yet."
```

## GitHub CLI Commands

### Authentication

```bash
gh auth status
```

### PR Management

```bash
# View your PR status
gh pr status

# View specific PR
gh pr view <number>

# List open PRs
gh pr list

# Check out a PR locally
gh pr checkout <number>

# Merge a PR (if you have permission)
gh pr merge <number>
```

### Issues

```bash
# List issues
gh issue list

# Create issue
gh issue create --title "Bug: description" --body "Details"

# View issue
gh issue view <number>
```

### View PR Comments

```bash
gh api repos/tylerganter/gnarwall/pulls/<PR_NUMBER>/comments
```

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

## Best Practices

1. **Always work on feature branches** - Never commit directly to main; check your branch before any work
2. **Commit early and often** - On feature branches, commit after each logical unit of work
3. **Push frequently** - Back up your work by pushing to remote regularly
4. **Create PRs proactively** - When work is ready for review, open a PR without being asked
5. **Use descriptive branch names** - `feature/`, `fix/`, `docs/` prefixes help identify purpose
6. **Keep PRs focused** - One logical change per PR for easier review
7. **Write clear commit messages** - Focus on "why" not "what"; include co-author line

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
