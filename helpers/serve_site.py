#!/usr/bin/env python3
"""Local preview: python helpers/serve_site.py --port 8020"""
from __future__ import annotations

import argparse
import http.server
import socketserver
import threading
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8020)
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the site in the default browser after the server starts.",
    )
    args = parser.parse_args()

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(ROOT), **kw)

    url = f"http://{args.bind}:{args.port}/index.html"

    if args.open:
        def _open_browser() -> None:
            time.sleep(0.6)
            webbrowser.open(url)

        threading.Thread(target=_open_browser, daemon=True).start()

    with socketserver.TCPServer((args.bind, args.port), Handler) as httpd:
        print(f"Knowledge Treasury: {url}")
        print("Press Ctrl+C to stop the server.")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
