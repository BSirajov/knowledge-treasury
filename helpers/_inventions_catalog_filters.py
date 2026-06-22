"""Shared catalog filter helpers for inventions pages."""
from __future__ import annotations

import html
import re

from _historical_periods import (
    PERIOD_LABELS,
    PERIOD_SLUGS,
    anchor_year,
    extract_years,
    infer_period_slug,
)


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def cat_number(title: str) -> str:
    m = re.match(r"(\d+)", title.strip())
    return m.group(1) if m else ""


def cat_label(title: str) -> str:
    return re.sub(r"^\d+\.\s*", "", title).strip()


def infer_period(meta: str, milestones: list[str], *, slug: str | None = None) -> str:
    return infer_period_slug(meta, milestones, slug=slug)


def render_category_select(data: dict) -> str:
    opts = ['<option value="">📚 Category</option>']
    for cat in data["categories"]:
        if not cat["entries"]:
            continue
        num = cat_number(cat["title"])
        label = cat_label(cat["title"])
        opts.append(f'<option value="{esc(num)}">{esc(num)}. {esc(label)}</option>')
    return "\n".join(opts)


def render_period_select() -> str:
    opts = ['<option value="">⏳ Historical period</option>']
    for slug in PERIOD_SLUGS:
        label = PERIOD_LABELS.get(slug, slug)
        opts.append(f'<option value="{esc(slug)}">{esc(label)}</option>')
    return "\n".join(opts)
