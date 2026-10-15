# Swedish Parliamentary Education Motions: NLP Pipeline

## Overview
Processing 13,957 Swedish parliamentary education motions (1986-2025) through an optimized NLP pipeline to extract thematic structure via Latent Dirichlet Allocation (LDA). Current approach: **44-topic title-weighted LDA with lemmatization**, testing stability improvements over baseline 32-topic model.

## Pipeline Architecture

```
Raw XML (data_xml/)
    ↓
07_extract_from_xml.py
    ↓
extracted_text_xml/ (13,957 raw motions)
    ↓
02_remove_stopwords.py (133 Swedish stop words)
    ↓
stopword_removed/ (intermediate)
    ↓
03_remove_boilerplate.py (66 parliamentary/structural patterns)
    ↓
boilerplate_removed/ (intermediate)
    ↓
04_normalize_and_deduplicate.py (normalize, detect 133 duplicates)
    ↓
normalized/ (cleaned, ready for LDA)
    ↓
05_fit_baseline_lda.py (32-topic LDA on normalized text)
    ↓
baseline_lda_32/ (FINAL MODEL)
    ↓
06_display_lda_topics.py
    ↓
results/ (32_TOPICS_FINAL.csv, top_30_topic_words.txt)
```

## Processing Steps

### 1. **Extraction** (07_extract_from_xml.py)
- **Input:** 181,194 XML files from Swedish parliament data portal
- **Filter:** UbU committee (Education Committee), case-insensitive
- **Extract:** dok_id, date, title, body text (Inledning → signature blocks)
- **Format conversion:** XML → JSON lines (one motion per line)
- **Output:** 13,957 motions in 4 temporal bins (1986-1993, 1994-2004, 2005-2014, 2015-2025)
- **Storage:** `data/input/extracted_text_xml/` (87 MB, persisted in git)
  - **Note:** Folder name means "text extracted FROM XML", not "XML files"
  - **Actual format:** JSON lines (each line is a complete JSON motion object)
  - **Rationale for JSON:** Easier to add fields, better for streaming processing, compatible with all downstream scripts

### 2. **Stopword Removal** (02_remove_stopwords.py)
- **Swedish stop words:** 114 from NLTK
- **Supplementary (19):** Auxiliary verbs (ska, skall, blir, varit, blivit), prepositions/connectors (kommer, enligt, genom, dock, fall, ge, ta, del, fler), generic words (olika, mer, behöver, vill, nya)
- **Total:** 133 stop words
- **Reason:** Remove high-frequency, low-information words

### 3. **Boilerplate Removal** (03_remove_boilerplate.py)
- **66 parliamentary/structural patterns** (updated from initial 129 after CSS removal)
- **Categories:**
  - OCR artifacts (inskann*, inscann*, skann*)
  - Parliamentary structure (ställer, bakom, föreslå*, anför*, regering*, riksdag*, proposition*)
  - Metadata markers (hemställ*, hänvisa*, beslut*, anledning*, antal*, sverige)
  - Abbreviations (ub, uhä, ex, prop, fl)
  - Currency/year (kronor, miljoner, kr, år)
  - Party names (centerparti*, socialdemokrat*, moderaterna, etc.)
  - Personal names (johan, eriksson)
- **Rationale:** Remove domain-specific metadata and structural language that doesn't represent education policy content

### 4. **Normalization & Deduplication** (04_normalize_and_deduplicate.py)
- **Normalization:** Lowercase, remove numbers/punctuation, collapse whitespace
- **Deduplication:** MD5 hash detection of exact duplicates after normalization
- **Result:** 13,957 motions, 133 duplicates detected (0.92%) and flagged but kept in dataset
- **Output:** `text_normalized` field ready for LDA fitting

### 5. **LDA Fitting - Current Approach: Title-Weighted (10_fit_title_weighted_lda.py)**
- **Algorithm:** scikit-learn LatentDirichletAllocation
- **Text preprocessing for weighting:**
  - Input text: `text_lemmatized` (lemmatized body text, despite historical quality concerns)
  - Title enhancement: `title_processed` (preprocessed titles appended 3x)
  - Weighted document: body + (title words × 3 additional copies)
  - Rationale: Emphasize motion intent (title) while preserving full textual context
- **Vectorization:**
  - max_features: 10,000 (vocabulary truncation to top 10k terms)
  - Rationale: Preserve domain-specific terminology while reducing dimensionality
  - Note: Removes rare words beyond top 10k frequency
  - Vocabulary shared with baseline (loaded from baseline_lda_44/baseline_vectorizer.pkl)
- **LDA Parameters:**
  - n_components: 44 topics (increased from baseline 32 for finer-grained thematic coverage)
  - max_iter: 50 iterations (sufficient for convergence on 13k+ documents)
  - learning_method: online (stochastic, requires adequate iterations)
  - n_jobs: 2
- **Convergence monitoring:** Reports actual iterations run (n_iter_) to verify convergence
- **Output:** 
  - title_weighted_lda_44_topics.pkl (2.7 MB model)
  - (Uses shared baseline vectorizer)
- **Diagnostic metric:** Training perplexity (diagnostic only, not evidence of generalization)

### 5a. **LDA Fitting - Baseline (07_fit_baseline_lda.py)**
- **Preserved for comparison:** 32-topic baseline model (non-lemmatized, no title weighting)
- **Used as vocabulary reference:** Baseline vectorizer ensures consistency across models
- **Output:** 
  - baseline_lda_32_topics.pkl (2.4 MB model)
  - baseline_vectorizer.pkl (152 KB)
- **Diagnostic metric:** Training perplexity 1770.22 (diagnostic only)

### 6. **Topic Display** (06_display_lda_topics.py)
- **Output:** Top 10 words per topic with weights
- **Format:** Neutral naming (Topic 1-32, no interpretive labels)
- **Rationale:** Allow manual inspection without prior bias

### 7. **Results Export**
- **32_TOPICS_FINAL.csv** - All 32 topics × top 10 words with weights
- **top_30_topic_words.txt** - Aggregate top 30 words across all topics
- **COHERENCE_TESTING_REPORT.txt** - Topic count optimization (29, 32, 36... 64 tested)

## Configuration Files

### `config/boilerplate_phrases.txt` (66 patterns)
Dynamically loaded by `03_remove_boilerplate.py`. Supports wildcard patterns:
- `regering*` matches regering, regeringen, regering's variants
- `hemställ*` matches hemställan, hemställs, hemställs, etc.
- Exact phrases like `moderata samlingspartiet` supported with word boundaries

### `preprocessing/02_remove_stopwords.py` (133 words)
Hard-coded supplementary words; NLTK supplies base 114.

## Key Decision Points

### Stop Words vs Boilerplate
- **Stop words:** General Swedish, universally applicable
- **Boilerplate:** Parliamentary/domain-specific structural language
- **Rationale:** Separation allows reuse of stop words for other Swedish texts

### Lemmatization: Tested, Revised Implementation (Current)
- **Initial testing:** spaCy sv_core_news_sm showed domain-mismatch problems (documented below)
- **Current approach:** Using `text_lemmatized` field in deduplicated data
  - Lemmatization applied as part of preprocessing pipeline despite initial quality concerns
  - Reasoning: Reduced inflectional noise may improve topic stability across seeds
- **Historical quality issues (initial testing):**
  - **"första" (first) → "en" (article)** — Model confused by parliamentary sentence structure
  - **"högre" (higher-ed) → "hög" (high)** — Lost comparative form (destroying key concept)
  - **"stora" (large) → "stor"** — Lost plurality information
  - **Root cause:** Model trained on news text; parliamentary language confuses POS/lemmatization
- **Decision rationale (revised):** Despite quality concerns, lemmatization is now used with:
  - Title weighting (3x) to prioritize motion intent over body text
  - Stability testing to validate whether the tradeoff improves topic consistency
  - 44 topics (vs. 32 baseline) to capture more granular thematic variation

### Topic Count: 44 (Current) vs. 32 (Baseline)
- **Baseline (32 topics):** Original selection via concentration analysis (6, 10, 14, 18, 22, 29, 32, 36, 43, 50, 57, 64 tested)
  - 32 ÷ 4 temporal bins = 8 topics/bin (clean division)
  - Reference: Gordon et al. used 60 topics (15/bin); our data preferred lower count
- **Current approach (44 topics):** Increased for title-weighted model
  - Rationale: With title weighting emphasizing motion intent, higher topic count captures finer-grained thematic variation
  - Stability testing will validate whether 44 improves consistency across seeds relative to 32
  - Preserves flexibility for future temporal binning (44 ÷ 4 = 11 topics/bin if needed)

## Data Quality Metrics

| Metric | Value | Note |
|--------|-------|------|
| Total motions | 13,957 | After extraction filter (UbU committee) |
| Temporal bins | 4 | 1986-1993, 1994-2004, 2005-2014, 2015-2025 |
| Duplicates detected | 133 (0.92%) | Flagged, kept in dataset |
| Vocabulary (truncated) | 10,000 unique tokens | CountVectorizer max_features=10000 |
| Stop words | 133 | 114 NLTK + 19 supplementary |
| Boilerplate patterns | 66 | Parliamentary + metadata |
| LDA topics (baseline) | 32 | Non-lemmatized, no title weighting |
| LDA topics (current) | 44 | Title-weighted (3x), lemmatized text |
| Title coverage | ~99.5% | Documents with processed titles for weighting |
| Training perplexity (current) | TBD | Diagnostic only; stability testing in progress |

## Implementation Beyond Proposal

The pipeline implementation exceeds the proposal requirements in several areas to enable robust temporal analysis and ensure data integrity:

### ✅ Normalized Word Probabilities
- **Proposal:** Top words per topic
- **Implementation:** All topic probabilities normalized (P(word|topic)) and displayed with 4-6 decimal precision
- **Benefit:** Enables quantitative comparisons across topics and time periods

### ✅ Complete Document-Topic Distribution
- **Proposal:** Topic mixture per document (θ_d)
- **Implementation:** All 32 topic probabilities per document (not just dominant + top 3)
- **Output:** `document_topic_distribution.csv` with doc_id, title, year + 32 probability columns
- **Benefit:** Enables downstream temporal prevalence calculations and topic trajectory analysis

### ✅ Document Metadata Preservation
- **Proposal:** Document grouping by temporal bins
- **Implementation:** Full traceability for each document (doc_id, title, year) carried through all preprocessing steps
- **Benefit:** Enables document-to-topic linkage for temporal analysis and qualitative validation

### ✅ Malformed JSON Tracking
- **Proposal:** Data quality monitoring (implied)
- **Implementation:** Explicit counting and reporting of malformed JSON lines across 4 preprocessing stages
- **Output:** Per-bin and total malformed-line warnings with ⚠️ flag
- **Benefit:** Ensures no silent data loss; full transparency in data pipeline

### ✅ Comprehensive Pipeline Documentation
- **Proposal:** Method description
- **Implementation:** End-to-end documentation (PIPELINE_DOCUMENTATION.md) covering all steps, decisions, and rationale
- **Includes:** Configuration details, data flow diagrams, decision points, and next steps

### ✅ Methodological Rigor
- **Proposal:** Topic evaluation on "baseline comparison, stability, and interpretability"
- **Implementation:** 
  - Explicit distinction between topic concentration testing (our method) vs. semantic coherence testing (not used)
  - Training perplexity labeled as diagnostic-only, not generalization evidence
  - Random seed fixed (reproducibility) but stability testing can be added before temporal binning

## Usage

```bash
# Full pipeline from normalized text to final topics
python modeling/05_fit_baseline_lda.py data/output/normalized models
python modeling/06_display_lda_topics.py models

# Output: results/32_TOPICS_FINAL.csv, results/top_30_topic_words.txt
```

**Note:** Lemmatization was tested (results archived in `logs/LEMMATIZATION_BENCHMARK.txt`) but rejected due to quality issues. Use non-lemmatized normalized text as pipeline input.

## Project Proposal TBD Resolution

**Status: COMPLETED**

Lemmatization (TBD in proposal) was systematically tested and rejected:
1. ✅ Reviewed Swedish lemmatization options (spaCy, Snowball, custom)
2. ✅ Selected spaCy sv_core_news_sm for testing (easiest, off-the-shelf)
3. ✅ Verified context-aware processing (full documents, not isolated words)
4. ✅ Ran comprehensive benchmarks (2 models, 6 metrics)
5. ✅ Discovered systematic quality issues (POS/lemmatization errors, vocabulary collapse)
6. ✅ Documented findings and rationale for rejection

**Argument for proposal:** "Lemmatization testing (TBD) revealed that spaCy sv_core_news_sm shows domain-mismatch problems when applied to parliamentary Swedish. While benchmark metrics improved (-23.85% perplexity, +12.50% coherence), this masked systematic quality degradation: critical terms disappeared from vocabulary, and domain-specific concepts were corrupted (e.g., 'högre utbildning'→'hög'). We concluded that reliable lemmatization would require a parliamentary-domain-specific model, so the baseline pipeline uses normalized (non-lemmatized) text instead."

## File Organization

```
project/
├── preprocessing/           # Data cleaning pipeline
│   ├── 02_remove_stopwords.py
│   ├── 03_remove_boilerplate.py
│   └── 04_normalize_and_deduplicate.py
├── modeling/               # LDA fitting & analysis
│   ├── 05_fit_baseline_lda.py
│   ├── 06_display_lda_topics.py
│   └── 08_extended_lda_testing.py
├── config/
│   └── boilerplate_phrases.txt (66 patterns)
├── data/
│   ├── input/extracted_text_xml/  (13,957 raw motions)
│   └── output/
│       ├── stopword_removed/
│       ├── boilerplate_removed/
│       └── normalized/
├── models/
│   ├── baseline_lda_32/             (32-topic baseline - non-lemmatized)
│   ├── baseline_lda_44/             (44-topic baseline - non-lemmatized, shared vectorizer)
│   └── title_weighted_lda_44/       (CURRENT MODEL - title-weighted 3x, lemmatized)
├── results/
│   ├── 32_TOPICS_FINAL.csv
│   ├── 44_TOPICS_FINAL.csv
│   ├── weighted_44_TOPICS_FINAL.csv (Current model topics)
│   ├── weighted_topics_wordclouds.html
│   └── SEED_STABILITY_3X_WEIGHTED_CORRECTED.md (Testing in progress)
└── logs/
    ├── COHERENCE_TESTING_REPORT.txt
    ├── LEMMATIZATION_BENCHMARK.txt
    └── PROJECT_LOG_XML_EXTRACTION.txt
```

## Current Phase: Title-Weighted Stability Testing (2026-10-14)

**Objective:** Validate whether title weighting (3x) + lemmatization improves topic stability in a 44-topic model.

**Hypothesis:** By emphasizing motion intent (titles) and reducing inflectional noise (lemmatization), the model should discover more consistent topics across random seeds.

**Testing approach:**
- Fit 44-topic title-weighted LDA with 5 different seeds (42, 123, 456, 789, 999)
- Compare topic matching using Hungarian algorithm (optimal matching)
- Metrics: Cosine similarity (full distributions) + Jaccard overlap (top 20 words)
- Comparison baseline: Baseline 32-topic and 44-topic non-weighted models

**Status:** Tests prepared in `analysis/13_seed_stability_3x_weighted.py`; awaiting execution.

---

## Baseline Stability Testing (Historical - 2026-10-13)

**Finding:** The 32-topic whole-corpus model is **highly unstable** across random seeds.

| Seed Pair | Mean Jaccard | Status |
|-----------|--------------|--------|
| 42 vs 123 | 0.020 | ❌ Unstable |
| 42 vs 456 | 0.010 | ❌ Unstable |
| 123 vs 456 | 0.033 | ❌ Unstable |
| **Overall** | **0.021** | **Below 0.60 threshold** |

**Interpretation:** Topics are completely reshuffled between seeds. Topic 1 in seed 42 covers government administration, in seed 123 covers teacher education, and in seed 456 covers healthcare — demonstrating that the model cannot reliably identify topic structure in this corpus.

**Why this happens:** 
- Heterogeneous corpus (39 years, author concentration in pre-1880)
- Domain-specific parliamentary vocabulary evolves over time
- LDA struggles to find consistent themes across such diversity

**This validates Gordon's approach:** Gordon found identical whole-corpus instability (Jaccard 0.26–0.31) and solved it with temporal binning, which constrains each period's vocabulary and author mix, enabling stable topic discovery.

**Detailed analysis:** See `results/STABILITY_ANALYSIS_REPORT.txt`

## Next Steps (Current Phase: Stability Validation)

1. **Run seed-stability test** on 44-topic title-weighted model
   - Compare to baseline 32-topic stability metrics
   - Assess whether title weighting (3x) and lemmatization improve consistency
2. **Evaluate results:**
   - If 44-topic weighted model shows improved stability → Use as primary model
   - If baseline 32 is more stable → Revert to baseline with optional title weighting
3. **Decision point:** Based on stability results, proceed to either:
   - **Temporal binning phase** (4 separate models, 8-11 topics each)
   - **Extended topic testing** (try additional topic counts with confirmed best approach)
4. **Topic alignment and trajectory analysis** (post-stability validation)
5. **Publication:** Document findings for thesis/paper
