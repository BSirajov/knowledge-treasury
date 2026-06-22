#!/usr/bin/env python3
"""Re-verify suspect links with browser-like GET + redirect following."""
from __future__ import annotations

import json
import re
import ssl
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "helpers" / "_invention_link_report.json"
OUT = ROOT / "helpers" / "_invention_link_reverify.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch(url: str) -> dict:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
            return {
                "url": url,
                "status": resp.status,
                "final_url": resp.geturl(),
                "ok": 200 <= resp.status < 400,
                "error": None,
            }
    except urllib.error.HTTPError as exc:
        return {
            "url": url,
            "status": exc.code,
            "final_url": exc.geturl() if hasattr(exc, "geturl") else url,
            "ok": False,
            "error": str(exc),
        }
    except Exception as exc:
        return {
            "url": url,
            "status": None,
            "final_url": url,
            "ok": False,
            "error": str(exc),
        }


def main() -> None:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    skip = (
        "bilik-xezinesi.az",
        "fonts.googleapis.com",
        "fonts.gstatic.com",
    )
    urls = [
        item["url"]
        for item in data["broken"]
        if not any(s in item["url"] for s in skip)
    ]
    results = []
    for url in urls:
        print(url, flush=True)
        results.append(fetch(url))

    still_broken = [r for r in results if not r["ok"]]
    OUT.write_text(
        json.dumps({"checked": len(urls), "still_broken": still_broken, "all": results}, indent=2),
        encoding="utf-8",
    )
    print(f"\nStill broken: {len(still_broken)} / {len(urls)}")
    for item in still_broken:
        print(f"  [{item.get('status')}] {item['url']}")


if __name__ == "__main__":
    main()
