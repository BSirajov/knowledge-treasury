#!/usr/bin/env python3
"""Fetch candidate free-licensed invention icons from Wikimedia Commons into images/temp."""
from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMP = ROOT / "images" / "temp"
MANIFEST = TEMP / "candidate-images-manifest.json"

# slug -> (search query, preferred filename)
CANDIDATES: dict[str, tuple[str, str]] = {
    "controlled-use-of-fire": ("controlled fire prehistoric campfire 3d render", "controlled-use-of-fire.png"),
    "agriculture-and-domestication": ("agriculture domestication neolithic farming 3d", "agriculture-and-domestication.png"),
    "the-wheel": ("ancient wheel invention pottery wheel 3d render", "the-wheel.png"),
    "writing-systems": ("cuneiform writing tablet ancient 3d", "writing-systems.png"),
    "mathematics-and-the-concept-of-zero": ("mathematics zero numbers 3d illustration", "mathematics-and-the-concept-of-zero.png"),
    "paper": ("paper making ancient china 3d render", "paper.png"),
    "the-compass": ("magnetic compass navigation 3d render", "the-compass.png"),
    "gunpowder": ("gunpowder black powder 3d illustration", "gunpowder.png"),
    "the-printing-press": ("Gutenberg printing press 3d render", "the-printing-press.png"),
    "the-scientific-method": ("scientific method laboratory experiment 3d", "the-scientific-method.png"),
    "the-telescope": ("optical telescope astronomy 3d render", "the-telescope.png"),
    "the-microscope": ("optical microscope science 3d render", "the-microscope.png"),
    "newtonian-mechanics": ("Isaac Newton gravity apple mechanics 3d", "newtonian-mechanics.png"),
    "steam-engine": ("steam engine locomotive industrial 3d render", "steam-engine.png"),
    "electricity-generation-and-distribution": ("electric power generation grid 3d", "electricity-generation-and-distribution.png"),
    "electromagnetism": ("electromagnetism magnetic field 3d illustration", "electromagnetism.png"),
    "internal-combustion-engine": ("internal combustion engine piston 3d render", "internal-combustion-engine.png"),
    "automobile": ("early automobile vintage car 3d render", "automobile.png"),
    "airplane": ("airplane aviation aircraft 3d render", "airplane.png"),
    "refrigeration": ("refrigerator refrigeration cooling 3d render", "refrigeration.png"),
    "vaccination": ("vaccination syringe immunization 3d render", "vaccination.png"),
    "antibiotics": ("penicillin antibiotics medicine 3d render", "antibiotics.png"),
    "germ-theory-of-disease": ("bacteria germ theory microorganism 3d", "germ-theory-of-disease.png"),
    "anaesthesia": ("anaesthesia ether medical surgery 3d", "anaesthesia.png"),
    "x-rays-and-medical-imaging": ("x-ray medical imaging radiography 3d", "x-rays-and-medical-imaging.png"),
    "sanitation-and-clean-water-systems": ("clean water sanitation plumbing 3d", "sanitation-and-clean-water-systems.png"),
    "dna-structure-and-molecular-genetics": ("DNA double helix molecular 3d render", "dna-structure-and-molecular-genetics.png"),
    "human-genome-sequencing": ("human genome sequencing DNA 3d", "human-genome-sequencing.png"),
    "crispr-gene-editing": ("CRISPR Cas9 gene editing 3d render", "crispr-gene-editing.png"),
    "the-periodic-table": ("periodic table elements 3d render", "the-periodic-table.png"),
    "quantum-mechanics": ("quantum mechanics atom orbital 3d render", "quantum-mechanics.png"),
    "theory-of-relativity": ("theory of relativity spacetime black hole 3d", "theory-of-relativity.png"),
    "nuclear-energy-and-nuclear-science": ("nuclear energy atom fission 3d render", "nuclear-energy-and-nuclear-science.png"),
    "plastics-and-synthetic-materials": ("plastic polymer molecules 3d render", "plastics-and-synthetic-materials.png"),
    "fertilisers-and-modern-agricultural-chemistry": ("fertilizer agriculture nitrogen 3d", "fertilisers-and-modern-agricultural-chemistry.png"),
    "artificial-intelligence": ("artificial intelligence neural network 3d render", "artificial-intelligence.png"),
    "renewable-energy-technologies": ("renewable energy solar wind turbine 3d", "renewable-energy-technologies.png"),
    "battery-technology": ("lithium ion battery technology 3d render", "battery-technology.png"),
    "electric-vehicles": ("electric vehicle car charging 3d render", "electric-vehicles.png"),
    "robotics": ("industrial robot arm automation 3d render", "robotics.png"),
    "3d-printing-additive-manufacturing": ("3d printing additive manufacturing 3d render", "3d-printing-additive-manufacturing.png"),
    "blockchain": ("blockchain distributed ledger 3d illustration", "blockchain.png"),
}

ALLOWED_LICENSE_SNIPPETS = (
    "public domain",
    "cc0",
    "cc-by-sa",
    "cc-by",
    "pd-us",
    "pd-old",
    "pd-self",
    "pd-art",
    "pd-ineligible",
    "cc pd",
)

USER_AGENT = "KnowledgeTreasuryBot/1.0 (image research; contact: info@bilik-xezinesi.az)"


def api_get(params: dict) -> dict:
    base = "https://commons.wikimedia.org/w/api.php"
    params = {**params, "format": "json"}
    url = base + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def meta_value(meta: dict, key: str) -> str:
    val = meta.get(key, "")
    if isinstance(val, dict):
        val = val.get("value", "")
    return re.sub(r"<[^>]+>", "", str(val)).strip()


def license_ok(meta: dict) -> bool:
    blob = " ".join(meta_value(meta, k) for k in ("LicenseShortName", "UsageTerms", "License")).lower()
    return any(s in blob for s in ALLOWED_LICENSE_SNIPPETS)


def extract_license(meta: dict) -> str:
    for key in ("LicenseShortName", "UsageTerms", "License"):
        val = meta_value(meta, key)
        if val:
            return val
    return "Unknown — verify on Wikimedia Commons"


def extract_artist(meta: dict) -> str:
    return meta_value(meta, "Artist") or "Unknown"


def search_openverse(query: str, limit: int = 12) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "q": query,
            "page_size": str(limit),
            "license": "cc0,pdm,by,by-sa",
        }
    )
    url = f"https://api.openverse.org/v1/images/?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    results = []
    for item in data.get("results", []):
        w = int(item.get("width") or 0)
        h = int(item.get("height") or 0)
        if w < 400 or h < 400:
            continue
        license_name = (item.get("license") or "").upper()
        license_version = item.get("license_version") or ""
        results.append(
            {
                "title": item.get("title") or str(item.get("id")),
                "page_url": item.get("foreign_landing_url") or item.get("url"),
                "download_url": item.get("url"),
                "full_url": item.get("url"),
                "width": w,
                "height": h,
                "license": f"{license_name} {license_version}".strip(),
                "artist": item.get("creator") or item.get("source") or "Unknown",
                "mime": "image/jpeg",
                "source": "Openverse",
            }
        )
    results.sort(key=lambda r: min(r["width"], r["height"]), reverse=True)
    return results


def search_commons(query: str, limit: int = 15) -> list[dict]:
    data = api_get(
        {
            "action": "query",
            "generator": "search",
            "gsrsearch": f"filetype:bitmap {query}",
            "gsrnamespace": 6,
            "gsrlimit": str(limit),
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|mime|size",
            "iiurlwidth": "1024",
        }
    )
    pages = data.get("query", {}).get("pages", {})
    results = []
    for page in pages.values():
        infos = page.get("imageinfo") or []
        if not infos:
            continue
        info = infos[0]
        meta = info.get("extmetadata") or {}
        mime = info.get("mime", "")
        if mime not in ("image/png", "image/jpeg", "image/webp"):
            continue
        if not license_ok(meta):
            continue
        width = int(info.get("width") or 0)
        height = int(info.get("height") or 0)
        if width < 400 or height < 400:
            continue
        title = page.get("title", "")
        results.append(
            {
                "title": title,
                "page_url": f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
                "download_url": info.get("thumburl") or info.get("url"),
                "full_url": info.get("url"),
                "width": width,
                "height": height,
                "license": extract_license(meta),
                "artist": extract_artist(meta),
                "mime": mime,
                "source": "Wikimedia Commons",
            }
        )
    results.sort(key=lambda r: min(r["width"], r["height"]), reverse=True)
    return results


def find_image(query: str) -> list[dict]:
    hits = search_commons(query)
    if hits:
        return hits
    short = " ".join(query.split()[:4])
    hits = search_commons(short)
    if hits:
        return hits
    return search_openverse(query)


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    dest.write_bytes(data)


def main() -> None:
    TEMP.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    failures: list[dict] = []

    for slug, (query, filename) in CANDIDATES.items():
        print(f"Searching: {slug} ...")
        hits = find_image(query)
        if not hits:
            failures.append({"slug": slug, "query": query, "error": "No suitable free image found"})
            print("  FAILED")
            continue
        hit = hits[0]
        dest = TEMP / filename
        try:
            download(hit["download_url"], dest)
            entry = {
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
            }
            manifest.append(entry)
            print(f"  OK -> {filename} ({hit['license']})")
        except Exception as exc:  # noqa: BLE001
            failures.append({"slug": slug, "query": query, "error": str(exc)})
            print(f"  ERROR: {exc}")
        time.sleep(0.4)

    output = {"candidates": manifest, "failures": failures}
    MANIFEST.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"\nSaved {len(manifest)} images to {TEMP}")
    print(f"Failures: {len(failures)}")
    print(f"Manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
