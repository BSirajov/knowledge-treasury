#!/usr/bin/env python3
"""Summarise invention period corrections (broken min-year vs corrected taxonomy)."""
from __future__ import annotations

import re
from pathlib import Path

from _historical_periods import PERIOD_LABELS_EN, infer_period_slug
from _paths import ROOT


def broken_infer(meta: str, slug: str) -> str:
  # Old behaviour: min extracted year without overrides or anchor logic.
    import re as _re

    years: list[int] = []
    for m in _re.finditer(r"(\d{1,3}(?:,\d{3})*|\d+)\s*(BCE|BC|CE|AD)?", meta, _re.I):
        raw = m.group(1).replace(",", "")
        if not raw.isdigit():
            continue
        year = int(raw)
        era = (m.group(2) or "").upper()
        if era in {"BCE", "BC"}:
            year = -year
        years.append(year)
    if not years:
        return "modern"
    anchor = min(years)
    if anchor < -3000:
        return "prehistory"
    if anchor < 500:
        return "ancient"
    if anchor < 1500:
        return "medieval"
    if anchor < 1800:
        return "early-modern"
    if anchor < 1900:
        return "industrial"
    if anchor < 2000:
        return "modern"
    return "contemporary"


def main() -> None:
    html = (ROOT / "en" / "scientific_inventions_research.html").read_text(encoding="utf-8")
    entries = re.findall(
        r'data-number="([^"]+)"[^>]*\n\s*data-search="[^"]*Period: ([^|]+)',
        html,
    )
  # fallback parse
    if not entries:
        entries = []
        for m in re.finditer(
            r'data-number="([^"]+)".*?research-entry__meta">Period: ([^<]+)</p>',
            html,
            re.S,
        ):
            entries.append((m.group(1), m.group(2)))

    slug_entries = re.findall(
        r'id="([^"]+)"[^>]*data-period="([^"]+)"[^>]*data-number="([^"]+)"',
        html,
    )
    by_slug = {slug: (period, num) for slug, period, num in slug_entries}

    changes = []
    for slug, (new, num) in sorted(by_slug.items(), key=lambda x: x[1][1]):
        meta_m = re.search(
            rf'id="{re.escape(slug)}".*?Period: ([^<]+)</p>',
            html,
            re.S,
        )
        meta = meta_m.group(1) if meta_m else ""
        old = broken_infer(meta, slug)
        if old != new:
            changes.append(
                {
                    "num": num,
                    "slug": slug,
                    "old": PERIOD_LABELS_EN.get(old, OLD := old),
                    "new": PERIOD_LABELS_EN.get(new, new),
                }
            )

    print(f"Invention period corrections: {len(changes)}")
    for item in changes:
        print(f"- {item['num']} {item['slug']}: {item['old']} -> {item['new']}")


if __name__ == "__main__":
    main()
