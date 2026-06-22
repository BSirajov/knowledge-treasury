#!/usr/bin/env python3
"""Scan the Knowledge Treasury tree for legacy external-project markers."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _paths import ROOT

PATTERNS = [
    re.compile(r"daab", re.I),
    re.compile(r"waas", re.I),
    re.compile(r"data-daab", re.I),
    re.compile(r"gorkemli_shexsiyyetler", re.I),
    re.compile(r"World Association of Azerbaijani Scientists", re.I),
    re.compile(r"Dünya Azərbaycanlı.*Alimlər Birliyi", re.I),
    re.compile(r"scientists-catalog-toolbar", re.I),
    re.compile(r"kt-scientists-toolbar", re.I),
    re.compile(r"kt-encyclopedia-page", re.I),
]

SKIP_DIRS = {".git", ".cursor", "node_modules", ".venv", "venv", "__pycache__", "preview", "documents"}
SKIP_FILES = {
    "_kt_independence_audit.py",
    "_kt_independence_refs.py",
    "_kt_trim_breadcrumbs_fallback.py",
}


def main() -> int:
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".woff", ".woff2"}:
            continue
        if path.name in SKIP_FILES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern in PATTERNS:
            if pattern.search(text):
                hits.append(f"{path.relative_to(ROOT)} ({pattern.pattern})")
                break
    if hits:
        print("Legacy markers found:")
        for hit in sorted(hits):
            print(" ", hit)
        return 1
    print("No legacy DAAB/WAAS markers found in scanned text files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
