#!/usr/bin/env python3
"""OCR infographic PNGs (857x308) with region crops and build structured JSON."""
from __future__ import annotations

import io
import json
import re
import zipfile
from pathlib import Path

from PIL import Image
from rapidocr_onnxruntime import RapidOCR

ROOT = Path(__file__).resolve().parent.parent
DOCX = ROOT / "documents" / "Most_Influential_Scientific_Inventions_and_Innovations (with references).docx"
OUT = ROOT / "helpers" / "_inventions_table_data_ocr.json"

W, H = 857, 308
HEADER = (0, 0, W, 72)
LEFT_TEXT = (118, 72, 520, H)
RIGHT_FACTS = (528, 72, W, H)

OCR = RapidOCR()


def ocr_region(img: Image.Image, box: tuple[int, int, int, int]) -> str:
    crop = img.crop(box)
    result, _ = OCR(crop)
    if not result:
        return ""
    lines = [item[1].strip() for item in result if item[1].strip()]
    return "\n".join(lines)


def parse_period(header: str) -> str:
    # period often on second line or after title
    lines = [ln.strip() for ln in header.splitlines() if ln.strip()]
    for ln in lines:
        if re.search(r"\b(BCE|CE|\d{4}|AWS|c\.)", ln, re.I):
            return ln.replace("C.", "c.").replace("–", "–")
    if len(lines) >= 2:
        return lines[-1]
    return ""


def parse_key_figures(left: str) -> str:
    m = re.search(r"Key figure\(s\):\s*(.+)", left, re.I | re.S)
    if m:
        text = m.group(1).strip()
        text = re.split(r"\n|KEY FACTS", text, flags=re.I)[0].strip()
        return re.sub(r"\s+", " ", text)
    return ""


def parse_summary(left: str) -> str:
    body = re.sub(r"Key figure\(s\):.*?(?:\n|$)", "", left, flags=re.I | re.S).strip()
    body = re.sub(r"\s+", " ", body)
    return body


def parse_key_facts(right: str) -> list[str]:
    text = re.sub(r"KEY FACTS\s*", "", right, flags=re.I)
    lines = [re.sub(r"\s+", " ", ln.strip()) for ln in text.splitlines() if ln.strip()]
    facts = []
    for ln in lines:
        ln = re.sub(r"^[•\-\u2022]\s*", "", ln)
        if ln and not ln.upper().startswith("KEY FACTS"):
            facts.append(ln)
    return facts


def extract_from_image(img: Image.Image) -> dict:
    header = ocr_region(img, HEADER)
    left = ocr_region(img, LEFT_TEXT)
    right = ocr_region(img, RIGHT_FACTS)
    return {
        "period": parse_period(header),
        "key_figures": parse_key_figures(left),
        "summary": parse_summary(left),
        "key_facts": parse_key_facts(right),
        "raw_header": header,
        "raw_left": left,
        "raw_right": right,
    }


def main() -> None:
    entries: list[dict] = []
    with zipfile.ZipFile(DOCX) as zf:
        media = sorted(
            (n for n in zf.namelist() if re.fullmatch(r"word/media/image\d+\.png", n)),
            key=lambda n: int(re.search(r"image(\d+)", n).group(1)),
        )
        for name in media:
            img = Image.open(io.BytesIO(zf.read(name)))
            idx = int(re.search(r"image(\d+)", name).group(1))
            data = extract_from_image(img)
            data["image"] = name
            data["image_index"] = idx
            entries.append(data)
            print(f"image{idx}: facts={len(data['key_facts'])} period={data['period'][:40]!r}")

    OUT.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} OCR entries -> {OUT}")


if __name__ == "__main__":
    main()
