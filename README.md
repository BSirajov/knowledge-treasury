# Bilik xəzinəsi / Knowledge Treasury

Independent bilingual knowledge platform (AZ/EN) dedicated to collecting and presenting humanity's most influential scientific discoveries, inventions, innovations, and intellectual heritage — from ancient times to the present day.

This repository is a **standalone** static site. It does not depend on, link to, or share branding with any other web project.

## Contents

- **Home** (`az/index.html`, `en/index.html`)
- **Prominent Figures** — 201 profiles (`prominent_figures.html`)
- **Industrial Revolutions** — placeholder
- **Major Scientific Inventions** — 60 inventions (`en/scientific_inventions_research.html`)

## Local preview

```bat
START-SITE.bat
```

Or:

```bat
python helpers/serve_site.py --bind 127.0.0.1 --port 8020
```

Open http://localhost:8020/index.html

## Structure

- `az/`, `en/` — locale pages
- `css/`, `js/`, `images/` — shared Knowledge Treasury assets (`kt-*` naming)
- `i18n/` — navigation and UI strings
- `helpers/` — catalog build scripts (not deployed)

## Regenerate catalog after profile edits

```bat
python helpers/_build_prominent_figures_catalog.py
python helpers/_build_en_prominent_figures.py
```

## Independence audit

```bat
python helpers/_kt_independence_audit.py
```
