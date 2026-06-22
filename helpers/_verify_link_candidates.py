#!/usr/bin/env python3
"""Verify candidate replacement URLs."""
from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

CANDIDATES = {
    "https://airandspace.si.edu/explore/topics/apollo/apollo11.cfm": "https://airandspace.si.edu/exhibitions/apollo-to-the-moon",
    "https://airandspace.si.edu/explore/topics/wright-brothers": "https://airandspace.si.edu/collection-objects/1903-wright-flyer",
    "https://americanhistory.si.edu/": "https://www.si.edu/museums/national-museum-american-history",
    "https://americanhistory.si.edu/collections/search/object/nmah_1106986": "https://www.si.edu/object/telegraph-key-used-samuel-morse1844:nmah_1106986",
    "https://americanhistory.si.edu/collections/search/object/nmah_849543": "https://www.si.edu/object/printing-press-used-johannes-gutenberg:nmah_849543",
    "https://computerhistory.org/stories/integrated-circuit/": "https://www.computerhistory.org/siliconengine/",
    "https://computerhistory.org/stories/mobile-phone/": "https://www.computerhistory.org/revolution/mobile-computing/smartphones/",
    "https://computerhistory.org/stories/transistor/": "https://www.computerhistory.org/siliconengine/introduction/",
    "https://cudl.lib.cam.ac.uk/view/PR-ADV-B-00039-00001": "https://cudl.lib.cam.ac.uk/collections/newton/1",
    "https://doi.org/10.1126/science.1225829": "https://pubmed.ncbi.nlm.nih.gov/22723414/",
    "https://ethw.org/Electric_Power": "https://ethw.org/History_of_electric_power_transmission",
    "https://humanorigins.si.edu/human-characteristics/fire": "https://humanorigins.si.edu/evidence/control-fire-use-and-cooking",
    "https://innovativegenomics.org/crisprpedia/": "https://innovativegenomics.org/what-is-crispr/",
    "https://micro.magnet.fsu.edu/primer/museum/microscopy.html": "https://micro.magnet.fsu.edu/primer/index.html",
    "https://ourworldindata.org/battery-price-declines": "https://ourworldindata.org/batteries",
    "https://ourworldindata.org/energy-crypto-currencies": "https://ourworldindata.org/energy-consumption-bitcoin",
    "https://ourworldindata.org/social-media": "https://ourworldindata.org/rise-of-social-media",
    "https://radiopaedia.org/": "https://radiopaedia.org/articles/home?lang=us",
    "https://royalsociety.org/collections/newton/": "https://makingscience.royalsociety.org/s/rs/903274/NTc4NjQ4/TG9vazovL2NvbGxlY3Rpb25zL25ld3Rvbg",
    "https://webfoundation.org/about/history/": "https://webfoundation.org/about/vision/history-of-the-web/",
    "https://www.aps.org/publications/apsnews/200010/history.cfm": "https://www.aps.org/publications/apsnews/200010/history",
    "https://www.asml.com/en/technology/euv-lithography/how-euv-works": "https://www.asml.com/en/technology",
    "https://www.bbc.co.uk/history/british/middle_ages/blackpowder_01.shtml": "https://www.bbc.co.uk/history/ancient/chinese_inventions/gunpowder_01.shtml",
    "https://www.bbc.co.uk/programmes/p004kl5l": "https://www.bbc.co.uk/programmes/b00dxjls",
    "https://www.bbc.co.uk/programmes/b00btblm": "https://www.bbc.co.uk/history/historic_figures/newton_isaac.shtml",
    "https://www.bbc.co.uk/programmes/b04bch1p": "https://www.bbc.co.uk/programmes/b04bch1p/episodes/guide",
    "https://www.bbc.co.uk/programmes/b06f22jg": "https://www.bbc.co.uk/programmes/b06f22jg/episodes/guide",
    "https://www.bbc.co.uk/programmes/p004kl5l": "https://www.bbc.co.uk/history/ancient/british_prehistory/iron_age_01.shtml",
    "https://www.bbc.co.uk/programmes/p00gkwy6": "https://www.bbc.co.uk/history/historic_figures/fleming_alexander.shtml",
    "https://www.bbc.co.uk/programmes/p0b0dmq4": "https://www.bbc.co.uk/iplayer/episodes/p0b0dmq4",
    "https://www.bl.uk/gutenberg-bible": "https://www.bl.uk/collection-items/gutenberg-bible",
    "https://www.britishmuseum.org/learn/schools/ages-14/ancient-egypt/the-history-of-writing": "https://www.britishmuseum.org/learn/schools/ages-7-11/ancient-egypt/writing",
    "https://www.cdc.gov/rabies/prevention/history.html": "https://archive.cdc.gov/www_cdc_gov/rabies/history/history.html",
    "https://www.cfr.org/book/chip-war": "https://www.cfr.org/article/chip-war-chris-miller",
    "https://www.corning.com/optical-communications/": "https://www.corning.com/optical-communications/worldwide/en/home/products/optical-fiber.html",
    "https://www.corning.com/optical-communications/worldwide/en/home/inside-the-network/fiber-optic-technology.html": "https://www.corning.com/optical-communications/worldwide/en/home/products/optical-fiber.html",
    "https://www.discovermagazine.com/planet-earth/the-worst-mistake-in-the-history-of-the-human-race": "https://www.discovermagazine.com/planet-earth/jared-diamond-the-worst-mistake-in-the-history-of-the-human-race",
    "https://www.esa.int/Enabling_Support/Operations/How_do_satellites_work": "https://www.esa.int/Science_Exploration/Space_Science/How_do_satellites_work",
    "https://www.feynmanlectures.caltech.edu/": "https://www.feynmanlectures.caltech.edu/I/toc.html",
    "https://www.iaea.org/topics/nuclear-power": "https://www.iaea.org/topics/nuclear-energy",
    "https://www.internetsociety.org/internet/history-internet/": "https://www.internetsociety.org/internet/history/",
    "https://www.johnsnowsociety.org/john-snow.html": "https://www.ph.ucla.edu/epi/snow.html",
    "https://www.ligo.caltech.edu/page/press-release-gr150914": "https://www.ligo.caltech.edu/news/ligo20160211",
    "https://www.loc.gov/collections/alexander-graham-bell/": "https://www.loc.gov/collections/alexander-graham-bell-papers/about-this-collection/",
    "https://www.loc.gov/preservation/resources/resthomes/paper.html": "https://www.loc.gov/preservation/scientists/projects/papers/",
    "https://www.massgeneral.org/museum/exhibit/ether-dome": "https://www.massgeneral.org/heritage/ether-dome",
    "https://www.nasa.gov/audience/forstudents/5-8/features/nasa-knows/what-is-a-telescope-58.html": "https://science.nasa.gov/resource/what-is-a-telescope/",
    "https://www.nasa.gov/centers/glenn/about/history/wright.html": "https://www.nasa.gov/history/wright-brothers/",
    "https://www.nasa.gov/satellites/": "https://www.nasa.gov/learning-resources/for-kids-and-students/what-is-a-satellite-grades-5-8/",
    "https://www.nature.com/articles/d41586-019-02665-9": "https://doi.org/10.1038/d41586-019-02665-9",
    "https://www.nature.com/articles/news.2012.299": "https://doi.org/10.1038/news.2012.299",
    "https://www.pbs.org/wgbh/americanexperience/features/green-revolution/": "https://www.pbs.org/wgbh/americanexperience/films/green-revolution/",
    "https://www.pbs.org/wgbh/frontline/documentary/vaccine-war/": "https://www.pbs.org/wgbh/frontline/film/vaccine-war/",
    "https://www.pbs.org/wgbh/nova/physics/scientific-revolution.html": "https://www.pbs.org/wgbh/nova/series/science-revolution/",
    "https://www.pbs.org/wgbh/nova/tech/steam-engine.html": "https://www.pbs.org/wgbh/nova/article/industrial-revolution-steam-engine/",
    "https://www.pewresearch.org/topic/internet-technology/platforms-services/social-media/": "https://www.pewresearch.org/internet/fact-sheet/social-media/",
    "https://www.rigb.org/our-history/famous-scientists/michael-faraday": "https://www.rigb.org/explore-science/explore/popular-science/faraday-laboratory",
    "https://www.rms.org.uk/discover-engage/microscopy-exploration.html": "https://www.rms.org.uk/discover-microscopy/",
    "https://www.rsc.org/education/eic/issues/2013mar/haber-process-fertilisers.asp": "https://edu.rsc.org/resources/the-haber-process/2213.article",
    "https://www.sciencemuseum.org.uk/objects-and-stories/steam-engine": "https://www.sciencemuseum.org.uk/objects-and-stories/history-steam-engine",
    "https://www.sciencemuseum.org.uk/objects-and-stories/technology-engineering/internal-combustion-engine": "https://www.sciencemuseum.org.uk/objects-and-stories/history-internal-combustion-engine",
    "https://www.ted.com/talks/ramez_naam_the_case_for_optimism_on_climate_change": "https://www.ted.com/talks/ramez_naam_how_cheap_can_solar_get_very_very_cheap",
    "https://www.thameswater.co.uk/about-us/responsibility/engineering/history-of-our-sewers": "https://www.thameswater.co.uk/about-us/who-we-are/our-history/the-great-stink",
    "https://www.thehenryford.org/explore/stories-of-innovation/": "https://www.thehenryford.org/current-events/stories-of-innovation/",
    "https://www.turing.ac.uk/alan-turing": "https://www.turing.ac.uk/research/research-areas/artificial-intelligence/alan-turing",
    "https://www.turing.ac.uk/research/interest-groups/trustworthy-human-centric-ai": "https://www.turing.ac.uk/research/research-areas/artificial-intelligence/ai-safety",
    "https://www.wired.com/2014/05/the-victorian-internet/": "https://www.wired.com/story/the-victorian-internet-tom-standage/",
}


def check(url: str) -> bool:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
            return 200 <= resp.status < 400
    except urllib.error.HTTPError as exc:
        return exc.code in (301, 302, 303, 307, 308)
    except Exception:
        return False


def main() -> None:
    ok = {}
    bad = {}
    for old, new in CANDIDATES.items():
        if check(new):
            ok[old] = new
            print(f"OK  {new}")
        else:
            bad[old] = new
            print(f"BAD {new}")
    print(f"\nOK: {len(ok)} BAD: {len(bad)}")
    if bad:
        print("Failed replacements:")
        for old, new in bad.items():
            print(f"  {old}\n    -> {new}")


if __name__ == "__main__":
    main()
