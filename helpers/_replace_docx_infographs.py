#!/usr/bin/env python3
"""Replace invention infographic images in the references docx from images/infographs."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from docx import Document
from docx.text.paragraph import Paragraph
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DOCX = ROOT / "documents" / "Most_Influential_Scientific_Inventions_and_Innovations (with references).docx"
INFOGRAPHS = ROOT / "images" / "infographs"
EMU_PER_INCH = 914400

sys.path.insert(0, str(ROOT / "helpers"))
from _analyze_inventions_docx import (  # noqa: E402
    NS,
    has_drawing,
    image_rids_in_paragraph,
    iter_block_items,
)


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "entry"


def collect_infographic_paragraphs(doc: Document) -> list[tuple[str, str, Paragraph]]:
    pending_title: str | None = None
    entries: list[tuple[str, str, Paragraph]] = []

    for block in iter_block_items(doc):
        if not isinstance(block, Paragraph):
            continue
        style = block.style.name if block.style else ""
        text = block.text.strip()
        if style == "Heading 2" and text:
            pending_title = text
            continue
        if pending_title and has_drawing(block):
            entries.append((pending_title, slugify(pending_title), block))
            pending_title = None

    return entries


def image_path_for(slug: str, *, artefacts: bool) -> Path:
    if artefacts:
        return INFOGRAPHS / f"{slug}-artefact.png"
    return INFOGRAPHS / f"{slug}.png"


def display_size_inches(
    pixel_width: int,
    pixel_height: int,
    *,
    artefacts: bool,
) -> tuple[float, float]:
    if artefacts:
        # Portrait illustration icons: readable but compact beside article text.
        width_in = 2.4
        height_in = width_in * (pixel_height / pixel_width)
        return width_in, height_in

    # Full 857×308 summary cards: preserve the document's existing width.
    width_in = 6.4
    height_in = width_in * (pixel_height / pixel_width)
    return width_in, height_in


def set_drawing_size(paragraph: Paragraph, width_in: float, height_in: float) -> None:
    cx = str(int(round(width_in * EMU_PER_INCH)))
    cy = str(int(round(height_in * EMU_PER_INCH)))
    for xpath in (".//wp:extent", ".//a:ext"):
        for element in paragraph._element.findall(xpath, NS):
            element.set("cx", cx)
            element.set("cy", cy)


def replace_image_blob(doc: Document, rid: str, image_path: Path) -> bool:
    part = doc.part.related_parts.get(rid)
    if part is None:
        raise KeyError(f"Missing relationship {rid!r} in document")

    new_bytes = image_path.read_bytes()
    if part.blob == new_bytes:
        return False

    part._blob = new_bytes
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--full",
        action="store_true",
        help="Use full summary-card infographics ({slug}.png) instead of artefact illustrations.",
    )
    args = parser.parse_args()
    use_artefacts = not args.full

    if not DOCX.exists():
        raise FileNotFoundError(DOCX)
    if not INFOGRAPHS.is_dir():
        raise FileNotFoundError(INFOGRAPHS)

    preview = collect_infographic_paragraphs(Document(str(DOCX)))
    if not preview:
        raise RuntimeError("No infographic paragraphs found in document")

    missing = [
        slug for _, slug, _ in preview if not image_path_for(slug, artefacts=use_artefacts).exists()
    ]
    if missing:
        kind = "artefact" if use_artefacts else "infograph"
        raise FileNotFoundError(f"Missing {kind} files for: {', '.join(missing)}")

    backup = DOCX.with_suffix(f".backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.docx")
    shutil.copy2(DOCX, backup)
    print(f"Backup: {backup.relative_to(ROOT)}")

    doc = Document(str(DOCX))
    entries = collect_infographic_paragraphs(doc)

    replaced = 0
    resized = 0
    kind_label = "artefact" if use_artefacts else "infograph"

    for title, slug, paragraph in entries:
        path = image_path_for(slug, artefacts=use_artefacts)
        pixel_width, pixel_height = Image.open(path).size
        width_in, height_in = display_size_inches(
            pixel_width,
            pixel_height,
            artefacts=use_artefacts,
        )
        set_drawing_size(paragraph, width_in, height_in)
        resized += 1

        rids = image_rids_in_paragraph(paragraph)
        if not rids:
            raise RuntimeError(f"No embedded image in paragraph for {title!r}")
        if len(rids) > 1:
            raise RuntimeError(f"Expected one image for {title!r}, found {len(rids)}")

        if replace_image_blob(doc, rids[0], path):
            replaced += 1
            print(f"  replaced: {path.name} ({pixel_width}x{pixel_height} -> {width_in:.2f}x{height_in:.2f} in)")
        else:
            print(f"  resized only: {path.name} ({width_in:.2f}x{height_in:.2f} in)")

    doc.save(str(DOCX))
    print(
        f"Updated {DOCX.relative_to(ROOT)} "
        f"({replaced}/{len(entries)} {kind_label} images replaced, {resized} display sizes set)"
    )


if __name__ == "__main__":
    main()
