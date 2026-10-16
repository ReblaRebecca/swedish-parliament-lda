# Swedish Parliamentary Education Motions: NLP Pipeline

## Overview
Processing 13,917 Swedish parliamentary education motions (1986-2025) through an NLP pipeline to extract thematic structure via Latent Dirichlet Allocation (LDA). Current approach: **44-topic LDA on the body text, lemmatized with Stanza**. Titles are processed and kept as a separate field for later use, but are not added to the model's documents: title weighting was tested and dropped (2026-10-16, see *Seed-Stability Results*).

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
    └── modeling/07_fit_baseline_lda.py        → models/baseline_lda_44/
            ├── modeling/08_display_lda_topics.py       → results/44_TOPICS_FINAL.csv
            ├── modeling/14_generate_topic_explorer.py  → results/topic_explorer.html
            └── analysis/09_test_lda_stability.py       → results/BASELINE_STABILITY_44TOPICS_CORRECTED.md
```

Every data stage stores one JSONL file per temporal bin: `group1_1986-1993.jsonl`, `group2_1994-2004.jsonl`, `group3_2005-2014.jsonl`, `group4_2015-2025.jsonl`. Each stage adds fields and keeps earlier ones, so metadata (`dok_id`, title, date, author names) is carried through to the models. All of `data/` is ignored by git.

**Why this order:** Stanza is the only slow step, so it runs once, right after extraction, and saves every word with its original form, lemma and part of speech. Everything after it works from that saved output and takes minutes, so the boilerplate list and stopwords can be changed and re-run without running Stanza again.

**Titles** go through exactly the same steps as the body text, in the same scripts (fields prefixed `title_`). The final title (`title_processed`) is kept in the data for later use; the model uses the body text only.

## Processing Steps

### 1. Extraction (`extraction/01_extract_from_xml.py`)
- **Input:** XML files from the Swedish parliament open data portal (default `../data_xml/`, organized by year). Pass another location as the first argument: `python extraction/01_extract_from_xml.py <xml_dir> [output_dir]`
- **Method:** follows Bruinsma & Johansson (2024)
- **Filter:** UbU committee (Education Committee), case-insensitive
- **Extract:** dok_id, date, title, author names, body text (between the introduction and signature markers); HTML entities decoded
- **HTML to text:** text pieces are joined without separators, with whitespace only at block-level tags (`<p>`, `<br>`, `<td>`, headings, …). The source HTML often splits single words across inline `<span>`s (`uppföljni</span><span>ng`, and in some motions every å/ä/ö is its own span), so joining with spaces fragmented words in ~4,400 motions (fixed 2026-10-15)
- **Character repair (body and title):** soft hyphens (U+00AD) removed; text NFC-normalized; spacing diacritics after a base letter replaced (`a°` → `å`, `a¨` → `ä`, `o¨` → `ö`)
- **Title heading removed:** the title appears as a heading near the start of the body in ~97% of motions. The first word-by-word match of the title within the first 400 characters is removed (13,532 motions), so the body holds the motion's own text and the title is kept only as its separate field. Later mentions of the title phrase (e.g. in the proposed decision) are kept as body text
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
- **Phrases:** loaded from `config/boilerplate_phrases.txt` (440 entries, one explicit word or phrase per line, no wildcards), matched case-insensitively against the **original word forms** saved by step 2, so the list keeps its surface forms (`riksdagen`, `med anledning av`). A word is removed only if a phrase match covers the whole word, apart from trailing punctuation (Stanza keeps the full stop in abbreviations, so the phrase `mot` removes `Mot.`); phrases never match across sentences
- **Categories:** OCR/scanning artifacts, government and parliamentary institutions, parliamentary document/reference terms, procedural language, party names, etc.
- **Output is lemmas** of the remaining words, one sentence per line
- **Dropped tokens:** auxiliary verbs (UPOS `AUX`), punctuation and symbols. Stanza lemmatizes the modal *ska/skall/skulle* to `skola`, which would merge with the noun *skola* (school); all auxiliaries are stopwords anyway
- **Dropped abbreviation lemmas:** words whose lemma contains an underscore. Stanza expands abbreviations into multi-word lemmas (`t.ex.` → `till_exempel`, `bl.a.` → `bland_annat`, `s.k.` → `så_kallad`, `dvs` → `det_vill_säga`, `m.fl.` → `med_flera`), sometimes garbled (`få_cetera`); the underscore would otherwise make each one a single token in the model. Every dropped word is counted in `data/output/boilerplate_removed/underscore_lemmas.json` (lemma → total count and word forms, most frequent first) for manual review of whether any are worth keeping
- **Lemma corrections:** known Stanza lemma errors are corrected from `config/lemma_corrections.txt` (`kompet` → `kompetens`, `lärosät` → `lärosäte`, `anslagen` → `anslag`, …). Stanza guesses lemmas for words it has not seen in training, and some guesses are truncated; the list corrects those errors found in the model review (`MODEL_REVIEW.md`), it does not replace the lemmatizer
- **Rationale:** remove domain-specific metadata and structural language that doesn't represent education policy content
- The per-word Stanza output is not copied further; it stays in `data/output/lemmatized/`
- **Output fields:** `text_no_boilerplate`, `title_no_boilerplate`

### 4. Normalization (`preprocessing/04_normalize_text.py`)
- Lowercase, remove numbers and punctuation, collapse whitespace
- Drops single-character words; preserves line breaks
- **Output fields:** `text_normalized`, `title_normalized`

### 5. Stopword Removal (`preprocessing/05_remove_stopwords.py`)
- **Base list:** NLTK Swedish stop words
- **Supplementary (hard-coded):** parliamentary abbreviations (ub, dvs, osv, …), auxiliary verbs (ska, skall, blir, …), generic connectors, verbs and adjectives identified from LDA inspection (kommer, enligt, olika, göra, …), and the **lemma forms** of inflected entries (behöva, vilja, kunna, ny, stor, olik, mången, …), since the text is lemmatized
- **Removed 2026-10-16:** the stopwords added to hide extraction fragments (`tt`, `rn`, `ngd`, …), no longer needed since the extraction fix, and the content abbreviations `fn`, `eg`, `ky`, `ib`, which are education-policy terms (see `MODEL_REVIEW.md`)
- **Output fields:** `text_no_stopwords` (final body text, used by the model) and `title_processed` (final title text, kept for later use)

### Duplicate count — for the report, not a pipeline step (`analysis/count_duplicates.py`)
- Not part of the pipeline: models use all motions, duplicates are not removed
- MD5 hash of the whitespace-normalized final text (`text_no_stopwords`); one hash dictionary shared across all bins, so duplicates are detected across time periods
- Prints duplicates per bin, the total and percentage, and each duplicate → original `dok_id`; writes no data
- The count depends on the final text, so re-run it after changing the boilerplate or stopword lists
- Last recorded result: 133 duplicates (0.92%), measured on the earlier normalized-text pipeline; re-check after re-running
- Optional argument: `[input_dir]` (default `data/output/stopword_removed`)

### 8. LDA Model (`modeling/07_fit_baseline_lda.py`)
- **Input:** `text_no_stopwords` (body text only; titles are not added). Motions with no body text left after preprocessing are skipped (4 motions)
- **Vectorizer:** `CountVectorizer(max_df=0.5, min_df=5, max_features=10000)`, default token pattern
- **LDA:** scikit-learn `LatentDirichletAllocation`, 44 topics, `max_iter=50`, `learning_method='online'`, `random_state=42`, `n_jobs=2`
- **Shared settings:** the topic count, LDA settings, stability seeds and the text-loading function live in one module, `modeling/lda_common.py`. The model (07), the stability test (09) and the topic explorer (14) import them from there, so the stability test always measures the same model that is reported
- **No convergence check:** with `learning_method='online'` and sklearn's default `evaluate_every=-1`, every fit runs exactly `max_iter=50` passes; the printed iteration count (always 50) confirms the setting, not convergence
- **Output:** `models/baseline_lda_44/baseline_lda_44_topics.pkl`, `models/baseline_lda_44/baseline_vectorizer.pkl`, `results/document_topic_distribution.csv`
- The vectorizer is reused by the stability test and the topic explorer, so they share one vocabulary. The script and model folder keep the name *baseline* from when a title-weighted model was compared against it
- **Diagnostic metric:** training perplexity (diagnostic only, not evidence of generalization)

### 9. Topic Display and Visualization
| Script | Reads | Writes |
|---|---|---|
| `modeling/08_display_lda_topics.py [model_dir]` | `models/baseline_lda_44/` | `results/44_TOPICS_FINAL.csv` (top 20 words/topic) |
| `modeling/14_generate_topic_explorer.py` | `models/baseline_lda_44/`, `data/output/stopword_removed/`, template `modeling/topic_explorer_template.html` | `results/topic_explorer.html`: word cloud per topic, share overall and per period, top 8 motions with year/party/id, party concentration among the top 5 motions. Reads the model directly. Replaces the earlier word cloud scripts (12, 13) and their template |

- Word weights are shown as normalized probabilities P(word | topic)
- Topics use neutral names (Topic 1–44, no interpretive labels) so they can be inspected without prior bias

## Analysis Scripts (`analysis/`)

| Script | Purpose | Output |
|---|---|---|
| `topic_matching.py` | Module: Hungarian-algorithm topic matching between two LDA models; cosine similarity (full distributions) + Jaccard (top words) | — |
| `11_validate_matching_quick.py` | Smoke test on 2,000 real documents + synthetic permutation test (8 topics) | stdout |
| `seed_stability.py` | Module: shared seed-stability procedure (fit one model per seed, match every pair, write the report) used by 09 | — |
| `09_test_lda_stability.py` | Seed stability of the 44-topic baseline | `results/BASELINE_STABILITY_44TOPICS_CORRECTED.md` |

**Seed-stability reports** list, per seed, the training perplexity and iteration count; then the **stability per topic** of the reference model (seed 42, the seed of the reported model); then cosine and Jaccard statistics for each of the 10 seed pairs; then pooled statistics over all 440 matched topic pairs.

**Stability per topic:** each topic of the seed-42 model is compared with its matched topic in each of the other 4 models. The table gives its top words, in how many of the 4 models it is *found* (matched cosine ≥ 0.70, a judgement call set in `seed_stability.FOUND_COSINE`), and its mean and minimum cosine and mean Jaccard. The same numbers are saved as CSV next to the report (`results/BASELINE_STABILITY_44TOPICS_PER_TOPIC.csv`). The seed-42 model is fitted on the same data with the same settings as the reported model, so its topic numbers are those of the reported model. Use this to decide which topics to interpret with confidence.

**Interpreting the pooled statistics:** the 440 matched topic pairs are not independent. Each seed's model appears in 4 of the 10 pairs, so the same topics are counted several times. The pooled mean is a fair summary, but the pooled standard deviation understates the real uncertainty. For the spread across runs, report the 10 per-pair means (or their range) rather than the pooled standard deviation.

## Configuration Files

### `config/boilerplate_phrases.txt`
440 explicit words/phrases, one per line, grouped by category with `#` comment headers. Loaded by `03_remove_boilerplate.py` and matched against original word forms (body and title). An alternative file can be passed as the 3rd argument to `03_remove_boilerplate.py`. After editing it, re-run steps 03–05 (no need to re-run Stanza).

### `config/lemma_corrections.txt`
Corrections for known Stanza lemma errors, one `wrong correct` pair per line with `#` comments. Applied in `03_remove_boilerplate.py` to body and title, case-insensitively. A wrong lemma marked with a leading `*` is also corrected at the end of a compound (`*kompet kompetens`: `gymnasiekompet` → `gymnasiekompetens`); mark an entry only after checking its compounds (`anslagen` must not be marked, because of *sammanslagen*). After editing it, re-run steps 03–05.

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

### Title Weighting: Not Used (decided 2026-10-16)
- **Tested:** appending the processed title 3× or 5× to the body text, on the idea that titles state the motion's intent concisely
- **Result:** a small stability gain only (mean matched cosine 0.539 for both weights vs. 0.525 without; per-pair ranges overlap); see *Seed-Stability Results*
- **Decision:** no title weighting. The gain does not justify an extra modelling choice that would have to be motivated and kept consistent across the whole-corpus and period models. The model uses body text only
- **Titles are kept:** extraction still separates the title and removes the title heading from the body; titles go through every preprocessing step and are saved as `title_processed`, so they are available if needed later (e.g. for labelling topics or as a separate analysis)
- The weighting code (scripts 06, 10, 11, the two 13 seed scripts and the weighting functions in `lda_common.py`) was removed on 2026-10-16 and remains in the git history

### Topic Count: 44 (Current) vs. 32 (Historical Baseline)
- **Historical baseline (32 topics):** original selection via topic concentration analysis (6, 10, 14, 18, 22, 29, 32, 36, 43, 50, 57, 64 tested; non-lemmatized text). 32 ÷ 4 temporal bins = 8 topics/bin. Gordon et al. used 60 topics (15/bin).
- **Current (44 topics):** Chosen to capture finer-grained thematic variation; 44 ÷ 4 = 11 topics/bin for later temporal binning.

## Data Quality Metrics

| Metric | Value | Note |
|--------|-------|------|
| Total motions | 13,917 | 13,957 UbU files; 40 without body text or outside 1986–2025 |
| Temporal bins | 4 | 1986-1993, 1994-2004, 2005-2014, 2015-2025 |
| Duplicates detected | 133 (0.92%) | Earlier pipeline; flagged, kept in dataset |
| Vocabulary | 10,000 | `max_features` |
| Stop words | NLTK (114) + 85 supplementary | |
| Boilerplate phrases | 440 | Explicit phrases, no wildcards |
| Lemmatizer | Stanza | Swedish Talbanken model; auxiliaries dropped |
| LDA topics | 44 | |
| Title weighting | None | Tested 3× and 5×, dropped 2026-10-16 |
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

# Model (also creates the vectorizer the stability test and topic explorer use)
python modeling/07_fit_baseline_lda.py
python modeling/08_display_lda_topics.py
python modeling/14_generate_topic_explorer.py   # word clouds

# Stability test (5 seeds; about 1 hour)
python analysis/09_test_lda_stability.py
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
  - **Text loading:** body text only (titles not added), motions without body text skipped, malformed lines counted
  - **No drift:** the model (07) and the stability test (09) use the very same functions from `lda_common.py`; no other script creates its own LDA model; fitted models carry the shared settings; the reported seed (42) is among the tested seeds
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
│   ├── 07_fit_baseline_lda.py
│   ├── 08_display_lda_topics.py
│   ├── 14_generate_topic_explorer.py
│   ├── topic_explorer_template.html
│   └── lda_common.py                     (shared LDA settings, text loading)
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
│   └── count_duplicates.py               (duplicate count for the report)
├── config/
│   ├── boilerplate_phrases.txt
│   └── lemma_corrections.txt              (corrections for known Stanza lemma errors)
├── results/                               (not in git; regenerated by the scripts)
├── data/                                  (not in git)
│   ├── input/extracted_text_xml/
│   └── output/{lemmatized,boilerplate_removed,normalized,stopword_removed}/
├── models/                                (not in git)
│   └── baseline_lda_44/
├── PIPELINE_DOCUMENTATION.md
├── PREPROCESSING_ARTIFACTS.md
├── MODEL_REVIEW.md                        (review of the first models on the Stanza pipeline)
└── PROGRESS_SEMINAR_1.md                  (status and open decisions, seminar 2026-10-19)
```

## Seed-Stability Results: Body Text vs. 3× and 5× Title Weighting (2026-10-16)

**Question:** does title weighting make the 44-topic whole-corpus model more stable across random seeds, and which weight should be used?

**Setup:** for each of the three variants, 44-topic LDA fitted with 5 seeds (42, 123, 456, 789, 999) on the same preprocessed text (Stanza pipeline after the model-review fixes, incl. the `kompetens` compound fix) and the same vocabulary (baseline vectorizer); topics matched between every pair of seeds with the Hungarian algorithm (10 pairs, 440 matched topic pairs per variant); cosine similarity over the full topic-word distributions, Jaccard over the top 20 words. A topic of the seed-42 model counts as *found* in another seed's model if its matched topic has cosine ≥ 0.70. Reports: `results/BASELINE_STABILITY_44TOPICS_CORRECTED.md` (body text; reproducible with `09_test_lda_stability.py`) and `results/SEED_STABILITY_{5X,3X}_WEIGHTED_CORRECTED.md` (produced by the 13 seed scripts, since removed; in git history), with per-topic CSVs alongside.

| | Body text only | Title ×5 | Title ×3 |
|---|---|---|---|
| Mean cosine, all matched pairs | 0.525 | 0.539 | 0.539 |
| Range of the 10 per-pair means | 0.486–0.566 | 0.506–0.573 | 0.521–0.554 |
| Mean Jaccard (top 20) | 0.24 | 0.24 | 0.23 |
| Seed-42 topics found in 4 of 4 other models | 5 | 7 | **10** |
| … in 3 of 4 | 7 | 7 | 3 |
| … in 2 of 4 | 7 | 6 | 6 |
| … in 1 of 4 | 6 | 6 | 4 |
| … in 0 of 4 | 19 | 18 | 21 |
| Training perplexity, seeds 42/123/456/789/999 | 2166/2161/2159/2153/2168 | 2115/2124/2084/2098/2105 | 2152/2139/2121/2134/2119 |

**Topics found in all four other models**
- Baseline (5): independent schools/municipality, preschool/childcare, research/higher education, grants/appropriations, technical higher education.
- Title ×5 (7): upper secondary school, children/parents, society/knowledge, gender equality (*kvinna, jämställdhet, flicka, pojke*), research, teacher education, compulsory school/preschool.
- Title ×3 (10): children with special needs, sport/physical activity, language/Swedish, upper secondary school/grades, distance education (Gävle, Kalmar), society/knowledge, independent schools/municipality, gender equality, research, teacher education.

**Interpretation**
1. **Stability is moderate for all three variants.** About 12–13 of 44 topics are found again reliably (3–4 of 4); about 18–21 depend on the seed. The unstable ones are mainly place-name topics (Gävle, Skövde, Växjö/Blekinge, Stockholm/Södertörn), residual topics of general words (*många, land, öka, problem*), and narrow mixed topics (driving licences + degree-awarding powers, LGBT + deviation reports).
2. **Title weighting helps a little.** Both weighted variants are about 0.014 above the baseline in mean cosine, and the per-pair ranges overlap with the baseline's, so the gain is small. The weighted variants do, however, give more topics that are found in every seed (7 and 10 vs. 5), and those are substantive education themes (gender equality, teacher education, language, sport) rather than budget or administrative topics.
3. **3× vs. 5×.** The two weights have the same mean cosine (0.539). 3× is the more even across seed pairs (range 0.521–0.554, vs. 0.506–0.573) and has the most topics found in all four other models (10, vs. 7 and 5), but these differences are small.
4. **Caveats.** All differences come from one set of 5 seeds; the *found* counts depend on the 0.70 threshold and are counted for the seed-42 model only; the pooled statistics are not independent (each seed appears in 4 of 10 pairs).
5. **Many seed-dependent topics** suggest that 44 topics split the corpus more finely than the data supports. This is relevant to the topic count of the period models (see *Plan* below) and to the progress seminar.

**Decision: no title weighting.** The gain (≈0.014 in mean cosine, overlapping ranges) is too small to justify an extra modelling choice. A first decision for 3× (the most even and with the most fully stable topics) was reversed the same day for this reason. All further models, whole-corpus and period models, use the body text only; titles are kept in the data for later use.

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

## Plan: Period Models and Cross-Period Comparison (not yet implemented)

Separate LDA models will be fitted for each of the four periods and their topics compared across periods with cosine similarity. Cosine similarity between two topic-word vectors is only meaningful if both vectors refer to **the same words in the same order** (supervisor's comment, 2026-10-16). The design below guarantees that.

**Already in place**
- `analysis/topic_matching.py` refuses to compute similarities unless both models have an identical vocabulary in identical column order (`np.array_equal`); different or reordered vocabularies raise a `ValueError`. This is tested in `tests/test_topic_matching.py` (vocabulary mismatch, reordered vocabulary), so a misaligned comparison cannot pass silently.
- The whole-corpus model and all seed-stability runs already share one vocabulary: the vectorizer saved by `07_fit_baseline_lda.py`.

**Design for the period models**
1. **One shared vocabulary for all four periods.** Fit a single `CountVectorizer` once on the full corpus (or reuse the baseline vectorizer), then transform each period's motions with it before fitting that period's LDA model. Every period model's `components_` then has the same columns, in the same order, and topics can be compared across periods directly.
2. **Same matching code.** Cross-period comparisons go through `match_and_evaluate` in `topic_matching.py`, which enforces the vocabulary check. With the same number of topics per period (about 11), the Hungarian matching gives a one-to-one alignment; matching with different topic counts is possible with `require_same_n_topics=False`.
3. **Shared settings.** The period models use the LDA settings and text loading from `modeling/lda_common.py`, like the whole-corpus model (body text only).
4. **Test.** A unit test that the four period models are fitted with an identical vocabulary (same words, same order).

**Consequences to keep in mind**
- **Words absent from a period** get near-zero weight in that period's topics (only the LDA prior). That is correct, but it means period-specific vocabulary also contributes to topics looking different across periods; this should be noted when interpreting similarities.
- **Vocabulary thresholds** (`min_df=5`, `max_df=0.5`, `max_features=10000`) are applied to the full corpus, not per period. A word frequent in one period but rare overall is still included; a word used in more than half of all motions is excluded everywhere.

## Next Steps

0. **Act on the first model review** (`MODEL_REVIEW.md`, 2026-10-16): the first models on the Stanza pipeline are fitted and reviewed; the review's vocabulary fixes (boilerplate gaps, abbreviation matching in step 03, artifact stopwords, Stanza lemma errors) are done; a few small leftovers remain (see the review)
1. ✅ **Seed-stability tests** for the 44-topic model on body text and with 3×/5× title weighting (2026-10-16; see *Seed-Stability Results*)
2. ✅ **Evaluate:** title weighting gives only a small stability gain; **no title weighting**, weighting code removed
3. **Decision point:** proceed to either
   - **Temporal binning** (4 separate models, ~11 topics each, one shared vocabulary; see *Plan: Period Models* above), or
   - **Extended topic-count testing** with the best approach
4. **Topic alignment and trajectory analysis**
5. **Publication:** document findings for thesis/paper
