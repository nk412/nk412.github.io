@@title: About this site
@@date: 20210418

# About this site

This static site is hosted on Github Pages, and is built with a custom minimal script powered by Python and markdown. There are many similar static site generators, and this one lacks quite a few features, but this one is mine! Markdown posts are stored under `./src/posts/`, and the build script uses Python `markdown` to render these as HTML. In addition to supporting standard Markdown Plus features, additional metadata like `@@title` and `@@date` can be provided, which allows them to be indexed correctly under the post listings. 

### Building

Run `make build` to:

1. Convert all `src/posts/*.md` files to `posts/*.html`
2. Update `index.html` with a post listing sorted by date (newest first)

### Dependencies

- Python 3.10+
- `markdown` package (auto-installed via `uv run` if using the script directly)

### See it on GitHub

On [Github](https://github.com/nk412/nk412.github.io)
