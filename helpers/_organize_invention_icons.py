#!/usr/bin/env python3
"""Organize invention icons into section subfolders under images/icons/."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from _paths import ROOT

ICONS_DIR = ROOT / "images" / "icons"
TABLE_DATA = ROOT / "helpers" / "_inventions_table_data.json"
CARD_DATA = ROOT / "preview" / "inventions-card-data.json"
ICON_INDEX = ROOT / "helpers" / "_invention_icon_index.json"

SECTION_FOLDERS: dict[str, str] = {
    "1": "1-foundational-civilisational-innovations",
    "2": "2-knowledge-science-and-measurement",
    "3": "3-industrial-energy-and-transport-revolutions",
    "4": "4-medicine-biology-and-public-health",
    "5": "5-physics-chemistry-and-materials-science",
    "6": "6-digital-space-and-communication-technologies",
    "7": "7-emerging-and-transformative-technologies",
}

# Card-data slugs not present in the inventions table (section number for folder lookup).
EXTRA_ICON_SECTIONS: dict[str, str] = {
    "cloud-computing": "6",
}

# Legacy flat filenames in images/icons/ (before slug-normalisation).
SOURCE_ALIASES: dict[str, str] = {
    "the-wheel": "wheel.png",
    "the-compass": "compass.png",
    "the-microscope": "microscope.png",
    "the-telescope": "telescope.png",
    "the-printing-press": "printing-press.png",
    "the-scientific-method": "scientific-method.png",
    "the-periodic-table": "periodic-table.png",
    "mathematics-and-the-concept-of-zero": "mathematics-and-concept-of-zero.png",
}


def section_folder(num: str) -> str:
    return SECTION_FOLDERS[num.split(".", 1)[0]]


def icon_rel_path(slug: str, num: str) -> str:
    folder = section_folder(num)
    return f"images/icons/{folder}/{slug}.png"


def site_icon_path(slug: str, num: str) -> str:
    """Path from en/ or az/ HTML pages."""
    folder = section_folder(num)
    return f"../images/icons/{folder}/{slug}.png"


def resolve_source(slug: str, flat_dir: Path) -> Path | None:
    for name in (SOURCE_ALIASES.get(slug, f"{slug}.png"), f"{slug}.png"):
        candidate = flat_dir / name
        if candidate.exists():
            return candidate
    return None


def load_entries() -> list[dict]:
    return json.loads(TABLE_DATA.read_text(encoding="utf-8"))


def slug_section_num(slug: str, by_slug: dict[str, dict]) -> str | None:
    entry = by_slug.get(slug)
    if entry:
        return entry["num"]
    extra = EXTRA_ICON_SECTIONS.get(slug)
    return f"{extra}.0" if extra else None


def organize_icons() -> dict[str, str]:
    entries = load_entries()
    by_slug = {e["slug"]: e for e in entries}
    all_slugs = list(by_slug)
    for slug in EXTRA_ICON_SECTIONS:
        if slug not in all_slugs:
            all_slugs.append(slug)

    moved: dict[str, str] = {}

    for slug in all_slugs:
        entry = by_slug.get(slug)
        if entry:
            num = entry["num"]
        elif slug in EXTRA_ICON_SECTIONS:
            num = f"{EXTRA_ICON_SECTIONS[slug]}.0"
        else:
            continue
        folder = section_folder(num)
        dest_dir = ICONS_DIR / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"{slug}.png"

        if dest.exists():
            moved[slug] = str(dest.relative_to(ROOT)).replace("\\", "/")
            continue

        src = resolve_source(slug, ICONS_DIR)
        if src is None:
            # Already in section folder under a legacy alias filename.
            alias_name = SOURCE_ALIASES.get(slug)
            if alias_name:
                alias_in_folder = dest_dir / alias_name
                if alias_in_folder.exists():
                    alias_in_folder.rename(dest)
                    moved[slug] = str(dest.relative_to(ROOT)).replace("\\", "/")
                    print(f"  {alias_in_folder.name} -> {dest.relative_to(ROOT)} (rename)")
                    continue
            print(f"  skip (no source): {slug}")
            continue

        shutil.move(str(src), str(dest))
        moved[slug] = str(dest.relative_to(ROOT)).replace("\\", "/")
        print(f"  {src.name} -> {dest.relative_to(ROOT)}")

    leftovers = sorted(ICONS_DIR.glob("*.png"))
    if leftovers:
        print(f"\nWarning: {len(leftovers)} icon(s) still in images/icons/ root:")
        for path in leftovers:
            print(f"  {path.name}")

    return moved


def update_card_data(entries: list[dict]) -> int:
    if not CARD_DATA.exists():
        return 0
    cards = json.loads(CARD_DATA.read_text(encoding="utf-8"))
    by_slug = {e["slug"]: e for e in entries}
    updated = 0
    for slug, card in cards.items():
        num = slug_section_num(slug, by_slug)
        if not num:
            continue
        new_path = icon_rel_path(slug, num)
        if card.get("icon") != new_path:
            card["icon"] = new_path
            updated += 1
    CARD_DATA.write_text(json.dumps(cards, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return updated


def write_index(entries: list[dict]) -> None:
    by_slug = {e["slug"]: e for e in entries}
    icon_slugs = list(by_slug)
    for slug in EXTRA_ICON_SECTIONS:
        if slug not in icon_slugs:
            icon_slugs.append(slug)

    icons: dict[str, dict] = {}
    for slug in icon_slugs:
        num = slug_section_num(slug, by_slug)
        if not num:
            continue
        icons[slug] = {
            "num": num if slug in by_slug else EXTRA_ICON_SECTIONS.get(slug, "") + ".0",
            "section": section_folder(num),
            "path": icon_rel_path(slug, num),
            "site_path": site_icon_path(slug, num),
        }

    index = {"section_folders": SECTION_FOLDERS, "icons": icons}
    ICON_INDEX.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    entries = load_entries()
    print("Organizing icons into section subfolders...")
    moved = organize_icons()
    print(f"\nMoved or verified {len(moved)} icons.")
    updated = update_card_data(entries)
    print(f"Updated {updated} icon paths in {CARD_DATA.relative_to(ROOT)}")
    write_index(entries)
    print(f"Wrote {ICON_INDEX.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
