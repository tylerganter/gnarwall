# WordPress to Static Site Migration - Plan v2

## Goal
Replace WordPress hosting with a static site on GitHub Pages, keeping the site functional while minimizing repository size.

---

## Phase 1: Lean HTML Structure ✅ COMPLETE

- [x] Clear `/workspace/docs/` directory
- [x] Copy homepage (`index.html`)
- [x] Copy static pages (`/about/`, `/contact/`)
- [x] Copy 56 blog posts (just main `index.html` per post)
- [x] Copy `_static/` directory (CSS/fonts)
- [x] Test locally with `python3 -m http.server`
- [x] Commit and push

**Result: 59 HTML files instead of 3,400+**

### Notes
- **Source**: WordPress export at `/workspace/gnarwall-export/gnarwall.org/` (6.3GB)
- **Excluded bloat**: `/feed/` directories, image attachment pages, `?w=xxx` image variants
- **`_static/` directory**: Files have ugly URL-encoded names (WordPress minified CSS). Analysis found 31 files with 18 duplicates (9 pairs). Left as-is since ugliness is hidden from visitors. Future improvement: rename to `style-1.css`, etc.

---

## Phase 2: Hosting Setup & Debugging ✅ COMPLETE

### Part A: Local Server (Devcontainer) ✅ COMPLETE
- [x] Determine how to run HTTP server accessible from outside devcontainer
- [x] Start server hosting `/workspace/docs/`
- [x] Verify you can access the site in browser
- [x] Confirm layout renders (images will be broken - expected)

### Part B: GitHub Pages Setup ✅ COMPLETE
- [x] Enable GitHub Pages on the repository (Settings → Pages)
- [x] Configure to serve from `docs/` directory on main branch
- [x] Merge PR to main branch
- [x] Verify site is accessible at GitHub Pages URL
- [x] Confirm layout renders on GitHub Pages

**Checkpoint: Site accessible both locally and via GitHub Pages (without images)** ✅

---

## Phase 3: Image Optimization ✅ COMPLETE

### Source and Destination
- **Originals preserved in**: `/workspace/gnarwall-export/` (6.3GB WordPress export)
- **Optimized images**: `/workspace/docs/wp-content/uploads/` (559MB, ready to commit)

### Optimization Strategy
Process images with size-based compression:

| Original Size | Max Dimension | JPEG Quality | Rationale |
|---------------|---------------|--------------|-----------|
| < 100KB | No resize | Copy as-is | Already small, compression would hurt quality |
| 100KB - 500KB | 1600px | 85 | Light compression |
| 500KB - 2MB | 1600px | 80 | Standard compression |
| > 2MB | 1600px | 75 | Aggressive compression for large files |

### Steps
- [x] Create destination directory structure
- [x] Write optimization script implementing size-based strategy
- [x] Run optimization on all 1,987 images
- [x] Verify output file count matches input
- [x] Compare before/after sizes (5.6GB → 559MB, 90% reduction)
- [x] Test locally - verify images exist at expected paths
- [x] Move optimized images to `docs/wp-content/uploads/`

**Result: 5.6GB → 559MB (90% reduction)**

---

## Phase 4: Single Post Test ✅ COMPLETE

Test the full workflow on one post before applying to all. Using the last post: `2018/05/17/北京市/` (Beijing).

### Part A: Fix Image Paths in Test Post ✅
- [x] Rewrite image `src` attributes in test post HTML
- [x] Test locally - verify images display in the post

### Part B: Commit and Deploy Test Post ✅
- [x] Identify which images the test post needs (26 from 2018/05 + 1 logo from 2017/09)
- [x] Commit only those images + the updated HTML
- [x] Push and create PR (#14)
- [x] Verify images display on GitHub Pages

**Checkpoint: Single post displays correctly with images on GitHub Pages** ✅

---

## Phase 5: All Posts

Apply the same fixes to all remaining posts, starting with the homepage index.

### Part A: Homepage Index (thumbnails for all posts)
- [x] Analyze index.html to understand image structure (one thumbnail per post)
- [x] Identify the image path pattern for post thumbnails
- [x] Fix image paths in index.html
- [x] Test locally - verify thumbnails display
- [x] Commit required thumbnail images + updated HTML
- [ ] Deploy and verify on GitHub Pages (PR #15 ready for merge)

### Part B: Fix Image Paths in All Post HTML
- [ ] Rewrite image `src` attributes in all 56 HTML files
- [ ] Test locally - verify images display across posts

### Part C: Commit All Images
- [ ] Commit remaining images (~559MB total)
- [ ] Push and create PR
- [ ] Verify on GitHub Pages

### Part D: CSS Fixes for Homepage
- [ ] Verify CSS fixes work on GitHub Pages (scrolling, image cropping)
- [ ] Address any remaining user feedback

See [SUBPLAN.md](SUBPLAN.md) for detailed analysis and fix documentation.

---

## Phase 6: Final Verification

- [ ] Test full site navigation (local + GitHub Pages)
- [ ] Verify all 56 posts display with images
- [ ] Confirm site is ready to replace WordPress hosting
- [ ] Update DNS or redirect from WordPress to GitHub Pages

---

## Current State

| Component | Files | Size | Status |
|-----------|-------|------|--------|
| Blog posts | 56 | ~10MB | ✅ Committed (1 with local images) |
| Static pages | 3 | ~300KB | ✅ Committed |
| CSS/fonts (_static) | 31 | ~2MB | ✅ Committed |
| Images (Beijing post) | 27 | ~5MB | ✅ Committed |
| Images (remaining) | ~1,960 | ~554MB | ✅ Optimized, NOT committed |

---

## File Structure (Target)

```
docs/
├── index.html                     # Homepage
├── about/index.html               # About page
├── contact/index.html             # Contact page
├── _static/                       # CSS, fonts (31 files)
├── wp-content/uploads/            # Optimized images
│   ├── 2017/07/                   # 186 images
│   ├── 2017/08/                   # 124 images
│   └── ...
└── 2017/                          # Blog posts
    └── 07/11/kobenhavnmalmo-with-fam/index.html
```

---

## Notes

- **Current branch**: `main`
- **GitHub Pages URL**: https://tylerganter.github.io/gnarwall/
- **Local dev server**: `cd /workspace/docs && python3 -m http.server 8000` → http://localhost:8000
- **Images on disk**: `/workspace/docs/wp-content/uploads/` (559MB optimized, NOT committed)
