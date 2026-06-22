#!/usr/bin/env python3
"""Find missing invention images referenced in major_scientific_inventions.html."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
html = (ROOT / "en" / "major_scientific_inventions.html").read_text(encoding="utf-8")

# All img src under images/inventions
refs = re.findall(r'src="(\.\./images/inventions/[^"]+)"', html)
refs = sorted(set(refs))

missing = []
present = []
for r in refs:
    p = ROOT / "en" / r.replace("../", "")
    if p.exists():
        present.append((r, p.stat().st_size))
    else:
        missing.append(r)

print(f"Unique invention image refs: {len(refs)}")
print(f"Present: {len(present)}")
print(f"Missing: {len(missing)}")
for m in missing:
    print(f"  MISSING: {m}")

# Extract entry id -> img mapping
entries = re.findall(
    r'id="([^"]+)"[^>]*data-search="[^"]*?(\d+\.\d+)[^"]*".*?'
    r'<img src="(\.\./images/inventions/[^"]+)"',
    html,
    re.S,
)
# Simpler: line by line
entry_imgs = []
current_id = None
for line in html.splitlines():
    m = re.search(r'<article class="inventions-entry" id="([^"]+)"', line)
    if m:
        current_id = m.group(1)
    m = re.search(r'<img src="(\.\./images/inventions/[^"]+)" alt="Illustration: ([^"]+)"', line)
    if m and current_id:
        path = ROOT / "en" / m.group(1).replace("../", "")
        entry_imgs.append({
            "id": current_id,
            "title": m.group(2),
            "src": m.group(1),
            "exists": path.exists(),
            "bytes": path.stat().st_size if path.exists() else 0,
        })
        current_id = None

print(f"\nEntry icons: {len(entry_imgs)}")
missing_entries = [e for e in entry_imgs if not e["exists"]]
print(f"Entries with missing files: {len(missing_entries)}")
for e in missing_entries:
    print(f"  {e['id']}: {e['src']}")

# Very small files might be placeholders
small = [e for e in entry_imgs if e["exists"] and e["bytes"] < 5000]
print(f"\nEntries with very small images (<5KB, possible placeholder): {len(small)}")
for e in sorted(small, key=lambda x: x["bytes"]):
    print(f"  {e['bytes']:5d} B  {e['id']}")

# Overview section images
if "overview-by-category" in html:
    start = html.index('id="overview-by-category"')
    chunk = html[start:start + 15000]
    ov_imgs = re.findall(r'src="([^"]+)"', chunk)
    print(f"\nOverview section images: {len(ov_imgs)}")
    for img in ov_imgs:
        p = ROOT / "en" / img.replace("../", "") if img.startswith("../") else ROOT / img.lstrip("/")
        print(f"  {img} -> {'OK' if p.exists() else 'MISSING'}")
