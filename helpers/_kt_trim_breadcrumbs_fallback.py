#!/usr/bin/env python3
"""Trim legacy DAAB-WAAS fallback data from kt-breadcrumbs.js."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

KT_FALLBACK_PAGES = """  var FALLBACK_ROUTES = {
    pages: [
      { id: "home", az: "az/index.html", en: "en/index.html", navParent: null },
      {
        id: "prominent-figures",
        az: "az/prominent_figures.html",
        en: "en/prominent_figures.html",
        navParent: null
      },
      {
        id: "industrial-revolutions",
        az: "az/industrial_revolutions.html",
        en: "en/industrial_revolutions.html",
        navParent: null
      },
      {
        id: "major-scientific-inventions",
        az: "en/scientific_inventions_research.html",
        en: "en/scientific_inventions_research.html",
        navParent: null
      },
      {
        id: "prominent-figure",
        az: "az/prominent_figures.html",
        en: "en/prominent_figures.html",
        navParent: null
      }
    ]
  };"""

KT_FALLBACK_UI = """  var FALLBACK_UI = {
    breadcrumbs: {
      az: {
        aria: "Səhifə yolu",
        home: "Ana səhifə",
        prominentFigures: "Görkəmli şəxsiyyətlər",
        industrialRevolutions: "Sənaye inqilabları",
        majorScientificInventions: "Əsas elmi ixtiralar",
        scientificInventionsResearch: "Elmi ixtiralar — tədqiqat"
      },
      en: {
        aria: "Breadcrumb",
        home: "Home",
        prominentFigures: "Prominent Figures",
        industrialRevolutions: "Industrial Revolutions",
        majorScientificInventions: "Major Scientific Inventions",
        scientificInventionsResearch: "Scientific Inventions Research"
      }
    },
    nav: {
      az: {
        home: "Ana səhifə",
        prominentFigures: "Görkəmli şəxsiyyətlər",
        industrialRevolutions: "Sənaye inqilabları",
        majorScientificInventions: "Əsas elmi ixtiralar",
        scientificInventionsResearch: "Elmi ixtiralar — tədqiqat"
      },
      en: {
        home: "Home",
        prominentFigures: "Prominent Figures",
        industrialRevolutions: "Industrial Revolutions",
        majorScientificInventions: "Major Scientific Inventions",
        scientificInventionsResearch: "Scientific Inventions Research"
      }
    }
  };"""


def main() -> None:
    path = ROOT / "js" / "kt-breadcrumbs.js"
    text = path.read_text(encoding="utf-8")

    text = re.sub(
        r"  var SKIP_BREADCRUMB_PAGE_IDS = \{[\s\S]*?\};",
        "  var SKIP_BREADCRUMB_PAGE_IDS = {};",
        text,
        count=1,
    )
    text = re.sub(
        r"  var GROUP_LABEL_KEYS = \{[\s\S]*?\};",
        "  var GROUP_LABEL_KEYS = {};",
        text,
        count=1,
    )
    text = re.sub(
        r"  var PRIMARY_GROUP_PARENTS = \{[\s\S]*?\};",
        "  var PRIMARY_GROUP_PARENTS = {};",
        text,
        count=1,
    )
    text = re.sub(
        r"  function usesForumHubCrumb\(page\) \{[\s\S]*?\n  \}",
        "  function usesForumHubCrumb() {\n    return false;\n  }",
        text,
        count=1,
    )
    text = re.sub(
        r"  var FALLBACK_ROUTES = \{[\s\S]*?\n  \};",
        KT_FALLBACK_PAGES,
        text,
        count=1,
    )
    text = re.sub(
        r"  var FALLBACK_UI = \{[\s\S]*?\n  \};",
        KT_FALLBACK_UI,
        text,
        count=1,
    )

    path.write_text(text, encoding="utf-8", newline="\n")
    print("Updated", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
