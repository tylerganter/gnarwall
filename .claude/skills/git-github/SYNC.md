# Starting Work & Syncing with Main

Run this check when beginning work, especially after a PR may have been merged.

## Check Current Status

```bash
git fetch --prune
git branch -vv | head -5
```

## If Your Branch Was Merged and Deleted

The output shows `[origin/branch: gone]` for branches deleted on remote:

```
* feature/old-task  abc1234 [origin/feature/old-task: gone] Last commit msg
  main              def5678 [origin/main] Some commit
```

**Recovery steps:**

```bash
# Switch to main and pull latest (includes your merged changes)
git checkout main
git pull

# Delete the stale local branch
git branch -d feature/old-task

# Create a new branch for the next task
git checkout -b feature/next-task
```

## If You're on Main

```bash
git pull
git checkout -b feature/descriptive-name
```

## If Your Branch Still Exists

The PR is still open or in review. Continue working on the existing branch.

## Branch Naming Conventions

Use prefixes to indicate the type of work:

| Prefix | Purpose |
|--------|---------|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `docs/` | Documentation updates |
| `refactor/` | Code restructuring |
| `chore/` | Maintenance tasks |
