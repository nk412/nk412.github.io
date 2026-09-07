#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow>=11.2"]
# ///
"""Convert photos to AVIF for the photoblog.

Resizes so the short edge is SHORT_EDGE pixels, applies EXIF rotation,
and writes <name>.avif into assets/<post>/.

Usage:
    uv run tools/to_avif.py <post> <image> [<image> ...]
    uv run tools/to_avif.py greenland ~/Pictures/DSC01234.jpg

Output filename is the input stem, lowercased. Pass --name to override
(single input only). Pass --short-edge to change the target size.
"""

import argparse
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).parent.parent
SHORT_EDGE = 2000
QUALITY = 75


def convert(src: Path, dst: Path, short_edge: int = SHORT_EDGE) -> None:
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = im.size
    scale = short_edge / min(w, h)
    if scale < 1:
        im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, quality=QUALITY, speed=4)
    print(f"  {src.name} -> {dst.relative_to(ROOT)} {im.size[0]}x{im.size[1]} {dst.stat().st_size // 1024}KB")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("post", help="post name, i.e. the folder under assets/")
    p.add_argument("images", nargs="+", type=Path)
    p.add_argument("--name", help="output stem (single input only)")
    p.add_argument("--short-edge", type=int, default=SHORT_EDGE, help=f"target short edge in px (default {SHORT_EDGE})")
    args = p.parse_args()
    if args.name and len(args.images) > 1:
        p.error("--name only works with a single input image")
    out_dir = ROOT / "assets" / args.post
    for src in args.images:
        stem = args.name or src.stem.lower()
        convert(src, out_dir / f"{stem}.avif", args.short_edge)


if __name__ == "__main__":
    main()
