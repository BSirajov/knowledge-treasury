#!/usr/bin/env python3
"""Bump ?v= query on script/link tags across HTML."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

BUMPS = {
    "js/kt-primary-nav.js": 59,
    "js/kt-i18n.js": 33,
}


def bump(text: str) -> tuple[str, int]:
    changes = 0
    for asset, version in BUMPS.items():
        pattern = re.compile(re.escape(asset) + r"\?v=\d+")
        repl = f"{asset}?v={version}"
        text, n = pattern.subn(repl, text)
        changes += n
    return text, changes


def main() -> None:
    files = 0
    tags = 0
    for path in ROOT.rglob("*.html"):
        if any(part in {".git", "preview", "documents"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        updated, n = bump(text)
        if n:
            path.write_text(updated, encoding="utf-8", newline="\n")
            files += 1
            tags += n
    print(f"Bumped {tags} script tags in {files} HTML files")


if __name__ == "__main__":
    main()
