#!/usr/bin/env python3
"""Generate prominent figure profile HTML pages from structured data."""
from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from _paths import ROOT

ASSET = "../../../"
SITE = "https://bilik-xezinesi.az"

CSS_LINKS = "\n".join(
    [
        f'<link href="{ASSET}css/kt-common.css?v=70" rel="stylesheet"/>',
        f'<link href="{ASSET}css/kt-perf.css?v=1" rel="stylesheet"/>',
        f'<link href="{ASSET}css/kt-mobile.css?v=13" rel="stylesheet"/>',
        f'<link href="{ASSET}css/kt-sticky-chrome.css?v=1" rel="stylesheet"/>',
        f'<link href="{ASSET}css/kt-site-background.css?v=6" rel="stylesheet"/>',
        f'<link href="{ASSET}css/kt-back-to-top.css?v=2" rel="stylesheet"/>',
        f'<link href="{ASSET}css/kt-lang.css?v=13" rel="stylesheet"/>',
        f'<link href="{ASSET}css/kt-nav-mega.css?v=69" rel="stylesheet"/>',
        f'<link href="{ASSET}css/kt-hero-summary.css?v=13" rel="stylesheet"/>',
        f'<link href="{ASSET}css/kt-prominent-figure-profile.css?v=3" rel="stylesheet"/>',
    ]
)

JS_SCRIPTS = "\n".join(
    [
        f'<script src="{ASSET}js/kt-mobile.js?v=6" defer></script>',
        f'<script src="{ASSET}js/kt-perf.js?v=1" defer></script>',
        f'<script src="{ASSET}js/kt-sticky-chrome.js?v=3" defer></script>',
        f'<script src="{ASSET}js/kt-back-to-top.js?v=3" defer></script>',
        f'<script src="{ASSET}js/kt-i18n.js?v=33" defer></script>',
        f'<script src="{ASSET}js/kt-lang-position.js?v=7" defer></script>',
        f'<script src="{ASSET}js/kt-design-tokens.js?v=2" defer></script>',
        f'<script src="{ASSET}js/kt-nav.js?v=31" defer></script>',
        f'<script src="{ASSET}js/kt-primary-nav.js?v=59" defer></script>',
        f'<script src="{ASSET}js/kt-breadcrumbs.js?v=34" defer></script>',
        f'<script src="{ASSET}js/kt-shell.js?v=15" defer></script>',
    ]
)

CATEGORY_TAG = {
    "az": {"azturk": "Azərbaycan və türk dünyası", "world": "Dünya alimləri"},
    "en": {"azturk": "Azerbaijani & Turkic heritage", "world": "World scientists"},
}

UI = {
    "az": {
        "skip": "Məzmuna keç",
        "nav_aria": "Əsas naviqasiya",
        "menu_open": "Menyunu aç",
        "home_title": "Ana səhifə",
        "home_aria": "Bilik xəzinəsi ana səhifə",
        "brand": "Bilik<br class=\"mobile-hidden-break\">xəzinəsi",
        "nav_pf": "👤 Görkəmli şəxsiyyətlər",
        "nav_inv": "💡 Əsas elmi ixtiralar",
        "nav_ir": "⚙️ Sənaye inqilabları",
        "about": "haqqında",
        "life": "Həyat yolu",
        "work": "Elmi və yaradıcılıq fəaliyyəti",
        "impact": "Cəmiyyətə təsiri",
        "works_title": "Əsas əsərləri və fəaliyyəti",
        "events_title": "Həyatından maraqlı hadisələr",
        "sources_title": "Qaynaqlar",
        "sources_note": (
            "Bu profil akademik ensiklopediyalar, universitet resursları və "
            "tanınmış elmi nəşrlər əsasında hazırlanmışdır."
        ),
        "info_title": "Şəxsi Məlumat",
        "full_name": "Tam adı",
        "birth": "Doğum tarixi",
        "death": "Vəfat tarixi",
        "origin": "Xalq / mənsubiyyət",
        "period": "Dövr / dövlət",
        "field": "Sahə",
        "contrib_title": "Cəmiyyətə Töhfələr",
        "see_also": "Həmçinin Baxın",
        "catalog_link": "Bütün profillərə bax",
        "footer_brand": "Bilik xəzinəsi",
        "footer_contact": "Əlaqə",
        "footer_rights": "© 2026 Bilik xəzinəsi — Bütün hüquqlar qorunur",
        "page_suffix": "Görkəmli Şəxsiyyətlər | Bilik xəzinəsi",
    },
    "en": {
        "skip": "Skip to content",
        "nav_aria": "Main navigation",
        "menu_open": "Open menu",
        "home_title": "Home page",
        "home_aria": "Knowledge Treasury home",
        "brand": "Knowledge<br class=\"mobile-hidden-break\">Treasury",
        "nav_pf": "👤 Prominent Figures",
        "nav_inv": "💡 Major Scientific Inventions",
        "nav_ir": "⚙️ Industrial Revolutions",
        "about": "About",
        "life": "Life and career",
        "work": "Scholarly and creative work",
        "impact": "Contribution to society",
        "works_title": "Key works and contributions",
        "events_title": "Notable aspects of the life and work",
        "sources_title": "Sources",
        "sources_note": (
            "This profile is compiled from academic encyclopedias, university resources, "
            "and established scholarly reference works."
        ),
        "info_title": "Personal information",
        "full_name": "Full name",
        "birth": "Year of birth",
        "death": "Year of death",
        "origin": "People / origin",
        "period": "Period / context",
        "field": "Field",
        "contrib_title": "Contributions to society",
        "see_also": "See also",
        "catalog_link": "Browse all profiles",
        "footer_brand": "Knowledge Treasury",
        "footer_contact": "Contact",
        "footer_rights": "© 2026 Knowledge Treasury — All rights reserved",
        "page_suffix": "Knowledge Treasury",
    },
}


def esc(text: str) -> str:
    return html.escape(text or "", quote=True)


def pick(fig: dict[str, Any], lang: str, key: str) -> str:
    return str(fig.get(f"{key}_{lang}") or fig.get(key) or "")


def works_html(fig: dict[str, Any], lang: str) -> str:
    items = []
    for i, work in enumerate(fig.get("works") or [], start=1):
        name = pick(work, lang, "name")
        desc = pick(work, lang, "desc")
        items.append(
            f'<li class="work-item"><div class="work-num">{i}</div><div>'
            f'<div class="work-name"><em>{esc(name)}</em></div>'
            f'<div class="work-desc">{esc(desc)}</div></div></li>'
        )
    return "\n".join(items)


def events_html(fig: dict[str, Any], lang: str) -> str:
    items = []
    for event in fig.get("events") or []:
        icon = event.get("icon") or "📌"
        title = pick(event, lang, "title")
        text = pick(event, lang, "text")
        items.append(
            f'<div class="event-item"><div class="event-title">'
            f'<span aria-hidden="true">{esc(icon)}</span> {esc(title)}</div>'
            f'<div class="event-text">{esc(text)}</div></div>'
        )
    return "\n".join(items)


def sources_html(fig: dict[str, Any], lang: str) -> str:
    items = []
    for src in fig.get("sources") or []:
        title = pick(src, lang, "title")
        url = src.get("url") or "#"
        items.append(
            f'<li><a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(title)}</a></li>'
        )
    return "\n".join(items)


def contributions_html(fig: dict[str, Any], lang: str) -> str:
    key = f"contributions_{lang}"
    return "\n".join(
        f'<li class="contribution-item">{esc(item)}</li>'
        for item in (fig.get(key) or [])
    )


def nav_strip(lang: str) -> str:
    u = UI[lang]
    inv_href = "../../scientific_inventions_research.html" if lang == "en" else "../../en/scientific_inventions_research.html"
    return (
        f'<nav aria-label="{esc(u["nav_aria"])}" class="nav-strip"><div class="nav-inner">'
        f'<button class="mobile-menu-toggle" type="button" aria-label="{esc(u["menu_open"])}" '
        f'aria-expanded="false" aria-controls="primaryNavMenu"><span></span><span></span><span></span></button>'
        f'<div class="page-logo"><a title="{esc(u["home_title"])}" aria-label="{esc(u["home_aria"])}" '
        f'href="../../index.html"><img src="{ASSET}images/kt-logo.png" class="nav-brand-logo" '
        f'alt="{esc(u["footer_brand"])}"></a></div>'
        f'<a aria-label="{esc(u["home_aria"])}" class="nav-brand" href="../../index.html">'
        f'<span class="nav-brand-text">{u["brand"]}</span></a>'
        f'<div class="nav-menu" id="primaryNavMenu" data-kt-nav-placeholder="1"><div class="nav-divider"></div>'
        f'<a class="nav-link" href="../../prominent_figures.html" data-nav-id="prominent-figures">{u["nav_pf"]}</a>'
        f'<a class="nav-link" href="{inv_href}" data-nav-id="major-scientific-inventions">{u["nav_inv"]}</a>'
        f'<a class="nav-link" href="../../industrial_revolutions.html" data-nav-id="industrial-revolutions">{u["nav_ir"]}</a>'
        f"</div></div></nav>"
    )


def render_profile(fig: dict[str, Any], lang: str) -> str:
    slug = fig["slug"]
    category = fig["category"]
    u = UI[lang]
    name = pick(fig, lang, "name")
    dates = fig.get("dates") or ""
    emoji = fig.get("emoji") or "⭐"
    country = pick(fig, lang, "country")
    field = pick(fig, lang, "field")
    category_tag = CATEGORY_TAG[lang][category]
    birth = fig.get("birth") or ""
    death = fig.get("death") or ""
    life = pick(fig, lang, "life")
    work = pick(fig, lang, "work")
    impact = pick(fig, lang, "impact")
    quote = pick(fig, lang, "quote")
    quote_src = pick(fig, lang, "quote_source") or f"— {name}"

    canonical = f"{SITE}/{lang}/prominent_figures/{category}/{slug}.html"
    alt_az = f"{SITE}/az/prominent_figures/{category}/{slug}.html"
    alt_en = f"{SITE}/en/prominent_figures/{category}/{slug}.html"
    meta = esc(life[:220] if life else f"{name} — {country}. {field}.")

    og_locale = "en_US" if lang == "en" else "az_AZ"
    og_alt = "az_AZ" if lang == "en" else "en_US"
    title_suffix = u["page_suffix"]
    if lang == "en" and category == "azturk":
        title_suffix = "Azerbaijani & Turkic Heritage | Knowledge Treasury"

    return f"""<!DOCTYPE html>
<html lang="{lang}" data-kt-lang="{lang}" data-kt-asset-root="{ASSET}" data-kt-page-id="prominent-figure" data-kt-profile-name="{esc(name)}" data-kt-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(name)} — {esc(title_suffix)}</title>
<meta name="description" content="{meta}"/>
<!-- kt-seo -->
<link rel="icon" href="{ASSET}images/kt-favicon.png" type="image/png" sizes="32x32"/>
<link rel="icon" href="{ASSET}images/kt-logo.png" type="image/png" sizes="512x512"/>
<link rel="apple-touch-icon" href="{ASSET}images/apple-touch-icon.png"/>
<link rel="canonical" href="{canonical}"/>
<link rel="alternate" hreflang="az" href="{alt_az}"/>
<link rel="alternate" hreflang="en" href="{alt_en}"/>
<link rel="alternate" hreflang="x-default" href="{alt_az}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="{esc(u['footer_brand'])}"/>
<meta property="og:title" content="{esc(name)} — {esc(title_suffix)}"/>
<meta property="og:description" content="{meta}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:locale" content="{og_locale}"/>
<meta property="og:locale:alternate" content="{og_alt}"/>
<meta name="twitter:card" content="summary"/>
<meta name="twitter:title" content="{esc(name)} — {esc(title_suffix)}"/>
<meta name="twitter:description" content="{meta}"/>
<!-- /kt-seo -->
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..900&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
{CSS_LINKS}
{JS_SCRIPTS}
</head>
<body class="kt-prominent-figure-page">
<a class="skip" href="#content">{esc(u["skip"])}</a>
{nav_strip(lang)}
<header class="hero pf-profile-hero"><div class="hero-inner shell pf-profile-hero__inner"><section class="hero-copy"><div class="pf-profile-hero__title-row"><aside class="pf-hero-symbol" aria-hidden="true"><span class="pf-hero-symbol__icon">{emoji}</span></aside><h1>{esc(name)}</h1></div><p class="pf-hero-dates">{esc(dates)}</p><div class="hero-tags"><span class="hero-tag gold">{esc(country)}</span>
<span class="hero-tag">{esc(category_tag)}</span></div></section></div></header><main class="pf-main" id="content"><div class="content-grid"><div class="main-col">
<div class="section-card"><h2 class="section-title"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>{esc(name)} {u["about"]}</h2>
  <div class="prose pf-profile-article"><h3>{esc(u["life"])}</h3><p>{esc(life)}</p><h3>{esc(u["work"])}</h3><p>{esc(work)}</p><h3>{esc(u["impact"])}</h3><p>{esc(impact)}</p></div>
</div>
<div class="section-card"><h2 class="section-title"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>{esc(u["works_title"])}</h2><ul class="works-list">{works_html(fig, lang)}</ul></div>
<div class="section-card"><h2 class="section-title"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>{esc(u["events_title"])}</h2>{events_html(fig, lang)}</div>
<div class="quote-block"><div class="quote-text">{esc(quote)}</div><div class="quote-source">{esc(quote_src)}</div></div>
<div class="section-card" id="qaynaqlar"><h2 class="section-title"><span aria-hidden="true">📚</span> {esc(u["sources_title"])}</h2><div class="prose"><p>{esc(u["sources_note"])}</p><ul class="source-links">{sources_html(fig, lang)}</ul></div></div>
</div><aside class="sidebar"><div class="info-card"><div class="info-title">{esc(u["info_title"])}</div><div class="info-row"><span class="info-label">{esc(u["full_name"])}</span><span class="info-val">{esc(name)}</span></div><div class="info-row"><span class="info-label">{esc(u["birth"])}</span><span class="info-val">{esc(birth)}</span></div><div class="info-row"><span class="info-label">{esc(u["death"])}</span><span class="info-val">{esc(death)}</span></div><div class="info-row"><span class="info-label">{esc(u["origin"])}</span><span class="info-val">{esc(country)}</span></div><div class="info-row"><span class="info-label">{esc(u["period"])}</span><span class="info-val">{esc(category_tag)}</span></div><div class="info-row"><span class="info-label">{esc(u["field"])}</span><span class="info-val">{esc(country)}, {esc(field)}</span></div><div class="info-divider"></div><div class="info-title">{esc(u["contrib_title"])}</div><ul class="contribution-list">{contributions_html(fig, lang)}</ul></div><div class="info-card"><div class="info-title">{esc(u["see_also"])}</div><a href="../../prominent_figures.html" class="nav-person-link"><div class="avatar">📚</div><div><div class="nav-person-name">{esc(u["catalog_link"])}</div><div class="nav-person-dates">{esc(category_tag)}</div></div></a></div></aside></div></div></main>
<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>{esc(u["footer_brand"])}</h3></div>
<div class="footer-grid">
<div class="footer-col"><div class="footer-title">{esc(u["footer_contact"])}</div><div class="footer-item"><span aria-hidden="true">✉</span> <a href="mailto:info@bilik-xezinesi.az">info@bilik-xezinesi.az</a></div><div class="footer-item"><span aria-hidden="true">🌐</span> <a href="https://bilik-xezinesi.az" target="_blank" rel="noopener noreferrer">bilik-xezinesi.az</a></div></div>
</div>
</div>
<div class="footer-bottom">{esc(u["footer_rights"])}</div>
</footer>
</body>
</html>
"""


def write_profile(fig: dict[str, Any], lang: str) -> Path:
    slug = fig["slug"]
    category = fig["category"]
    out = ROOT / lang / "prominent_figures" / category / f"{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_profile(fig, lang), encoding="utf-8", newline="\n")
    return out
