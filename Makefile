.PHONY: build serve

build:
	uv run tools/build_site.py

serve:
	uv run tools/serve.py
