#!/usr/bin/env python3
"""Re-extract invention icons and correct squeezed circular elements."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from _clean_invention_strips import CARD_H, CARD_W, TEXT_LEFT, extract_clean, trim_vertical_margins
from _paths import ROOT

ICONS_DIR = ROOT / "images" / "icons"
ICON_INDEX = ROOT / "helpers" / "_invention_icon_index.json"
BG = np.array([245, 249, 252], dtype=np.int16)

TARGET_SLUGS = (
    "gunpowder",
    "the-compass",
    "the-wheel",
    "x-rays-and-medical-imaging",
)

SLUG_FILE_ALIASES: dict[str, list[str]] = {
    "the-compass": ["compass"],
    "the-wheel": ["wheel"],
}

MAX_DIMENSION = 196
Y_SCALE_CLAMP = (0.55, 2.2)


def slug_output_paths(slug: str) -> list[Path]:
    paths: list[Path] = []
    if ICON_INDEX.exists():
        rel = json.loads(ICON_INDEX.read_text(encoding="utf-8")).get("icons", {}).get(slug, {}).get(
            "path"
        )
        if rel:
            paths.append(ROOT / rel)
    for alt in SLUG_FILE_ALIASES.get(slug, []):
        for match in ICONS_DIR.rglob(f"{alt}.png"):
            paths.append(match)
    if not paths:
        for match in ICONS_DIR.rglob(f"{slug}.png"):
            paths.append(match)
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen and path.exists():
            seen.add(resolved)
            unique.append(path)
    return unique


def remove_gold_strip(image: Image.Image) -> Image.Image:
    rgb = np.array(image.convert("RGB"))
    gold = (rgb[:, :, 0] > 165) & (rgb[:, :, 1] > 125) & (rgb[:, :, 2] < 105)
    left = 0
    for x in range(rgb.shape[1]):
        if gold[:, x].mean() > 0.25:
            left = x + 1
        elif left > 0:
            break
    if left <= 0:
        return image
    return image.crop((left, 0, image.width, image.height))


def trim_horizontal_margins(image: Image.Image, pad: int = 6) -> Image.Image:
    rgb = np.array(image.convert("RGB"))
    diff = np.abs(rgb.astype(np.int16) - BG).sum(axis=2)
    xs = np.where(diff > 18)[1]
    if len(xs) == 0:
        return image
    left = max(0, int(xs.min()) - pad)
    right = min(rgb.shape[1], int(xs.max()) + pad + 1)
    return image.crop((left, 0, right, image.height))


def prepare_source(slug: str) -> Image.Image:
    extracted = extract_clean(slug)
    if extracted is None:
        raise FileNotFoundError(f"No infograph source for {slug}")
    image = remove_gold_strip(extracted)
    image = trim_vertical_margins(image)
    image = trim_horizontal_margins(image)
    return image.convert("RGBA")


def content_center(alpha: np.ndarray) -> tuple[float, float]:
    ys, xs = np.where(alpha > 20)
    if len(xs) == 0:
        h, w = alpha.shape
        return w / 2, h / 2
    return (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2


def measure_y_scale(image: Image.Image, slug: str) -> float:
    arr = np.array(image.convert("RGBA"))
    gray = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGBA2GRAY)
    alpha = arr[:, :, 3] > 20
    if slug in {"the-compass", "the-wheel", "gunpowder"}:
        mask = (gray < 100) & alpha
        if mask.sum() < 120:
            mask = alpha
    else:
        mask = (gray < 90) & alpha
        if mask.sum() < 120:
            mask = alpha

    mask_u8 = mask.astype(np.uint8) * 255
    contours, _ = cv2.findContours(mask_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return 1.0

    contour = max(contours, key=cv2.contourArea)
    if len(contour) < 5:
        return 1.0

    (_, _), (axis_a, axis_b), angle = cv2.fitEllipse(contour)
    rad = np.deg2rad(angle)
    horiz = np.sqrt((axis_a * np.cos(rad) / 2) ** 2 + (axis_b * np.sin(rad) / 2) ** 2) * 2
    vert = np.sqrt((axis_a * np.sin(rad) / 2) ** 2 + (axis_b * np.cos(rad) / 2) ** 2) * 2
    if vert <= 0:
        return 1.0
    return float(horiz / vert)


def apply_y_scale(image: Image.Image, y_scale: float) -> Image.Image:
    rgba = image.convert("RGBA")
    w, h = rgba.size
    arr = np.array(rgba)
    _, cy = content_center(arr[:, :, 3])
    matrix = (1, 0, 0, 0, y_scale, cy * (1 - y_scale))
    return rgba.transform((w, h), Image.AFFINE, matrix, resample=Image.Resampling.BICUBIC)


def recenter_on_canvas(image: Image.Image, max_dimension: int = MAX_DIMENSION) -> Image.Image:
    rgba = image.convert("RGBA")
    arr = np.array(rgba)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 10)
    if len(xs) == 0:
        return rgba

    cropped = rgba.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    cw, ch = cropped.size
    scale = min(1.0, max_dimension / max(cw, ch))
    if scale < 1.0:
        cropped = cropped.resize(
            (max(1, int(round(cw * scale))), max(1, int(round(ch * scale)))),
            Image.Resampling.LANCZOS,
        )
        cw, ch = cropped.size

    canvas_w = max(cw, int(round(ch * 0.82)))
    canvas_h = max(ch, int(round(cw * 1.05)))
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    paste_x = (canvas_w - cw) // 2
    paste_y = (canvas_h - ch) // 2
    canvas.paste(cropped, (paste_x, paste_y), cropped)
    return canvas


def fix_slug(slug: str) -> tuple[float, Image.Image]:
    source = prepare_source(slug)
    y_scale = measure_y_scale(source, slug)
    y_scale = max(Y_SCALE_CLAMP[0], min(Y_SCALE_CLAMP[1], y_scale))
    corrected = apply_y_scale(source, y_scale)
    final = recenter_on_canvas(corrected)
    return y_scale, final


def main() -> None:
    print("Correcting circular invention icons...")
    for slug in TARGET_SLUGS:
        try:
            y_scale, image = fix_slug(slug)
        except FileNotFoundError as exc:
            print(f"  skip {slug}: {exc}")
            continue

        paths = slug_output_paths(slug)
        if not paths:
            print(f"  skip {slug}: no destination path")
            continue

        for path in paths:
            path.parent.mkdir(parents=True, exist_ok=True)
            image.save(path, format="PNG", optimize=True)
            print(
                f"  {path.relative_to(ROOT)}: y_scale={y_scale:.3f} "
                f"size={image.size[0]}x{image.size[1]}"
            )


if __name__ == "__main__":
    main()
