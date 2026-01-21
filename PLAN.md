# Gnarwall Static Site Rebuild - Plan v3

## Goal

Replace the WordPress-exported site with a clean, maintainable static site. The WordPress export contains extensive cruft (login scripts, infinite scroll, external dependencies) that makes iterative fixes intractable. A fresh build from extracted content will be simpler and more maintainable.

---

## Current State

| Component | Count/Size | Location | Status |
|-----------|------------|----------|--------|
| Blog posts (HTML) | 56 | `docs/201*/` | Committed (WordPress cruft) |
| Static pages | 2 | `docs/about/`, `docs/index.html` | Committed (WordPress cruft) |
| CSS/fonts | 1.8MB | `docs/_static/` | Committed (minified, unreadable names) |
| Images (Beijing post) | 27 | `docs/wp-content/uploads/2018/05/` | Committed |
| Images (remaining) | ~1,967 | `docs/wp-content/uploads/` | NOT committed (564MB total) |
| Original WordPress export | 6.3GB | `/workspace/gnarwall-export/` | NOT committed (reference only) |

**Current branch**: `main`
**GitHub Pages URL**: https://tylerganter.github.io/gnarwall/
**GitHub Pages source**: `docs/` directory on `main` branch

---

## Architecture Decision

### Why Fresh Build > Iterative Cleanup

| Factor | WordPress Export | Fresh Build |
|--------|-----------------|-------------|
| HTML per page | ~1,350 lines | ~50-100 lines |
| Dead JavaScript | ~200 lines (login, infinite scroll) | 0 |
| CSS | 1.8MB minified, 16 files with URL-encoded names | ~5-10KB, 1 readable file |
| External deps | fonts.wp.com, gravatar.com, wordpress.com | Google Fonts only (or self-hosted) |
| Maintainability | Fighting WordPress forever | Full control |

### What We Keep
- **Images**: Already optimized (564MB), just need to commit
- **Content**: Extract titles, dates, body text, image references from existing HTML
- **URL structure**: Preserve `2017/07/11/post-name/` paths for any existing links

### What We Replace
- All HTML files (regenerate from clean templates)
- All CSS (write minimal responsive styles)
- All JavaScript (remove entirely, or add minimal if needed)

### What We Remove
- **Contact page**: No forms needed for a static site
- **Comments**: Not supported in static site
- **Search**: Not needed (small site, easy to browse)
- **WordPress login/admin**: Obviously not needed

---

## Phase 1: Content Extraction ✅ COMPLETE

Extract structured data from the WordPress HTML files.

### Checkpoint 1A: Extraction Script ✅
- [x] Write Python script to parse existing HTML files
- [x] Extract: title, date, body content (inner HTML of `.entry-content`), featured image
- [x] Output: JSON file with all post data
- [x] **Test**: Verify extraction captures all 56 posts correctly
- [x] **Review**: Human spot-check of extracted content

### Checkpoint 1B: Content Validation ✅
- [x] Review extracted JSON for any parsing errors
- [x] Verify image paths are captured correctly
- [x] Confirm Unicode post titles/slugs are preserved
- [x] **Commit**: Extraction script + extracted data JSON

**Results:**
- 56 posts extracted with titles, dates, content, and featured images
- 1 static page (about) - contact page removed (not needed for static site)
- All image paths cleaned and normalized
- Output: `/workspace/data/content.json` (4MB)

---

## Phase 2: Template Design

Create clean HTML/CSS templates. User provides design direction.

### Checkpoint 2A: Design Input ✅
- [x] User provides screenshots or description of desired look
- [x] Confirm layout preferences (grid vs list, sidebar vs no sidebar, etc.)
- [x] Choose typography (Google Fonts, system fonts, or self-hosted)
- [x] **Review**: Agree on design direction before coding

**Results**: See [DESIGN.md](DESIGN.md) for full design notes.
- Layout: Grid (3/2/1 columns responsive)
- Typography: System fonts
- Dual-author colors: Keep (cyan/yellow)

### Checkpoint 2B: Homepage Template ✅
- [x] Create `templates/index.html` with post grid layout
- [x] Write CSS for responsive grid (mobile-first)
- [x] Add site header, navigation, footer
- [x] **Test locally**: `python3 -m http.server` with dummy data
- [x] **Review**: Human approval of homepage look

**Results**:
- `templates/index.html` - Jinja2 template for site generator
- `docs/css/style.css` - Responsive CSS (~4KB)
- Dark theme, hamburger menu, hover effects implemented

### Checkpoint 2C: Post Template ✅
- [x] Create `templates/post.html` for individual posts
- [x] Style for readable long-form content with images
- [x] Navigation: prev/next post, back to home
- [x] **Test locally**: Verify with sample post content
- [x] **Review**: Human approval of post layout

**Results**:
- `templates/post.html` - Jinja2 template for individual posts
- Post header with centered date and title
- Content area with max-width 700px, readable typography
- Full-width images that extend beyond content column
- WordPress tiled gallery support (CSS grid)
- Dual-author colored text (Tyler=cyan, Kristina=yellow)
- Hide WordPress cruft (sharedaddy, jp-relatedposts, etc.)
- Prev/next/home navigation

### Checkpoint 2D: About Page ✅
- [x] Create about page template
- [x] **Test locally**: Verify page renders correctly
- [x] **Commit**: All templates + CSS

**Results**:
- `templates/about.html` - Jinja2 template for static pages
- Centered page title, readable content area
- Reuses post-content typography styles
- Hides WordPress cruft

---

## Phase 2 Complete ✅

All templates created:
- `templates/index.html` - Homepage grid
- `templates/post.html` - Individual posts
- `templates/about.html` - Static pages
- `docs/css/style.css` - All styles (~700 lines)

---

## Phase 3: Site Generation

Generate the new static site from templates + extracted content.

### Checkpoint 3A: Build Script ✅
- [x] Write Python script to generate HTML from templates + JSON
- [x] Generate `docs/index.html` (homepage with all post cards)
- [x] Generate `docs/YYYY/MM/DD/slug/index.html` for each post
- [x] Generate `docs/about/index.html`
- [x] **Test locally**: Full site navigation works
- [x] **Review**: Spot-check several posts

**Results:**
- `scripts/build.py` - Site generator using Jinja2 templates
- 56 posts generated in `docs/2017/` and `docs/2018/`
- Homepage with post grid at `docs/index.html`
- About page at `docs/about/index.html`

### Checkpoint 3B: Image Path Verification ✅
- [x] Verify all image `src` paths point to correct locations
- [x] Confirm images display on homepage thumbnails
- [x] Confirm images display in post bodies
- [x] **Test locally**: No broken images

**Results:**
- All images use `/gnarwall/wp-content/uploads/YYYY/MM/filename.jpeg` paths
- Images verified to exist at referenced paths (2017 and 2018 posts checked)
- Homepage thumbnails use same path format

### Checkpoint 3C: Clean Deployment ✅
- [x] Remove old WordPress files from `docs/`
- [x] Remove `docs/_static/` (old WordPress CSS)
- [x] Remove `docs/contact/` (WordPress contact page not needed)
- [x] Keep `docs/wp-content/uploads/` (optimized images)
- [x] **Test locally**: Site works with new files only
- [x] **Commit**: Cleanup changes committed
- [x] **PR**: PR #27 created for review

**Results:**
- Removed 31 WordPress CSS files from `docs/_static/` (1.8MB)
- Removed old contact page
- Added 3 previously untracked images
- Site verified working locally with new CSS only

---

## Phase 3 Complete ✅

All site generation tasks completed:
- Build script generates all pages from templates
- Image paths verified and images committed
- Old WordPress cruft removed

---

## Phase 4: Image Commit ✅ COMPLETE

Commit remaining images in manageable chunks.

### Checkpoint 4A-4M: Commit All Images ✅
- [x] Inventory images referenced in posts (1959 unique images, 553MB)
- [x] Commit 2018 images: 545 images, 156MB (PR #25)
- [x] Commit 2017 images: 1414 images, 397MB (PR #26)
- [x] Merge PRs to main

**Results:**
- All 56 posts now have their images committed
- 2 referenced images were missing from disk (excluded)
- Total: 1959 images across 2017/07 - 2018/05

---

## Phase 5: Final Verification

### Checkpoint 5A: GitHub Pages Testing
- [ ] Verify homepage loads and displays correctly
- [ ] Verify all 56 posts are accessible
- [ ] Verify about/contact pages work
- [ ] Test on mobile viewport
- [ ] Check for console errors

### Checkpoint 5B: Cleanup
- [ ] Remove `/workspace/gnarwall-export/` (6.3GB) if no longer needed
- [ ] Remove any temporary build scripts if not needed
- [ ] Update README if applicable
- [ ] **Final commit**: Any cleanup changes

---

## File Structure (Target)

```
docs/
├── index.html                          # Homepage (post grid)
├── about/index.html                    # About page
├── css/
│   └── style.css                       # Single CSS file (~5-10KB)
├── wp-content/uploads/                 # Images (preserved)
│   ├── 2017/07/                        # ~186 images
│   ├── 2017/08/                        # ~124 images
│   └── ...
└── 2017/                               # Blog posts
    └── 07/11/post-name/index.html
```

---

## Development Notes

- **Local server**: `cd /workspace/docs && python3 -m http.server 8000`
- **GitHub repo**: https://github.com/tylerganter/gnarwall
- **Current branch**: `main` (create feature branches for new work)
- **Build tools**: Python 3 + BeautifulSoup for extraction/generation (no npm/node required)

---

## Future Improvements (Nice to Have)

- **Panorama edge-to-edge**: Very wide panorama images don't quite reach the browser viewport edges. The current CSS centering technique has limitations. A future improvement could use JavaScript to detect panoramas and apply full-bleed styling.

---

## Risk Mitigation

1. **Content loss**: Keep WordPress export until Phase 5 complete
2. **URL breakage**: Preserve exact URL structure (`/2017/07/11/post-name/`)
3. **Large commits**: Split image commits by month to avoid GitHub limits
4. **Rollback**: Tag current state before major changes

---

## Next Step

**Phase 5, Checkpoint 5A**: Merge PR #27, then verify GitHub Pages deployment - test homepage, posts, and about page on live site.
