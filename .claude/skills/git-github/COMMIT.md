# Committing, Pushing, and Pull Requests

## When to Commit

Commit proactively when on a feature branch:
- After completing a logical unit of work
- Before switching contexts or tasks
- When you have working code worth preserving
- At natural stopping points

## How to Commit

```bash
git add -A
git commit -m "Brief summary of changes

Optional longer description of why.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### Commit Message Guidelines

- First line: Brief summary (50 chars or less)
- Blank line, then details if needed
- Focus on "why" not "what"
- Always include the co-author line

## Pushing Changes

```bash
# First push of a new branch
git push -u origin $(git branch --show-current)

# Subsequent pushes
git push
```

### Quick Reference

```bash
git add -A && git commit -m "Description

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>" && git push
```

## Creating Pull Requests

Create a PR proactively when:
- A feature or fix is complete and ready for review
- You want feedback on work in progress (mark as draft)
- The branch has diverged significantly from main

```bash
gh pr create --title "Add feature X" --body "## Summary
- What this PR does
- Why it's needed

## Test plan
- How to verify the changes"
```

### Draft PRs for Work in Progress

```bash
gh pr create --draft --title "WIP: Feature X" --body "Work in progress."
```

## Addressing Review Feedback

When the user has left comments on a PR:

```bash
# Make changes, then commit and push to the same branch
git add -A && git commit -m "Address review feedback

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>" && git push
```

The PR updates automatically when you push to the branch.

## PR Management Commands

```bash
gh pr status          # View your PR status
gh pr view <number>   # View specific PR
gh pr list            # List open PRs
gh pr checkout <n>    # Check out a PR locally
```

## Issue Commands

```bash
gh issue list
gh issue create --title "Bug: description" --body "Details"
gh issue view <number>
```
