---
name: git-github
description: Git and GitHub workflows for the gnarwall devcontainer. Use when working with git operations, creating branches, committing code, pushing changes, opening PRs, or managing issues. Activates automatically when code changes need to be committed or pushed.
allowed-tools: Bash, Read, Grep, Glob
---

# Git & GitHub Workflow

## Prerequisites

Check authentication status before GitHub operations:

```bash
gh auth status
```

If authentication fails, see [SETUP.md](./SETUP.md) for one-time GitHub setup.

## Core Principle: Always Work on Feature Branches

**Never work directly on `main`.** The main branch is protected and requires PRs with approval. Always ensure you're on a feature branch before making changes.

### Proactive Behavior

When on a non-main branch, be **permissive and proactive** about:
- Committing changes frequently (after completing logical units of work)
- Pushing to remote to back up work
- Creating PRs when a feature or fix is ready for review

Don't wait to be asked—if you've made meaningful changes on a feature branch, commit and push them.

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

## Best Practices

1. **Always work on feature branches** - Never commit directly to main; check your branch before any work
2. **Commit early and often** - On feature branches, commit after each logical unit of work
3. **Push frequently** - Back up your work by pushing to remote regularly
4. **Create PRs proactively** - When work is ready for review, open a PR without being asked
5. **Use descriptive branch names** - `feature/`, `fix/`, `docs/` prefixes help identify purpose
6. **Keep PRs focused** - One logical change per PR for easier review
7. **Write clear commit messages** - Focus on "why" not "what"; include co-author line
