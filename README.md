# nk412.github.io

## Writing Posts

Create markdown files in `src/posts/`. Each post requires metadata at the top:

```
@@title: Post Title
@@date: YYYYMMDD
```

### Optional Metadata

| Key | Values | Description |
|-----|--------|-------------|
| `@@type` | any string | Shown in listing as "Title (type)" in gray |
| `@@unlisted` | flag | Builds the page but hides it from the listing |
| `@@draft` | true/false | If true, skips building entirely (default: false) |
| `@@photos` | true/false | If true, adds lazy loading to images (default: false) |
| `@@essay` | flag | Centered single-column layout; enables `::bleed:` full-width images |
| `@@theme` | dark | Dark background, for night photography essays |

## Content Directives

Inline `::name:args(caption)` patterns in the markdown body:

| Directive | Example | Result |
|-----------|---------|--------|
| `::image:` | `::image:a.avif(cap)` | Single image, or comma-separated side-by-side row |
| `::image-sq:` | `::image-sq:a.avif` | Square crop via CSS |
| `::image-grid:` | `::image-grid:a.avif,b.avif,c.avif,d.avif` | 2-column masonry grid |
| `::bleed:` | `::bleed:a.avif(cap)` | Full-bleed image, edge-to-edge (needs `@@essay`) |
| `::image-side:` | `::image-side:a.avif(cap)` | Caption in the side margin, stacks on mobile |
| `::kicker` | `::kicker(PHOTO ESSAY · SVALBARD)` | Letterspaced eyebrow label above a heading |
| `::dek` | `::dek(Intro text.)` | Standfirst: large italic intro paragraph |
| `::pullquote` | `::pullquote(A striking line.)` | Big display-font quote with rules above/below |
| `::dropcap` | `::dropcap(Opening paragraph...)` | Large CSS drop cap on the first letter |

## Photos

Convert originals to AVIF (2000px on the short edge) into `assets/<post>/`:

```
uv run tools/to_avif.py <post> photo.jpg [more.jpg ...]
```

## Building

```
make build
```

Outputs to `index.html` and `posts/`.
