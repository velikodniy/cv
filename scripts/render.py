#!/usr/bin/env python3
"""Jinja2 template renderer with YAML data and markdown link conversion.

This script renders Jinja2 templates using YAML data files and provides
a custom filter for converting markdown-style links to HTML.
"""

# /// script
# dependencies = [
#     "pyyaml",
#     "jinja2",
# ]
# ///

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, Union

import yaml
from jinja2 import Environment, FileSystemLoader, TemplateError


def render_markdown_links(text: Union[str, Any]) -> Union[str, Any]:
    """Convert markdown links [text](url) to HTML links <a href="url">text</a>.

    Args:
        text: Input text that may contain markdown links

    Returns:
        Text with markdown links converted to HTML, or original value if not a string
    """
    if not isinstance(text, str):
        return text

    link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    return re.sub(link_pattern, r'<a href="\2">\1</a>', text)


def load_yaml_data(yaml_path: Path) -> Dict[str, Any]:
    """Load and parse YAML data file.

    Args:
        yaml_path: Path to YAML file

    Returns:
        Parsed YAML data as dictionary

    Raises:
        FileNotFoundError: If YAML file doesn't exist
        yaml.YAMLError: If YAML file is malformed
    """
    try:
        with yaml_path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"Error: YAML file not found: {yaml_path}", file=sys.stderr)
        raise
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML file {yaml_path}: {e}", file=sys.stderr)
        raise


def setup_jinja_environment(template_path: Path) -> tuple[Environment, str]:
    """Set up Jinja2 environment with custom filters.

    Args:
        template_path: Path to template file

    Returns:
        Tuple of (Jinja2 environment, template name)
    """
    template_dir = template_path.parent
    template_name = template_path.name

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=True,  # Enable auto-escaping for security
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["markdown_links"] = render_markdown_links

    return env, template_name


def render_template(
    template_path: Path, yaml_path: Path, output_path: Union[Path, str]
) -> None:
    """Render Jinja2 template with YAML data.

    Args:
        template_path: Path to Jinja2 template file
        yaml_path: Path to YAML data file
        output_path: Output file path or "-" for stdout

    Raises:
        TemplateError: If template rendering fails
    """
    # Load data and set up template environment
    data = load_yaml_data(yaml_path)
    env, template_name = setup_jinja_environment(template_path)

    try:
        template = env.get_template(template_name)
        html_content = template.render(**data)
    except TemplateError as e:
        print(f"Error: Template rendering failed: {e}", file=sys.stderr)
        raise

    # Write output
    if output_path == "-":
        print(html_content)
    else:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with output_file.open("w", encoding="utf-8") as f:
            f.write(html_content)

        print(
            f"Successfully rendered {template_path} -> {output_file}", file=sys.stderr
        )


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Render Jinja2 templates with YAML data and markdown link conversion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s template.j2 data.yaml output.html
  %(prog)s template.j2 data.yaml - | minify --html > output.html
        """.strip(),
    )
    parser.add_argument("template", type=Path, help="Input Jinja2 template file (.j2)")
    parser.add_argument("yaml_file", type=Path, help="YAML data file")
    parser.add_argument("output", help='Output file path (use "-" for stdout)')

    args = parser.parse_args()

    try:
        render_template(args.template, args.yaml_file, args.output)
    except (FileNotFoundError, yaml.YAMLError, TemplateError):
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
