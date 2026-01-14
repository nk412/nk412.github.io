#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown", "watchfiles"]
# ///
"""Dev server with auto-rebuild on changes."""

import http.server
import socketserver
import threading
from pathlib import Path

from watchfiles import watch
from build_site import main as build

ROOT = Path(__file__).parent.parent
SRC = ROOT / "src"
PORT = 8000


def serve():
    """Run HTTP server in background thread."""
    import os
    os.chdir(ROOT)

    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    build()

    server_thread = threading.Thread(target=serve, daemon=True)
    server_thread.start()
    print(f"\nServing at http://localhost:{PORT}")
    print("Watching src/ for changes...\n")

    for changes in watch(SRC):
        print(f"Changed: {[c[1] for c in changes]}")
        build()
        print()
