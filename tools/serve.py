#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown", "watchfiles"]
# ///
"""Dev server with auto-rebuild on changes."""

import argparse
import http.server
import socketserver
import threading
from pathlib import Path

from watchfiles import watch
from build_site import main as build_site

ROOT = Path(__file__).parent.parent
SRC = ROOT / "src"
PORT = 8000


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler that disables caching for HTML only."""
    def end_headers(self):
        if self.path.endswith((".html", "/")):
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()


class ReuseAddrServer(socketserver.TCPServer):
    """TCPServer that allows immediate port reuse after kill."""
    allow_reuse_address = True


def serve():
    """Run HTTP server in background thread."""
    import os
    os.chdir(ROOT)

    with ReuseAddrServer(("", PORT), NoCacheHandler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dev server with auto-rebuild")
    parser.add_argument(
        "--include-unlisted",
        action="store_true",
        help="Include posts with list: false in the index",
    )
    args = parser.parse_args()

    def build():
        build_site(include_unlisted=args.include_unlisted)

    build()

    server_thread = threading.Thread(target=serve, daemon=True)
    server_thread.start()
    print(f"\nServing at http://localhost:{PORT}")
    print("Watching src/ for changes...\n")

    for changes in watch(SRC):
        print(f"Changed: {[c[1] for c in changes]}")
        try:
            build()
        except Exception as e:
            print(f"Build error: {e}")
        print()
