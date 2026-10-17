# Swedish Parliamentary Education Motions: NLP Pipeline

## Overview

13,917 motions to the Swedish parliament's Education Committee (Utbildningsutskottet, UbU), 1986–2025, processed into lemmatized body text and modelled with Latent Dirichlet Allocation (LDA), following the temporally binned design of Gordon (2026):

- **Four period models**, one per period (1986–1993, 1994–2004, 2005–2014, 2015–2025), **8 topics each**, aligned across adjacent periods into topic chains
- **One whole-corpus model with 32 topics** (= 4 × 8, the same total capacity as the four period models together), as the point of comparison
- **Body text only.** Titles are processed and kept as a separate field, but are not part of the model's documents
- **Seed stability** is tested for every model (5 seeds, Hungarian matching)

How the design was reached, and the open questions, are in `PROGRESS_SEMINAR_1.md`; the seed-stability reports are in `reports/`.

All paths below are relative to `project/`. Documentation and reports are in `docs/` and the HTML visualizations in `visualizations/` (both in git); generated tables (CSV) are in `results/`, data in `data/` and fitted models in `models/` (not in git). The raw XML is in `../../swedish-parliament-data/`, next to the repository. Every script resolves its default paths from its own location, so scripts can be run from any working directory.

## Pipeline Architecture

```
../../swedish-parliament-data/ (raw riksdag XML, one folder per period)
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
    └── modeling/07_fit_baseline_lda.py        → models/baseline_lda_32/ (whole-corpus model + the shared vectorizer)
            ├── modeling/08_display_lda_topics.py       → results/32_TOPICS_FINAL.csv
            ├── modeling/14_generate_topic_explorer.py  → visualizations/topic_explorer.html
            ├── analysis/09_test_lda_stability.py       → docs/reports/BASELINE_STABILITY_32TOPICS_CORRECTED.md
            │   (period models: same vocabulary, the vectorizer saved by 07)
            ├── modeling/15_fit_period_lda.py [k]       → models/period_lda_<k>/, results/period_<k>_topics.csv
            │       ↓ modeling/17_generate_period_explorer.py → visualizations/period_explorer.html
            └── analysis/16_seed_stability_periods.py   → docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md, results/period_stability/
```

Every data stage stores one JSONL file per period: `group1_1986-1993.jsonl`, `group2_1994-2004.jsonl`, `group3_2005-2014.jsonl`, `group4_2015-2025.jsonl`. Each stage adds fields and keeps earlier ones, so metadata (`dok_id`, title, date, author names) is carried through to the models. Every stage counts and reports malformed JSON lines per period, so no data is lost silently.

**Why this order:** Stanza is the only slow step, so it runs once, right after extraction, and saves every word with its original form, lemma and part of speech. Everything after it works from that saved output and takes minutes, so the boilerplate list and stopwords can be changed and re-run without running Stanza again.

**Titles** go through exactly the same steps as the body text, in the same scripts (fields prefixed `title_`). The final title (`title_processed`) is kept in the data for later use (e.g. labelling topics).

## Processing Steps

### 1. Extraction (`extraction/01_extract_from_xml.py`)
- **Input:** XML files from the Swedish parliament open data portal, searched recursively (default `../../swedish-parliament-data/`; another location can be passed as the first argument)
- **Method:** follows Bruinsma & Johansson (2024)
- **Filter:** UbU committee (`organ` field), case-insensitive
- **Extract:** dok_id, date, title, author names, body text (between the introduction and signature markers); HTML entities decoded
- **HTML to text:** text pieces are joined without separators, with whitespace only at block-level tags (`<p>`, `<br>`, `<td>`, headings, …). The source HTML often splits single words across inline `<span>`s (`uppföljni</span><span>ng`, and in some motions every å/ä/ö is its own span), so joining with spaces would fragment words (see `PREPROCESSING_ARTIFACTS.md`)
- **Character repair (body and title):** soft hyphens (U+00AD) removed; text NFC-normalized; spacing diacritics after a base letter replaced (`a°` → `å`, `a¨` → `ä`, `o¨` → `ö`)
- **Title heading removed:** the title appears as a heading near the start of the body in ~97% of motions. The first word-by-word match of the title within the first 400 characters is removed (13,532 motions), so the body holds the motion's own text. Later mentions of the title phrase (e.g. in the proposed decision) are kept
- **Metadata removed (body and title):** motion numbers (`1989/90:Ub742`, `GE02A1`) and the motion's own author names (from the XML author list, whole-word, case-insensitive). Done before Stanza, so numbers are not split into odd tokens and names are not lemmatized
- **Period:** assigned from the year of the motion's date
- **Output:** 13,917 motions (13,957 UbU files; 40 have no body text or a date outside 1986–2025) in `data/input/extracted_text_xml/`. Fields: `text` (cleaned body), `title` (original title, for display), `title_text` (cleaned title, for processing). The files are JSONL; the folder name means "text extracted from XML"

### 2. Tagging and Lemmatization (`preprocessing/02_lemmatize.py`) — run once
- **Tool:** [Stanza](https://stanfordnlp.github.io/stanza/) Swedish pipeline (`tokenize,pos,lemma`, default Talbanken model), stored in `SU/stanza_resources/` and downloaded there automatically if missing
- Runs on the running text of body and title, so the tagger sees full sentences and can use context
- **Saves every word** as `[word, lemma, upos]`, grouped by sentence, in `tokens` (body) and `title_tokens` (title). Nothing is removed at this step
- **Resumable:** motions already in the output file are skipped, so an interrupted run continues where it stopped
- **Runtime:** CPU-heavy; hours for the full corpus

### 3. Boilerplate Removal (`preprocessing/03_remove_boilerplate.py`)
- **Phrases:** `config/boilerplate_phrases.txt` (440 entries, one explicit word or phrase per line, no wildcards), matched case-insensitively against the **original word forms** saved by step 2, so the list keeps its surface forms (`riksdagen`, `med anledning av`). A word is removed only if a phrase match covers the whole word, apart from trailing punctuation (Stanza keeps the full stop in abbreviations, so the phrase `mot` removes `Mot.`); phrases never match across sentences
- **Categories:** OCR/scanning artifacts, government and parliamentary institutions, parliamentary document/reference terms, procedural language, party names, etc.
- **Output is lemmas** of the remaining words, one sentence per line
- **Dropped tokens:** auxiliary verbs (UPOS `AUX`), punctuation and symbols. Stanza lemmatizes the modal *ska/skall/skulle* to `skola`, which would merge with the noun *skola* (school); all auxiliaries are stopwords anyway
- **Dropped abbreviation lemmas:** words whose lemma contains an underscore. Stanza expands abbreviations into multi-word lemmas (`t.ex.` → `till_exempel`, `bl.a.` → `bland_annat`, `s.k.` → `så_kallad`, `m.fl.` → `med_flera`), sometimes garbled (`få_cetera`). Every dropped word is counted in `data/output/boilerplate_removed/underscore_lemmas.json` (lemma → count and word forms) for manual review
- **Lemma corrections:** known Stanza lemma errors are corrected from `config/lemma_corrections.txt` (`kompet` → `kompetens`, `lärosät` → `lärosäte`, `anslagen` → `anslag`, …). Stanza guesses lemmas for words it has not seen in training, and some guesses are truncated; the list corrects the errors found in the model review (`MODEL_REVIEW.md`), it does not replace the lemmatizer
- **Output fields:** `text_no_boilerplate`, `title_no_boilerplate`

### 4. Normalization (`preprocessing/04_normalize_text.py`)
- Lowercase, remove numbers and punctuation, collapse whitespace
- Drops single-character words; preserves line breaks
- **Output fields:** `text_normalized`, `title_normalized`

### 5. Stopword Removal (`preprocessing/05_remove_stopwords.py`)
- **Base list:** NLTK Swedish stop words (114)
- **Supplementary (85, hard-coded):** parliamentary abbreviations (ub, dvs, osv, …), auxiliary verbs (ska, skall, blir, …), generic connectors, verbs and adjectives identified from LDA inspection (kommer, enligt, olika, göra, …), and the **lemma forms** of inflected entries (behöva, vilja, kunna, ny, stor, olik, mången, …), since the text is lemmatized. Content abbreviations such as `fn`, `eg`, `ky`, `ib` are deliberately not stopwords (education-policy terms; see `MODEL_REVIEW.md`)
- **Output fields:** `text_no_stopwords` (final body text, used by the models) and `title_processed` (final title text)

### Duplicate count (`analysis/count_duplicates.py`) — for the report, not a pipeline step
- Models use all motions; duplicates are not removed
- MD5 hash of the whitespace-normalized final text; one hash dictionary across all periods, so duplicates are found across periods. Prints duplicates per period, the total and each duplicate → original `dok_id`; writes no data
- The count depends on the final text, so re-run it after changing the boilerplate or stopword lists
- **Current result: 515 duplicates of 13,917 motions (3.70%)** in 404 groups of identical texts; per period 11 / 25 / 177 / 302
  - Almost all are the **same motion resubmitted in a later year** (only 26 of the 515 copies share the year of their original), e.g. *Forskningsreaktor i Oskarshamn* 2015–2017. Motion numbers and author names are removed at extraction, so a resubmitted motion is identical to its original
  - Most are full-length texts (307 copies over 100 words, 200 of 21–100 words); 8 are near-empty bodies
  - A resubmitted motion counts once per year it was submitted, which weights recurring proposals in prominence; whether to keep them is open (seminar notes 2.10)

## Models

### Shared settings (`modeling/lda_common.py`)
Topic counts (`NUM_TOPICS = 32`, `PERIOD_TOPICS = 8`), the model folder name (`BASELINE_MODEL_DIR`), LDA settings, the reported seed (42), the stability seeds (42, 123, 456, 789, 999) and text loading live in this one module. Every model, stability test and explorer imports them from there, so the stability tests always measure the same models that are reported. A test checks that no other script creates its own LDA model.

- **LDA:** scikit-learn `LatentDirichletAllocation`, `learning_method='online'`, `max_iter=50`, `random_state=42`, `n_jobs=2`; symmetric default priors
- **No convergence check:** with online learning and sklearn's default `evaluate_every=-1`, every fit runs exactly 50 passes. The motions are processed in mini-batches of 128 (about 109 updates per pass) with a step size that decays with every update, so topics stop changing towards the end whether or not they have converged. The iteration count in the reports (always 50) confirms the setting, not convergence
- **Input:** `text_no_stopwords` (body text only). Motions with no body text left after preprocessing are skipped (4 motions)
- **Diagnostic:** training perplexity, reported as a diagnostic only, not evidence of generalization

### Whole-corpus model (`modeling/07_fit_baseline_lda.py`)
- **Vectorizer:** `CountVectorizer(max_df=0.5, min_df=5, max_features=10000)`, default token pattern. This vectorizer is **the vocabulary of every model**: the whole-corpus model, the period models, the stability tests and both explorers
- **Model:** 32 topics
- **Output:** `models/baseline_lda_32/baseline_lda_32_topics.pkl`, `models/baseline_lda_32/baseline_vectorizer.pkl`, and `results/document_topic_distribution.csv` (doc_id, title, year and the probability of every topic for every motion, for prevalence analysis)
- The name *baseline* is kept from the scripts' history; it is the whole-corpus model

### Period models (`modeling/15_fit_period_lda.py [k]`)
- One model per period, 8 topics each (`k` overrides the count), with the shared settings and **the global vocabulary** of the whole-corpus vectorizer. Each period's motions are transformed with that vectorizer, so every period model has the same columns in the same order and topics can be compared across periods directly
- The script checks that all period models have the same vocabulary in the same order; `analysis/topic_matching.py` also refuses to compare models whose vocabularies differ or are reordered (both tested)
- **Output:** `models/period_lda_<k>/` (one model per period + `vocabulary.txt`), `results/period_<k>_topics.csv` (top 20 words per topic and period). Models exist for k = 8 (the analysis) and 11 and 15 (comparison in the period explorer)
- **Consequences of the global vocabulary:** words absent from a period get near-zero weight in that period's topics (only the prior), so period-specific vocabulary also makes topics look different across periods. The vocabulary thresholds apply to the full corpus: a word frequent in one period but rare overall is still included; a word in more than half of all motions is excluded everywhere
- **Vocabulary design is open** (seminar notes 2.2): Gordon uses one vocabulary per period and compares adjacent periods over their shared words. Switching would change `period_vectorizers()` in 15 and add a step restricting two periods' topics to their shared words before matching

### Topic matching (`analysis/topic_matching.py`)
Hungarian-algorithm one-to-one matching between two models' topics on cosine similarity over the full topic-word distributions, with Jaccard overlap of the top words as a secondary measure. Used for seed stability (matching models with different seeds) and for alignment across periods (matching adjacent periods). One-to-one matching cannot represent a topic splitting or merging.

## Seed-Stability Testing

| Script | Tests | Output |
|---|---|---|
| `analysis/09_test_lda_stability.py` | The whole-corpus model | `docs/reports/BASELINE_STABILITY_32TOPICS_CORRECTED.md`, `results/BASELINE_STABILITY_32TOPICS_PER_TOPIC.csv` |
| `analysis/16_seed_stability_periods.py [k ...]` | The period models, for several topic counts (default 8, 11, 15) | `docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md`; full report per period and count in `docs/reports/period_stability/`; per-topic CSV in `results/period_stability/` (read by the period explorer) |

Both use the shared procedure in `analysis/seed_stability.py`: fit one model per seed (5 seeds), match every pair of models with the Hungarian algorithm (10 pairs), and compare matched topics by cosine (full distributions) and Jaccard (top 20 words).

**Reports** list, per seed, the training perplexity and iteration count; then the **stability per topic** of the reference model (seed 42, the seed of the reported model); then cosine and Jaccard statistics for each of the 10 seed pairs; then pooled statistics over all matched topic pairs.

**Stability per topic:** each topic of the seed-42 model is compared with its matched topic in each of the other 4 models. A topic is *found* in a model if the matched cosine is at least 0.70 (a judgement call, `seed_stability.FOUND_COSINE`), and *stable* if found in at least 3 of the 4. The table gives its top words, the number of models it is found in, and its mean and minimum cosine and mean Jaccard. The seed-42 model is fitted on the same data with the same settings as the reported model, so its topic numbers are those of the reported model. Use this to decide which topics to interpret with confidence.

**Pooled statistics:** the matched topic pairs are not independent (each seed's model appears in 4 of the 10 pairs). The pooled mean is a fair summary, but the pooled standard deviation understates the uncertainty; for the spread across runs, report the 10 per-pair means or their range.

## Current Results

### Whole-corpus model (32 topics)
Report: `docs/reports/BASELINE_STABILITY_32TOPICS_CORRECTED.md`.

| | 32 topics |
|---|---|
| Mean cosine (mean of the 10 per-pair means) | 0.591 |
| Range of the 10 per-pair means | 0.554–0.646 |
| Mean Jaccard (top 20) | 0.283 (per-pair 0.25–0.35) |
| Seed-42 topics found in 4 / 3 / 2 / 1 / 0 of the other 4 models | 8 / 4 / 2 / 7 / 11 |
| Stable (3–4 of 4) | 12 of 32 (38%) |
| Training perplexity, 5 seeds | 1691–1704 |

- **Found in all four other models (8):** preschool/childcare (mean cosine 0.98), independent schools/school choice (0.96), teachers/teacher education (0.94), research/universities (0.89), compulsory and upper secondary school (0.87), society/knowledge/curriculum (0.85), higher-education places (0.84), medical research/health care (0.73). **In 3 of 4:** regional higher education, adult education/labour market, regional development, student finance
- **Unstable:** grades (*betyg, godkänd, betygssystem, mälardalens, ant*; found in no other model, mean cosine 0.015, possibly a few motions with repeated words rather than a theme; to check); SFI/immigrants (*sfi, invandrare, nyanländ*; 0.16, a clear theme whose words other seeds spread over other topics); residual topics (*idrott, it, västerås*; *stat, statlig, stiftelse*); place-name topics (*Göteborg, Lund, Malmö*; *läkare, Jönköping, Gävle*)
- **Use:** prominence trends and any mapping of period topics onto whole-corpus topics should rely on the stable topics, or report the range over seeds
- For comparison, the earlier 44-topic model had mean cosine 0.525 and 12 of 44 topics stable (`docs/reports/BASELINE_STABILITY_44TOPICS_CORRECTED.md`): fewer topics removed mainly seed-dependent ones

### Period models
Report: `docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md`.

| Period | 8 topics: mean cosine / stable | 11 topics | 15 topics |
|---|---|---|---|
| 1986–1993 | 0.73 / 4 of 8 (50%) | 0.63 / 4 of 11 (36%) | 0.52 / 5 of 15 (33%) |
| 1994–2004 | 0.71 / 4 of 8 (50%) | 0.65 / 7 of 11 (64%) | 0.59 / 7 of 15 (47%) |
| 2005–2014 | 0.75 / 6 of 8 (75%) | 0.70 / 6 of 11 (55%) | 0.62 / 6 of 15 (40%) |
| 2015–2025 | 0.76 / 5 of 8 (62%) | 0.70 / 4 of 11 (36%) | 0.61 / 6 of 15 (40%) |
| **All periods** | **19 of 32 (59%)** | **21 of 44 (48%)** | **24 of 60 (40%)** |

- The period models are more stable than the whole-corpus model, which supports Gordon's case for period models
- The number of robust themes per period is about 4–7 whatever the topic count (8 → 15 adds 28 topics but only 5 stable ones), and stability falls with the topic count in every period
- The oldest period (1986–1993) is the least stable at 11 and 15 topics, although it has the most motions

**Alignment across periods (8 topics):** matched mean cosine 0.53, 0.62 and 0.68 for the three transitions. 5 of 8 chains hold by Gordon's criterion (mean link ≥ 0.50): research and higher education, higher education and regions, school (pupils, teachers), and two chains (7 and 3) whose first link, 1986–1993 → 1994–2004, is weak. 3 of 8 have every link ≥ 0.50. Without the permutation null these are provisional.

### Comparison with Gordon (2026)

*Tracing Thematic Change in Early English-Language Science Fiction, 1818–1930* (`../../swedish-parliament-instructions/tracing_thematic_change.pdf`).

| | Gordon | This study |
|---|---|---|
| Whole-corpus seed stability (mean Jaccard of the top words) | 0.26–0.31 | 0.283, per-pair range 0.25–0.35 (32 topics) |
| Matched mean cosine between adjacent periods, 15 topics per period | 0.44–0.59 | 0.41–0.54 |
| Same, 8 topics per period (the chosen count) | — | 0.53, 0.62, 0.68 |
| Chains with mean cosine ≥ 0.50 over the three transitions | 7 of 15 | 7 of 15 (15 topics); 7 of 11 (11 topics); 5 of 8 (8 topics) |

- **Seed instability is of the same size as Gordon's**, so it is not a weakness of this pipeline; Gordon uses the same finding as part of his argument for period models
- **At Gordon's topic count (15 per period) the alignment is almost identical to his**, in matched cosine and in the number of chains that pass his criterion. At 8 topics the links are stronger, as expected with fewer, broader topics
- Different corpora, algorithms and vocabulary designs: the agreement shows results of the same order, not equivalent methods

| Point | Gordon | This study | Assessment |
|---|---|---|---|
| Algorithm | MALLET, Gibbs sampling, 1,000 iterations, asymmetric hyperparameter optimization every 10 iterations | scikit-learn, online variational Bayes, 50 passes, symmetric priors | Probably the largest difference; convergence not checked |
| Vocabulary | Per period, adjacent periods compared over their shared words | One global vocabulary | Open (seminar notes 2.2) |
| Author signal | Authorless preprocessing (MALLET `DownsampleLabelWords`) | None | Counterpart here: MP/constituency signal (place names) |
| Documents | 1,000-word book chunks | Whole motions | Natural units, most shorter than 1,000 words |
| Proper names | Removed | Kept | Open (seminar notes 2.7) |
| Lemmatization | None | Stanza | Swedish inflection |
| Topics | 15 per period, 60 whole corpus | 8 per period, 32 whole corpus | Chosen by seed stability; 11 and 15 shown for comparison |
| Seed stability | Whole-corpus runs only | Every model | Extension |

**Not yet comparable:** the permutation null and z-scores (Gordon: matched 0.44–0.59 against 0.22–0.25 for random pairings, z = 7–9), the rubric coding (coherent, thematic, concentration) of all models, and a whole-corpus model with 8 topics (the counterpart of Gordon's k = 15 control).

## Visualizations

| Script | Reads | Writes |
|---|---|---|
| `modeling/08_display_lda_topics.py [model_dir]` | `models/baseline_lda_32/` | `results/32_TOPICS_FINAL.csv` (top 20 words per topic, as P(word \| topic)) |
| `modeling/14_generate_topic_explorer.py` | `models/baseline_lda_32/`, `data/output/stopword_removed/`, template `modeling/topic_explorer_template.html` | `visualizations/topic_explorer.html` |
| `modeling/17_generate_period_explorer.py [k ...]` | `models/period_lda_<k>/` for k = 8, 11, 15 (default), the shared vectorizer, `data/output/stopword_removed/`, the per-topic CSVs of 16, template `modeling/period_explorer_template.html` | `visualizations/period_explorer.html` |

Both pages are self-contained HTML (open in a browser; internet needed only for the fonts). Word weights are shown as P(word | topic). Topics have neutral names (Topic 1–32, T1–T8 per period), so they can be inspected without interpretive labels.

### Topic explorer (whole-corpus model)
- **Per topic, two columns:** the word cloud (top 30 words) with the share-by-period chart under it on the left; the top 8 motions (year, party, id, θ) on the right; stacked on narrow screens. The heading gives the overall share and the party concentration among the top 5 motions (gold when 4 or 5 share the first signatory's party)
- **Word size:** square root of P(word | topic), on **one scale for all clouds**, so sizes can be compared between topics; if a word does not fit, all clouds shrink together. A topic spread over many words has a smaller, sparser cloud. The tooltip gives the exact probability
- **Order:** opens sorted by overall share, largest first (topic numbers are arbitrary); also by topic number, rise or fall (first vs last period; valid here since one model covers all periods, but the middle periods are ignored) and party concentration
- **Search:** covers only the 30 words shown per cloud (also as part of longer words), as stated next to the search box; a word that is not found can still have some probability in the topic

### Period explorer (period models)
- **Topic counts:** opens on the chosen count (8, marked *chosen*); 11 and 15 are selectable as *comparison*, to see which chains hold whatever the number of topics
- **Rows are chains.** Each period model has its own topics, so topic numbers do not correspond across periods. Topics of adjacent periods are matched one-to-one (Hungarian algorithm on cosine) and each row follows the matches from a topic of the first period to the last
- **Chain holds (main criterion, Gordon's):** the heading says *holds* if the mean cosine of the chain's three links is at least 0.50, otherwise *does not hold* (gold), with the mean and the weakest link
- **Weak links (additional information):** a single link below 0.50 breaks the row: the accent bar over the clouds stops, a dashed gold rule separates the cells and the cell reads *Alignment uncertain*. The heading names the strongly linked segments, or says *forced matches, not a continuous topic* when no link reaches 0.50. A chain can hold on the mean and still have one weak link
- **Per cloud:** the period, the topic's number in that period model, its share (mean θ over the period's motions), its seed stability from 16 (`seed n/4`, gold when below 3; shown only if the stability CSV's top words match the model) and the cosine with the matched topic of the previous period
- **Word colour = persistence within the chain:** in how many of the chain's four periods the word is among the top 20 words (the words shown): dark blue all four, medium blue three, light blue two, grey one. With 8 topics, 12% of the words shown are in all four periods and 44% in only one. Bold marks the three most probable words of each cloud
- **Word size:** square root of P(word | topic), on **one scale per chain**, so sizes can be compared across a chain's periods but not between chains; if a word does not fit, the chain's four clouds shrink together. The tooltip gives the exact probability
- **Order:** opens with the strongest chain first (mean link, high to low); also by chain number, weakest link first, and rise or fall in share (first vs last period, only for chains with every link ≥ 0.50, since a change across a weak link may compare unrelated topics; other chains are listed last, marked *no change computed*)
- **Search:** covers only the 20 words shown per cloud (also as part of longer words), as stated next to the search box
- **Limitations:** the matching gives every topic a partner, so a topic that exists in only one period still sits in a chain, joined by weak links, and a topic that appears in a later period cannot start its own row. Provisional alignment for inspection, without Gordon's permutation null

## Design Decisions

- **Stopwords vs. boilerplate.** Stopwords are general Swedish words, applied to the lemmatized, normalized text; boilerplate is parliamentary and domain-specific language (institutions, procedure, references), matched on the original word forms. Keeping them apart lets the stopword list be reused for other Swedish texts
- **Stanza lemmatization.** Swedish inflection splits one word into many forms (*skola, skolan, skolor, skolornas*), which fragments topics. Stanza is a general, context-aware lemmatizer run once on full sentences, with a small table of corrections for known errors. Known trade-offs: comparatives are reduced to the positive (*högre utbildning* → `hög utbildning`), rare compounds can get wrong lemmas (*arbetsvillkor* → `arbetsvillka`), and modal *ska* gets the lemma `skola` (handled by dropping auxiliaries). spaCy's `sv_core_news_sm` and a hand-made lookup table of education terms were tried earlier and rejected
- **Body text only.** Appending the title 3× or 5× to the body gave only a small stability gain (mean matched cosine 0.539 against 0.525 at 44 topics, overlapping ranges; reports `docs/reports/SEED_STABILITY_{3X,5X}_WEIGHTED_CORRECTED.md`), too small to justify an extra modelling choice. Titles are kept in the data
- **Topic count: 8 per period, 32 for the whole corpus.** 8 is the only tested count (8, 11, 15) at which at least half of the topics are stable in every period, and it has the highest mean cosine in every period; since the number of robust themes is about the same at every count, 8 loses little substance and avoids many chance topics. The whole-corpus model has the same total capacity as the four period models, as in Gordon (60 = 4 × 15)
- **Global vocabulary** for all models, so topics can be compared across periods directly; Gordon's per-period vocabularies are the open alternative (see *Period models*)
- **Chain criterion:** Gordon's mean of the three links ≥ 0.50, so results are comparable with his; single weak links are shown as additional information

## Configuration Files

- **`config/boilerplate_phrases.txt`:** 440 explicit words/phrases, one per line, grouped by category with `#` headers. Matched against original word forms (body and title). An alternative file can be passed as the 3rd argument to `03_remove_boilerplate.py`. After editing, re-run steps 03–05 (no need to re-run Stanza)
- **`config/lemma_corrections.txt`:** corrections for known Stanza lemma errors, one `wrong correct` pair per line with `#` comments, applied in step 03 to body and title, case-insensitively. A wrong lemma with a leading `*` is also corrected at the end of a compound (`*kompet kompetens`: `gymnasiekompet` → `gymnasiekompetens`); mark an entry only after checking its compounds (`anslagen` must not be marked, because of *sammanslagen*). After editing, re-run steps 03–05
- **Stopwords:** hard-coded in `preprocessing/05_remove_stopwords.py` (NLTK base + supplementary list, including lemma forms)

## Data Summary

| Metric | Value | Note |
|--------|-------|------|
| Motions | 13,917 | 13,957 UbU files; 40 without body text or outside 1986–2025 |
| Periods | 4 | 1986–1993, 1994–2004, 2005–2014, 2015–2025 (3,257–3,770 motions each) |
| Duplicates | 515 (3.70%) | Mostly resubmissions in later years; kept |
| Vocabulary | 10,000 | `max_features`; one global vocabulary |
| Stopwords | NLTK (114) + 85 supplementary | |
| Boilerplate phrases | 440 | Explicit phrases, no wildcards |
| Lemmatizer | Stanza | Swedish Talbanken model; auxiliaries dropped |
| LDA topics | 8 per period, 32 whole corpus | 11 and 15 per period kept for comparison |
| Title coverage | ~99.5% | Motions with a processed title |

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
python extraction/01_extract_from_xml.py      # default input: ../../swedish-parliament-data
python preprocessing/02_lemmatize.py          # slow (hours); resumable if interrupted

# Cheap: re-run these after changing the boilerplate list, lemma corrections or stopwords
python preprocessing/03_remove_boilerplate.py
python preprocessing/04_normalize_text.py
python preprocessing/05_remove_stopwords.py
python analysis/check_pipeline_output.py      # sanity checks on the output (read-only)
python analysis/count_duplicates.py           # for the report

# Whole-corpus model (also creates the vectorizer every other model uses)
python modeling/07_fit_baseline_lda.py        # about 3 minutes
python modeling/08_display_lda_topics.py
python modeling/14_generate_topic_explorer.py
python analysis/09_test_lda_stability.py      # 5 seeds; under an hour

# Period models (after 07: they use its vectorizer)
for k in 8 11 15; do python modeling/15_fit_period_lda.py $k; done   # about 7 minutes
python analysis/16_seed_stability_periods.py  # 4 periods x 3 counts x 5 seeds = 60 fits; about 35 minutes
python modeling/17_generate_period_explorer.py
```

`01_extract_from_xml.py` accepts `[xml_dir] [output_dir]`; preprocessing scripts 02–05 and `07_fit_baseline_lda.py` accept `[input_dir] [output_dir]` to override the defaults.

## Tests

```bash
cd project

# Unit tests (about 10 seconds; synthetic examples only, no corpus, Stanza model or fitted models needed)
python -m unittest discover -s tests -v

# Sanity checks on the pipeline output after running 01-05 (about a minute; read-only)
python analysis/check_pipeline_output.py
```

- **`tests/test_preprocessing.py`** — HTML parsing (words split across spans are joined), character repair, title heading removal, motion number and author name removal, period boundaries, boilerplate matching on word forms (AUX `ska` dropped while the noun `skola` is kept), normalization, and the stopword list (lemma forms included; content words such as `skola`, `lärare`, `utbildning` excluded)
- **`tests/test_period_models.py`** — the period models:
  - **Loading:** the periods together hold exactly the motions of the whole-corpus model, in the same order, with the same skip rule
  - **Shared vocabulary:** every period model has the same vocabulary in the same order; a word absent from a period still has a column with only prior weight; a reordered vocabulary is rejected; adjacent periods can be matched. A mutation check (giving each period its own vectorizer) makes these tests fail
  - **Stability summary:** per-pair means, found-in-all/none and stable counts; one summary row per period and count
  - **Period explorer chains:** rows follow the Hungarian matches between adjacent periods (shuffled identical topics are linked correctly), a link below the threshold is reported as weak, and the seed-stability CSV is used only if its top words match the model
- **`tests/test_topic_matching.py`** — Hungarian matching on synthetic topic matrices: identical models match with cosine 1, a known permutation is recovered, mismatched or reordered vocabularies and mismatched topic counts are rejected, summary statistics equal the per-topic values
- **`tests/test_seed_stability.py`** — the seed-stability tests and the shared LDA code:
  - **Text loading:** body text only, motions without body text skipped, malformed lines counted
  - **No drift:** the model (07) and the stability test (09) use the very same functions from `lda_common.py`; no other script creates its own LDA model; the whole-corpus topic count is 4 × the period count; the reported seed is among the tested seeds
  - **Seeds:** the same seed reproduces the model exactly, a different seed changes it
  - **Planted topics:** on a synthetic corpus with three clearly separated topics, the full procedure finds cosine > 0.99 for every matched topic, so it can detect stability when it is there
  - **Report:** on a synthetic 5-seed, 44-topic setup, 10 pairs and 440 matched pairs; per-pair and pooled statistics equal those computed directly; the per-seed table and the notes on convergence and pooled statistics are present
- **`analysis/check_pipeline_output.py`** — for each stage that has been run: all four period files present, no malformed lines, required fields present, no `dok_id` twice, the same motions as extraction; no soft hyphens or broken diacritics after extraction; Stanza output well-formed; final text lowercase letters only with no digits, punctuation, single-character words or stopwords. Warns about empty texts and frequent known extraction fragments. Exit code 1 if any check fails. Optional argument: `[data_dir]`

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
│   ├── lda_common.py                     (shared settings, text loading)
│   ├── 07_fit_baseline_lda.py            (whole-corpus model + shared vectorizer)
│   ├── 08_display_lda_topics.py
│   ├── 14_generate_topic_explorer.py
│   ├── 15_fit_period_lda.py              (one model per period)
│   ├── 17_generate_period_explorer.py
│   ├── topic_explorer_template.html
│   └── period_explorer_template.html
├── analysis/
│   ├── topic_matching.py                 (Hungarian matching, cosine and Jaccard)
│   ├── seed_stability.py                 (shared seed-stability procedure and report)
│   ├── 09_test_lda_stability.py
│   ├── 16_seed_stability_periods.py
│   ├── check_pipeline_output.py          (sanity checks on pipeline output)
│   └── count_duplicates.py               (duplicate count for the report)
├── tests/
│   ├── test_preprocessing.py
│   ├── test_topic_matching.py
│   ├── test_seed_stability.py
│   └── test_period_models.py
├── config/
│   ├── boilerplate_phrases.txt
│   └── lemma_corrections.txt
├── docs/                                  (in git)
│   ├── PIPELINE_DOCUMENTATION.md          (this file: the current pipeline)
│   ├── PROGRESS_SEMINAR_1.md              (status, decisions and open questions, seminar 2026-10-19)
│   ├── MODEL_REVIEW.md                    (review of the first models on the Stanza pipeline)
│   ├── PREPROCESSING_ARTIFACTS.md         (the extraction artifacts and their fix)
│   └── reports/                           (seed-stability reports of 09 and 16; period_stability/ per period and count)
├── visualizations/                        (in git: topic_explorer.html, period_explorer.html)
├── results/                               (not in git: generated CSV tables)
├── data/                                  (not in git)
│   ├── input/extracted_text_xml/
│   └── output/{lemmatized,boilerplate_removed,normalized,stopword_removed}/
└── models/                                (not in git)
    ├── baseline_lda_32/
    └── period_lda_{8,11,15}/
```

## Open Points and Next Steps

1. **Vocabulary design** (global vs. Gordon's per-period vocabularies; seminar notes 2.2) and **place names** (keep, remove or downweight; 2.7)
2. **Algorithm and framing** (under discussion with the supervisor; seminar notes 0.4): the current plan is to keep scikit-learn and present the study as an adaptation of Gordon's workflow rather than a computational replication (MALLET, Gibbs sampling). If so, check convergence of the 50-pass fits (a 200-pass fit and a second seed)
3. **Alignment evidence:** Gordon's permutation null and z-scores for the period transitions (2.5)
4. **Rubric coding** (coherent, thematic, concentration) of the whole-corpus and period models (2.6), and a whole-corpus model with 8 topics as the counterpart of Gordon's k = 15 control
5. **Prominence analysis** with the whole-corpus model, restricted to stable topics (2.4)
6. **Checks:** the unstable *grades* topic (*mälardalens*, *ant*: possibly an artifact of a few motions); remaining small leftovers of the model review (`MODEL_REVIEW.md`); duplicates kept or dropped (2.10)
7. **Report writing**
