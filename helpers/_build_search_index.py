#!/usr/bin/env python3
"""Build i18n/search-index.json for global site search."""
from __future__ import annotations

import json
import re
from pathlib import Path

from _paths import ROOT

OUT = ROOT / "i18n" / "search-index.json"
OUT_JS = ROOT / "i18n" / "search-index.js"
ROUTES = json.loads((ROOT / "i18n" / "routes.json").read_text(encoding="utf-8"))
UI = json.loads((ROOT / "i18n" / "ui.json").read_text(encoding="utf-8"))

PAGE_LABEL_KEYS = {
    "home": "home",
    "prominent-figures": "prominentFigures",
    "industrial-revolutions": "industrialRevolutions",
    "major-scientific-inventions": "majorScientificInventions",
}
PAGE_ICONS = {
    "home": "🏠",
    "prominent-figures": "👤",
    "industrial-revolutions": "⚙️",
    "major-scientific-inventions": "💡",
}
PAGE_TYPES = {
    "home": "page",
    "prominent-figures": "page",
    "industrial-revolutions": "page",
    "major-scientific-inventions": "page",
}
SKIP_PAGE_IDS = {"prominent-figure"}


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "entry"


def parse_catalog_js(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    match = re.search(r"=\s*(\[.*\])\s*;?\s*$", text, re.DOTALL)
    if not match:
        return []
    return json.loads(match.group(1))


def profile_tags(row: dict) -> str:
    parts = [
        row.get("name") or "",
        row.get("dates") or "",
        row.get("country") or "",
        row.get("field") or "",
        row.get("period") or "",
        row.get("categoryLabel") or "",
        row.get("summary") or "",
    ]
    return " ".join(p for p in parts if p).strip()


def profile_entry(az_row: dict | None, en_row: dict | None) -> dict:
    row = en_row or az_row or {}
    entry_id = (en_row or az_row or {}).get("id") or slugify(row.get("name", "profile"))
    icon = row.get("emoji") or "👤"
    az = az_row or en_row or {}
    en = en_row or az_row or {}
    return {
        "id": entry_id,
        "type": "profile",
        "icon": icon,
        "az": {
            "title": az.get("name") or en.get("name") or entry_id,
            "desc": az.get("dates") or en.get("dates") or "",
            "href": f"az/{az.get('href') or en.get('href', '')}",
            "tags": profile_tags(az if az_row else en),
        },
        "en": {
            "title": en.get("name") or az.get("name") or entry_id,
            "desc": en.get("dates") or az.get("dates") or "",
            "href": f"en/{en.get('href') or az.get('href', '')}",
            "tags": profile_tags(en if en_row else az),
        },
    }


def page_entry(page: dict) -> dict:
    page_id = page["id"]
    key = PAGE_LABEL_KEYS.get(page_id, page_id)
    icon = PAGE_ICONS.get(page_id, "📄")
    return {
        "id": page_id,
        "type": PAGE_TYPES.get(page_id, "page"),
        "icon": icon,
        "az": {
            "title": UI["nav"]["az"].get(key, page_id),
            "desc": UI["nav"]["az"].get(key + "Desc", ""),
            "href": page["az"],
            "tags": UI["nav"]["az"].get(key, page_id),
        },
        "en": {
            "title": UI["nav"]["en"].get(key, page_id),
            "desc": UI["nav"]["en"].get(key + "Desc", ""),
            "href": page["en"],
            "tags": UI["nav"]["en"].get(key, page_id),
        },
    }


def invention_entries() -> list[dict]:
    data_path = ROOT / "helpers" / "_inventions_table_data_merged.json"
    if not data_path.exists():
        return []
    rows = json.loads(data_path.read_text(encoding="utf-8"))
    entries: list[dict] = []
    for row in rows:
        name = row.get("name") or ""
        if not name:
            continue
        slug = slugify(name)
        summary = row.get("summary") or ""
        period = row.get("period") or ""
        figures = row.get("key_figures") or ""
        tags = " ".join(
            p
            for p in [name, period, figures, summary, " ".join(row.get("key_facts") or [])]
            if p
        )
        entries.append(
            {
                "id": f"invention-{slug}",
                "type": "invention",
                "icon": "💡",
                "az": {
                    "title": name,
                    "desc": period,
                    "href": f"en/major_scientific_inventions.html#{slug}",
                    "tags": tags,
                },
                "en": {
                    "title": name,
                    "desc": period,
                    "href": f"en/major_scientific_inventions.html#{slug}",
                    "tags": tags,
                },
            }
        )
    return entries


def merge_profiles(az_rows: list[dict], en_rows: list[dict]) -> list[dict]:
    by_id: dict[str, dict] = {}
    for row in az_rows:
        by_id[row["id"]] = {"az": row}
    for row in en_rows:
        slot = by_id.setdefault(row["id"], {})
        slot["en"] = row
    out: list[dict] = []
    for pid in sorted(by_id.keys()):
        slot = by_id[pid]
        out.append(profile_entry(slot.get("az"), slot.get("en")))
    return out


def main() -> None:
    entries: list[dict] = []
    for page in ROUTES.get("pages", []):
        if page.get("id") in SKIP_PAGE_IDS:
            continue
        if page.get("sitemap") is False and page.get("id") not in PAGE_LABEL_KEYS:
            continue
        entries.append(page_entry(page))

    az_profiles = parse_catalog_js(ROOT / "js" / "prominent-figures-catalog-data.js")
    en_profiles = parse_catalog_js(ROOT / "js" / "prominent-figures-catalog-data-en.js")
    entries.extend(merge_profiles(az_profiles, en_profiles))
    entries.extend(invention_entries())

    payload = {"version": 1, "entries": entries}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_JS.write_text(
        "window.__KT_SEARCH_INDEX__ = "
        + json.dumps(payload, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(entries)} entries to {OUT.relative_to(ROOT)}")
    print(f"Wrote {OUT_JS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
