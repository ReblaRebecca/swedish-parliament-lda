# Preprocessing Artifacts in Shared Vocabulary

**Total suspicious/fragment words in top-20 topics: 191**

These words passed the `min_df=5` threshold but appear to be tokenization artifacts, truncations, or noise from the preprocessing pipeline.

## Single-Letter Words (7 total)
Likely parsing errors or characters accidentally tokenized:
- `j`, `k`, `p`, `br`, `el`, `gr`, `sf`

## Obvious Truncations/Fragments (50+ words)

### Missing suffix fragments:
- `beh` → behov (need)
- `nda` → anda/andra/grundande
- `ggare` → skapare (creator)  
- `arbetsl` → arbetslös (unemployed)
- `nyanl` → nyanlända (newly arrived)
- `lder` → ålder (age)
- `ldre` → äldre (elderly)
- `llet` → älskat/fullt?
- `mne` → ämne (subject)

### Character sequence artifacts:
- `tt`, `tta`, `ttas`, `ttre` (probably word boundaries with "ett")
- `rs`, `rn`, `rns`, `rd`, `rda`, `ret`, `rer` (probably "r" + suffix)
- `ng`, `ngd`, `ngs` (probably "-ing" or "-ning" fragments)
- `gre` (truncated adjective?)

### Proper nouns/place names (shouldn't be separate entries):
- `ume` (Umeå)
- `lund` (Lund)
- `malm` (Malmö)
- `ping` (Jönköping)
- `borl` (Borås)
- `sk` (Skåne)
- `link` (Linköping)

## Legitimate Acronyms/Abbreviations (correctly included):
- `csn` (Centrala Studiestödsnämnden - Swedish student finance agency)
- `sfi` (Swedish for immigrants program)
- `hbt` (LGBT in Swedish)
- `eu` (European Union)
- `adhd` (neurodevelopmental disorder)

## Root Cause (identified 2026-10-15)

Most fragments were created by **extraction**, not tokenization. The source HTML often splits single words across inline `<span>` elements, and `01_extract_from_xml.py` joined every text piece with a space:

| Source HTML | Extracted text (before fix) |
|---|---|
| `uppföljni</span><span>ng` | `uppföljni ng` |
| `hö</span><span>gre` | `hö gre` |
| `ansva</span><span>­</span><span>ret` (soft hyphen) | `ansva ­ ret` |
| `f</span><span>ö</span><span>r` (every å/ä/ö its own span) | `f ö r` |

This affected 4,431 of 13,917 motions (mostly 2015–2025). The most frequent fragments were `ning`, `skol`, `arbets`, `ningen`, `utbild`, `ningar`, each in 150–280 documents.

Minor additional sources, also fixed at extraction:
- Soft hyphens (U+00AD) inside words: 2,693 motions
- Spacing diacritics (`ma°ste`, `sa¨tt`): ~10 motions
- Combining diacritics (non-NFC text): 9 motions

Not fixed (genuine source damage): 2 motions from 1997 (e.g. GL02Ub807) have å/ä/ö deleted entirely (`Ume universitet`, `Linkpings`).

**Fix:** extraction now joins text pieces without separators and inserts whitespace only at block-level tags, removes soft hyphens, and repairs diacritics. Re-run the pipeline from extraction.

## Not All Listed Tokens Are Artifacts

Several tokens in the lists above and in `TWO_LETTER_WORDS.txt` are real words or abbreviations: `k`/`p` (from `s.k.`, `p.g.a.`), `malm` (ore), `el` (electricity, El Sistema), `sa` (said), `te` (appear), `sj`, `nt`, `hb`, `oh`, `rs` (acronyms). After re-running extraction, the artifact stopwords in `05_remove_stopwords.py` (also used for titles) should be re-evaluated, since some remove real words.

## Recommendation

- Re-run the pipeline from `01_extract_from_xml.py` and rebuild the vocabulary
- Re-check the vocabulary for remaining fragments before keeping the artifact stopwords

## Impact on Analysis

- **Wordcloud display**: These words will appear in topic visualizations, reducing readability
- **Model quality**: Artifacts compete with meaningful words for probability mass
- **Interpretation**: Makes some topics harder to interpret semantically

The current analysis is still valid—the topics reflect actual document content—but the word lists are noisier than ideal.
