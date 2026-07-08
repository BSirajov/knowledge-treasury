"""Audit prominent figures catalog by origin group."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GROUPS = {
    "Kazakh": ["Qazax", "Qazaxıstan", "Kazakh", "Kazakhstan", "Türk/Qazax"],
    "Kyrgyz": ["Qırğız", "Qırğızıstan", "Kyrgyz", "Kyrgyzstan", "Qaraxanlı"],
    "Uzbek": ["Özbək", "Uzbek", "Türk/Özbək", "Teymurid", "Timurid", "Xivə", "Buxara", "Səmərqənd"],
    "Turkmen": ["Türkmən", "Turkmen"],
    "Ottoman": ["Osmanlı", "Ottoman"],
    "Chinese": ["Çin", "Chinese"],
    "Arab": ["Ərəb", "Arab", "İslam dünyası", "Islamic world", "Suriya", "Misir", "Əndəlüs", "Andalus", "Bağdad", "Baghdad"],
}

for lang, fname in [("AZ", "js/prominent-figures-catalog-data.js"), ("EN", "js/prominent-figures-catalog-data-en.js")]:
    text = (ROOT / fname).read_text(encoding="utf-8")
    data = json.loads(re.search(r"=\s*(\[.*\])\s*;", text, re.S).group(1))
    print(f"=== {lang} total: {len(data)} ===\n")
    for g, keys in GROUPS.items():
        hits = [r for r in data if any(k.lower() in (r.get("country") or "").lower() for k in keys)]
        print(f"{g}: {len(hits)}")
        for r in sorted(hits, key=lambda x: x["name"]):
            print(f"  - {r['id']}: {r['name']} ({r.get('country')}) [{r.get('field')}]")
        print()
