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
| `@@list` | true/false | If false, builds page but hides from listing (default: true) |
| `@@draft` | true/false | If true, skips building entirely (default: false) |

## Building

```
make build
```

Outputs to `index.html` and `posts/`.
