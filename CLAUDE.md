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

Static travel blog (migrated from WordPress). See `README.md` for build instructions.

### Key Directories
- `/workspace/docs/` - Static site output (served by GitHub Pages)
- `/workspace/data/` - Extracted content JSON
- `/workspace/templates/` - Jinja2 HTML templates
- `/workspace/scripts/` - Build scripts (build.py, extract_content.py)
- `/workspace/gnarwall-export/` - Original WordPress export (6.3GB, not committed)
