#!/usr/bin/env python3
"""Repair malformed css/? and js/? asset references across site HTML."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

CSS_FIX = 'css/kt-site-background.css?v=6'
JS_BROKEN = re.compile(r'\n<script src="[^"]*js/\?v=12" defer></script>')

changed = 0
for path in ROOT.rglob("*.html"):
    if "node_modules" in path.parts:
        continue
    text = path.read_text(encoding="utf-8")
    original = text
    text = text.replace('css/?v=6', CSS_FIX)
    text = JS_BROKEN.sub("", text)
    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        changed += 1

print(f"Fixed {changed} HTML files")
