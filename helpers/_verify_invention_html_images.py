#!/usr/bin/env python3
"""Verify invention page image references resolve to files on disk."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

HTML = ROOT / "en" / "major_scientific_inventions.html"


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    refs = re.findall(r'src="(\.\./images/[^"]+)"', html)
    icon_refs = sorted({r for r in refs if "/icons/" in r})
    invention_refs = sorted({r for r in refs if "/inventions/" in r})
    missing = [r for r in icon_refs + invention_refs if not (ROOT / r.removeprefix("../")).is_file()]
    placeholders = len(re.findall(r"inventions-entry-icon-placeholder", html))

    print(f"Icon references: {len(icon_refs)}")
    print(f"Invention references: {len(invention_refs)}")
    print(f"Placeholders: {placeholders}")
    print(f"Missing files: {len(missing)}")
    for path in missing:
        print(f"  {path}")
    if missing or placeholders:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
