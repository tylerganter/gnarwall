# Homepage CSS Issues Sub-plan

**Status**: Deferred until after Phase 5 Part C (all images committed)

---

## Context

Image paths have been fixed and thumbnails now load from local files instead of WordPress CDN. However, the original WordPress theme relied on CSS that may have been optimized for WordPress-served images (which included server-side cropping via query parameters like `?w=300&h=300&crop=1`). Now that we're serving static images without server-side processing, some CSS styling issues have emerged.

**Goal**: Ensure the homepage displays correctly with proper scrolling and square-cropped thumbnail images.

---

## Tasks

| # | Task | Status |
|---|------|--------|
| 1 | Investigate how Claude can visualize the locally hosted website (screenshot capability) | ⚠️ Limited |
| 2 | Fix: Scrolling jitters/stops after visible blog posts section | Pending |
| 3 | Fix: Non-square images not cropping correctly (should fill the square) | Pending |
| 4 | Verify fixes work on GitHub Pages after deployment | Pending |

---

## Task 1 Findings (Screenshot Capability)

- Container lacks browser binaries (Chromium, Firefox) and system dependencies
- Cannot install system packages without root/sudo access
- Puppeteer/Playwright installation fails due to missing deps
- **Workaround**: Can use WebFetch to get HTML description of live GitHub Pages site
- **Alternative**: User can take screenshots and share via file path, or we analyze CSS directly through code inspection
- **Future**: Could add browser to devcontainer Dockerfile if visual testing becomes routine

---

## Task 2 Analysis (Scrolling Issue)

- The theme uses `height: 100vh` and `overflow: hidden` in certain contexts
- JavaScript in `_static/` files manipulates height dynamically based on `body.single` or `body.page` classes
- Homepage has `body.home.blog` class - may need different overflow handling
- Root cause: A container was set to `overflow: hidden` blocking scroll past visible posts

---

## Task 3 Analysis (Image Cropping Issue)

- **Root cause identified**: WordPress used server-side cropping via URL params (`?w=980&h=980&crop=1`)
- After stripping query params, images are served at original aspect ratios (e.g., 3938x2482)
- HTML specifies `width="980" height="980"` but actual images are not square
- The JavaScript ratio/crop logic in `_static/` only runs for `body.page` or `body.single` pages
- Homepage (`body.home.blog`) doesn't trigger this logic

---

## Fix Attempted (Scrapped)

**File**: `docs/_static/custom-fixes.css` (deleted)

Attempted CSS fix that did not work:
- Added `object-fit: cover` to `.entry-thumbnail img` for home/blog/archive pages
- Added overflow overrides to ensure page scrolls normally on homepage
- Linked CSS in `index.html` `<head>` after the main WordPress CSS

**Result**: The CSS fixes did not resolve the issues. Further investigation needed after all images are committed.

---

## Verification

- [ ] Test locally after all images committed
- [ ] Deploy to GitHub Pages
- [ ] Verify scrolling works on live site
- [ ] Verify thumbnails display as squares on live site
