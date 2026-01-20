# Customizations from Reference Devcontainer

This document tracks changes made to the official Claude Code devcontainer reference (stored in `claude-code/` for comparison).

## devcontainer.json

| Change | Reference | Custom | Reason |
|--------|-----------|--------|--------|
| Mounts | 2 volumes | 3 volumes | Added `gnarwall-gh-config` volume |

**Added mount:**
```json
"source=gnarwall-gh-config,target=/home/node/.config/gh,type=volume"
```

Persists GitHub CLI authentication across container rebuilds.

## Dockerfile

| Change | Reference | Custom | Reason |
|--------|-----------|--------|--------|
| SHELL | `/bin/zsh` | `/bin/bash` | User preference |
| Packages | Standard | Added `tree` | Directory visualization |
| .bashrc | None | Custom config | Colors, aliases, helpers |
| gh-setup | Not present | Installed | GitHub App auth support |

**Custom .bashrc additions:**
- PS1 with colors (cyan user, magenta host, yellow dir)
- Aliases: `ll`, `la`, `grep --color`, `tree -F`
- Helper functions: `fc` (file count), `duall` (disk usage), `pprint` (JSON pretty print)
- GitHub auth status check on shell startup

**GitHub App setup:**
- Installs `gh-setup.sh` as `/usr/local/bin/gh-setup`

## init-firewall.sh

| Change | Reference | Custom | Reason |
|--------|-----------|--------|--------|
| gh config ownership | Not present | Added chown | Fix volume permissions |

**Added at script start:**
```bash
# Fix ownership of gh config directory (Docker volume mounts as root)
chown -R node:node /home/node/.config/gh
```

Docker creates volume mounts with root ownership. This fixes permissions so the `gh` CLI can write its configuration.

## Additional Files

Files added that don't exist in the reference:

| File | Purpose |
|------|---------|
| `.gh-app/` | GitHub App credentials (gitignored) |
| `.gitignore` | Ignores `.gh-app/` directory |
| `gh-app-token.sh` | Generates GitHub App installation tokens |
| `gh-setup.sh` | Interactive GitHub App setup wizard |
| `GITHUB.md` | GitHub App setup documentation |
| `README.md` | General devcontainer documentation |
| `CUSTOMIZATIONS.md` | This file |

## Summary

The primary customization theme is **GitHub App authentication**, which enables:
- AI-created PRs that humans can approve (separate identity)
- Persistent GitHub CLI auth across container rebuilds
- Automated token generation and refresh

Secondary customizations are personal shell preferences (bash, colors, aliases).
