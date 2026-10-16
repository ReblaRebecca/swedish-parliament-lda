# Swedish Parliamentary Education Motions: NLP Pipeline

## Overview
Processing 13,917 Swedish parliamentary education motions (1986-2025) through an NLP pipeline to extract thematic structure via Latent Dirichlet Allocation (LDA). Current approach: **44-topic title-weighted LDA (titles appended 5×) on text lemmatized with Stanza**, compared against a 44-topic baseline (body text only) on the same preprocessed text.

All paths below are relative to `project/`. Every script resolves its default paths from its own location, so scripts can be run from any working directory. Data (`data/`), models (`models/`) and the raw XML (`../data_xml/`) are not version controlled.

## Pipeline Architecture

```
../data_xml/ (raw riksdag XML, by year)
    ↓  extraction/01_extract_from_xml.py        ┐ run once
data/input/extracted_text_xml/        fields: text, title_text           │ (minutes)
    ↓  preprocessing/02_lemmatize.py            │ run once
data/output/lemmatized/               fields: tokens, title_tokens       ┘ (Stanza, hours)
    ↓  preprocessing/03_remove_boilerplate.py   ┐
data/output/boilerplate_removed/      fields: text_no_boilerplate, title_no_boilerplate
    ↓  preprocessing/04_normalize_text.py       │ cheap, re-run freely
data/output/normalized/               fields: text_normalized, title_normalized
    ↓  preprocessing/05_remove_stopwords.py     ┘ (e.g. after editing the boilerplate or stopword lists)
data/output/stopword_removed/         fields: text_no_stopwords, title_processed   ← final text used by all models
    ↓
    ├── modeling/07_fit_baseline_lda.py        → models/baseline_lda_44/
    │       ↓ modeling/08_display_lda_topics.py → results/44_TOPICS_FINAL.csv
    │
    ├── modeling/10_fit_title_weighted_lda.py  → models/title_weighted_lda_44/
    │       ↓ modeling/11_display_weighted_lda_topics.py → results/weighted_44_TOPICS_FINAL.csv
    │       ↓ modeling/12_generate_weighted_wordclouds.py → results/weighted_topics_wordclouds.html
    │
    └── modeling/06_build_shared_vocabulary_and_fit_models.py  (alternative: shared 20k vocabulary)
            → models/baseline_lda_44_shared_vocab/, models/weighted_lda_44_shared_vocab/
            ↓ modeling/13_extract_topics_and_update_wordcloud.py
              → results/weighted_44_TOPICS_SHARED_VOCAB.csv, results/weighted_topics_wordclouds_shared_vocab.html
```

Every data stage stores one JSONL file per temporal bin: `group1_1986-1993.jsonl`, `group2_1994-2004.jsonl`, `group3_2005-2014.jsonl`, `group4_2015-2025.jsonl`. Each stage adds fields and keeps earlier ones, so metadata (`dok_id`, title, date, author names) is carried through to the models. All of `data/` is ignored by git.

**Why this order:** Stanza is the only slow step, so it runs once, right after extraction, and saves every word with its original form, lemma and part of speech. Everything after it works from that saved output and takes minutes, so the boilerplate list, stopwords and title weighting can be changed and re-run without running Stanza again.

**Titles** go through exactly the same steps as the body text, in the same scripts (fields prefixed `title_`).

## Processing Steps

### 1. Extraction (`extraction/01_extract_from_xml.py`)
- **Input:** XML files from the Swedish parliament open data portal (default `../data_xml/`, organized by year). Pass another location as the first argument: `python extraction/01_extract_from_xml.py <xml_dir> [output_dir]`
- **Method:** follows Bruinsma & Johansson (2024)
- **Filter:** UbU committee (Education Committee), case-insensitive
- **Extract:** dok_id, date, title, author names, body text (between the introduction and signature markers); HTML entities decoded
- **HTML to text:** text pieces are joined without separators, with whitespace only at block-level tags (`<p>`, `<br>`, `<td>`, headings, …). The source HTML often splits single words across inline `<span>`s (`uppföljni</span><span>ng`, and in some motions every å/ä/ö is its own span), so joining with spaces fragmented words in ~4,400 motions (fixed 2026-10-15)
- **Character repair (body and title):** soft hyphens (U+00AD) removed; text NFC-normalized; spacing diacritics after a base letter replaced (`a°` → `å`, `a¨` → `ä`, `o¨` → `ö`)
- **Title heading removed:** the title appears as a heading near the start of the body in ~97% of motions. The first word-by-word match of the title within the first 400 characters is removed (13,532 motions), so title weighting counts the title exactly 5×. Later mentions of the title phrase (e.g. in the proposed decision) are kept as body text
- **Metadata removed (body and title):** motion numbers (`1989/90:Ub742`, `GE02A1`) and the motion's own author names (from the XML author list, whole-word, case-insensitive). Done here, before Stanza, so numbers are not split into odd tokens and names are not lemmatized
- **Output:** 13,917 motions as JSON lines (13,957 UbU files; 40 have no body text or fall outside 1986–2025) in 4 temporal bins, in `data/input/extracted_text_xml/`. Fields: `text` (cleaned body), `title` (original title, for display), `title_text` (cleaned title, for processing)
  - The folder name means "text extracted FROM XML"; the files are JSONL, not XML

### 2. Tagging and Lemmatization (`preprocessing/02_lemmatize.py`) — run once
- **Tool:** [Stanza](https://stanfordnlp.github.io/stanza/) Swedish pipeline (`tokenize,pos,lemma`, default Talbanken model), stored in `SU/stanza_resources/` and downloaded there automatically if missing
- Runs on the extracted running text of body and title, so the tagger sees full sentences and can use context
- **Saves every word** as `[word, lemma, upos]`, grouped by sentence, in `tokens` (body) and `title_tokens` (title). Nothing is removed at this step
- **Resumable:** motions already in the output file are skipped, so an interrupted run continues where it stopped
- **Runtime:** CPU-heavy; expect hours for the full corpus

### 3. Boilerplate Removal (`preprocessing/03_remove_boilerplate.py`)
- **Phrases:** loaded from `config/boilerplate_phrases.txt` (432 entries, one explicit word or phrase per line, no wildcards), matched case-insensitively against the **original word forms** saved by step 2, so the list keeps its surface forms (`riksdagen`, `med anledning av`). A word is removed only if a phrase match covers the whole word; phrases never match across sentences
- **Categories:** OCR/scanning artifacts, government and parliamentary institutions, parliamentary document/reference terms, procedural language, party names, etc.
- **Output is lemmas** of the remaining words, one sentence per line
- **Dropped tokens:** auxiliary verbs (UPOS `AUX`), punctuation and symbols. Stanza lemmatizes the modal *ska/skall/skulle* to `skola`, which would merge with the noun *skola* (school); all auxiliaries are stopwords anyway
- **Dropped abbreviation lemmas:** words whose lemma contains an underscore. Stanza expands abbreviations into multi-word lemmas (`t.ex.` → `till_exempel`, `bl.a.` → `bland_annat`, `s.k.` → `så_kallad`, `dvs` → `det_vill_säga`, `m.fl.` → `med_flera`), sometimes garbled (`få_cetera`); the underscore would otherwise make each one a single token in the model. Every dropped word is counted in `data/output/boilerplate_removed/underscore_lemmas.json` (lemma → total count and word forms, most frequent first) for manual review of whether any are worth keeping
- **Rationale:** remove domain-specific metadata and structural language that doesn't represent education policy content
- The per-word Stanza output is not copied further; it stays in `data/output/lemmatized/`
- **Output fields:** `text_no_boilerplate`, `title_no_boilerplate`

### 4. Normalization (`preprocessing/04_normalize_text.py`)
- Lowercase, remove numbers and punctuation, collapse whitespace
- Drops single-character words; preserves line breaks
- **Output fields:** `text_normalized`, `title_normalized`

### 5. Stopword Removal (`preprocessing/05_remove_stopwords.py`)
- **Base list:** NLTK Swedish stop words
- **Supplementary (hard-coded):** parliamentary abbreviations (ub, dvs, osv, …), auxiliary verbs (ska, skall, blir, …), generic connectors, verbs and adjectives identified from LDA inspection (kommer, enligt, olika, göra, …), two-letter and longer fragment artifacts (see `PREPROCESSING_ARTIFACTS.md` and `TWO_LETTER_WORDS.txt`), and the **lemma forms** of inflected entries (behöva, vilja, kunna, ny, stor, olik, mången, …), since the text is lemmatized
- **Output fields:** `text_no_stopwords` and `title_processed` — the final body and title text used by all models

### Duplicate count — for the report, not a pipeline step (`analysis/count_duplicates.py`)
- Not part of the pipeline: models use all motions, duplicates are not removed
- MD5 hash of the whitespace-normalized final text (`text_no_stopwords`); one hash dictionary shared across all bins, so duplicates are detected across time periods
- Prints duplicates per bin, the total and percentage, and each duplicate → original `dok_id`; writes no data
- The count depends on the final text, so re-run it after changing the boilerplate or stopword lists
- Last recorded result: 133 duplicates (0.92%), measured on the earlier normalized-text pipeline; re-check after re-running
- Optional argument: `[input_dir]` (default `data/output/stopword_removed`)

### 8a. Baseline LDA (`modeling/07_fit_baseline_lda.py`)
- **Input:** `text_no_stopwords` (body only, no title weighting)
- **Vectorizer:** `CountVectorizer(max_df=0.5, min_df=5, max_features=10000)`, default token pattern
- **LDA:** scikit-learn `LatentDirichletAllocation`, 44 topics, `max_iter=50`, `learning_method='online'`, `random_state=42`, `n_jobs=2`
- **Shared settings:** the topic count, LDA settings, title weight, stability seeds and the text-loading and title-weighting functions live in one module, `modeling/lda_common.py`. Every model (07, 10, 06) and every stability test (09, 13) imports them from there, so the stability tests always measure the same model that is reported
- **No convergence check:** with `learning_method='online'` and sklearn's default `evaluate_every=-1`, every fit runs exactly `max_iter=50` passes; the printed iteration count (always 50) confirms the setting, not convergence
- **Output:** `models/baseline_lda_44/baseline_lda_44_topics.pkl`, `models/baseline_lda_44/baseline_vectorizer.pkl`, `results/document_topic_distribution.csv`
- The baseline vectorizer is reused by the weighted model and the stability tests, so they share one vocabulary
- **Diagnostic metric:** training perplexity (diagnostic only, not evidence of generalization)

### 8b. Title-Weighted LDA — current model (`modeling/10_fit_title_weighted_lda.py`)
- **Weighted document:** `text_no_stopwords` + `title_processed` appended **5 times**. The title heading is removed from the body at extraction, so the title counts exactly 5× (plus any genuine mentions of the title phrase in the body text). Documents without a title use body text only.
- **Vectorizer:** loads `models/baseline_lda_44/baseline_vectorizer.pkl` (run 8a first)
- **LDA:** same settings as the baseline (44 topics, seed 42), from `modeling/lda_common.py`
- **Output:** `models/title_weighted_lda_44/title_weighted_lda_44_topics.pkl`, `models/title_weighted_lda_44/title_weighting_stats.txt`, `results/document_topic_distribution.csv`
- ⚠️ Writes the same `results/document_topic_distribution.csv` as 8a and overwrites it. `12_generate_weighted_wordclouds.py` expects the weighted version, so run 10 after 07.

### 8c. Shared-Vocabulary Variant (`modeling/06_build_shared_vocabulary_and_fit_models.py`)
- Builds a separate 20,000-feature vocabulary from body + one title copy, then fits both a baseline (body only) and a weighted (body + 5× title) 44-topic model on it
- **Output:** `models/baseline_lda_44_shared_vocab/`, `models/weighted_lda_44_shared_vocab/` (model + `shared_vectorizer.pkl` each), `results/baseline_document_topic_distribution.csv`, `results/weighted_document_topic_distribution.csv`

### 9. Topic Display and Visualization
| Script | Reads | Writes |
|---|---|---|
| `modeling/08_display_lda_topics.py [model_dir]` | `models/baseline_lda_44/` | `results/44_TOPICS_FINAL.csv` (top 20 words/topic) |
| `modeling/11_display_weighted_lda_topics.py` | `models/title_weighted_lda_44/` + baseline vectorizer | `results/weighted_44_TOPICS_FINAL.csv` |
| `modeling/12_generate_weighted_wordclouds.py` | `weighted_44_TOPICS_FINAL.csv`, `document_topic_distribution.csv`, template `results/topics_wordclouds.html` | `results/weighted_topics_wordclouds.html`, `results/topic_statistics.csv` |
| `modeling/13_extract_topics_and_update_wordcloud.py` | `models/weighted_lda_44_shared_vocab/` | `results/weighted_44_TOPICS_SHARED_VOCAB.csv`, `results/weighted_topics_wordclouds_shared_vocab.html` |

- Word weights are shown as normalized probabilities P(word | topic)
- Topics use neutral names (Topic 1–44, no interpretive labels) so they can be inspected without prior bias

## Analysis Scripts (`analysis/`)

| Script | Purpose | Output |
|---|---|---|
| `topic_matching.py` | Module: Hungarian-algorithm topic matching between two LDA models; cosine similarity (full distributions) + Jaccard (top words) | — |
| `11_validate_matching_quick.py` | Smoke test on 2,000 real documents + synthetic permutation test (8 topics) | stdout |
| `seed_stability.py` | Module: shared seed-stability procedure (fit one model per seed, match every pair, write the report) used by 09 and both 13 scripts | — |
| `09_test_lda_stability.py` | Seed stability of the 44-topic baseline | `results/BASELINE_STABILITY_44TOPICS_CORRECTED.md` |
| `13_seed_stability_3x_weighted.py` | Seed stability with 3× title weighting | `results/SEED_STABILITY_3X_WEIGHTED_CORRECTED.md` |
| `13_seed_stability_5x_weighted.py` | Seed stability with 5× title weighting (matches the current model) | `results/SEED_STABILITY_5X_WEIGHTED_CORRECTED.md` |
| `compare_weighted_vs_baseline.py` | ⚠️ **Deprecated** — unvalidated coherence metric; use the stability tests instead | — |

**Seed-stability reports** list, per seed, the training perplexity and iteration count, then cosine and Jaccard statistics for each of the 10 seed pairs, then pooled statistics over all 440 matched topic pairs.

**Interpreting the pooled statistics:** the 440 matched topic pairs are not independent. Each seed's model appears in 4 of the 10 pairs, so the same topics are counted several times. The pooled mean is a fair summary, but the pooled standard deviation understates the real uncertainty. For the spread across runs, report the 10 per-pair means (or their range) rather than the pooled standard deviation.

## Configuration Files

### `config/boilerplate_phrases.txt`
432 explicit words/phrases, one per line, grouped by category with `#` comment headers. Loaded by `03_remove_boilerplate.py` and matched against original word forms (body and title). An alternative file can be passed as the 3rd argument to `03_remove_boilerplate.py`. After editing it, re-run steps 03–06 (no need to re-run Stanza).

### Stop words
Hard-coded in `preprocessing/05_remove_stopwords.py` (NLTK base + supplementary list, including lemma forms).

## Key Decision Points

### Stop Words vs Boilerplate
- **Stop words:** general Swedish (plus fragment artifacts), applied to lemmatized, normalized text
- **Boilerplate:** parliamentary/domain-specific structural language, applied to raw text
- **Rationale:** separation allows reuse of the stop word list for other Swedish texts

### Lemmatization: Stanza (since 2026-10-15)
History:
1. **spaCy `sv_core_news_sm` — rejected.** Domain-mismatch problems on parliamentary Swedish (results archived in `logs/LEMMATIZATION_BENCHMARK.txt`): `första → en`, `högre → hög`, `stora → stor`. Benchmark metrics improved (-23.85% perplexity, +12.50% coherence), but this masked quality degradation.
2. **Controlled lookup table — replaced.** A hand-made CSV of ~284 variant→lemma mappings for education terms. It only covered the words listed, and ran after stopword removal on a bag of words.
3. **Stanza — current.** A general, context-aware lemmatizer (Swedish Talbanken model) run once on full sentences right after extraction; every word is saved with its original form and lemma, so boilerplate removal still matches original word forms. The controlled table was dropped entirely (no domain overrides).

Known trade-offs of the current approach (seen when testing on example sentences):
- Comparatives are reduced to the positive form: *högre utbildning* → `hög utbildning`. This is correct lemmatization but merges *higher education* with *hög* in other senses.
- Rare compounds can get wrong lemmas, e.g. *arbetsvillkor* → `arbetsvillka`.
- Modal *ska/skall/skulle* gets lemma `skola`, colliding with the noun *skola*; handled by dropping all auxiliaries (UPOS `AUX`) in the boilerplate step.
- The earlier proposal argument ("replaced automatic lemmatization with a controlled table") no longer describes the pipeline.

### Title Weighting
- Titles state the motion's intent concisely; appending them several times shifts document-topic inference toward that intent while keeping the full body text
- The current model (`10_fit_title_weighted_lda.py`) and the shared-vocabulary variant use 5×; 3× is tested in `13_seed_stability_3x_weighted.py`
- The title heading is removed from the body at extraction, so the weight is exactly 5× (or 3×) rather than one extra from the heading

### Topic Count: 44 (Current) vs. 32 (Historical Baseline)
- **Historical baseline (32 topics):** original selection via topic concentration analysis (6, 10, 14, 18, 22, 29, 32, 36, 43, 50, 57, 64 tested; non-lemmatized text). 32 ÷ 4 temporal bins = 8 topics/bin. Gordon et al. used 60 topics (15/bin).
- **Current (44 topics):** both baseline and weighted models. Chosen to capture finer-grained thematic variation; 44 ÷ 4 = 11 topics/bin for later temporal binning.

## Data Quality Metrics

| Metric | Value | Note |
|--------|-------|------|
| Total motions | 13,917 | 13,957 UbU files; 40 without body text or outside 1986–2025 |
| Temporal bins | 4 | 1986-1993, 1994-2004, 2005-2014, 2015-2025 |
| Duplicates detected | 133 (0.92%) | Earlier pipeline; flagged, kept in dataset |
| Vocabulary | 10,000 (baseline/weighted), 20,000 (shared-vocab variant) | `max_features` |
| Stop words | NLTK + 135 supplementary | |
| Boilerplate phrases | 432 | Explicit phrases, no wildcards |
| Lemmatizer | Stanza | Swedish Talbanken model; auxiliaries dropped |
| LDA topics | 44 | Baseline and title-weighted |
| Title weighting | 5× | Current model |
| Title coverage | ~99.5% | Documents with processed titles |

## Implementation Beyond Proposal

### ✅ Normalized Word Probabilities
- **Proposal:** top words per topic
- **Implementation:** topic-word weights normalized to P(word|topic) and displayed with 4–6 decimal precision
- **Benefit:** enables quantitative comparisons across topics and time periods

### ✅ Complete Document-Topic Distribution
- **Proposal:** topic mixture per document (θ_d)
- **Implementation:** all 44 topic probabilities per document (not just dominant + top 3)
- **Output:** `document_topic_distribution.csv` with doc_id, title, year + 44 probability columns
- **Benefit:** enables temporal prevalence calculations and topic trajectory analysis

### ✅ Document Metadata Preservation
- Full traceability for each document (doc_id, title, year) through all preprocessing steps, enabling document-to-topic linkage for temporal analysis and qualitative validation

### ✅ Malformed JSON Tracking
- Every stage counts and reports malformed JSON lines per bin, so there is no silent data loss

### ✅ Methodological Rigor
- Topic matching across seeds via the Hungarian algorithm (topic indices are arbitrary between runs)
- Explicit distinction between topic concentration testing (our method) and semantic coherence testing (not used)
- Training perplexity labeled as diagnostic only, not evidence of generalization

## Usage

Setup (once, from the repo root; Python 3.9):

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
source venv/bin/activate   # in each new terminal before running scripts
```

NLTK stopwords are read from (and downloaded to) `SU/nltk_data/`, next to the repo. Stanza's Swedish model (~190 MB) is read from (and downloaded to on first run) `SU/stanza_resources/`.

```bash
cd project

# Run once: extraction and Stanza (each step reads the previous step's output)
python extraction/01_extract_from_xml.py ../../swedish-parliament-data   # or omit to use ../data_xml/
python preprocessing/02_lemmatize.py          # slow (hours); resumable if interrupted

# Cheap: re-run these after changing the boilerplate list or stopwords
python preprocessing/03_remove_boilerplate.py
python preprocessing/04_normalize_text.py
python preprocessing/05_remove_stopwords.py

# For the report: duplicate count on the final text (not needed by the models)
python analysis/count_duplicates.py

# Baseline model (also creates the vectorizer the weighted model needs)
python modeling/07_fit_baseline_lda.py
python modeling/08_display_lda_topics.py

# Title-weighted model (run after 07)
python modeling/10_fit_title_weighted_lda.py
python modeling/11_display_weighted_lda_topics.py
python modeling/12_generate_weighted_wordclouds.py

# Stability tests
python analysis/09_test_lda_stability.py
python analysis/13_seed_stability_5x_weighted.py
```

`01_extract_from_xml.py` accepts `[xml_dir] [output_dir]`; preprocessing scripts 02–05 and `07_fit_baseline_lda.py` accept `[input_dir] [output_dir]` arguments to override the defaults.

## Tests

```bash
cd project

# Unit tests: preprocessing, topic matching and the seed-stability code
# (about 10 seconds; synthetic examples only, no corpus, Stanza model or fitted models needed)
python -m unittest discover -s tests -v

# Sanity checks on the pipeline output after running 01-05 (about a minute; read-only)
python analysis/check_pipeline_output.py
```

- **`tests/test_preprocessing.py`** — HTML parsing (words split across spans are joined), character repair, title heading removal, motion number and author name removal, period boundaries, boilerplate matching on word forms (and AUX `ska` dropped while the noun `skola` is kept), normalization, and the stopword list (lemma forms included, content words such as `skola`, `lärare`, `utbildning` excluded)
- **`tests/test_topic_matching.py`** — Hungarian matching on synthetic topic matrices: identical models match with cosine 1, a known permutation is recovered, mismatched or reordered vocabularies and mismatched topic counts are rejected, summary statistics equal the per-topic values
- **`tests/test_seed_stability.py`** — the seed-stability tests and the shared LDA code:
  - **Title weighting:** title words appear exactly 5 extra times (3 in the 3× test), empty titles give body only, loaders skip empty documents and count malformed lines
  - **No drift:** the models (07, 10, 06) and stability tests (09, 13) use the very same functions from `lda_common.py`; no other script creates its own LDA model or title weighting; fitted models carry the shared settings; each 13 script loads with its own weight; the reported seed (42) is among the tested seeds
  - **Seeds:** the same seed reproduces the model exactly, a different seed changes it
  - **Planted topics:** on a synthetic corpus with three clearly separated topics, the full procedure (fit three seeds, match, measure) finds cosine > 0.99 for every matched topic, so it can detect stability when it is there
  - **Report:** 10 pairs and 440 matched topic pairs for 5 seeds × 44 topics; per-pair and pooled statistics equal those computed directly; per-seed table and the notes on convergence and pooled statistics are present
- **`analysis/check_pipeline_output.py`** — for each stage that has been run: all four period files present, no malformed lines, required fields present, no `dok_id` written twice, the same motions as extraction. Plus stage-specific checks: no soft hyphens or broken diacritics after extraction; Stanza output well-formed and every text tagged; final text lowercase letters only with no digits, punctuation, single-character words or stopwords left. Warns about empty texts or titles and frequent known extraction fragments. `FAIL` means the output is wrong; exit code 1 if any check fails. Optional argument: `[data_dir]`

## File Organization

```
project/
├── extraction/
│   └── 01_extract_from_xml.py
├── preprocessing/
│   ├── 02_lemmatize.py
│   ├── 03_remove_boilerplate.py
│   ├── 04_normalize_text.py
│   └── 05_remove_stopwords.py
├── modeling/
│   ├── 06_build_shared_vocabulary_and_fit_models.py
│   ├── 07_fit_baseline_lda.py
│   ├── 08_display_lda_topics.py
│   ├── 10_fit_title_weighted_lda.py
│   ├── 11_display_weighted_lda_topics.py
│   ├── 12_generate_weighted_wordclouds.py
│   ├── 13_extract_topics_and_update_wordcloud.py
│   └── lda_common.py                     (shared LDA settings, title weighting, text loading)
├── tests/
│   ├── test_preprocessing.py             (unit tests for steps 01, 03, 04, 05)
│   ├── test_topic_matching.py            (unit tests for analysis/topic_matching.py)
│   └── test_seed_stability.py            (seed-stability tests and shared LDA code)
├── analysis/
│   ├── check_pipeline_output.py          (sanity checks on pipeline output)
│   ├── topic_matching.py
│   ├── seed_stability.py                 (shared seed-stability procedure and report)
│   ├── 09_test_lda_stability.py
│   ├── 11_validate_matching_quick.py
│   ├── 13_seed_stability_3x_weighted.py
│   ├── 13_seed_stability_5x_weighted.py
│   ├── count_duplicates.py               (duplicate count for the report)
│   └── compare_weighted_vs_baseline.py   (deprecated)
├── config/
│   └── boilerplate_phrases.txt
├── results/
│   └── topics_wordclouds.html            (template for the word cloud scripts; other results are regenerated)
├── data/                                  (not in git)
│   ├── input/extracted_text_xml/
│   └── output/{lemmatized,boilerplate_removed,normalized,stopword_removed}/
├── models/                                (not in git)
│   ├── baseline_lda_44/
│   ├── title_weighted_lda_44/
│   ├── baseline_lda_44_shared_vocab/
│   └── weighted_lda_44_shared_vocab/
├── PIPELINE_DOCUMENTATION.md
├── PREPROCESSING_ARTIFACTS.md
└── TWO_LETTER_WORDS.txt
```

## Current Phase: Title-Weighted Stability Testing (2026-10-14)

**Objective:** validate whether title weighting improves topic stability in a 44-topic model.

**Hypothesis:** by emphasizing motion intent (titles) and reducing inflectional noise, the model should discover more consistent topics across random seeds.

**Testing approach:**
- Fit 44-topic title-weighted LDA with 5 seeds (42, 123, 456, 789, 999), at 3× and 5× weighting
- Match topics with the Hungarian algorithm (optimal one-to-one matching)
- Metrics: cosine similarity (full distributions) + Jaccard overlap (top 20 words)
- Comparison: 44-topic baseline (`09_test_lda_stability.py`)

**Status:** tests prepared in `analysis/13_seed_stability_{3x,5x}_weighted.py`; awaiting execution.

---

## Baseline Stability Testing (Historical - 2026-10-13)

**Finding:** the 32-topic whole-corpus model (non-lemmatized) was **highly unstable** across random seeds. Note: this test appears to predate the "corrected" Hungarian-matching scripts; index-by-index comparison understates stability, so re-run with `09_test_lda_stability.py` before relying on these numbers.

| Seed Pair | Mean Jaccard | Status |
|-----------|--------------|--------|
| 42 vs 123 | 0.020 | ❌ Unstable |
| 42 vs 456 | 0.010 | ❌ Unstable |
| 123 vs 456 | 0.033 | ❌ Unstable |
| **Overall** | **0.021** | **Below 0.60 threshold** |

**Interpretation:** topics were reshuffled between seeds. Topic 1 in seed 42 covered government administration, in seed 123 teacher education, and in seed 456 healthcare.

**Possible causes:**
- Heterogeneous corpus spanning 39 years
- Domain-specific parliamentary vocabulary evolves over time
- LDA struggles to find consistent themes across such diversity

**Relation to Gordon's approach:** Gordon found similar whole-corpus instability (Jaccard 0.26–0.31) and addressed it with temporal binning, which constrains each period's vocabulary and author mix.

## Next Steps

1. **Run seed-stability tests** for the 44-topic baseline and the 3×/5× title-weighted models
2. **Evaluate:** if title weighting improves stability → use the weighted model as primary; otherwise keep the baseline
3. **Decision point:** proceed to either
   - **Temporal binning** (4 separate models, ~11 topics each), or
   - **Extended topic-count testing** with the best approach
4. **Topic alignment and trajectory analysis**
5. **Publication:** document findings for thesis/paper
