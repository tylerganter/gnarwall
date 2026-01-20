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

**Current branch**: `feature/homepage-thumbnails`
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

### Checkpoint 2A: Design Input
- [ ] User provides screenshots or description of desired look
- [ ] Confirm layout preferences (grid vs list, sidebar vs no sidebar, etc.)
- [ ] Choose typography (Google Fonts, system fonts, or self-hosted)
- [ ] **Review**: Agree on design direction before coding

### Checkpoint 2B: Homepage Template
- [ ] Create `templates/index.html` with post grid layout
- [ ] Write CSS for responsive grid (mobile-first)
- [ ] Add site header, navigation, footer
- [ ] **Test locally**: `python3 -m http.server` with dummy data
- [ ] **Review**: Human approval of homepage look

### Checkpoint 2C: Post Template
- [ ] Create `templates/post.html` for individual posts
- [ ] Style for readable long-form content with images
- [ ] Navigation: prev/next post, back to home
- [ ] **Test locally**: Verify with sample post content
- [ ] **Review**: Human approval of post layout

### Checkpoint 2D: About Page
- [ ] Create about page template
- [ ] **Test locally**: Verify page renders correctly
- [ ] **Commit**: All templates + CSS

---

## Phase 3: Site Generation

Generate the new static site from templates + extracted content.

### Checkpoint 3A: Build Script
- [ ] Write Python script to generate HTML from templates + JSON
- [ ] Generate `docs/index.html` (homepage with all post cards)
- [ ] Generate `docs/YYYY/MM/DD/slug/index.html` for each post
- [ ] Generate `docs/about/index.html`
- [ ] **Test locally**: Full site navigation works
- [ ] **Review**: Spot-check several posts

### Checkpoint 3B: Image Path Verification
- [ ] Verify all image `src` paths point to correct locations
- [ ] Confirm images display on homepage thumbnails
- [ ] Confirm images display in post bodies
- [ ] **Test locally**: No broken images

### Checkpoint 3C: Clean Deployment
- [ ] Remove old WordPress files from `docs/`
- [ ] Remove `docs/_static/` (old WordPress CSS)
- [ ] Keep `docs/wp-content/uploads/` (optimized images)
- [ ] Add new generated HTML + CSS
- [ ] **Test locally**: Site works with new files only
- [ ] **Commit**: New site files (HTML + CSS)
- [ ] **PR**: Create PR for review before merging to main

---

## Phase 4: Image Commit

Commit remaining images in manageable chunks.

### Checkpoint 4A: Image Inventory
- [ ] List all uncommitted images by directory
- [ ] Plan commit order (by date: 2017/07, 2017/08, etc.)
- [ ] Estimate sizes per commit

### Checkpoint 4B-4L: Commit Images by Month
For each month directory:
- [ ] Stage images for that month
- [ ] Commit with descriptive message
- [ ] Push to branch
- [ ] Verify push succeeds (watch for size limits)

### Checkpoint 4M: Final Image Verification
- [ ] All images committed
- [ ] **Test locally**: Every post displays images correctly
- [ ] **PR**: Create PR to merge to main
- [ ] **Deploy**: Merge to main, verify on GitHub Pages

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
- **Current branch**: `feature/homepage-thumbnails` (will continue here or create new branch)
- **Build tools**: Python 3 + BeautifulSoup for extraction/generation (no npm/node required)

---

## Risk Mitigation

1. **Content loss**: Keep WordPress export until Phase 5 complete
2. **URL breakage**: Preserve exact URL structure (`/2017/07/11/post-name/`)
3. **Large commits**: Split image commits by month to avoid GitHub limits
4. **Rollback**: Tag current state before major changes

---

## Next Step

**Phase 1, Checkpoint 1A**: Write content extraction script to parse existing WordPress HTML and extract structured post data.
