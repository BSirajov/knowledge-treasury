#!/usr/bin/env python3
"""Compare old 4-bucket PF periods with corrected taxonomy."""
from __future__ import annotations

import json
import re
from pathlib import Path

from _paths import ROOT

OUT = ROOT / "helpers" / "_pf_period_change_report.json"


def old_bucket(year: int | None, dates: str) -> str:
    lower = (dates or "").lower()
    if any(t in lower for t in ("bce", "bc", "e.ə", "ə.e", "legendary")):
        return "Antiquity"
    if year is None:
        return ""
    if year < 500:
        return "Antiquity"
    if year < 1500:
        return "Middle Ages"
    if year < 1800:
        return "Modern era"
    return "Contemporary era"


def main() -> None:
    text = (ROOT / "js" / "prominent-figures-catalog-data-en.js").read_text(encoding="utf-8")
    rows = json.loads(re.search(r"=\s*(\[.*\])\s*;", text, re.S).group(1))
    changes = []
    for row in rows:
        year = row.get("birthYear")
        old = old_bucket(year, row.get("dates", ""))
        new = row.get("period", "")
        if old != new:
            changes.append(
                {
                    "id": row["id"],
                    "name": row["name"],
                    "dates": row.get("dates", ""),
                    "old": old,
                    "new": new,
                }
            )
    OUT.write_text(json.dumps(changes, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(changes)} changes to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
