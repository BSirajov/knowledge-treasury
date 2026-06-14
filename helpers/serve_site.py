#!/usr/bin/env python3
"""Local preview: python helpers/serve_site.py --port 8020"""
from __future__ import annotations

import argparse
import http.server
import socketserver
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8020)
    args = parser.parse_args()

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(ROOT), **kw)

    with socketserver.TCPServer((args.bind, args.port), Handler) as httpd:
        print(f"Knowledge Treasury: http://{args.bind}:{args.port}/index.html")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
