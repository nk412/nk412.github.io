#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown"]
# ///
"""Build static site from markdown posts."""

import re
import sys
from pathlib import Path

# Add tools directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from md2html import parse_metadata, convert_markdown_to_html, HTML_TEMPLATE

ROOT = Path(__file__).parent.parent
SRC_POSTS = ROOT / "src" / "posts"
OUT_POSTS = ROOT / "posts"
SRC_INDEX = ROOT / "src" / "index.html"
OUT_INDEX = ROOT / "index.html"

REQUIRED_FIELDS = ["title", "date"]


def build_post(md_path: Path) -> dict | None:
    """Build a single post, return metadata for index. Returns None for drafts."""
    md_content = md_path.read_text(encoding="utf-8")
    metadata, content = parse_metadata(md_content)

    # Replace @@image:filename with markdown image syntax
    post_name = md_path.stem
    content = re.sub(r"@@image:(\S+)", rf"![](../assets/{post_name}/\1)", content)

    # Skip drafts entirely
    if metadata.get("draft", "false").lower() == "true":
        print(f"  {md_path.name} (draft, skipped)")
        return None

    # Validate required fields
    missing = [f for f in REQUIRED_FIELDS if not metadata.get(f)]
    if missing:
        print(f"Error: {md_path.name} missing required fields: {', '.join(missing)}")
        sys.exit(1)

    # Convert to HTML
    html_content = convert_markdown_to_html(content)

    # Add lazy loading for photo posts
    if metadata.get("photos", "false").lower() == "true":
        html_content = html_content.replace("<img ", '<img loading="lazy" ')

    full_html = HTML_TEMPLATE.format(title=metadata["title"], content=html_content)

    # Write output
    out_path = OUT_POSTS / md_path.with_suffix(".html").name
    out_path.write_text(full_html, encoding="utf-8")
    print(f"  {md_path.name} -> {out_path.name}")

    return {
        "title": metadata["title"],
        "date": metadata["date"],
        "filename": out_path.name,
        "type": metadata.get("type"),
        "list": metadata.get("list", "true").lower() != "false",
    }


def format_date(date_str: str) -> str:
    """Convert YYYYMMDD to DD/MM/YYYY."""
    # Assume date is in YYYYMMDD format
    return f"{date_str[6:8]}/{date_str[4:6]}/{date_str[:4]}"


def generate_post_list(posts: list[dict]) -> str:
    """Generate HTML for post list, sorted by date descending."""
    sorted_posts = sorted(posts, key=lambda p: p["date"], reverse=True)
    lines = []
    for post in sorted_posts:
        date_formatted = format_date(post["date"])
        type_suffix = f' <span style="color: #999;">({post["type"]})</span>' if post["type"] else ""
        lines.append(
            f'        <small style="font-family: monospace; color: #999;">{date_formatted}</small> '
            f'/ <a href="posts/{post["filename"]}">{post["title"]}</a>{type_suffix}<br>'
        )
    return "\n".join(lines)


def build_index(posts: list[dict]) -> None:
    """Build index.html from template."""
    template = SRC_INDEX.read_text(encoding="utf-8")
    post_list = generate_post_list(posts)
    html = template.replace("<!-- POSTS -->", post_list + "\n")
    OUT_INDEX.write_text(html, encoding="utf-8")
    print(f"  index.html updated with {len(posts)} post(s)")


def main():
    print("Building posts...")
    OUT_POSTS.mkdir(exist_ok=True)

    md_files = list(SRC_POSTS.glob("*.md"))
    if not md_files:
        print("No markdown files found in src/posts/")
        sys.exit(1)

    posts = []
    for md_path in md_files:
        post = build_post(md_path)
        if post:
            posts.append(post)

    print("\nBuilding index...")
    listed_posts = []
    for p in posts:
        if p["list"]:
            listed_posts.append(p)
        else:
            print(f"  Skipping {p['filename']} (list: false)")
    build_index(listed_posts)

    print("\nDone!")


if __name__ == "__main__":
    main()
