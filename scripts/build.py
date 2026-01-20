#!/usr/bin/env python3
"""
Static site generator for gnarwall.org

Generates HTML pages from Jinja2-style templates and content.json data.
Uses only Python standard library (no external dependencies).
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

# Base URL for GitHub Pages (site is at tylerganter.github.io/gnarwall/)
# Set to empty string for local development
BASE_URL = '/gnarwall'


class SimpleTemplate:
    """
    Minimal Jinja2-compatible template engine using only stdlib.
    Supports: {{ var }}, {{ obj.attr }}, {% for %}, {% if %}, {% else %}
    """

    def __init__(self, template_str):
        self.template = template_str

    def render(self, **context):
        result = self.template

        # Process {% for item in items %}...{% endfor %}
        result = self._process_for_loops(result, context)

        # Process {% if var %}...{% else %}...{% endif %}
        result = self._process_if_blocks(result, context)

        # Process {{ variable }} substitutions
        result = self._process_variables(result, context)

        return result

    def _get_value(self, expr, context):
        """Get value from context using dot notation (e.g., 'post.title')"""
        expr = expr.strip()
        parts = expr.split('.')
        value = context
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part, '')
            elif hasattr(value, part):
                value = getattr(value, part)
            else:
                return ''
        return value if value is not None else ''

    def _process_variables(self, text, context):
        """Replace {{ var }} with values from context"""
        def replace_var(match):
            expr = match.group(1).strip()
            value = self._get_value(expr, context)
            # Handle safe HTML (don't escape)
            return str(value)

        return re.sub(r'\{\{\s*(.+?)\s*\}\}', replace_var, text)

    def _process_for_loops(self, text, context):
        """Process {% for item in items %}...{% endfor %} blocks"""
        pattern = r'\{%\s*for\s+(\w+)\s+in\s+(\w+(?:\.\w+)*)\s*%\}(.*?)\{%\s*endfor\s*%\}'

        def replace_for(match):
            item_name = match.group(1)
            items_expr = match.group(2)
            body = match.group(3)

            items = self._get_value(items_expr, context)
            if not items:
                return ''

            result = []
            for item in items:
                item_context = {**context, item_name: item}
                # Recursively process nested structures
                processed = self._process_for_loops(body, item_context)
                processed = self._process_if_blocks(processed, item_context)
                processed = self._process_variables(processed, item_context)
                result.append(processed)

            return ''.join(result)

        return re.sub(pattern, replace_for, text, flags=re.DOTALL)

    def _process_if_blocks(self, text, context):
        """Process {% if var %}...{% else %}...{% endif %} blocks"""
        # Handle if/else/endif
        pattern = r'\{%\s*if\s+(.+?)\s*%\}(.*?)(?:\{%\s*else\s*%\}(.*?))?\{%\s*endif\s*%\}'

        def replace_if(match):
            condition = match.group(1).strip()
            if_body = match.group(2)
            else_body = match.group(3) or ''

            # Evaluate condition
            value = self._get_value(condition, context)

            if value:
                result = if_body
            else:
                result = else_body

            # Recursively process nested structures
            result = self._process_if_blocks(result, context)
            result = self._process_variables(result, context)
            return result

        return re.sub(pattern, replace_if, text, flags=re.DOTALL)


def load_template(template_path):
    """Load a template file and return a SimpleTemplate instance"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return SimpleTemplate(f.read())


def load_content(content_path):
    """Load the content.json file"""
    with open(content_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def ensure_dir(path):
    """Create directory if it doesn't exist"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def fix_content_paths(html, base_url):
    """Add base_url prefix to absolute paths in content HTML"""
    if not base_url:
        return html

    # Fix image src paths: src="/wp-content/... -> src="/gnarwall/wp-content/...
    html = re.sub(r'src="(/wp-content/)', f'src="{base_url}\\1', html)

    # Fix any other absolute paths that might exist
    html = re.sub(r'href="(/wp-content/)', f'href="{base_url}\\1', html)

    return html


def generate_homepage(template, posts, output_dir, year, base_url):
    """Generate the homepage with post grid"""
    html = template.render(posts=posts, year=year, base_url=base_url)
    output_path = os.path.join(output_dir, 'index.html')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated: {output_path}")


def generate_post_pages(template, posts, output_dir, year, base_url):
    """Generate individual post pages"""
    for i, post in enumerate(posts):
        # Determine prev/next posts (posts are in reverse chronological order)
        prev_post = posts[i - 1] if i > 0 else None
        next_post = posts[i + 1] if i < len(posts) - 1 else None

        # Fix paths in content HTML
        post_copy = post.copy()
        post_copy['content_html'] = fix_content_paths(post['content_html'], base_url)

        html = template.render(
            post=post_copy,
            prev_post=prev_post,
            next_post=next_post,
            year=year,
            base_url=base_url
        )

        # Output to docs/YYYY/MM/DD/slug/index.html
        output_path = os.path.join(output_dir, post['slug'], 'index.html')
        ensure_dir(output_path)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"Generated: {output_path}")


def generate_about_page(template, page, output_dir, year, base_url):
    """Generate the about page"""
    # Fix paths in content HTML
    page_copy = page.copy()
    page_copy['content_html'] = fix_content_paths(page['content_html'], base_url)

    html = template.render(page=page_copy, year=year, base_url=base_url)
    output_path = os.path.join(output_dir, 'about', 'index.html')
    ensure_dir(output_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated: {output_path}")


def main():
    # Paths
    project_root = Path(__file__).parent.parent
    templates_dir = project_root / 'templates'
    content_path = project_root / 'data' / 'content.json'
    output_dir = project_root / 'docs'

    # Current year for copyright
    year = datetime.now().year

    # Load content
    print("Loading content...")
    content = load_content(content_path)
    posts = content['posts']
    pages = content.get('pages', [])

    print(f"Found {len(posts)} posts and {len(pages)} pages")

    # Load templates
    print("Loading templates...")
    index_template = load_template(templates_dir / 'index.html')
    post_template = load_template(templates_dir / 'post.html')
    about_template = load_template(templates_dir / 'about.html')

    # Generate homepage
    print("\nGenerating homepage...")
    generate_homepage(index_template, posts, output_dir, year, BASE_URL)

    # Generate post pages
    print(f"\nGenerating {len(posts)} post pages...")
    generate_post_pages(post_template, posts, output_dir, year, BASE_URL)

    # Generate about page
    print("\nGenerating about page...")
    about_page = next((p for p in pages if p['slug'] == 'about'), None)
    if about_page:
        generate_about_page(about_template, about_page, output_dir, year, BASE_URL)
    else:
        print("Warning: No about page found in content.json")

    print("\nBuild complete!")
    print(f"Site generated in: {output_dir}")


if __name__ == '__main__':
    main()
