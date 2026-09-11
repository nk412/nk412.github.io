#!/usr/bin/env python3
"""Content directive handlers for inline transformations.

Directives use ::name:args syntax in markdown content.
This is distinct from @@key: value metadata at the top of files.
"""

import re
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
_pil_warned = False


def orientation(post_name: str, filename: str) -> str:
    """'landscape' or 'portrait' from the image file's pixel size; '' if unknown.

    Essay pages use the class to let landscapes break out of the text column
    while portraits stay on it. Needs Pillow with AVIF support (>=11.2).
    """
    global _pil_warned
    try:
        from PIL import Image
    except ImportError:
        if not _pil_warned:
            print("Warning: Pillow not installed; images get no orientation class", file=sys.stderr)
            _pil_warned = True
        return ""
    try:
        with Image.open(ASSETS_DIR / post_name / filename) as im:
            w, h = im.size
    except (OSError, ValueError):
        return ""
    return "landscape" if w > h else "portrait"


def image(args: str, post_name: str, caption: str = None) -> str:
    """Single image or comma-separated row.

    Usage:
        ::image:photo.avif
        ::image:photo.avif(Optional caption)
        ::image:left.avif,right.avif
        ::image:left.avif,right.avif(Shared caption)
        ::image:left.avif,right.avif(Left caption|Right caption)

    A row caption is shared by all images unless it contains "|", in which
    case it is split into one caption per image, in order. An empty segment
    leaves that image uncaptioned. On mobile the row stacks into separate
    captioned figures, exactly as if each image had its own ::image: tag.

    A single <img> carries its orientation as a class ("landscape" or
    "portrait"); essay pages let landscapes break out of the text column.
    The uncaptioned form stays a markdown image (with an attr_list class) so
    consecutive images keep sharing one paragraph, as they always have.
    """
    files = args.split(",")
    if len(files) == 1:
        o = orientation(post_name, files[0])
        cls = f' class="{o}"' if o else ""
        if caption:
            img = f'<img{cls} src="../assets/{post_name}/{files[0]}" />'
            return f"<figure>{img}<figcaption>{caption}</figcaption></figure>"
        attrs = f"{{: .{o}}}" if o else ""
        return f"![](../assets/{post_name}/{files[0]}){attrs}"
    if caption and "|" in caption:
        captions = [c.strip() for c in caption.split("|")]
        if len(captions) > len(files):
            print(
                f"Warning: ::image:{args} has {len(files)} images but "
                f"{len(captions)} captions; extra captions dropped",
                file=sys.stderr,
            )
        figures = []
        for i, f in enumerate(files):
            img = f'<img src="../assets/{post_name}/{f}" />'
            cap = captions[i] if i < len(captions) else ""
            if cap:
                figures.append(f"<figure>{img}<figcaption>{cap}</figcaption></figure>")
            else:
                figures.append(f"<figure>{img}</figure>")
        return f'<div class="img-row captioned">{"".join(figures)}</div>'
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


def image_grid(args: str, post_name: str, caption: str = None) -> str:
    """2-column masonry grid for 4 images.

    Usage:
        ::image-grid:tl.avif,tr.avif,bl.avif,br.avif
    """
    files = args.split(",")
    imgs = "".join(f'<img src="../assets/{post_name}/{f}" />' for f in files)
    grid = f'<div class="img-grid">{imgs}</div>'
    if caption:
        return f"<figure>{grid}<figcaption>{caption}</figcaption></figure>"
    return grid


def bleed(args: str, post_name: str, caption: str = None) -> str:
    """Full-bleed image, edge-to-edge on essay pages (requires @@essay).

    Usage:
        ::bleed:photo.avif
        ::bleed:photo.avif(Optional caption)
    """
    img = f'<img src="../assets/{post_name}/{args}" />'
    if caption:
        return f'<figure class="bleed">{img}<figcaption>{caption}</figcaption></figure>'
    return f'<figure class="bleed">{img}</figure>'


def image_side(args: str, post_name: str, caption: str = None) -> str:
    """Image with its caption set in the side margin (stacks on mobile).

    Usage:
        ::image-side:photo.avif(Caption text)
    """
    o = orientation(post_name, args)
    cls = f' class="{o}"' if o else ""
    img = f'<img{cls} src="../assets/{post_name}/{args}" />'
    if caption:
        return f'<figure class="img-side">{img}<figcaption>{caption}</figcaption></figure>'
    return f"<figure>{img}</figure>"


def kicker(args: str, post_name: str, caption: str = None) -> str:
    """Small letterspaced label above a headline (eyebrow).

    Usage:
        ::kicker(PHOTO ESSAY · SVALBARD)
    """
    return f'<p class="kicker">{caption or args or ""}</p>'


def dek(args: str, post_name: str, caption: str = None) -> str:
    """Standfirst: the large italic intro paragraph under the title.

    Usage:
        ::dek(One or two scene-setting sentences.)
    """
    return f'<p class="dek">{caption or args or ""}</p>'


def pullquote(args: str, post_name: str, caption: str = None) -> str:
    """Large display-font quote lifted from the essay.

    Usage:
        ::pullquote(A striking line from the text.)
    """
    return f'<aside class="pullquote">{caption or args or ""}</aside>'


def dropcap(args: str, post_name: str, caption: str = None) -> str:
    """Paragraph whose first letter is set as a large drop cap.

    Usage:
        ::dropcap(Opening paragraph text...)
    """
    return f'<p class="dropcap">{caption or args or ""}</p>'


# Registry: directive name -> handler function
# Each handler takes (args: str, post_name: str, caption: str | None) -> str
DIRECTIVES = {
    "image": image,
    "image-sq": image_sq,
    "image-grid": image_grid,
    "bleed": bleed,
    "image-side": image_side,
    "kicker": kicker,
    "dek": dek,
    "pullquote": pullquote,
    "dropcap": dropcap,
}

# Directives that require a file argument; left untouched if none is given
FILE_DIRECTIVES = {"image", "image-sq", "image-grid", "bleed", "image-side"}


def process_directives(content: str, post_name: str) -> str:
    """Process all ::directive:args patterns in content.

    Supports optional caption in parentheses: ::image:file.avif(caption text)
    """

    def replace(match):
        name, args, caption = match.group(1), match.group(2), match.group(3)
        handler = DIRECTIVES.get(name)
        if handler:
            if name in FILE_DIRECTIVES and not args:
                return match.group(0)  # File directives need a file
            return handler(args, post_name, caption)
        return match.group(0)  # Leave unknown directives unchanged

    # :args is now optional, so text directives can be written ::name(text).
    # Captions may contain one level of nested parentheses, e.g. (Bond (2021) died here).
    return re.sub(
        r"::([a-z-]+)(?::([^\s(]+))?(?:\(((?:[^()]|\([^()]*\))+)\))?",
        replace,
        content,
    )
