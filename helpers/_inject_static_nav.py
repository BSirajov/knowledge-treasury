#!/usr/bin/env python3
"""Inject static primary-nav links into HTML (visible before / without JS)."""
from __future__ import annotations

import json
import re
from pathlib import Path

from _paths import ROOT

NAV = json.loads((ROOT / "i18n" / "nav.json").read_text(encoding="utf-8"))
ROUTES = {p["id"]: p for p in json.loads((ROOT / "i18n" / "routes.json").read_text(encoding="utf-8"))["pages"]}
UI = json.loads((ROOT / "i18n" / "ui.json").read_text(encoding="utf-8"))

ICONS = {
    "prominent-figures": "👤",
    "major-scientific-inventions": "💡",
    "industrial-revolutions": "⚙️",
}
LABEL_KEYS = {
    "prominent-figures": "prominentFigures",
    "major-scientific-inventions": "majorScientificInventions",
    "industrial-revolutions": "industrialRevolutions",
}

PLACEHOLDER_RE = re.compile(
    r'<div class="nav-menu" id="primaryNavMenu"[^>]*>\s*'
    r'(?:<div class="nav-divider"></div>\s*)?'
    r'(?:<a class="nav-link"[^>]*>.*?</a>\s*)*'
    r'</div>',
    re.DOTALL,
)


def path_key(html_path: Path) -> str:
    rel = html_path.relative_to(ROOT).as_posix().lower()
    return rel


def page_href(page: dict, lang: str, html_path: Path) -> str:
    target = page["en" if lang == "en" else "az"]
    prefix = f"{lang}/"
    if target.lower().startswith(prefix):
        target = target[len(prefix) :]
    parts = path_key(html_path).split("/")
    if parts and parts[0] in {"az", "en"}:
        here_suffix = "/".join(parts[1:])
    else:
        here_suffix = "/".join(parts)
    here_parts = [p for p in here_suffix.split("/") if p]
    if here_parts:
        here_parts.pop()
    up = len(here_parts)
    return ("../" * up if up else "") + target


def detect_lang(html_path: Path, text: str) -> str:
    m = re.search(r'data-kt-lang="(az|en)"', text)
    if m:
        return m.group(1)
    if html_path.parts and html_path.parts[0] == "en":
        return "en"
    if html_path.parts and html_path.parts[0] == "az":
        return "az"
    return "az"


def build_static_nav(lang: str, html_path: Path) -> str:
    links: list[str] = ['<div class="nav-divider"></div>']
    for item in NAV.get("primary", []):
        if item.get("type") != "page":
            continue
        page = ROUTES.get(item["id"])
        if not page:
            continue
        key = LABEL_KEYS[item["id"]]
        label = UI["nav"][lang][key]
        icon = ICONS.get(item["id"], "")
        href = page_href(page, lang, html_path)
        links.append(
            f'<a class="nav-link" href="{href}" data-nav-id="{item["id"]}">{icon}\xa0{label}</a>'
        )
    return (
        '<div class="nav-menu" id="primaryNavMenu" data-kt-nav-placeholder="1">'
        + "".join(links)
        + "</div>"
    )


def inject_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'id="primaryNavMenu"' not in text:
        return False
    lang = detect_lang(path, text)
    block = build_static_nav(lang, path)
    updated, count = PLACEHOLDER_RE.subn(block, text, count=1)
    if count != 1 or updated == text:
        return False
    path.write_text(updated, encoding="utf-8", newline="\n")
    return True


def main() -> None:
    updated = 0
    for path in ROOT.rglob("*.html"):
        if any(part in {".git", "preview", "documents"} for part in path.parts):
            continue
        if path.name == "index.html" and path.parent == ROOT:
            continue
        if inject_file(path):
            updated += 1
    print(f"Injected static nav links in {updated} HTML files")


if __name__ == "__main__":
    main()
