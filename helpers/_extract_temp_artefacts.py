#!/usr/bin/env python3
"""Crop invention artefact illustrations from temp infographic PNGs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _clean_temp_artefacts import remove_text_fragments

ROOT = Path(__file__).resolve().parent.parent
TEMP = ROOT / "images" / "temp"
MANIFEST = TEMP / "infographics-manifest.json"
OUT_MANIFEST = TEMP / "artefacts-manifest.json"

CARD_W, CARD_H = 857, 308
HEADER_H = 72
# Full left illustration panel on the 857×308 card (text column begins ~x198).
PANEL_BOX = (12, HEADER_H, 198, 304)
BG = np.array([245, 251, 255], dtype=np.int16)
PAD = 8


def scale_box(size: tuple[int, int], box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    w, h = size
    if (w, h) == (CARD_W, CARD_H):
        return box
    return (
        int(box[0] * w / CARD_W),
        int(box[1] * h / CARD_H),
        int(box[2] * w / CARD_W),
        int(box[3] * h / CARD_H),
    )


def illustration_crop_box(image: Image.Image) -> tuple[int, int, int, int]:
    """Return a crop box for the full illustration, trimming only empty margins."""
    panel = scale_box(image.size, PANEL_BOX)
    rgb = np.array(image.convert("RGB"))
    x1, y1, x2, y2 = panel
    region = rgb[y1:y2, x1:x2]
    diff = np.abs(region.astype(np.int16) - BG).sum(axis=2)
    mask = diff > 25
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return panel

    # Keep full panel width so wide icons are never clipped; trim top/bottom only.
    top = max(y1, y1 + int(ys.min()) - PAD)
    bottom = min(rgb.shape[0], y1 + int(ys.max()) + PAD + 1)
    return (x1, top, x2, bottom)


def ensure_manifest() -> list[dict]:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))

    items: list[dict] = []
    for index, path in enumerate(sorted(TEMP.glob("*.png")), start=1):
        if path.stem.endswith("-artefact") or path.stem.endswith("-test"):
            continue
        if "-artefact-" in path.stem:
            continue
        slug = path.stem
        title = slug.replace("-", " ").title()
        items.append(
            {
                "index": index,
                "title": title,
                "slug": slug,
                "file": f"images/temp/{path.name}",
            }
        )

    MANIFEST.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return items


def main() -> None:
    items = ensure_manifest()
    artefacts: list[dict] = []

    for item in items:
        slug = item["slug"]
        src = TEMP / f"{slug}.png"
        if not src.exists():
            raise FileNotFoundError(src)

        image = Image.open(src).convert("RGBA")
        box = illustration_crop_box(image)
        crop = image.crop(box)
        crop = remove_text_fragments(crop)
        dest = TEMP / f"{slug}-artefact.png"
        crop.save(dest, format="PNG", optimize=True)

        artefacts.append(
            {
                "index": item["index"],
                "title": item["title"],
                "slug": slug,
                "source_infographic": f"images/temp/{slug}.png",
                "file": f"images/temp/{slug}-artefact.png",
                "size": list(crop.size),
                "crop_box": list(box),
                "text_removed": True,
            }
        )

    OUT_MANIFEST.write_text(
        json.dumps(artefacts, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(artefacts)} artefacts to {TEMP.relative_to(ROOT)}")
    print(f"Manifest: {OUT_MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
