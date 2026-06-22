#!/usr/bin/env python3
"""Extract professionally corrected invention card copy from the inventions DOCX."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _build_inventions_page import meta_key_figures, parse_docx
from _paths import ROOT

DOCX = ROOT / "documents" / "Most_Influential_Scientific_Inventions_and_Innovations (with references).docx"
TABLE_DATA = ROOT / "helpers" / "_inventions_table_data.json"
OUT_JSON = ROOT / "helpers" / "_inventions_card_copy.json"

SIGNIFICANCE = "SCIENTIFIC / TECHNOLOGICAL SIGNIFICANCE"
HISTORICAL = "HISTORICAL CONTEXT"

SUMMARY_MAX = 200

# Model entries and other hand-polished summaries (docx-informed).
SUMMARY_OVERRIDES: dict[str, str] = {
    "controlled-use-of-fire": (
        "Fire evidence from Wonderwerk Cave, South Africa dates to ~1 million years ago. "
        "Deliberate control enabled cooking, warmth, and protection — reshaping human biology and culture."
    ),
    "the-wheel": (
        "The wheel appeared in Mesopotamia ~3500 BCE. The key insight was the axle, allowing free rotation. "
        "The wheel's principle underpins gears, turbines, engines, and all machinery."
    ),
    "anaesthesia": (
        "Morton's public demonstration of ether anaesthesia at Massachusetts General Hospital on "
        "16 October 1846 is the conventional start date. Chloroform anaesthesia, introduced by Simpson in 1847, "
        "transformed surgery worldwide."
    ),
    "artificial-intelligence": (
        "Deep learning's breakthrough (AlexNet, 2012) triggered the modern AI era. "
        "AlphaFold (2020) solved the 50-year protein structure problem; LLMs now write, code, and reason."
    ),
}

# Simplified key figures matching clean card style (meta is source of truth when absent).
KEY_FIGURES_OVERRIDES: dict[str, str] = {
    "controlled-use-of-fire": "Homo erectus; later Homo sapiens",
    "the-wheel": "Mesopotamia; Eurasian steppe (debated)",
    "anaesthesia": (
        "Crawford Long (ether, 1842); William Morton (1846); James Young Simpson (chloroform, 1847)"
    ),
    "artificial-intelligence": "Alan Turing; John McCarthy; Geoffrey Hinton; Yann LeCun; Yoshua Bengio",
    "agriculture-and-domestication": (
        "Multiple independent centres: Fertile Crescent, China, Mesoamerica, Africa"
    ),
    "writing-systems": (
        "Sumer (cuneiform); Egypt (hieroglyphs); China and Mesoamerica (independent inventions)"
    ),
    "mathematics-and-the-concept-of-zero": (
        "Babylonian, Egyptian, Indian (Brahmagupta), and Maya mathematicians"
    ),
    "paper": "Cai Lun (Han Dynasty China); later Islamic and European paper mills",
    "the-compass": "Han Dynasty China; independently developed in Europe c. 12th century",
    "gunpowder": (
        "Chinese alchemists (Tang Dynasty); spread to Islamic world and Europe by 13th century"
    ),
    "the-printing-press": (
        "Johannes Gutenberg (Europe); Bi Sheng (China, c. 1040 CE, earlier movable type)"
    ),
    "the-scientific-method": (
        "Ibn al-Haytham (optics, c. 1021); Francis Bacon; Galileo Galilei; René Descartes"
    ),
    "the-telescope": (
        "Hans Lipperhey (inventor, Netherlands); Galileo Galilei (first systematic astronomical use)"
    ),
    "the-microscope": (
        "Zacharias Janssen (compound microscope, c. 1590); Antoni van Leeuwenhoek (high-power single-lens)"
    ),
    "steam-engine": (
        "Thomas Newcomen; James Watt (improved design); Richard Trevithick (high-pressure steam)"
    ),
    "electricity-generation-and-distribution": (
        "Michael Faraday; Thomas Edison; Nikola Tesla; George Westinghouse"
    ),
    "electromagnetism": "Hans Christian Ørsted; André-Marie Ampère; Michael Faraday; James Clerk Maxwell",
    "internal-combustion-engine": "Étienne Lenoir; Nikolaus Otto (four-stroke cycle, 1876); Rudolf Diesel (1897)",
    "automobile": "Karl Benz; Gottlieb Daimler; Henry Ford (mass production)",
    "airplane": (
        "Orville and Wilbur Wright; later: Louis Blériot, Anthony Fokker, Frank Whittle (jet engine)"
    ),
    "refrigeration": "Jacob Perkins; Carl von Linde; Clarence Birdseye (commercial frozen food)",
    "vaccination": "Edward Jenner (smallpox); Louis Pasteur (rabies, cholera); Jonas Salk (polio)",
    "antibiotics": (
        "Alexander Fleming (discovery, 1928); Howard Florey and Ernst Chain (development, 1940s)"
    ),
    "germ-theory-of-disease": "Louis Pasteur; Robert Koch; Ignaz Semmelweis; John Snow",
    "x-rays-and-medical-imaging": (
        "Wilhelm Conrad Röntgen (X-rays, 1895); Godfrey Hounsfield and Allan Cormack (CT, 1971)"
    ),
    "sanitation-and-clean-water-systems": (
        "Joseph Bazalgette (London sewers); Edwin Chadwick; John Snow; Lemuel Shattuck"
    ),
    "dna-structure-and-molecular-genetics": (
        "James Watson, Francis Crick; Rosalind Franklin (X-ray crystallography); Erwin Chargaff; Oswald Avery"
    ),
    "human-genome-sequencing": (
        "Human Genome Project consortium (NIH, Wellcome Trust, multiple nations); Craig Venter (Celera Genomics)"
    ),
    "crispr-gene-editing": (
        "Jennifer Doudna and Emmanuelle Charpentier (Nobel Prize 2020); Feng Zhang (independent parallel work)"
    ),
    "the-periodic-table": "Dmitri Mendeleev; Lothar Meyer (independent parallel work)",
    "quantum-mechanics": (
        "Max Planck; Niels Bohr; Werner Heisenberg; Erwin Schrödinger; Paul Dirac; Albert Einstein"
    ),
    "nuclear-energy-and-nuclear-science": (
        "Otto Hahn, Lise Meitner, Fritz Strassmann (fission); Enrico Fermi (reactor); Manhattan Project team"
    ),
    "plastics-and-synthetic-materials": "Leo Baekeland (Bakelite); Wallace Carothers (nylon); DuPont chemists",
    "fertilisers-and-modern-agricultural-chemistry": (
        "Fritz Haber; Carl Bosch (BASF); Norman Borlaug (Green Revolution)"
    ),
    "telegraph": "Samuel Morse; Alfred Vail; William Cooke; Charles Wheatstone",
    "telephone": "Alexander Graham Bell; Elisha Gray (disputed co-inventor); Antonio Meucci",
    "radio": "Guglielmo Marconi; Nikola Tesla; Heinrich Hertz (discovery of radio waves, 1887)",
    "transistor": "William Shockley, John Bardeen, Walter Brattain (Bell Labs)",
    "integrated-circuit-microchip": "Jack Kilby (Texas Instruments); Robert Noyce (Fairchild Semiconductor)",
    "computer": (
        "Alan Turing (theoretical foundation); Konrad Zuse (Z3, 1941); ENIAC team (1945); John von Neumann"
    ),
    "internet": (
        "ARPA/DARPA team; Vint Cerf and Bob Kahn (TCP/IP, 1974); Tim Berners-Lee (WWW, 1989–1991)"
    ),
    "world-wide-web": "Tim Berners-Lee; Robert Cailliau; Marc Andreessen (Mosaic browser)",
    "search-engines": "Alan Emtage (Archie, 1990); Larry Page and Sergey Brin (Google, 1998)",
    "satellite-technology": (
        "Soviet space programme (Sputnik); NASA; Arthur C. Clarke (geostationary orbit concept, 1945)"
    ),
    "gps-global-positioning-system": (
        "US Department of Defense; Roger L. Easton, Ivan Getting, Bradford Parkinson"
    ),
    "semiconductor-technology": "Bell Labs; Texas Instruments; Intel; TSMC; ASML",
    "laser": (
        "Theodore Maiman (first ruby laser, 1960); Charles Townes and Arthur Schawlow (theoretical basis, MASER)"
    ),
    "fibre-optic-communication": (
        "Charles Kao (Nobel Prize 2009); George Hockham; Robert Maurer, Donald Keck, Peter Schultz (Corning)"
    ),
    "spaceflight": "Sergei Korolev (Soviet); Wernher von Braun (US); NASA; Yuri Gagarin; Neil Armstrong",
    "smartphones": "IBM (Simon, 1994); Apple (iPhone, 2007, Steve Jobs); Google (Android, 2008)",
    "social-media-platforms": (
        "Mark Zuckerberg (Facebook); Jack Dorsey (Twitter); Kevin Systrom (Instagram); multiple others"
    ),
    "renewable-energy-technologies": (
        "Bell Labs (silicon solar cell, 1954); Darrieus and other wind turbine pioneers; multiple researchers"
    ),
    "battery-technology": (
        "Alessandro Volta (electrochemical battery, 1800); John Goodenough, M. Stanley Whittingham, "
        "Akira Yoshino (lithium-ion battery — Nobel Prize 2019)"
    ),
    "electric-vehicles": "Charles Jeantaud (France, 1881); GM EV1 (1996); Elon Musk / Martin Eberhard (Tesla, 2003)",
    "robotics": (
        "George Devol (Unimate, 1961); Joseph Engelberger; Boston Dynamics; Rodney Brooks; Masahiro Mori"
    ),
    "3d-printing-additive-manufacturing": (
        "Chuck Hull (stereolithography, 1984); Carl Deckard (SLS); Scott Crump (FDM, Stratasys)"
    ),
    "blockchain": "Satoshi Nakamoto (pseudonym, identity unknown); Vitalik Buterin (Ethereum)",
    "cloud-computing": (
        "Amazon Web Services (Jeff Bezos, Andy Jassy); Salesforce (Marc Benioff, early SaaS); Google; Microsoft"
    ),
}

# Professionally corrected key facts for all 60 entries (docx + cleaned infographic/table data).
KEY_FACTS: dict[str, list[str]] = {
    "controlled-use-of-fire": [
        "Oldest evidence: ~1 million years ago",
        "Key sites: Wonderwerk Cave, South Africa",
        "Cooking fuelled human brain development",
        "Enabled settlement in colder climates",
        "Precursor to metallurgy and industry",
    ],
    "agriculture-and-domestication": [
        "At least 7 independent origins worldwide",
        "First crops: wheat, barley, millet, rice",
        "First animals: goats, sheep, cattle, pigs",
        "Enabled cities, states, writing, trade",
        "Also introduced zoonotic diseases",
    ],
    "the-wheel": [
        "First use: pottery wheel (~5500 BCE)",
        "Transport wheels: ~3500 BCE, Mesopotamia",
        "Americas and Africa developed without it",
        "Rotary principle → all modern machinery",
        "Spindle, lathe, centrifuge all derived",
    ],
    "writing-systems": [
        "At least 4 independent inventions",
        "Cuneiform: earliest writing (~3400 BCE)",
        "Alphabet invented in ancient Levant ~1800 BCE",
        "Enabled law, science, literature, history",
        "Foundational to all accumulated knowledge",
    ],
    "mathematics-and-the-concept-of-zero": [
        "Brahmagupta formalised zero: 628 CE",
        "Babylonian algebra dates to ~2000 BCE",
        "Hindu-Arabic numerals spread via Islamic world",
        "Calculus (Newton/Leibniz) built on this base",
        "Binary arithmetic underpins all computing",
    ],
    "paper": [
        "Invented in Han Dynasty China, 105 CE",
        "Reached Islamic world: 8th century",
        "Reached Europe via Islamic Spain: 12th century",
        "Made books affordable before printing press",
        "Global production today: 400M tonnes/year",
    ],
    "the-compass": [
        "Earliest Chinese compass: ~200 BCE",
        "Maritime use: Chinese texts ~1040–1119 CE",
        "European navigation use: ~1190 CE",
        "Enabled Age of Exploration voyages",
        "Foundation of modern navigation science",
    ],
    "gunpowder": [
        "Discovered by Tang Dynasty alchemists ~850 CE",
        "Military use in China: 10th century",
        "Reached Europe via Islamic scholars: 13th century",
        "Made feudal stone castles obsolete",
        "Later enabled mining and civil engineering",
    ],
    "the-printing-press": [
        "Movable type in China: Bi Sheng, ~1040 CE",
        "Gutenberg press: Mainz, Germany, ~1440 CE",
        "Gutenberg Bible printed c. 1455",
        "Book cost fell ~90% within decades",
        "Accelerated Renaissance and Reformation",
    ],
    "the-scientific-method": [
        "Ibn al-Haytham's 'Book of Optics': c. 1021 CE",
        "Bacon's 'Novum Organum': 1620",
        "Galileo introduced quantitative measurement",
        "Self-correcting: errors exposed by experiment",
        "Foundation of all modern science and tech",
    ],
    "the-telescope": [
        "Patent: Hans Lipperhey, Netherlands, 1608",
        "Galileo's observations began Jan 1610",
        "Revealed moons of Jupiter, craters on Moon",
        "Began modern observational astronomy",
        "JWST (2021) is its direct descendant",
    ],
    "the-microscope": [
        "Compound microscope: Janssen ~1590",
        "Leeuwenhoek magnified up to 270×, 1670s",
        "First observations of bacteria and protozoa",
        "Robert Hooke's Micrographia: 1665",
        "Electron microscopes now image individual atoms",
    ],
    "newtonian-mechanics": [
        "Principia Mathematica published: 1687",
        "Three laws of motion + law of gravitation",
        "Co-invented calculus with Leibniz",
        "Unified terrestrial and celestial physics",
        "Foundation of all classical engineering",
    ],
    "steam-engine": [
        "Newcomen atmospheric engine: 1712",
        "Watt's separate condenser patent: 1769",
        "First steam railway: Trevithick, 1804",
        "Powered mills, mines, ships, railways",
        "Inaugurated large-scale fossil fuel use",
    ],
    "electricity-generation-and-distribution": [
        "Faraday's electromagnetic induction: 1831",
        "Edison's DC system vs Tesla's AC: 1880s–1890s",
        "AC won: enables long-distance distribution",
        "~750M people still lack electricity today",
        "Most versatile energy form ever developed",
    ],
    "electromagnetism": [
        "Ørsted: electricity deflects compass: 1820",
        "Faraday: electromagnetic induction: 1831",
        "Maxwell's equations published: 1865",
        "Predicted light, radio, X-rays as EM waves",
        "Foundation of all motors, radios, Wi-Fi",
    ],
    "internal-combustion-engine": [
        "Lenoir's first commercial ICE: 1859",
        "Otto four-stroke cycle patent: 1876",
        "Diesel compression-ignition engine: 1897",
        "Compact design enabled cars and aircraft",
        "Now driving transition to electric vehicles",
    ],
    "automobile": [
        "Benz Patent-Motorwagen: 1885",
        "Ford Model T price fell from $825 to $260",
        "Ford moving assembly line: 1913",
        "Created entire new industrial ecosystem",
        "~1.35M road fatalities globally per year",
    ],
    "airplane": [
        "First powered flight: 17 December 1903",
        "First powered, heavier-than-air flight at Kitty Hawk",
        "Jet engine patent: Whittle, 1937",
        "First operational jet aircraft: 1944",
        "4+ billion passengers/year pre-pandemic",
    ],
    "refrigeration": [
        "Vapour-compression patent: Perkins, 1834",
        "Von Linde's industrial refrigeration: 1870s",
        "Birdseye quick-freezing process: 1920s",
        "Eliminates most foodborne illness risk",
        "Enables vaccine and medicine cold chains",
    ],
    "vaccination": [
        "Jenner's first vaccination: 1796",
        "Smallpox eradicated by WHO: 1980",
        "Polio reduced by >99.9% from peak",
        "Vaccines saved 154M lives (Lancet, 2024)",
        "mRNA vaccines developed in 2020 for COVID-19",
    ],
    "antibiotics": [
        "Fleming's discovery: 28 September 1928",
        "Florey and Chain's purification: 1940",
        "Mass production by WWII: 1944",
        "Added ~23 years to average lifespan",
        "Antimicrobial resistance: top global threat",
    ],
    "germ-theory-of-disease": [
        "Snow traced cholera to water pump: 1854",
        "Semmelweis: handwashing reduces deaths: 1847",
        "Pasteur's germ theory experiments: 1859–61",
        "Koch identified TB and cholera bacteria",
        "Foundation of vaccines, antibiotics, surgery",
    ],
    "anaesthesia": [
        "First ether use in surgery: Long, 1842",
        "Public ether demonstration: Morton, 1846",
        "Chloroform introduced: Simpson, 1847",
        "Made complex operations possible",
        "Modern anaesthesia uses sophisticated drug combos",
    ],
    "x-rays-and-medical-imaging": [
        "X-rays discovered: 8 November 1895",
        "Nobel Prize in Physics: Röntgen, 1901",
        "CT scanner: Hounsfield and Cormack, 1971",
        "MRI (no ionising radiation): 1977–1980s",
        "Now includes PET, ultrasound, functional MRI",
    ],
    "sanitation-and-clean-water-systems": [
        "London's Great Stink: 1858",
        "Bazalgette's sewer network: completed 1870s",
        "First water chlorination: Jersey City, 1908",
        "Eliminated most cholera and typhoid",
        "2B people still lack safe water (WHO 2023)",
    ],
    "dna-structure-and-molecular-genetics": [
        "Avery showed DNA carries genetic info: 1944",
        "Franklin's 'Photo 51': critical X-ray data",
        "Watson and Crick double helix: April 1953",
        "Nobel Prize: Watson, Crick, Wilkins, 1962",
        "Opened molecular biology, biotechnology, CRISPR",
    ],
    "human-genome-sequencing": [
        "HGP launched: 1990",
        "Draft sequence completed: 2001",
        "HGP declared complete: April 2003",
        "Cost fell from $3B in 2003 to under $200 by 2024",
        "Gapless T2T sequence: 2022",
    ],
    "crispr-gene-editing": [
        "Doudna & Charpentier CRISPR paper: 2012",
        "Nobel Prize in Chemistry: 2020",
        "First FDA-approved CRISPR therapy: 2023",
        "Applications: genetic disease, cancer, crops",
        "Ethical debate: germline editing prohibited",
    ],
    "the-periodic-table": [
        "Published: Mendeleev, 1869",
        "Left gaps for undiscovered elements",
        "All three predicted elements confirmed by 1886",
        "Modern table organised by atomic number (1913)",
        "118 elements confirmed; organises all chemistry",
    ],
    "quantum-mechanics": [
        "Planck's quantum hypothesis: 1900",
        "Bohr atomic model: 1913",
        "Heisenberg/Schrödinger equations: 1925–26",
        "Dirac predicted antimatter: 1928",
        "Foundation: laser, transistor, MRI, computing",
    ],
    "theory-of-relativity": [
        "Special relativity (E=mc²): 1905",
        "General relativity: 1915",
        "GPS requires relativistic corrections to work",
        "Gravitational waves detected by LIGO: 2015",
        "First black hole image: EHT, 2019",
    ],
    "nuclear-energy-and-nuclear-science": [
        "Fission discovered: Hahn, Meitner: Dec 1938",
        "First controlled chain reaction: Fermi, 1942",
        "Atomic bombs used: August 1945",
        "First electricity from nuclear: USSR, 1954",
        "~10% of world electricity, very low-carbon",
    ],
    "plastics-and-synthetic-materials": [
        "Bakelite (first synthetic plastic): 1907",
        "Nylon developed by Carothers at DuPont: 1935",
        "Polyethylene discovered by ICI: 1933",
        "Global production: 400M+ tonnes/year",
        "~8M tonnes enter oceans annually",
    ],
    "fertilisers-and-modern-agricultural-chemistry": [
        "Haber-Bosch process patented: 1909",
        "~50% of human body nitrogen from this process",
        "Enabled 3× increase in food production",
        "Green Revolution saved ~1B people from famine",
        "Nitrogen runoff causes major water pollution",
    ],
    "telegraph": [
        "Cooke and Wheatstone patent: 1837",
        "Morse code system: 1838",
        "First transcontinental US line: 1861",
        "Transatlantic cable: 1866",
        "Created Reuters, AP, and financial wire services",
    ],
    "telephone": [
        "Bell's telephone patent: 7 March 1876",
        "Bell Telephone Company founded: 1877",
        "Legal disputes with Gray and Meucci",
        "Became AT&T, dominated US for a century",
        "Phone network became early internet backbone",
    ],
    "radio": [
        "Hertz demonstrated EM waves: 1887",
        "Marconi's transatlantic signal: 1901",
        "BBC founded: 1922",
        "Radio was decisive in both World Wars",
        "Underpins Wi-Fi, Bluetooth, GPS, mobile phones",
    ],
    "transistor": [
        "First transistor demonstrated: 23 Dec 1947",
        "Nobel Prize in Physics: 1956",
        "First transistor radio: 1954",
        "Silicon transistor (Texas Instruments): 1954",
        "100B+ transistors on modern chips",
    ],
    "integrated-circuit-microchip": [
        "Kilby's IC: 12 September 1958",
        "Noyce's planar silicon IC: 1959",
        "Kilby Nobel Prize in Physics: 2000",
        "Intel founded by Noyce and Moore: 1968",
        "Semiconductor industry: >$600B revenue/year",
    ],
    "computer": [
        "Turing's 'Computable Numbers' paper: 1936",
        "Zuse Z3 (first programmable computer): 1941",
        "ENIAC (first electronic): 1945",
        "Von Neumann architecture: 1945",
        "Universal machine: same hardware, any software",
    ],
    "internet": [
        "ARPANET first message: 29 October 1969",
        "TCP/IP protocol: Cerf and Kahn, 1974",
        "NSFNET opened to commerce: 1991",
        "5 billion active internet users (2024)",
        "Carries ~5 exabytes of data per day",
    ],
    "world-wide-web": [
        "Web proposal submitted: March 1989",
        "First website went live: 6 August 1991",
        "Mosaic browser (mass-market): 1993",
        "No patents: made available to all freely",
        "~60 trillion web pages; 5B+ users",
    ],
    "search-engines": [
        "First internet search tool (Archie): 1990",
        "AltaVista, Lycos, Yahoo: mid-1990s",
        "Google PageRank patent: 1998",
        "Google processes ~8.5B searches/day",
        "AI chatbots now beginning to challenge search",
    ],
    "satellite-technology": [
        "Sputnik 1: 4 October 1957",
        "Clarke's geostationary orbit concept: 1945",
        "First geostationary comms satellite: 1963",
        "9,000+ satellites in orbit (2024)",
        "Underpins weather, GPS, internet, TV",
    ],
    "gps-global-positioning-system": [
        "First Block I GPS satellite: 1978",
        "Full 24-satellite constellation: 1993",
        "Full civilian accuracy: May 2000",
        "Also: GLONASS, Galileo, BeiDou systems",
        "Economic value to US economy: $1T+",
    ],
    "semiconductor-technology": [
        "Transistor: Bell Labs, 1947",
        "Moore's Law (doubles every ~2 years): 1965",
        "Silicon Valley: from planar process, 1959",
        "Modern nodes: 3–5 nm (2023–2024)",
        "ASML EUV machines: ~$380M each",
    ],
    "laser": [
        "First working laser: Maiman, May 1960",
        "LASER = Light Amplification by Stimulated Emission",
        "Based on Einstein's 1917 stimulated emission",
        "Used in LASIK, fibre optics, manufacturing",
        "LiDAR in self-driving vehicles uses lasers",
    ],
    "fibre-optic-communication": [
        "Theoretical paper: Kao and Hockham, 1966",
        "Low-loss fibre achieved: Corning, 1970",
        "First commercial fibre phone link: 1977",
        "Carries ~99% of international internet data",
        "Nobel Prize in Physics: Kao, 2009",
    ],
    "spaceflight": [
        "Sputnik 1: 4 October 1957",
        "Gagarin: first human in space: 12 April 1961",
        "Moon landing (Apollo 11): 20 July 1969",
        "ISS continuously inhabited since: 2000",
        "Global space economy: $546B (2022)",
    ],
    "smartphones": [
        "IBM Simon (first smartphone concept): 1994",
        "Apple iPhone launched: 29 June 2007",
        "Google Android launched: 2008",
        "App Store opened: July 2008",
        "6.9B smartphone users globally (2024)",
    ],
    "social-media-platforms": [
        "SixDegrees (first social network): 1997",
        "Facebook: Harvard launch, 2004",
        "Twitter: 2006; Instagram: 2010; TikTok: 2016",
        "~5B active social media users (2024)",
        "Algorithmic curation: major societal debate",
    ],
    "artificial-intelligence": [
        "Turing Test proposed: 1950",
        "'Artificial intelligence' coined: 1956",
        "AlexNet deep learning: 2012 inflection",
        "AlphaFold solved protein folding: 2020",
        "LLMs: GPT, Claude, Gemini (2020s)",
    ],
    "renewable-energy-technologies": [
        "First practical silicon solar cell: Bell Labs, 1954",
        "Solar cost fell 99% since 1976",
        "Wind cost fell ~90% since 1980s",
        "Solar and wind: ~13% of global electricity (2023)",
        "IEA projects majority of electricity by 2030s",
    ],
    "battery-technology": [
        "Volta's electrochemical pile: 1800",
        "Lead-acid battery: Planté, 1859",
        "Li-ion commercialised by Sony: 1991",
        "Li-ion cost fell ~97% since 1991",
        "Nobel Prize in Chemistry: 2019",
    ],
    "electric-vehicles": [
        "Early EVs predated gasoline cars: 1880s",
        "GM EV1 (modern attempt): 1996–1999",
        "Tesla Roadster launched: 2008",
        "Global EV sales >10M/year: 2022",
        "Many nations target ICE phase-out: 2030–2040",
    ],
    "robotics": [
        "Unimate robot at GM: 1961",
        "Industrial robots spread in auto industry: 1970s–90s",
        "da Vinci surgical robot approved: 1999",
        "Boston Dynamics Atlas robots: 2013–present",
        "Global robotics market: >$60B (2023)",
    ],
    "3d-printing-additive-manufacturing": [
        "Hull's stereolithography patent: 1984",
        "Selective laser sintering (SLS): Deckard, 1987",
        "FDM patent expired: 2009 (RepRap movement)",
        "Used for titanium implants, jet engine parts",
        "3D bioprinting of tissue: emerging field",
    ],
    "blockchain": [
        "Bitcoin whitepaper: October 2008",
        "Bitcoin network launched: January 2009",
        "Ethereum (smart contracts) launched: 2015",
        "Bitcoin market cap: $1–2T (variable)",
        "Applications: supply chain, identity, DeFi",
    ],
    "cloud-computing": [
        "Salesforce pioneered SaaS: 1999",
        "Amazon Web Services launched: 2006",
        "Google Cloud and Microsoft Azure: 2008–2010",
        "Pay-as-you-go elastic infrastructure model",
        "Enables AI, analytics without owning data centres",
    ],
}

OCR_JUNK_RE = re.compile(
    r"KEY\s*FACT|ikebdi|CHk\s*EY|MAcasmerica|ventional|ssachusetts|KEMFAEJTS|K&amp;Y",
    re.IGNORECASE,
)


def first_sentence(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    match = re.match(r"^(.+?[.!?])(?:\s|$)", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text


def trim_summary(text: str, max_len: int = SUMMARY_MAX) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    if len(text) <= max_len:
        return text
    cut = text[: max_len - 1].rsplit(" ", 1)[0]
    if cut and cut[-1] not in ".!?":
        cut += "…"
    return cut


def extract_summary(entry: dict) -> str:
    slug = entry["slug"]
    if slug in SUMMARY_OVERRIDES:
        return SUMMARY_OVERRIDES[slug]

    sections = entry.get("sections", {})
    for key in (SIGNIFICANCE, HISTORICAL):
        paras = sections.get(key, [])
        if paras:
            sentence = first_sentence(paras[0] if isinstance(paras[0], str) else str(paras[0]))
            if sentence:
                return trim_summary(sentence)
    return ""


def extract_key_figures(entry: dict) -> str:
    slug = entry["slug"]
    if slug in KEY_FIGURES_OVERRIDES:
        return KEY_FIGURES_OVERRIDES[slug]
    meta = entry.get("meta", "")
    figures = meta_key_figures(meta)
    if figures and not OCR_JUNK_RE.search(figures):
        return figures
    return figures.strip()


def extract_key_facts(slug: str, table_by_slug: dict[str, dict]) -> list[str]:
    if slug in KEY_FACTS:
        return KEY_FACTS[slug]

    row = table_by_slug.get(slug, {})
    facts = row.get("key_facts", [])
    if facts and all(isinstance(f, str) and not OCR_JUNK_RE.search(f) for f in facts):
        return [re.sub(r"\s+", " ", f.strip()) for f in facts if f.strip()]

    return []


def load_table_data() -> dict[str, dict]:
    if not TABLE_DATA.exists():
        return {}
    rows = json.loads(TABLE_DATA.read_text(encoding="utf-8"))
    return {row["slug"]: row for row in rows}


def build_card_copy() -> dict[str, dict]:
    data = parse_docx()
    table_by_slug = load_table_data()
    result: dict[str, dict] = {}

    for entry in data["entries"]:
        slug = entry["slug"]
        result[slug] = {
            "key_figures": extract_key_figures(entry),
            "summary": extract_summary(entry),
            "key_facts": extract_key_facts(slug, table_by_slug),
        }

    return result


def main() -> None:
    card_copy = build_card_copy()
    OUT_JSON.write_text(
        json.dumps(card_copy, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(card_copy)} entries to {OUT_JSON.relative_to(ROOT)}")
    missing_facts = [s for s, v in card_copy.items() if not v["key_facts"]]
    missing_summary = [s for s, v in card_copy.items() if not v["summary"]]
    if missing_facts:
        print(f"  Warning: missing key_facts for {missing_facts}")
    if missing_summary:
        print(f"  Warning: missing summary for {missing_summary}")


if __name__ == "__main__":
    main()
