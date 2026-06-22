#!/usr/bin/env python3
"""Strip right-panel illustrations outside section 6 via the page builder."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILDER = ROOT / "helpers" / "_build_inventions_page.py"


def main() -> None:
    subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
