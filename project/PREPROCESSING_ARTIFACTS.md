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

## Root Cause

These artifacts appear because:

1. **Tokenization errors** during preprocessing created word fragments
2. **min_df=5 threshold** allows any word appearing ≥5 times in the corpus
3. Many fragments occur frequently enough (appearing in different contexts or documents) to meet this threshold
4. No post-processing to remove obvious artifacts

## Recommendation

To clean this up in future iterations:
- Review tokenization in preprocessing (check for encoding/character boundary issues)
- Post-filter vocabulary to exclude short fragments (words <3 chars except known abbreviations)
- Or increase min_df threshold (e.g., min_df=10) to filter out rare/artifact terms
- Explicitly exclude known artifact patterns

## Impact on Analysis

- **Wordcloud display**: These words will appear in topic visualizations, reducing readability
- **Model quality**: Artifacts compete with meaningful words for probability mass
- **Interpretation**: Makes some topics harder to interpret semantically

The current analysis is still valid—the topics reflect actual document content—but the word lists are noisier than ideal.
