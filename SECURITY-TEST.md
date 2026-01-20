# Branch Protection Security Test

This document describes how to verify that the AI assistant running inside the devcontainer cannot modify the `main` branch without human approval.

## Prerequisites

1. Container is running and configured (see `DEVCONTAINER.md`)
2. GitHub App is authenticated via `gh-setup`
3. Branch protection ruleset is configured on the repository

## Test Procedure

Run these commands inside the container to verify each protection is working.

### 1. Direct Push to Main

```bash
git checkout main
echo "test" >> test-file.txt
git add test-file.txt
git commit -m "Test direct push"
git push origin main
```

**Expected**: Push is rejected with "Changes must be made through a pull request"

```bash
# Cleanup
git reset --hard HEAD~1
git checkout -
```

### 2. Self-Approve PR

```bash
# First create a test PR
git checkout -b test/security-check
echo "test" >> test-file.txt
git add test-file.txt
git commit -m "Test PR"
git push -u origin test/security-check
gh pr create --title "Security Test PR" --body "Testing self-approval"

# Try to self-approve
gh pr review --approve
```

**Expected**: Review is rejected with "Can not approve your own pull request"

### 3. Merge Without Approval

```bash
gh pr merge --merge
```

**Expected**: Merge is rejected with message about requiring approving reviews

### 4. Admin Merge Override

```bash
gh pr merge --admin
```

**Expected**: Merge is rejected—the token lacks admin bypass permissions

### 5. Force Push

```bash
git checkout main
git push --force origin main
```

**Expected**: Force push is rejected by branch protection rules

### 6. Modify Ruleset via API

```bash
gh api repos/{owner}/{repo}/rulesets
```

**Expected**: "Resource not accessible" or 403 error—the app lacks Administration permission

### 7. Add Collaborator

```bash
gh api repos/{owner}/{repo}/collaborators/some-user -X PUT
```

**Expected**: "Resource not accessible"—the app cannot modify repository access

### Cleanup

After testing, delete the test branch and PR:

```bash
gh pr close --delete-branch
git checkout main
git branch -D test/security-check
```

## What Makes This Secure

The security model has two layers:

| Layer | What It Controls |
|-------|------------------|
| **GitHub App Permissions** | Which API actions are allowed (no admin, no workflows) |
| **Branch Protection Ruleset** | Server-side enforcement of PR and approval requirements |

Key points:
- GitHub prevents PR authors from approving their own PRs
- Rulesets are enforced server-side and cannot be bypassed by any client
- The app lacks Administration permission, so it cannot modify rulesets or add collaborators
- Even if the app had more permissions, the ruleset has no bypass actors configured
