#!/usr/bin/env python3
"""Content directive handlers for inline transformations.

Directives use ::name:args syntax in markdown content.
This is distinct from @@key: value metadata at the top of files.
"""

import re


def image(args: str, post_name: str) -> str:
    """Single image or comma-separated row.

    Usage:
        ::image:photo.avif
        ::image:left.avif,right.avif
    """
    files = args.split(",")
    if len(files) == 1:
        return f"![](../assets/{post_name}/{files[0]})"
    imgs = "".join(f'<img src="../assets/{post_name}/{f}" />' for f in files)
    return f'<div class="img-row">{imgs}</div>'


def image_sq(args: str, post_name: str) -> str:
    """Square-cropped image.

    Usage:
        ::image-sq:photo.avif
    """
    return f'<div class="img-square"><img src="../assets/{post_name}/{args}" /></div>'


# Registry: directive name -> handler function
# Each handler takes (args: str, post_name: str) -> str
DIRECTIVES = {
    "image": image,
    "image-sq": image_sq,
}


def process_directives(content: str, post_name: str) -> str:
    """Process all ::directive:args patterns in content."""

    def replace(match):
        name, args = match.group(1), match.group(2)
        handler = DIRECTIVES.get(name)
        if handler:
            return handler(args, post_name)
        return match.group(0)  # Leave unknown directives unchanged

    return re.sub(r"::([a-z-]+):(\S+)", replace, content)
