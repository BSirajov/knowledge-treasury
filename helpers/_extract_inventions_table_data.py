#!/usr/bin/env python3
"""Extract invention infographic data from major_scientific_inventions.html."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "en" / "major_scientific_inventions.html"


def parse_inventions(html: str) -> list[dict]:
    entries = []
    pattern = re.compile(
        r'<article class="inventions-entry" id="([^"]+)"[^>]*data-search="([^"]*)"[^>]*>'
        r".*?"
        r'<span class="inventions-entry-num"[^>]*>([^<]+)</span>'
        r'<span class="inventions-entry-name">([^<]+)</span>'
        r".*?"
        r'<p class="inventions-entry-visual-figures"><strong>Key figure\(s\):</strong>\s*([^<]*)</p>'
        r'<p class="inventions-entry-visual-summary">([^<]*)</p>'
        r'.*?<div class="inventions-key-facts"><h4>Key facts</h4><ul>(.*?)</ul>',
        re.DOTALL,
    )
    for m in pattern.finditer(html):
        slug, data_search, num, name, figures, summary, facts_html = m.groups()
        facts = re.findall(r"<li>([^<]+)</li>", facts_html)
        period = ""
        pm = re.search(r"Period:\s*([^|]+)", data_search)
        if pm:
            period = pm.group(1).strip()
        entries.append(
            {
                "slug": slug,
                "num": num.strip(),
                "name": name.strip(),
                "period": period,
                "key_figures": figures.strip(),
                "summary": summary.strip(),
                "key_facts": facts,
            }
        )
    return entries


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    entries = parse_inventions(html)
    out = ROOT / "helpers" / "_inventions_table_data.json"
    out.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Parsed {len(entries)} entries -> {out}")
    for e in entries[:2]:
        print(json.dumps(e, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
