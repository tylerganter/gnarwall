# Gnarwall

A static travel blog migrated from WordPress.

**Live site**: https://tylerganter.github.io/gnarwall/

**Note**: This static site has not yet replaced the original WordPress site at gnarwall.org. DNS/hosting changes are still needed to make the static site accessible at the primary domain.

## Site Structure

- **56 blog posts** from 2017-2018
- **~1959 images** (553MB)
- Posts at `/YYYY/MM/DD/slug/` URLs
- Dark theme with dual-author colored text (Tyler=cyan, Kristina=yellow)

## Rebuilding the Site

The site is generated from extracted WordPress content using Python and Jinja2 templates.

### Prerequisites

- Python 3
- Jinja2 (`pip install jinja2`)
- BeautifulSoup4 (`pip install beautifulsoup4`) - only needed for content extraction

### Build Process

1. **Content extraction** (already done, output in `data/content.json`):
   ```bash
   python scripts/extract_content.py
   ```

2. **Generate static HTML**:
   ```bash
   python scripts/build.py
   ```

### Key Files

| Path | Purpose |
|------|---------|
| `data/content.json` | Extracted post content (4MB) |
| `templates/` | Jinja2 templates (index, post, about) |
| `scripts/build.py` | Site generator |
| `scripts/extract_content.py` | WordPress HTML parser |
| `docs/` | Generated static site (served by GitHub Pages) |

## Local Development

```bash
cd docs && python3 -m http.server 8000
```

Then visit http://localhost:8000/gnarwall/

## Known Limitations

- Panorama images don't quite reach full browser width due to CSS centering constraints
