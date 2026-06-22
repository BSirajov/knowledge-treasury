#!/usr/bin/env python3
"""Check external links in major_scientific_inventions.html."""
from __future__ import annotations

import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import ROOT
from _build_inventions_page import fix_url

HTML = ROOT / "en" / "major_scientific_inventions.html"
OUT = ROOT / "helpers" / "_invention_link_report.json"

USER_AGENT = "KnowledgeTreasury-LinkChecker/1.0 (+https://bilik-xezinesi.az)"
TIMEOUT = 20
SKIP_HOSTS = ("bilik-xezinesi.az", "fonts.googleapis.com", "fonts.gstatic.com")


def extract_urls(html: str) -> list[str]:
    urls = re.findall(r'href="(https?://[^"]+)"', html)
    fixed = []
    for url in urls:
        if any(host in url for host in SKIP_HOSTS):
            continue
        fixed_url = fix_url(url) or url
        fixed.append(fixed_url)
    return sorted(set(fixed))


def check_url(url: str) -> dict:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            return {
                "url": url,
                "status": resp.status,
                "final_url": resp.geturl(),
                "ok": 200 <= resp.status < 400,
                "error": None,
            }
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 405, 501):
            return check_url_get(url)
        return {
            "url": url,
            "status": exc.code,
            "final_url": exc.geturl() if hasattr(exc, "geturl") else url,
            "ok": False,
            "error": str(exc),
        }
    except Exception:
        return check_url_get(url)


def check_url_get(url: str) -> dict:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(
        url,
        method="GET",
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
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
    html = HTML.read_text(encoding="utf-8")
    urls = extract_urls(html)
    results = []
    broken = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url[:90]}...", flush=True)
        result = check_url(url)
        results.append(result)
        if not result["ok"]:
            broken.append(result)
        time.sleep(0.15)

    OUT.write_text(json.dumps({"total": len(urls), "broken": broken, "all": results}, indent=2), encoding="utf-8")
    print(f"\nTotal: {len(urls)} | Broken: {len(broken)} | Report: {OUT}")
    for item in broken:
        print(f"  FAIL [{item.get('status')}] {item['url']}")
        if item.get("error"):
            print(f"       {item['error'][:120]}")


if __name__ == "__main__":
    main()
