#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown"]
# ///
"""Convert markdown files to HTML."""

import argparse
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Error: 'markdown' package not installed. Run: pip install markdown")
    sys.exit(1)


HTML_TEMPLATE = """\
<!DOCTYPE html>
<html>
<head>
    <meta charSet="utf-8" name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&family=Outfit:wght@600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container{container_class}">

    <p><a href="../#posts">&larr; back</a></p>

{content}

    <hr>
    <p><a href="../#posts">&larr; back to posts</a></p>

    </div>
</body>
</html>
"""


def parse_metadata(md_content: str) -> tuple[dict[str, str], str]:
    """Parse @@ metadata lines from top of file.

    Returns (metadata_dict, remaining_content).
    """
    lines = md_content.split("\n")
    metadata = {}
    content_start = 0

    for i, line in enumerate(lines):
        if line.startswith("@@"):
            # Parse @@key: value or @@key value
            match = re.match(r"^@@(\w+)[:\s]\s*(.+)$", line)
            if match:
                metadata[match.group(1).lower()] = match.group(2).strip()
            content_start = i + 1
        elif line.strip() == "":
            # Skip blank lines between metadata and content
            continue
        else:
            break

    remaining = "\n".join(lines[content_start:]).lstrip("\n")
    return metadata, remaining


def extract_title(md_content: str) -> str:
    """Extract title from first H1 heading."""
    match = re.search(r"^#\s+(.+)$", md_content, re.MULTILINE)
    return match.group(1) if match else "Untitled"


def convert_markdown_to_html(md_content: str) -> str:
    """Convert markdown content to HTML."""
    # Pre-process: convert ~~text~~ to <s>text</s> for strikethrough
    md_content = re.sub(r"~~(.+?)~~", r"<s>\1</s>", md_content)

    md = markdown.Markdown(
        extensions=[
            "tables",
            "fenced_code",
            "md_in_html",
        ],
    )
    return md.convert(md_content)


def build_page(md_content: str) -> str:
    """Build full HTML page from markdown content."""
    metadata, content = parse_metadata(md_content)
    title = metadata.get("title") or extract_title(content)
    html_content = convert_markdown_to_html(content)
    return HTML_TEMPLATE.format(title=title, content=html_content, container_class="")


def main():
    parser = argparse.ArgumentParser(description="Convert markdown to HTML")
    parser.add_argument("input", type=Path, help="Input markdown file")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output HTML file (default: stdout)",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: {args.input} not found", file=sys.stderr)
        sys.exit(1)

    md_content = args.input.read_text(encoding="utf-8")
    html_content = build_page(md_content)

    if args.output:
        args.output.write_text(html_content, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(html_content)


if __name__ == "__main__":
    main()
