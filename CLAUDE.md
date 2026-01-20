# Project Context for Claude Code

## Development Environment

- **Platform**: macOS with devcontainer CLI (npm install, not VS Code)
- **Container runtime**: Docker via devcontainer CLI
- **Working directory**: `/workspace` (inside container)

## Local Development Server

```bash
cd /workspace/docs && python3 -m http.server 8000
```

Then visit http://localhost:8000/gnarwall/ (the symlink `docs/gnarwall -> .` enables this).

## Project Overview

WordPress to static site migration for gnarwall.org. See `PLAN.md` for current status.

### Key Directories
- `/workspace/docs/` - Static site output (served by GitHub Pages)
- `/workspace/gnarwall-export/` - Original WordPress export (6.3GB, not committed)
