# Swedish Parliamentary Education Motions: NLP Pipeline

## Overview

13,957 motions to the Swedish parliament's Education Committee (Utbildningsutskottet, UbU), parliamentary sessions 1985/86–2025/26, processed into lemmatized body text and modelled with Latent Dirichlet Allocation (LDA), following the temporally binned design of Gordon (2026):

- **Four period models**, one per period (1985/86–1993/94, 1994/95–2005/06, 2006/07–2013/14, 2014/15–2025/26; complete electoral terms, see *Periods*), **8 topics each**, each with **its own vocabulary**, aligned across adjacent periods over their shared words into topic chains (as Gordon)
- **One whole-corpus model with 32 topics** (= 4 × 8, the same total capacity as the four period models together), as the point of comparison
- **Body text only.** Titles are processed and kept as a separate field, but are not part of the model's documents
- **Seed stability** is tested for every model (5 seeds, Hungarian matching)

Open questions are listed at the end; the seed-stability reports are in `reports/`.

All paths below are relative to `project/`. Documentation and reports are in `docs/` and the HTML visualizations in `visualizations/` (both in git); generated tables (CSV) are in `results/`, data in `data/` and fitted models in `models/` (not in git). The raw XML is in `../../swedish-parliament-data/`, next to the repository. Every script resolves its default paths from its own location, so scripts can be run from any working directory.

## Data Source

Motions (*motioner*) from **Riksdagens öppna data** (data.riksdagen.se), the Swedish parliament's open data portal, downloaded as XML datasets, one per span of years, and unpacked into `../../swedish-parliament-data/` (one XML file per document):

| Dataset (folder) | Files |
|---|---|
| `mot-1980-1989.xml` | 33,517 |
| `mot-1990-1997.xml` | 24,646 |
| `mot-1998-2001.xml` | 13,617 |
| `mot-2002-2005.xml` | 16,549 |
| `mot-2006-2009.xml` | 14,191 |
| `mot-2010-2013.xml` | 14,635 |
| `mot-2014-2017.xml` | 14,389 |
| `mot-2018-2021.xml` | 15,668 |
| `mot-2022-2025.xml` | 13,010 |
| **Total** | **160,222** |

- All motions to all committees; extraction keeps the 13,957 referred to the Committee on Education (UbU) in sessions 1985/86–2025/26 (see *Periods*). The earliest UbU motions are in `mot-1980-1989` (session 1985/86, from January 1986)
- The datasets are named by calendar years, but `mot-2022-2025` also holds session 2025/26, which ended in June 2026
- **Unpacked 2026-10-15; download date to be confirmed.** The portal's datasets are updated while a session is running, so a download before the end of session 2025/26 would hold fewer motions of that session. Re-downloading may also bring corrections to older documents; the file counts above identify the version used

## Pipeline Architecture

```
../../swedish-parliament-data/ (raw riksdag XML, as downloaded)
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
    └── modeling/07_fit_baseline_lda.py        → models/baseline_lda_32/ (whole-corpus model + its vectorizer)
            ├── modeling/08_display_lda_topics.py       → results/32_TOPICS_FINAL.csv
            ├── modeling/14_generate_topic_explorer.py  → visualizations/topic_explorer.html
            └── analysis/09_test_lda_stability.py       → docs/reports/BASELINE_STABILITY_32TOPICS.md
    └── modeling/15_fit_period_lda.py [k]       → models/period_lda_<k>/ (one model and vocabulary per period), results/period_<k>_topics.csv
            ├── modeling/17_generate_period_explorer.py → visualizations/period_explorer.html
            ├── analysis/16_seed_stability_periods.py   → docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md, results/period_stability/
            └── analysis/18_alignment_null.py           → docs/reports/PERIOD_ALIGNMENT_NULL.md
            (analysis/corpus_statistics.py: words and different words per step, for the report)
```

Every data stage stores one JSONL file per period: `group1_1985-1994.jsonl`, `group2_1994-2006.jsonl`, `group3_2006-2014.jsonl`, `group4_2014-2026.jsonl` (named after the calendar years the period's sessions span). Each stage adds fields and keeps earlier ones, so metadata (`dok_id`, session, title, date, author names) is carried through to the models. Every stage counts and reports malformed JSON lines per period, so no data is lost silently.

**Why this order:** Stanza is the only slow step, so it runs once, right after extraction, and saves every word with its original form, lemma and part of speech. Everything after it works from that saved output and takes minutes, so the boilerplate list and stopwords can be changed and re-run without running Stanza again.

### Periods (`periods.py`)

The four periods are defined once, in `periods.py`, and imported by every script. They follow **complete electoral terms** (mandatperioder), grouped so that the periods are as equal in size as the terms allow:

| Period | Sessions | Electoral terms beginning | UbU motions |
|---|---|---|---|
| 1 | 1985/86–1993/94 | 1985, 1988, 1991 | 4,029 |
| 2 | 1994/95–2005/06 | 1994, 1998, 2002 | 3,477 |
| 3 | 2006/07–2013/14 | 2006, 2010 | 2,879 |
| 4 | 2014/15–2025/26 | 2014, 2018, 2022 | 3,572 |

- **Why electoral terms:** a period then covers whole terms of the Riksdag and its governments, so no term is split between two periods. Of the possible groupings of the 11 terms into four consecutive periods, this one has the most even sizes (largest / smallest = 1.40)
- **Assigned by session, not by date:** a motion belongs to the period of its parliamentary session (riksmöte, XML field `rm`, e.g. `1993/94`; session 1999/2000 is written with four digits). The session is the unit of parliamentary work, and some motions carry a placeholder date (motions of 1985/86 dated 1985-01-01)
- **Coverage:** the first session in the data is 1985/86, but UbU motions start in January 1986 (motions of autumn 1985 are not tagged with the committee); the last period runs to the end of session 2025/26, the last session before the 2026 election
- Pages and reports name the periods by their sessions (1985/86–1993/94); file and model names use the calendar years (`1985-1994`)

**Titles** go through exactly the same steps as the body text, in the same scripts (fields prefixed `title_`). The final title (`title_processed`) is kept in the data for later use (e.g. labelling topics).

## Processing Steps

### 1. Extraction (`extraction/01_extract_from_xml.py`)
- **Input:** the XML files of the motion datasets (see *Data Source*), searched recursively (default `../../swedish-parliament-data/`; another location can be passed as the first argument)
- **Method:** follows Bruinsma & Johansson (2024)
- **Filter:** UbU committee (`organ` field), case-insensitive
- **Extract:** dok_id, date, title, author names, body text (between the introduction and signature markers); HTML entities decoded
- **HTML to text:** text pieces are joined without separators, with whitespace only at block-level tags (`<p>`, `<br>`, `<td>`, headings, …). The source HTML often splits single words across inline `<span>`s (`uppföljni</span><span>ng`, and in some motions every å/ä/ö is its own span), so joining with spaces would fragment words
- **Character repair (body and title):** soft hyphens (U+00AD) removed; text NFC-normalized; spacing diacritics after a base letter replaced (`a°` → `å`, `a¨` → `ä`, `o¨` → `ö`)
- **Title heading removed:** the title appears as a heading near the start of the body in ~97% of motions. The first word-by-word match of the title within the first 400 characters is removed, so the body holds the motion's own text. Later mentions of the title phrase (e.g. in the proposed decision) are kept
- **Metadata removed (body and title):** motion numbers (`1989/90:Ub742`, `GE02A1`) and the motion's own author names (from the XML author list, whole-word, case-insensitive). Done before Stanza, so numbers are not split into odd tokens and names are not lemmatized
- **Period:** assigned from the motion's session (`rm`), see *Periods*
- **Output:** 13,957 motions in `data/input/extracted_text_xml/`. Fields: `session`, `text` (cleaned body), `title` (original title, for display), `title_text` (cleaned title, for processing). The files are JSONL; the folder name means "text extracted from XML"

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
- **Lemma corrections:** known Stanza lemma errors are corrected from `config/lemma_corrections.txt` (`kompet` → `kompetens`, `lärosät` → `lärosäte`, `anslagen` → `anslag`, …). Stanza guesses lemmas for words it has not seen in training, and some guesses are truncated; the list corrects the errors found by inspecting the models, it does not replace the lemmatizer
- **Output fields:** `text_no_boilerplate`, `title_no_boilerplate`

### 4. Normalization (`preprocessing/04_normalize_text.py`)
- Lowercase, remove numbers and punctuation, collapse whitespace
- Drops single-character words; preserves line breaks
- **Output fields:** `text_normalized`, `title_normalized`

### 5. Stopword Removal (`preprocessing/05_remove_stopwords.py`)
- **Base list:** NLTK Swedish stop words (114)
- **Supplementary (85, hard-coded):** parliamentary abbreviations (ub, dvs, osv, …), auxiliary verbs (ska, skall, blir, …), generic connectors, verbs and adjectives identified from LDA inspection (kommer, enligt, olika, göra, …), and the **lemma forms** of inflected entries (behöva, vilja, kunna, ny, stor, olik, mången, …), since the text is lemmatized. Content abbreviations such as `fn`, `eg`, `ky`, `ib` are deliberately not stopwords (education-policy terms)
- **Output fields:** `text_no_stopwords` (final body text, used by the models) and `title_processed` (final title text)

### Duplicate count (`analysis/count_duplicates.py`) — for the report, not a pipeline step
- Models use all motions; duplicates are not removed
- MD5 hash of the whitespace-normalized final text; one hash dictionary across all periods, so duplicates are found across periods. Prints duplicates per period, the total and each duplicate → original `dok_id`; writes no data
- The count depends on the final text, so re-run it after changing the boilerplate or stopword lists
- **Current result: 515 duplicates of 13,957 motions (3.69%)**; per period 11 / 31 / 154 / 319
  - Almost all are the **same motion resubmitted in a later session**, e.g. *Forskningsreaktor i Oskarshamn* 2015–2017. Motion numbers and author names are removed at extraction, so a resubmitted motion is identical to its original
  - Most are full-length texts (307 copies over 100 words, 200 of 21–100 words); 8 are near-empty bodies
  - A resubmitted motion counts once per year it was submitted, which weights recurring proposals in prominence; whether to keep them is open

## Models

### Shared settings (`modeling/lda_common.py`)
Topic counts (`NUM_TOPICS = 32`, `PERIOD_TOPICS = 8`), the model folder name (`BASELINE_MODEL_DIR`), the vocabulary rule of every model (`VECTORIZER_PARAMS`), LDA settings, the reported seed (42), the stability seeds (42, 123, 456, 789, 999) and text loading live in this one module. Every model, stability test and explorer imports them from there, so the stability tests always measure the same models that are reported. A test checks that no other script creates its own LDA model.

- **LDA:** scikit-learn `LatentDirichletAllocation`, `learning_method='online'`, `max_iter=50`, `random_state=42`, `n_jobs=2`; symmetric default priors
- **No convergence check:** with online learning and sklearn's default `evaluate_every=-1`, every fit runs exactly 50 passes. The motions are processed in mini-batches of 128 (about 109 updates per pass) with a step size that decays with every update, so topics stop changing towards the end whether or not they have converged. The iteration count in the reports (always 50) confirms the setting, not convergence
- **Input:** `text_no_stopwords` (body text only). Motions with no body text left after preprocessing are skipped (4 motions), so the models use 13,953 motions (per period 4,025 / 3,477 / 2,879 / 3,572)
- **Diagnostic:** training perplexity, reported as a diagnostic only, not evidence of generalization

### Whole-corpus model (`modeling/07_fit_baseline_lda.py`)
- **Vectorizer:** `CountVectorizer(min_df=10, max_df=0.5)`, default token pattern: the same rule as the period models (`VECTORIZER_PARAMS` in `lda_common.py`; Gordon 2026, 3.3), applied to all motions: words in at least 10 and at most 50% of the motions, no cap on the vocabulary size. 15,962 words. The vocabulary of the whole-corpus model, its stability test and the topic explorer
- **Model:** 32 topics
- **Output:** `models/baseline_lda_32/baseline_lda_32_topics.pkl`, `models/baseline_lda_32/baseline_vectorizer.pkl`, and `results/document_topic_distribution.csv` (doc_id, title, year, session, period and the probability of every topic for every motion, for prevalence analysis)
- *Baseline* in script and file names means the whole-corpus model

### Period models (`modeling/15_fit_period_lda.py [k]`)
- One model per period, 8 topics each (`k` overrides the count), with the shared LDA settings
- **Vocabulary per period, as Gordon (2026, 3.3):** each period's vectorizer is built on that period's motions only, keeping words in at least 10 and at most 50% of them, with no cap on the vocabulary size (`VECTORIZER_PARAMS`, `fit_period_vectorizer()` in `lda_common.py`; the whole-corpus model uses the same rule over all motions). Vocabularies: 7,302 / 7,981 / 4,926 / 6,876 words. Each period model is built on its own most relevant words: a word typical of one period is not crowded out by frequencies over 40 years, and a word frequent in one period is excluded only there
- **Output:** `models/period_lda_<k>/` (per period: the model, its vectorizer and `vocabulary_<period>.txt`), `results/period_<k>_topics.csv` (top 20 words per topic and period). k = 8 (`PERIOD_TOPICS`); another count can be passed to reproduce the topic-count choice

### Topic matching (`analysis/topic_matching.py`)
Hungarian-algorithm one-to-one matching between two models' topics on cosine similarity over the full topic-word distributions, with Jaccard overlap of the top words as a secondary measure. Used for seed stability (matching models with different seeds) and for alignment across periods (matching adjacent periods). One-to-one matching cannot represent a topic splitting or merging.

- **Seed stability:** the models share one vectorizer; cosine is computed over the full, identical vocabularies, and different or reordered vocabularies are an error
- **Adjacent periods (`shared_vocabulary=True`), as Gordon (2026, 3.4):** cosine over the words both periods' vocabularies contain (4,236–5,464 words per transition), put in the same order. Cosine does not depend on the scale of the vectors, so this equals Gordon's cosine on L2-normalized distributions over the shared words. Words outside the intersection do not count: so that vocabulary change is not hidden, the share of each topic's weight outside the shared words is reported (*Current Results*)

## Seed-Stability Testing

| Script | Tests | Output |
|---|---|---|
| `analysis/09_test_lda_stability.py` | The whole-corpus model | `docs/reports/BASELINE_STABILITY_32TOPICS.md`, `results/BASELINE_STABILITY_32TOPICS_PER_TOPIC.csv` |
| `analysis/16_seed_stability_periods.py [k ...]` | The period models (default 8; `8 11 15` reproduces the topic-count choice) | `docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md`; full report per period in `docs/reports/period_stability/`; per-topic CSV in `results/period_stability/` |

Both use the shared procedure in `analysis/seed_stability.py`: fit one model per seed (5 seeds), match every pair of models with the Hungarian algorithm (10 pairs), and compare matched topics by cosine (full distributions) and Jaccard (top 20 words).

**Reports** list, per seed, the training perplexity and iteration count; then the **stability per topic** of the reference model (seed 42, the seed of the reported model); then cosine and Jaccard statistics for each of the 10 seed pairs; then pooled statistics over all matched topic pairs.

**Stability per topic:** each topic of the seed-42 model is compared with its matched topic in each of the other 4 models. A topic is *found* in a model if the matched cosine is at least 0.70 (a judgement call, `seed_stability.FOUND_COSINE`), and *stable* if found in at least 3 of the 4. The table gives its top words, the number of models it is found in, and its mean and minimum cosine and mean Jaccard. The seed-42 model is fitted on the same data with the same settings as the reported model, so its topic numbers are those of the reported model. Use this to decide which topics to interpret with confidence.

**Pooled statistics:** the matched topic pairs are not independent (each seed's model appears in 4 of the 10 pairs). The pooled mean is a fair summary, but the pooled standard deviation understates the uncertainty; for the spread across runs, report the 10 per-pair means or their range.

## Current Results

### Whole-corpus model (32 topics)
Report: `docs/reports/BASELINE_STABILITY_32TOPICS.md`. Vocabulary: the same rule as the period models (15,962 words).

| | 32 topics |
|---|---|
| Mean cosine (mean of the 10 per-pair means) | 0.549 |
| Range of the 10 per-pair means | 0.496–0.621 |
| Mean Jaccard (top 20) | 0.253 (per-pair 0.20–0.30) |
| Seed-42 topics found in 4 / 3 / 2 / 1 / 0 of the other 4 models | 3 / 8 / 4 / 4 / 13 |
| Stable (3–4 of 4) | 11 of 32 (34%) |
| Training perplexity, 5 seeds | 1987–2014 |

- **Found in all four other models (3):** compulsory school, teaching and goals (mean cosine 0.96), municipalities and independent schools (0.92), research and universities (0.90). **In 3 of 4 (8):** teachers and teacher education (0.86), society, democracy and curriculum (0.84), physical activity and sport (0.84), language and international (0.79), preschool (0.76), students and adult education (0.74), higher-education places and funding (0.72), children, families and sign language (0.59)
- **Found in no other model (13):** some clear themes whose words other seeds spread over other topics (youth and mental health 0.40, food and home economics 0.58, Swedish and SFI 0.46, research and the EU 0.50, profit and private providers 0.36, vocational and apprenticeship education 0.30, national minorities 0.16), and residual topics of unrelated words or place names (*lund, kalmar, professur*; *ersättning, alliansregering, merkostnad*; *hbt, adhd, folkmord*; *it, digitalisering, utanförskap*; *vinstdrivande, musik, uf*; *utgiftsområde, vetenskapsråd, riksrevision*; 0.02–0.26), probably held together by a few motions
- **Use:** prominence trends and any mapping of period topics onto whole-corpus topics should rely on the stable topics, or report the range over seeds

### Period models
Report: `docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md`.

| Period | Mean cosine | Stable (3–4 of 4) |
|---|---|---|
| 1985/86–1993/94 | 0.74 | 4 of 8 (50%) |
| 1994/95–2005/06 | 0.78 | 6 of 8 (75%) |
| 2006/07–2013/14 | 0.76 | 6 of 8 (75%) |
| 2014/15–2025/26 | 0.77 | 5 of 8 (62%) |
| **All periods** | | **21 of 32 (66%)** |

- The period models are more stable than the whole-corpus model, with the same vocabulary rule. Part of the difference is the topic count: at 15 topics per period (topic-count test, one global vocabulary for all periods) 42% of the period topics were stable, close to the whole-corpus model's 34%. The comparison supports Gordon's case for period models only together with the choice of 8 topics
- The first period is exactly at half stable; the smallest period (2006/07–2013/14) is not less stable than the others
- **How 8 was chosen:** see *Design Decisions*

**Alignment across periods (8 topics):** matched mean cosine 0.67, 0.78 and 0.76 for the three transitions. All 8 chains hold by Gordon's criterion (mean link ≥ 0.50), 4 of them with every link ≥ 0.50: upper secondary school, pupils and teachers (mean link 0.85), higher education and research (0.82), municipalities and independent schools (0.79), and children, health and bullying (0.63). The other four hold on the mean but have one weak link: preschool (0.498 at the first link, just below the threshold, then 0.94 and 0.95), research (0.42 at the last link), higher education turning into labour market (0.32) and students (0.36).

**Permutation test (Gordon's, `analysis/18_alignment_null.py`; report `docs/reports/PERIOD_ALIGNMENT_NULL.md`):** for each transition, the matched mean cosine is compared with 1,000 random one-to-one pairings of the same topics; z = (matched − null mean) / null SD, p one-sided from the standard normal distribution, as Gordon.

| Transition | Matched | Null mean (SD) | z |
|---|---|---|---|
| 1985/86–1993/94 → 1994/95–2005/06 | 0.668 | 0.348 (0.076) | 4.2 |
| 1994/95–2005/06 → 2006/07–2013/14 | 0.782 | 0.347 (0.080) | 5.4 |
| 2006/07–2013/14 → 2014/15–2025/26 | 0.755 | 0.354 (0.071) | 5.6 |

- Every transition is far above chance (p < 0.0001): the alignment shows continuity, not forced matches. It does not show that every single link is the same theme
- The z-scores are lower than Gordon's 7–9 although the matched cosines are higher: with 8 topics the mean of a random pairing varies more than with 15 (larger null SD), and the null mean is higher (0.35 against his 0.22–0.25), since 8 broad topics share more general education vocabulary
- The first transition is the weakest, as in the chains (two of the four weak links are at the first transition)
- **Against the seed-stability ceiling:** the period models' mean seed cosine is 0.74–0.78. The second and third transitions (0.78, 0.76) are at that level, so across them the topics change no more than between seeds of one period; the first transition (0.67) is below it. Seed cosine is over the full vocabulary and alignment over shared words, so the comparison is approximate

**Vocabulary outside the shared words:** on average 3.5–9.8% of a topic's weight falls on words outside the vocabulary it shares with the neighbouring period (range per topic 2.4–12.9%). The share is highest for the first period against the second (9.8%) and for the last against the third (7.8%).

### Comparison with Gordon (2026)

*Tracing Thematic Change in Early English-Language Science Fiction, 1818–1930* (`../../swedish-parliament-instructions/tracing_thematic_change.pdf`).

| | Gordon | This study |
|---|---|---|
| Whole-corpus seed stability (mean Jaccard of the top words) | 0.26–0.31 | 0.253, per-pair range 0.20–0.30 (32 topics) |
| Matched mean cosine between adjacent periods, 8 topics per period | — | 0.67, 0.78, 0.76 |
| Same, at Gordon's 15 topics per period (fitted once for this comparison) | 0.44–0.59 | 0.43, 0.60, 0.62 |
| Chains with mean cosine ≥ 0.50 over the three transitions | 7 of 15 | 8 of 8 (8 topics); 9 of 15 at 15 topics |
| Permutation test: null mean, z (per transition) | 0.22–0.25, z = 7–9 (15 topics) | 0.35, z = 4.2–5.6 (8 topics) |

- **Seed instability is of the same size as Gordon's** (slightly below his range on average), so it is not a weakness of this pipeline; Gordon uses the same finding as part of his argument for period models
- **At Gordon's topic count (15 per period), with his vocabulary design, the alignment is close to his:** matched cosine in the same range, and a few more chains pass his criterion (9 against 7). At 8 topics the links are stronger, as expected with fewer, broader topics
- Different corpora and algorithms: the agreement shows results of the same order, not equivalent methods

| Point | Gordon | This study | Assessment |
|---|---|---|---|
| Algorithm | MALLET, Gibbs sampling, 1,000 iterations, asymmetric hyperparameter optimization every 10 iterations | scikit-learn, online variational Bayes, 50 passes, symmetric priors | Probably the largest difference; convergence not checked |
| Vocabulary | Per period (≥ 10 documents, ≤ 50%), adjacent periods compared over their shared words | The same; the whole-corpus model uses the same rule over all motions (15,962 words) | Followed |
| Author signal | Authorless preprocessing (MALLET `DownsampleLabelWords`) | None | Counterpart here: MP/constituency signal (place names) |
| Documents | 1,000-word book chunks | Whole motions | Natural units, most shorter than 1,000 words |
| Proper names | Removed | Kept | Open |
| Lemmatization | None | Stanza | Swedish inflection |
| Topics | 15 per period, 60 whole corpus | 8 per period, 32 whole corpus | Chosen by seed stability (8, 11 and 15 tested) |
| Seed stability | Whole-corpus runs only | Every model | Extension |

**Not yet comparable:** the rubric coding (coherent, thematic, concentration) of all models, and a whole-corpus model with 8 topics (the counterpart of Gordon's k = 15 control).

## Visualizations

| Script | Reads | Writes |
|---|---|---|
| `modeling/08_display_lda_topics.py [model_dir]` | `models/baseline_lda_32/` | `results/32_TOPICS_FINAL.csv` (top 20 words per topic, as P(word \| topic)) |
| `modeling/14_generate_topic_explorer.py` | `models/baseline_lda_32/`, `data/output/stopword_removed/`, `config/topic_names_32.tsv`, template `modeling/topic_explorer_template.html` | `visualizations/topic_explorer.html` |
| `modeling/17_generate_period_explorer.py` | `models/period_lda_8/` (models and vectorizers), `data/output/stopword_removed/`, the per-topic CSVs of 16, `config/period_topic_names_8.tsv`, `config/chain_names_8.tsv`, template `modeling/period_explorer_template.html` | `visualizations/period_explorer.html` |

Both pages are self-contained HTML (open in a browser; internet needed only for the fonts). Word weights are shown as P(word | topic). Topics have Swedish names, an interpretation of each topic's top words and top motions: `config/topic_names_32.tsv` for the whole-corpus model (*Restämne* marks residual topics: unrelated words held together by a few motions) and `config/period_topic_names_8.tsv` for the period models, one name per period topic (*Blandat* marks broad topics without one clear theme). A name is shown only if the topic's three most probable words still match the file (`load_topic_names()` in `lda_common.py`), so a refitted model gets no wrong names. Named topics and chains are shown without their numbers.

### Topic explorer (whole-corpus model)
- **Per topic, two columns:** the word cloud (top 20 words, as in the period explorer, the topic tables and the seed-stability comparison) with the share-by-period chart under it on the left; the top 10 motions (session, party, id, θ) on the right; stacked on narrow screens. The heading gives the overall share; the party concentration among these 10 motions is shown next to “Top motions” (gold when 8 or more share the first signatory's party; renamed parties count as one: FP = L, KDS = KD, VPK = V). Parties are shown by name: the chip under today's name, each motion under the name at the time
- **Word size:** square root of P(word | topic), on **one scale for all clouds**, so sizes can be compared between topics; if a word does not fit, all clouds shrink together. A topic spread over many words has a smaller, sparser cloud. The tooltip gives the exact probability
- **Order:** largest overall share first (topic numbers are arbitrary); no sorting or search controls and no explanation block on the page; this section describes what it shows

### Period explorer (period models)
- **8 topics per period,** the chosen count
- **Rows are chains.** The page has no explanation block; this section describes what it shows. Each period model has its own topics, so topic numbers do not correspond across periods. Topics of adjacent periods are matched one-to-one (Hungarian algorithm on cosine over the words both periods' vocabularies contain) and each row follows the matches from a topic of the first period to the last The chains have Swedish names from `config/chain_names_8.tsv`, shown only if the chain still consists of the same four topics
- **Chain heading:** the chain's name (no chain number) and the mean of its three links (*Average similarity*; Gordon's criterion: the chain holds if it is at least 0.50); no continuity label, weakest link or link summary, since the weak links are visible in the row. The similarity has two decimals, or three where two would round across 0.50
- **Weak links (additional information):** a single link below 0.50 breaks the row: the accent bar over the clouds stops, a dashed gold rule separates the cells and the cell reads *Alignment uncertain*. A chain can hold on the mean and still have one weak link
- **Per cloud:** the period, the topic's name (its number in the period model only in the tooltip), its share in percent (mean θ over the period's motions; explained in the introduction). Seed stability is not shown on the page; it is reported in `docs/reports/period_stability/` and *Current Results*. The cosine of each link is not shown: a link is either strong or weak (below 0.50), and a weak one is marked in the row
- **Word colour = persistence within the chain:** in how many of the chain's four periods the word is among the top 20 words (the words shown): dark blue all four, medium blue three, light blue two, grey one. With 8 topics, 15% of the words shown are in all four periods and 41% in only one. Bold marks the three most probable words of each cloud
- **Word size:** square root of P(word | topic), on **one scale per chain**, so sizes can be compared across a chain's periods but not between chains; if a word does not fit, the chain's four clouds shrink together. The tooltip gives the exact probability
- **Order:** strongest chain first (mean link, high to low, ties by the weakest link); no sorting or search controls
- **Limitations:** the matching gives every topic a partner, so a topic that exists in only one period still sits in a chain, joined by weak links, and a topic that appears in a later period cannot start its own row. The permutation test (`18_alignment_null.py`) shows that each transition is far above chance, not that every link is the same theme

## Design Decisions

- **Stopwords vs. boilerplate.** Stopwords are general Swedish words, applied to the lemmatized, normalized text; boilerplate is parliamentary and domain-specific language (institutions, procedure, references), matched on the original word forms. Keeping them apart lets the stopword list be reused for other Swedish texts
- **Stanza lemmatization.** Swedish inflection splits one word into many forms (*skola, skolan, skolor, skolornas*), which fragments topics. Stanza is a general, context-aware lemmatizer run once on full sentences, with a small table of corrections for known errors. Known trade-offs: comparatives are reduced to the positive (*högre utbildning* → `hög utbildning`), rare compounds can get wrong lemmas (*arbetsvillkor* → `arbetsvillka`), and modal *ska* gets the lemma `skola` (handled by dropping auxiliaries). spaCy's `sv_core_news_sm` and a hand-made lookup table of education terms were tried and rejected
- **Body text only.** Appending the title 3× or 5× to the body gave only a small stability gain (mean matched cosine 0.539 against 0.525 at 44 topics, overlapping ranges), too small to justify an extra modelling choice. Titles are kept in the data
- **Topic count: 8 per period, 32 for the whole corpus.** 8 is the only tested count (8, 11, 15) at which at least half of the topics are stable in every period, and it has the highest mean cosine in every period; since the number of robust themes is about the same at every count, 8 loses little substance and avoids many chance topics. The margin is small in the first and last periods (exactly half stable). The test (16 with `8 11 15`; reports in `docs/reports/topic_count_choice/`):

  | Period | 8 topics: mean cosine / stable | 11 topics | 15 topics |
  |---|---|---|---|
  | 1985/86–1993/94 | 0.70 / 4 of 8 (50%) | 0.63 / 4 of 11 (36%) | 0.55 / 4 of 15 (27%) |
  | 1994/95–2005/06 | 0.77 / 7 of 8 (88%) | 0.67 / 6 of 11 (55%) | 0.62 / 6 of 15 (40%) |
  | 2006/07–2013/14 | 0.80 / 6 of 8 (75%) | 0.65 / 4 of 11 (36%) | 0.58 / 6 of 15 (40%) |
  | 2014/15–2025/26 | 0.72 / 4 of 8 (50%) | 0.67 / 6 of 11 (55%) | 0.62 / 9 of 15 (60%) |
  | **All periods** | **21 of 32 (66%)** | **20 of 44 (45%)** | **25 of 60 (42%)** |

  The number of robust themes per period is about 4–9 at every count (8 → 15 adds 28 topics but only 4 stable ones), and the mean cosine falls with the topic count in every period. The test was run with one global vocabulary for all periods; with the per-period vocabularies the 8-topic models are as stable (21 of 32), and 11 and 15 were not re-tested. The 11- and 15-topic models are not kept; they can be refitted with `15_fit_period_lda.py <k>`. The whole-corpus model has the same total capacity as the four period models, as in Gordon (60 = 4 × 15)
- **Periods by electoral term, assigned by session** (see *Periods*): whole terms per period, as equal in size as the terms allow. Compared with four calendar-year bins of roughly equal size (1986–1993, 1994–2004, 2005–2014, 2015–2025, assigned by date), the period models at 8 topics are slightly more stable (21 against 19 of 32 topics stable) and the alignment stronger (all 8 chains pass Gordon's criterion, against 5). The differences are small
- **Vocabulary per period, compared over shared words** (Gordon's method; see *Period models* and *Topic matching*). Compared with one global vocabulary for all periods, stability is the same at 8 topics (21 of 32 topics stable) and the alignment stronger (matched mean cosine 0.67, 0.78, 0.76 against 0.65, 0.69, 0.67; all 8 chains hold in both), as expected when words outside the shared vocabulary do not count
- **Whole-corpus vocabulary by the same rule:** words in at least 10 and at most 50% of all motions, no cap (15,962 words), as the period models, so that the two designs differ only in the time split and the topic count
- **Chain criterion:** Gordon's mean of the three links ≥ 0.50, so results are comparable with his; single weak links are shown as additional information

## Configuration Files

- **`config/boilerplate_phrases.txt`:** 440 explicit words/phrases, one per line, grouped by category with `#` headers. Matched against original word forms (body and title). An alternative file can be passed as the 3rd argument to `03_remove_boilerplate.py`. After editing, re-run steps 03–05 (no need to re-run Stanza)
- **`config/lemma_corrections.txt`:** corrections for known Stanza lemma errors, one `wrong correct` pair per line with `#` comments, applied in step 03 to body and title, case-insensitively. A wrong lemma with a leading `*` is also corrected at the end of a compound (`*kompet kompetens`: `gymnasiekompet` → `gymnasiekompetens`); mark an entry only after checking its compounds (`anslagen` must not be marked, because of *sammanslagen*). After editing, re-run steps 03–05
- **Stopwords:** hard-coded in `preprocessing/05_remove_stopwords.py` (NLTK base + supplementary list, including lemma forms)

## Corpus Size per Step

Body text of all 13,957 motions (`analysis/corpus_statistics.py`, read-only). Words are Stanza's tokens throughout, so every step is counted the same way: step 02 runs Stanza on the extracted text, so its word forms are the extracted text as Stanza splits it. A word is a token with at least one letter (punctuation and pure numbers are not counted); different words are counted case-insensitively.

| Step | Words | Different words | Words per motion (median / mean) |
|---|---|---|---|
| 01 Extraction (word forms) | 10,360,566 | 137,918 | 383 / 742 |
| 02 Lemmatization (lemmas) | 10,360,566 | 96,875 | 383 / 742 |
| 03 Boilerplate removed | 8,800,067 | 95,956 | 325 / 631 |
| 04 Normalized | 8,494,260 | 84,342 | 313 / 609 |
| 05 Stopwords removed (final text) | 4,622,680 | 84,176 | 169 / 331 |
| Whole-corpus model vocabulary | 4,058,083 | 15,962 | 147 / 291 |
| Period models' vocabularies (together) | 3,899,123 | 11,661 | – |

- **Extraction:** Stanza keeps punctuation inside and next to some tokens, so the extracted text has spelling variants of the same word among its different words: abbreviations (*t.ex.*, *bl.a.*, *mot.*), party letters from "(m)" (*m)*, *s)*), and compound ellipsis (*läs-* in "läs- och skrivförmåga"). Steps 03 and 04 remove them
- **Lemmatization** reduces the number of different words by 30% (137,918 word forms to 96,875 lemmas) without removing any words: each word is replaced by its lemma (*skolan*, *skolorna*, *skolor* → *skola*), so word forms and lemmas are the same tokens and have the same count
- **Boilerplate removal** (with auxiliaries and multi-word abbreviation lemmas) removes 15% of the words but few different ones: the removed words are a small set of frequent parliamentary phrases
- **Normalization** removes digits, turns punctuation inside tokens into spaces (hyphenated lemmas are split: *it-kompetens* → *it*, *kompetens*; *1990-talet* → *talet*) and drops single characters: −3% words, −12% different words
- **Stopword removal** halves the number of words (−46%) but removes only 166 different words: stopwords are few and very frequent
- **The models' vocabularies** keep 84–88% of the final words (whole corpus: 15,962 of 84,176 different words, 88% of the words); most of the 84,176 are rare. Per period: 1,052,497 / 1,263,414 / 571,556 / 1,011,656 words in vocabularies of 7,302 / 7,981 / 4,926 / 6,876 different words

## Data Summary

| Metric | Value | Note |
|--------|-------|------|
| Motions | 13,957 | All UbU motions, sessions 1985/86–2025/26; 13,953 with body text are modelled |
| Periods | 4 | 1985/86–1993/94, 1994/95–2005/06, 2006/07–2013/14, 2014/15–2025/26 (2,879–4,029 motions each) |
| Duplicates | 515 (3.69%) | Mostly resubmissions in later years; kept |
| Vocabulary | Period models: 4,926–7,981 per period; whole-corpus model: 15,962 | ≥ 10 and ≤ 50% of the model's motions, no cap (Gordon) |
| Stopwords | NLTK (114) + 85 supplementary | |
| Boilerplate phrases | 440 | Explicit phrases, no wildcards |
| Lemmatizer | Stanza | Swedish Talbanken model; auxiliaries dropped |
| LDA topics | 8 per period, 32 whole corpus | 8, 11 and 15 per period tested |
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
python analysis/corpus_statistics.py          # words per step, for the report (a few minutes; after 15)
python analysis/word_lists_latex.py           # stopword and boilerplate lists as LaTeX tables (docs/tables/)

# Whole-corpus model
python modeling/07_fit_baseline_lda.py        # about 3 minutes
python modeling/08_display_lda_topics.py
python modeling/14_generate_topic_explorer.py
python analysis/09_test_lda_stability.py      # 5 seeds; under an hour

# Period models (each with its own vocabulary; independent of 07)
python modeling/15_fit_period_lda.py          # 8 topics; about 2 minutes
python analysis/16_seed_stability_periods.py  # 4 periods x 5 seeds = 20 fits; about 10 minutes
                                              # (with 8 11 15: the topic-count choice, about 35 minutes)
python modeling/17_generate_period_explorer.py
python analysis/18_alignment_null.py          # permutation test; seconds
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

- **`tests/test_preprocessing.py`** — HTML parsing (words split across spans are joined), character repair, title heading removal, motion number and author name removal, periods by session (boundaries, the four-digit 1999/2000, invalid sessions, a placeholder date), boilerplate matching on word forms (AUX `ska` dropped while the noun `skola` is kept), normalization, and the stopword list (lemma forms included; content words such as `skola`, `lärare`, `utbildning` excluded)
- **`tests/test_period_models.py`** — the period models:
  - **Loading:** the periods together hold exactly the motions of the whole-corpus model, in the same order, with the same skip rule; each motion's metadata carries its session and period; periods are shown by their sessions
  - **Vocabulary per period:** each vocabulary holds exactly the words of its period that pass Gordon's limits (a word in 12 of 40 motions kept, in one dropped, in more than half dropped); a word of one period only is absent from the others; adjacent periods have different vocabularies and are matched over their shared words, and matching them without that step is an error
  - **Stability summary:** per-pair means, found-in-all/none and stable counts; one summary row per period and count
  - **Period explorer chains:** rows follow the Hungarian matches between adjacent periods (shuffled identical topics are linked correctly), and a link below the threshold is reported as weak
- **`tests/test_topic_matching.py`** — Hungarian matching on synthetic topic matrices: identical models match with cosine 1, a known permutation is recovered, mismatched or reordered vocabularies and mismatched topic counts are rejected, summary statistics equal the per-topic values. **Permutation null:** a clear matching is far above the null (null mean 0.1 + 0.8/n for a diagonal of 0.9, as expected from one fixed point per random permutation), the matched mean uses the Hungarian matching, a matrix without structure gives z = 0, z and p follow the formula, results are reproducible with a seed. **Shared vocabulary:** the same topics in different vocabularies (other column order, extra words) match with cosine 1; weight on words outside the intersection does not change the cosine; vocabularies without common words are rejected
- **`tests/test_seed_stability.py`** — the seed-stability tests and the shared LDA code:
  - **Text loading:** body text only, motions without body text skipped, malformed lines counted
  - **No drift:** the model (07) and the stability test (09) use the very same functions from `lda_common.py`; no other script creates its own LDA model; the whole-corpus topic count is 4 × the period count; the reported seed is among the tested seeds
  - **Seeds:** the same seed reproduces the model exactly, a different seed changes it
  - **Planted topics:** on a synthetic corpus with three clearly separated topics, the full procedure finds cosine > 0.99 for every matched topic, so it can detect stability when it is there
  - **Report:** on a synthetic 5-seed, 44-topic setup, 10 pairs and 440 matched pairs; per-pair and pooled statistics equal those computed directly; the per-seed table and the notes on convergence and pooled statistics are present
- **`tests/test_corpus_statistics.py`** — the corpus size per step on two hand-worked motions: what counts as a word (no punctuation or pure numbers), different words counted case-insensitively, lemmatization keeping the number of words while merging forms (*skolan*, *skolorna* → *skola*), one lemma counted per word form even when the lemma has no letter (*6:e* → *6:*), the counts after boilerplate, normalization and stopwords, and the words inside the models' vocabularies
- **`analysis/check_pipeline_output.py`** — for each stage that has been run: all four period files present, no malformed lines, required fields present, no `dok_id` twice, the same motions as extraction; every motion in the period of its session; no soft hyphens or broken diacritics after extraction; Stanza output well-formed; final text lowercase letters only with no digits, punctuation, single-character words or stopwords. Warns about empty texts and frequent known extraction fragments. Exit code 1 if any check fails. Optional argument: `[data_dir]`

## File Organization

```
project/
├── periods.py                            (the four periods, by session)
├── extraction/
│   └── 01_extract_from_xml.py
├── preprocessing/
│   ├── 02_lemmatize.py
│   ├── 03_remove_boilerplate.py
│   ├── 04_normalize_text.py
│   └── 05_remove_stopwords.py
├── modeling/
│   ├── lda_common.py                     (shared settings, text loading)
│   ├── 07_fit_baseline_lda.py            (whole-corpus model + its vectorizer)
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
│   ├── 18_alignment_null.py               (Gordon's permutation test of the alignment)
│   ├── check_pipeline_output.py          (sanity checks on pipeline output)
│   ├── count_duplicates.py               (duplicate count for the report)
│   ├── corpus_statistics.py              (words and different words per step, for the report)
│   └── word_lists_latex.py               (stopword and boilerplate lists as LaTeX tables)
├── tests/
│   ├── test_preprocessing.py
│   ├── test_topic_matching.py
│   ├── test_seed_stability.py
│   ├── test_period_models.py
│   └── test_corpus_statistics.py
├── config/
│   ├── boilerplate_phrases.txt
│   ├── lemma_corrections.txt
│   ├── topic_names_32.tsv
│   ├── period_topic_names_8.tsv
│   └── chain_names_8.tsv
├── docs/                                  (in git)
│   ├── PIPELINE_DOCUMENTATION.md          (this file: the current pipeline)
│   ├── tables/                            (LaTeX tables for the report: preprocessing decisions with corpus size per step and the word lists; model-training decisions compared with Gordon; compile preprocessing_preview.tex or training_preview.tex)
│   └── reports/                           (seed-stability reports of 09 and 16; period_stability/ per period; topic_count_choice/ the 8/11/15 test)
├── visualizations/                        (in git: topic_explorer.html, period_explorer.html)
├── results/                               (not in git: generated CSV tables)
├── data/                                  (not in git)
│   ├── input/extracted_text_xml/
│   └── output/{lemmatized,boilerplate_removed,normalized,stopword_removed}/
└── models/                                (not in git)
    ├── baseline_lda_32/
    └── period_lda_8/
```

## Open Points and Next Steps

1. **Place names** (keep, remove or downweight)
2. **Party analysis:** with the session and author metadata, which parties' motions carry each topic, per period
3. **Algorithm and framing** (under discussion with the supervisor): the current plan is to keep scikit-learn and present the study as an adaptation of Gordon's workflow rather than a computational replication (MALLET, Gibbs sampling). If so, check convergence of the 50-pass fits (a 200-pass fit and a second seed)
4. **Rubric coding** (coherent, thematic, concentration) of the whole-corpus and period models, and a whole-corpus model with 8 topics as the counterpart of Gordon's k = 15 control
5. **Prominence analysis** with the whole-corpus model, restricted to stable topics
6. **Checks:** the residual topics of the whole-corpus model (*mälardalens, sexualitet*; *riksrevision, hbt*: possibly a few motions); duplicates kept or dropped
7. **Report writing**
