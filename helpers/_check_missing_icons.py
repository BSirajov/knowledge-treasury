#!/usr/bin/env python3
"""List missing invention icons referenced by card data and the icon index."""
import json
import re
from pathlib import Path

from _paths import ROOT

ICONS_DIR = ROOT / "images" / "icons"
CARD_DATA = ROOT / "preview" / "inventions-card-data.json"
ICON_INDEX = ROOT / "helpers" / "_invention_icon_index.json"


def check_card_data() -> list[tuple[str, str]]:
    if not CARD_DATA.exists():
        return []
    cards = json.loads(CARD_DATA.read_text(encoding="utf-8"))
    missing = []
    for slug, card in cards.items():
        rel = card.get("icon", "")
        if rel and not (ROOT / rel).is_file():
            missing.append((slug, rel))
    return missing


def check_html_site_paths() -> list[tuple[str, str]]:
    html = (ROOT / "en" / "major_scientific_inventions.html").read_text(encoding="utf-8")
    refs = re.findall(r'src="(\.\./images/icons/[^"]+)"', html)
    missing = []
    for ref in sorted(set(refs)):
        rel = ref.removeprefix("../")
        if not (ROOT / rel).is_file():
            missing.append((ref, rel))
    return missing


def main() -> None:
    card_missing = check_card_data()
    html_missing = check_html_site_paths()
    section_counts = {
        d.name: len(list(d.glob("*.png")))
        for d in sorted(ICONS_DIR.iterdir())
        if d.is_dir()
    }
    root_loose = len(list(ICONS_DIR.glob("*.png")))

    print("Section icon counts:")
    for name, count in section_counts.items():
        print(f"  {name}: {count}")
    print(f"  (root loose: {root_loose})")
    print(f"\nCard-data missing: {len(card_missing)}")
    for slug, path in card_missing:
        print(f"  {slug}: {path}")
    print(f"\nHTML missing: {len(html_missing)}")
    for ref, path in html_missing:
        print(f"  {ref}")


if __name__ == "__main__":
    main()
