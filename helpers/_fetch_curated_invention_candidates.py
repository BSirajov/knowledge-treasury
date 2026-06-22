#!/usr/bin/env python3
"""Download hand-curated free-licensed candidate images for missing invention icons."""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMP = ROOT / "images" / "temp"
MANIFEST = TEMP / "candidate-images-manifest.json"
USER_AGENT = "KnowledgeTreasuryBot/1.0 (image research; contact: info@bilik-xezinesi.az)"

# Curated Wikimedia / Openverse sources chosen for relevance + clear license.
CURATED = [
    {
        "section": "1.1 Controlled Use of Fire",
        "section_id": "controlled-use-of-fire",
        "filename": "controlled-use-of-fire.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Campfire_icon_(Pixabay_1345870).png",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Campfire_icon_%28Pixabay_1345870%29.png/960px-Campfire_icon_%28Pixabay_1345870%29.png",
        "license": "CC0 1.0 (Pixabay / Creative Commons Zero)",
        "artist": "Elionas (via Pixabay)",
    },
    {
        "section": "1.2 Agriculture and Domestication",
        "section_id": "agriculture-and-domestication",
        "filename": "agriculture-and-domestication.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Early_farming.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Early_farming.jpg/1280px-Early_farming.jpg",
        "license": "Public domain (USDA)",
        "artist": "U.S. Department of Agriculture",
    },
    {
        "section": "1.3 The Wheel",
        "section_id": "the-wheel",
        "filename": "the-wheel.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Potters_wheel_in_Ishwa,_Rwanda.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Potters_wheel_in_Ishwa%2C_Rwanda.jpg/1280px-Potters_wheel_in_Ishwa%2C_Rwanda.jpg",
        "license": "CC BY-SA 3.0",
        "artist": "Dr. Avishai Teicher",
    },
    {
        "section": "1.4 Writing Systems",
        "section_id": "writing-systems",
        "filename": "writing-systems.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Cuneiform_tablet-_fragment_of_a_letter_from_Ashurbanipal_to_the_Babylonian_citizens_Wellcome_L0057894.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Cuneiform_tablet-_fragment_of_a_letter_from_Ashurbanipal_to_the_Babylonian_citizens_Wellcome_L0057894.jpg/1280px-Cuneiform_tablet-_fragment_of_a_letter_from_Ashurbanipal_to_the_Babylonian_citizens_Wellcome_L0057894.jpg",
        "license": "CC BY 4.0",
        "artist": "Wellcome Collection",
    },
    {
        "section": "1.5 Mathematics and the Concept of Zero",
        "section_id": "mathematics-and-the-concept-of-zero",
        "filename": "mathematics-and-the-concept-of-zero.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:3D_Mandelbrot_set_slice.png",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/3D_Mandelbrot_set_slice.png/1280px-3D_Mandelbrot_set_slice.png",
        "license": "CC BY-SA 3.0",
        "artist": "Wolfgang Beyer",
    },
    {
        "section": "1.6 Paper",
        "section_id": "paper",
        "filename": "paper.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Paper_making_in_Xuan_Cheng,_China.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Paper_making_in_Xuan_Cheng%2C_China.jpg/1280px-Paper_making_in_Xuan_Cheng%2C_China.jpg",
        "license": "CC BY-SA 3.0",
        "artist": "Fanghong",
    },
    {
        "section": "1.7 The Compass",
        "section_id": "the-compass",
        "filename": "the-compass.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Compass.svg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Compass.svg/960px-Compass.svg.png",
        "license": "CC0 1.0",
        "artist": "Openclipart / public domain dedication",
    },
    {
        "section": "1.8 Gunpowder",
        "section_id": "gunpowder",
        "filename": "gunpowder.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Black_powder_for_muzzleloaders.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Black_powder_for_muzzleloaders.jpg/1280px-Black_powder_for_muzzleloaders.jpg",
        "license": "CC BY-SA 3.0",
        "artist": "Hans Hillewaert",
    },
    {
        "section": "1.9 The Printing Press",
        "section_id": "the-printing-press",
        "filename": "the-printing-press.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Gutenberg_Press.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Gutenberg_Press.jpg/1280px-Gutenberg_Press.jpg",
        "license": "Public domain",
        "artist": "Unknown (historical photograph)",
    },
    {
        "section": "2.1 The Scientific Method",
        "section_id": "the-scientific-method",
        "filename": "the-scientific-method.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Scientific_method.svg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Scientific_method.svg/960px-Scientific_method.svg.png",
        "license": "CC BY-SA 3.0",
        "artist": "ArchonMaid",
    },
    {
        "section": "2.2 The Telescope",
        "section_id": "the-telescope",
        "filename": "the-telescope.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Thirty_Meter_Telescope_Render_(7950_tio_tmt_EXPL_0087).jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Thirty_Meter_Telescope_Render_%287950_tio_tmt_EXPL_0087%29.jpg/1280px-Thirty_Meter_Telescope_Render_%287950_tio_tmt_EXPL_0087%29.jpg",
        "license": "CC BY 4.0",
        "artist": "NOIRLab/NSF/AURA",
    },
    {
        "section": "2.3 The Microscope",
        "section_id": "the-microscope",
        "filename": "the-microscope.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Microscope_(PSF).png",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Microscope_%28PSF%29.png/960px-Microscope_%28PSF%29.png",
        "license": "Public domain",
        "artist": "Pearson Scott Foresman (archival)",
    },
    {
        "section": "2.4 Newtonian Mechanics",
        "section_id": "newtonian-mechanics",
        "filename": "newtonian-mechanics.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Newton%27s_reflecting_telescope,_1668,_Replica,_Science_Museum,_London.JPG",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Newton%27s_reflecting_telescope%2C_1668%2C_Replica%2C_Science_Museum%2C_London.JPG/1280px-Newton%27s_reflecting_telescope%2C_1668%2C_Replica%2C_Science_Museum%2C_London.JPG",
        "license": "CC BY-SA 4.0",
        "artist": "Geni",
    },
    {
        "section": "3.1 Steam Engine",
        "section_id": "steam-engine",
        "filename": "steam-engine.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Steam_engine_in_action.gif",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Steam_engine_in_action.gif",
        "license": "Public domain",
        "artist": "Wikimedia contributor",
        "note": "Animated GIF; may need conversion to PNG for final use.",
    },
    {
        "section": "3.2 Electricity Generation and Distribution",
        "section_id": "electricity-generation-and-distribution",
        "filename": "electricity-generation-and-distribution.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Electricity_pylons_in_the_sunset.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Electricity_pylons_in_the_sunset.jpg/1280px-Electricity_pylons_in_the_sunset.jpg",
        "license": "CC BY 2.0",
        "artist": "Jürgen Mangelsdorf",
    },
    {
        "section": "3.3 Electromagnetism",
        "section_id": "electromagnetism",
        "filename": "electromagnetism.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Magnet_compasses.svg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Magnet_compasses.svg/960px-Magnet_compasses.svg.png",
        "license": "CC BY-SA 4.0",
        "artist": "Geek3",
    },
    {
        "section": "3.4 Internal Combustion Engine",
        "section_id": "internal-combustion-engine",
        "filename": "internal-combustion-engine.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Four_stroke_engine_diagram.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Four_stroke_engine_diagram.jpg/1280px-Four_stroke_engine_diagram.jpg",
        "license": "Public domain",
        "artist": "U.S. Federal Government / Wikimedia",
    },
    {
        "section": "3.5 Automobile",
        "section_id": "automobile",
        "filename": "automobile.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Ford_Model_T_1910.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Ford_Model_T_1910.jpg/1280px-Ford_Model_T_1910.jpg",
        "license": "Public domain",
        "artist": "Unknown",
    },
    {
        "section": "3.6 Airplane",
        "section_id": "airplane",
        "filename": "airplane.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Wright_Flyer_III_over_Huffman_Prairie.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Wright_Flyer_III_over_Huffman_Prairie.jpg/1280px-Wright_Flyer_III_over_Huffman_Prairie.jpg",
        "license": "Public domain",
        "artist": "Unknown",
    },
    {
        "section": "3.7 Refrigeration",
        "section_id": "refrigeration",
        "filename": "refrigeration.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Refrigerator_interior.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Refrigerator_interior.jpg/960px-Refrigerator_interior.jpg",
        "license": "CC BY-SA 3.0",
        "artist": "Mattes",
    },
    {
        "section": "4.1 Vaccination",
        "section_id": "vaccination",
        "filename": "vaccination.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:COVID-19_vaccination_in_Sweden_2021.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/COVID-19_vaccination_in_Sweden_2021.jpg/1280px-COVID-19_vaccination_in_Sweden_2021.jpg",
        "license": "CC BY-SA 4.0",
        "artist": "Frankie Fouganthin",
    },
    {
        "section": "4.2 Antibiotics",
        "section_id": "antibiotics",
        "filename": "antibiotics.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Penicillin_core.svg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Penicillin_core.svg/960px-Penicillin_core.svg.png",
        "license": "Public domain",
        "artist": "Ben Mills / Wikimedia",
    },
    {
        "section": "4.3 Germ Theory of Disease",
        "section_id": "germ-theory-of-disease",
        "filename": "germ-theory-of-disease.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:EscherichiaColi_NIAID.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/EscherichiaColi_NIAID.jpg/1280px-EscherichiaColi_NIAID.jpg",
        "license": "Public domain (NIH/NIAID)",
        "artist": "National Institute of Allergy and Infectious Diseases",
    },
    {
        "section": "4.4 Anaesthesia",
        "section_id": "anaesthesia",
        "filename": "anaesthesia.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Anaesthetic_machine.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Anaesthetic_machine.jpg/1280px-Anaesthetic_machine.jpg",
        "license": "CC BY-SA 3.0",
        "artist": "Rama",
    },
    {
        "section": "4.5 X-Rays and Medical Imaging",
        "section_id": "x-rays-and-medical-imaging",
        "filename": "x-rays-and-medical-imaging.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:X-ray_of_hand.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/X-ray_of_hand.jpg/960px-X-ray_of_hand.jpg",
        "license": "Public domain",
        "artist": "Unknown",
    },
    {
        "section": "4.6 Sanitation and Clean Water Systems",
        "section_id": "sanitation-and-clean-water-systems",
        "filename": "sanitation-and-clean-water-systems.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Clean_drinking_water.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Clean_drinking_water.jpg/1280px-Clean_drinking_water.jpg",
        "license": "CC BY 2.0",
        "artist": "U.S. Agency for International Development",
    },
    {
        "section": "4.7 DNA Structure and Molecular Genetics",
        "section_id": "dna-structure-and-molecular-genetics",
        "filename": "dna-structure-and-molecular-genetics.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:DNA_Double_Helix.png",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/DNA_Double_Helix.png/960px-DNA_Double_Helix.png",
        "license": "Public domain",
        "artist": "National Human Genome Research Institute",
    },
    {
        "section": "4.8 Human Genome Sequencing",
        "section_id": "human-genome-sequencing",
        "filename": "human-genome-sequencing.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:DNA_sequencing_454_GS_FLX.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/DNA_sequencing_454_GS_FLX.jpg/1280px-DNA_sequencing_454_GS_FLX.jpg",
        "license": "CC BY 2.0",
        "artist": "National Human Genome Research Institute",
    },
    {
        "section": "4.9 CRISPR Gene Editing",
        "section_id": "crispr-gene-editing",
        "filename": "crispr-gene-editing.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:CRISPR-Cas9_Editing_of_the_Genome_(26453307604).jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/CRISPR-Cas9_Editing_of_the_Genome_%2826453307604%29.jpg/1280px-CRISPR-Cas9_Editing_of_the_Genome_%2826453307604%29.jpg",
        "license": "CC BY 2.0",
        "artist": "National Human Genome Research Institute",
    },
    {
        "section": "5.1 The Periodic Table",
        "section_id": "the-periodic-table",
        "filename": "the-periodic-table.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Periodic_table.svg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Periodic_table.svg/1280px-Periodic_table.svg.png",
        "license": "Public domain",
        "artist": "Sandbh / Wikimedia community",
    },
    {
        "section": "5.2 Quantum Mechanics",
        "section_id": "quantum-mechanics",
        "filename": "quantum-mechanics.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Atomic_orbitals_n123_m-eigenstates.png",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Atomic_orbitals_n123_m-eigenstates.png/960px-Atomic_orbitals_n123_m-eigenstates.png",
        "license": "CC BY-SA 4.0",
        "artist": "Geek3",
    },
    {
        "section": "5.3 Theory of Relativity",
        "section_id": "theory-of-relativity",
        "filename": "theory-of-relativity.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Gravitational_lens-full.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Gravitational_lens-full.jpg/1280px-Gravitational_lens-full.jpg",
        "license": "Public domain (NASA/ESA)",
        "artist": "NASA, ESA, and Johan Richard",
    },
    {
        "section": "5.4 Nuclear Energy and Nuclear Science",
        "section_id": "nuclear-energy-and-nuclear-science",
        "filename": "nuclear-energy-and-nuclear-science.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Nuclear_power_plant_Cattenom.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Nuclear_power_plant_Cattenom.jpg/1280px-Nuclear_power_plant_Cattenom.jpg",
        "license": "CC BY-SA 3.0",
        "artist": "Amada44",
    },
    {
        "section": "5.5 Plastics and Synthetic Materials",
        "section_id": "plastics-and-synthetic-materials",
        "filename": "plastics-and-synthetic-materials.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Plastic_pollution.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Plastic_pollution.jpg/1280px-Plastic_pollution.jpg",
        "license": "CC BY-SA 4.0",
        "artist": "Bo Eide",
    },
    {
        "section": "5.6 Fertilisers and Modern Agricultural Chemistry",
        "section_id": "fertilisers-and-modern-agricultural-chemistry",
        "filename": "fertilisers-and-modern-agricultural-chemistry.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Ammonium_nitrate.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Ammonium_nitrate.jpg/1280px-Ammonium_nitrate.jpg",
        "license": "Public domain",
        "artist": "Unknown",
    },
    {
        "section": "7.1 Artificial Intelligence",
        "section_id": "artificial-intelligence",
        "filename": "artificial-intelligence.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Artificial_neural_network.svg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Artificial_neural_network.svg/960px-Artificial_neural_network.svg.png",
        "license": "CC BY-SA 3.0",
        "artist": "Cburnett",
    },
    {
        "section": "7.2 Renewable Energy Technologies",
        "section_id": "renewable-energy-technologies",
        "filename": "renewable-energy-technologies.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Wind_turbines_and_solar_panels.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Wind_turbines_and_solar_panels.jpg/1280px-Wind_turbines_and_solar_panels.jpg",
        "license": "CC BY-SA 3.0",
        "artist": "Petar Milošević",
    },
    {
        "section": "7.3 Battery Technology",
        "section_id": "battery-technology",
        "filename": "battery-technology.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Lithium-ion_battery.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Lithium-ion_battery.jpg/1280px-Lithium-ion_battery.jpg",
        "license": "CC BY-SA 3.0",
        "artist": "TeslaFan",
    },
    {
        "section": "7.4 Electric Vehicles",
        "section_id": "electric-vehicles",
        "filename": "electric-vehicles.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Tesla_Model_S_2012.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Tesla_Model_S_2012.jpg/1280px-Tesla_Model_S_2012.jpg",
        "license": "CC BY-SA 3.0",
        "artist": "Myth",
    },
    {
        "section": "7.5 Robotics",
        "section_id": "robotics",
        "filename": "robotics.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Industrial_robot_arm.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Industrial_robot_arm.jpg/1280px-Industrial_robot_arm.jpg",
        "license": "CC BY-SA 3.0",
        "artist": "Glogger",
    },
    {
        "section": "7.6 3D Printing (Additive Manufacturing)",
        "section_id": "3d-printing-additive-manufacturing",
        "filename": "3d-printing-additive-manufacturing.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:3D_printer_extruding.jpg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/3D_printer_extruding.jpg/1280px-3D_printer_extruding.jpg",
        "license": "CC BY-SA 3.0",
        "artist": "Zortrax",
    },
    {
        "section": "7.7 Blockchain",
        "section_id": "blockchain",
        "filename": "blockchain.png",
        "source_url": "https://commons.wikimedia.org/wiki/File:Blockchain.svg",
        "download_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Blockchain.svg/960px-Blockchain.svg.png",
        "license": "CC BY-SA 4.0",
        "artist": "Mysid",
    },
]


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    TEMP.mkdir(parents=True, exist_ok=True)
    manifest = []
    errors = []
    for item in CURATED:
        dest = TEMP / item["filename"]
        try:
            download(item["download_url"], dest)
            manifest.append(
                {
                    "section": item["section"],
                    "section_id": item["section_id"],
                    "placeholder_for": item["filename"],
                    "saved_as": f"images/temp/{item['filename']}",
                    "source_url": item["source_url"],
                    "download_url": item["download_url"],
                    "license": item["license"],
                    "artist": item["artist"],
                    "note": item.get("note", ""),
                }
            )
            print(f"OK {item['filename']}")
        except Exception as exc:  # noqa: BLE001
            errors.append({**item, "error": str(exc)})
            print(f"FAIL {item['filename']}: {exc}")

    MANIFEST.write_text(
        json.dumps({"candidates": manifest, "failures": errors}, indent=2),
        encoding="utf-8",
    )
    print(f"\nSaved {len(manifest)} / {len(CURATED)} to {TEMP}")


if __name__ == "__main__":
    main()
