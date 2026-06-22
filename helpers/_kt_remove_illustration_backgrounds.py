#!/usr/bin/env python3
"""Remove flat illustration backgrounds so PNGs blend with their parent frame."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import binary_propagation

from _paths import ROOT

SKIP_DIRS = {".git", "preview", "documents", "archive", "orijinal", "temp", "forum-sessions"}
SKIP_NAMES = {
    "kt-logo.png",
    "kt-logo 1.png",
    "kt-logo 2.png",
    "kt-favicon.png",
    "kt-logo-192.png",
    "apple-touch-icon.png",
}

TARGET_ROOTS = (
    ROOT / "images" / "icons",
    ROOT / "images" / "inventions",
    ROOT / "images" / "inventions" / "icons",
)

BG_TOL = 32
WHITE_MIN = 238


def corner_background(rgb: np.ndarray) -> np.ndarray:
    h, w = rgb.shape[:2]
    pad_y = min(4, max(1, h // 20))
    pad_x = min(4, max(1, w // 20))
    samples = np.concatenate(
        [
            rgb[0:pad_y, 0:pad_x].reshape(-1, 3),
            rgb[0:pad_y, w - pad_x : w].reshape(-1, 3),
            rgb[h - pad_y : h, 0:pad_x].reshape(-1, 3),
            rgb[h - pad_y : h, w - pad_x : w].reshape(-1, 3),
        ],
        axis=0,
    )
    return np.median(samples, axis=0).astype(np.int16)


def background_mask(rgb: np.ndarray, bg: np.ndarray) -> np.ndarray:
    diff = np.abs(rgb.astype(np.int16) - bg).sum(axis=2)
    similar = diff <= BG_TOL
    white = (
        (rgb[:, :, 0] >= WHITE_MIN)
        & (rgb[:, :, 1] >= WHITE_MIN)
        & (rgb[:, :, 2] >= WHITE_MIN)
    )
    candidate = similar | white
    h, w = candidate.shape
    seeds = np.zeros_like(candidate, dtype=bool)
    seeds[0, :] = candidate[0, :]
    seeds[-1, :] = candidate[-1, :]
    seeds[:, 0] = candidate[:, 0]
    seeds[:, -1] = candidate[:, -1]
    return binary_propagation(seeds, mask=candidate)


def remove_background(path: Path) -> bool:
    with Image.open(path) as image:
        rgba = np.array(image.convert("RGBA"))
    rgb = rgba[:, :, :3]
    alpha = rgba[:, :, 3]
    if alpha.min() == 0 and alpha.max() == 0:
        return False

    bg = corner_background(rgb)
    mask = background_mask(rgb, bg)
    if not mask.any():
        return False

    new_alpha = alpha.copy()
    new_alpha[mask] = 0
    rgba[:, :, 3] = new_alpha

    # Drop fully transparent margins.
    ys, xs = np.where(new_alpha > 8)
    if len(xs) == 0:
        return False
    top, bottom = int(ys.min()), int(ys.max()) + 1
    left, right = int(xs.min()), int(xs.max()) + 1
    cropped = rgba[top:bottom, left:right]
    Image.fromarray(cropped).save(path, format="PNG", optimize=True)
    return True


def should_process(path: Path) -> bool:
    if path.suffix.lower() != ".png":
        return False
    if path.name in SKIP_NAMES:
        return False
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.stem.endswith("-artefact") or path.stem.endswith("-artifact"):
        return False
    return True


def iter_targets() -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for root in TARGET_ROOTS:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.png")):
            resolved = path.resolve()
            if resolved in seen or not should_process(path):
                continue
            seen.add(resolved)
            paths.append(path)
    return paths


def main() -> None:
    updated = 0
    for path in iter_targets():
        if remove_background(path):
            updated += 1
            print(path.relative_to(ROOT))
    print(f"Transparent backgrounds applied to {updated} illustration(s)")


if __name__ == "__main__":
    main()
