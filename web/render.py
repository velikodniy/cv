#!/usr/bin/env python3
# /// script
# dependencies = [
#     "pyyaml",
#     "jinja2",
# ]
# ///

import yaml
import re
import argparse
import os
from jinja2 import Environment, FileSystemLoader

def render_markdown_links(text):
    """Convert markdown links [text](url) to HTML links <a href="url">text</a>"""
    if not isinstance(text, str):
        return text

    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.sub(link_pattern, r'<a href="\2">\1</a>', text)

def main():
    parser = argparse.ArgumentParser(description='Render Jinja2 templates with YAML data and markdown link conversion')
    parser.add_argument('template', help='Input Jinja2 template file (.j2)')
    parser.add_argument('yaml_file', help='YAML data file')
    parser.add_argument('output', help='Output file')

    args = parser.parse_args()

    # Load YAML data
    with open(args.yaml_file, 'r') as f:
        data = yaml.safe_load(f)

    # Set up Jinja2 environment with custom filter
    template_dir = os.path.dirname(args.template) or '.'
    template_name = os.path.basename(args.template)

    env = Environment(loader=FileSystemLoader(template_dir))
    env.filters['markdown_links'] = render_markdown_links
    template = env.get_template(template_name)

    # Render template
    html_content = template.render(**data)

    # Write output
    if args.output == '-':
        print(html_content)
    else:
        with open(args.output, 'w') as f:
            f.write(html_content)
        print(f"Successfully rendered {args.template} -> {args.output}")

if __name__ == '__main__':
    main()
