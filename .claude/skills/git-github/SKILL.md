---
name: git-github
description: Git and GitHub workflows for the gnarwall devcontainer. Use when working with git operations, creating branches, committing code, pushing changes, opening PRs, or managing issues. Activates automatically when code changes need to be committed or pushed.
allowed-tools: Bash, Read, Grep, Glob
---

# Git & GitHub Workflow

## Prerequisites

```bash
gh auth status
```

If authentication fails, see [SETUP.md](./SETUP.md) for one-time setup.

## Token Refresh

GitHub App tokens expire after **1 hour**. If you see authentication errors during a session, refresh the token:

```bash
.devcontainer/gh-app-token.sh | gh auth login --with-token
```

This regenerates the token using the stored app credentials. Run `gh-setup` only for initial setup or to reconfigure credentials.

## Core Principle

**Never work directly on `main`.** Always use feature branches. Main is protected and requires PRs with approval.

## The Workflow Loop

```
┌─────────────────────────────────────────────────────────────┐
│  1. Sync with main          →  SYNC.md                      │
│  2. Create feature branch   →  SYNC.md                      │
│  3. Work, commit, push      →  COMMIT.md                    │
│  4. Create PR               →  COMMIT.md                    │
│  5. User merges on GitHub   (branch auto-deleted)           │
│  6. Return to step 1                                        │
└─────────────────────────────────────────────────────────────┘
```

## What Are You Doing?

| Task | Guide |
|------|-------|
| Starting new work or returning after PR merged | [SYNC.md](./SYNC.md) |
| Made changes, need to commit/push | [COMMIT.md](./COMMIT.md) |
| Ready to create a PR or address review feedback | [COMMIT.md](./COMMIT.md) |
| Authentication or setup issues | [SETUP.md](./SETUP.md) |

## Proactive Behavior

When on a feature branch, be **permissive and proactive** about:
- Committing frequently (after logical units of work)
- Pushing to remote to back up work
- Creating PRs when ready for review

Don't wait to be asked—if you've made meaningful changes, commit and push them.
