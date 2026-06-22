#!/usr/bin/env python3
"""Re-extract clean invention illustrations from full infographic cards."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _clean_temp_artefacts import BG, BG_TOL, remove_text_fragments

ROOT = Path(__file__).resolve().parent.parent
INVENTIONS = ROOT / "images" / "inventions"
INFOGRAPHS = ROOT / "images" / "infographs"

CARD_W, CARD_H = 857, 308
TEXT_LEFT = 118
PAD = 8
ARTEFACT_SIZE = (186, 233)

INFOGRAPH_ALIASES: dict[str, str] = {
    "microchip": "integrated-circuit-microchip",
    "fibre-optic": "fibre-optic-communication",
}


def infograph_slug(stem: str) -> str:
    return INFOGRAPH_ALIASES.get(stem, stem)


def is_center_navy(row: np.ndarray) -> np.ndarray:
    return (row[:, 0] < 55) & (row[:, 1] < 80) & (row[:, 2] > 95) & (row[:, 2] < 130)


def detect_body_top(card: np.ndarray) -> int:
    h, w = card.shape[:2]
    cx = slice(int(300 * w / CARD_W), int(500 * w / CARD_W))
    last_navy = 14
    for y in range(14, h):
        if is_center_navy(card[y, cx]).mean() > 0.5:
            last_navy = y
    return last_navy + 1


def detect_gold_right(card: np.ndarray, body_top: int) -> int:
    h, w = card.shape[:2]
    gold = (card[:, :, 0] > 165) & (card[:, :, 1] > 125) & (card[:, :, 2] < 105)
    max_x = min(int(80 * w / CARD_W), w)
    last = 0
    for x in range(max_x):
        if gold[body_top:, x].mean() > 0.65:
            last = x
    return max(last + 1, int(28 * w / CARD_W))


def has_card_strips(rgb: np.ndarray) -> bool:
    h, w = rgb.shape[:2]
    gold = (rgb[:, :, 0] > 165) & (rgb[:, :, 1] > 125) & (rgb[:, :, 2] < 105)
    navy = (rgb[:, :, 0] < 55) & (rgb[:, :, 1] < 80) & (rgb[:, :, 2] > 95) & (rgb[:, :, 2] < 130)
    for x in range(min(20, w)):
        if gold[:, x].sum() > h * 0.35:
            return True
    for y in range(min(25, h)):
        if navy[y].sum() > w * 0.55:
            return True
    return False


def trim_vertical_margins(image: Image.Image) -> Image.Image:
    rgb = np.array(image.convert("RGB"))
    diff = np.abs(rgb.astype(np.int16) - BG.astype(np.int16)).sum(axis=2)
    ys = np.where(diff > BG_TOL)[0]
    if len(ys) == 0:
        return image
    top = max(0, int(ys.min()) - PAD)
    bottom = min(rgb.shape[0], int(ys.max()) + PAD + 1)
    return image.crop((0, top, image.width, bottom))


def extract_clean(slug: str) -> Image.Image | None:
    src = INFOGRAPHS / f"{infograph_slug(slug)}.png"
    if not src.exists():
        return None

    card = np.array(Image.open(src).convert("RGB"))
    h, w = card.shape[:2]
    body_top = detect_body_top(card)
    gold_right = detect_gold_right(card, body_top)
    text_left = int(TEXT_LEFT * w / CARD_W)

    crop = Image.fromarray(card).crop((gold_right, body_top, text_left, h))
    crop = trim_vertical_margins(crop)
    return remove_text_fragments(crop)


def should_process(path: Path) -> bool:
    if path.stem.startswith("_"):
        return False
    image = Image.open(path)
    if image.size == ARTEFACT_SIZE:
        return True
    return has_card_strips(np.array(image.convert("RGB")))


def main() -> None:
    paths = sorted(INVENTIONS.glob("*.png"))
    updated: list[str] = []
    skipped: list[str] = []
    missing: list[str] = []

    for path in paths:
        if not should_process(path):
            skipped.append(path.name)
            continue

        cleaned = extract_clean(path.stem)
        if cleaned is None:
            missing.append(path.name)
            continue

        cleaned.save(path, format="PNG", optimize=True)
        updated.append(f"{path.name} ({cleaned.size[0]}x{cleaned.size[1]})")

    for test_file in INVENTIONS.glob("_test*.png"):
        test_file.unlink()

    print(f"Updated {len(updated)} images in {INVENTIONS.relative_to(ROOT)}")
    for line in updated:
        print(f"  {line}")
    if skipped:
        print(f"Skipped {len(skipped)} already-clean images")
    if missing:
        print(f"No infograph source for {len(missing)} images: {', '.join(missing)}")


if __name__ == "__main__":
    main()
