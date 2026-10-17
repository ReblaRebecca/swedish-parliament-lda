# Swedish Parliamentary Education Motions: NLP Pipeline

## Overview
Processing 13,917 Swedish parliamentary education motions (1986-2025) through an NLP pipeline to extract thematic structure via Latent Dirichlet Allocation (LDA). Current approach: **LDA on the body text, lemmatized with Stanza: 8 topics per period model and 32 (= 4 × 8) for the whole-corpus model** (decided 2026-10-17, see *Period Models*, *Topic count per period*; the 44-topic results below are from before that decision). Titles are processed and kept as a separate field for later use, but are not added to the model's documents: title weighting was tested and dropped (2026-10-16, see *Seed-Stability Results*).

All paths below are relative to `project/`. Documentation and reports are in `docs/` (in git), the HTML visualizations in `visualizations/` (in git), and generated tables (CSV) in `results/` (not in git). Every script resolves its default paths from its own location, so scripts can be run from any working directory. Data (`data/`), models (`models/`) and the raw XML (`../data_xml/`) are not version controlled.

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
    └── modeling/07_fit_baseline_lda.py        → models/baseline_lda_32/
            ├── modeling/08_display_lda_topics.py       → results/44_TOPICS_FINAL.csv
            ├── modeling/14_generate_topic_explorer.py  → visualizations/topic_explorer.html
            ├── analysis/09_test_lda_stability.py       → docs/reports/BASELINE_STABILITY_44TOPICS_CORRECTED.md
            │   (period models: same vocabulary, the vectorizer saved by 07)
            ├── modeling/15_fit_period_lda.py [k]       → models/period_lda_<k>/, results/period_<k>_topics.csv
            │       ↓ modeling/17_generate_period_explorer.py → visualizations/period_explorer.html
            └── analysis/16_seed_stability_periods.py   → docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md, results/period_stability/
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
- Last result (2026-10-16, current pipeline): **515 duplicates of 13,917 motions (3.70%)** in 404 groups of identical texts; per period 11 / 25 / 177 / 302, so mostly after 2005
  - Almost all are the **same motion resubmitted in a later year** (only 26 of the 515 copies share the year of their original), e.g. *Forskningsreaktor i Oskarshamn* 2015–2017, *Barnomsorg på obekväm arbetstid* 2018–2021
  - Most are full-length texts (307 copies over 100 words, 200 of 21–100 words); 8 are near-empty bodies (e.g. only `sakna`)
  - The earlier count (133, 0.92%) was on the pre-Stanza pipeline. The rise is expected: motion numbers and author names are now removed at extraction, so a resubmitted motion becomes identical to its original
  - Relevance: a resubmitted motion counts once per year it was submitted, which weights recurring proposals in prominence; whether to keep them is an open point in the seminar notes (2.10)
- Optional argument: `[input_dir]` (default `data/output/stopword_removed`)

### 8. LDA Model (`modeling/07_fit_baseline_lda.py`)
- **Input:** `text_no_stopwords` (body text only; titles are not added). Motions with no body text left after preprocessing are skipped (4 motions)
- **Vectorizer:** `CountVectorizer(max_df=0.5, min_df=5, max_features=10000)`, default token pattern
- **LDA:** scikit-learn `LatentDirichletAllocation`, 32 topics (`NUM_TOPICS`; period models 8, `PERIOD_TOPICS`), `max_iter=50`, `learning_method='online'`, `random_state=42`, `n_jobs=2`
- **Shared settings:** the topic count, LDA settings, stability seeds and the text-loading function live in one module, `modeling/lda_common.py`. The model (07), the stability test (09) and the topic explorer (14) import them from there, so the stability test always measures the same model that is reported
- **No convergence check:** with `learning_method='online'` and sklearn's default `evaluate_every=-1`, every fit runs exactly `max_iter=50` passes; the printed iteration count (always 50) confirms the setting, not convergence
- **Output:** `models/baseline_lda_32/baseline_lda_32_topics.pkl`, `models/baseline_lda_32/baseline_vectorizer.pkl` (directory name `BASELINE_MODEL_DIR` in `lda_common.py`), `results/document_topic_distribution.csv`
- The vectorizer is reused by the stability test and the topic explorer, so they share one vocabulary. The script and model folder keep the name *baseline* from when a title-weighted model was compared against it
- **Diagnostic metric:** training perplexity (diagnostic only, not evidence of generalization)

### 9. Topic Display and Visualization
| Script | Reads | Writes |
|---|---|---|
| `modeling/08_display_lda_topics.py [model_dir]` | `models/baseline_lda_32/` | `results/32_TOPICS_FINAL.csv` (top 20 words/topic) |
| `modeling/15_fit_period_lda.py [num_topics]` | `data/output/stopword_removed/`, baseline vectorizer | `models/period_lda_<k>/` (one model per period + `vocabulary.txt`), `results/period_<k>_topics.csv` (top 20 words per topic and period). See *Period Models* |
| `modeling/17_generate_period_explorer.py [k ...]` | `models/period_lda_<k>/` for k = 8, 11, 15 (default), baseline vectorizer, `data/output/stopword_removed/`, the per-topic CSVs of 16, template `modeling/period_explorer_template.html` | `visualizations/period_explorer.html`: one row (chain) per topic of the first period with four word clouds, one per period, words coloured by how many of the four periods they appear in; topics per period switchable (8/11/15). See *Period explorer* below |
| `modeling/14_generate_topic_explorer.py` | `models/baseline_lda_32/`, `data/output/stopword_removed/`, template `modeling/topic_explorer_template.html` | `visualizations/topic_explorer.html`: word cloud per topic, share overall and per period, top 8 motions with year/party/id, party concentration among the top 5 motions. Reads the model directly. Replaces the earlier word cloud scripts (12, 13) and their template |

- Word weights are shown as normalized probabilities P(word | topic)
- Topics use neutral names (Topic 1–32, no interpretive labels) so they can be inspected without prior bias
- **Topic explorer layout:** per topic, two columns: the word cloud with the share-by-period chart under it on the left, the top motions on the right (stacked on narrow screens)
- **Topic explorer word size:** square root of P(word | topic) on one scale for all clouds, so sizes can be compared between topics; if a word does not fit, all clouds shrink together. A topic spread over many words has a smaller, sparser cloud. The tooltip gives the exact probability
- **Topic explorer order and search:** opens sorted by overall share, largest first (topic numbers are arbitrary). Rise and fall compare the first and last period of the same topic, which is valid here since the whole-corpus model has one set of topics for all periods, but they ignore the middle periods. The search covers only the top 30 words shown (also as part of longer words), as stated next to the search box: a word that is not found can still have some probability in the topic

## Analysis Scripts (`analysis/`)

| Script | Purpose | Output |
|---|---|---|
| `topic_matching.py` | Module: Hungarian-algorithm topic matching between two LDA models; cosine similarity (full distributions) + Jaccard (top words) | — |
| `11_validate_matching_quick.py` | Smoke test on 2,000 real documents + synthetic permutation test (8 topics) | stdout |
| `seed_stability.py` | Module: shared seed-stability procedure (fit one model per seed, match every pair, write the report) used by 09 | — |
| `09_test_lda_stability.py` | Seed stability of the whole-corpus model | `docs/reports/BASELINE_STABILITY_<k>TOPICS_CORRECTED.md` (32: current model; 44: before 2026-10-17) |
| `16_seed_stability_periods.py [k ...]` | Seed stability of the period models for several topic counts (default 8, 11, 15), to choose the count per period | `docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md`; full report per period and count in `docs/reports/period_stability/`, per-topic CSV in `results/period_stability/` |

**Seed-stability reports** list, per seed, the training perplexity and iteration count; then the **stability per topic** of the reference model (seed 42, the seed of the reported model); then cosine and Jaccard statistics for each of the 10 seed pairs; then pooled statistics over all 440 matched topic pairs.

**Stability per topic:** each topic of the seed-42 model is compared with its matched topic in each of the other 4 models. The table gives its top words, in how many of the 4 models it is *found* (matched cosine ≥ 0.70, a judgement call set in `seed_stability.FOUND_COSINE`), and its mean and minimum cosine and mean Jaccard. The same numbers are saved as CSV in `results/` (`results/BASELINE_STABILITY_44TOPICS_PER_TOPIC.csv`). The seed-42 model is fitted on the same data with the same settings as the reported model, so its topic numbers are those of the reported model. Use this to decide which topics to interpret with confidence.

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

### Topic Count: 8 per Period, 32 for the Whole Corpus (Decided 2026-10-17)
- **Current: 8 topics per period, 32 = 4 × 8 for the whole corpus.** The per-period count was chosen with the seed-stability test of the period models: 8 is the only tested count (8, 11, 15) at which at least half of the topics are stable in every period (see *Period Models*, *Topic count per period*). The whole-corpus model has the same total capacity as the four period models together, as in Gordon et al. (60 = 4 × 15).
- **Previously (until 2026-10-16): 44 topics** (= 4 × 11), chosen to capture finer-grained variation. Its seed test found only about 12 of 44 topics stable (see *Seed-Stability Results*).
- **Historical baseline (32 topics):** original selection via topic concentration analysis (6, 10, 14, 18, 22, 29, 32, 36, 43, 50, 57, 64 tested; non-lemmatized text). The new count coincides with it, but was chosen independently, by seed stability.

## Data Quality Metrics

| Metric | Value | Note |
|--------|-------|------|
| Total motions | 13,917 | 13,957 UbU files; 40 without body text or outside 1986–2025 |
| Temporal bins | 4 | 1986-1993, 1994-2004, 2005-2014, 2015-2025 |
| Duplicates detected | 515 (3.70%) | Mostly resubmissions in later years; kept in dataset |
| Vocabulary | 10,000 | `max_features` |
| Stop words | NLTK (114) + 85 supplementary | |
| Boilerplate phrases | 440 | Explicit phrases, no wildcards |
| Lemmatizer | Stanza | Swedish Talbanken model; auxiliaries dropped |
| LDA topics | 32 (whole corpus), 8 per period | 44 until 2026-10-16 |
| Title weighting | None | Tested 3× and 5×, dropped 2026-10-16 |
| Title coverage | ~99.5% | Documents with processed titles |

## Implementation Beyond Proposal

### ✅ Normalized Word Probabilities
- **Proposal:** top words per topic
- **Implementation:** topic-word weights normalized to P(word|topic) and displayed with 4–6 decimal precision
- **Benefit:** enables quantitative comparisons across topics and time periods

### ✅ Complete Document-Topic Distribution
- **Proposal:** topic mixture per document (θ_d)
- **Implementation:** all topic probabilities per document (not just dominant + top 3)
- **Output:** `document_topic_distribution.csv` with doc_id, title, year + one probability column per topic
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

# Period models (run after 07: they use its vectorizer)
python analysis/16_seed_stability_periods.py    # choose the topic count first: 60 fits, roughly 1-3 hours
python modeling/15_fit_period_lda.py 11         # then fit with the chosen count
for k in 8 11 15; do python modeling/15_fit_period_lda.py $k; done   # all three, for the period explorer (about 7 min)
python modeling/17_generate_period_explorer.py
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
- **`tests/test_period_models.py`** — the period models:
  - **Loading:** the periods together hold exactly the motions of the whole-corpus model, in the same order, with the same skip rule; periods come in order with their labels
  - **Shared vocabulary:** one model per period with the shared settings; every model has the same vocabulary in the same order; a word absent from a period still has a column there with only prior weight; a reordered vocabulary is rejected; adjacent periods can be matched with `topic_matching.py`. A mutation check (giving each period its own vectorizer) makes these tests fail
  - **Stability summary:** per-pair means, found-in-all/none and stable counts computed correctly; one summary row per period and count
  - **Period explorer chains:** rows follow the Hungarian matches between adjacent periods (shuffled identical topics are linked correctly), a link below the chain criterion is reported as weak, and the seed-stability CSV is only used if its top words match the model (so it cannot describe another model)
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
│   ├── 15_fit_period_lda.py              (one model per period, shared vocabulary)
│   ├── 17_generate_period_explorer.py    (word clouds per period, topics linked across periods)
│   ├── period_explorer_template.html
│   ├── topic_explorer_template.html
│   └── lda_common.py                     (shared LDA settings, text loading)
├── tests/
│   ├── test_preprocessing.py             (unit tests for steps 01, 03, 04, 05)
│   ├── test_topic_matching.py            (unit tests for analysis/topic_matching.py)
│   ├── test_seed_stability.py            (seed-stability tests and shared LDA code)
│   └── test_period_models.py             (period models and their seed-stability test)
├── analysis/
│   ├── check_pipeline_output.py          (sanity checks on pipeline output)
│   ├── topic_matching.py
│   ├── seed_stability.py                 (shared seed-stability procedure and report)
│   ├── 09_test_lda_stability.py
│   ├── 16_seed_stability_periods.py      (seed stability per period and topic count)
│   ├── 11_validate_matching_quick.py
│   └── count_duplicates.py               (duplicate count for the report)
├── config/
│   ├── boilerplate_phrases.txt
│   └── lemma_corrections.txt              (corrections for known Stanza lemma errors)
├── docs/                                  (in git)
│   ├── PIPELINE_DOCUMENTATION.md
│   ├── PREPROCESSING_ARTIFACTS.md
│   ├── MODEL_REVIEW.md                    (review of the first models on the Stanza pipeline)
│   ├── PROGRESS_SEMINAR_1.md              (status and open decisions, seminar 2026-10-19)
│   └── reports/                           (seed-stability reports written by 09 and 16; period_stability/ per period and count)
├── visualizations/                        (in git; topic_explorer.html, period_explorer.html)
├── results/                               (not in git; generated CSV tables)
├── data/                                  (not in git)
│   ├── input/extracted_text_xml/
│   └── output/{lemmatized,boilerplate_removed,normalized,stopword_removed}/
└── models/                                (not in git)
    ├── baseline_lda_32/          (baseline_lda_44/: the earlier 44-topic model)
    └── period_lda_{8,11,15}/              (one model per period + vocabulary.txt)
```

## Seed-Stability Results: Body Text vs. 3× and 5× Title Weighting (2026-10-16)

**Question:** does title weighting make the 44-topic whole-corpus model more stable across random seeds, and which weight should be used?

**Setup:** for each of the three variants, 44-topic LDA fitted with 5 seeds (42, 123, 456, 789, 999) on the same preprocessed text (Stanza pipeline after the model-review fixes, incl. the `kompetens` compound fix) and the same vocabulary (baseline vectorizer); topics matched between every pair of seeds with the Hungarian algorithm (10 pairs, 440 matched topic pairs per variant); cosine similarity over the full topic-word distributions, Jaccard over the top 20 words. A topic of the seed-42 model counts as *found* in another seed's model if its matched topic has cosine ≥ 0.70. Reports: `docs/reports/BASELINE_STABILITY_44TOPICS_CORRECTED.md` (body text; reproducible with `09_test_lda_stability.py`) and `docs/reports/SEED_STABILITY_{5X,3X}_WEIGHTED_CORRECTED.md` (produced by the 13 seed scripts, since removed; in git history), with per-topic CSVs in `results/`.

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
5. **Many seed-dependent topics** suggest that 44 topics split the corpus more finely than the data supports. For the whole-corpus model this matters less (see *What the whole-corpus instability means* below), but it is a warning for the period models (see *Period Models*, *Topic count per period*).

**What the whole-corpus instability means**
- **The topic count was first kept at 44,** and later changed to 32 = 4 × 8 when the period models were set to 8 topics (2026-10-17, see *Topic count per period*). As in Gordon, the whole-corpus model is mainly a point of comparison: it is rated with the same rubric as the period models. Gordon chose k=60 = 4 × 15 so that it matches four periods of 15 topics; 32 = 4 × 8 follows the same logic. Unstable whole-corpus topics are also the very finding Gordon uses to motivate period models, so they support the design rather than undermine it.
- **Where it does matter:**
  - *Prominence* (mean topic share per period from the whole-corpus model): seed-dependent topics give seed-dependent trends. Restrict the prominence analysis to stable topics, or report it with the range over seeds.
  - *Mapping period topics onto whole-corpus topics* (the proposed extension): the mapping becomes noisy for unstable whole-corpus topics.

**Decision: no title weighting.** The gain (≈0.014 in mean cosine, overlapping ranges) is too small to justify an extra modelling choice. A first decision for 3× (the most even and with the most fully stable topics) was reversed the same day for this reason. All further models, whole-corpus and period models, use the body text only; titles are kept in the data for later use.

---

## Seed-Stability Results: 32-Topic Whole-Corpus Model (2026-10-17)

**Setup:** as for the 44-topic test above: body text only, baseline vectorizer (the same 10,000 words in the same order as before), 5 seeds (42, 123, 456, 789, 999), Hungarian matching between every pair (10 pairs, 320 matched topic pairs), cosine over the full topic-word distributions, Jaccard over the top 20 words, *found* = matched cosine ≥ 0.70, counted for the seed-42 model. Report: `docs/reports/BASELINE_STABILITY_32TOPICS_CORRECTED.md` (`analysis/09_test_lda_stability.py`); per-topic CSV in `results/`. All fits ran 50 passes; training perplexity 1691–1704. A joblib warning during seed 789 ("a worker stopped") did not affect the fit.

| | 44 topics (2026-10-16) | 32 topics |
|---|---|---|
| Mean cosine (mean of the 10 per-pair means) | 0.525 | **0.591** |
| Range of the 10 per-pair means | 0.486–0.566 | 0.554–0.646 |
| Seed-42 topics found in 4 of 4 other models | 5 | **8** |
| … in 3 of 4 | 7 | 4 |
| … in 2 of 4 | 7 | 2 |
| … in 1 of 4 | 6 | 7 |
| … in 0 of 4 | 19 | 11 |
| Stable (3–4 of 4) | 12 of 44 (27%) | **12 of 32 (38%)** |

**Topics found in all four other models (8):** preschool/childcare (mean cosine 0.98), independent schools/school choice (0.96), teachers/teacher education (0.94), research/universities (0.89), compulsory and upper secondary school (0.87), society/knowledge/curriculum (0.85), higher-education places (0.84), medical research/health care (0.73). **In 3 of 4 (4):** regional higher education, adult education/labour market, regional development, student finance.

**Interpretation**
1. **32 topics are more stable than 44**, in mean cosine (+0.07, ranges barely overlapping) and in the share of stable topics (38% vs. 27%). The number of stable topics is the same (12), so, as in the period models, fewer topics mainly remove seed-dependent ones.
2. **The whole-corpus model is still less stable than the period models** (8 topics per period: mean cosine 0.71–0.76, 59% stable). This supports Gordon's case for period models.
3. **Unstable topics:**
   - *Grades* (*betyg, godkänd, betygssystem, mälardalens, ant*): found in no other model, mean cosine 0.015, so the topic does not exist at all with other seeds. With the odd words *mälardalens* and *ant*, it may be a small group of motions with repeated words rather than a theme; to check.
   - *SFI/immigrants* (*sfi, invandrare, nyanländ*): found in no other model (0.16), although it is a clear policy theme; with other seeds its words are probably spread over other topics.
   - Residual topics: *idrott, it, västerås, eskilstuna* (0.17) and *stat, statlig, stiftelse* (0.13).
   - Place-name topics (*Göteborg, Lund, Malmö*; *läkare, Jönköping, Gävle*) remain unstable, as at 44 topics.
4. **Consequences** as in *What the whole-corpus instability means* above: prominence trends and any mapping of period topics onto whole-corpus topics should use the stable topics, or report the range over seeds.

Caveats: one set of seeds, the 0.70 threshold, found-counts for the seed-42 model only.

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

## Period Models and Cross-Period Comparison (first run 2026-10-16; vocabulary option still open)

Separate LDA models will be fitted for each of the four periods and their topics compared across periods with cosine similarity. Cosine similarity between two topic-word vectors is only meaningful if both vectors refer to **the same words in the same order** (supervisor's comment, 2026-10-16). The design below guarantees that.

**Already in place**
- `analysis/topic_matching.py` refuses to compute similarities unless both models have an identical vocabulary in identical column order (`np.array_equal`); different or reordered vocabularies raise a `ValueError`. This is tested in `tests/test_topic_matching.py` (vocabulary mismatch, reordered vocabulary), so a misaligned comparison cannot pass silently.
- The whole-corpus model and all seed-stability runs already share one vocabulary: the vectorizer saved by `07_fit_baseline_lda.py`.
- **Period models (2026-10-16):** `modeling/15_fit_period_lda.py` fits one model per period with that same vectorizer (option A below; design points 1–4 implemented), checks that all period models have the same vocabulary in the same order, and saves the models and the vocabulary. `analysis/16_seed_stability_periods.py` runs the seed-stability test per period and topic count. Both are tested in `tests/test_period_models.py`. Both have been run on the corpus with option A (results below); the period models for 8, 11 and 15 topics are saved in `models/period_lda_{8,11,15}/`.
- **Vocabulary option still open** (seminar notes, 0.1/2.2): the code uses option A, one global vocabulary. If option B (per-period vocabularies compared over shared words, as Gordon) is chosen, `period_vectorizers()` in 15 changes to fit one vectorizer per period, and a step is added that restricts two periods' topic vectors to their shared words before matching; the vocabulary check would then apply to that restricted pair.

**Design for the period models**
1. **One shared vocabulary for all four periods.** Fit a single `CountVectorizer` once on the full corpus (or reuse the baseline vectorizer), then transform each period's motions with it before fitting that period's LDA model. Every period model's `components_` then has the same columns, in the same order, and topics can be compared across periods directly.
2. **Same matching code.** Cross-period comparisons go through `match_and_evaluate` in `topic_matching.py`, which enforces the vocabulary check. With the same number of topics per period (8), the Hungarian matching gives a one-to-one alignment; matching with different topic counts is possible with `require_same_n_topics=False`.
3. **Shared settings.** The period models use the LDA settings and text loading from `modeling/lda_common.py`, like the whole-corpus model (body text only).
4. **Test.** A unit test that the four period models are fitted with an identical vocabulary (same words, same order).

**Topic count per period: test seed stability before fixing it**

The period models have about as many motions per topic as the whole-corpus model (~3,500 motions / 11 topics ≈ 13,900 / 44 ≈ 316), so they may be just as unstable. That matters more here, because the cross-period chains are built from period topics: a chain through a topic that exists only with seed 42 and disappears with other seeds is a chance effect, not thematic development.

Procedure, for each of the four periods:
1. Fit the period's LDA model with the same 5 seeds (42, 123, 456, 789, 999), shared settings from `lda_common.py`, shared vocabulary.
2. Match topics between every pair of seeds with the Hungarian algorithm and compute cosine and Jaccard, as in the whole-corpus seed test (`analysis/seed_stability.py` already does this for any document-term matrix and topic count).
3. Count how many of the period's topics are found again in the other seeds' models (matched cosine ≥ 0.70).
4. Repeat for a few topic counts, e.g. 8, 11 and 15 per period.

Choosing the count:
- Fewer topics are nearly always more stable but coarser; more topics are finer but more seed-dependent. The aim is the **highest count at which most topics are still stable and interpretable**, not simply the most stable one.
- **The same count in all four periods** is simplest to compare and to justify, and is what Gordon does (15 per period). If the result is a count other than 11, use it in all periods.
- Cost: 4 periods × 3 counts × 5 seeds = 60 fits, each on about a quarter of the motions and with fewer topics, so roughly 15 whole-corpus fits or less: at most about three whole-corpus seed tests (each about an hour).

Alternative: fix 11 per period (like Gordon's fixed 15) and use the seed test only to flag uncertain topics and chains. Simpler, but leaves open whether 11 suits this data.

**Seed-stability results per period (2026-10-16, option A)**

`analysis/16_seed_stability_periods.py`, 5 seeds, 10 pairs per period and count; *stable* = found again (cosine ≥ 0.70) in at least 3 of the 4 other seeds' models. Full results: `docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md` and `docs/reports/period_stability/`. Runtime 33 minutes.

| Period | 8 topics: mean cosine / stable | 11 topics | 15 topics |
|---|---|---|---|
| 1986–1993 | 0.73 / 4 of 8 (50%) | 0.63 / 4 of 11 (36%) | 0.52 / 5 of 15 (33%) |
| 1994–2004 | 0.71 / 4 of 8 (50%) | 0.65 / 7 of 11 (64%) | 0.59 / 7 of 15 (47%) |
| 2005–2014 | 0.75 / 6 of 8 (75%) | 0.70 / 6 of 11 (55%) | 0.62 / 6 of 15 (40%) |
| 2015–2025 | 0.76 / 5 of 8 (62%) | 0.70 / 4 of 11 (36%) | 0.61 / 6 of 15 (40%) |
| **All periods** | **19 of 32 (59%)** | **21 of 44 (48%)** | **24 of 60 (40%)** |

- **The period models are more stable than the whole-corpus model** (mean cosine 0.525, about 27% stable): 0.63–0.76 at 8 or 11 topics. This supports Gordon's case for period models.
- **The number of robust themes per period is roughly constant**, about 4–7, whatever the topic count: going from 8 to 15 topics adds 28 topics but only 5 stable ones.
- **Stability falls with the topic count** in every period, in mean cosine and in the stable share; 15 (Gordon's count) is the least stable everywhere.
- **The oldest period (1986–1993) is the least stable at 11 and 15 topics**, although it has the most motions.
- **Decision (2026-10-17): 8 topics per period, and 32 = 4 × 8 for the whole-corpus model.** 8 is the only tested count at which at least half of the topics are stable in every period (50–75%), and it has the highest mean cosine in every period. 11 gives about as many stable topics (21 vs. 19), but about half of its topics are seed-dependent, and in two periods only 36% are stable. Since the number of robust themes is about the same at every count, 8 loses little substance and avoids many chance topics. The whole-corpus model follows to keep the same total capacity as Gordon (`NUM_TOPICS = 32`, `PERIOD_TOPICS = 8` in `lda_common.py`); re-fitted and seed-tested at 32 on 2026-10-17 (see *Seed-Stability Results: 32-Topic Whole-Corpus Model*). Caveats: one set of seeds, the 0.70 threshold, and option A; option B may change the numbers somewhat.

**Period explorer (`modeling/17_generate_period_explorer.py`)**

A page for inspecting the period models before the formal alignment: `visualizations/period_explorer.html`, with 8, 11 or 15 topics per period selectable. It opens on the chosen count (8, `PERIOD_TOPICS`), marked *chosen*; 11 and 15 are kept as *comparison*, to see which chains hold whatever the number of topics (a robustness check for the choice of 8). The models `period_lda_11/`, `period_lda_15/` and their per-topic stability CSVs are therefore kept.
- **Rows are chains.** Each period model has its own topics, so topic numbers do not correspond across periods. Topics of adjacent periods are matched one-to-one with the Hungarian algorithm on cosine (`topic_matching.py`), and each row starts from a topic of the first period and follows the matches to the last.
- **Per cloud:** the period, the topic's number in that period model, its share (mean θ over the period's motions), its seed stability from 16 (`seed n/4`, gold when below 3; shown only if the stability CSV's top words match the model) and the cosine with the matched topic of the previous period. Links below 0.50 are shown as weak (0.50 is Gordon's threshold, but he applies it to the mean of a chain's three links, not to each link; see *Comparison with Gordon*).
- **Weak links break the row:** a solid accent bar runs only over periods joined by links ≥ 0.50; at a weak link the bar stops, a dashed gold rule separates the cells and the cell reads *Alignment uncertain*. The chain heading names the continuous segments (e.g. *linked 1994–2014 only*), or says *forced matches, not a continuous topic* when no link reaches 0.50, so a row of forced matches is not read as one trajectory
- **Word colour = persistence within the chain:** in how many of the chain's four periods the word is among the top 20 words (the words shown): dark blue all four, medium blue three, light blue two, grey one. Bold marks the three most probable words of each cloud. With 8 topics, 12% of the words shown are in all four periods and 44% in only one
- **Word size = probability, one scale per chain:** square root of the word's probability in that period's topic, scaled between the smallest and largest probability shown in the chain's four clouds; if a word does not fit, all four clouds shrink together. A word at 5% is therefore drawn larger than one at 1.5% across the chain's periods. Sizes are not comparable between chains (each chain has its own scale); the tooltip gives the exact probability
- **Sorting and search:** by default strongest chain first (weakest link, high to low: chains linked through all periods at the top, forced matches at the bottom); also by chain number, weakest link first, rise or fall in share (first vs last period, computed only for chains linked through all four periods, since a change across a weak link may compare unrelated topics; broken chains are listed last, marked *no change computed*); a word search filters chains and highlights the word. The search covers only the top 20 words shown in each cloud (also as part of longer words), as stated next to the search box: a word that is not found can still have some probability in the topic, so a search cannot show that a word is absent from a topic.
- **Limitations:** the Hungarian matching gives every topic a partner, so a topic that exists in only one period still sits in a chain, joined by weak links; a topic that appears in a later period cannot start its own row. This is a provisional alignment for inspection only, without Gordon's permutation null (seminar notes 2.5).
- **First observation (option A):** few chains hold through all four periods: 3 of 8, 3 of 11 and 4 of 15 have every link ≥ 0.50 (by Gordon's mean criterion: 5 of 8, 7 of 11 and 7 of 15). Those that hold are research and higher education, higher education and regions, and school (pupils, teachers). The other topics change between periods or are linked to different themes, which is the kind of change the analysis is about, but also why the permutation test is needed to tell real links from chance.

**Consequences to keep in mind**
- **Words absent from a period** get near-zero weight in that period's topics (only the LDA prior). That is correct, but it means period-specific vocabulary also contributes to topics looking different across periods; this should be noted when interpreting similarities.
- **Vocabulary thresholds** (`min_df=5`, `max_df=0.5`, `max_features=10000`) are applied to the full corpus, not per period. A word frequent in one period but rare overall is still included; a word used in more than half of all motions is excluded everywhere.

## Comparison with Gordon (2026) (2026-10-17)

How the current pipeline (32-topic whole-corpus model, 8-topic period models, global vocabulary) compares with the reference study, *Tracing Thematic Change in Early English-Language Science Fiction, 1818–1930*.

**Comparable numbers**

| | Gordon | This study |
|---|---|---|
| Whole-corpus seed stability (mean Jaccard of the top words) | 0.26–0.31 | 0.283, per-pair range 0.25–0.35 (32 topics) |
| Matched mean cosine between adjacent periods, 15 topics per period | 0.44–0.59 | 0.41–0.54 |
| Same, 8 topics per period (the chosen count) | — | 0.53, 0.62, 0.68 |
| Chains with mean cosine ≥ 0.50 over the three transitions | 7 of 15 | 7 of 15 (15 topics); 5 of 8 (8 topics); 7 of 11 (11 topics) |

- **Seed instability is of the same size as Gordon's.** The instability of the whole-corpus model is therefore not a weakness of this pipeline; Gordon found the same and uses it as part of his argument for period models.
- **At Gordon's topic count (15 per period) the alignment is almost identical to his**, both in the matched cosine and in the number of chains that pass his criterion. At 8 topics the links are stronger, as expected with fewer, broader topics.
- Caveat: different corpora, algorithms and vocabulary designs (below), so the agreement shows that the results are of the same order, not that the methods are equivalent.

**Chain criterion: Gordon's vs. the period explorer's**

Gordon counts a chain as holding if the **mean** cosine of its three links is at least 0.50. The period explorer currently breaks a chain at **every** link below 0.50, which is stricter: at 8 topics 3 chains have every link ≥ 0.50, but 5 pass Gordon's criterion (chains 4: 0.40, 0.57, 0.53, and 3: 0.33, 0.76, 0.70, pass on the mean but have one weak link). Proposed: Gordon's mean criterion as the main one, for comparability, and the link-by-link display as additional information on where a chain is uncertain. Not yet changed in the period explorer.

**Methodological differences**

| Point | Gordon | This study | Assessment |
|---|---|---|---|
| Algorithm | MALLET, Gibbs sampling, 1,000 iterations, asymmetric hyperparameter optimization | scikit-learn, online variational Bayes, 50 passes, symmetric priors | Probably the largest difference. Convergence is not checked (see below) |
| Vocabulary | Per period, adjacent periods compared over their shared words | One global vocabulary | Open (seminar notes 2.2); the shared-word comparison may change the cosines somewhat |
| Documents | 1,000-word book chunks | Whole motions | Justified: natural units, most shorter than 1,000 words |
| Proper names | Removed | Kept | Open (seminar notes 2.7); the place-name topics are a parallel to Gordon's author signal |
| Lemmatization | None | Stanza | Justified by Swedish inflection |
| Topics | 15 per period, 60 whole corpus | 8 per period, 32 whole corpus | Justified by the seed-stability test; 11 and 15 are shown for comparison |
| Seed stability | Whole-corpus runs only | Every model | Extension |

**Convergence.** Every fit runs exactly 50 passes (`max_iter=50`, no convergence check). Online LDA processes the motions in mini-batches of 128 (about 109 updates per pass, about 5,400 in 50 passes) with a step size that decays with every update, to about 0.2% of the first in the last passes. Topics therefore stop changing towards the end whether or not they have reached a good solution, so a settled model is not evidence of convergence. Gordon's 1,000 Gibbs iterations are a different algorithm and not directly comparable. Too few passes could contribute to the seed instability. Proposed check (not run): a 200-pass fit with perplexity and topic change recorded every 5 passes, and a second seed at 200 passes to see whether stability improves.

**Not yet done, so not yet comparable**
- **Permutation null and z-scores:** Gordon's matched cosine is 0.44–0.59 against 0.22–0.25 for random pairings (z = 7–9). Without the null, the alignments can be said to look similar, not to be significant.
- **Rubric coding** (coherent, thematic, concentration) of the whole-corpus and period models: Gordon's main comparison of binned and unbinned models.
- **A whole-corpus model with 8 topics**, the counterpart of Gordon's k = 15 control (one period's number of topics). Only the 4 × 8 = 32 counterpart of his k = 60 exists.

---

## Next Steps

0. **Act on the first model review** (`MODEL_REVIEW.md`, 2026-10-16): the first models on the Stanza pipeline are fitted and reviewed; the review's vocabulary fixes (boilerplate gaps, abbreviation matching in step 03, artifact stopwords, Stanza lemma errors) are done; a few small leftovers remain (see the review)
1. ✅ **Seed-stability tests** for the 44-topic model on body text and with 3×/5× title weighting (2026-10-16; see *Seed-Stability Results*)
2. ✅ **Evaluate:** title weighting gives only a small stability gain; **no title weighting**, weighting code removed
3. **Period models** (see *Period Models* above): fitted and seed-tested with option A for 8, 11 and 15 topics, inspectable in the period explorer. ✅ Topic count chosen: 8 per period, 32 for the whole corpus (2026-10-17). ✅ Whole-corpus model re-fitted and seed-tested at 32 (2026-10-17: mean cosine 0.591, 12 of 32 topics stable) and topic explorer regenerated (14). To do: regenerate the topic list (08); re-run 15/16 if the seminar chooses vocabulary option B
4. **Topic alignment and trajectory analysis**
5. **Publication:** document findings for thesis/paper
