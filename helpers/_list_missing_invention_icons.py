#!/usr/bin/env python3
"""List missing invention icons referenced by major_scientific_inventions.html."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
html = (ROOT / "en" / "major_scientific_inventions.html").read_text(encoding="utf-8")
icons_dir = ROOT / "images" / "inventions" / "icons"

entries = []
current_id = None
num = None
for line in html.splitlines():
    m = re.search(r'<article class="inventions-entry" id="([^"]+)"', line)
    if m:
        current_id = m.group(1)
    m = re.search(r'inventions-entry-num[^>]*>([^<]+)</span>', line)
    if m and current_id:
        num = m.group(1).strip()
    m = re.search(
        r'<img src="\.\./images/inventions/icons/([^"]+)" alt="Illustration: ([^"]+)"',
        line,
    )
    if m and current_id:
        fname = m.group(1)
        title = m.group(2)
        path = icons_dir / fname
        entries.append(
            {
                "section": num or "?",
                "id": current_id,
                "title": title,
                "filename": fname,
                "exists": path.is_file(),
                "bytes": path.stat().st_size if path.is_file() else 0,
            }
        )
        current_id = None
        num = None

missing = [e for e in entries if not e["exists"]]
present = [e for e in entries if e["exists"]]
print(f"Total entries: {len(entries)}")
print(f"Present: {len(present)}")
print(f"Missing: {len(missing)}\n")
for e in missing:
    print(f"{e['section']}\t{e['id']}\t{e['filename']}")
