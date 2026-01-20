# Design Notes - Adventures of Gallivanter Ganter

Based on screenshots of the current WordPress site.

---

## Confirmed Decisions

| Decision | Choice | Notes |
|----------|--------|-------|
| Homepage layout | Grid (3/2/1 columns) | Responsive square image cards |
| Typography | System fonts | Fast loading, no external requests |
| Dual-author posts | Keep colors | Cyan for Tyler, yellow for Kristina |
| Sidebar | None | Full-width content |

---

## Site Identity

- **Title**: "ADVENTURES OF GALLIVANTER GANTER"
- **Style**: All caps, sans-serif, letter-spaced
- **Domain**: gnarwall.org

---

## Color Palette

| Element | Color | Notes |
|---------|-------|-------|
| Background | Dark gray/black | ~#1a1a1a or #222 |
| Primary text | White | #fff |
| Accent/links | Teal/Cyan | ~#00bcd4 or similar |
| Secondary accent | Yellow | ~#ffeb3b (used for dual-author posts) |
| Date text | Light gray | Slightly muted white |

---

## Typography

**Using system font stack** (no external fonts):

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```

- **Site title**: Sans-serif, uppercase, generous letter-spacing
- **Post titles**: Support Unicode scripts (Chinese 北京市, Korean 서울특별시, Hindi काठमाडौं, Arabic سینا, etc.)
- **Body text**: Readable size, good line-height (~1.6-1.8)
- **Post dates**: Smaller, formatted as "May 17, 2018"

---

## Homepage Layout

### Desktop (3 columns)
- Grid of square post thumbnails
- Each card shows:
  - Featured image (fills entire card, cropped square)
  - Date overlay at bottom (small text)
  - Title overlay at bottom (larger text, below date)
- Cards appear to have slight hover effect (teal tint visible in some screenshots)

### Tablet (2 columns)
- Same card style, responsive 2-column grid

### Mobile (1 column)
- Single column, full-width cards
- Cards stack vertically

### Header
- Site title on left
- Hamburger menu icon on right (three horizontal lines)

---

## Navigation Menu

Opens as full-screen overlay with dark background.

### Menu Items
- **Home** - Keep
- **About** - Keep
- **Contact** - EXCLUDE (not needed for static site)
- **Professional Website** - Keep (external link)

### Other Menu Elements
- Search bar - EXCLUDE (not needed, small site)
- Close button (X) in top right

---

## Post Page Layout

### Header Area
- Date centered at top (e.g., "May 17, 2018")
- Post title centered below date (supports Unicode)

### Content Area
- Centered column with max-width for readability
- White text on dark background
- Generous paragraph spacing

### Images in Posts
- Full-width single images
- Image grids (2-up, 3x3 arrangements)
- Clickable for lightbox view

### Dual-Author Posts
- Special feature: Some posts have two authors (Tyler + Kristina)
- Text is color-coded by author:
  - Tyler's text: Cyan/teal
  - Kristina's text: Yellow
- Intro text explains the color coding

---

## About Page

- "ABOUT" heading centered
- Two paragraphs of body text
- Simple, clean layout
- Same dark background as rest of site

---

## Image Lightbox/Gallery

When clicking an image in a post:
- Full-screen overlay
- Image centered
- Previous/Next arrows on sides (< >)
- Close button (X) in top right
- Dot indicators at bottom (for multi-image galleries)

**Decision**: May implement simple lightbox or just link to full-size images.

---

## Features to EXCLUDE (WordPress Cruft)

These appear in screenshots but should NOT be implemented:

| Feature | Reason |
|---------|--------|
| Subscribe button | Requires backend/email service |
| Like button | WordPress.com social feature |
| Comment section | Requires backend |
| Reblog button | WordPress.com social feature |
| Search | Not needed for small site |
| Contact page/form | Requires backend |
| Infinite scroll | Replace with static page |
| Login/admin | Obviously not needed |

---

## Responsive Breakpoints (Suggested)

| Breakpoint | Columns | Notes |
|------------|---------|-------|
| Desktop (>1024px) | 3 | Full grid |
| Tablet (768-1024px) | 2 | Medium screens |
| Mobile (<768px) | 1 | Single column stack |

---

## Implementation Notes

### Must Support
- Unicode post titles (Chinese, Korean, Hindi, Arabic, etc.)
- Responsive images
- Dark theme throughout
- Clean, minimal aesthetic

### Nice to Have
- Simple image lightbox (could use vanilla JS, ~20 lines)
- Smooth hover effects on homepage cards
- Dual-author color coding (only affects a few posts)

### Keep Simple
- No JavaScript frameworks needed
- Single CSS file
- Static HTML generation from templates

---

## File References

Screenshots analyzed:
1. Homepage grid (desktop, tablet, mobile views)
2. Menu overlay
3. About page
4. Post page - Beijing (北京市)
5. Post page with image grids
6. Image lightbox view
7. Dual-author post (سینا/Sinai) with color-coded text
8. Post footer with WordPress buttons (to exclude)

---

## Next Steps

1. Confirm design direction with user
2. Choose typography (Google Fonts or system fonts)
3. Create homepage template with responsive grid
4. Create post template with content styling
5. Create about page template
