#!/usr/bin/env python3
"""Generate AZ/EN prominent figure pages from _new_prominent_figures_data.py and rebuild catalog."""
from __future__ import annotations

import subprocess
import sys

from _new_prominent_figures_data import FIGURES as FIGURES_BATCH1
from _prominent_figures_batch2_data import FIGURES as FIGURES_BATCH2
from _prominent_figures_batch3_data import FIGURES as FIGURES_BATCH3

FIGURES = FIGURES_BATCH1 + FIGURES_BATCH2 + FIGURES_BATCH3
from _profile_page_builder import write_profile
from _paths import ROOT


def main() -> None:
    written = 0
    for fig in FIGURES:
        slug = fig["slug"]
        for lang in ("az", "en"):
            path = write_profile(fig, lang)
            print(f"Wrote {path.relative_to(ROOT)}")
            written += 1
    print(f"\nGenerated {written} profile pages ({len(FIGURES)} figures × 2 languages).")

    print("\nRebuilding catalog…")
    subprocess.run(
        [sys.executable, str(ROOT / "helpers" / "_build_prominent_figures_catalog.py")],
        check=True,
        cwd=str(ROOT / "helpers"),
    )

    print("\nRebuilding search index…")
    subprocess.run(
        [sys.executable, str(ROOT / "helpers" / "_build_search_index.py")],
        check=True,
        cwd=str(ROOT / "helpers"),
    )

    print("\nDone.")


if __name__ == "__main__":
    main()
