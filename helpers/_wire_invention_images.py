#!/usr/bin/env python3
"""Copy invention illustrations into images/inventions/ and update HTML img paths."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INVENTIONS = ROOT / "images" / "inventions"
INFOGRAPHS = ROOT / "images" / "infographs"
HTML_FILES = [
    ROOT / "en" / "major_scientific_inventions.html",
    ROOT / "az" / "major_scientific_inventions.html",
]

# HTML filename stem -> artefact slug in images/infographs
ARTEFACT_ALIASES: dict[str, str] = {
    "microchip": "integrated-circuit-microchip",
    "fibre-optic": "fibre-optic-communication",
}


def artefact_source(slug: str) -> Path | None:
    artefact_slug = ARTEFACT_ALIASES.get(slug, slug)
    artefact = INFOGRAPHS / f"{artefact_slug}-artefact.png"
    if artefact.exists():
        return artefact

    for candidate in (
        INVENTIONS / f"{slug}.png",
        INVENTIONS / "icons" / f"{slug}.png",
        INVENTIONS / "icons" / f"{artefact_slug}.png",
    ):
        if candidate.exists():
            return candidate
    return None


def ensure_invention_image(slug: str) -> Path | None:
    dest = INVENTIONS / f"{slug}.png"
    if dest.exists():
        return dest

    src = artefact_source(slug)
    if src is None:
        return None

    shutil.copy2(src, dest)
    return dest


def collect_slugs(html: str) -> set[str]:
    return set(re.findall(r'inventions-entry-icon"><img src="[^"]+/([^"/]+)\.png"', html))


def update_html(path: Path, slugs: set[str]) -> tuple[int, list[str]]:
    text = path.read_text(encoding="utf-8")
    missing: list[str] = []
    replacements = 0

    for slug in slugs:
        dest = ensure_invention_image(slug)
        if dest is None:
            missing.append(slug)
            continue

        new_src = f"../images/inventions/{slug}.png"
        for old in (
            f"../images/inventions/icons/{slug}.png",
            f"../images/infographs/{slug}-artefact.png",
            f"../images/infographs/{slug}.png",
            f"../images/temp/{slug}-artefact.png",
            f"../images/temp/{slug}.png",
        ):
            if old in text:
                count = text.count(old)
                text = text.replace(old, new_src)
                replacements += count

    if text != path.read_text(encoding="utf-8"):
        path.write_text(text, encoding="utf-8")

    return replacements, missing


def main() -> None:
    INVENTIONS.mkdir(parents=True, exist_ok=True)

    slugs: set[str] = set()
    for html in HTML_FILES:
        slugs |= collect_slugs(html.read_text(encoding="utf-8"))

    added = 0
    for slug in sorted(slugs):
        dest = INVENTIONS / f"{slug}.png"
        if dest.exists():
            continue
        src = artefact_source(slug)
        if src:
            shutil.copy2(src, dest)
            added += 1
            print(f"  added {dest.name} <- {src.relative_to(ROOT)}")

    still_missing: list[str] = []
    total_repl = 0
    for html in HTML_FILES:
        repl, missing = update_html(html, slugs)
        total_repl += repl
        still_missing.extend(missing)
        icons_left = html.read_text(encoding="utf-8").count("../images/inventions/icons/")
        print(f"{html.relative_to(ROOT)}: {repl} path updates, icons refs left={icons_left}")

    still_missing = sorted(set(still_missing))
    print(f"Added {added} images; {total_repl} src path replacements")
    if still_missing:
        print(f"Missing ({len(still_missing)}): {', '.join(still_missing)}")
    else:
        print(f"All {len(slugs)} entries wired to images/inventions/")


if __name__ == "__main__":
    main()
