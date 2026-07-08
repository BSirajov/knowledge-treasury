"""Audit prominent figures by East/South/Southeast Asian origin."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GROUPS = {
    "India": ["Hindistan", "India", "Qədim Hindistan"],
    "Japan": ["Yaponiya", "Japan"],
    "Korea": ["Koreya", "Korea"],
    "China": ["Çin", "Chinese"],
    "Indonesia": ["İndoneziya", "Indonesia"],
    "Vietnam": ["Vyetnam", "Vietnam"],
    "Cambodia": ["Kamboca", "Cambodia"],
    "Thailand": ["Tailand", "Thailand"],
    "Mongolia": ["Monqolistan", "Mongolia"],
    "Persia/Iran": ["Fars/İran", "Persia", "Iran"],
}

text = (ROOT / "js/prominent-figures-catalog-data.js").read_text(encoding="utf-8")
data = json.loads(re.search(r"=\s*(\[.*\])\s*;", text, re.S).group(1))
print(f"Total catalog: {len(data)}\n")
for g, keys in GROUPS.items():
    hits = [r for r in data if any(k.lower() in (r.get("country") or "").lower() for k in keys)]
    print(f"{g}: {len(hits)}")
    for r in sorted(hits, key=lambda x: x["name"]):
        print(f"  - {r['id']}: {r['name']}")
    print()
