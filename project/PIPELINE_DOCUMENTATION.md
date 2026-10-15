# Swedish Parliamentary Education Motions: NLP Pipeline

## Overview
Processing 13,957 Swedish parliamentary education motions (1986-2025) through an NLP pipeline to extract thematic structure via Latent Dirichlet Allocation (LDA). Current approach: **44-topic title-weighted LDA (titles appended 5×) on text with controlled lemmatization**, compared against a 44-topic baseline (body text only) on the same preprocessed text.

All paths below are relative to `project/`. Every script resolves its default paths from its own location, so scripts can be run from any working directory. Data (`data/`), models (`models/`) and the raw XML (`../data_xml/`) are not version controlled.

## Pipeline Architecture

```
../data_xml/ (raw riksdag XML, by year)
    ↓  extraction/01_extract_from_xml.py
data/input/extracted_text_xml/        field: text
    ↓  preprocessing/02_remove_boilerplate.py
data/output/boilerplate_removed/      field: text_no_boilerplate
    ↓  preprocessing/03_normalize_text.py
data/output/normalized/               field: text_normalized
    ↓  preprocessing/04_remove_stopwords.py
data/output/stopword_removed/         field: text_no_stopwords
    ↓  preprocessing/05_apply_lemmatization.py
data/output/lemmatized/               field: text_lemmatized
    ↓  preprocessing/06_detect_duplicates.py
data/output/deduplicated/             fields: is_duplicate, duplicate_of, text_hash
    ↓  preprocessing/09_preprocess_titles.py   (updates files in place)
data/output/deduplicated/             field: title_processed
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

Every data stage stores one JSONL file per temporal bin: `group1_1986-1993.jsonl`, `group2_1994-2004.jsonl`, `group3_2005-2014.jsonl`, `group4_2015-2025.jsonl`. Each stage adds a field and keeps all earlier fields, so metadata (`dok_id`, title, date, author names) is carried through to the models.

## Processing Steps

### 1. Extraction (`extraction/01_extract_from_xml.py`)
- **Input:** XML files from the Swedish parliament open data portal (`../data_xml/`, organized by year)
- **Method:** follows Bruinsma & Johansson (2024)
- **Filter:** UbU committee (Education Committee), case-insensitive
- **Extract:** dok_id, date, title, author names, body text (between the introduction and signature markers); HTML entities decoded
- **Output:** 13,957 motions as JSON lines in 4 temporal bins, in `data/input/extracted_text_xml/`
  - The folder name means "text extracted FROM XML"; the files are JSONL, not XML

### 2. Boilerplate Removal (`preprocessing/02_remove_boilerplate.py`)
- Runs first, on raw text with original structure (newlines, punctuation), so multi-word phrases can be matched
- **Phrases:** loaded from `config/boilerplate_phrases.txt` (432 entries, one explicit word or phrase per line, no wildcards), matched on word boundaries
- **Categories:** OCR/scanning artifacts, government and parliamentary institutions, parliamentary document/reference terms, procedural language, party names, etc.
- **Rationale:** remove domain-specific metadata and structural language that doesn't represent education policy content
- **Output field:** `text_no_boilerplate`

### 3. Normalization (`preprocessing/03_normalize_text.py`)
- Removes the document's own author names (from extracted metadata, whole-word, case-insensitive)
- Lowercase, remove numbers and punctuation, collapse whitespace
- Drops single-character words; preserves line breaks
- **Output field:** `text_normalized`

### 4. Stopword Removal (`preprocessing/04_remove_stopwords.py`)
- **Base list:** NLTK Swedish stop words
- **Supplementary (135, hard-coded):** parliamentary abbreviations (ub, dvs, osv, …), auxiliary verbs (ska, skall, blir, …), generic connectors, verbs and adjectives identified from LDA inspection (kommer, enligt, olika, göra, …), and two-letter and longer fragment artifacts (see `PREPROCESSING_ARTIFACTS.md` and `TWO_LETTER_WORDS.txt`)
- **Output field:** `text_no_stopwords`

### 5. Controlled Lemmatization (`preprocessing/05_apply_lemmatization.py`)
- Uses a manual lookup table, `config/controlled_lemmatization.csv` (351 `variant,lemma` pairs, e.g. `skolan → skola`), focused on education terminology
- Words not in the table are left unchanged
- Replaces the earlier spaCy approach, which was rejected (see "Lemmatization" below)
- **Output field:** `text_lemmatized`

### 6. Duplicate Detection (`preprocessing/06_detect_duplicates.py`)
- MD5 hash of the whitespace-normalized lemmatized text; one hash dictionary shared across all bins, so duplicates are detected across time periods
- Duplicates are **flagged, not removed**: `is_duplicate`, `duplicate_of` (dok_id of the original), `text_hash`
- Last recorded result: 133 duplicates (0.92%), measured on the earlier normalized-text pipeline; re-check after re-running
- Optional arguments: `[input_dir] [output_dir]`

### 7. Title Preprocessing (`preprocessing/09_preprocess_titles.py`)
- Runs boilerplate removal, normalization, stopword removal and lemmatization on titles, using the same config files as the body pipeline
- ⚠️ The stopword list is a separate hard-coded copy that differs from `04_remove_stopwords.py`: it adds ~34 spatial/directional words (uppåt, bakom, här, där, …) and lacks some later additions (e.g. 'fn', 'of', 'mr', 'är', 'trots', 'första', 'även')
- Writes `title_processed` back into the files in `data/output/deduplicated/`
- Title coverage ~99.5%

### 8a. Baseline LDA (`modeling/07_fit_baseline_lda.py`)
- **Input:** `text_lemmatized` (body only, no title weighting)
- **Vectorizer:** `CountVectorizer(max_df=0.5, min_df=5, max_features=10000)`, default token pattern
- **LDA:** scikit-learn `LatentDirichletAllocation`, 44 topics, `max_iter=50`, `learning_method='online'`, `random_state=42`, `n_jobs=2`
- **Output:** `models/baseline_lda_44/baseline_lda_44_topics.pkl`, `models/baseline_lda_44/baseline_vectorizer.pkl`, `results/document_topic_distribution.csv`
- The baseline vectorizer is reused by the weighted model and the stability tests, so they share one vocabulary
- **Diagnostic metric:** training perplexity (diagnostic only, not evidence of generalization)

### 8b. Title-Weighted LDA — current model (`modeling/10_fit_title_weighted_lda.py`)
- **Weighted document:** `text_lemmatized` + `title_processed` appended **5 additional times** (effective title weight up to 6× if title words also appear in the body). Documents without a title use body text only.
- **Vectorizer:** loads `models/baseline_lda_44/baseline_vectorizer.pkl` (run 8a first)
- **LDA:** same settings as the baseline (44 topics, seed 42)
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
| `test_topic_matching.py` | Unit tests for `topic_matching.py` (identical, permuted, synthetic models) | stdout |
| `11_validate_matching_quick.py` | Smoke test on 2,000 real documents + synthetic permutation test (8 topics) | stdout |
| `09_test_lda_stability.py` | Seed stability of the 44-topic baseline | `results/BASELINE_STABILITY_44TOPICS_CORRECTED.md` |
| `13_seed_stability_3x_weighted.py` | Seed stability with 3× title weighting | `results/SEED_STABILITY_3X_WEIGHTED_CORRECTED.md` |
| `13_seed_stability_5x_weighted.py` | Seed stability with 5× title weighting (matches the current model) | `results/SEED_STABILITY_5X_WEIGHTED_CORRECTED.md` |
| `compare_weighted_vs_baseline.py` | ⚠️ **Deprecated** — unvalidated coherence metric; use the stability tests instead | — |

## Configuration Files

### `config/boilerplate_phrases.txt`
432 explicit words/phrases, one per line, grouped by category with `#` comment headers. Loaded by `02_remove_boilerplate.py` and `09_preprocess_titles.py`. An alternative file can be passed as the 3rd argument to `02_remove_boilerplate.py`.

### `config/controlled_lemmatization.csv`
351 `variant,lemma` mappings. Loaded by `05_apply_lemmatization.py` and `09_preprocess_titles.py`.

### Stop words
Hard-coded in `preprocessing/04_remove_stopwords.py` (NLTK base + 135 supplementary).

## Key Decision Points

### Stop Words vs Boilerplate
- **Stop words:** general Swedish (plus fragment artifacts), applied after normalization
- **Boilerplate:** parliamentary/domain-specific structural language, applied to raw text
- **Rationale:** separation allows reuse of the stop word list for other Swedish texts

### Lemmatization: spaCy Rejected, Controlled Lemmatization Adopted
- **Initial testing:** spaCy `sv_core_news_sm` showed domain-mismatch problems on parliamentary Swedish (results archived in `logs/LEMMATIZATION_BENCHMARK.txt`):
  - **"första" (first) → "en" (article)** — model confused by parliamentary sentence structure
  - **"högre" (higher-ed) → "hög" (high)** — lost the comparative form, destroying a key concept
  - **"stora" (large) → "stor"** — lost plurality information
  - **Root cause:** model trained on news text; parliamentary language confuses POS tagging/lemmatization
  - Benchmark metrics improved (-23.85% perplexity, +12.50% coherence), but this masked systematic quality degradation
- **Current approach:** a manual lookup table (`config/controlled_lemmatization.csv`) that only merges known inflectional variants of education terms. This reduces inflectional noise without the spaCy errors, since unlisted words are untouched.
- **Argument for proposal:** "Lemmatization testing (TBD) revealed that spaCy sv_core_news_sm shows domain-mismatch problems when applied to parliamentary Swedish: critical terms disappeared from vocabulary, and domain-specific concepts were corrupted (e.g., 'högre utbildning'→'hög'). We therefore replaced automatic lemmatization with a controlled, manually curated lemmatization table restricted to education terminology."

### Title Weighting
- Titles state the motion's intent concisely; appending them several times shifts document-topic inference toward that intent while keeping the full body text
- The current model (`10_fit_title_weighted_lda.py`) and the shared-vocabulary variant use 5×; 3× is tested in `13_seed_stability_3x_weighted.py`

### Topic Count: 44 (Current) vs. 32 (Historical Baseline)
- **Historical baseline (32 topics):** original selection via topic concentration analysis (6, 10, 14, 18, 22, 29, 32, 36, 43, 50, 57, 64 tested; non-lemmatized text). 32 ÷ 4 temporal bins = 8 topics/bin. Gordon et al. used 60 topics (15/bin).
- **Current (44 topics):** both baseline and weighted models. Chosen to capture finer-grained thematic variation; 44 ÷ 4 = 11 topics/bin for later temporal binning.

## Data Quality Metrics

| Metric | Value | Note |
|--------|-------|------|
| Total motions | 13,957 | After extraction filter (UbU committee) |
| Temporal bins | 4 | 1986-1993, 1994-2004, 2005-2014, 2015-2025 |
| Duplicates detected | 133 (0.92%) | Earlier pipeline; flagged, kept in dataset |
| Vocabulary | 10,000 (baseline/weighted), 20,000 (shared-vocab variant) | `max_features` |
| Stop words | NLTK + 135 supplementary | |
| Boilerplate phrases | 432 | Explicit phrases, no wildcards |
| Lemmatization mappings | 351 | Controlled lookup table |
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

```bash
cd project

# Extraction and preprocessing (each step reads the previous step's output)
python extraction/01_extract_from_xml.py
python preprocessing/02_remove_boilerplate.py
python preprocessing/03_normalize_text.py
python preprocessing/04_remove_stopwords.py
python preprocessing/05_apply_lemmatization.py
python preprocessing/06_detect_duplicates.py
python preprocessing/09_preprocess_titles.py

# Baseline model (also creates the vectorizer the weighted model needs)
python modeling/07_fit_baseline_lda.py
python modeling/08_display_lda_topics.py

# Title-weighted model (run after 07)
python modeling/10_fit_title_weighted_lda.py
python modeling/11_display_weighted_lda_topics.py
python modeling/12_generate_weighted_wordclouds.py

# Stability tests
python analysis/test_topic_matching.py
python analysis/09_test_lda_stability.py
python analysis/13_seed_stability_5x_weighted.py
```

Preprocessing scripts 02–06 and `07_fit_baseline_lda.py` also accept `[input_dir] [output_dir]` arguments to override the defaults.

## File Organization

```
project/
├── extraction/
│   └── 01_extract_from_xml.py
├── preprocessing/
│   ├── 02_remove_boilerplate.py
│   ├── 03_normalize_text.py
│   ├── 04_remove_stopwords.py
│   ├── 05_apply_lemmatization.py
│   ├── 06_detect_duplicates.py
│   └── 09_preprocess_titles.py
├── modeling/
│   ├── 06_build_shared_vocabulary_and_fit_models.py
│   ├── 07_fit_baseline_lda.py
│   ├── 08_display_lda_topics.py
│   ├── 10_fit_title_weighted_lda.py
│   ├── 11_display_weighted_lda_topics.py
│   ├── 12_generate_weighted_wordclouds.py
│   └── 13_extract_topics_and_update_wordcloud.py
├── analysis/
│   ├── topic_matching.py
│   ├── test_topic_matching.py
│   ├── 09_test_lda_stability.py
│   ├── 11_validate_matching_quick.py
│   ├── 13_seed_stability_3x_weighted.py
│   ├── 13_seed_stability_5x_weighted.py
│   └── compare_weighted_vs_baseline.py   (deprecated)
├── config/
│   ├── boilerplate_phrases.txt
│   └── controlled_lemmatization.csv
├── results/
│   └── topics_wordclouds.html            (template for the word cloud scripts; other results are regenerated)
├── data/                                  (not in git)
│   ├── input/extracted_text_xml/
│   └── output/{boilerplate_removed,normalized,stopword_removed,lemmatized,deduplicated}/
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

**Objective:** validate whether title weighting + controlled lemmatization improves topic stability in a 44-topic model.

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
