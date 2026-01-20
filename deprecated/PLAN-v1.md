# Website Consolidation & Simplification Plan

## Current State
- **tylerganter.com**: Simple one-page portfolio (HTML/CSS), hosted on GitHub Pages, domain registered through WordPress
- **gnarwall.org**: WordPress.com travel blog from 2017-2018, image-heavy posts documenting Asia travels

## Three Perspectives Analysis

### (1) Modern Web Dev Expert
- **Hosting**: Free static hosting (Cloudflare Pages, Netlify, or GitHub Pages) is the standard for static sites
- **Domains**: Transfer to Cloudflare Registrar (at-cost pricing, no markup) or Porkbun (cheap, good UX)
- **Stack**: For a frozen travel blog, even plain HTML is fine. If you want templating, 11ty or Hugo are lightweight options
- **Future-proofing**: Subdomains of tylerganter.com (blog.tylerganter.com, projects.tylerganter.com) are the clean way to add future sites

### (2) Frugal Businessman
- **Current cost**: ~$48-96/year WordPress hosting + ~$25-30/year for two domains = ~$75-125/year
- **Optimized cost**: Free hosting + ~$20-22/year for domains at Cloudflare = **~$20-22/year total**
- **Savings**: $55-100/year
- **ROI**: Even with AI doing most work, this pays off in year one

### (3) Pragmatic Friend
- Keep domains separate - "gnarwall.org" is a fun standalone brand for that specific trip
- Don't over-engineer for hypothetical future needs
- The portfolio site already works - don't touch it beyond DNS changes
- With AI assistance, the migration work is minimal, so the frugal approach makes sense here

---

## Recommended Approach

### Domain Strategy
- **Keep domains separate** - gnarwall.org has character as a standalone travel memoir
- **Transfer both** from WordPress to Cloudflare Registrar (~$9-10/year each, at-cost pricing)
- **Future sites**: Use subdomains of tylerganter.com (e.g., blog.tylerganter.com for a new personal blog)

### Hosting Strategy
- **tylerganter.com**: Keep on GitHub Pages (already working, free)
- **gnarwall.org**: Move to GitHub Pages or Cloudflare Pages (free, you own the code)

### WordPress Migration Approach
Export the travel blog to static HTML while preserving the current theme/styling.

**Approach**: `wget` site mirror (confirmed: <50 posts, small site)
```bash
wget --mirror --convert-links --adjust-extension --page-requisites \
     --no-parent https://gnarwall.org
```
- Creates complete static copy preserving the WordPress Cubic theme
- Downloads all images, CSS, fonts, and JS
- Converts internal links to work as static files
- No need for a static site generator - just host the mirrored files

---

## Order of Operations

---

## IMMEDIATE EXECUTION (Steps 1-2)

### Step 1: Export WordPress to Static Site
1. Mirror the live site using `wget`:
   ```bash
   wget --mirror --convert-links --adjust-extension --page-requisites \
        --no-parent -P /tmp/claude/gnarwall-export https://gnarwall.org
   ```
2. Clean up the export (remove unnecessary WordPress artifacts)
3. Verify the static export works locally with a simple HTTP server

### Step 2: Push to GitHub & Enable GitHub Pages
1. Clone existing repo: https://github.com/tylerganter/gnarwall
2. Copy static site files into the repo
3. Push to main branch
4. Enable GitHub Pages in repo settings (Settings > Pages > Deploy from branch)
5. **Deliverable**: Site live at https://tylerganter.github.io/gnarwall

**STOP HERE** - User will verify the site works at the github.io URL before proceeding.

---

## LATER (Steps 3-4, after user verification)

### Step 3: Domain Transfer
1. Unlock domains at WordPress
2. Get transfer authorization codes
3. Initiate transfer to Cloudflare Registrar
4. Wait for transfer to complete (~5-7 days)

### Step 4: DNS Cutover & Cleanup
1. Update DNS for gnarwall.org to point to GitHub Pages
2. Add CNAME file to repo with `gnarwall.org`
3. Verify everything works at gnarwall.org
4. Cancel WordPress hosting plan

---

## Future Considerations

**If you want a new personal blog:**
- Host at blog.tylerganter.com (subdomain)
- Use a simple static site generator (11ty, Astro, or Hugo)
- Same free hosting (GitHub Pages or Cloudflare Pages)

**If you have dev projects to showcase:**
- Link from portfolio to GitHub repos
- Or create project-specific subdomains (projectname.tylerganter.com)
- Keep portfolio as the hub that links to everything

---

## Cost Summary

| Item | Current | After Migration |
|------|---------|-----------------|
| WordPress hosting | ~$48-96/year | $0 |
| tylerganter.com domain | ~$15/year | ~$10/year |
| gnarwall.org domain | ~$15/year | ~$12/year |
| **Total** | **~$78-126/year** | **~$22/year** |

---

## Verification Plan

### After Steps 1-2 (User checkpoint):
1. Visit https://tylerganter.github.io/gnarwall
2. Check homepage loads with correct styling
3. Click through 3-4 blog posts - verify images load
4. Test internal navigation links
5. Check on mobile device

### After Steps 3-4:
1. Visit https://gnarwall.org - should show the static site
2. Verify HTTPS works correctly
3. Monitor for a week before canceling WordPress
