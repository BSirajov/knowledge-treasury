#!/usr/bin/env python3
"""Remove text remnants from temp artefact illustration crops."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
TEMP = ROOT / "images" / "temp"
MANIFEST = TEMP / "artefacts-manifest.json"

BG = np.array([245, 251, 255], dtype=np.uint8)
BG_TOL = 25
MIN_ILLUSTRATION_AREA = 800
STRUCTURAL_MAX_X = 120


def sample_background(rgb: np.ndarray) -> np.ndarray:
    """Estimate card body background from low-traffic edge samples."""
    h, w = rgb.shape[:2]
    samples = np.concatenate(
        [
            rgb[2 : h // 3, 24:40].reshape(-1, 3),
            rgb[h // 2 :, 24:40].reshape(-1, 3),
            rgb[h - 4 : h, 40 : w // 2].reshape(-1, 3),
        ],
        axis=0,
    )
    diff = np.abs(samples.astype(np.int16) - BG.astype(np.int16)).sum(axis=1)
    quiet = samples[diff <= BG_TOL]
    if len(quiet):
        return np.median(quiet, axis=0).astype(np.uint8)
    return BG.copy()


def remove_text_fragments(image: Image.Image) -> Image.Image:
    """Drop small right-side text blobs; fill with the card background color."""
    rgb = np.array(image.convert("RGB"))
    bg = sample_background(rgb)
    bg_i = bg.astype(np.int16)

    diff = np.abs(rgb.astype(np.int16) - bg_i).sum(axis=2)
    is_bg = diff <= BG_TOL
    foreground = ~is_bg

    labeled, count = ndimage.label(foreground)
    keep = np.zeros(foreground.shape, dtype=bool)

    for label in range(1, count + 1):
        component = labeled == label
        area = int(component.sum())
        xs = np.where(component)[1]
        centroid_x = float(xs.mean())
        if area >= MIN_ILLUSTRATION_AREA or centroid_x < STRUCTURAL_MAX_X:
            keep |= component

    out = rgb.copy()
    remove = foreground & ~keep
    out[remove] = bg

    # Soften one-pixel halos around removed text without touching illustration edges.
    halo = ndimage.binary_dilation(remove, iterations=1) & ~keep & ~is_bg
    halo_diff = np.abs(out.astype(np.int16) - bg_i).sum(axis=2)
    out[halo & (halo_diff <= 70)] = bg

    return Image.fromarray(out)


def main() -> None:
    paths = sorted(TEMP.glob("*-artefact.png"))
    if not paths:
        raise SystemExit(f"No artefact images found in {TEMP.relative_to(ROOT)}")

    cleaned: list[dict] = []
    for path in paths:
        image = Image.open(path)
        size = image.size
        cleaned_image = remove_text_fragments(image)
        if cleaned_image.size != size:
            raise RuntimeError(f"Size changed for {path.name}: {size} -> {cleaned_image.size}")
        cleaned_image.save(path, format="PNG", optimize=True)
        cleaned.append({"slug": path.stem.removesuffix("-artefact"), "file": f"images/temp/{path.name}"})

    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cleaned_slugs = {entry["slug"] for entry in cleaned}
        for entry in manifest:
            if entry.get("slug") in cleaned_slugs:
                entry["text_removed"] = True
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Cleaned {len(cleaned)} artefacts in {TEMP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
