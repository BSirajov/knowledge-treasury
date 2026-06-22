#!/usr/bin/env python3
"""Download 5 remaining temp PNGs and rebuild manifest metadata for all temp candidates."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMP = ROOT / "images" / "temp"
HTML = ROOT / "en" / "major_scientific_inventions.html"
MANIFEST = TEMP / "candidate-images-manifest.json"
USER_AGENT = "KnowledgeTreasuryBot/1.0 (image research; contact: info@bilik-xezinesi.az)"

REMAINING = {
    "gunpowder": "File:2023 Czarny proch Vesuvit LC (1).jpg",
    "the-printing-press": "File:Printing press 05.jpg",
    "refrigeration": "File:LG refrigerator interior.jpg",
    "vaccination": "File:Pravaz syringe Wellcome L0033875.jpg",
    "fertilisers-and-modern-agricultural-chemistry": "File:Ammonium nitrate 33,5 EC-fertilizer by Borealis.jpg",
}

# Load find_image + CANDIDATES from fetch script
spec = importlib.util.spec_from_file_location(
    "fetch", ROOT / "helpers" / "_fetch_invention_candidates.py"
)
fetch = importlib.util.module_from_spec(spec)
sys.modules["fetch"] = fetch
spec.loader.exec_module(fetch)


def api_get(params: dict) -> dict:
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({**params, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def meta_value(meta: dict, key: str) -> str:
    val = meta.get(key, "")
    if isinstance(val, dict):
        val = val.get("value", "")
    return re.sub(r"<[^>]+>", "", str(val)).strip()


def resolve_file(title: str) -> dict | None:
    data = api_get(
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|mime",
            "iiurlwidth": "1280",
        }
    )
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        if "missing" in page:
            return None
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata") or {}
        return {
            "wikimedia_file": title,
            "source_url": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
            "download_url": info.get("thumburl") or info.get("url"),
            "license": meta_value(meta, "LicenseShortName") or meta_value(meta, "UsageTerms") or "Verify on Commons",
            "artist": meta_value(meta, "Artist") or "Unknown",
        }
    return None


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def parse_sections() -> dict[str, str]:
    text = HTML.read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    for m in re.finditer(
        r'id="([^"]+)"[^>]*data-search="([^"]+)"',
        text,
    ):
        slug, data = m.group(1), m.group(2)
        num_name = data.split(" Period:")[0].strip()
        if re.match(r"^\d+\.\d+\s", num_name):
            sections[slug] = num_name
    return sections


def main() -> None:
    TEMP.mkdir(parents=True, exist_ok=True)
    sections = parse_sections()

    # Download remaining 5 with curated Commons files
    curated_meta: dict[str, dict] = {}
    for slug, title in REMAINING.items():
        dest = TEMP / f"{slug}.png"
        print(f"Downloading {slug} from {title}...")
        info = resolve_file(title)
        time.sleep(3)
        if not info or not info.get("download_url"):
            print("  FAILED")
            continue
        download(info["download_url"], dest)
        curated_meta[slug] = info
        print(f"  OK -> {dest.name}")
        time.sleep(3)

    # Preserve manually curated entries from existing manifest when available
    preserved: dict[str, dict] = {}
    if MANIFEST.exists():
        old = json.loads(MANIFEST.read_text(encoding="utf-8"))
        for c in old.get("candidates", []):
            sid = c.get("section_id")
            if sid:
                preserved[sid] = c

    candidates = []
    failures = []

    for slug, (query, filename) in fetch.CANDIDATES.items():
        section = sections.get(slug, slug)
        dest = TEMP / filename
        if not dest.exists():
            failures.append(
                {
                    "section": section,
                    "section_id": slug,
                    "filename": filename,
                    "error": "No candidate file in images/temp",
                }
            )
            continue

        if slug in curated_meta:
            info = curated_meta[slug]
            entry = {
                "section": section,
                "section_id": slug,
                "placeholder_for": filename,
                "saved_as": f"images/temp/{filename}",
                "source_url": info["source_url"],
                "download_url": info["download_url"],
                "license": info["license"],
                "artist": info["artist"],
                "wikimedia_file": info["wikimedia_file"],
                "search_query": query,
                "source_site": "Wikimedia Commons (curated pick)",
            }
        elif slug in preserved and preserved[slug].get("source_url"):
            entry = {**preserved[slug], "section": section, "placeholder_for": filename, "saved_as": f"images/temp/{filename}"}
        else:
            print(f"Metadata lookup: {slug}...")
            hits = fetch.find_image(query)
            time.sleep(1.5)
            if not hits:
                failures.append(
                    {
                        "section": section,
                        "section_id": slug,
                        "filename": filename,
                        "error": "File present but source metadata not found",
                    }
                )
                continue
            hit = hits[0]
            entry = {
                "section": section,
                "section_id": slug,
                "placeholder_for": filename,
                "saved_as": f"images/temp/{filename}",
                "source_url": hit["page_url"],
                "download_url": hit["download_url"],
                "license": hit["license"],
                "artist": hit["artist"],
                "dimensions": f"{hit['width']}x{hit['height']}",
                "search_query": query,
                "source_site": hit.get("source", "Wikimedia Commons"),
                "note": "Auto-selected via search; verify visual fit (prefer 3D-style consistency).",
            }

        candidates.append(entry)

    out = {
        "candidates": sorted(candidates, key=lambda c: c["section"]),
        "failures": failures,
        "total_files": len(list(TEMP.glob("*.png"))),
    }
    MANIFEST.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nManifest: {len(candidates)} entries, {len(failures)} failures, {out['total_files']} PNG files")


if __name__ == "__main__":
    main()
