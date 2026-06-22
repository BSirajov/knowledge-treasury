#!/usr/bin/env python3
"""Build the interactive Scientific Inventions Research web page."""
from __future__ import annotations

import json
import re
from pathlib import Path

from _build_inventions_page import (
    esc,
    linkify_text,
    load_card_copy,
    load_card_data,
    load_card_overrides,
    load_icon_index,
    load_nav_html,
    render_entry_icon,
    site_icon_src,
)
from _parse_research_docx import parse_research_docx
from _kt_favicon import favicon_links
from _inventions_catalog_filters import (
    PERIOD_LABELS,
    cat_label,
    cat_number,
    infer_period,
    render_category_select,
    render_period_select,
)
from _paths import HELPERS, ROOT

OUT_HTML = ROOT / "en" / "scientific_inventions_research.html"
ENTRY_REFERENCES = HELPERS / "_invention_entry_references.json"
ALL_REFS = HELPERS / "_all_refs.json"

CATEGORY_INTROS = {
    "1": (
        "Foundational civilisational innovations — fire, agriculture, the wheel, writing, mathematics, "
        "paper, navigation, gunpowder, and printing — established the material and intellectual "
        "preconditions for all later science and technology."
    ),
    "2": (
        "Knowledge and scientific instruments transformed how humans observe, measure, and explain "
        "the natural world, from the scientific method through telescopes, microscopes, and Newtonian mechanics."
    ),
    "3": (
        "Industrial, energy, and transport technologies converted scientific understanding into "
        "mechanical power, electrical grids, and global mobility."
    ),
    "4": (
        "Medicine, biology, and public health innovations extended human lifespan and quality of life "
        "through vaccination, antibiotics, germ theory, anaesthesia, imaging, sanitation, and molecular genetics."
    ),
    "5": (
        "Physics, chemistry, and materials science revealed the structure of matter and energy, "
        "enabling the periodic table, quantum theory, relativity, nuclear science, plastics, and fertilisers."
    ),
    "6": (
        "Digital, space, and communication technologies interconnected the planet through telegraphy, "
        "telephony, radio, semiconductors, computing, the internet, satellites, GPS, lasers, and fibre optics."
    ),
    "7": (
        "Emerging and transformative technologies — artificial intelligence, renewables, batteries, "
        "electric vehicles, robotics, additive manufacturing, and blockchain — are reshaping the 21st century."
    ),
}

PAGE_SUMMARY = {
    "title": "Landmarks of science and technology",
    "lead": (
        "From the controlled use of fire to artificial intelligence — sixty research articles organised "
        "across seven thematic categories, each examining historical origins, pioneering contributors, "
        "scientific principles, development milestones, societal impact, and verified scholarly sources."
    ),
}

RESEARCH_SECTIONS = [
    ("background", "Historical background"),
    ("contributors", "Key inventors and contributors"),
    ("principles", "Scientific and technological principles"),
    ("milestones", "Development timeline and major milestones"),
    ("impact", "Impact on society"),
    ("significance", "Long-term significance"),
    ("references", "References and sources"),
]


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def build_search_blob(entry: dict) -> str:
    parts = [
        entry.get("number", ""),
        entry["title"],
        entry.get("meta", ""),
        entry.get("summary", ""),
        entry.get("card_key_figures", ""),
        " ".join(entry.get("card_facts", [])),
    ]
    for key, _label in RESEARCH_SECTIONS:
        parts.extend(entry.get("sections", {}).get(key, []))
        parts.extend(entry.get("lists", {}).get(key, []))
    return " ".join(p for p in parts if p).strip()


def render_list(items: list[str], ordered: bool = False) -> str:
    if not items:
        return ""
    tag = "ol" if ordered else "ul"
    lis = "".join(f"<li>{esc(item)}</li>" for item in items)
    return f"<{tag} class=\"research-list\">{lis}</{tag}>"


def render_references_list(items: list[str]) -> str:
    if not items:
        return "<p class=\"research-empty\">See the general bibliography at the end of this resource.</p>"
    lis = "".join(f"<li>{linkify_text(item)}</li>" for item in items)
    return f'<ol class="research-bibliography">{lis}</ol>'


def attach_research_cards(data: dict) -> None:
    cards = load_card_data()
    overrides = load_card_overrides()
    card_copy = load_card_copy()
    icon_index = load_icon_index()
    for entry in data["entries"]:
        card = cards.get(entry["slug"], {})
        override = overrides.get(entry["slug"], {})
        clean = card_copy.get(entry["slug"], {})
        entry["card_key_figures"] = (
            override.get("key_figures") or clean.get("key_figures") or card.get("key_figures", "")
        )
        entry["card_facts"] = (
            override.get("key_facts") or clean.get("key_facts") or card.get("key_facts", [])
        )
        raw_icon = override.get("icon") or card.get("icon", "")
        entry["card_icon"] = site_icon_src(entry["slug"], icon_index, raw_icon)
        if not entry.get("summary"):
            entry["summary"] = clean.get("summary") or card.get("summary", "")


def render_research_entry(entry: dict, cat_num: str) -> str:
    slug = entry["slug"]
    number = entry.get("number", "")
    milestones = entry.get("lists", {}).get("milestones", [])
    period = infer_period(entry.get("meta", ""), milestones, slug=slug)
    body_id = f"research-body-{slug}"
    search = build_search_blob(entry)

    header_btn = (
        f'<button type="button" class="research-entry__toggle" '
        f'aria-expanded="false" aria-controls="{esc(body_id)}" id="research-toggle-{esc(slug)}">'
        f'<span class="research-entry__title-wrap">'
        f'<span class="research-entry__num" aria-hidden="true">{esc(number)}</span>'
        f'<span class="research-entry__name">{esc(entry["title"])}</span>'
        f"</span>"
        f'<span class="research-entry__badges">'
        f'<span class="research-badge research-badge--period">{esc(PERIOD_LABELS.get(period, period))}</span>'
        f"</span>"
        f'<span class="research-entry__chevron" aria-hidden="true"></span>'
        f"</button>"
    )

    teaser_bits: list[str] = []
    if entry.get("meta"):
        teaser_bits.append(f'<p class="research-entry__meta">{esc(entry["meta"])}</p>')
    if entry.get("summary"):
        teaser_bits.append(f'<p class="research-entry__summary">{esc(entry["summary"])}</p>')

    sections_html: list[str] = []

    if entry.get("card_icon") or entry.get("card_facts") or entry.get("card_key_figures"):
        visual_parts = ['<div class="research-entry__visual inventions-entry-visual">']
        visual_parts.append(
            render_entry_icon(entry).replace(
                "inventions-entry-icon", "inventions-entry-icon research-entry__icon"
            )
        )
        copy_bits: list[str] = []
        if entry.get("card_key_figures"):
            copy_bits.append(
                '<p class="inventions-entry-visual-figures">'
                f'<strong>Key figure(s):</strong> {esc(entry["card_key_figures"])}</p>'
            )
        if entry.get("card_facts"):
            items = "".join(f"<li>{esc(f)}</li>" for f in entry["card_facts"])
            copy_bits.append(
                '<div class="inventions-key-facts"><h4>At a glance</h4>'
                f"<ul>{items}</ul></div>"
            )
        if copy_bits:
            visual_parts.append(
                '<div class="inventions-entry-visual-copy">' + "".join(copy_bits) + "</div>"
            )
        visual_parts.append("</div>")
        sections_html.append("".join(visual_parts))

    for section_id, label in RESEARCH_SECTIONS:
        if section_id in {"contributors", "milestones"}:
            body = render_list(
                entry.get("lists", {}).get(section_id, []),
                ordered=(section_id == "milestones"),
            )
        elif section_id == "references":
            body = render_references_list(entry.get("lists", {}).get(section_id, []))
        else:
            lines = entry.get("sections", {}).get(section_id, [])
            body = "".join(f"<p>{esc(line)}</p>" for line in lines)

        if not body.strip():
            continue

        sections_html.append(
            f'<section class="research-section" id="{esc(slug)}-{esc(section_id)}">'
            f"<h3>{esc(label)}</h3>{body}</section>"
        )

    return f"""
<article class="research-entry" id="{esc(slug)}"
  data-search="{esc(search)}"
  data-category="{esc(cat_num)}"
  data-period="{esc(period)}"
  data-number="{esc(number)}">
  <header class="research-entry__header">
    {header_btn}
    {''.join(teaser_bits)}
  </header>
  <div class="research-entry__body" id="{esc(body_id)}" hidden>
    {''.join(sections_html)}
  </div>
</article>"""


def render_toc(data: dict) -> str:
    items = ['<ul class="timeline-list research-toc" id="researchTocList">']
    for cat in data["categories"]:
        if not cat["entries"]:
            continue
        num = cat_number(cat["title"])
        label = cat_label(cat["title"])
        items.append(
            f'<li class="research-toc-cat" data-toc-cat="{esc(cat["slug"])}" data-category="{esc(num)}">'
            f'<button type="button" class="research-toc-cat__btn" aria-expanded="true" '
            f'aria-controls="research-toc-group-{esc(num)}">'
            f'<span class="tl-date">§{esc(num)}</span>'
            f'<span class="research-toc-cat__label">{esc(label)}</span>'
            f'<span class="research-toc-cat__count">{len(cat["entries"])}</span>'
            f"</button></li>"
        )
        items.append(f'<li class="research-toc-group" id="research-toc-group-{esc(num)}"><ul>')
        for entry in cat["entries"]:
            number = entry.get("number", "")
            items.append(
                f'<li class="research-toc-entry" data-toc-entry="{esc(entry["slug"])}" '
                f'data-toc-cat="{esc(cat["slug"])}" data-category="{esc(num)}" '
                f'data-search="{esc((number + " " if number else "") + entry["title"])}">'
                f'<span class="tl-date">{esc(number) if number else "·"}</span>'
                f'<a href="#{esc(entry["slug"])}">{esc(entry["title"])}</a></li>'
            )
        items.append("</ul></li>")
    items.append(
        '<li class="research-toc-extra"><span class="tl-date">⊕</span>'
        '<a href="#research-bibliography">General bibliography</a></li>'
    )
    items.append("</ul>")
    return "\n".join(items)


def render_categories(data: dict) -> str:
    parts: list[str] = []
    for cat in data["categories"]:
        if not cat["entries"]:
            continue
        num = cat_number(cat["title"])
        intro = cat.get("intro") or CATEGORY_INTROS.get(num, "")
        entries_html = "\n".join(render_research_entry(e, num) for e in cat["entries"])
        intro_html = f'<p class="research-category__intro">{esc(intro)}</p>' if intro else ""
        parts.append(
            f'<section class="research-category" id="{esc(cat["slug"])}" '
            f'data-category="{esc(num)}">'
            f'<h2 class="research-category__head">{esc(cat["title"])}</h2>'
            f"{intro_html}{entries_html}</section>"
        )
    return "\n".join(parts)


def render_general_bibliography(ref_index: dict[str, str]) -> str:
    general = [
        r["text"]
        for r in load_json(ALL_REFS)
        if r.get("group", "").startswith("A.")
    ][:10]
    items = "".join(f"<li>{linkify_text(t)}</li>" for t in general)
    search = "General bibliography " + " ".join(general)
    count = len(general)
    return f"""
<article class="research-entry research-bibliography-entry" id="research-bibliography"
  data-search="{esc(search)}">
  <header class="research-entry__header">
    <button type="button" class="research-entry__toggle research-entry__toggle--category"
      aria-expanded="false" aria-controls="research-body-bibliography" id="research-toggle-bibliography">
      <span class="research-entry__title-wrap">
        <span class="research-entry__name">General bibliography</span>
      </span>
      <span class="research-entry__chevron" aria-hidden="true"></span>
    </button>
    <p class="research-entry__summary">These sources support multiple entries throughout this research resource ({count} cross-cutting references).</p>
  </header>
  <div class="research-entry__body" id="research-body-bibliography" hidden>
    <ol class="research-bibliography research-bibliography--general">{items}</ol>
    <p class="research-source-note">URLs were verified at the time of preparation (June 2026). Peer-reviewed items include DOI or journal details where available. Museum, encyclopaedia, and educational resources are included for accessibility.</p>
  </div>
</article>"""


def count_entries(data: dict) -> int:
    return sum(len(cat["entries"]) for cat in data["categories"])


def build_html(data: dict) -> str:
    nav = load_nav_html()
    return f"""<!DOCTYPE html>
<html lang="en" data-kt-lang="en" data-kt-asset-root="../" data-kt-page-id="major-scientific-inventions" data-kt-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
{favicon_links("../")}
<title>Knowledge Treasury — Scientific Inventions Research Reference</title>
<meta name="description" content="Comprehensive scholarly research on 60 landmark scientific inventions — historical background, contributors, timelines, principles, societal impact, and verified references."/>
<link rel="canonical" href="https://bilik-xezinesi.az/en/scientific_inventions_research.html"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..900&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
<link href="../css/kt-common.css?v=70" rel="stylesheet"/>
<link href="../css/kt-perf.css?v=1" rel="stylesheet"/>
<link href="../css/kt-mobile.css?v=13" rel="stylesheet"/>
<link href="../css/kt-sticky-chrome.css?v=1" rel="stylesheet"/>
<link href="../css/kt-site-background.css?v=6" rel="stylesheet"/>
<link href="../css/kt-back-to-top.css?v=2" rel="stylesheet"/>
<link href="../css/kt-lang.css?v=13" rel="stylesheet"/>
<link href="../css/kt-nav-mega.css?v=69" rel="stylesheet"/>
<link href="../css/kt-hero-summary.css?v=13" rel="stylesheet"/>
<link href="../css/kt-content-hero.css?v=7" rel="stylesheet"/>
<link href="../css/kt-sidebar-widget.css?v=7" rel="stylesheet"/>
<link href="../css/kt-catalog-toolbar.css?v=15" rel="stylesheet"/>
<link href="../css/kt-inventions.css?v=25" rel="stylesheet"/>
<link href="../css/kt-inventions-research.css?v=12" rel="stylesheet"/>
<script src="../js/kt-mobile.js?v=6" defer></script>
<script src="../js/kt-perf.js?v=1" defer></script>
<script src="../js/kt-sticky-chrome.js?v=3" defer></script>
<script src="../js/kt-back-to-top.js?v=3" defer></script>
<script src="../js/kt-i18n.js?v=32" defer></script>
<script src="../js/kt-lang-position.js?v=7" defer></script>
<script src="../js/kt-design-tokens.js?v=2" defer></script>
<script src="../js/kt-nav.js?v=31" defer></script>
<script src="../js/kt-primary-nav.js?v=56" defer></script>
<script src="../js/kt-breadcrumbs.js?v=34" defer></script>
<script src="../js/kt-shell.js?v=13" defer></script>
<script src="../js/kt-page-subtitle.js?v=2" defer></script>
<script src="../js/kt-catalog-multi-filter.js?v=2" defer></script>
<script src="../js/kt-catalog-toolbar-mobile.js?v=8" defer></script>
<script src="../js/kt-historical-periods.js?v=1" defer></script>
<script src="../js/kt-sidebar-toc-groups.js?v=7" defer></script>
<script src="../js/kt-inventions-research.js?v=12" defer></script>
</head>
<body class="charter-page inventions-research-page">
<a class="skip" href="#content">Skip to content</a>
{nav}
<header class="hero page-hero research-hero">
<div class="hero-inner shell">
<section class="hero-copy">
<h1 aria-describedby="page-hero-subtitle">Scientific Inventions Research</h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">Comprehensive scholarly reference — historical background, contributors, timelines, principles, and verified sources</p>
</section>
<aside aria-label="About this research resource" class="hero-summary-panel">
<div class="hero-summary-card">
<h2 class="panel-title">{esc(PAGE_SUMMARY["title"])}</h2>
<p class="hero-text panel-copy-lead">{esc(PAGE_SUMMARY["lead"])}</p>
</div>
</aside>
</div>
</header>
<main class="main" id="content">
<div class="toolbar catalog-toolbar" aria-label="Research filters">
<div class="catalog-toolbar__head">
<div class="search-wrap">
<svg fill="none" height="15" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="15" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><line x1="21" x2="16.65" y1="21" y2="16.65"></line></svg>
<input type="search" id="researchSearch" placeholder="Search titles, figures, periods, principles, references…" aria-label="Search research articles" autocomplete="off"/>
</div>
<button type="button" class="catalog-toolbar__toggle" aria-expanded="false" aria-controls="catalogFilterPanel" aria-label="Show filters"><svg class="catalog-toolbar__toggle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 5h18l-7 9v5l-4-2v-3L3 5z"/></svg><span class="catalog-toolbar__toggle-text">Filters</span><span class="catalog-toolbar__badge" hidden></span></button>
</div>
<div class="catalog-toolbar__panel" id="catalogFilterPanel">
<div class="catalog-toolbar__panel-inner">
<div class="filter-group">
<span class="filter-icon-label" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 5h18l-7 9v5l-4-2v-3L3 5z"/></svg><span>Filters</span></span>
<div class="filter-group__primary">
<div class="sel-wrap">
<select id="filterCategory" aria-label="Category">{render_category_select(data)}</select>
<button class="sel-clear" data-for="filterCategory" title="Clear filter" type="button">×</button>
</div>
<div class="sel-wrap">
<select id="filterPeriod" aria-label="Historical period">{render_period_select()}</select>
<button class="sel-clear" data-for="filterPeriod" title="Clear filter" type="button">×</button>
</div>
</div>
<button class="btn-clear" id="clearFilters" type="button">Clear all</button>
</div>
</div>
</div>
</div>
<div class="research-no-results" id="researchNoResults" hidden>No articles match the current search and filters.</div>
<div class="research-progress" aria-hidden="true"><span class="research-progress__bar" id="researchProgressBar"></span></div>
<div class="charter-layout research-layout">
<aside class="charter-sidebar toc-card research-sidebar" aria-label="Table of contents">
<div class="sidebar-widget events-open" id="researchTocWidget">
<div class="widget-head">
<h2 class="widget-head__title"><span class="widget-head__icon" aria-hidden="true">📑</span> Contents</h2>
<button type="button" class="events-menu-toggle" aria-expanded="true" aria-controls="researchTocWidgetBody" aria-label="Toggle table of contents"><span></span><span></span><span></span></button>
</div>
<div class="widget-actions" role="group" aria-label="Contents section controls">
<button type="button" class="widget-action-btn widget-action-btn--toggle widget-action-btn--will-collapse" data-toc-action="toggle-categories" data-bulk-kind="categories" data-bulk-action="collapse" aria-pressed="true" aria-expanded="true" aria-label="Collapse all categories" title="Collapse All Categories"><span class="widget-action-btn__icon" aria-hidden="true"></span><span class="widget-action-btn__label">Collapse All Categories</span></button>
</div>
<div class="widget-body" id="researchTocWidgetBody">
{render_toc(data)}
</div>
</div>
</aside>
<div class="research-main">
<div class="sidebar-widget sidebar-widget--controls-only articles-panel-widget" id="researchArticlesPanel" aria-label="Articles">
<div class="widget-head">
<h2 class="widget-head__title"><span class="widget-head__icon" aria-hidden="true">📚</span> Articles</h2>
</div>
<div class="widget-actions" role="group" aria-label="Articles controls">
<button type="button" class="widget-action-btn widget-action-btn--toggle widget-action-btn--will-expand" id="researchToggleArticles" data-article-action="toggle-articles" data-bulk-kind="articles" data-bulk-action="expand" aria-pressed="false" aria-expanded="false" aria-label="Expand all articles" title="Expand All Articles"><span class="widget-action-btn__icon" aria-hidden="true"></span><span class="widget-action-btn__label">Expand All Articles</span></button>
<button type="button" class="widget-action-btn widget-action-btn--toggle widget-action-btn--will-collapse" id="researchToggleCategories" data-article-action="toggle-categories" data-bulk-kind="categories" data-bulk-action="collapse" aria-pressed="true" aria-expanded="true" aria-label="Collapse all categories" title="Collapse All Categories"><span class="widget-action-btn__icon" aria-hidden="true"></span><span class="widget-action-btn__label">Collapse All Categories</span></button>
</div>
</div>
<div class="charter-stack research-stack">
{render_categories(data)}
{render_general_bibliography({})}
</div>
</div>
</div>
</main>
<button type="button" class="research-toc-fab" id="researchTocFab" aria-label="Open table of contents" aria-controls="researchTocWidget" hidden>
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h10"/></svg>
</button>
</body>
</html>"""


def main() -> None:
    data = parse_research_docx()
    attach_research_cards(data)
    html = build_html(data)
    OUT_HTML.write_text(html, encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_HTML.relative_to(ROOT)} ({count_entries(data)} articles)")


if __name__ == "__main__":
    main()
