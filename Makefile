.PHONY: build serve

build:
	uv run tools/build_site.py --include-unlisted

serve:
	uv run tools/serve.py --include-unlisted
