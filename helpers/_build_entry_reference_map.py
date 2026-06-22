#!/usr/bin/env python3
"""Build slug -> reference-id mapping for per-article bibliographies."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_invention_entry_references.json"

# ref_id -> one or more entry slugs (curated from bottom bibliography)
REF_TO_SLUGS: dict[str, list[str]] = {
    # A. Books
    "a-books-and-major-scholarly-works:3": ["agriculture-and-domestication", "gunpowder"],
    "a-books-and-major-scholarly-works:4": ["the-printing-press"],
    "a-books-and-major-scholarly-works:5": ["quantum-mechanics", "electromagnetism"],
    "a-books-and-major-scholarly-works:6": ["controlled-use-of-fire", "agriculture-and-domestication"],
    "a-books-and-major-scholarly-works:9": ["the-compass", "mathematics-and-the-concept-of-zero"],
    "a-books-and-major-scholarly-works:10": [
        "semiconductor-technology",
        "integrated-circuit-microchip",
        "transistor",
    ],
    "a-books-and-major-scholarly-works:11": ["steam-engine"],
    "a-books-and-major-scholarly-works:13": ["nuclear-energy-and-nuclear-science"],
    "a-books-and-major-scholarly-works:14": ["agriculture-and-domestication"],
    "a-books-and-major-scholarly-works:15": ["telegraph"],
    "a-books-and-major-scholarly-works:16": ["the-microscope", "semiconductor-technology"],
    "a-books-and-major-scholarly-works:17": ["controlled-use-of-fire"],
    # B. Peer-reviewed
    "b-peer-reviewed-articles-and-original-scientific-papers:0": ["dna-structure-and-molecular-genetics"],
    "b-peer-reviewed-articles-and-original-scientific-papers:1": ["crispr-gene-editing"],
    "b-peer-reviewed-articles-and-original-scientific-papers:2": ["x-rays-and-medical-imaging"],
    "b-peer-reviewed-articles-and-original-scientific-papers:3": ["vaccination"],
    "b-peer-reviewed-articles-and-original-scientific-papers:4": ["fibre-optic-communication"],
    "b-peer-reviewed-articles-and-original-scientific-papers:5": ["laser"],
    "b-peer-reviewed-articles-and-original-scientific-papers:6": ["integrated-circuit-microchip"],
    "b-peer-reviewed-articles-and-original-scientific-papers:7": ["blockchain"],
    "b-peer-reviewed-articles-and-original-scientific-papers:8": ["search-engines"],
    "b-peer-reviewed-articles-and-original-scientific-papers:9": ["x-rays-and-medical-imaging"],
    "b-peer-reviewed-articles-and-original-scientific-papers:10": ["dna-structure-and-molecular-genetics"],
    "b-peer-reviewed-articles-and-original-scientific-papers:11": ["human-genome-sequencing"],
    # C. Institutional
    "c-institutional-and-government-publications-and-reports:0": ["refrigeration"],
    "c-institutional-and-government-publications-and-reports:1": ["sanitation-and-clean-water-systems"],
    "c-institutional-and-government-publications-and-reports:2": [
        "electric-vehicles",
        "battery-technology",
    ],
    "c-institutional-and-government-publications-and-reports:3": ["renewable-energy-technologies"],
    "c-institutional-and-government-publications-and-reports:4": ["nuclear-energy-and-nuclear-science"],
    "c-institutional-and-government-publications-and-reports:5": ["spaceflight"],
    "c-institutional-and-government-publications-and-reports:6": ["human-genome-sequencing"],
    "c-institutional-and-government-publications-and-reports:7": ["social-media-platforms"],
    "c-institutional-and-government-publications-and-reports:8": ["sanitation-and-clean-water-systems"],
    "c-institutional-and-government-publications-and-reports:9": ["vaccination"],
    "c-institutional-and-government-publications-and-reports:10": ["antibiotics"],
    "c-institutional-and-government-publications-and-reports:11": ["vaccination"],
    "c-institutional-and-government-publications-and-reports:12": ["plastics-and-synthetic-materials"],
    "c-institutional-and-government-publications-and-reports:13": ["renewable-energy-technologies"],
    "c-institutional-and-government-publications-and-reports:14": ["artificial-intelligence"],
    # D. Museum / archive (skip d:9 — cited throughout)
    "d-museum-archive-and-library-resources:0": ["the-printing-press"],
    "d-museum-archive-and-library-resources:1": ["newtonian-mechanics"],
    "d-museum-archive-and-library-resources:2": ["transistor"],
    "d-museum-archive-and-library-resources:3": ["integrated-circuit-microchip"],
    "d-museum-archive-and-library-resources:4": ["computer", "smartphones"],
    "d-museum-archive-and-library-resources:5": ["theory-of-relativity"],
    "d-museum-archive-and-library-resources:6": ["automobile"],
    "d-museum-archive-and-library-resources:7": ["telephone"],
    "d-museum-archive-and-library-resources:8": ["anaesthesia"],
    "d-museum-archive-and-library-resources:10": ["newtonian-mechanics"],
    "d-museum-archive-and-library-resources:11": ["steam-engine", "internal-combustion-engine"],
    "d-museum-archive-and-library-resources:12": ["airplane"],
    "d-museum-archive-and-library-resources:13": [
        "vaccination",
        "anaesthesia",
        "x-rays-and-medical-imaging",
    ],
    # E. Documentary
    "e-documentary-films-and-broadcast-media:0": ["computer"],
    "e-documentary-films-and-broadcast-media:1": ["newtonian-mechanics"],
    "e-documentary-films-and-broadcast-media:2": ["dna-structure-and-molecular-genetics"],
    "e-documentary-films-and-broadcast-media:3": ["antibiotics"],
    "e-documentary-films-and-broadcast-media:4": ["mathematics-and-the-concept-of-zero"],
    "e-documentary-films-and-broadcast-media:5": ["radio"],
    "e-documentary-films-and-broadcast-media:6": ["nuclear-energy-and-nuclear-science"],
    "e-documentary-films-and-broadcast-media:7": ["fertilisers-and-modern-agricultural-chemistry"],
    "e-documentary-films-and-broadcast-media:8": ["vaccination"],
    "e-documentary-films-and-broadcast-media:9": ["electricity-generation-and-distribution"],
    "e-documentary-films-and-broadcast-media:10": ["human-genome-sequencing"],
    "e-documentary-films-and-broadcast-media:11": ["internet"],
    "e-documentary-films-and-broadcast-media:12": ["social-media-platforms"],
    # F. Video / TED
    "f-online-video-lectures-ted-talks-and-educational-series:0": ["3d-printing-additive-manufacturing"],
    "f-online-video-lectures-ted-talks-and-educational-series:1": ["world-wide-web"],
    "f-online-video-lectures-ted-talks-and-educational-series:2": ["crispr-gene-editing"],
    "f-online-video-lectures-ted-talks-and-educational-series:3": ["renewable-energy-technologies"],
    "f-online-video-lectures-ted-talks-and-educational-series:4": ["controlled-use-of-fire"],
    "f-online-video-lectures-ted-talks-and-educational-series:5": ["computer"],
    "f-online-video-lectures-ted-talks-and-educational-series:6": ["steam-engine"],
    "f-online-video-lectures-ted-talks-and-educational-series:7": ["the-scientific-method"],
    "f-online-video-lectures-ted-talks-and-educational-series:8": ["quantum-mechanics"],
    "f-online-video-lectures-ted-talks-and-educational-series:9": ["theory-of-relativity"],
    "f-online-video-lectures-ted-talks-and-educational-series:10": ["agriculture-and-domestication"],
    "f-online-video-lectures-ted-talks-and-educational-series:11": ["the-periodic-table"],
    "f-online-video-lectures-ted-talks-and-educational-series:12": ["the-microscope"],
    "f-online-video-lectures-ted-talks-and-educational-series:13": ["the-printing-press"],
    "f-online-video-lectures-ted-talks-and-educational-series:14": ["vaccination"],
    "f-online-video-lectures-ted-talks-and-educational-series:15": ["mathematics-and-the-concept-of-zero"],
    "f-online-video-lectures-ted-talks-and-educational-series:16": ["writing-systems"],
    "f-online-video-lectures-ted-talks-and-educational-series:17": ["transistor"],
    "f-online-video-lectures-ted-talks-and-educational-series:18": ["agriculture-and-domestication"],
    "f-online-video-lectures-ted-talks-and-educational-series:19": ["blockchain"],
    # G. Space / physics labs
    "g-space-agencies-physics-laboratories-and-major-scientific-resources:0": ["world-wide-web"],
    "g-space-agencies-physics-laboratories-and-major-scientific-resources:1": ["world-wide-web"],
    "g-space-agencies-physics-laboratories-and-major-scientific-resources:2": ["artificial-intelligence"],
    "g-space-agencies-physics-laboratories-and-major-scientific-resources:3": ["satellite-technology"],
    "g-space-agencies-physics-laboratories-and-major-scientific-resources:4": ["the-telescope"],
    "g-space-agencies-physics-laboratories-and-major-scientific-resources:5": ["the-telescope", "theory-of-relativity"],
    "g-space-agencies-physics-laboratories-and-major-scientific-resources:6": ["crispr-gene-editing"],
    "g-space-agencies-physics-laboratories-and-major-scientific-resources:7": ["theory-of-relativity"],
    "g-space-agencies-physics-laboratories-and-major-scientific-resources:8": ["airplane"],
    "g-space-agencies-physics-laboratories-and-major-scientific-resources:9": ["satellite-technology"],
    "g-space-agencies-physics-laboratories-and-major-scientific-resources:10": ["x-rays-and-medical-imaging"],
    "g-space-agencies-physics-laboratories-and-major-scientific-resources:11": ["the-telescope"],
    # H. Professional societies (skip h:10 — cited throughout)
    "h-professional-societies-standards-bodies-and-academic-databases:0": ["laser"],
    "h-professional-societies-standards-bodies-and-academic-databases:1": ["dna-structure-and-molecular-genetics"],
    "h-professional-societies-standards-bodies-and-academic-databases:2": ["the-microscope"],
    "h-professional-societies-standards-bodies-and-academic-databases:3": ["electricity-generation-and-distribution"],
    "h-professional-societies-standards-bodies-and-academic-databases:4": ["telephone"],
    "h-professional-societies-standards-bodies-and-academic-databases:5": ["robotics"],
    "h-professional-societies-standards-bodies-and-academic-databases:6": ["the-periodic-table"],
    "h-professional-societies-standards-bodies-and-academic-databases:7": ["germ-theory-of-disease"],
    "h-professional-societies-standards-bodies-and-academic-databases:8": ["mathematics-and-the-concept-of-zero"],
    "h-professional-societies-standards-bodies-and-academic-databases:9": ["radio"],
    "h-professional-societies-standards-bodies-and-academic-databases:11": ["electromagnetism"],
    "h-professional-societies-standards-bodies-and-academic-databases:12": ["the-microscope"],
    "h-professional-societies-standards-bodies-and-academic-databases:13": ["the-periodic-table"],
    "h-professional-societies-standards-bodies-and-academic-databases:14": [
        "fertilisers-and-modern-agricultural-chemistry"
    ],
    "h-professional-societies-standards-bodies-and-academic-databases:15": ["plastics-and-synthetic-materials"],
    "h-professional-societies-standards-bodies-and-academic-databases:16": ["the-scientific-method"],
    # I. Data / infrastructure
    "i-data-visualisation-mapping-and-infrastructure-resources:0": ["cloud-computing"],
    "i-data-visualisation-mapping-and-infrastructure-resources:1": ["semiconductor-technology"],
    "i-data-visualisation-mapping-and-infrastructure-resources:2": ["blockchain"],
    "i-data-visualisation-mapping-and-infrastructure-resources:3": ["robotics"],
    "i-data-visualisation-mapping-and-infrastructure-resources:4": ["fibre-optic-communication"],
    "i-data-visualisation-mapping-and-infrastructure-resources:5": ["gps-global-positioning-system"],
    "i-data-visualisation-mapping-and-infrastructure-resources:6": ["search-engines"],
    "i-data-visualisation-mapping-and-infrastructure-resources:7": ["internet"],
    "i-data-visualisation-mapping-and-infrastructure-resources:8": [
        "internet",
        "fibre-optic-communication",
    ],
    "i-data-visualisation-mapping-and-infrastructure-resources:9": ["world-wide-web"],
    # J. Press / popular
    "j-press-popular-science-and-general-reference:0": ["agriculture-and-domestication"],
    "j-press-popular-science-and-general-reference:1": ["paper"],
    "j-press-popular-science-and-general-reference:2": ["refrigeration"],
    "j-press-popular-science-and-general-reference:3": ["the-wheel"],
    "j-press-popular-science-and-general-reference:4": ["3d-printing-additive-manufacturing"],
    "j-press-popular-science-and-general-reference:5": ["telegraph"],
    "j-press-popular-science-and-general-reference:6": ["x-rays-and-medical-imaging"],
    "j-press-popular-science-and-general-reference:7": ["writing-systems"],
    "j-press-popular-science-and-general-reference:8": ["agriculture-and-domestication"],
    "j-press-popular-science-and-general-reference:9": ["crispr-gene-editing"],
    "j-press-popular-science-and-general-reference:10": ["semiconductor-technology"],
    "j-press-popular-science-and-general-reference:11": ["controlled-use-of-fire"],
}

ALL_SLUGS = [
    "controlled-use-of-fire",
    "agriculture-and-domestication",
    "the-wheel",
    "writing-systems",
    "mathematics-and-the-concept-of-zero",
    "paper",
    "the-compass",
    "gunpowder",
    "the-printing-press",
    "the-scientific-method",
    "the-telescope",
    "the-microscope",
    "newtonian-mechanics",
    "steam-engine",
    "electricity-generation-and-distribution",
    "electromagnetism",
    "internal-combustion-engine",
    "automobile",
    "airplane",
    "refrigeration",
    "vaccination",
    "antibiotics",
    "germ-theory-of-disease",
    "anaesthesia",
    "x-rays-and-medical-imaging",
    "sanitation-and-clean-water-systems",
    "dna-structure-and-molecular-genetics",
    "human-genome-sequencing",
    "crispr-gene-editing",
    "the-periodic-table",
    "quantum-mechanics",
    "theory-of-relativity",
    "nuclear-energy-and-nuclear-science",
    "plastics-and-synthetic-materials",
    "fertilisers-and-modern-agricultural-chemistry",
    "telegraph",
    "telephone",
    "radio",
    "transistor",
    "integrated-circuit-microchip",
    "computer",
    "internet",
    "world-wide-web",
    "search-engines",
    "satellite-technology",
    "gps-global-positioning-system",
    "semiconductor-technology",
    "laser",
    "fibre-optic-communication",
    "spaceflight",
    "smartphones",
    "social-media-platforms",
    "artificial-intelligence",
    "renewable-energy-technologies",
    "battery-technology",
    "electric-vehicles",
    "robotics",
    "3d-printing-additive-manufacturing",
    "blockchain",
    "cloud-computing",
]


def main() -> None:
    slug_to_refs: dict[str, list[str]] = defaultdict(list)
    for ref_id, slugs in REF_TO_SLUGS.items():
        for slug in slugs:
            if ref_id not in slug_to_refs[slug]:
                slug_to_refs[slug].append(ref_id)

    # Preserve bibliography order within each entry
    refs_json = json.loads((ROOT / "_all_refs.json").read_text(encoding="utf-8"))
    ref_order = {r["id"]: i for i, r in enumerate(refs_json)}

    missing = [s for s in ALL_SLUGS if s not in slug_to_refs or not slug_to_refs[s]]
    if missing:
        raise SystemExit(f"Entries without references: {missing}")

    payload = {
        "_comment": "Maps invention entry slugs to bottom-bibliography ref IDs (group-slug:index).",
        "entries": {
            slug: sorted(slug_to_refs[slug], key=lambda rid: ref_order.get(rid, 9999))
            for slug in ALL_SLUGS
        },
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(ALL_SLUGS)} entries)")

    assigned = {rid for ids in slug_to_refs.values() for rid in ids}
    all_ids = {r["id"] for r in refs_json}
    unassigned = sorted(all_ids - assigned)
    print(f"Assigned {len(assigned)} / {len(all_ids)} references to entries")
    if unassigned:
        print("General / document-wide refs (bottom bibliography only):")
        for rid in unassigned:
            text = next(r["text"][:70] for r in refs_json if r["id"] == rid)
            print(f"  {rid}: {text}...")


if __name__ == "__main__":
    main()
