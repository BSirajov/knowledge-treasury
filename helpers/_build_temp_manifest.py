#!/usr/bin/env python3
"""Download remaining temp candidates and rebuild full manifest from Wikimedia metadata."""
from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMP = ROOT / "images" / "temp"
HTML = ROOT / "en" / "major_scientific_inventions.html"
MANIFEST = TEMP / "candidate-images-manifest.json"
USER_AGENT = "KnowledgeTreasuryBot/1.0 (image research; contact: info@bilik-xezinesi.az)"

# Remaining downloads that failed earlier
REMAINING = {
    "gunpowder": "File:2023 Czarny proch Vesuvit LC (1).jpg",
    "the-printing-press": "File:Printing press 05.jpg",
    "refrigeration": "File:LG refrigerator interior.jpg",
    "vaccination": "File:Pravaz syringe Wellcome L0033875.jpg",
    "fertilisers-and-modern-agricultural-chemistry": "File:Ammonium nitrate 33,5 EC-fertilizer by Borealis.jpg",
}


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
            "mime": info.get("mime", ""),
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
        r'<article class="inventions-entry" id="([^"]+)"[^>]*>.*?'
        r'<span class="inventions-entry-num"[^>]*>([^<]+)</span>'
        r'<span class="inventions-entry-name">([^<]+)</span>',
        text,
        re.DOTALL,
    ):
        slug, num, name = m.group(1), m.group(2).strip(), m.group(3).strip()
        sections[slug] = f"{num} {name}"
    return sections


def main() -> None:
    TEMP.mkdir(parents=True, exist_ok=True)
    sections = parse_sections()

    # Download remaining 5
    for slug, title in REMAINING.items():
        dest = TEMP / f"{slug}.png"
        print(f"Resolving {slug}...")
        info = resolve_file(title)
        time.sleep(3)
        if not info or not info.get("download_url"):
            print(f"  FAILED: {title}")
            continue
        print(f"  Downloading -> {dest.name}")
        download(info["download_url"], dest)
        time.sleep(3)

    # Build manifest for all PNGs in temp
    candidates = []
    failures = []
    for png in sorted(TEMP.glob("*.png")):
        slug = png.stem
        section = sections.get(slug, slug)
        placeholder = f"{slug}.png"

        # Try to find wikimedia metadata by searching manifest cache or re-query
        existing = None
        if MANIFEST.exists():
            old = json.loads(MANIFEST.read_text(encoding="utf-8"))
            for c in old.get("candidates", []):
                if c.get("section_id") == slug:
                    existing = c
                    break

        if existing and (TEMP / png.name).stat().st_size > 0:
            entry = {**existing, "saved_as": f"images/temp/{png.name}", "placeholder_for": placeholder}
            entry.setdefault("section", section)
            candidates.append(entry)
            continue

        # Search commons for file that was downloaded - use imageinfo from hash is hard; search by slug words
        query = slug.replace("-", " ")
        search = api_get(
            {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "srnamespace": "6",
                "srlimit": "1",
            }
        )
        time.sleep(2)
        hits = search.get("query", {}).get("search", [])
        if hits:
            title = hits[0]["title"]
            info = resolve_file(title)
            time.sleep(2)
            if info:
                candidates.append(
                    {
                        "section": section,
                        "section_id": slug,
                        "placeholder_for": placeholder,
                        "saved_as": f"images/temp/{png.name}",
                        "source_url": info["source_url"],
                        "download_url": info["download_url"],
                        "license": info["license"],
                        "artist": info["artist"],
                        "wikimedia_file": info["wikimedia_file"],
                        "note": "Auto-matched via Commons search; verify visual fit and topic relevance.",
                    }
                )
                continue

        failures.append({"section": section, "section_id": slug, "filename": png.name, "error": "Could not resolve metadata"})

    out = {"candidates": candidates, "failures": failures, "total_files": len(list(TEMP.glob("*.png")))}
    MANIFEST.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote manifest: {len(candidates)} candidates, {len(failures)} metadata failures, {out['total_files']} PNG files")


if __name__ == "__main__":
    main()
