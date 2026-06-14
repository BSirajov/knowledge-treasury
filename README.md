# Bilik xəzinəsi / Knowledge Treasury

This web project is dedicated to collecting and presenting the most influential scientific discoveries, inventions, innovations, and other valuable knowledge from different fields of human activity throughout history — from ancient times to the present day.

Independent bilingual knowledge platform (AZ/EN), bootstrapped from the DAAB website Treasury section.

## Contents

- **Home** (`az/index.html`, `en/index.html`)
- **Prominent Figures** — 201 profiles (`encyclopedia.html`)
- **Industrial Revolutions** — placeholder
- **Major Scientific Inventions** — placeholder

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
- `css/`, `js/`, `images/` — shared assets
- `i18n/` — navigation and UI strings
- `helpers/` — catalog build scripts (not deployed)

## Regenerate catalog after profile edits

```bat
python helpers/_build_prominent_figures_catalog.py
python helpers/_build_en_prominent_figures.py
```
