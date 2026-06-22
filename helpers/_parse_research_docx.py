"""Parse the Scientific Inventions Research Reference Word document."""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document

from _build_inventions_page import slugify
from _paths import ROOT

RESEARCH_DOCX = ROOT / "documents" / "Most_Influential_Scientific_Inventions_Research_Reference (Cursor).docx"

SECTION_MAP = {
    "historical background": "background",
    "key inventors and contributors": "contributors",
    "scientific and technological principles": "principles",
    "development timeline and major milestones": "milestones",
    "impact on society": "impact",
    "long-term significance": "significance",
    "references and sources": "references",
}

ENTRY_RE = re.compile(r"^(\d+)\.(\d+)\s+(.+)$")
SKIP_H1 = {
    "comprehensive research reference",
    "contents",
    "general bibliography",
}


def _style_name(para) -> str:
    return (para.style.name if para.style else "").lower()


def _is_heading(para, level: int | None = None) -> bool:
    name = _style_name(para)
    if "heading" not in name:
        return False
    if level is None:
        return True
    return name == f"heading {level}"


def parse_research_docx(path: Path | None = None) -> dict:
    doc = Document(path or RESEARCH_DOCX)
    categories: list[dict] = []
    current_cat: dict | None = None
    current_entry: dict | None = None
    current_section: str | None = None
    pending_cat_title: str | None = None
    pending_intro: str | None = None
    started = False

    def flush_entry() -> None:
        nonlocal current_entry
        if current_entry and current_cat is not None:
            current_cat["entries"].append(current_entry)
        current_entry = None

    def flush_cat() -> None:
        nonlocal current_cat, pending_intro
        flush_entry()
        if current_cat and current_cat.get("entries"):
            if pending_intro and not current_cat.get("intro"):
                current_cat["intro"] = pending_intro
            categories.append(current_cat)
        current_cat = None
        pending_intro = None

    def open_category(cat_num: str, label: str) -> None:
        nonlocal current_cat, pending_intro
        flush_cat()
        current_cat = {
            "title": f"{cat_num}. {label}",
            "slug": slugify(f"{cat_num}-{label}"),
            "intro": pending_intro or "",
            "entries": [],
        }
        pending_intro = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        if _is_heading(para, 1):
            lower = text.lower()
            if lower in SKIP_H1:
                continue

            m_entry = ENTRY_RE.match(text)
            if m_entry:
                if not started:
                    started = True
                cat_num, _sub, title = m_entry.group(1), m_entry.group(2), m_entry.group(3).strip()
                if pending_cat_title:
                    open_category(cat_num, pending_cat_title)
                    pending_cat_title = None
                elif current_cat is None or cat_number(current_cat["title"]) != cat_num:
                    open_category(cat_num, title)

                flush_entry()
                current_entry = {
                    "number": f"{cat_num}.{m_entry.group(2)}",
                    "title": title,
                    "slug": slugify(title),
                    "meta": "",
                    "summary": "",
                    "sections": {},
                    "lists": {},
                }
                current_section = None
                continue

            if not started:
                if lower == "contents":
                    continue
                pending_cat_title = text
                pending_intro = None
                continue

            pending_cat_title = text
            pending_intro = None
            current_section = None
            continue

        if not started:
            continue

        if _is_heading(para, 2):
            key = SECTION_MAP.get(text.lower())
            current_section = key
            if current_entry is not None and key:
                current_entry["sections"].setdefault(key, [])
                current_entry["lists"].setdefault(key, [])
            continue

        if pending_cat_title and current_entry is None and current_cat is None:
            if _style_name(para) == "normal" and not text.lower().startswith("period:"):
                pending_intro = text
                continue

        if current_entry is None:
            continue

        style = _style_name(para)
        if current_section in {"contributors", "milestones", "references"}:
            if style.startswith("list"):
                current_entry["lists"].setdefault(current_section, []).append(text)
            elif current_section == "references" and re.match(r"^\d+\.", text):
                current_entry["lists"].setdefault(current_section, []).append(
                    re.sub(r"^\d+\.\s*", "", text)
                )
            else:
                current_entry["sections"].setdefault(current_section, []).append(text)
            continue

        if not current_section:
            if not current_entry.get("meta") and text.lower().startswith("period:"):
                current_entry["meta"] = text
            elif not current_entry.get("summary"):
                current_entry["summary"] = text
            continue

        current_entry["sections"].setdefault(current_section, []).append(text)

    flush_cat()
    entries = [entry for cat in categories for entry in cat["entries"]]
    return {"categories": categories, "entries": entries}


def cat_number(title: str) -> str:
    m = re.match(r"(\d+)", title.strip())
    return m.group(1) if m else ""
