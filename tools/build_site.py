#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown"]
# ///
"""Build static site from markdown posts."""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

# Add tools directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from md2html import parse_metadata, convert_markdown_to_html, HTML_TEMPLATE
from directives import process_directives

ROOT = Path(__file__).parent.parent
SRC_POSTS = ROOT / "src" / "posts"
OUT_POSTS = ROOT / "posts"
SRC_INDEX = ROOT / "src" / "index.html"
OUT_INDEX = ROOT / "index.html"

REQUIRED_FIELDS = ["title", "date"]


@dataclass
class Post:
    """A parsed post with metadata and content."""
    path: Path
    metadata: dict[str, str]
    content: str  # markdown initially, HTML after transform


def is_true(metadata: dict, key: str) -> bool:
    """Check if a metadata key is truthy (present without value, or value is 'true')."""
    return metadata.get(key, "false").lower() == "true"


# --- Pipeline functions ---

def parse_post(md_path: Path) -> Post | None:
    """Read file and extract metadata. Returns None for drafts."""
    md_content = md_path.read_text(encoding="utf-8")
    metadata, content = parse_metadata(md_content)

    if is_true(metadata, "draft"):
        print(f"  {md_path.name} (draft, skipped)")
        return None

    return Post(path=md_path, metadata=metadata, content=content)


def validate_post(post: Post) -> None:
    """Validate required fields. Exits on failure."""
    missing = [f for f in REQUIRED_FIELDS if not post.metadata.get(f)]
    if missing:
        print(f"Error: {post.path.name} missing required fields: {', '.join(missing)}")
        sys.exit(1)


def transform_content(post: Post) -> Post:
    """Apply all content transformations: directives -> markdown -> lazy loading."""
    content = post.content

    # Process inline directives (::image:, ::image-sq:, etc.)
    content = process_directives(content, post.path.stem)

    # Convert markdown to HTML
    content = convert_markdown_to_html(content)

    # Lazy loading for images
    if is_true(post.metadata, "lazy"):
        content = content.replace("<img ", '<img loading="lazy" ')

    return Post(path=post.path, metadata=post.metadata, content=content)


def render_html(post: Post) -> str:
    """Apply HTML template to post."""
    container_class = " wide" if is_true(post.metadata, "wide") else ""
    return HTML_TEMPLATE.format(
        title=post.metadata["title"],
        content=post.content,
        container_class=container_class,
    )


def write_post(html: str, out_path: Path) -> None:
    """Write HTML to disk."""
    out_path.write_text(html, encoding="utf-8")


def post_to_index_entry(post: Post, filename: str) -> dict:
    """Extract index entry data from a post."""
    return {
        "title": post.metadata["title"],
        "date": post.metadata["date"],
        "filename": filename,
        "type": post.metadata.get("type"),
        "unlisted": is_true(post.metadata, "unlisted"),
    }


# --- Index generation ---

def format_date(date_str: str) -> str:
    """Convert YYYYMMDD to DD/MM/YYYY."""
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


# --- Main ---

def main(include_unlisted: bool = False):
    print("Building posts...")
    OUT_POSTS.mkdir(exist_ok=True)

    md_files = list(SRC_POSTS.glob("*.md"))
    if not md_files:
        print("No markdown files found in src/posts/")
        sys.exit(1)

    index_entries = []
    for md_path in md_files:
        # Parse
        post = parse_post(md_path)
        if not post:
            continue

        # Validate
        validate_post(post)

        # Transform
        post = transform_content(post)

        # Render
        html = render_html(post)

        # Write
        out_path = OUT_POSTS / md_path.with_suffix(".html").name
        write_post(html, out_path)
        print(f"  {md_path.name} -> {out_path.name}")

        # Collect for index
        index_entries.append(post_to_index_entry(post, out_path.name))

    print("\nBuilding index...")
    listed_posts = []
    for entry in index_entries:
        if not entry["unlisted"]:
            listed_posts.append(entry)
        elif include_unlisted:
            listed_posts.append({**entry, "type": "unlisted"})
        else:
            print(f"  Skipping {entry['filename']} (unlisted)")
    build_index(listed_posts)

    print("\nDone!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build static site")
    parser.add_argument(
        "--include-unlisted",
        action="store_true",
        help="Include posts with list: false in the index",
    )
    args = parser.parse_args()
    main(include_unlisted=args.include_unlisted)
