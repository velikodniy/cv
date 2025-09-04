#!/usr/bin/env python3
# /// script
# dependencies = [
#     "pyyaml",
#     "jinja2",
# ]
# ///

import yaml
import re
from jinja2 import Environment, FileSystemLoader

def render_markdown_links(text):
    """Convert markdown links [text](url) to HTML links <a href="url">text</a>"""
    if not isinstance(text, str):
        return text

    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.sub(link_pattern, r'<a href="\2">\1</a>', text)

def main():
    # Load YAML data
    with open('data.yaml', 'r') as f:
        data = yaml.safe_load(f)

    # Set up Jinja2 environment with custom filter
    env = Environment(loader=FileSystemLoader('.'))
    env.filters['markdown_links'] = render_markdown_links
    template = env.get_template('index.html.j2')

    # Render template
    html_content = template.render(**data)

    # Write output
    with open('index.html', 'w') as f:
        f.write(html_content)

    print("Successfully rendered index.html.j2 -> index.html")

if __name__ == '__main__':
    main()
