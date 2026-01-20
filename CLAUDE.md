# Project Context for Claude Code

## Development Environment

- **Platform**: macOS with devcontainer CLI (npm install, not VS Code)
- **Container runtime**: Docker via devcontainer CLI
- **Working directory**: `/workspace` (inside container)

## Local Development Server

To preview the static site locally:

```bash
cd /workspace/docs && python3 -m http.server 8000
```

Then access http://localhost:8000 in your browser.

## Port Forwarding

The devcontainer is configured with `-p 8000:8000` in `runArgs`, but this only applies at container creation time. If port forwarding isn't working after a rebuild, the container must be fully recreated (not just rebuilt) for the port mapping to take effect.

## Project Overview

WordPress to static site migration for gnarwall.org. See `PLAN.md` for current status.

### Key Directories
- `/workspace/docs/` - Static site output (served by GitHub Pages)
- `/workspace/gnarwall-export/` - Original WordPress export (6.3GB, not committed)
