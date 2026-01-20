#!/usr/bin/env python3
"""
Extract content from WordPress-exported HTML files.

Parses the existing HTML structure to extract:
- Post title, date, slug, content, and featured image
- Static page content (about, contact)

Outputs JSON for use in site generation.
"""

import json
import os
import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
from datetime import datetime

# BeautifulSoup is preferred but let's check if it's available
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    print("Warning: BeautifulSoup not installed. Run: pip install beautifulsoup4")
    print("Falling back to regex parsing (less reliable)")


DOCS_DIR = Path("/workspace/docs")
OUTPUT_FILE = Path("/workspace/data/content.json")


def extract_with_bs4(html_path: Path) -> dict:
    """Extract content using BeautifulSoup."""
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Extract title
    title_elem = soup.select_one('h1.entry-title')
    title = title_elem.get_text(strip=True) if title_elem else None

    # Extract date
    date_elem = soup.select_one('time.entry-date.published')
    date_str = None
    date_iso = None
    if date_elem:
        date_iso = date_elem.get('datetime', '')
        date_str = date_elem.get_text(strip=True)

    # Extract content
    content_elem = soup.select_one('div.entry-content')
    content_html = None
    if content_elem:
        # Remove sharing buttons and related posts
        for elem in content_elem.select('#jp-post-flair, .sharedaddy, #jp-relatedposts'):
            elem.decompose()
        content_html = str(content_elem)

    return {
        'title': title,
        'date_iso': date_iso,
        'date_display': date_str,
        'content_html': content_html,
    }


def extract_with_regex(html_path: Path) -> dict:
    """Fallback extraction using regex (less reliable)."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract title
    title_match = re.search(r'<h1[^>]*class="entry-title"[^>]*>([^<]+)</h1>', html)
    title = unescape(title_match.group(1).strip()) if title_match else None

    # Extract date
    date_match = re.search(r'<time[^>]*class="entry-date published"[^>]*datetime="([^"]+)"[^>]*>([^<]+)</time>', html)
    date_iso = date_match.group(1) if date_match else None
    date_str = unescape(date_match.group(2).strip()) if date_match else None

    # Extract content (rough - between entry-content div and its closing)
    content_match = re.search(r'<div class="entry-content">(.*?)</div><!-- \.entry-content -->', html, re.DOTALL)
    content_html = content_match.group(1).strip() if content_match else None

    return {
        'title': title,
        'date_iso': date_iso,
        'date_display': date_str,
        'content_html': content_html,
    }


def extract_featured_images_from_homepage() -> dict:
    """Extract featured images from homepage, keyed by post URL."""
    homepage = DOCS_DIR / "index.html"
    if not homepage.exists():
        return {}

    featured = {}

    if HAS_BS4:
        with open(homepage, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        for article in soup.select('article.hentry'):
            # Get the post URL
            link = article.select_one('a.entry-link, h1.entry-title a')
            if not link:
                continue
            href = link.get('href', '')

            # Get the featured image
            img = article.select_one('.entry-thumbnail img')
            if img:
                src = img.get('src', '')
                # Clean up WordPress CDN URLs - extract the path
                if 'wp-content/uploads/' in src:
                    # Extract just the path part
                    match = re.search(r'/wp-content/uploads/[^\s?]+', src)
                    if match:
                        src = match.group(0)
                featured[href] = src
    else:
        # Regex fallback
        with open(homepage, 'r', encoding='utf-8') as f:
            html = f.read()

        # Find all articles with featured images
        pattern = r'<article[^>]*>.*?<div class="entry-thumbnail">\s*<img[^>]*src="([^"]+)"[^>]*>.*?<a href="([^"]+)"[^>]*class="entry-link"'
        for match in re.finditer(pattern, html, re.DOTALL):
            src, href = match.groups()
            if 'wp-content/uploads/' in src:
                path_match = re.search(r'/wp-content/uploads/[^\s?]+', src)
                if path_match:
                    src = path_match.group(0)
            featured[href] = src

    return featured


def get_slug_from_path(html_path: Path) -> str:
    """Extract URL slug from file path."""
    # Path like /workspace/docs/2017/07/11/post-name/index.html
    # Returns: 2017/07/11/post-name
    rel = html_path.relative_to(DOCS_DIR)
    parts = rel.parts[:-1]  # Remove 'index.html'
    return '/'.join(parts)


def clean_image_path(path: str) -> str:
    """Clean up image path - remove query strings and normalize."""
    # Extract the path portion before any query string
    if '?' in path:
        path = path.split('?')[0]
    # Remove HTML entities
    path = path.replace('&amp;', '&')
    if '&' in path:
        path = path.split('&')[0]
    # Handle URL-encoded characters
    path = path.replace('%3F', '?').replace('%3D', '=')
    if '?' in path:
        path = path.split('?')[0]
    # Normalize to /wp-content/uploads/...
    if 'wp-content/uploads/' in path and not path.startswith('/'):
        match = re.search(r'/wp-content/uploads/[^\s?&]+', path)
        if match:
            path = match.group(0)
    return path


def extract_images_from_content(content_html: str) -> list:
    """Extract all image paths from content HTML."""
    if not content_html:
        return []

    images = []
    # Find all image sources - both src and data-orig-file
    for pattern in [r'src="([^"]*wp-content/uploads/[^"\s]+)',
                    r'data-orig-file="([^"]*wp-content/uploads/[^"\s]+)']:
        for match in re.finditer(pattern, content_html):
            path = clean_image_path(match.group(1))
            if path and path not in images:
                images.append(path)

    return images


def clean_content_html(content_html: str) -> str:
    """Clean up content HTML for the new site."""
    if not content_html:
        return ""

    if HAS_BS4:
        soup = BeautifulSoup(content_html, 'html.parser')

        # Fix image sources - convert WordPress CDN URLs to local paths
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if 'wp-content/uploads/' in src:
                # Extract just the path
                match = re.search(r'/wp-content/uploads/[^\s?]+', src)
                if match:
                    img['src'] = match.group(0)

            # Remove srcset (we'll use simple img tags)
            if img.has_attr('srcset'):
                del img['srcset']
            if img.has_attr('sizes'):
                del img['sizes']
            # Remove data attributes
            for attr in list(img.attrs.keys()):
                if attr.startswith('data-'):
                    del img[attr]

        # Remove links that wrap images (WordPress attachment pages)
        for a in soup.find_all('a'):
            href = a.get('href', '')
            # If link goes to an attachment page, unwrap it
            if '/index.html' in href and a.find('img'):
                a.unwrap()

        # Simplify gallery structure - keep images and captions
        for gallery in soup.select('.tiled-gallery'):
            images = gallery.find_all('img')
            captions = gallery.select('.tiled-gallery-caption')

            # Create simple figure elements
            new_content = soup.new_tag('div')
            new_content['class'] = 'gallery'

            for i, img in enumerate(images):
                figure = soup.new_tag('figure')
                new_img = soup.new_tag('img')
                new_img['src'] = img.get('src', '')
                new_img['alt'] = img.get('alt', '')
                figure.append(new_img)

                # Check if there's a caption for this image
                img_caption = img.find_parent('div', class_='tiled-gallery-item')
                if img_caption:
                    caption_elem = img_caption.select_one('.tiled-gallery-caption')
                    if caption_elem and caption_elem.get_text(strip=True):
                        figcaption = soup.new_tag('figcaption')
                        figcaption.string = caption_elem.get_text(strip=True)
                        figure.append(figcaption)

                new_content.append(figure)

            gallery.replace_with(new_content)

        return str(soup)
    else:
        # Basic regex cleanup
        # Fix image src attributes
        def fix_img_src(match):
            full_tag = match.group(0)
            src_match = re.search(r'src="([^"]+)"', full_tag)
            if src_match:
                src = src_match.group(1)
                if 'wp-content/uploads/' in src:
                    path_match = re.search(r'/wp-content/uploads/[^\s?]+', src)
                    if path_match:
                        new_src = path_match.group(0)
                        full_tag = re.sub(r'src="[^"]+"', f'src="{new_src}"', full_tag)
            # Remove srcset
            full_tag = re.sub(r'\s*srcset="[^"]*"', '', full_tag)
            full_tag = re.sub(r'\s*sizes="[^"]*"', '', full_tag)
            return full_tag

        content_html = re.sub(r'<img[^>]+>', fix_img_src, content_html)
        return content_html


def process_post(html_path: Path, featured_images: dict) -> dict:
    """Process a single blog post."""
    extract_fn = extract_with_bs4 if HAS_BS4 else extract_with_regex
    data = extract_fn(html_path)

    slug = get_slug_from_path(html_path)

    # Extract images from content first
    images = extract_images_from_content(data['content_html'])

    # Look up featured image
    # The homepage uses relative paths like "2017/07/11/post-name/index.html"
    relative_url = slug + '/index.html'
    featured_image = featured_images.get(relative_url, '')

    # Fall back to first content image if no featured image from homepage
    if not featured_image and images:
        featured_image = images[0]

    # Clean up content HTML
    clean_html = clean_content_html(data['content_html'])

    return {
        'type': 'post',
        'slug': slug,
        'title': data['title'],
        'date_iso': data['date_iso'],
        'date_display': data['date_display'],
        'featured_image': featured_image,
        'images': images,
        'content_html': clean_html,
        'source_file': str(html_path.relative_to(DOCS_DIR)),
    }


def process_static_page(html_path: Path, page_type: str) -> dict:
    """Process a static page (about, contact)."""
    extract_fn = extract_with_bs4 if HAS_BS4 else extract_with_regex
    data = extract_fn(html_path)

    # Clean content
    clean_html = clean_content_html(data['content_html'])

    return {
        'type': 'page',
        'slug': page_type,
        'title': data['title'],
        'content_html': clean_html,
        'source_file': str(html_path.relative_to(DOCS_DIR)),
    }


def main():
    print("Extracting content from WordPress HTML...")
    print(f"Using: {'BeautifulSoup' if HAS_BS4 else 'regex fallback'}")

    # Create output directory
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Extract featured images from homepage
    print("\nExtracting featured images from homepage...")
    featured_images = extract_featured_images_from_homepage()
    print(f"  Found {len(featured_images)} featured images")

    # Find all blog posts
    print("\nProcessing blog posts...")
    posts = []
    post_dirs = sorted(DOCS_DIR.glob("20*/[0-9][0-9]/[0-9][0-9]/*/index.html"))

    for html_path in post_dirs:
        try:
            post = process_post(html_path, featured_images)
            posts.append(post)
            print(f"  ✓ {post['slug']}: {post['title']}")
        except Exception as e:
            print(f"  ✗ {html_path}: {e}")

    print(f"\nProcessed {len(posts)} posts")

    # Sort posts by date (newest first)
    posts.sort(key=lambda p: p['date_iso'] or '', reverse=True)

    # Process static pages
    print("\nProcessing static pages...")
    pages = []

    for page_type in ['about', 'contact']:
        html_path = DOCS_DIR / page_type / 'index.html'
        if html_path.exists():
            try:
                page = process_static_page(html_path, page_type)
                pages.append(page)
                print(f"  ✓ {page_type}: {page['title']}")
            except Exception as e:
                print(f"  ✗ {page_type}: {e}")

    # Extract site metadata from homepage
    site_title = "Adventures of Gallivanter Ganter"  # Default
    if HAS_BS4:
        homepage = DOCS_DIR / "index.html"
        if homepage.exists():
            with open(homepage, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            title_elem = soup.select_one('h1.site-title')
            if title_elem:
                site_title = title_elem.get_text(strip=True)

    # Build output
    output = {
        'site': {
            'title': site_title,
            'extracted_at': datetime.now().isoformat(),
        },
        'posts': posts,
        'pages': pages,
        'stats': {
            'total_posts': len(posts),
            'total_pages': len(pages),
            'total_featured_images': len([p for p in posts if p['featured_image']]),
        }
    }

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Extracted content saved to: {OUTPUT_FILE}")
    print(f"  Posts: {output['stats']['total_posts']}")
    print(f"  Pages: {output['stats']['total_pages']}")
    print(f"  Posts with featured images: {output['stats']['total_featured_images']}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
