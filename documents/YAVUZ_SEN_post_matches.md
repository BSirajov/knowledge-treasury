# Yavuz Şen LinkedIn posts — cross-match against the 245-story collection

## Method

- His public LinkedIn activity (`linkedin.com/in/yavuzşen` → *recent-activity/all*) was scrolled while authenticated and **676 posts** were harvested into `documents/_yavuz_posts.json` (each with its activity id, exact date derived from the Snowflake id, and text).
- The **245 collection stories** (titles + full Azerbaijani body from `documents/_stories_segmented.json`, cross-checked against `documents/HEKAYƏ_MƏNBƏLƏRİ_(origins).md`) were compared against all 676 posts.
- Matching used a cross-lingual (Azerbaijani↔Turkish) normalization + distinctive-token (IDF-weighted) overlap to build a shortlist, followed by **manual reading of each candidate**. A pair is flagged only when it is unmistakably the **same underlying story/parable/anecdote** — not merely a shared theme or moral.

## Corpus coverage & caveat

- **Date range actually covered:** **2023-06-06 → 2026-01-17.**
- This is roughly **676 of his ~2,105 total posts (~32%)** and **does NOT reach 2015.** LinkedIn hides / lazy-limits older activity behind login and infinite-scroll, so the earliest ~8 years of his posting are not in this sample.
- Therefore **absence of a match here is not proof of absence.** Any story could still appear in an older post outside this window.

## Summary

| Metric | Value |
|---|---|
| Posts compared | 676 |
| Collection stories compared | 245 |
| **Confirmed** same-story matches | **7** |
| **Likely** (probable but not verbatim) matches | 0 |

All 7 confirmed matches are **near sentence-by-sentence Azerbaijani translations** of his Turkish posts — i.e. the exact same story text, not just the same idea. All 7 of his matching posts date from **June–November 2023**.

## Confirmed matches

| Collection story (AZ title) | His LinkedIn post excerpt (Turkish) | Post date | Confidence | Note |
|---|---|---|---|---|
| **Frankfurt hakiminin ədalətli hökmü** | "ADALET… Olay 1506'da Frankfurt'ta kaydedilmiştir. Bir tüccar 800 lonca kaybeder. Yoldan geçen bir marangoz da… çantasını bulur…" | 2023-06-19 | confirmed | Identical anecdote: Frankfurt 1506, lost purse of 800, devout carpenter, greedy merchant, judge's verdict. |
| **Quzuların dərisi** | "AL SANA EKONOMİK ÇÖZÜM… Şam valisi Esat paşa sıfırı tüketir ve hazine boşalır… dokumacılara fazladan vergi…" | 2023-07-19 | confirmed | Same Esad Pasha of Damascus tale ("shear the rams, don't skin the lambs"); same dialogue with advisers. |
| **Sədəf çiçəyi** | "Mahkeme salonunda, seksen yaşlarındaki yaşlı çiftin durumu içler acısıydı… Hakim… 'neden boşanmak istiyorsun?'" | 2023-08-05 | confirmed | Same 80-year-old-couple divorce-court story with the mother-of-pearl flower; matching sentences. |
| **Evlilikdə pozan** | "BABANIN MUHTEŞEM NASİHATİ… Beyaz Kâğıt, Kalem ve Silgi getirmesini istedi…" | 2023-08-14 | confirmed | Identical "paper, pencil & eraser" marriage-advice parable, line for line. |
| **Erkən evlilik** | "İŞTE DESTAN BÖYLE BAŞLADI… öğretmenler odasında sınav kâğıtlarını okuyordum… kız öğrencilerin yanlış cevaplarını silip…" | 2023-09-04 | confirmed | Same teacher-erasing-girls'-exam-answers-to-delay-child-marriage story; matching opening & logic. |
| **Mercedes** | "MERCEDES… Mercedes, kurucusunun soyadı ya da büyük bir motor şirketinin adı değildi. Otomobil tutkunu bir babanın kızının adıydı…" | 2023-09-09 | confirmed | Same "Mercedes named after a daughter" piece, incl. 1902 / 1929 / age-39 cancer details. |
| **Övlad tərbiyəsi** | "Bir kadın vardı. Çocuğuna hiç laf geçiremiyordu… ayı oynatıcısı gördü…" | 2023-11-21 | confirmed | Same unruly-child / bear-trainer parenting parable; near-verbatim opening. |

## Closest "same genre but NOT the same story" pairs (illustrative)

The collection and his feed clearly draw from the **same pool of Turkish *hikmetli hikâye*** (wisdom stories), so there are many thematic neighbours that are *not* the same text:

- His African "Her sabah bir ceylan / aslan uyanır Afrika'da…" gazelle-and-lion motivational piece (2023-06-22) vs. collection **"Ovçunun vəsfi"** (the African proverb *"until the lion learns to write, every tale will glorify the hunter"*) — same savanna/lion imagery, different pieces.
- His bread-and-poor-child posts (e.g. the döner-shop boy warming his feet) vs. collection **"İsti çörək"** (old man buying hot bread for his grandchild) — same tender-bread motif, different stories.
- His "Akşam eğlencesi" reverse-psychology parable (retiree pays noisy kids, then stops) — a classic that circulates widely but does **not** appear in the collection.
- His philosopher's-paradox execution anecdote ("Beni asarak öldüreceksiniz") — again a well-known parable, not present in the collection.

## Conclusion

Yavuz Şen's LinkedIn feed is built from exactly the same anonymous, widely-circulating Turkish wisdom-story tradition that the collection was adapted from, and **7 of the 245 stories appear, essentially verbatim, in his posts.** However:

1. Every matching post is a **reshared Turkish viral piece**, not original content he authored — the same texts appear on countless Turkish blogs, Facebook pages and forums (consistent with the origins report).
2. All 7 matches fall in **mid-2023**, i.e. within the harvested window and **long after** the collection would have been compiled; nothing here predates the collection.
3. The sample reaches only back to **June 2023**, so his 2015-era posts (his suspected earlier activity) were **not** accessible.

**Verdict:** The evidence shows Yavuz Şen is a **fellow curator/re-sharer of the same Turkish story pool**, not a demonstrable original source or transmission channel for this specific Azerbaijani collection. The overlap is real but shallow (7/245) and fully explained by both parties drawing from common circulating material rather than one deriving from the other.
