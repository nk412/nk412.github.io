#!/usr/bin/env python3
"""Content directive handlers for inline transformations.

Directives use ::name:args syntax in markdown content.
This is distinct from @@key: value metadata at the top of files.
"""

import re


def image(args: str, post_name: str, caption: str = None) -> str:
    """Single image or comma-separated row.

    Usage:
        ::image:photo.avif
        ::image:photo.avif(Optional caption)
        ::image:left.avif,right.avif
    """
    files = args.split(",")
    if len(files) == 1:
        img = f'<img src="../assets/{post_name}/{files[0]}" />'
        if caption:
            return f"<figure>{img}<figcaption>{caption}</figcaption></figure>"
        return f"![](../assets/{post_name}/{files[0]})"
    imgs = "".join(f'<img src="../assets/{post_name}/{f}" />' for f in files)
    row = f'<div class="img-row">{imgs}</div>'
    if caption:
        return f"<figure>{row}<figcaption>{caption}</figcaption></figure>"
    return row


def image_sq(args: str, post_name: str, caption: str = None) -> str:
    """Square-cropped image.

    Usage:
        ::image-sq:photo.avif
    """
    img = f'<img src="../assets/{post_name}/{args}" />'
    if caption:
        return f'<figure class="img-square">{img}<figcaption>{caption}</figcaption></figure>'
    return f'<div class="img-square">{img}</div>'


# Registry: directive name -> handler function
# Each handler takes (args: str, post_name: str, caption: str | None) -> str
DIRECTIVES = {
    "image": image,
    "image-sq": image_sq,
}


def process_directives(content: str, post_name: str) -> str:
    """Process all ::directive:args patterns in content.

    Supports optional caption in parentheses: ::image:file.avif(caption text)
    """

    def replace(match):
        name, args, caption = match.group(1), match.group(2), match.group(3)
        handler = DIRECTIVES.get(name)
        if handler:
            return handler(args, post_name, caption)
        return match.group(0)  # Leave unknown directives unchanged

    return re.sub(r"::([a-z-]+):([^\s(]+)(?:\(([^)]+)\))?", replace, content)
