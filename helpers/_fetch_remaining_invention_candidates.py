#!/usr/bin/env python3
"""Resolve Wikimedia file titles to URLs and download with rate limiting."""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMP = ROOT / "images" / "temp"
MANIFEST = TEMP / "candidate-images-manifest.json"
USER_AGENT = "KnowledgeTreasuryBot/1.0 (image research; contact: info@bilik-xezinesi.az)"

# Remaining 12 missing placeholders -> exact Wikimedia file titles
REMAINING = [
    {
        "section": "1.1 Controlled Use of Fire",
        "section_id": "controlled-use-of-fire",
        "filename": "controlled-use-of-fire.png",
        "file_title": "File:Campfire icon (Pixabay 1345870).png",
    },
    {
        "section": "1.7 The Compass",
        "section_id": "the-compass",
        "filename": "the-compass.png",
        "file_title": "File:Compass.svg",
    },
    {
        "section": "1.8 Gunpowder",
        "section_id": "gunpowder",
        "filename": "gunpowder.png",
        "file_title": "File:Gunpowder.jpg",
    },
    {
        "section": "1.9 The Printing Press",
        "section_id": "the-printing-press",
        "filename": "the-printing-press.png",
        "file_title": "File:Gutenberg Bible, Lenox Copy, New York Public Library, 2009. Pic 2.jpg",
    },
    {
        "section": "3.7 Refrigeration",
        "section_id": "refrigeration",
        "filename": "refrigeration.png",
        "file_title": "File:Fridge interior.jpg",
    },
    {
        "section": "4.1 Vaccination",
        "section_id": "vaccination",
        "filename": "vaccination.png",
        "file_title": "File:COVID-19 vaccine administration in Sweden.jpg",
    },
    {
        "section": "4.2 Antibiotics",
        "section_id": "antibiotics",
        "filename": "antibiotics.png",
        "file_title": "File:Penicillin core.svg",
    },
    {
        "section": "4.3 Germ Theory of Disease",
        "section_id": "germ-theory-of-disease",
        "filename": "germ-theory-of-disease.png",
        "file_title": "File:EscherichiaColi NIAID.jpg",
    },
    {
        "section": "4.6 Sanitation and Clean Water Systems",
        "section_id": "sanitation-and-clean-water-systems",
        "filename": "sanitation-and-clean-water-systems.png",
        "file_title": "File:Drinking water.jpg",
    },
    {
        "section": "5.5 Plastics and Synthetic Materials",
        "section_id": "plastics-and-synthetic-materials",
        "filename": "plastics-and-synthetic-materials.png",
        "file_title": "File:Plastic pollution.jpg",
    },
    {
        "section": "5.6 Fertilisers and Modern Agricultural Chemistry",
        "section_id": "fertilisers-and-modern-agricultural-chemistry",
        "filename": "fertilisers-and-modern-agricultural-chemistry.png",
        "file_title": "File:Ammonium nitrate.jpg",
    },
    {
        "section": "7.7 Blockchain",
        "section_id": "blockchain",
        "filename": "blockchain.png",
        "file_title": "File:Blockchain.svg",
    },
]


def api_image(title: str) -> dict | None:
    params = {
        "action": "query",
        "titles": title,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|mime|size",
        "iiurlwidth": "1024",
        "format": "json",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        if "missing" in page:
            return None
        infos = page.get("imageinfo") or []
        if not infos:
            return None
        info = infos[0]
        meta = info.get("extmetadata") or {}

        def meta_val(key: str) -> str:
            val = meta.get(key, "")
            if isinstance(val, dict):
                val = val.get("value", "")
            return str(val).strip()

        return {
            "page_url": f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
            "download_url": info.get("thumburl") or info.get("url"),
            "license": meta_val("LicenseShortName") or meta_val("UsageTerms") or "See source page",
            "artist": meta_val("Artist") or "Unknown",
            "mime": info.get("mime", ""),
        }
    return None


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    TEMP.mkdir(parents=True, exist_ok=True)
    existing = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"candidates": [], "failures": []}
    added = []
    failures = []
    for item in REMAINING:
        print(item["filename"], "...")
        meta = api_image(item["file_title"])
        time.sleep(3)
        if not meta or not meta.get("download_url"):
            failures.append({**item, "error": "Could not resolve Wikimedia file"})
            continue
        dest = TEMP / item["filename"]
        try:
            download(meta["download_url"], dest)
            added.append(
                {
                    "section": item["section"],
                    "section_id": item["section_id"],
                    "placeholder_for": item["filename"],
                    "saved_as": f"images/temp/{item['filename']}",
                    "source_url": meta["page_url"],
                    "download_url": meta["download_url"],
                    "license": meta["license"],
                    "artist": meta["artist"],
                    "wikimedia_file": item["file_title"],
                }
            )
            print("  OK")
        except Exception as exc:  # noqa: BLE001
            failures.append({**item, "error": str(exc)})
            print(f"  FAIL {exc}")
        time.sleep(3)

    # merge with prior manifest entries (dedupe by filename)
    by_name = {c["placeholder_for"]: c for c in existing.get("candidates", [])}
    for c in added:
        by_name[c["placeholder_for"]] = c
    merged = {"candidates": sorted(by_name.values(), key=lambda x: x["section_id"]), "failures": failures}
    MANIFEST.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    print(f"Added {len(added)}; total candidates {len(merged['candidates'])}")


if __name__ == "__main__":
    main()
