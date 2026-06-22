#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
html = (ROOT / "en" / "major_scientific_inventions.html").read_text(encoding="utf-8")
needed = sorted(set(re.findall(r"icons/([^\"]+\.png)", html)))

folders = [
    ROOT / "images" / "inventions" / "icons",
    ROOT / "en" / "_images",
    ROOT / "en" / "_images" / "inventions" / "icons",
]
for folder in folders:
    if not folder.exists():
        print(f"{folder}: MISSING DIR")
        continue
    files = {f.name for f in folder.glob("*.png")}
    missing = [n for n in needed if n not in files]
    print(f"{folder.relative_to(ROOT)}: {len(files)} png, missing {len(missing)}/{len(needed)}")
    if folder.name == "_images" or "icons" in str(folder):
        for n in missing:
            stem = n.replace(".png", "")
            fuzzy = [f for f in files if stem in f or f.replace(".png", "") in stem]
            if fuzzy:
                print(f"  fuzzy {n} -> {fuzzy[:2]}")
