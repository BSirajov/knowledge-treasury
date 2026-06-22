#!/usr/bin/env python3
"""Rebuild prominent-figures catalogue data with corrected period labels."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

from _historical_periods import infer_pf_period_az, infer_pf_period_en
from _paths import ROOT

FIGURES_ROOT_AZ = ROOT / "az" / "prominent_figures"
FIGURES_ROOT_EN = ROOT / "en" / "prominent_figures"
OUT_AZ = ROOT / "js" / "prominent-figures-catalog-data.js"
OUT_EN = ROOT / "js" / "prominent-figures-catalog-data-en.js"

RE_NAME = re.compile(r"<h1>([^<]+)</h1>")
RE_DATES = re.compile(r'<p class="pf-hero-dates">([^<]+)</p>')
RE_SHORT = re.compile(
    r'class="prose pf-profile-article">.*?<p>([^<]{20,400})</p>',
    re.DOTALL,
)
RE_EMOJI = re.compile(r'<span class="pf-hero-symbol__icon">([^<]+)</span>')
RE_GOLD = re.compile(r'<span class="hero-tag gold">([^<]+)</span>')
RE_FIELD = re.compile(
    r'info-label">(?:Sahə|Field)</span><span class="info-val">([^<]+)</span>'
)
RE_BIRTH = re.compile(
    r'info-label">(?:Doğum tarixi|Year of birth)</span><span class="info-val">([^<]+)</span>'
)
RE_YEAR = re.compile(r"(\d{3,4})")

CATEGORY_LABELS = {
    "azturk": "Azərbaycan və türk dünyası",
    "world": "Dünya alimləri",
}
CATEGORY_LABEL_EN = {
    "azturk": "Azerbaijani & Turkic heritage",
    "world": "World scientists",
}


def parse_century_year(text: str) -> int | None:
    m = re.search(
        r"\b(\d{1,2})(?:st|nd|rd|th)?\s*century\b|"
        r"\b(\d{1,2})\s*(?:-ci|-cü|-cu|-cü|-nci|-ncü|-ncu|-ncü)\s*əsr\b",
        text,
        re.I,
    )
    if not m:
        return None
    century = int(m.group(1) or m.group(2))
    return max(1, (century - 1) * 100 + 1)


def birth_year(dates: str, birth_val: str) -> int | None:
    from _historical_periods import anchor_year, extract_years

    combined = f"{dates} {birth_val}".strip()
    if not combined:
        return None
    years = extract_years(combined)
    return anchor_year(combined, years)


def parse_profile(path: Path, category: str, *, en: bool) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    name_m = RE_NAME.search(text)
    if not name_m:
        return None
    name = html.unescape(name_m.group(1).strip())
    dates = html.unescape(RE_DATES.search(text).group(1).strip()) if RE_DATES.search(text) else ""
    short_m = RE_SHORT.search(text)
    summary = html.unescape(short_m.group(1).strip()) if short_m else ""
    emoji_m = RE_EMOJI.search(text)
    emoji = html.unescape(emoji_m.group(1).strip()) if emoji_m else "⭐"
    country = (
        html.unescape(RE_GOLD.search(text).group(1).strip()) if RE_GOLD.search(text) else ""
    )
    field_raw = (
        html.unescape(RE_FIELD.search(text).group(1).strip()) if RE_FIELD.search(text) else ""
    )
    birth_val = (
        html.unescape(RE_BIRTH.search(text).group(1).strip())
        if RE_BIRTH.search(text)
        else ""
    )
    slug = path.stem
    href = f"prominent_figures/{category}/{slug}.html"
    by = birth_year(dates, birth_val)
    period = (
        infer_pf_period_en(dates, birth_val, by)
        if en
        else infer_pf_period_az(dates, birth_val, by)
    )
    return {
        "id": slug,
        "name": name,
        "dates": dates,
        "summary": summary,
        "emoji": emoji,
        "country": country,
        "field": field_raw,
        "region": "",
        "period": period,
        "category": category,
        "categoryLabel": CATEGORY_LABEL_EN[category] if en else CATEGORY_LABELS[category],
        "href": href,
        "birthYear": by,
    }


def collect_rows(figures_root: Path, *, en: bool) -> list[dict]:
    rows: list[dict] = []
    for category in ("azturk", "world"):
        folder = figures_root / category
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.html")):
            if path.name == "hazirlanir.html" or path.stem.endswith("_EN"):
                continue
            row = parse_profile(path, category, en=en)
            if row:
                rows.append(row)
    rows.sort(key=lambda r: r["name"].casefold())
    return rows


def write_catalog(rows: list[dict], var_name: str, out_path: Path) -> None:
    payload = json.dumps(rows, ensure_ascii=False, indent=2)
    out_path.write_text(f"window.{var_name} = {payload};\n", encoding="utf-8", newline="\n")


def load_old_en() -> dict[str, str]:
    if not OUT_EN.exists():
        return {}
    text = OUT_EN.read_text(encoding="utf-8")
    m = re.search(r"=\s*(\[.*\])\s*;", text, re.S)
    rows = json.loads(m.group(1))
    return {row["id"]: row.get("period", "") for row in rows}


def main() -> int:
    old = load_old_en()
    az_rows = collect_rows(FIGURES_ROOT_AZ, en=False)
    en_rows = collect_rows(FIGURES_ROOT_EN, en=True)
    write_catalog(az_rows, "PROMINENT_FIGURES_CATALOG", OUT_AZ)
    write_catalog(en_rows, "PROMINENT_FIGURES_CATALOG_EN", OUT_EN)

    changes = []
    for row in en_rows:
        prev = old.get(row["id"], "")
        if prev != row["period"]:
            changes.append((row["name"], row["id"], prev, row["period"]))

    print(f"Wrote {len(az_rows)} AZ + {len(en_rows)} EN profiles")
    print(f"Period changes: {len(changes)}")
    for name, slug, prev, new in sorted(changes, key=lambda x: x[0].casefold()):
        print(f"- {name} ({slug}): {prev or '(empty)'} -> {new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
