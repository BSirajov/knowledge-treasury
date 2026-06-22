#!/usr/bin/env python3
"""Audit and rebuild historical period classifications across catalogues."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from _build_prominent_figures_catalog import (
    CATEGORY_LABELS,
    CATEGORY_LABEL_EN,
    collect_rows,
    write_catalog,
)
from _historical_periods import (
    PERIOD_LABELS_EN,
    infer_period_slug,
    infer_pf_period_az,
    infer_pf_period_en,
)
from _inventions_catalog_filters import infer_period
from _paths import ROOT

OUT_AZ = ROOT / "js" / "prominent-figures-catalog-data.js"
OUT_EN = ROOT / "js" / "prominent-figures-catalog-data-en.js"


def load_pf_rows(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"=\s*(\[.*\])\s*;", text, re.S)
    return json.loads(m.group(1))


def audit_inventions() -> list[dict]:
    html = (ROOT / "en" / "major_scientific_inventions.html").read_text(encoding="utf-8")
    entries = re.findall(
        r'<article class="inventions-entry" id="([^"]+)"[^>]*>'
        r'.*?<p class="inventions-entry-meta">Period:\s*([^<]+)</p>',
        html,
        re.S,
    )
    changes: list[dict] = []
    for slug, meta in entries:
        old = infer_period_slug("", [], slug=slug)  # placeholder
        # Old logic simulation: min-year broken classifier
        from _historical_periods import extract_years, anchor_year, slug_from_year

        years = extract_years(meta)
        old_slug = "modern"
        if years:
            old_slug = slug_from_year(min(years)) if False else infer_period_slug(f"Period: {meta}", [], slug=None)
        # get truly old from html research if present
        new = infer_period(f"Period: {meta}", [], slug=slug)
        # read old from research html data-period if available
        changes.append(
            {
                "type": "invention",
                "id": slug,
                "meta": meta[:80],
                "new": new,
                "new_label": PERIOD_LABELS_EN[new],
            }
        )
    return changes


def rebuild_pf_catalog() -> list[dict]:
    old_en = load_pf_rows(OUT_EN) if OUT_EN.exists() else []
    old_by_id = {row["id"]: row.get("period", "") for row in old_en}

    az_rows = collect_rows(ROOT / "az" / "prominent_figures", CATEGORY_LABELS, en=False)
    write_catalog(az_rows, "PROMINENT_FIGURES_CATALOG", OUT_AZ)

    en_rows = collect_rows(ROOT / "en" / "prominent_figures", CATEGORY_LABEL_EN, en=True)
    write_catalog(en_rows, "PROMINENT_FIGURES_CATALOG_EN", OUT_EN)

    changes: list[dict] = []
    for row in en_rows:
        old = old_by_id.get(row["id"], "")
        new = row.get("period", "")
        if old != new:
            changes.append(
                {
                    "type": "prominent_figure",
                    "id": row["id"],
                    "name": row.get("name", ""),
                    "old": old,
                    "new": new,
                }
            )
    return changes


def main() -> int:
    pf_changes = rebuild_pf_catalog()

    try:
        from _build_inventions_research_page import main as build_research

        build_research()
        research_built = True
    except Exception as exc:  # noqa: BLE001
        print(f"Research page rebuild skipped: {exc}")
        research_built = False

    print("\n=== Prominent figures period changes ===")
    for item in sorted(pf_changes, key=lambda x: x["name"].casefold()):
        print(f"- {item['name']} ({item['id']}): {item['old'] or '(empty)'} -> {item['new']}")

    print(f"\nTotal PF changes: {len(pf_changes)}")
    print(f"Research page rebuilt: {research_built}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
