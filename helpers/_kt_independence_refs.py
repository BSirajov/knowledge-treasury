#!/usr/bin/env python3
"""Replace legacy asset paths after Knowledge Treasury independence rename."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

REPLACEMENTS = [
    ("scientists-catalog-toolbar.css", "kt-catalog-toolbar.css"),
    ("kt-scientists-toolbar-mobile.js", "kt-catalog-toolbar-mobile.js"),
    ("kt-encyclopedia-page.css", "kt-prominent-figures-page.css"),
]

SKIP_DIRS = {".git", ".cursor", "node_modules", ".venv", "venv", "__pycache__"}
TEXT_SUFFIXES = {
    ".html",
    ".css",
    ".js",
    ".py",
    ".json",
    ".md",
    ".bat",
    ".xml",
    ".txt",
}


def should_scan(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    return True


def main() -> None:
    changed: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or not should_scan(path):
            continue
        if path.name == "_kt_independence_refs.py":
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            changed.append(str(path.relative_to(ROOT)))
    print(f"Updated {len(changed)} files")
    for item in sorted(changed):
        print(f"  {item}")


if __name__ == "__main__":
    main()
