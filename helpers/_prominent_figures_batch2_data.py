"""Batch 2: academically documented figures across seven origin groups (AZ/EN)."""

from __future__ import annotations

from typing import Any


def _fig(
    slug: str,
    category: str,
    emoji: str,
    dates: str,
    birth: str,
    death: str,
    name_az: str,
    name_en: str,
    country_az: str,
    country_en: str,
    field_az: str,
    field_en: str,
    life_az: str,
    life_en: str,
    work_az: str,
    work_en: str,
    impact_az: str,
    impact_en: str,
    quote_az: str,
    quote_en: str,
    quote_source_az: str,
    quote_source_en: str,
    contributions_az: list[str],
    contributions_en: list[str],
    works: list[dict[str, str]],
    events: list[dict[str, str]],
    sources: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "slug": slug,
        "category": category,
        "emoji": emoji,
        "dates": dates,
        "birth": birth,
        "death": death,
        "name_az": name_az,
        "name_en": name_en,
        "country_az": country_az,
        "country_en": country_en,
        "field_az": field_az,
        "field_en": field_en,
        "life_az": life_az,
        "life_en": life_en,
        "work_az": work_az,
        "work_en": work_en,
        "impact_az": impact_az,
        "impact_en": impact_en,
        "quote_az": quote_az,
        "quote_en": quote_en,
        "quote_source_az": quote_source_az,
        "quote_source_en": quote_source_en,
        "contributions_az": contributions_az,
        "contributions_en": contributions_en,
        "works": works,
        "events": events,
        "sources": sources,
    }


def _w(name_az, name_en, desc_az, desc_en):
    return {"name_az": name_az, "name_en": name_en, "desc_az": desc_az, "desc_en": desc_en}


def _e(icon, title_az, title_en, text_az, text_en):
    return {
        "icon": icon,
        "title_az": title_az,
        "title_en": title_en,
        "text_az": text_az,
        "text_en": text_en,
    }


def _s(title_az, title_en, url):
    return {"title_az": title_az, "title_en": title_en, "url": url}


FIGURES: list[dict[str, Any]] = [
    # ── Kazakh ──────────────────────────────────────────────────────────────
    _fig(
        "ablai_khan", "azturk", "👑", "1711 – 1781", "1711", "1781",
        "Ablai xan", "Ablai Khan", "Qazax", "Kazakh",
        "Dövlət idarəçiliyi və diplomatiya", "Governance and diplomacy",
        "Ablai xan (1711–1781) Orta Qazax xanlığının hökmranı olmuş, "
        "qazax tayfalarını vahid siyasət altında birləşdirməyə çalışmış "
        "və Qazaxıstanın müstəqilliyini qorumaq üçün Rusiya və Çin "
        "arasında balanslı diplomatiya aparmışdır.",
        "Ablai Khan (1711–1781) ruled the Middle Kazakh Khanate, sought to "
        "unite Kazakh tribes under a single political order, and pursued "
        "balanced diplomacy between Russia and China to preserve Kazakh autonomy.",
        "Ablai xan hərbi təşkilatı möhkəmləndirmiş, ticarət yollarını "
        "qoruyub qonşu dövlətlərlə sülh müqavilələri bağlamış, "
        "qazax elinin siyasi birliyini gücləndirmişdir.",
        "Ablai Khan strengthened military organization, secured trade routes, "
        "concluded peace treaties with neighboring states, and reinforced "
        "the political unity of the Kazakh people.",
        "Ablai xan Qazax xanlığının son mərhələsində milli birliyin "
        "və müstəqil siyasətin simvolu sayılır; onun dövrü "
        "qazax dövlətçilik ənənəsinin zirvəsidir.",
        "Ablai Khan is regarded as a symbol of national unity and independent "
        "policy in the final phase of the Kazakh Khanate; his era marks a "
        "high point of Kazakh statecraft.",
        "Xalq birliyi güclü idarəetmənin əsasidir.",
        "The unity of the people is the foundation of strong governance.",
        "— Ablai xan irsinin ümumi ideyası", "— A guiding idea associated with Ablai Khan's legacy",
        ["Qazax tayfalarının siyasi birləşdirilməsi", "Rusiya və Çin arasında diplomatiya", "Qazax xanlığının müstəqilliyinin qorunması"],
        ["Political unification of Kazakh tribes", "Diplomacy between Russia and China", "Preservation of Kazakh Khanate autonomy"],
        [
            _w("Diplomatik siyasət", "Diplomatic policy", "Qonşu imperiyalarla balanslı münasibətlər strategiyası.", "Strategy of balanced relations with neighboring empires."),
            _w("Hərbi təşkilat", "Military organization", "Qazax ordusunun möhkəmləndirilməsi.", "Strengthening of the Kazakh military."),
            _w("Ticarət yollarının qorunması", "Protection of trade routes", "Silk Road marşrutlarının təhlükəsizliyinin təmin edilməsi.", "Securing safety on Silk Road routes."),
        ],
        [
            _e("🤝", "Diplomat xan", "Diplomat khan", "Rusiya və Çin arasında balanslı siyasət aparmışdır.", "Pursued balanced policy between Russia and China."),
            _e("⚔️", "Birlik", "Unity", "Qazax tayfalarını vahid siyasət altında birləşdirməyə çalışmışdır.", "Sought to unite Kazakh tribes under one political order."),
        ],
        [
            _s("Encyclopaedia Britannica — Kazakhstan", "Encyclopaedia Britannica — Kazakhstan", "https://www.britannica.com/place/Kazakhstan/History"),
            _s("UNESCO — Qazax mədəni irsi", "UNESCO — Kazakhstan cultural heritage", "https://ich.unesco.org/en/state/kazakhstan-KZ"),
            _s("Britannica — Orta Asiya tarixi", "Britannica — Central Asia history", "https://www.britannica.com/place/Central-Asia"),
        ],
    ),
    _fig(
        "akhmet_baitursynov", "azturk", "📚", "1872 – 1937", "1872", "1937",
        "Axmet Baitursınov", "Akhmet Baitursynov", "Qazax", "Kazakh",
        "Dilçilik və təhsil", "Linguistics and education",
        "Axmet Baitursınov (1872–1937) qazax dilçisi, pedaqoq və ictimai xadimdir. "
        "Əlifba islahatı, qazax dilinin qrammatikasının elmi təsdiqi və "
        "«Alaş» hərəkatında milli maarifçilik ideyalarının irəli sürülməsi "
        "ilə tanınır.",
        "Akhmet Baitursynov (1872–1937) was a Kazakh linguist, educator, and public "
        "figure known for alphabet reform, scholarly codification of Kazakh grammar, "
        "and advancing national enlightenment in the Alash movement.",
        "Baitursınov «Qazaq tili» (1914) əsəri ilə qazax dilinin qrammatikasını "
        "sistemli şəkildə təsvir etmiş, latın əlifbasına keçid ideyalarını "
        "inkişaf etdirmiş və milli məktəblərin açılmasına töhfə vermişdir.",
        "Baitursynov systematically described Kazakh grammar in Qazaq tili (1914), "
        "developed ideas for transition to the Latin alphabet, and contributed "
        "to opening national schools.",
        "O, qazax yazı dilinin elmi normalaşdırılmasının və modern təhsil "
        "sisteminin formalaşmasının əsas fiqurlarından biridir.",
        "He is one of the key figures in the scholarly standardization of written "
        "Kazakh and the formation of a modern education system.",
        "Dil — xalqın ruhu və yaddaşıdır.",
        "Language is the soul and memory of a people.",
        "— Axmet Baitursınov irsinin ümumi ideyası", "— A guiding idea associated with Baitursynov's legacy",
        ["Qazax dilinin qrammatikasının elmi təsdiqi", "Əlifba islahatı", "Milli təhsil və «Alaş» hərəkatı"],
        ["Scholarly codification of Kazakh grammar", "Alphabet reform", "National education and the Alash movement"],
        [
            _w("Qazaq tili", "Qazaq tili", "Qazax dilinin qrammatikası barədə fundamental əsər.", "Fundamental work on Kazakh grammar."),
            _w("Əlifba islahatı", "Alphabet reform", "Latın əlifbasına keçid layihələri.", "Projects for transition to the Latin alphabet."),
            _w("Maarifçilik fəaliyyəti", "Enlightenment activity", "Milli məktəblər və ictimai təhsil.", "National schools and public education."),
        ],
        [
            _e("📖", "Qazaq tili", "Qazaq tili", "1914-cü ildə qazax dilinin ilk elmi qrammatikası nəşr olunmuşdur.", "The first scholarly grammar of Kazakh was published in 1914."),
            _e("🏛️", "Alaş hərəkatı", "Alash movement", "Qazax milli özünüidarəetmə ideyalarının irəli sürülməsində iştirak etmişdir.", "Participated in advancing Kazakh national self-governance."),
        ],
        [
            _s("Britannica — Qazax dili", "Britannica — Kazakh language", "https://www.britannica.com/topic/Kazakh-language"),
            _s("UNESCO — Qazaxıstan", "UNESCO — Kazakhstan", "https://ich.unesco.org/en/state/kazakhstan-KZ"),
            _s("Britannica — Orta Asiya ədəbiyyatı", "Britannica — Central Asian literature", "https://www.britannica.com/art/Central-Asian-arts/Literature"),
        ],
    ),
    _fig(
        "kurmangazy_sagyrbayuly", "azturk", "🎵", "1823 – 1889", "1823", "1889",
        "Qurmangazy Saqırbaev", "Kurmangazy Sagyrbayuly", "Qazax", "Kazakh",
        "Musiqi və bədii irs", "Music and cultural heritage",
        "Qurmangazy Saqırbaev (1823–1889) qazax klassik musiqisinin "
        "ən böyük kompozitorlarından biridir. Dombyra üçün yazdığı "
        "küyələr qazax musiqi irsinin ayrılmaz hissəsidir.",
        "Kurmangazy Sagyrbayuly (1823–1889) was one of the greatest composers "
        "of classical Kazakh music. His dombra küy (instrumental pieces) "
        "are an integral part of Kazakh musical heritage.",
        "Qurmangazy «Sary arqa», «Kishkentay» və «Aman bol, qazaq eli» "
        "kimi küylər yaratmış, qazax musiqi dilinin ifadə imkanlarını "
        "genişləndirmişdir.",
        "Kurmangazy composed pieces such as Sary Arqa, Kishkentay, and "
        "Aman Bol, Qazaq Eli, expanding the expressive range of Kazakh music.",
        "Onun əsərləri UNESCO-nun qeyri-maddi mədəni irs siyahısına "
        "daxil edilmiş qazax dombyra küy ənənəsinin təməl daşıdır.",
        "His works are foundational to the Kazakh dombra küy tradition, "
        "recognized within UNESCO intangible cultural heritage frameworks.",
        "Küy — xalqın ürəyinin səsi, tarixin səsi.",
        "A küy is the voice of the people's heart and of history.",
        "— Qazax musiqi ənənəsinin ümumi ideyası", "— A guiding idea of Kazakh musical tradition",
        ["Qazax klassik dombyra küyünün inkişafı", "Milli musiqi irsinin sənədləşdirilməsi", "UNESCO qeyri-maddi irs kontekstində tanınma"],
        ["Development of classical Kazakh dombra küy", "Documentation of national musical heritage", "Recognition within UNESCO intangible heritage"],
        [
            _w("Sary arqa", "Sary Arqa", "Qazax klassik küy repertuarının ən tanınmış əsərlərindən biri.", "One of the best-known works of the classical küy repertoire."),
            _w("Aman bol, qazaq eli", "Aman Bol, Qazaq Eli", "Milli ruhu əks etdirən simvolik küy.", "Symbolic küy reflecting national spirit."),
            _w("Dombyra repertuarı", "Dombra repertoire", "Qazax xalq musiqisinin klassik kolleksiyası.", "Classical collection of Kazakh folk music."),
        ],
        [
            _e("🎸", "Dombyra ustası", "Dombra master", "Qazax dombyrasının ən böyük virtuozlarından biri sayılır.", "Regarded as one of the greatest dombra virtuosos."),
            _e("🌍", "UNESCO irsi", "UNESCO heritage", "Qazax küy ənənəsi qeyri-maddi mədəni irs kimi qorunur.", "The Kazakh küy tradition is protected as intangible cultural heritage."),
        ],
        [
            _s("UNESCO — Qazax dombyra küy", "UNESCO — Kazakh dombra küy", "https://ich.unesco.org/en/state/kazakhstan-KZ"),
            _s("Britannica — Qazax musiqisi", "Britannica — Kazakh music", "https://www.britannica.com/art/Kazakhstan/Music"),
            _s("Britannica — Mərkəzi Asiya musiqisi", "Britannica — Central Asian music", "https://www.britannica.com/art/Central-Asian-arts/Music"),
        ],
    ),
    _fig(
        "ybyrai_altynsarin", "azturk", "🏫", "1841 – 1889", "1841", "1889",
        "Ybyray Altynsarin", "Ybyrai Altynsarin", "Qazax", "Kazakh",
        "Təhsil və pedaqogika", "Education and pedagogy",
        "Ybyray Altynsarin (1841–1889) qazax pedaqoq və maarifçi, "
        "Qazaxıstanda ilk laik məktəblərin təsisçisidir. "
        "Qadın təhsilinə diqqət yetirmiş və qazax dilində dərsliklər hazırlamışdır.",
        "Ybyrai Altynsarin (1841–1889) was a Kazakh educator and founder of "
        "the first secular schools in Kazakhstan. He promoted girls' education "
        "and prepared textbooks in the Kazakh language.",
        "Altynsarin «Qazaq xrestomatiyası» (1879) və «İlk addımlar» kimi "
        "dərsliklər yazmış, Torgay vilayətində məktəb şəbəkəsi yaratmışdır.",
        "Altynsarin wrote textbooks including Qazaq Reader (1879) and First Steps, "
        "and built a school network in the Turgai region.",
        "O, qazax təhsil sisteminin laikləşməsinin və milli dilin "
        "məktəb tədrisində istifadəsinin pioneridir.",
        "He pioneered the secularization of Kazakh education and the use "
        "of the national language in school instruction.",
        "Təhsil olmadan xalqın gələcəyi yoxdur.",
        "Without education there is no future for a people.",
        "— Ybyray Altynsarin irsinin ümumi ideyası", "— A guiding idea associated with Altynsarin's legacy",
        ["Qazaxıstanda ilk laik məktəblərin açılması", "Qazax dilində dərsliklərin yaradılması", "Qadın təhsilinin təbliği"],
        ["Opening of the first secular schools in Kazakhstan", "Creation of textbooks in Kazakh", "Promotion of girls' education"],
        [
            _w("Qazaq xrestomatiyası", "Qazaq Reader", "1879-cu ildə nəşr olunan ilk qazax dərslik xrestomatiyası.", "First Kazakh textbook reader, published in 1879."),
            _w("İlk addımlar", "First Steps", "Uşaq təhsili üçün pedaqoji dərslik.", "Pedagogical textbook for children's education."),
            _w("Məktəb şəbəkəsi", "School network", "Torgay vilayətində laik məktəblərin təşkili.", "Organization of secular schools in Turgai province."),
        ],
        [
            _e("🏫", "İlk laik məktəblər", "First secular schools", "Qazaxıstanda laik təhsilin təməlini qoymuşdur.", "Laid the foundation for secular education in Kazakhstan."),
            _e("👧", "Qadın təhsili", "Girls' education", "Qız uşaqların məktəb təhsilinə cəlb edilməsini təbliğ etmişdir.", "Advocated enrolling girls in school education."),
        ],
        [
            _s("Britannica — Qazaxıstan tarixi", "Britannica — History of Kazakhstan", "https://www.britannica.com/place/Kazakhstan/History"),
            _s("UNESCO — Qazaxıstan", "UNESCO — Kazakhstan", "https://ich.unesco.org/en/state/kazakhstan-KZ"),
            _s("Britannica — Təhsil tarixi", "Britannica — Education", "https://www.britannica.com/topic/education"),
        ],
    ),

    # ── Kyrgyz ──────────────────────────────────────────────────────────────
    _fig(
        "sagymbai_orozbakov", "azturk", "📜", "1867 – 1970", "1867", "1970",
        "Sağımbay Orozbakov", "Sagymbai Orozbakov", "Qırğız", "Kyrgyz",
        "Epik irs və folklor", "Epic heritage and folklore",
        "Sağımbay Orozbakov (1867–1970) qırğız «Manas» destanının "
        "ən məşhur manasçılarından biridir. Onun ifa tərzi "
        "qırğız epik ənənəsinin qorunmasına fundamental töhfə vermişdir.",
        "Sagymbai Orozbakov (1867–1970) was one of the most renowned "
        "manaschy (reciters) of the Kyrgyz Manas epic. His performance "
        "tradition made a fundamental contribution to preserving Kyrgyz epic heritage.",
        "Orozbakov «Manas» destanının tam versiyasını ifa etmiş, "
        "qeydə alınmış və nəsil-nəsil ötürülən epik irsin canlı "
        "körpüsü olmuşdur.",
        "Orozbakov performed the full version of the Manas epic, "
        "recorded it, and served as a living bridge for epic heritage "
        "passed from generation to generation.",
        "UNESCO «Manas» destanını qeyri-maddi mədəni irs kimi tanıyır; "
        "Sağımbayın ifası bu irsin qlobal tanınmasında mühüm rol oynamışdır.",
        "UNESCO recognizes the Manas epic as intangible cultural heritage; "
        "Sagymbai's performance played a vital role in its global recognition.",
        "Manas — qırğız xalqının yaddaşı və ruhu.",
        "Manas is the memory and soul of the Kyrgyz people.",
        "— Qırğız epik ənənəsinin ümumi ideyası", "— A guiding idea of Kyrgyz epic tradition",
        ["«Manas» destanının tam ifası və qeydə alınması", "Qırğız epik ənənəsinin qorunması", "UNESCO qeyri-maddi mədəni irs"],
        ["Full performance and recording of the Manas epic", "Preservation of Kyrgyz epic tradition", "UNESCO intangible cultural heritage"],
        [
            _w("Manas destanı", "Manas epic", "Qırğız xalq epossunun tam ifa versiyası.", "Full performance version of the Kyrgyz national epic."),
            _w("Manasçılıq sənəti", "Manaschy art", "Epik ifa və nəslindən-nəslinə ötürülmə.", "Epic recitation and oral transmission."),
            _w("Səs qeydləri", "Audio recordings", "XX əsrin ortalarında aparılmış epik qeydlər.", "Epic recordings made in the mid-20th century."),
        ],
        [
            _e("🎤", "Manasçı", "Manaschy", "«Manas» destanının ən tanınmış ifaçılarından biri.", "One of the best-known reciters of the Manas epic."),
            _e("🌍", "UNESCO", "UNESCO", "Manas qeyri-maddi mədəni irs kimi tanınır.", "Manas is recognized as intangible cultural heritage."),
        ],
        [
            _s("UNESCO — Manas", "UNESCO — Manas", "https://ich.unesco.org/en/RL/epic-of-manas-00258"),
            _s("Britannica — Qırğızıstan", "Britannica — Kyrgyzstan", "https://www.britannica.com/place/Kyrgyzstan"),
            _s("Britannica — Oral tradition", "Britannica — Oral tradition", "https://www.britannica.com/art/oral-tradition"),
        ],
    ),
    # ── Uzbek ───────────────────────────────────────────────────────────────
    _fig(
        "jamshid_al_kashi", "world", "📐", "1380 – 1429", "1380", "1429",
        "Cəmsid əl-Kaşi", "Jamshid al-Kashi", "Özbək", "Uzbek",
        "Riyaziyyat və astronomiya", "Mathematics and astronomy",
        "Giyaseddin Cəmsid ibn Masud əl-Kaşi (1380–1429) Səmərqənddə "
        "Ulubəy rasadxanasında çalışmış riyaziyyatçı və astronomdur. "
        "Onun «Əl-Kaşi qaydası» onluq kəsr hesablamasının inkişafına "
        "fundamental töhfə vermişdir.",
        "Ghiyath al-Din Jamshid al-Kashi (1380–1429) was a mathematician "
        "and astronomer who worked at Ulugh Beg's observatory in Samarkand. "
        "His al-Kashi's rule made a fundamental contribution to decimal fraction computation.",
        "Əl-Kaşi π ədədini 16 onluq yerə qədər hesablamış, "
        "«Risalə fi'l-Hisab» traktatında riyazi metodları sistemləşdirmiş, "
        "Səmərqənd elmi məktəbinin zirvəsini təmsil etmişdir.",
        "Al-Kashi calculated pi to 16 decimal places, systematized mathematical "
        "methods in his Treatise on Computation, and represents the peak of "
        "the Samarkand scientific school.",
        "Onun işləri Avropa riyaziyyatına da təsir etmiş, "
        "Timurid elmi mərkəzinin dünya elminə töhfəsini sübut etmişdir.",
        "His work also influenced European mathematics, demonstrating the "
        "contribution of the Timurid scientific center to world science.",
        "Riyaziyyat kainatın dilidir.",
        "Mathematics is the language of the universe.",
        "— Cəmsid əl-Kaşi irsinin ümumi ideyası", "— A guiding idea associated with al-Kashi's legacy",
        ["π-nin 16 onluq yerə qədər hesablanması", "Onluq kəsr hesablamasının inkişafı", "Səmərqənd elmi məktəbi"],
        ["Calculation of pi to 16 decimal places", "Development of decimal fraction computation", "Samarkand scientific school"],
        [
            _w("Risalə fi'l-Hisab", "Treatise on Computation", "Riyazi hesablama üsulları barədə traktat.", "Treatise on methods of mathematical computation."),
            _w("Əl-Kaşi qaydası", "Al-Kashi's rule", "Onluq kəsr hesablamasının inkişaf etdirilmiş formulu.", "Refined formula for decimal fraction computation."),
            _w("Ulubəy rasadxanası", "Ulugh Beg Observatory", "Səmərqənddə aparılmış astronomik müşahidələr.", "Astronomical observations at Samarkand."),
        ],
        [
            _e("🔭", "Səmərqənd", "Samarkand", "Ulubəy rasadxanasında aparılmış elmi işlər.", "Scientific work at Ulugh Beg Observatory."),
            _e("π", "Pi calculation", "Pi calculation", "π ədədini rekord dəqiqliklə hesablamışdır.", "Calculated pi with record precision for his era."),
        ],
        [
            _s("Encyclopaedia Britannica — al-Kashi", "Encyclopaedia Britannica — al-Kashi", "https://www.britannica.com/biography/al-Kashi"),
            _s("Britannica — Ulubəy", "Britannica — Ulugh Beg", "https://www.britannica.com/biography/Ulugh-Beg"),
            _s("Britannica — Səmərqənd", "Britannica — Samarkand", "https://www.britannica.com/place/Samarkand"),
        ],
    ),
    _fig(
        "ahmad_al_farghani", "world", "🌟", "c. 800 – c. 870", "c. 800", "c. 870",
        "Əhməd əl-Fərqani", "Ahmad al-Farghani", "Özbək", "Uzbek",
        "Astronomiya və coğrafiya", "Astronomy and geography",
        "Əbu'l-Abbas Əhməd ibn Məhəmməd əl-Fərqani (Farqan, indiki Özbəkistan) "
        "Fərqani astronom və riyaziyyatçıdır. «Kitab fi-Harakat» əsəri "
        "Avropada «Alfraganus» adı ilə geniş tanınmışdır.",
        "Abu al-Abbas Ahmad ibn Muhammad al-Farghani (Farghana, present-day Uzbekistan) "
        "was an astronomer and mathematician. His Book on Celestial Motions "
        "became widely known in Europe as Alfraganus.",
        "Əl-Fərqani Nil çayının axını, günəş tutulmaları və "
        "səma cisimlərinin hərəkətini izah etmiş, "
        "Əl-Mamun rasadxanasında işləmişdir.",
        "Al-Farghani explained the flow of the Nile, solar eclipses, and "
        "the motion of celestial bodies, and worked at al-Mamun's observatory.",
        "Onun əsərləri Orta Əsr Avropa universitetlərində dərslik "
        "kimi istifadə olunmuş, İslam astronomiyasının Qərb elminə "
        "keçməsinə kömək etmişdir.",
        "His works were used as textbooks in medieval European universities, "
        "helping transmit Islamic astronomy to Western science.",
        "Göy cisimlərinin hərəkəti riyazi qanunlarla izah olunur.",
        "The motion of celestial bodies is explained by mathematical laws.",
        "— Əl-Fərqani irsinin ümumi ideyası", "— A guiding idea associated with al-Farghani's legacy",
        ["İslam astronomiyasının Avropaya ötürülməsi", "Səma cisimlərinin hərəkətinin izahı", "Fərqan elmi məktəbi"],
        ["Transmission of Islamic astronomy to Europe", "Explanation of celestial motion", "Farghana scientific tradition"],
        [
            _w("Kitab fi-Harakat", "Book on Celestial Motions", "Səma cisimlərinin hərəkəti barədə traktat.", "Treatise on the motion of celestial bodies."),
            _w("Alfraganus", "Alfraganus", "Latın tərcüməsi Avropa universitetlərində dərslik olmuşdur.", "Latin translation used as textbook in European universities."),
            _w("Nil çayının ölçülməsi", "Nile measurement", "Nilin axın sürətinin hesablanması.", "Calculation of the Nile's flow rate."),
        ],
        [
            _e("🌍", "Avropa təsiri", "European influence", "Alfraganus Orta Əsr Avropa elminə təsir etmişdir.", "Alfraganus influenced medieval European science."),
            _e("🔭", "Rasadxana", "Observatory", "Əl-Mamun rasadxanasında astronomik işlər aparmışdır.", "Conducted astronomical work at al-Mamun's observatory."),
        ],
        [
            _s("Encyclopaedia Britannica — al-Farghani", "Encyclopaedia Britannica — al-Farghani", "https://www.britannica.com/biography/al-Farghani"),
            _s("Britannica — İslam astronomiyası", "Britannica — Islamic astronomy", "https://www.britannica.com/science/Islamic-astronomy"),
            _s("Britannica — Fərqanə", "Britannica — Fergana", "https://www.britannica.com/place/Fergana-Valley"),
        ],
    ),
    _fig(
        "kamoliddin_bekhzod", "azturk", "🎨", "1455 – 1535", "1455", "1535",
        "Kamoliddin Bəhzhad", "Kamoliddin Bekhzod", "Özbək", "Uzbek",
        "Miniatür rəssamlığı", "Miniature painting",
        "Kamoliddin Bəhzhad (1455–1535) Herat və Buxara məktəblərinin "
        "ən böyük miniatür rəssamıdır. Teymurid dövrünün "
        "vizual incəsənətinin zirvəsini təmsil edir.",
        "Kamoliddin Bekhzod (1455–1535) was the greatest miniaturist of the "
        "Herat and Bukhara schools, representing the peak of Timurid visual art.",
        "Bəhzhad «Nəsrəddin Tusi» və «Səddi İskəndəriyyə» kimi "
        " əsərlərin illüstrasiyalarını yaratmış, "
        "pers-miniatür sənətinə yeni ifadə gətirmişdir.",
        "Bekhzod created illustrations for works such as those of Nasir al-Din Tusi "
        "and Sa'di of Shiraz, bringing new expression to Persian miniature art.",
        "Onun məktəbi sonrakı miniatür rəssamlarına təsir etmiş, "
        "Mərkəzi Asiya incəsənətinin dünya mədəni irsinə daxil olmasına "
        "kömək etmişdir.",
        "His school influenced later miniaturists and helped Central Asian "
        "art enter the canon of world cultural heritage.",
        "Gözəl sənət ruhun güzgüsüdür.",
        "Fine art is the mirror of the soul.",
        "— Bəhzhad irsinin ümumi ideyası", "— A guiding idea associated with Bekhzod's legacy",
        ["Teymurid miniatür sənətinin zirvəsi", "Herat-Buxara rəssamlıq məktəbi", "İllüstrasiya və kitab sənəti"],
        ["Peak of Timurid miniature art", "Herat-Bukhara painting school", "Illustration and book arts"],
        [
            _w("Herat miniatürləri", "Herat miniatures", "Teymurid dövrünün vizual incəsənət əsərləri.", "Visual art works of the Timurid period."),
            _w("Buxara məktəbi", "Bukhara school", "Miniatür rəssamlıq məktəbinin inkişafı.", "Development of the miniature painting school."),
            _w("Kitab illüstrasiyası", "Book illustration", "Ədəbiyyat və elmi əsərlərin vizual tərtibatı.", "Visual design of literary and scholarly works."),
        ],
        [
            _e("🎨", "Herat", "Herat", "Herat məktəbinin aparıcı rəssamı olmuşdur.", "Leading artist of the Herat school."),
            _e("🏛️", "Buxara", "Bukhara", "Buxara saray incəsənətinin inkişafına rəhbərlik etmişdir.", "Led development of Bukhara court art."),
        ],
        [
            _s("Britannica — İslam incəsənəti", "Britannica — Islamic art", "https://www.britannica.com/art/Islamic-arts/Painting"),
            _s("Britannica — Teymurid dövrü", "Britannica — Timurid period", "https://www.britannica.com/biography/Timur"),
            _s("Metropolitan Museum — İslam miniatür", "Metropolitan Museum — Islamic miniature", "https://www.metmuseum.org/learn/educators/curriculum-resources/art-of-the-islamic-world"),
        ],
    ),
    _fig(
        "abd_al_rahman_jami", "world", "✍️", "1414 – 1492", "1414", "1492",
        "Cəmi", "Abd al-Rahman Jami", "Özbək", "Uzbek",
        "Ədəbiyyat və fəlsəfə", "Literature and philosophy",
        "Nur ad-Din Abdurrahman Cəmi (1414–1492) Heratda yaşamış "
        "böyük şair, mütəfəkkir və Naqshbandi müəllimidir. "
        "Fars və özbək mədəni dünyasının klassik fiqurudur.",
        "Nur al-Din Abd al-Rahman Jami (1414–1492) was a major poet, "
        "thinker, and Naqshbandi teacher who lived in Herat, "
        "a classic figure of Persian and Central Asian culture.",
        "Cəmi «Ləvaih», «Yusuf və Zuleyxə» və «Nəfahatü'l-Uns» "
        "kimi əsərlər yazmış, sufizm və ədəbiyyatı birləşdirmişdir.",
        "Jami wrote works including Lawa'ih, Yusuf and Zulaikha, and "
        "Nafahat al-Uns, combining Sufism and literature.",
        "Onun şeirləri və nəsr əsərləri Mərkəzi Asiya, İran və "
        "Hindistan ədəbiyyatına geniş təsir göstərmişdir.",
        "His poetry and prose widely influenced Central Asian, Iranian, "
        "and Indian literature.",
        "Həqiqət həm sözdə, həm ürəkdə axtarılır.",
        "Truth is sought both in words and in the heart.",
        "— Cəmi irsinin ümumi ideyası", "— A guiding idea associated with Jami's legacy",
        ["Fars-özbək ədəbiyyatının klassik fiquru", "Sufi ədəbiyyatının inkişafı", "Herat mədəni həyatının simvolu"],
        ["Classic figure of Persian-Uzbek literature", "Development of Sufi literature", "Symbol of Herat cultural life"],
        [
            _w("Yusuf və Zuleyxə", "Yusuf and Zulaikha", "Məsnavisi ilə tanınan epik poem.", "Epic poem known for its masnavi form."),
            _w("Nəfahatü'l-Uns", "Nafahat al-Uns", "Sufi müəllimlərin biografiyası.", "Biographies of Sufi masters."),
            _w("Ləvaih", "Lawa'ih", "Sufi fəlsəfə və mistika traktatı.", "Sufi philosophical and mystical treatise."),
        ],
        [
            _e("📖", "Herat", "Herat", "Heratın mədəni zirvə dövrünün aparıcı şairi.", "Leading poet of Herat's cultural golden age."),
            _e("🕌", "Naqshbandi", "Naqshbandi", "Naqshbandi sufi təliminin tanınmış müəllimi.", "Renowned teacher of the Naqshbandi Sufi order."),
        ],
        [
            _s("Encyclopaedia Britannica — Jami", "Encyclopaedia Britannica — Jami", "https://www.britannica.com/biography/Jami"),
            _s("Britannica — Fars ədəbiyyatı", "Britannica — Persian literature", "https://www.britannica.com/art/Persian-literature"),
            _s("Britannica — Herat", "Britannica — Herat", "https://www.britannica.com/place/Herat"),
        ],
    ),
    _fig(
        "ahmad_donish", "azturk", "📐", "1827 – 1897", "1827", "1897",
        "Ahmad Doniş", "Ahmad Donish", "Özbək", "Uzbek",
        "Təhsil və diplomatiya", "Education and diplomacy",
        "Ahmad Doniş (1827–1897) Buxaralı alim, pedaqoq, riyaziyyatçı "
        "və diplomatdır. Buxara emirliyində islahat ideyalarının "
        "aparıcı təbliğçilərindən biridir.",
        "Ahmad Donish (1827–1897) was a Bukharan scholar, educator, "
        "mathematician, and diplomat, a leading advocate of reform "
        "in the Bukhara Emirate.",
        "Doniş «Riyaziyyat», «Nodira-i maqol» və «Navodir-ul-maqol» "
        "əsərlərini yazmış, Buxara mədrəsə təhsilini modernləşdirməyə "
        "çalışmışdır.",
        "Donish wrote Riyaziyyat, Nodira-i maqol, and Navodir-ul-maqol, "
        "seeking to modernize madrasa education in Bukhara.",
        "O, Mərkəzi Asiyada elmi maarifçilik və islahat düşüncəsinin "
        "XIX əsrin mühüm nümayəndələrindən biridir.",
        "He is one of the important 19th-century representatives of "
        "scientific enlightenment and reform thought in Central Asia.",
        "Elm və təhsil cəmiyyətin gələcəyidir.",
        "Science and education are the future of society.",
        "— Ahmad Doniş irsinin ümumi ideyası", "— A guiding idea associated with Donish's legacy",
        ["Buxara təhsil islahatlarının təbliği", "Riyaziyyat və elmi ədəbiyyat", "Diplomatik fəaliyyət"],
        ["Advocacy of Bukhara education reform", "Mathematics and scholarly literature", "Diplomatic activity"],
        [
            _w("Riyaziyyat", "Riyaziyyat", "Riyazi biliklərin Buxara dilində təqdimatı.", "Presentation of mathematical knowledge in Bukharan context."),
            _w("Navodir-ul-maqol", "Navodir-ul-maqol", "Elmi və maarifçilik məqalələri toplusu.", "Collection of scientific and enlightenment essays."),
            _w("Diplomatik missiyalar", "Diplomatic missions", "Rusiya və Qərb ölkələrinə səfərlər.", "Missions to Russia and Western countries."),
        ],
        [
            _e("🏛️", "Buxara", "Bukhara", "Buxara emirliyində islahat ideyalarını irəli sürmüşdür.", "Advanced reform ideas in the Bukhara Emirate."),
            _e("🎓", "Maarifçilik", "Enlightenment", "Mədrəsə təhsilinin modernləşdirilməsinə çalışmışdır.", "Sought to modernize madrasa education."),
        ],
        [
            _s("Britannica — Buxara", "Britannica — Bukhara", "https://www.britannica.com/place/Bukhara"),
            _s("Britannica — Orta Asiya tarixi", "Britannica — Central Asia history", "https://www.britannica.com/place/Central-Asia/History"),
            _s("Britannica — İslam təhsili", "Britannica — Islamic education", "https://www.britannica.com/topic/madrasah"),
        ],
    ),

    # ── Turkmen ─────────────────────────────────────────────────────────────
    _fig(
        "abu_al_ghazi_bahadur", "azturk", "📜", "1603 – 1663", "1603", "1663",
        "Abu'l-Ghazi Bahadur", "Abu al-Ghazi Bahadur", "Türkmən", "Turkmen",
        "Tarix və etnoqrafiya", "History and ethnography",
        "Abu'l-Ghazi Bahadur (1603–1663) Xivə xanı və tarixçidir. "
        "«Şəcərə-i türk» («Türkmən şəcərəsi») əsəri ilə "
        "türkmən və türk xalqlarının geneologiyasını və tarixini sənədləşdirmişdir.",
        "Abu al-Ghazi Bahadur (1603–1663) was Khan of Khiva and a historian. "
        "With Shajare-i Tarakime (Genealogy of the Turkmens) he documented "
        "the genealogy and history of Turkmen and Turkic peoples.",
        "Onun əsəri türkmən tayfalarının mənşəyi, adət-ənənələri və "
        "tarixi haqqında fundamental mənbədir; Avropa dillərinə "
        "tərcümə olunmuşdur.",
        "His work is a fundamental source on Turkmen tribal origins, customs, "
        "and history; it was translated into European languages.",
        "Abu'l-Ghazi türkmən tarixi yazısının banisi sayılır və "
        "Mərkəzi Asiya etnoqrafiyasının klassik müəllifidir.",
        "Abu al-Ghazi is considered a founder of Turkmen historical writing "
        "and a classic author of Central Asian ethnography.",
        "Tarix xalqların yaddaşıdır.",
        "History is the memory of peoples.",
        "— Abu'l-Ghazi irsinin ümumi ideyası", "— A guiding idea associated with Abu al-Ghazi's legacy",
        ["Türkmən geneologiyasının sənədləşdirilməsi", "Xivə dövlət tarixi", "Etnoqrafik mənbə"],
        ["Documentation of Turkmen genealogy", "History of the Khiva state", "Ethnographic source"],
        [
            _w("Şəcərə-i türk", "Shajare-i Tarakime", "Türkmən xalqlarının geneologiyası və tarixi.", "Genealogy and history of Turkmen peoples."),
            _w("Xivə xanlığı tarixi", "History of Khiva Khanate", "Xivə dövlətinin siyasi tarixi.", "Political history of the Khiva state."),
            _w("Etnoqrafik qeydlər", "Ethnographic notes", "Tayfa adət-ənənələri barədə məlumat.", "Information on tribal customs."),
        ],
        [
            _e("👑", "Xivə xanı", "Khan of Khiva", "1663-cü ildə Xivə taxtında olmuşdur.", "Ruled the Khiva throne in 1663."),
            _e("📖", "Şəcərə-i türk", "Shajare-i Tarakime", "Türkmən tarixi yazısının klassik əsəri.", "Classic work of Turkmen historical writing."),
        ],
        [
            _s("Britannica — Xivə", "Britannica — Khiva", "https://www.britannica.com/place/Khiva"),
            _s("Britannica — Türkmənistan tarixi", "Britannica — Turkmenistan history", "https://www.britannica.com/place/Turkmenistan/History"),
            _s("Britannica — Orta Asiya", "Britannica — Central Asia", "https://www.britannica.com/place/Central-Asia"),
        ],
    ),
    _fig(
        "seyitnazar_seydi", "azturk", "✍️", "1775 – 1836", "1775", "1836",
        "Seyitnazar Seydi", "Seyitnazar Seydi", "Türkmən", "Turkmen",
        "Şeirlik", "Poetry",
        "Seyitnazar Seydi (1775–1836) klassik türkmən şairi, "
        "Maqtumquli Firaqinin müasili və türkmən ədəbiyyatının "
        "ənənəvi poeziya formasının davamçısıdır.",
        "Seyitnazar Seydi (1775–1836) was a classical Turkmen poet, "
        "contemporary of Mahtumkuli Firaqi and continuer of traditional "
        "Turkmen poetic forms.",
        "Seydi ictimai ədalət, mənəviyyat və türkmən milli "
        "kimliyi mövzularında şeirlər yazmış, "
        "xalq dilində fəlsəfi-fikri irsi inkişaf etdirmişdir.",
        "Seydi wrote poetry on social justice, morality, and Turkmen "
        "national identity, developing philosophical heritage in the vernacular.",
        "Onun yaradıcılığı türkmən ədəbiyyatının klassik dövrünün "
        "mühüm hissəsidir və sonrakı şairlərə təsir etmişdir.",
        "His work is an important part of the classical period of Turkmen "
        "literature and influenced later poets.",
        "Söz — xalqa yol göstərən işıqdır.",
        "The word is the light that guides a people.",
        "— Seyitnazar Seydi irsinin ümumi ideyası", "— A guiding idea associated with Seydi's legacy",
        ["Klassik türkmən poeziyasının inkişafı", "Milli kimlik və mənəviyyat mövzuları", "Maqtumquli ədəbiyyat ənənəsinin davamı"],
        ["Development of classical Turkmen poetry", "Themes of national identity and morality", "Continuation of Mahtumkuli literary tradition"],
        [
            _w("Klassik gəzəllər", "Classical ghazals", "Türkmən dilində lirik şeirlər.", "Lyrical poems in Turkmen."),
            _w("Sosial poeziya", "Social poetry", "Ədalət və cəmiyyət mövzuları.", "Themes of justice and society."),
            _w("Milli irs", "National heritage", "Türkmən mədəni irsinin poeziyada əks olunması.", "Reflection of Turkmen cultural heritage in poetry."),
        ],
        [
            _e("✍️", "Klassik şair", "Classical poet", "Maqtumquli dövrünün aparıcı şairlərindən biri.", "One of the leading poets of Mahtumkuli's era."),
            _e("📚", "Ədəbiyyat irsi", "Literary heritage", "Türkmən ədəbiyyatının klassik dövrünə töhfə.", "Contribution to the classical period of Turkmen literature."),
        ],
        [
            _s("Britannica — Türkmən ədəbiyyatı", "Britannica — Turkmen literature", "https://www.britannica.com/art/Turkmen-literature"),
            _s("Britannica — Türkmənistan", "Britannica — Turkmenistan", "https://www.britannica.com/place/Turkmenistan"),
            _s("UNESCO — Türkmənistan", "UNESCO — Turkmenistan", "https://ich.unesco.org/en/state/turkmenistan-TM"),
        ],
    ),
    # ── Ottoman ─────────────────────────────────────────────────────────────
    _fig(
        "suleiman_the_magnificent", "azturk", "👑", "1494 – 1566", "1494", "1566",
        "Süleyman Qanuni", "Suleiman the Magnificent", "Osmanlı", "Ottoman",
        "Dövlət idarəçiliyi və hüquq", "Governance and law",
        "Süleyman I (1494–1566), Qanuni adı ilə tanınan Osmanlı padşahı, "
        "imperiyanın siyasi, hərbi və mədəni zirvə dövrünün "
        "hökmranıdır. «Qanuni» ləqəbi hüquq sisteminin kodlaşdırılması "
        "ilə bağlıdır.",
        "Suleiman I (1494–1566), known as the Magnificent or the Lawgiver, "
        "ruled at the political, military, and cultural peak of the Ottoman "
        "Empire. His epithet Lawgiver reflects codification of legal systems.",
        "Süleymanın dövründə «Qanunnamə» hüquq kolleksiyaları hazırlanmış, "
        "Memar Sinan, Piri Reis kimi fiqurlar fəaliyyət göstərmiş, "
        "Osmanlı Avropada və Asiyada aparıcı güc olmuşdur.",
        "Under Suleiman, Kanunname legal collections were compiled; figures "
        "such as Mimar Sinan and Piri Reis flourished; the Ottomans became "
        "a leading power in Europe and Asia.",
        "Qanuni dövrü Osmanlı idarəetmə modelinin, incəsənətinin və "
        "hüquq ənənəsinin klassik mərhələsidir.",
        "The age of Suleiman is a classic phase of Ottoman governance, "
        "art, and legal tradition.",
        "Adalet mülkün təməlidir.",
        "Justice is the foundation of rule.",
        "— Süleyman Qanuni irsinin ümumi ideyası", "— A guiding idea associated with Suleiman's legacy",
        ["Osmanlı hüquq sisteminin kodlaşdırılması", "İmperiyanın siyasi zirvəsi", "Mədəni və memarlıq inkişafı"],
        ["Codification of Ottoman legal system", "Political peak of the empire", "Cultural and architectural development"],
        [
            _w("Qanunnamə", "Kanunname", "Osmanlı hüquq kolleksiyaları.", "Ottoman legal collections."),
            _w("Diplomatik siyasət", "Diplomatic policy", "Avropa və Şərq dövlətləri ilə münasibətlər.", "Relations with European and Eastern states."),
            _w("Mədəni patronaj", "Cultural patronage", "Memarlıq və incəsənətin dəstəklənməsi.", "Support for architecture and the arts."),
        ],
        [
            _e("⚖️", "Qanuni", "Lawgiver", "Hüquq sisteminin kodlaşdırılması ilə tanınır.", "Known for codification of the legal system."),
            _e("🏛️", "Zirvə dövr", "Golden age", "Osmanlı imperiyasının ən güclü dövrü.", "The most powerful period of the Ottoman Empire."),
        ],
        [
            _s("Encyclopaedia Britannica — Süleyman I", "Encyclopaedia Britannica — Suleiman I", "https://www.britannica.com/biography/Suleiman-the-Magnificent"),
            _s("Britannica — Osmanlı imperiyası", "Britannica — Ottoman Empire", "https://www.britannica.com/place/Ottoman-Empire"),
            _s("Britannica — İslam hüququ", "Britannica — Islamic law", "https://www.britannica.com/topic/sharia"),
        ],
    ),
    _fig(
        "hayreddin_barbarossa", "azturk", "⚓", "c. 1478 – 1546", "c. 1478", "1546",
        "Xeyrəddin Barbarossa", "Hayreddin Barbarossa", "Osmanlı", "Ottoman",
        "Dənizçilik və hərbi strategiya", "Naval warfare and strategy",
        "Xeyrəddin Barbarossa (təxminən 1478–1546) Osmanlı donanmasının "
        "kapitan-paşası, Aralıq dənizi hakimiyyətinin "
        "mərkəzi fiqurlarından biridir.",
        "Hayreddin Barbarossa (c. 1478–1546) was Kapudan Pasha of the Ottoman "
        "navy and a central figure in Mediterranean naval dominance.",
        "Barbarossa Preveza dəniz döyüşündə (1538) qələbə qazanmış, "
        "Osmanlı dəniz gücünü Qərbi Aralıq dənizində möhkəmləndirmiş, "
        "donanma təşkilatını modernləşdirmişdir.",
        "Barbarossa won the Battle of Preveza (1538), strengthened Ottoman "
        "naval power in the western Mediterranean, and modernized fleet organization.",
        "Onun dəniz strategiyası Osmanlı imperiyasının Avropa və "
        "Şimali Afrikada genişlənməsinə fundamental töhfə vermişdir.",
        "His naval strategy made a fundamental contribution to Ottoman "
        "expansion in Europe and North Africa.",
        "Dəniz — imperiyanın qüvvə yoludur.",
        "The sea is the path of imperial power.",
        "— Barbarossa irsinin ümumi ideyası", "— A guiding idea associated with Barbarossa's legacy",
        ["Osmanlı Aralıq dənizi hakimiyyəti", "Preveza dəniz döyüşü", "Donanma təşkilatının modernləşdirilməsi"],
        ["Ottoman Mediterranean dominance", "Battle of Preveza", "Modernization of naval organization"],
        [
            _w("Preveza döyüşü", "Battle of Preveza", "1538-ci il dəniz qələbəsi.", "1538 naval victory."),
            _w("Kapitan-paşa", "Kapudan Pasha", "Osmanlı donanmasının ali komandanlığı.", "Supreme command of the Ottoman navy."),
            _w("Aralıq dənizi strategiyası", "Mediterranean strategy", "Qərbi Aralıq dənizi siyasəti.", "Western Mediterranean policy."),
        ],
        [
            _e("⚓", "Preveza", "Preveza", "1538-ci il dəniz qələbəsi ilə tanınır.", "Known for the 1538 naval victory."),
            _e("🌊", "Donanma", "Navy", "Osmanlı dəniz gücünün zirvə komandiri.", "Peak commander of Ottoman naval power."),
        ],
        [
            _s("Encyclopaedia Britannica — Barbarossa", "Encyclopaedia Britannica — Barbarossa", "https://www.britannica.com/biography/Barbarossa-Ottoman-admiral"),
            _s("Britannica — Osmanlı donanması", "Britannica — Ottoman navy", "https://www.britannica.com/topic/Ottoman-Empire/Military-organization"),
            _s("Britannica — Preveza döyüşü", "Britannica — Battle of Preveza", "https://www.britannica.com/event/Battle-of-Preveza"),
        ],
    ),
    _fig(
        "ahmed_cevdet_pasha", "azturk", "⚖️", "1822 – 1895", "1822", "1895",
        "Ahmed Cəvdət Paşa", "Ahmed Cevdet Pasha", "Osmanlı", "Ottoman",
        "Hüquq və tarix", "Law and history",
        "Ahmed Cəvdət Paşa (1822–1895) Osmanlı tarixçisi, hüquqşünas "
        "və dövlət xadimidir. «Mecelle» — İslam mülki hüququnun "
        "kodlaşdırılması — layihəsinin aparıcı müəllifidir.",
        "Ahmed Cevdet Pasha (1822–1895) was an Ottoman historian, jurist, "
        "and statesman. He was a leading author of the Mecelle, "
        "the codification of Islamic civil law.",
        "Cəvdət Paşa «Tarih-i Cəvdət» çoxcildli tarixi yazmış, "
        "məktəb islahatları aparmış və Osmanlı hüquq sisteminin "
        "modernləşdirilməsinə rəhbərlik etmişdir.",
        "Cevdet Pasha wrote the multi-volume Tarih-i Cevdet, carried out "
        "school reforms, and led modernization of the Ottoman legal system.",
        "«Mecelle» Osmanlı imperiyasının hüquq sisteminin "
        "klasik kodu olmuş, müasir Türkiyə və region hüququna "
        "uzunmüddətli təsir göstərmişdir.",
        "The Mecelle became the classic code of the Ottoman legal system "
        "and long influenced modern Turkish and regional law.",
        "Hüquq cəmiyyətin nizamının təməlidir.",
        "Law is the foundation of social order.",
        "— Ahmed Cəvdət Paşa irsinin ümumi ideyası", "— A guiding idea associated with Cevdet Pasha's legacy",
        ["«Mecelle» — İslam mülki hüququnun kodu", "Osmanlı tarixi yazısı", "Təhsil islahatları"],
        ["The Mecelle — code of Islamic civil law", "Ottoman historical writing", "Education reforms"],
        [
            _w("Mecelle", "Mecelle", "İslam mülki hüququnun kodlaşdırılmış mətni.", "Codified text of Islamic civil law."),
            _w("Tarih-i Cəvdət", "Tarih-i Cevdet", "Osmanlı tarixi üzrə çoxcildli əsər.", "Multi-volume work on Ottoman history."),
            _w("Məktəb islahatları", "School reforms", "Osmanlı təhsil sisteminin modernləşdirilməsi.", "Modernization of the Ottoman education system."),
        ],
        [
            _e("⚖️", "Mecelle", "Mecelle", "İslam mülki hüququnun kodlaşdırılmasına rəhbərlik etmişdir.", "Led codification of Islamic civil law."),
            _e("📚", "Tarixçi", "Historian", "Osmanlı tarixinin sistemli tədqiqi.", "Systematic study of Ottoman history."),
        ],
        [
            _s("Encyclopaedia Britannica — Ahmed Cevdet Pasha", "Encyclopaedia Britannica — Ahmed Cevdet Pasha", "https://www.britannica.com/biography/Ahmed-Cevdet-Pasa"),
            _s("Britannica — Mecelle", "Britannica — Mecelle", "https://www.britannica.com/topic/Mecelle"),
            _s("Britannica — Osmanlı tarixi", "Britannica — Ottoman history", "https://www.britannica.com/place/Ottoman-Empire/History"),
        ],
    ),
    _fig(
        "halide_edib_adivar", "azturk", "✍️", "1884 – 1964", "1884", "1964",
        "Halide Edib Adıvar", "Halide Edib Adivar", "Osmanlı", "Ottoman",
        "Ədəbiyyat və sosial islahat", "Literature and social reform",
        "Halide Edib Adıvar (1884–1964) Osmanlı və Türkiyə "
        "yazıçısı, feminist və ictimai xadimdir. "
        "Qadın hüquqları və milli müstəqillik ideyalarının "
        "aparıcı təbliğçilərindən biridir.",
        "Halide Edib Adivar (1884–1964) was an Ottoman and Turkish writer, "
        "feminist, and public figure, a leading advocate of women's rights "
        "and national independence.",
        "Adıvar «Səfil Vatən», «Yeni Turan» və «Ateşten Gömlek» "
        "romanlarını yazmış, qadın təhsili və ictimai iştirak "
        "mövzularını irəli sürmüşdür.",
        "Adivar wrote novels including The Wretched Land, The New Turan, "
        "and The Shirt of Flame, advancing themes of women's education "
        "and social participation.",
        "O, Türkiyə müasir ədəbiyyatının və qadın hərəkatının "
        "formalaşmasında mühüm rol oynamışdır.",
        "She played an important role in the formation of modern Turkish "
        "literature and the women's movement.",
        "Azadlıq həm sözün, həm fəaliyyətin nəticəsidir.",
        "Freedom is the result of both words and action.",
        "— Halide Edib irsinin ümumi ideyası", "— A guiding idea associated with Halide Edib's legacy",
        ["Türkiyə müasir romanının inkişafı", "Qadın hüquqları və təhsili", "Milli müstəqillik ideyaları"],
        ["Development of the modern Turkish novel", "Women's rights and education", "Ideas of national independence"],
        [
            _w("Ateşten Gömlek", "The Shirt of Flame", "Milli mücadilə mövzusunda roman.", "Novel on the national struggle."),
            _w("Səfil Vatən", "The Wretched Land", "Sosial-realist roman.", "Social-realist novel."),
            _w("Qadın hüquqları", "Women's rights", "Qadın təhsili və ictimai iştirak.", "Women's education and social participation."),
        ],
        [
            _e("✍️", "Romançı", "Novelist", "Türkiyə müasir ədəbiyyatının aparıcı yazıçılarından.", "Leading writer of modern Turkish literature."),
            _e("👩", "Feminist", "Feminist", "Qadın hüquqları və təhsilinin təbliğçisi.", "Advocate of women's rights and education."),
        ],
        [
            _s("Encyclopaedia Britannica — Halide Edib Adıvar", "Encyclopaedia Britannica — Halide Edib Adivar", "https://www.britannica.com/biography/Halide-Edib-Adivar"),
            _s("Britannica — Türk ədəbiyyatı", "Britannica — Turkish literature", "https://www.britannica.com/art/Turkish-literature"),
            _s("Britannica — Qadın hüquqları", "Britannica — Women's rights", "https://www.britannica.com/topic/womens-movement"),
        ],
    ),
    _fig(
        "sokollu_mehmed_pasha", "azturk", "🏛️", "1505 – 1579", "1505", "1579",
        "Sokollu Mehmed Paşa", "Sokollu Mehmed Pasha", "Osmanlı", "Ottoman",
        "Dövlət idarəçiliyi", "Governance and administration",
        "Sokollu Mehmed Paşa (1505–1579) Süleyman Qanuni, Selim II "
        "və Murad III dövrlərində böyük vezir olmuş, "
        "Osmanlı imperiyasının idarəetmə sistemini möhkəmləndirmişdir.",
        "Sokollu Mehmed Pasha (1505–1579) served as grand vizier under "
        "Suleiman, Selim II, and Murad III, strengthening Ottoman "
        "administrative systems.",
        "Sokollu su təchizatı layihələri, maliyyə islahatları və "
        "strategik tikinti işləri həyata keçirmiş, "
        "imperiyanın mərkəzi idarəçiliyini inkişaf etdirmişdir.",
        "Sokollu implemented water supply projects, fiscal reforms, and "
        "strategic construction, developing central imperial administration.",
        "Onun idarəetmə modeli Osmanlı bürokratiyasının "
        "klasik dövrünü təmsil edir.",
        "His governance model represents the classic period of Ottoman bureaucracy.",
        "Güclü idarəetmə imperiyanın davamlılığını təmin edir.",
        "Strong administration ensures the continuity of empire.",
        "— Sokollu Mehmed Paşa irsinin ümumi ideyası", "— A guiding idea associated with Sokollu's legacy",
        ["Osmanlı böyük vezirliyi", "Maliyyə və infrastruktur islahatları", "Mərkəzi idarəetmənin inkişafı"],
        ["Ottoman grand vizierate", "Fiscal and infrastructure reforms", "Development of central administration"],
        [
            _w("Böyük vezirlik", "Grand vizierate", "Uzun müddətli ali dövlət idarəçiliyi.", "Long-term supreme state administration."),
            _w("Su təchizatı layihələri", "Water supply projects", "İstanbul və digər şəhərlərdə infrastruktur.", "Infrastructure in Istanbul and other cities."),
            _w("Maliyyə islahatları", "Fiscal reforms", "İmperiya maliyyə sisteminin təkmilləşdirilməsi.", "Improvement of imperial fiscal system."),
        ],
        [
            _e("🏛️", "Böyük vezir", "Grand vizier", "Üç padşah dövründə böyük vezir olmuşdur.", "Grand vizier under three sultans."),
            _e("💧", "İnfrastruktur", "Infrastructure", "Su təchizatı və tikinti layihələri.", "Water supply and construction projects."),
        ],
        [
            _s("Encyclopaedia Britannica — Sokollu Mehmed Pasha", "Encyclopaedia Britannica — Sokollu Mehmed Pasha", "https://www.britannica.com/biography/Sokollu-Mehmed-Pasa"),
            _s("Britannica — Osmanlı idarəetməsi", "Britannica — Ottoman administration", "https://www.britannica.com/place/Ottoman-Empire/Administration"),
            _s("Britannica — Süleyman dövrü", "Britannica — Age of Suleiman", "https://www.britannica.com/biography/Suleiman-the-Magnificent"),
        ],
    ),

    # ── Chinese ─────────────────────────────────────────────────────────────
    _fig(
        "laozi", "world", "☯️", "6th century BCE", "6th c. BCE", "6th c. BCE",
        "Laozi", "Laozi", "Çin", "Chinese",
        "Fəlsəfə", "Philosophy",
        "Laozi (tradisional olaraq VI əsr əvvəl) «Dao de jing» (Tao Te Ching) "
        "əsərinin müəllifi sayılan Çin fəlsəfəsinin banisidir. "
        "Daoizm fəlsəfi və mənəvi ənənəsinin formalaşmasına "
        "fundamental töhfə vermişdir.",
        "Laozi (traditionally 6th century BCE) is regarded as the author of "
        "the Tao Te Ching and founder of Chinese Daoist philosophical "
        "and spiritual tradition.",
        "Laozi «Dao» (Yol) anlayışını, təbiətlə uyğunluq və "
        "sadəlik ideyalarını inkişaf etdirmiş, "
        "Çin, Koreya, Yaponiya və dünya fəlsəfəsinə təsir etmişdir.",
        "Laozi developed the concept of the Dao (Way), harmony with nature, "
        "and simplicity, influencing Chinese, Korean, Japanese, and world philosophy.",
        "«Dao de jing» dünya ədəbiyyatının və fəlsəfəsinin "
        "ən çox tərcümə olunan klassiklərindən biridir.",
        "The Tao Te Ching is among the most translated classics "
        "of world literature and philosophy.",
        "Yol hər şeyin içindədir.",
        "The Way is within all things.",
        "— Laozi, «Dao de jing»", "— Laozi, Tao Te Ching",
        ["Daoizm fəlsəfəsinin banisi", "«Dao de jing» klassik əsəri", "Çin mənəvi ənənəsinin formalaşması"],
        ["Founder of Daoist philosophy", "Classic Tao Te Ching", "Formation of Chinese spiritual tradition"],
        [
            _w("Dao de jing", "Tao Te Ching", "Daoizmin fundamental fəlsəfi əsəri.", "Fundamental philosophical work of Daoism."),
            _w("Dao (Yol)", "Dao (Way)", "Kainatın və həyatın əsas prinsipi.", "Fundamental principle of cosmos and life."),
            _w("Wu wei", "Wu wei", "Təbii axına uyğun hərəkət prinsipi.", "Principle of action in harmony with natural flow."),
        ],
        [
            _e("📖", "Dao de jing", "Tao Te Ching", "Dünyanın ən təsirli fəlsəfi mətnlərindən biri.", "One of the world's most influential philosophical texts."),
            _e("☯️", "Daoizm", "Daoism", "Çin fəlsəfə və dininin əsas istiqaməti.", "Major direction of Chinese philosophy and religion."),
        ],
        [
            _s("Stanford Encyclopedia — Laozi", "Stanford Encyclopedia — Laozi", "https://plato.stanford.edu/entries/laozi/"),
            _s("Encyclopaedia Britannica — Laozi", "Encyclopaedia Britannica — Laozi", "https://www.britannica.com/biography/Laozi"),
            _s("Britannica — Daoizm", "Britannica — Daoism", "https://www.britannica.com/topic/Daoism"),
        ],
    ),
    _fig(
        "sima_qian", "world", "📜", "c. 145 – c. 86 BCE", "c. 145 BCE", "c. 86 BCE",
        "Sima Qian", "Sima Qian", "Çin", "Chinese",
        "Tarix", "History",
        "Sima Qian (təxminən e.ə. 145–86) Çin tarixinin "
        "klassik müəllifi, «Shiji» (Tarix yazıları) "
        "əsərinin müəllifidir. Dünya tarixi yazısının "
        "banilərindən biri sayılır.",
        "Sima Qian (c. 145–86 BCE) was the classic author of Chinese history, "
        "writer of Shiji (Records of the Grand Historian), "
        "regarded as a founder of world historiography.",
        "Sima Qian Çin imperiyasının tarixi, biografiya janrının "
        "formalaşması və hadisələrin səbəb-nəticə analizi "
        "üzrə metodoloji yanaşma yaratmışdır.",
        "Sima Qian created methodology for analyzing causes and effects of events, "
        "forming the biographical genre in the history of the Chinese empire.",
        "«Shiji» sonrakı Çin, Koreya, Yaponiya və dünya "
        "tarixçiliyinə fundamental model olmuşdur.",
        "Shiji became a foundational model for later Chinese, Korean, "
        "Japanese, and world historiography.",
        "Tarixçi həqiqəti qorumaq öhdəliyini daşıyır.",
        "The historian bears the duty to preserve truth.",
        "— Sima Qian irsinin ümumi ideyası", "— A guiding idea associated with Sima Qian's legacy",
        ["«Shiji» — Çin tarixinin klassik əsəri", "Biografiya janrının formalaşması", "Tarix yazısında metodologiya"],
        ["Shiji — classic work of Chinese history", "Formation of biographical genre", "Methodology in historical writing"],
        [
            _w("Shiji", "Shiji (Records of the Grand Historian)", "Çin tarixinin ilk sistemli kronikası.", "First systematic chronicle of Chinese history."),
            _w("Biografiya janrı", "Biographical genre", "Tarixi şəxsiyyətlərin həyatının təsviri.", "Description of historical figures' lives."),
            _w("Səbəb-nəticə analizi", "Causal analysis", "Tarixi hadisələrin izah metodologiyası.", "Methodology for explaining historical events."),
        ],
        [
            _e("📖", "Shiji", "Shiji", "Çin tarixinin klassik kronikası.", "Classic chronicle of Chinese history."),
            _e("🏛️", "Tarixçi", "Historian", "Dünya tarixi yazısının banilərindən biri.", "One of the founders of world historiography."),
        ],
        [
            _s("Encyclopaedia Britannica — Sima Qian", "Encyclopaedia Britannica — Sima Qian", "https://www.britannica.com/biography/Sima-Qian"),
            _s("Britannica — Çin tarixi", "Britannica — Chinese history", "https://www.britannica.com/topic/Chinese-history"),
            _s("Stanford Encyclopedia — Çin fəlsəfəsi", "Stanford Encyclopedia — Chinese philosophy", "https://plato.stanford.edu/entries/chinese-change/"),
        ],
    ),
    _fig(
        "cai_lun", "world", "📄", "c. 50 – 121", "c. 50", "121",
        "Cai Lun", "Cai Lun", "Çin", "Chinese",
        "Texnologiya", "Technology",
        "Cai Lun (təxminən 50–121) Han sülaləsinin məmuru, "
        "kağız istehsalının standartlaşdırılmasına "
        "fundamental töhfə vermişdir. Kağız sivilizasiyanın "
        "inkişafında həlledici rol oynamışdır.",
        "Cai Lun (c. 50–121) was a Han dynasty official who made "
        "a fundamental contribution to standardizing paper production. "
        "Paper played a decisive role in the development of civilization.",
        "Cai Lun lifli materialdan (təxminən ağcaqayın, konop, "
        "tənəffüs artıqlığı) kağız hazırlama texnologiyasını "
        "təkmilləşdirmiş və imperiya miqyasında tətbiq etmişdir.",
        "Cai Lun improved technology for making paper from fibrous materials "
        "(such as bark, hemp, and textile waste) and applied it empire-wide.",
        "Kağız bilik, ədəbiyyat, idarəetmə və elm "
        "infrastrukturunun qlobal yayılmasını mümkün etmişdir.",
        "Paper enabled the global spread of knowledge, literature, "
        "administration, and science infrastructure.",
        "Kağız biliklərin daşıyıcısıdır.",
        "Paper is the carrier of knowledge.",
        "— Cai Lun irsinin ümumi ideyası", "— A guiding idea associated with Cai Lun's legacy",
        ["Kağız istehsalının standartlaşdırılması", "Bilik və sənəd daşıyıcısının ixtirası", "Sivilizasiya inkişafına texnoloji töhfə"],
        ["Standardization of paper production", "Invention of a knowledge and document medium", "Technological contribution to civilization"],
        [
            _w("Kağız texnologiyası", "Paper technology", "Lifli materialdan kağız istehsalı.", "Paper production from fibrous materials."),
            _w("Han sülaləsi", "Han dynasty", "İmperiya miqyasında texnologiyanın tətbiqi.", "Empire-wide application of technology."),
            _w("Sənəd daşıyıcısı", "Document medium", "Yazı və idarəetmə üçün material.", "Material for writing and administration."),
        ],
        [
            _e("📄", "Kağız", "Paper", "Kağız istehsalının standartlaşdırılması ilə tanınır.", "Known for standardizing paper production."),
            _e("🌍", "Sivilizasiya", "Civilization", "Kağız bilik yayılmasının əsas vasitəsidir.", "Paper is a key medium for spreading knowledge."),
        ],
        [
            _s("Encyclopaedia Britannica — Cai Lun", "Encyclopaedia Britannica — Cai Lun", "https://www.britannica.com/biography/Cai-Lun"),
            _s("Britannica — Kağız tarixi", "Britannica — Paper", "https://www.britannica.com/technology/paper"),
            _s("Britannica — Han sülaləsi", "Britannica — Han dynasty", "https://www.britannica.com/topic/Han-dynasty"),
        ],
    ),
    _fig(
        "guo_shoujing", "world", "🔭", "1231 – 1316", "1231", "1316",
        "Guo Shoujing", "Guo Shoujing", "Çin", "Chinese",
        "Astronomiya və riyaziyyat", "Astronomy and mathematics",
        "Guo Shoujing (1231–1316) Yuan sülaləsi dövrünün "
        "aparıcı astronomu və mühəndisidir. "
        "Təqvim islahatı və su idarəetmə layihələri "
        "ilə tanınır.",
        "Guo Shoujing (1231–1316) was a leading astronomer and engineer "
        "of the Yuan dynasty, known for calendar reform and "
        "water management projects.",
        "Guo Shoujing «Shoushi Calendar» təqvimini hazırlamış, "
        "parallaks ölçmələri aparmış və "
        "Çin boyunca su kanalları layihələndirmişdir.",
        "Guo Shoujing prepared the Shoushi Calendar, conducted parallax "
        "measurements, and designed canal systems across China.",
        "Onun astronomik və mühəndislik işləri Çin elminin "
        "orta əsr zirvəsini təmsil edir.",
        "His astronomical and engineering work represents the "
        "medieval peak of Chinese science.",
        "Elm həm göyü, həm torpağı anlamaq deməkdir.",
        "Science means understanding both sky and earth.",
        "— Guo Shoujing irsinin ümumi ideyası", "— A guiding idea associated with Guo Shoujing's legacy",
        ["Shoushi təqvim islahatı", "Astronomik müşahidələr", "Su idarəetmə mühəndisliyi"],
        ["Shoushi calendar reform", "Astronomical observations", "Water management engineering"],
        [
            _w("Shoushi Calendar", "Shoushi Calendar", "Yuan dövrünün dəqiq təqvimi.", "Precise calendar of the Yuan period."),
            _w("Parallaks ölçmələri", "Parallax measurements", "Astronomik müşahidə metodları.", "Astronomical observation methods."),
            _w("Su kanalları", "Canal systems", "Kənd təsərrüfatı su idarəetməsi.", "Agricultural water management."),
        ],
        [
            _e("🔭", "Təqvim", "Calendar", "Shoushi təqvimi uzun müddət istifadə olunmuşdur.", "Shoushi calendar was used for a long period."),
            _e("💧", "Mühəndislik", "Engineering", "Su idarəetmə layihələri həyata keçirmişdir.", "Implemented water management projects."),
        ],
        [
            _s("Encyclopaedia Britannica — Guo Shoujing", "Encyclopaedia Britannica — Guo Shoujing", "https://www.britannica.com/biography/Guo-Shoujing"),
            _s("Britannica — Çin astronomiyası", "Britannica — Chinese astronomy", "https://www.britannica.com/science/Chinese-astronomy"),
            _s("Britannica — Yuan sülaləsi", "Britannica — Yuan dynasty", "https://www.britannica.com/topic/Yuan-dynasty"),
        ],
    ),
    _fig(
        "zheng_he", "world", "⛵", "1371 – 1433", "1371", "1433",
        "Zheng He", "Zheng He", "Çin", "Chinese",
        "Dənizçilik və diplomatiya", "Maritime exploration and diplomacy",
        "Zheng He (1371–1433) Ming sülaləsinin admiralı, "
        "yedi böyük dəniz ekspedisiyasının rəhbəridir. "
        "Orta çağın ən böyük dəniz səfərlərindən birini "
        "həyata keçirmişdir.",
        "Zheng He (1371–1433) was a Ming dynasty admiral who led "
        "seven major maritime expeditions, among the greatest "
        "sea voyages of the Middle Ages.",
        "Zheng He flotu Hindistan Okeanına, Persiya körfəzinə, "
        "Şərqi Afrikaya qədər səyahət etmiş, "
        "diplomatik və ticarət əlaqələri qurmuşdur.",
        "Zheng He's fleet traveled to the Indian Ocean, Persian Gulf, "
        "and East Africa, establishing diplomatic and trade relations.",
        "Onun səfərləri qlobal dənizçilik, coğrafiya və "
        "mədəni mübadilənin tarixinə fundamental töhfə vermişdir.",
        "His voyages made a fundamental contribution to the history "
        "of global seafaring, geography, and cultural exchange.",
        "Dəniz xalqları bir-birinə yaxınlaşdırır.",
        "The sea brings peoples closer together.",
        "— Zheng He irsinin ümumi ideyası", "— A guiding idea associated with Zheng He's legacy",
        ["Yeddi dəniz ekspedisiyası", "Hindistan Okeanı dənizçiliyi", "Diplomatik və ticarət əlaqələri"],
        ["Seven maritime expeditions", "Indian Ocean seafaring", "Diplomatic and trade relations"],
        [
            _w("Ming dəniz ekspedisiyaları", "Ming maritime expeditions", "1405–1433-cü illər arasında yeddi səfər.", "Seven voyages between 1405 and 1433."),
            _w("Treasure fleet", "Treasure fleet", "Böyük dəniz flotu.", "Large maritime fleet."),
            _w("Diplomatik missiyalar", "Diplomatic missions", "Asiya və Afrika limanlarına səfərlər.", "Voyages to Asian and African ports."),
        ],
        [
            _e("⛵", "Admiral", "Admiral", "Ming donanmasının ali komandiri.", "Supreme commander of the Ming navy."),
            _e("🌍", "Ekspedisiyalar", "Expeditions", "Orta çağın ən böyük dəniz səfərləri.", "Among the greatest medieval sea voyages."),
        ],
        [
            _s("Encyclopaedia Britannica — Zheng He", "Encyclopaedia Britannica — Zheng He", "https://www.britannica.com/biography/Zheng-He"),
            _s("Britannica — Ming sülaləsi", "Britannica — Ming dynasty", "https://www.britannica.com/topic/Ming-dynasty"),
            _s("Britannica — Dənizçilik tarixi", "Britannica — Navigation history", "https://www.britannica.com/technology/navigation"),
        ],
    ),
    _fig(
        "wang_yangming", "world", "📿", "1472 – 1529", "1472", "1529",
        "Wang Yangming", "Wang Yangming", "Çin", "Chinese",
        "Fəlsəfə", "Philosophy",
        "Wang Yangming (1472–1529) Ming dövrünün aparıcı "
        "neo-konfutsi fəlsəfəçisi və dövlət xadimidir. "
        "«Zhi xing he yi» (Bilik və hərəkət vahiddir) "
        "prinsipini irəli sürmüşdür.",
        "Wang Yangming (1472–1529) was a leading Ming neo-Confucian "
        "philosopher and statesman who advanced the principle "
        "that knowledge and action are one.",
        "Wang «liangzhi» (inherent moral knowing) anlayışını "
        "inkişaf etdirmiş, Konfutsi fəlsəfəsinə praktik "
        "etik boyukst vermişdir.",
        "Wang developed the concept of liangzhi (inherent moral knowing), "
        "giving practical ethical depth to Confucian philosophy.",
        "Onun fəlsəfəsi Çin, Koreya və Yaponiyada geniş "
        "təsir göstərmiş, Şərq fəlsəfəsinin klassik "
        "istiqamətlərindən biridir.",
        "His philosophy widely influenced China, Korea, and Japan "
        "and is a classic direction of Eastern philosophy.",
        "Bilik hərəkətlə tamamlanır.",
        "Knowledge is completed through action.",
        "— Wang Yangming", "— Wang Yangming",
        ["Neo-konfutsi fəlsəfəsinin inkişafı", "«Zhi xing he yi» prinsipi", "Praktik etika"],
        ["Development of neo-Confucian philosophy", "Unity of knowledge and action", "Practical ethics"],
        [
            _w("Zhi xing he yi", "Unity of knowledge and action", "Fəlsəfi prinsip.", "Philosophical principle."),
            _w("Liangzhi", "Liangzhi", "Daxili mənəvi bilik anlayışı.", "Concept of inherent moral knowing."),
            _w("Wang Xue", "Wang Xue (School of Mind)", "Wang Yangming fəlsəfi məktəbi.", "Wang Yangming philosophical school."),
        ],
        [
            _e("📿", "Neo-konfutsi", "Neo-Confucian", "Ming dövrünün aparıcı fəlsəfəçisi.", "Leading philosopher of the Ming period."),
            _e("⚖️", "Etika", "Ethics", "Praktik etik fəlsəfənin inkişafı.", "Development of practical ethical philosophy."),
        ],
        [
            _s("Stanford Encyclopedia — Wang Yangming", "Stanford Encyclopedia — Wang Yangming", "https://plato.stanford.edu/entries/wang-yangming/"),
            _s("Encyclopaedia Britannica — Wang Yangming", "Encyclopaedia Britannica — Wang Yangming", "https://www.britannica.com/biography/Wang-Yangming"),
            _s("Britannica — Neo-konfutsianlıq", "Britannica — Neo-Confucianism", "https://www.britannica.com/topic/Neo-Confucianism"),
        ],
    ),
    _fig(
        "lu_xun", "world", "✍️", "1881 – 1936", "1881", "1936",
        "Lu Xun", "Lu Xun", "Çin", "Chinese",
        "Ədəbiyyat", "Literature",
        "Lu Xun (1881–1936) Çin müasir ədəbiyyatının "
        "atası sayılan yazıçı, publisist və ictimai "
        "xadimdir. Realist qısa hekayə və esse janrlarının "
        "inkişafına fundamental töhfə vermişdir.",
        "Lu Xun (1881–1936) is regarded as the father of modern Chinese "
        "literature, a writer, essayist, and public figure who "
        "fundamentally contributed to realist short fiction and essays.",
        "Lu Xun «Diary of a Madman» (1918) və «The True Story of Ah Q» "
        "kimi əsərlərlə feodal cəmiyyət tənqidini irəli sürmüş, "
        "Çin yazı dilinin modernləşməsinə kömək etmişdir.",
        "Lu Xun advanced critique of feudal society with works such as "
        "Diary of a Madman (1918) and The True Story of Ah Q, "
        "helping modernize written Chinese.",
        "Onun yaradıcılığı XX əsr Çin mədəni "
        "və sosial düşüncəsinin formalaşmasında "
        "mərkəzi rol oynamışdır.",
        "His work played a central role in forming twentieth-century "
        "Chinese cultural and social thought.",
        "Ümid yoxdur demək olmaz.",
        "Hope cannot be said to exist, yet it cannot be denied.",
        "— Lu Xun", "— Lu Xun",
        ["Çin müasir ədəbiyyatının banisi", "Realist qısa hekayə janrı", "Feodal cəmiyyət tənqidi"],
        ["Founder of modern Chinese literature", "Realist short fiction genre", "Critique of feudal society"],
        [
            _w("Diary of a Madman", "Diary of a Madman", "1918-ci il modern qısa hekayə.", "1918 modern short story."),
            _w("The True Story of Ah Q", "The True Story of Ah Q", "Realist satirik roman.", "Realist satirical novella."),
            _w("Vernacular writing", "Vernacular writing", "Çin yazı dilinin modernləşməsi.", "Modernization of written Chinese."),
        ],
        [
            _e("✍️", "Modern ədəbiyyat", "Modern literature", "Çin müasir ədəbiyyatının atası.", "Father of modern Chinese literature."),
            _e("📰", "Publisist", "Essayist", "Sosial tənqid və ictimai fəaliyyət.", "Social critique and public activity."),
        ],
        [
            _s("Encyclopaedia Britannica — Lu Xun", "Encyclopaedia Britannica — Lu Xun", "https://www.britannica.com/biography/Lu-Xun"),
            _s("Britannica — Çin ədəbiyyatı", "Britannica — Chinese literature", "https://www.britannica.com/art/Chinese-literature/Modern-literature"),
            _s("Britannica — XX əsr Çin tarixi", "Britannica — 20th-century China", "https://www.britannica.com/place/China/The-republican-revolution-of-1911"),
        ],
    ),
    _fig(
        "li_bai", "world", "🌸", "701 – 762", "701", "762",
        "Li Bai", "Li Bai", "Çin", "Chinese",
        "Şeirlik", "Poetry",
        "Li Bai (701–762) Tan sülaləsinin ən böyük şairlərindən "
        "biridir. Romantik poeziyanın zirvəsini təmsil edir "
        "və Çin ədəbiyyatının klassik simvollarından biridir.",
        "Li Bai (701–762) was one of the greatest poets of the Tang dynasty, "
        "representing the peak of romantic poetry and a classic "
        "symbol of Chinese literature.",
        "Li Bai təbiət, sərbəstlik, dostluq və mistisizm "
        "mövzularında yüzlərlə şeir yazmış, "
        "Çin, Koreya və Yaponiya poeziyasına təsir etmişdir.",
        "Li Bai wrote hundreds of poems on nature, freedom, friendship, "
        "and mysticism, influencing Chinese, Korean, and Japanese poetry.",
        "Onun şeirləri dünya ədəbiyyatının klassik "
        "repertuarına daxildir və min illərdir "
        "tədris olunur.",
        "His poems belong to the classic repertoire of world literature "
        "and have been taught for millennia.",
        "Şeir ruhun sərbəstliyidir.",
        "Poetry is the freedom of the soul.",
        "— Li Bai irsinin ümumi ideyası", "— A guiding idea associated with Li Bai's legacy",
        ["Tan poeziyasının zirvəsi", "Romantik şeirlik", "Çin ədəbiyyatının klassik simvolu"],
        ["Peak of Tang poetry", "Romantic poetry", "Classic symbol of Chinese literature"],
        [
            _w("Tan şeirləri", "Tang poems", "Klassik Çin poeziyasının zirvəsi.", "Peak of classical Chinese poetry."),
            _w("Romantik poeziya", "Romantic poetry", "Təbiət və sərbəstlik mövzuları.", "Themes of nature and freedom."),
            _w("«Jing Ye Si»", "Quiet Night Thoughts", "Dünyanın ən tanınmış Çin şeirlərindən biri.", "One of the world's best-known Chinese poems."),
        ],
        [
            _e("🌸", "Tan şairi", "Tang poet", "Tan sülaləsinin ən böyük şairlərindən.", "Among the greatest poets of the Tang dynasty."),
            _e("🌍", "Dünya ədəbiyyatı", "World literature", "Şeirləri qlobal repertuara daxildir.", "Poems belong to the global repertoire."),
        ],
        [
            _s("Encyclopaedia Britannica — Li Bai", "Encyclopaedia Britannica — Li Bai", "https://www.britannica.com/biography/Li-Bai"),
            _s("Britannica — Tan sülaləsi", "Britannica — Tang dynasty", "https://www.britannica.com/topic/Tang-dynasty"),
            _s("Britannica — Çin poeziyası", "Britannica — Chinese poetry", "https://www.britannica.com/art/Chinese-literature/Poetry"),
        ],
    ),
    _fig(
        "du_fu", "world", "🍂", "712 – 770", "712", "770",
        "Du Fu", "Du Fu", "Çin", "Chinese",
        "Şeirlik", "Poetry",
        "Du Fu (712–770) Tan sülaləsinin ən böyük realist "
        "şairidir. Li Bai ilə birlikdə Çin poeziyasının "
        "klassik zirvəsini təmsil edir.",
        "Du Fu (712–770) was the greatest realist poet of the Tang dynasty, "
        "representing with Li Bai the classic peak of Chinese poetry.",
        "Du Fu müharibə, yoxsulluq, ictimati ədalətsizlik "
        "və fərdi faciə mövzularında dərin şeirlər yazmış, "
        "tarixi hadisələri poeziyada əks etdirmişdir.",
        "Du Fu wrote profound poems on war, poverty, social injustice, "
        "and personal tragedy, reflecting historical events in poetry.",
        "Ona «şeir tarixi» (poet-historian) deyilir; "
        "əsərləri Çin mədəni yaddaşının ayrılmaz hissəsidir.",
        "He is called the poet-historian; his works are an integral "
        "part of Chinese cultural memory.",
        "Şeir cəmiyyətin güzgüsüdür.",
        "Poetry is the mirror of society.",
        "— Du Fu irsinin ümumi ideyası", "— A guiding idea associated with Du Fu's legacy",
        ["Tan realist poeziyasının zirvəsi", "«Şeir tarixi» anlayışı", "Sosial və tarixi mövzular"],
        ["Peak of Tang realist poetry", "Poet-historian concept", "Social and historical themes"],
        [
            _w("Realist poeziya", "Realist poetry", "Müharibə və cəmiyyət mövzuları.", "Themes of war and society."),
            _w("«Spring View»", "Spring View", "Məşhur tarixi şeir.", "Famous historical poem."),
            _w("Poet-historian", "Poet-historian", "Tarixi hadisələrin poeziyada əks olunması.", "Reflection of historical events in poetry."),
        ],
        [
            _e("🍂", "Realist şair", "Realist poet", "Tan poeziyasının realist zirvəsi.", "Realist peak of Tang poetry."),
            _e("📜", "Şeir tarixi", "Poet-historian", "Tarixi hadisələri poeziyada əks etdirmişdir.", "Reflected historical events in poetry."),
        ],
        [
            _s("Encyclopaedia Britannica — Du Fu", "Encyclopaedia Britannica — Du Fu", "https://www.britannica.com/biography/Du-Fu"),
            _s("Britannica — Li Bai", "Britannica — Li Bai", "https://www.britannica.com/biography/Li-Bai"),
            _s("Britannica — Çin poeziyası", "Britannica — Chinese poetry", "https://www.britannica.com/art/Chinese-literature/Poetry"),
        ],
    ),
    # ── Arab ────────────────────────────────────────────────────────────────
    _fig(
        "ibn_battuta", "world", "🗺️", "1304 – 1369", "1304", "1369",
        "İbn Battuta", "Ibn Battuta", "Ərəb", "Arab",
        "Coğrafiya və səyyahlıq", "Geography and travel",
        "Şihab ad-Din Abu Abdullah İbn Battuta (1304–1369) "
        "Tangierdən (indiki Mərakeş) yola çıxmış, "
        "30 il ərzində Afrika, Orta Şərq, Hindistan, "
        "Cənubi-Şərqi Asiya və Çinə qədər səyahət etmişdir.",
        "Shihab al-Din Abu Abdullah Ibn Battuta (1304–1369) set out from "
        "Tangier and over 30 years traveled across Africa, the Middle East, "
        "India, Southeast Asia, and China.",
        "İbn Battuta «Rihla» səyahətnaməsini yazmış, "
        " XIV əsr dünyasının coğrafiyası, iqtisadiyyatı "
        "və mədəniyyəti barədə fundamental mənbə yaratmışdır.",
        "Ibn Battuta wrote the Rihla travelogue, creating a fundamental "
        "source on fourteenth-century world geography, economy, and culture.",
        "Onun səyahətləri orta əsr qlobal mübadilənin "
        "və coğrafi biliklərin inkişafına mühüm töhfə vermişdir.",
        "His travels made an important contribution to understanding "
        "medieval global exchange and geographic knowledge.",
        "Səyahət bilik genişləndirir.",
        "Travel expands knowledge.",
        "— İbn Battuta irsinin ümumi ideyası", "— A guiding idea associated with Ibn Battuta's legacy",
        ["«Rihla» səyahətnaməsi", "XIV əsr dünya coğrafiyası", "Qlobal mədəni mübadilə"],
        ["Rihla travelogue", "Fourteenth-century world geography", "Global cultural exchange"],
        [
            _w("Rihla", "Rihla", "30 illik səyahətlərin sənədləşdirilməsi.", "Documentation of 30 years of travel."),
            _w("Coğrafi qeydlər", "Geographic notes", "Afrika, Asiya və Orta Şərq barədə məlumat.", "Information on Africa, Asia, and the Middle East."),
            _w("Mədəni müşahidələr", "Cultural observations", "Xalqların adət-ənənələri barədə qeydlər.", "Notes on peoples' customs."),
        ],
        [
            _e("🗺️", "Səyyah", "Traveler", "Orta əsrin ən böyük səyyahlarından biri.", "One of the greatest travelers of the Middle Ages."),
            _e("📖", "Rihla", "Rihla", "Səyahət əsəri coğrafiya tarixinin klassikidir.", "Travel work is a classic of geographic history."),
        ],
        [
            _s("Encyclopaedia Britannica — Ibn Battuta", "Encyclopaedia Britannica — Ibn Battuta", "https://www.britannica.com/biography/Ibn-Battuta"),
            _s("Britannica — Səyahət tarixi", "Britannica — Travel literature", "https://www.britannica.com/art/travel-literature"),
            _s("UNESCO — İslam mədəni irsi", "UNESCO — Islamic cultural heritage", "https://ich.unesco.org/en/state/morocco-MA"),
        ],
    ),
    _fig(
        "al_idrisi", "world", "🗺️", "1100 – 1165", "1100", "1165",
        "Əl-İdrisi", "Al-Idrisi", "Ərəb", "Arab",
        "Coğrafiya və kartoqrafiya", "Geography and cartography",
        "Muhammad al-Idrisi (1100–1165) Siciliya (Palermo) "
        "sarayında çalışmış ərəb coğrafçı və kartoqrafdır. "
        "«Nuzhat al-mushtaq» əsəri orta əsr coğrafiyasının "
        "klassikidir.",
        "Muhammad al-Idrisi (1100–1165) was an Arab geographer and "
        "cartographer who worked at the Sicilian (Palermo) court. "
        "His Nuzhat al-mushtaq is a classic of medieval geography.",
        "Əl-İdrisi dünya xəritəsi (silver disk) hazırlamış, "
        "Avropa, Afrika və Asiyanın coğrafiyasını "
        "sistemli şəkildə təsvir etmişdir.",
        "Al-Idrisi prepared a world map (on a silver disk) and "
        "systematically described the geography of Europe, Africa, and Asia.",
        "Onun işləri Orta Əsr və İntibah dövrü "
        "Avropa coğrafiyasına təsir etmişdir.",
        "His work influenced medieval and Renaissance European geography.",
        "Coğrafiya dünyanı anlamaq deməkdir.",
        "Geography means understanding the world.",
        "— Əl-İdrisi irsinin ümumi ideyası", "— A guiding idea associated with al-Idrisi's legacy",
        ["Orta əsr dünya xəritəsi", "Sistemli coğrafi təsvir", "Kartoqrafiya elminin inkişafı"],
        ["Medieval world map", "Systematic geographic description", "Development of cartographic science"],
        [
            _w("Nuzhat al-mushtaq", "Nuzhat al-mushtaq", "Coğrafi traktat və xəritə.", "Geographic treatise and map."),
            _w("Dünya xəritəsi", "World map", "Gümüş disk üzərində xəritə.", "Map on a silver disk."),
            _w("Palermo məktəbi", "Palermo school", "Norman-Sicilian coğrafiya mərkəzi.", "Norman-Sicilian geographic center."),
        ],
        [
            _e("🗺️", "Kartoqraf", "Cartographer", "Orta əsrin ən böyük coğrafçılarından.", "Among the greatest geographers of the Middle Ages."),
            _e("🏛️", "Palermo", "Palermo", "Siciliya sarayında elmi iş aparmışdır.", "Conducted scholarly work at the Sicilian court."),
        ],
        [
            _s("Encyclopaedia Britannica — al-Idrisi", "Encyclopaedia Britannica — al-Idrisi", "https://www.britannica.com/biography/al-Idrisi"),
            _s("Britannica — İslam coğrafiyası", "Britannica — Islamic geography", "https://www.britannica.com/science/geography/Geography-in-the-early-Islamic-world"),
            _s("Britannica — Kartoqrafiya", "Britannica — Cartography", "https://www.britannica.com/science/cartography"),
        ],
    ),
    _fig(
        "ibn_arabi", "world", "📿", "1165 – 1240", "1165", "1240",
        "İbn Arabi", "Ibn Arabi", "Ərəb", "Arab",
        "Fəlsəfə və sufizm", "Philosophy and Sufism",
        "Muhyi ad-Din Ibn Arabi (1165–1240) Andalusiyadan "
        "olan böyük sufi mütəfəkkir və şairdir. "
        "«Vahdat al-vujud» (Varlığın birliyi) "
        "fəlsəfəsinin klassik müəllifidir.",
        "Muhyi al-Din Ibn Arabi (1165–1240) was a major Sufi thinker "
        "and poet from al-Andalus, classic author of the philosophy "
        "of wahdat al-wujud (unity of being).",
        "İbn Arabi «Futuhat al-Makkiyya» və «Fusus al-Hikam» "
        "əsərlərini yazmış, İslam mistik fəlsəfəsinin "
        "inkişafına fundamental töhfə vermişdir.",
        "Ibn Arabi wrote Futuhat al-Makkiyya and Fusus al-Hikam, "
        "making a fundamental contribution to Islamic mystical philosophy.",
        "Onun fikirləri Türkiyə, İran, Hindistan və "
        "dünya sufizm ənənəsinə geniş təsir göstərmişdir.",
        "His ideas widely influenced Turkish, Iranian, Indian, "
        "and world Sufi traditions.",
        "Varlıq birliyi həqiqətin özüdür.",
        "The unity of being is truth itself.",
        "— İbn Arabi irsinin ümumi ideyası", "— A guiding idea associated with Ibn Arabi's legacy",
        ["«Vahdat al-vujud» fəlsəfəsi", "Sufi mistik fəlsəfə", "İslam düşüncəsinin klassik fiquru"],
        ["Philosophy of wahdat al-wujud", "Sufi mystical philosophy", "Classic figure of Islamic thought"],
        [
            _w("Futuhat al-Makkiyya", "Futuhat al-Makkiyya", "Geniş sufizm traktatı.", "Extensive Sufi treatise."),
            _w("Fusus al-Hikam", "Fusus al-Hikam", "Hikmət və peyğəmbərlik haqqında əsər.", "Work on wisdom and prophethood."),
            _w("Vahdat al-vujud", "Wahdat al-wujud", "Varlığın birliyi fəlsəfəsi.", "Philosophy of the unity of being."),
        ],
        [
            _e("📿", "Sufi mütəfəkkir", "Sufi thinker", "İslam mistik fəlsəfəsinin klassik müəllifi.", "Classic author of Islamic mystical philosophy."),
            _e("📖", "Fusus", "Fusus", "Hikmət traktatı geniş təsir göstərmişdir.", "Treatise on wisdom had wide influence."),
        ],
        [
            _s("Stanford Encyclopedia — Ibn Arabi", "Stanford Encyclopedia — Ibn Arabi", "https://plato.stanford.edu/entries/ibn-arabi/"),
            _s("Encyclopaedia Britannica — Ibn Arabi", "Encyclopaedia Britannica — Ibn Arabi", "https://www.britannica.com/biography/Ibn-al-Arabi"),
            _s("Britannica — Sufizm", "Britannica — Sufism", "https://www.britannica.com/topic/Sufism"),
        ],
    ),
    _fig(
        "al_tabari", "world", "📜", "839 – 923", "839", "923",
        "Əl-Təbəri", "Al-Tabari", "Ərəb", "Arab",
        "Tarix", "History",
        "Muhammad ibn Jarir al-Tabari (839–923) Bağdad "
        "tarixçisi və mütəfəkkiridir. «Tarix ar-Rusul "
        "va-l-Muluk» (Peyğəmbərlər və padşahlar tarixi) "
        "əsəri İslam tarixi yazısının klassikidir.",
        "Muhammad ibn Jarir al-Tabari (839–923) was a historian "
        "and scholar of Baghdad. His History of the Prophets "
        "and Kings is a classic of Islamic historiography.",
        "Əl-Təbəri İslam tarixi, tafsir (Quran şərhi) "
        "və hüquq sahəsində geniş əsərlər yazmış, "
        "hadisə və sənəd analizi metodologiyasını inkişaf etdirmişdir.",
        "Al-Tabari wrote extensively on Islamic history, Quranic exegesis, "
        "and law, developing methodology for event and source analysis.",
        "Onun tarixi İslam dünyasının və sonrakı "
        "tarixçiliyin fundamental mənbəsidir.",
        "His history is a fundamental source for the Islamic world "
        "and later historiography.",
        "Tarixçi sənədləri diqqətlə yoxlamalıdır.",
        "The historian must carefully examine sources.",
        "— Əl-Təbəri irsinin ümumi ideyası", "— A guiding idea associated with al-Tabari's legacy",
        ["İslam tarixi yazısının klassik əsəri", "Tafsir (Quran şərhi)", "Tarix metodologiyası"],
        ["Classic work of Islamic historiography", "Quranic exegesis (tafsir)", "Historical methodology"],
        [
            _w("Tarix ar-Rusul va-l-Muluk", "History of the Prophets and Kings", "İslam tarixinin geniş kronikası.", "Broad chronicle of Islamic history."),
            _w("Tafsir", "Tafsir", "Quran şərhi.", "Quranic exegesis."),
            _w("Sənəd analizi", "Source analysis", "Tarix yazısında metodologiya.", "Methodology in historical writing."),
        ],
        [
            _e("📜", "Tarixçi", "Historian", "İslam tarixi yazısının klassik müəllifi.", "Classic author of Islamic historiography."),
            _e("📖", "Tafsir", "Tafsir", "Quran şərhi üzrə geniş traktat.", "Extensive treatise on Quranic exegesis."),
        ],
        [
            _s("Encyclopaedia Britannica — al-Tabari", "Encyclopaedia Britannica — al-Tabari", "https://www.britannica.com/biography/al-Tabari"),
            _s("Britannica — İslam tarixi", "Britannica — Islamic history", "https://www.britannica.com/topic/Islamic-world/History"),
            _s("Britannica — Tafsir", "Britannica — Tafsir", "https://www.britannica.com/topic/tafsir"),
        ],
    ),
    _fig(
        "al_masudi", "world", "🌍", "896 – 956", "896", "956",
        "Əl-Masudi", "Al-Masudi", "Ərəb", "Arab",
        "Tarix və coğrafiya", "History and geography",
        "Abu al-Hasan al-Masudi (896–956) ərəb tarixçi, "
        "coğrafçı və səyyahdır. «Muruj adh-dhahab» "
        "(Qızıl çaylar) əsəri dünya tarixi və coğrafiyasının "
        "klassik mənbəsidir.",
        "Abu al-Hasan al-Masudi (896–956) was an Arab historian, "
        "geographer, and traveler. His Muruj adh-dhahab "
        "(Meadows of Gold) is a classic source of world history and geography.",
        "Əl-Masudi Avropa, Afrika, Asiya və Hindistan "
        "barədə geniş məlumat toplamış, "
        "müxtəlif xalqların adət-ənənələrini sənədləşdirmişdir.",
        "Al-Masudi collected extensive information on Europe, Africa, "
        "Asia, and India, documenting customs of diverse peoples.",
        "O, orta əsr qlobal biliklərinin sintezinə "
        "fundamental töhfə vermişdir.",
        "He made a fundamental contribution to synthesizing "
        "medieval global knowledge.",
        "Bilik səyahət və müşahidə ilə genişlənir.",
        "Knowledge expands through travel and observation.",
        "— Əl-Masudi irsinin ümumi ideyası", "— A guiding idea associated with al-Masudi's legacy",
        ["«Muruj adh-dhahab» — dünya tarixi", "Coğrafi və etnoqrafik qeydlər", "Qlobal biliklərin sintezi"],
        ["Meadows of Gold — world history", "Geographic and ethnographic notes", "Synthesis of global knowledge"],
        [
            _w("Muruj adh-dhahab", "Meadows of Gold", "Dünya tarixi və coğrafiya traktatı.", "Treatise on world history and geography."),
            _w("Səyyah qeydləri", "Travel notes", "Geniş coğrafi müşahidələr.", "Broad geographic observations."),
            _w("Etnoqrafiya", "Ethnography", "Xalqların adət-ənənələri.", "Customs of peoples."),
        ],
        [
            _e("🌍", "Coğrafçı", "Geographer", "Orta əsr qlobal biliklərinin sintezi.", "Synthesis of medieval global knowledge."),
            _e("📖", "Muruj", "Meadows of Gold", "Dünya tarixinin klassik mənbəyi.", "Classic source of world history."),
        ],
        [
            _s("Encyclopaedia Britannica — al-Masudi", "Encyclopaedia Britannica — al-Masudi", "https://www.britannica.com/biography/al-Masudi"),
            _s("Britannica — İslam coğrafiyası", "Britannica — Islamic geography", "https://www.britannica.com/science/geography/Geography-in-the-early-Islamic-world"),
            _s("Britannica — Orta əsr tarixi", "Britannica — Medieval history", "https://www.britannica.com/event/Middle-Ages"),
        ],
    ),
    _fig(
        "al_khalil_ibn_ahmad", "world", "📖", "718 – 791", "718", "791",
        "Əl-Xəlil ibn Əhməd", "Al-Khalil ibn Ahmad", "Ərəb", "Arab",
        "Dilçilik", "Linguistics",
        "Al-Khalil ibn Ahmad (718–791) Basra dilçisi, "
        "«Kitab al-Ayn» — ərəb dilinin ilk "
        "ensiklopedik lüğətinin — müəllifidir. "
        "Ərəb prosodiyasının (aruz) banisi sayılır.",
        "Al-Khalil ibn Ahmad (718–791) was a Basran linguist, "
        "author of Kitab al-Ayn, the first encyclopedic "
        "dictionary of Arabic, and founder of Arabic prosody.",
        "Əl-Xəlil ərəb şeirliyinin ölçü sistemini (aruz) "
        "formalaşdırmış, qrammatika və fonetika "
        "elminin inkişafına töhfə vermişdir.",
        "Al-Khalil formulated the metrical system of Arabic poetry (arud), "
        "contributing to the development of grammar and phonetics.",
        "Onun işləri ərəb dil elminin və ədəbiyyat "
        "nəzəriyyəsinin fundamental bazisidir.",
        "His work is the fundamental basis of Arabic linguistics "
        "and literary theory.",
        "Dil elmi şeirin və hikmətin təməlidir.",
        "The science of language is the foundation of poetry and wisdom.",
        "— Əl-Xəlil ibn Əhməd irsinin ümumi ideyası", "— A guiding idea associated with al-Khalil's legacy",
        ["«Kitab al-Ayn» — ilk ərəb lüğəti", "Ərəb prosodiyasının (aruz) banisi", "Qrammatika elminin inkişafı"],
        ["Kitab al-Ayn — first Arabic dictionary", "Founder of Arabic prosody", "Development of grammatical science"],
        [
            _w("Kitab al-Ayn", "Kitab al-Ayn", "Ərəb dilinin ilk ensiklopedik lüğəti.", "First encyclopedic dictionary of Arabic."),
            _w("Aruz", "Arud (prosody)", "Ərəb şeir ölçü sisteminin formalaşdırılması.", "Formation of Arabic poetic meter system."),
            _w("Basra məktəbi", "Basra school", "Erkən ərəb dilçiliyi məktəbi.", "Early Arabic linguistics school."),
        ],
        [
            _e("📖", "Lüğət", "Dictionary", "Ərəb dilinin ilk ensiklopedik lüğətini yaratmışdır.", "Created the first encyclopedic Arabic dictionary."),
            _e("🎵", "Aruz", "Prosody", "Ərəb şeir ölçü sisteminin banisi.", "Founder of Arabic poetic meter system."),
        ],
        [
            _s("Encyclopaedia Britannica — al-Khalil ibn Ahmad", "Encyclopaedia Britannica — al-Khalil ibn Ahmad", "https://www.britannica.com/biography/al-Khalil-ibn-Ahmad"),
            _s("Britannica — Ərəb dili", "Britannica — Arabic language", "https://www.britannica.com/topic/Arabic-language"),
            _s("Britannica — Ərəb ədəbiyyatı", "Britannica — Arabic literature", "https://www.britannica.com/art/Arabic-literature"),
        ],
    ),
    _fig(
        "ibn_hazm", "world", "⚖️", "994 – 1064", "994", "1064",
        "İbn Hazm", "Ibn Hazm", "Ərəb", "Arab",
        "Hüquq və fəlsəfə", "Law and philosophy",
        "Abu Muhammad Ali ibn Hazm (994–1064) Andalusiyadan "
        "olan hüquqşünas, teoloq və filosofdur. "
        "«Al-Muhalla» hüquq traktatı və "
        "realist fəlsəfi yanaşması ilə tanınır.",
        "Abu Muhammad Ali ibn Hazm (994–1064) was a jurist, "
        "theologian, and philosopher from al-Andalus, known for "
        "the legal treatise Al-Muhalla and a realist philosophical approach.",
        "İbn Hazm hüquq, teologiya və məntiq sahəsində "
        "geniş əsərlər yazmış, Andalus mədəniyyətinin "
        "klassik mütəfəkkirlərindən biridir.",
        "Ibn Hazm wrote extensively on law, theology, and logic, "
        "and is among the classic thinkers of Andalusian culture.",
        "Onun hüquq və fəlsəfi işləri İslam hüquq "
        "elmində və Orta Əsr fəlsəfəsində "
        "mühüm yer tutur.",
        "His legal and philosophical work holds an important place "
        "in Islamic jurisprudence and medieval philosophy.",
        "Həqiqət hüquq və ağılla qorunur.",
        "Truth is protected by law and reason.",
        "— İbn Hazm irsinin ümumi ideyası", "— A guiding idea associated with Ibn Hazm's legacy",
        ["«Al-Muhalla» hüquq traktatı", "Andalus fəlsəfə və hüquq", "Realist teoloji yanaşma"],
        ["Al-Muhalla legal treatise", "Andalusian philosophy and law", "Realist theological approach"],
        [
            _w("Al-Muhalla", "Al-Muhalla", "Hüquq traktatı.", "Legal treatise."),
            _w("Andalus fəlsəfəsi", "Andalusian philosophy", "Realist fəlsəfi yanaşma.", "Realist philosophical approach."),
            _w("Hüquq elmi", "Jurisprudence", "İslam hüququnun tədqiqi.", "Study of Islamic law."),
        ],
        [
            _e("⚖️", "Hüquqşünas", "Jurist", "«Al-Muhalla» hüquq traktatının müəllifi.", "Author of the Al-Muhalla legal treatise."),
            _e("🏛️", "Andalus", "Al-Andalus", "Andalus mədəniyyətinin klassik mütəfəkkiri.", "Classic thinker of Andalusian culture."),
        ],
        [
            _s("Encyclopaedia Britannica — Ibn Hazm", "Encyclopaedia Britannica — Ibn Hazm", "https://www.britannica.com/biography/Ibn-Hazm"),
            _s("Britannica — Əndəlüs", "Britannica — Al-Andalus", "https://www.britannica.com/place/Spain/The-Visigothic-kingdom/Islamic-Spain"),
            _s("Britannica — İslam hüququ", "Britannica — Islamic law", "https://www.britannica.com/topic/sharia"),
        ],
    ),
    _fig(
        "naguib_mahfouz", "world", "✍️", "1911 – 2006", "1911", "2006",
        "Nəcib Məhfuz", "Naguib Mahfouz", "Ərəb", "Arab",
        "Ədəbiyyat", "Literature",
        "Nəcib Məhfuz (1911–2006) Misir yazıçısı, "
        "1988-ci ildə Ədəbiyyat üzrə Nobel mükafatının "
        "laureatıdır. Ərəb romanının modern "
        "inkişafının aparıcı fiqurudur.",
        "Naguib Mahfouz (1911–2006) was an Egyptian writer and "
        "1988 Nobel laureate in Literature, a leading figure "
        "in the modern development of the Arabic novel.",
        "Məhfuz «Cairo Trilogy» (Qahirə trilogiyası) "
        "və «Children of Gebelawi» kimi romanlar yazmış, "
        "Misir cəmiyyətinin sosial və mənəvi transformasiyasını "
        "realist üslubda təsvir etmişdir.",
        "Mahfouz wrote novels including the Cairo Trilogy and "
        "Children of Gebelawi, depicting the social and spiritual "
        "transformation of Egyptian society in a realist style.",
        "O, ərəb ədəbiyyatının dünya miqyasında "
        "tanınmasına fundamental töhfə vermişdir.",
        "He made a fundamental contribution to global recognition "
        "of Arabic literature.",
        "Ədəbiyyat cəmiyyətin güzgüsüdür.",
        "Literature is the mirror of society.",
        "— Nəcib Məhfuz irsinin ümumi ideyası", "— A guiding idea associated with Mahfouz's legacy",
        ["Ərəb romanının modern inkişafı", "Nobel mükafatı (1988)", "Misir cəmiyyətinin realist təsviri"],
        ["Modern development of the Arabic novel", "Nobel Prize (1988)", "Realist portrayal of Egyptian society"],
        [
            _w("Cairo Trilogy", "Cairo Trilogy", "Qahirə trilogiyası — klassik roman.", "Cairo Trilogy — classic novel."),
            _w("Children of Gebelawi", "Children of Gebelawi", "Simvolik-realist roman.", "Symbolic-realist novel."),
            _w("Realist roman", "Realist novel", "Misir cəmiyyətinin təsviri.", "Portrayal of Egyptian society."),
        ],
        [
            _e("🏆", "Nobel", "Nobel", "1988-ci ildə Ədəbiyyat üzrə Nobel mükafatı.", "1988 Nobel Prize in Literature."),
            _e("✍️", "Romançı", "Novelist", "Ərəb romanının modern inkişafının aparıcı fiquru.", "Leading figure in modern Arabic novel."),
        ],
        [
            _s("Encyclopaedia Britannica — Naguib Mahfouz", "Encyclopaedia Britannica — Naguib Mahfouz", "https://www.britannica.com/biography/Naguib-Mahfouz"),
            _s("Nobel Prize — Naguib Mahfouz", "Nobel Prize — Naguib Mahfouz", "https://www.nobelprize.org/prizes/literature/1988/mahfouz/biographical/"),
            _s("Britannica — Ərəb ədəbiyyatı", "Britannica — Arabic literature", "https://www.britannica.com/art/Arabic-literature"),
        ],
    ),
    _fig(
        "abbas_ibn_firnas", "world", "🪽", "810 – 887", "810", "887",
        "Abbas ibn Firnas", "Abbas ibn Firnas", "Ərəb", "Arab",
        "Elm və texnologiya", "Science and technology",
        "Abbas ibn Firnas (810–887) Andalusiyadan "
        "olan alim, mühəndis və sənətkardır. "
        "Uçuş cihazı ilə hava sınaqları aparmış, "
        "optika və saat mexanizmləri üzrə işləmişdir.",
        "Abbas ibn Firnas (810–887) was a scientist, engineer, "
        "and artist from al-Andalus who conducted flight "
        "experiments with a gliding device and worked on "
        "optics and clock mechanisms.",
        "İbn Firnas qanad formalı cihazla uçuş "
        "sınağı aparmış, optika və astronomiya "
        "sahəsində təcrübələr həyata keçirmişdir.",
        "Ibn Firnas conducted a flight test with a wing-shaped device "
        "and carried out experiments in optics and astronomy.",
        "O, erkən aviasiya və tətbiqi elmin "
        "tarixinə mühüm töhfə vermişdir.",
        "He made an important contribution to the history "
        "of early aviation and applied science.",
        "Elm təcrübə ilə irəliləyir.",
        "Science advances through experiment.",
        "— Abbas ibn Firnas irsinin ümumi ideyası", "— A guiding idea associated with Ibn Firnas's legacy",
        ["Erkən uçuş sınaqları", "Optika və astronomiya təcrübələri", "Andalus tətbiqi elmi"],
        ["Early flight experiments", "Optics and astronomy experiments", "Andalusian applied science"],
        [
            _w("Uçuş sınağı", "Flight experiment", "Qanad formalı cihazla uçuş.", "Flight with wing-shaped device."),
            _w("Optika", "Optics", "İşıq və linza təcrübələri.", "Light and lens experiments."),
            _w("Saat mexanizmləri", "Clock mechanisms", "Mexaniki saat texnologiyası.", "Mechanical clock technology."),
        ],
        [
            _e("🪽", "Uçuş", "Flight", "Erkən uçuş sınaqları ilə tanınır.", "Known for early flight experiments."),
            _e("🔬", "Alim", "Scientist", "Andalus tətbiqi elminin pioneri.", "Pioneer of Andalusian applied science."),
        ],
        [
            _s("Encyclopaedia Britannica — Abbas ibn Firnas", "Encyclopaedia Britannica — Abbas ibn Firnas", "https://www.britannica.com/biography/Abbas-ibn-Firnas"),
            _s("Britannica — Əndəlüs elmi", "Britannica — Science in al-Andalus", "https://www.britannica.com/place/Spain/The-Visigothic-kingdom/Islamic-Spain"),
            _s("Britannica — Aviasiya tarixi", "Britannica — Aviation history", "https://www.britannica.com/technology/history-of-flight"),
        ],
    ),
    _fig(
        "al_maari", "world", "✍️", "973 – 1057", "973", "1057",
        "Əl-Maarri", "Al-Ma'arri", "Ərəb", "Arab",
        "Ədəbiyyat və fəlsəfə", "Literature and philosophy",
        "Abu al-Ala al-Maarri (973–1057) Suriyadan "
        "olan şair, filosof və esseistdir. "
        "«Risalat al-Ghufran» və «Luzum ma la yalzam» "
        "əsərləri ərəb ədəbiyyatının klassikidir.",
        "Abu al-Ala al-Ma'arri (973–1057) was a Syrian poet, "
        "philosopher, and essayist. His Risalat al-Ghufran and "
        "Luzum ma la yalzam are classics of Arabic literature.",
        "Əl-Maarri humanist fikir, əxlaqi tənqid və "
        "poetik innovasiya ilə tanınır; "
        "vegan həyat tərzi və mənəvi müstəqillik "
        "ideyalarını irəli sürmüşdür.",
        "Al-Ma'arri is known for humanist thought, ethical critique, "
        "and poetic innovation; he advanced ideas of vegan living "
        "and spiritual independence.",
        "Onun yaradıcılığı ərəb humanist ədəbiyyatının "
        "və fəlsəfi poeziyanın zirvəsini təmsil edir.",
        "His work represents the peak of Arabic humanist literature "
        "and philosophical poetry.",
        "Ağıl azadlığı həqiqətin yoludur.",
        "Freedom of reason is the path to truth.",
        "— Əl-Maarri irsinin ümumi ideyası", "— A guiding idea associated with al-Ma'arri's legacy",
        ["Ərəb humanist ədəbiyyatı", "«Risalat al-Ghufran»", "Fəlsəfi və etik poeziya"],
        ["Arab humanist literature", "Risalat al-Ghufran", "Philosophical and ethical poetry"],
        [
            _w("Risalat al-Ghufran", "Risalat al-Ghufran", "Paradise journey allegorical poem.", "Allegorical poem of a paradise journey."),
            _w("Luzum ma la yalzam", "Luzum ma la yalzam", "Fəlsəfi poeziya toplusu.", "Collection of philosophical poetry."),
            _w("Humanist fikir", "Humanist thought", "Əxlaqi və fəlsəfi tənqid.", "Ethical and philosophical critique."),
        ],
        [
            _e("✍️", "Şair-filosof", "Poet-philosopher", "Ərəb humanist ədəbiyyatının klassik fiquru.", "Classic figure of Arab humanist literature."),
            _e("📖", "Risalat al-Ghufran", "Risalat al-Ghufran", "Allegorik poem ərəb ədəbiyyatının klassikidir.", "Allegorical poem is a classic of Arabic literature."),
        ],
        [
            _s("Encyclopaedia Britannica — al-Maarri", "Encyclopaedia Britannica — al-Ma'arri", "https://www.britannica.com/biography/al-Maarri"),
            _s("Britannica — Suriya ədəbiyyatı", "Britannica — Syrian literature", "https://www.britannica.com/place/Syria/Cultural-life"),
            _s("Britannica — Ərəb poeziyası", "Britannica — Arabic poetry", "https://www.britannica.com/art/Arabic-literature/Poetry"),
        ],
    ),
    _fig(
        "khalil_gibran", "world", "🕊️", "1883 – 1931", "1883", "1931",
        "Xəlil Gibran", "Khalil Gibran", "Ərəb", "Arab",
        "Ədəbiyyat və fəlsəfə", "Literature and philosophy",
        "Xəlil Gibran (1883–1931) Livan mənşəli "
        "şair, rəssam və esseistdir. «The Prophet» "
        "(Peyğəmbər) əsəri dünya ədəbiyyatının "
        "ən çox oxunan klassiklərindən biridir.",
        "Khalil Gibran (1883–1931) was a Lebanese poet, "
        "painter, and essayist. The Prophet is among "
        "the most widely read classics of world literature.",
        "Gibran «The Prophet», «The Broken Wings» "
        "və «Sand and Foam» kimi əsərlər yazmış, "
        "humanist, mistik və ictimai mövzuları "
        "birləşdirən poeziya və nəsr yaradılmışdır.",
        "Gibran wrote works including The Prophet, The Broken Wings, "
        "and Sand and Foam, creating poetry and prose combining "
        "humanist, mystical, and social themes.",
        "Onun yaradıcılığı ərəb-amerikan ədəbiyyatının "
        "və XX əsr humanist düşüncəsinin "
        "mühüm hissəsidir.",
        "His work is an important part of Arab-American literature "
        "and twentieth-century humanist thought.",
        "Sevgi həyatın ən böyük hikmətidir.",
        "Love is life's greatest wisdom.",
        "— Xəlil Gibran, «The Prophet»", "— Khalil Gibran, The Prophet",
        ["«The Prophet» — dünya klassik", "Ərəb-amerikan ədəbiyyatı", "Humanist və mistik poeziya"],
        ["The Prophet — world classic", "Arab-American literature", "Humanist and mystical poetry"],
        [
            _w("The Prophet", "The Prophet", "Fəlsəfi-mistik esse toplusu.", "Philosophical-mystical essay collection."),
            _w("The Broken Wings", "The Broken Wings", "Romantik-fəlsəfi roman.", "Romantic-philosophical novel."),
            _w("Rəssamlıq", "Painting", "Vizual incəsənət və illüstrasiya.", "Visual art and illustration."),
        ],
        [
            _e("📖", "The Prophet", "The Prophet", "Dünyanın ən çox tərcümə olunan əsərlərindən biri.", "One of the world's most translated works."),
            _e("🎨", "Şair-rəssam", "Poet-painter", "Söz və vizual incəsənəti birləşdirmişdir.", "Combined word and visual art."),
        ],
        [
            _s("Encyclopaedia Britannica — Khalil Gibran", "Encyclopaedia Britannica — Khalil Gibran", "https://www.britannica.com/biography/Khalil-Gibran"),
            _s("Britannica — Livan ədəbiyyatı", "Britannica — Lebanese literature", "https://www.britannica.com/place/Lebanon/Cultural-life"),
            _s("Britannica — Ərəb-amerikan ədəbiyyatı", "Britannica — Arab American literature", "https://www.britannica.com/art/Arabic-literature"),
        ],
    ),
]
