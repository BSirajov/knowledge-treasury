#!/usr/bin/env python3
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from _historical_periods import PERIOD_LABELS_EN
from _paths import ROOT

OLD_LABELS = {
    "prehistory": "Prehistory",
    "ancient": "Ancient",
    "medieval": "Medieval",
    "early-modern": "Early modern",
    "industrial": "19th century",
    "modern": "20th century",
    "contemporary": "21st century",
}


def audit(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    entries = re.findall(
        r'id="([^"]+)"[^>]*data-period="([^"]+)"[^>]*data-number="([^"]+)"',
        html,
    )
    print(f"\n{path.name} ({len(entries)} entries)")
    print("Distribution:", Counter(p for _, p, _ in entries))
    for slug, period, num in sorted(entries, key=lambda x: x[2]):
        label = PERIOD_LABELS_EN.get(period, period)
        print(f"  {num} {slug}: {label} ({period})")


if __name__ == "__main__":
    audit(ROOT / "en" / "scientific_inventions_research.html")
