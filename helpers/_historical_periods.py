"""Canonical historical period taxonomy and classification helpers."""
from __future__ import annotations

import re
from typing import Iterable

# Unified period slugs used by inventions catalogues (filters store slug values).
PERIOD_SLUGS: tuple[str, ...] = (
    "prehistory",
    "ancient",
    "classical",
    "medieval",
    "renaissance",
    "early-modern",
    "industrial",
    "modern",
    "contemporary",
)

PERIOD_LABELS_EN: dict[str, str] = {
    "prehistory": "Prehistoric Era",
    "ancient": "Ancient World",
    "classical": "Classical Antiquity",
    "medieval": "Middle Ages",
    "renaissance": "Renaissance",
    "early-modern": "Early Modern Period",
    "industrial": "Industrial Age",
    "modern": "Modern Era",
    "contemporary": "Contemporary Period",
}

PERIOD_LABELS_AZ: dict[str, str] = {
    "prehistory": "Tarix öncəsi dövr",
    "ancient": "Qədim dünya",
    "classical": "Klassik antik dövr",
    "medieval": "Orta əsrlər",
    "renaissance": "İntibah dövrü",
    "early-modern": "Erkən yeni dövr",
    "industrial": "Sənaye dövrü",
    "modern": "Müasir dövr",
    "contemporary": "Çağdaş dövr",
}

# Back-compat alias used by inventions builders.
PERIOD_LABELS = PERIOD_LABELS_EN

PERIOD_RANK: dict[str, int] = {slug: idx for idx, slug in enumerate(PERIOD_SLUGS, start=1)}

# Prominent figures catalogue stores display labels (EN / AZ) in data-period.
PF_PERIOD_SLUG_BY_EN: dict[str, str] = {label: slug for slug, label in PERIOD_LABELS_EN.items()}
PF_PERIOD_EN_BY_SLUG: dict[str, str] = dict(PERIOD_LABELS_EN)
PF_PERIOD_AZ_BY_SLUG: dict[str, str] = dict(PERIOD_LABELS_AZ)

# Legacy PF labels mapped to new slugs for migration.
PF_LEGACY_EN_TO_SLUG: dict[str, str] = {
    "Antiquity": "classical",
    "Middle Ages": "medieval",
    "Modern era": "early-modern",
    "Contemporary era": "contemporary",
    **PF_PERIOD_SLUG_BY_EN,
}

PF_LEGACY_AZ_TO_SLUG: dict[str, str] = {
    "Antik dövr": "classical",
    "Orta əsrlər": "medieval",
    "Yeni dövr": "early-modern",
    "Müasir dövr": "modern",
    "Çağdaş dövr": "contemporary",
    **{label: slug for slug, label in PF_PERIOD_AZ_BY_SLUG.items()},
}

# Scholarly overrides where automated inference from span text is unreliable.
INVENTION_PERIOD_OVERRIDES: dict[str, str] = {
    "controlled-use-of-fire": "prehistory",
    "agriculture-and-domestication": "prehistory",
    "the-wheel": "ancient",
    "writing-systems": "ancient",
    "mathematics-and-the-concept-of-zero": "classical",
    "paper": "classical",
    "the-compass": "medieval",
    "gunpowder": "medieval",
    "the-printing-press": "renaissance",
    "the-scientific-method": "renaissance",
    "the-telescope": "early-modern",
    "the-microscope": "early-modern",
    "newtonian-mechanics": "early-modern",
    "steam-engine": "industrial",
    "electricity-generation-and-distribution": "industrial",
    "electromagnetism": "industrial",
    "internal-combustion-engine": "industrial",
    "automobile": "industrial",
    "airplane": "modern",
    "refrigeration": "industrial",
    "vaccination": "industrial",
    "antibiotics": "modern",
    "germ-theory-of-disease": "industrial",
    "anaesthesia": "industrial",
    "x-rays-and-medical-imaging": "modern",
    "sanitation-and-clean-water-systems": "industrial",
    "dna-structure-and-molecular-genetics": "modern",
    "human-genome-sequencing": "contemporary",
    "crispr-gene-editing": "contemporary",
    "the-periodic-table": "industrial",
    "quantum-mechanics": "modern",
    "theory-of-relativity": "modern",
    "nuclear-energy-and-nuclear-science": "modern",
    "plastics-and-synthetic-materials": "modern",
    "fertilisers-and-modern-agricultural-chemistry": "modern",
    "telegraph": "industrial",
    "telephone": "industrial",
    "radio": "modern",
    "semiconductor-technology": "modern",
    "transistor": "modern",
    "integrated-circuit-microchip": "modern",
    "computer": "modern",
    "internet": "modern",
    "world-wide-web": "contemporary",
    "satellite-technology": "modern",
    "gps-global-positioning-system": "contemporary",
    "laser": "modern",
    "fibre-optic-communication": "modern",
    "artificial-intelligence": "contemporary",
    "renewable-energy-technologies": "contemporary",
    "battery-technology": "modern",
    "electric-vehicles": "contemporary",
    "robotics": "modern",
    "3d-printing-additive-manufacturing": "contemporary",
    "blockchain": "contemporary",
    "cloud-computing": "contemporary",
    "smartphones": "contemporary",
    "social-media-platforms": "contemporary",
    "search-engines": "contemporary",
    "spaceflight": "modern",
}

YEAR_RANGE_WITH_ERA_RE = re.compile(
    r"(?:c\.|ca\.|circa\s*)?"
    r"(\d{1,3}(?:,\d{3})*|\d{3,4})\s*"
    r"[–—-]\s*"
    r"(\d{1,3}(?:,\d{3})*|\d{3,4})\s*"
    r"(BCE|BC|CE|AD)?\b",
    re.I,
)
YEAR_WITH_ERA_RE = re.compile(
    r"(?:c\.|ca\.|circa\s*)?"
    r"(\d{1,3}(?:,\d{3})*|\d{3,4})\s*"
    r"(BCE|BC|CE|AD)?\b",
    re.I,
)
DECADE_RE = re.compile(r"\b(\d{3})0s\b", re.I)
CENTURY_RE = re.compile(
    r"\b(\d{1,2})(?:st|nd|rd|th)?\s*centur(?:y|ies)\b|"
    r"\b(\d{1,2})\s*(?:-ci|-cü|-cu|-cü|-nci|-ncü|-ncu|-ncü)\s*əsr\b",
    re.I,
)
FOUR_DIGIT_YEAR_RE = re.compile(r"\b(1[0-9]{3}|20[0-2]\d)\b")
ORDINAL_CENTURY_WORD_RE = re.compile(
    r"\b([IVXLCDM]{1,4}|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|"
    r"eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|"
    r"nineteenth|twentieth|twenty[- ]first)\s+century\b",
    re.I,
)
ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
WORD_CENTURY = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
    "tenth": 10,
    "eleventh": 11,
    "twelfth": 12,
    "thirteenth": 13,
    "fourteenth": 14,
    "fifteenth": 15,
    "sixteenth": 16,
    "seventeenth": 17,
    "eighteenth": 18,
    "nineteenth": 19,
    "twentieth": 20,
    "twenty-first": 21,
    "twenty first": 21,
}


def _roman_to_int(value: str) -> int | None:
    text = value.upper()
    if not text or any(ch not in ROMAN for ch in text):
        return None
    total = 0
    prev = 0
    for ch in reversed(text):
        num = ROMAN[ch]
        if num < prev:
            total -= num
        else:
            total += num
            prev = num
    return total or None


def _century_midyear(century: int) -> int:
    return max(1, (century - 1) * 100 + 50)


def extract_years(text: str) -> list[int]:
    """Extract plausible calendar years from catalogue metadata text."""
    raw = text or ""
    years: list[int] = []

    if re.search(r"million|400,000|1,000,000", raw, re.I):
        years.append(-1_000_000)

    for m in YEAR_RANGE_WITH_ERA_RE.finditer(raw):
        era = (m.group(3) or "").upper()
        for idx in (1, 2):
            digits = m.group(idx).replace(",", "")
            if not digits.isdigit():
                continue
            year = int(digits)
            if era in {"BCE", "BC"}:
                year = -year
            elif year < 100 and era not in {"CE", "AD"}:
                continue
            years.append(year)

    for m in YEAR_WITH_ERA_RE.finditer(raw):
        digits = m.group(1).replace(",", "")
        if not digits.isdigit():
            continue
        year = int(digits)
        era = (m.group(2) or "").upper()
        if era in {"BCE", "BC"}:
            year = -year
        elif year < 100 and era not in {"CE", "AD"}:
            continue
        if year > 3000 and era not in {"CE", "AD"}:
            continue
        years.append(year)

    for m in DECADE_RE.finditer(raw):
        years.append(int(m.group(1)) * 10)

    for m in CENTURY_RE.finditer(raw):
        century = int(m.group(1) or m.group(2))
        if 1 <= century <= 21:
            year = _century_midyear(century)
            tail = raw[m.end() : m.end() + 16]
            if re.search(r"\b(BCE|BC)\b", tail, re.I):
                year = -year
            years.append(year)

    for m in ORDINAL_CENTURY_WORD_RE.finditer(raw):
        token = m.group(1).lower().replace(" ", "-")
        if token in WORD_CENTURY:
            years.append(_century_midyear(WORD_CENTURY[token]))
        else:
            century = _roman_to_int(token)
            if century:
                years.append(_century_midyear(century))

    # Prefer explicit 4-digit years in the Period clause.
    period_m = re.search(r"Period:\s*([^|]+)", raw, re.I)
    segment = period_m.group(1) if period_m else raw[:160]
    for m in FOUR_DIGIT_YEAR_RE.finditer(segment):
        years.append(int(m.group(1)))

    return years


def anchor_year(text: str, years: Iterable[int] | None = None) -> int | None:
    """Pick the best representative year for period classification."""
    values = list(years if years is not None else extract_years(text))
    if not values:
        return None

    period_m = re.search(r"Period:\s*([^|]+)", text or "", re.I)
    segment = period_m.group(1) if period_m else (text or "")[:200]
    segment_years = extract_years(f"Period: {segment}")

    pool = segment_years or values
    if re.search(r"\b(BCE|BC)\b", text or "", re.I):
        bce_only = [y for y in pool if y < 0]
        if bce_only:
            return min(bce_only)

    deep_prehistory = [y for y in pool if y <= -100_000]
    if deep_prehistory:
        return min(deep_prehistory)

    bce = [y for y in pool if y < 0]
    ce = [y for y in pool if y > 0]

    if ce and bce:
        # Multi-era entries: classify by emergence / first major milestone (earliest CE).
        return min(ce)
    if bce:
        return min(bce)
    if ce:
        return min(ce)
    return min(pool)


def slug_from_year(year: int) -> str:
    if year < -3000:
        return "prehistory"
    if year < -800:
        return "ancient"
    if year < 500:
        return "classical"
    if year < 1400:
        return "medieval"
    if year < 1600:
        return "renaissance"
    if year < 1750:
        return "early-modern"
    if year < 1914:
        return "industrial"
    if year < 2000:
        return "modern"
    return "contemporary"


def infer_period_slug(
    text: str,
    milestones: list[str] | None = None,
    *,
    slug: str | None = None,
) -> str:
    if slug and slug in INVENTION_PERIOD_OVERRIDES:
        return INVENTION_PERIOD_OVERRIDES[slug]

    blob = " ".join([text or "", *(milestones or [])]).strip()
    year = anchor_year(blob)
    if year is None:
        return "modern"
    return slug_from_year(year)


def infer_pf_period_az(dates: str, birth_val: str, year: int | None) -> str:
    """Return Azerbaijani period label for prominent figures."""
    slug = infer_pf_period_slug(dates, birth_val, year)
    return PF_PERIOD_AZ_BY_SLUG[slug]


def infer_pf_period_en(dates: str, birth_val: str, year: int | None) -> str:
    slug = infer_pf_period_slug(dates, birth_val, year)
    return PF_PERIOD_EN_BY_SLUG[slug]


def infer_pf_period_slug(dates: str, birth_val: str, year: int | None) -> str:
    combined = f"{dates} {birth_val}".strip()
    lower = combined.lower()

    if any(token in lower for token in ("milli", "əfsanəvi", "legendary", "mythic")):
        return "ancient"

    resolved = year
    if resolved is None:
        years = extract_years(combined)
        resolved = anchor_year(combined, years)

    if resolved is None:
        if any(token in lower for token in ("bce", "bc", "e.ə", "ə.e", "e.e")):
            return "classical"
        return "modern"

    if resolved < 0:
        return slug_from_year(resolved)

    return slug_from_year(resolved)


def period_rank(slug: str) -> int:
    return PERIOD_RANK.get(slug, 999)
