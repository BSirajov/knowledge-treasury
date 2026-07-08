"""English display names for prominent figure profiles."""
from __future__ import annotations

NAMES: dict[str, str] = {
    "shoqan_walikhanov": "Shoqan Walikhanov",
    "kurmanjan_datka": "Kurmanjan Datka",
    "toktogul_satylganov": "Toktogul Satylganov",
    "togolok_moldo": "Togolok Moldo",
    "al_buxari": "Al-Bukhari",
    "dovletmammet_azadi": "Döwletmämmet Azadi",
    "mollanepes": "Mollanepes",
    "berdi_kerbabayev": "Berdi Kerbabayev",
    "kemine": "Kemine",
    "andalib": "Andalib",
    "ibrahim_muteferrika": "Ibrahim Muteferrika",
    "fatih_sultan_mehmed": "Mehmed II (Fatih Sultan Mehmed)",
    "ahmet_hasim": "Ahmet Haşim",
    "confucius": "Confucius",
    "li_shizhen": "Li Shizhen",
    "zhang_zhongjing": "Zhang Zhongjing",
    "tu_youyou": "Tu Youyou",
    "hua_luogeng": "Hua Luogeng",
    "bi_sheng": "Bi Sheng",
    "sun_zi": "Sun Tzu",
    "ibn_khaldun": "Ibn Khaldun",
    "al_jahiz": "Al-Jahiz",
    "ibn_rushd": "Ibn Rushd (Averroes)",
    "al_ghazali": "Al-Ghazali",
    "al_mutanabbi": "Al-Mutanabbi",
    "taha_hussein": "Taha Hussein",
    # Batch 2 — Kazakh
    "ablai_khan": "Ablai Khan",
    "akhmet_baitursynov": "Akhmet Baitursynov",
    "kurmangazy_sagyrbayuly": "Kurmangazy Sagyrbayuly",
    "ybyrai_altynsarin": "Ybyrai Altynsarin",
    # Kyrgyz
    "sagymbai_orozbakov": "Sagymbai Orozbakov",
    # Uzbek
    "jamshid_al_kashi": "Jamshid al-Kashi",
    "ahmad_al_farghani": "Ahmad al-Farghani",
    "kamoliddin_bekhzod": "Kamoliddin Bekhzod",
    "abd_al_rahman_jami": "Abd al-Rahman Jami",
    "ahmad_donish": "Ahmad Donish",
    # Turkmen
    "abu_al_ghazi_bahadur": "Abu al-Ghazi Bahadur",
    "seyitnazar_seydi": "Seyitnazar Seydi",
    # Ottoman
    "suleiman_the_magnificent": "Suleiman the Magnificent",
    "hayreddin_barbarossa": "Hayreddin Barbarossa",
    "ahmed_cevdet_pasha": "Ahmed Cevdet Pasha",
    "halide_edib_adivar": "Halide Edib Adivar",
    "sokollu_mehmed_pasha": "Sokollu Mehmed Pasha",
    # Chinese
    "laozi": "Laozi",
    "sima_qian": "Sima Qian",
    "cai_lun": "Cai Lun",
    "guo_shoujing": "Guo Shoujing",
    "zheng_he": "Zheng He",
    "wang_yangming": "Wang Yangming",
    "lu_xun": "Lu Xun",
    "li_bai": "Li Bai",
    "du_fu": "Du Fu",
    # Arab
    "ibn_battuta": "Ibn Battuta",
    "al_idrisi": "Al-Idrisi",
    "ibn_arabi": "Ibn Arabi",
    "al_tabari": "Al-Tabari",
    "al_masudi": "Al-Masudi",
    "al_khalil_ibn_ahmad": "Al-Khalil ibn Ahmad",
    "ibn_hazm": "Ibn Hazm",
    "naguib_mahfouz": "Naguib Mahfouz",
    "abbas_ibn_firnas": "Abbas ibn Firnas",
    "al_maari": "Al-Ma'arri",
    "khalil_gibran": "Khalil Gibran",
    # Batch 3 — India
    "panini": "Panini",
    "kautilya": "Kautilya (Chanakya)",
    "ashoka": "Ashoka",
    "srinivasa_ramanujan": "Srinivasa Ramanujan",
    "cv_raman": "C. V. Raman",
    "rabindranath_tagore": "Rabindranath Tagore",
    "mahatma_gandhi": "Mahatma Gandhi",
    "jagadish_chandra_bose": "Jagadish Chandra Bose",
    "satyendra_nath_bose": "Satyendra Nath Bose",
    "apj_abdul_kalam": "A. P. J. Abdul Kalam",
    # Japan
    "murasaki_shikibu": "Murasaki Shikibu",
    "matsuo_basho": "Matsuo Basho",
    "prince_shotoku": "Prince Shotoku",
    "kukai": "Kukai",
    "katsushika_hokusai": "Katsushika Hokusai",
    "fukuzawa_yukichi": "Fukuzawa Yukichi",
    "hideyo_noguchi": "Hideyo Noguchi",
    "hideki_yukawa": "Hideki Yukawa",
    # Korea
    "king_sejong": "King Sejong the Great",
    "yi_sun_sin": "Yi Sun-sin",
    "jeong_yak_yong": "Jeong Yak-yong",
    # Southeast Asia and other Oriental
    "raden_adjeng_kartini": "Raden Adjeng Kartini",
    "nguyen_trai": "Nguyen Trai",
    "jayavarman_vii": "Jayavarman VII",
    "ramkhamhaeng": "Ramkhamhaeng",
    "genghis_khan": "Genghis Khan",
    "ferdowsi": "Ferdowsi",
    "omar_khayyam": "Omar Khayyam",
}


def english_name(slug: str, az_name: str) -> str:
    return NAMES.get(slug, az_name)


def apply_english_names(text: str, slug: str) -> str:
    return text
