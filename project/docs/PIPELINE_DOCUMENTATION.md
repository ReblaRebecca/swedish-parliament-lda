# Swedish Parliamentary Education Motions: NLP Pipeline

## Overview

13,957 motions to the Swedish parliament's Education Committee (Utbildningsutskottet, UbU), parliamentary sessions 1985/86–2025/26, processed into lemmatized body text and modelled with Latent Dirichlet Allocation (LDA), following the temporally binned design of Gordon (2026):

- **Four period models**, one per period (1985/86–1993/94, 1994/95–2005/06, 2006/07–2013/14, 2014/15–2025/26; complete electoral terms, see *Periods*), **8 topics each**, each with **its own vocabulary**, aligned across adjacent periods over their shared words into topic chains (as Gordon)
- **One whole-corpus model with 32 topics** (= 4 × 8, the same total capacity as the four period models together), as the point of comparison
- **Body text only.** Titles are processed and kept as a separate field, but are not part of the model's documents
- **Seed stability** is tested for every model (5 seeds, Hungarian matching)

How the design was reached, and the open questions, are in `PROGRESS_SEMINAR_1.md`; the seed-stability reports are in `reports/`.

All paths below are relative to `project/`. Documentation and reports are in `docs/` and the HTML visualizations in `visualizations/` (both in git); generated tables (CSV) are in `results/`, data in `data/` and fitted models in `models/` (not in git). The raw XML is in `../../swedish-parliament-data/`, next to the repository. Every script resolves its default paths from its own location, so scripts can be run from any working directory.

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
            └── analysis/09_test_lda_stability.py       → docs/reports/BASELINE_STABILITY_32TOPICS_CORRECTED.md
    └── modeling/15_fit_period_lda.py [k]       → models/period_lda_<k>/ (one model and vocabulary per period), results/period_<k>_topics.csv
            ├── modeling/17_generate_period_explorer.py → visualizations/period_explorer.html
            └── analysis/16_seed_stability_periods.py   → docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md, results/period_stability/
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
- **Input:** XML files from the Swedish parliament open data portal, searched recursively (default `../../swedish-parliament-data/`; another location can be passed as the first argument)
- **Method:** follows Bruinsma & Johansson (2024)
- **Filter:** UbU committee (`organ` field), case-insensitive
- **Extract:** dok_id, date, title, author names, body text (between the introduction and signature markers); HTML entities decoded
- **HTML to text:** text pieces are joined without separators, with whitespace only at block-level tags (`<p>`, `<br>`, `<td>`, headings, …). The source HTML often splits single words across inline `<span>`s (`uppföljni</span><span>ng`, and in some motions every å/ä/ö is its own span), so joining with spaces would fragment words (see `PREPROCESSING_ARTIFACTS.md`)
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
- **Current result: 515 duplicates of 13,957 motions (3.69%)**; per period 11 / 31 / 154 / 319
  - Almost all are the **same motion resubmitted in a later session**, e.g. *Forskningsreaktor i Oskarshamn* 2015–2017. Motion numbers and author names are removed at extraction, so a resubmitted motion is identical to its original
  - Most are full-length texts (307 copies over 100 words, 200 of 21–100 words); 8 are near-empty bodies
  - A resubmitted motion counts once per year it was submitted, which weights recurring proposals in prominence; whether to keep them is open (seminar notes 2.10)

## Models

### Shared settings (`modeling/lda_common.py`)
Topic counts (`NUM_TOPICS = 32`, `PERIOD_TOPICS = 8`), the model folder name (`BASELINE_MODEL_DIR`), the period vocabulary settings (`PERIOD_VECTORIZER_PARAMS`), LDA settings, the reported seed (42), the stability seeds (42, 123, 456, 789, 999) and text loading live in this one module. Every model, stability test and explorer imports them from there, so the stability tests always measure the same models that are reported. A test checks that no other script creates its own LDA model.

- **LDA:** scikit-learn `LatentDirichletAllocation`, `learning_method='online'`, `max_iter=50`, `random_state=42`, `n_jobs=2`; symmetric default priors
- **No convergence check:** with online learning and sklearn's default `evaluate_every=-1`, every fit runs exactly 50 passes. The motions are processed in mini-batches of 128 (about 109 updates per pass) with a step size that decays with every update, so topics stop changing towards the end whether or not they have converged. The iteration count in the reports (always 50) confirms the setting, not convergence
- **Input:** `text_no_stopwords` (body text only). Motions with no body text left after preprocessing are skipped (4 motions), so the models use 13,953 motions (per period 4,025 / 3,477 / 2,879 / 3,572)
- **Diagnostic:** training perplexity, reported as a diagnostic only, not evidence of generalization

### Whole-corpus model (`modeling/07_fit_baseline_lda.py`)
- **Vectorizer:** `CountVectorizer(max_df=0.5, min_df=5, max_features=10000)`, default token pattern. The vocabulary of the whole-corpus model, its stability test and the topic explorer; the period models have their own (below)
- **Model:** 32 topics
- **Output:** `models/baseline_lda_32/baseline_lda_32_topics.pkl`, `models/baseline_lda_32/baseline_vectorizer.pkl`, and `results/document_topic_distribution.csv` (doc_id, title, year, session, period and the probability of every topic for every motion, for prevalence analysis)
- The name *baseline* is kept from the scripts' history; it is the whole-corpus model

### Period models (`modeling/15_fit_period_lda.py [k]`)
- One model per period, 8 topics each (`k` overrides the count), with the shared LDA settings
- **Vocabulary per period, as Gordon (2026, 3.3):** each period's vectorizer is built on that period's motions only, keeping words in at least 10 and at most 50% of them, with no cap on the vocabulary size (`PERIOD_VECTORIZER_PARAMS`, `fit_period_vectorizer()` in `lda_common.py`). Vocabularies: 7,302 / 7,981 / 4,926 / 6,876 words. Each period model is built on its own most relevant words: a word typical of one period is not crowded out by frequencies over 40 years, and a word frequent in one period is excluded only there
- **Output:** `models/period_lda_<k>/` (per period: the model, its vectorizer and `vocabulary_<period>.txt`), `results/period_<k>_topics.csv` (top 20 words per topic and period). k = 8 (`PERIOD_TOPICS`); another count can be passed to reproduce the topic-count choice

### Topic matching (`analysis/topic_matching.py`)
Hungarian-algorithm one-to-one matching between two models' topics on cosine similarity over the full topic-word distributions, with Jaccard overlap of the top words as a secondary measure. Used for seed stability (matching models with different seeds) and for alignment across periods (matching adjacent periods). One-to-one matching cannot represent a topic splitting or merging.

- **Seed stability:** the models share one vectorizer; cosine is computed over the full, identical vocabularies, and different or reordered vocabularies are an error
- **Adjacent periods (`shared_vocabulary=True`), as Gordon (2026, 3.4):** cosine over the words both periods' vocabularies contain (4,236–5,464 words per transition), put in the same order. Cosine does not depend on the scale of the vectors, so this equals Gordon's cosine on L2-normalized distributions over the shared words. Words outside the intersection do not count: so that vocabulary change is not hidden, the share of each topic's weight outside the shared words is reported (*Current Results*)

## Seed-Stability Testing

| Script | Tests | Output |
|---|---|---|
| `analysis/09_test_lda_stability.py` | The whole-corpus model | `docs/reports/BASELINE_STABILITY_32TOPICS_CORRECTED.md`, `results/BASELINE_STABILITY_32TOPICS_PER_TOPIC.csv` |
| `analysis/16_seed_stability_periods.py [k ...]` | The period models (default 8; `8 11 15` reproduces the topic-count choice) | `docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md`; full report per period in `docs/reports/period_stability/`; per-topic CSV in `results/period_stability/` (read by the period explorer) |

Both use the shared procedure in `analysis/seed_stability.py`: fit one model per seed (5 seeds), match every pair of models with the Hungarian algorithm (10 pairs), and compare matched topics by cosine (full distributions) and Jaccard (top 20 words).

**Reports** list, per seed, the training perplexity and iteration count; then the **stability per topic** of the reference model (seed 42, the seed of the reported model); then cosine and Jaccard statistics for each of the 10 seed pairs; then pooled statistics over all matched topic pairs.

**Stability per topic:** each topic of the seed-42 model is compared with its matched topic in each of the other 4 models. A topic is *found* in a model if the matched cosine is at least 0.70 (a judgement call, `seed_stability.FOUND_COSINE`), and *stable* if found in at least 3 of the 4. The table gives its top words, the number of models it is found in, and its mean and minimum cosine and mean Jaccard. The seed-42 model is fitted on the same data with the same settings as the reported model, so its topic numbers are those of the reported model. Use this to decide which topics to interpret with confidence.

**Pooled statistics:** the matched topic pairs are not independent (each seed's model appears in 4 of the 10 pairs). The pooled mean is a fair summary, but the pooled standard deviation understates the uncertainty; for the spread across runs, report the 10 per-pair means or their range.

## Current Results

### Whole-corpus model (32 topics)
Report: `docs/reports/BASELINE_STABILITY_32TOPICS_CORRECTED.md`.

| | 32 topics |
|---|---|
| Mean cosine (mean of the 10 per-pair means) | 0.568 |
| Range of the 10 per-pair means | 0.515–0.621 |
| Mean Jaccard (top 20) | 0.270 (per-pair 0.22–0.33) |
| Seed-42 topics found in 4 / 3 / 2 / 1 / 0 of the other 4 models | 7 / 5 / 7 / 5 / 8 |
| Stable (3–4 of 4) | 12 of 32 (38%) |
| Training perplexity, 5 seeds | 1702–1736 |

- **Found in all four other models (7):** compulsory school, teaching and grades (mean cosine 0.97), research (0.92), preschool/childcare (0.90), universities and students (0.90), upper secondary school (0.90), special support and disability (0.84), society, knowledge and democracy (0.84). **In 3 of 4:** higher-education places (0.86), regional higher education and business (0.81), international/SFI/immigrants (0.78), general problem words (*hög, många, problem, öka*; 0.73), medical education and health care (0.69)
- **Found in no other model (8):** youth and mental health (0.46), bullying (0.50), costs and fees (0.44), Stockholm institutions (0.23), vocational and apprenticeship education (0.06), and three residual topics of unrelated words (*mälardalens, sexualitet, helårsstudent*; *riksrevision, hbt, genusforskning*; *skog, värmland, skåne*; 0.12–0.14). Some are clear themes whose words other seeds spread over other topics (vocational education, bullying); the residual topics are probably held together by a few motions
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

- The period models are more stable than the whole-corpus model, which supports Gordon's case for period models
- The first period is exactly at half stable; the smallest period (2006/07–2013/14) is not less stable than the others
- **How 8 was chosen:** see *Design Decisions*

**Alignment across periods (8 topics):** matched mean cosine 0.67, 0.78 and 0.76 for the three transitions. All 8 chains hold by Gordon's criterion (mean link ≥ 0.50), 4 of them with every link ≥ 0.50: upper secondary school, pupils and teachers (mean link 0.85), higher education and research (0.82), municipalities and independent schools (0.79), and children, health and bullying (0.63). The other four hold on the mean but have one weak link: preschool (0.498 at the first link, just below the threshold, then 0.94 and 0.95), research (0.42 at the last link), higher education turning into labour market (0.32) and students (0.36). Without the permutation null these are provisional.

**Vocabulary outside the shared words:** on average 3.5–9.8% of a topic's weight falls on words outside the vocabulary it shares with the neighbouring period (range per topic 2.4–12.9%). The share is highest for the first period against the second (9.8%) and for the last against the third (7.8%).

### Comparison with Gordon (2026)

*Tracing Thematic Change in Early English-Language Science Fiction, 1818–1930* (`../../swedish-parliament-instructions/tracing_thematic_change.pdf`).

| | Gordon | This study |
|---|---|---|
| Whole-corpus seed stability (mean Jaccard of the top words) | 0.26–0.31 | 0.270, per-pair range 0.22–0.33 (32 topics) |
| Matched mean cosine between adjacent periods, 8 topics per period | — | 0.67, 0.78, 0.76 |
| Same, at Gordon's 15 topics per period (fitted once for this comparison) | 0.44–0.59 | 0.43, 0.60, 0.62 |
| Chains with mean cosine ≥ 0.50 over the three transitions | 7 of 15 | 8 of 8 (8 topics); 9 of 15 at 15 topics |

- **Seed instability is of the same size as Gordon's**, so it is not a weakness of this pipeline; Gordon uses the same finding as part of his argument for period models
- **At Gordon's topic count (15 per period), with his vocabulary design, the alignment is close to his:** matched cosine in the same range, and a few more chains pass his criterion (9 against 7). At 8 topics the links are stronger, as expected with fewer, broader topics
- Different corpora and algorithms: the agreement shows results of the same order, not equivalent methods

| Point | Gordon | This study | Assessment |
|---|---|---|---|
| Algorithm | MALLET, Gibbs sampling, 1,000 iterations, asymmetric hyperparameter optimization every 10 iterations | scikit-learn, online variational Bayes, 50 passes, symmetric priors | Probably the largest difference; convergence not checked |
| Vocabulary | Per period (≥ 10 documents, ≤ 50%), adjacent periods compared over their shared words | The same for the period models; the whole-corpus model has its own vocabulary (≥ 5 motions, ≤ 50%, 10,000 words) | Followed |
| Author signal | Authorless preprocessing (MALLET `DownsampleLabelWords`) | None | Counterpart here: MP/constituency signal (place names) |
| Documents | 1,000-word book chunks | Whole motions | Natural units, most shorter than 1,000 words |
| Proper names | Removed | Kept | Open (seminar notes 2.7) |
| Lemmatization | None | Stanza | Swedish inflection |
| Topics | 15 per period, 60 whole corpus | 8 per period, 32 whole corpus | Chosen by seed stability (8, 11 and 15 tested) |
| Seed stability | Whole-corpus runs only | Every model | Extension |

**Not yet comparable:** the permutation null and z-scores (Gordon: matched 0.44–0.59 against 0.22–0.25 for random pairings, z = 7–9), the rubric coding (coherent, thematic, concentration) of all models, and a whole-corpus model with 8 topics (the counterpart of Gordon's k = 15 control).

## Visualizations

| Script | Reads | Writes |
|---|---|---|
| `modeling/08_display_lda_topics.py [model_dir]` | `models/baseline_lda_32/` | `results/32_TOPICS_FINAL.csv` (top 20 words per topic, as P(word \| topic)) |
| `modeling/14_generate_topic_explorer.py` | `models/baseline_lda_32/`, `data/output/stopword_removed/`, template `modeling/topic_explorer_template.html` | `visualizations/topic_explorer.html` |
| `modeling/17_generate_period_explorer.py` | `models/period_lda_8/` (models and vectorizers), `data/output/stopword_removed/`, the per-topic CSVs of 16, template `modeling/period_explorer_template.html` | `visualizations/period_explorer.html` |

Both pages are self-contained HTML (open in a browser; internet needed only for the fonts). Word weights are shown as P(word | topic). Topics have neutral names (Topic 1–32, T1–T8 per period), so they can be inspected without interpretive labels.

### Topic explorer (whole-corpus model)
- **Per topic, two columns:** the word cloud (top 30 words) with the share-by-period chart under it on the left; the top 8 motions (session, party, id, θ) on the right; stacked on narrow screens. The heading gives the overall share and the party concentration among the top 5 motions (gold when 4 or 5 share the first signatory's party)
- **Word size:** square root of P(word | topic), on **one scale for all clouds**, so sizes can be compared between topics; if a word does not fit, all clouds shrink together. A topic spread over many words has a smaller, sparser cloud. The tooltip gives the exact probability
- **Order:** opens sorted by overall share, largest first (topic numbers are arbitrary); also by topic number, rise or fall (first vs last period; valid here since one model covers all periods, but the middle periods are ignored) and party concentration
- **Search:** covers only the 30 words shown per cloud (also as part of longer words), as stated next to the search box; a word that is not found can still have some probability in the topic

### Period explorer (period models)
- **8 topics per period,** the chosen count
- **Rows are chains.** Each period model has its own topics, so topic numbers do not correspond across periods. Topics of adjacent periods are matched one-to-one (Hungarian algorithm on cosine over the words both periods' vocabularies contain) and each row follows the matches from a topic of the first period to the last
- **Chain holds (main criterion, Gordon's):** the heading says *holds* if the mean cosine of the chain's three links is at least 0.50, otherwise *does not hold* (gold), with the mean and the weakest link
- **Weak links (additional information):** a single link below 0.50 breaks the row: the accent bar over the clouds stops, a dashed gold rule separates the cells and the cell reads *Alignment uncertain*. The heading names the strongly linked segments, or says *forced matches, not a continuous topic* when no link reaches 0.50. A chain can hold on the mean and still have one weak link
- **Per cloud:** the period, the topic's number in that period model, its share (mean θ over the period's motions), its seed stability from 16 (`seed n/4`, gold when below 3; shown only if the stability CSV's top words match the model) and the cosine with the matched topic of the previous period
- **Word colour = persistence within the chain:** in how many of the chain's four periods the word is among the top 20 words (the words shown): dark blue all four, medium blue three, light blue two, grey one. With 8 topics, 15% of the words shown are in all four periods and 41% in only one. Bold marks the three most probable words of each cloud
- **Word size:** square root of P(word | topic), on **one scale per chain**, so sizes can be compared across a chain's periods but not between chains; if a word does not fit, the chain's four clouds shrink together. The tooltip gives the exact probability
- **Order:** opens with the strongest chain first (mean link, high to low); also by chain number, weakest link first, and rise or fall in share (first vs last period, only for chains with every link ≥ 0.50, since a change across a weak link may compare unrelated topics; other chains are listed last, marked *no change computed*)
- **Search:** covers only the 20 words shown per cloud (also as part of longer words), as stated next to the search box
- **Limitations:** the matching gives every topic a partner, so a topic that exists in only one period still sits in a chain, joined by weak links, and a topic that appears in a later period cannot start its own row. Provisional alignment for inspection, without Gordon's permutation null

## Design Decisions

- **Stopwords vs. boilerplate.** Stopwords are general Swedish words, applied to the lemmatized, normalized text; boilerplate is parliamentary and domain-specific language (institutions, procedure, references), matched on the original word forms. Keeping them apart lets the stopword list be reused for other Swedish texts
- **Stanza lemmatization.** Swedish inflection splits one word into many forms (*skola, skolan, skolor, skolornas*), which fragments topics. Stanza is a general, context-aware lemmatizer run once on full sentences, with a small table of corrections for known errors. Known trade-offs: comparatives are reduced to the positive (*högre utbildning* → `hög utbildning`), rare compounds can get wrong lemmas (*arbetsvillkor* → `arbetsvillka`), and modal *ska* gets the lemma `skola` (handled by dropping auxiliaries). spaCy's `sv_core_news_sm` and a hand-made lookup table of education terms were tried earlier and rejected
- **Body text only.** Appending the title 3× or 5× to the body gave only a small stability gain (mean matched cosine 0.539 against 0.525 at 44 topics, overlapping ranges), too small to justify an extra modelling choice. Titles are kept in the data
- **Topic count: 8 per period, 32 for the whole corpus.** 8 is the only tested count (8, 11, 15) at which at least half of the topics are stable in every period, and it has the highest mean cosine in every period; since the number of robust themes is about the same at every count, 8 loses little substance and avoids many chance topics. The margin is small in the first and last periods (exactly half stable). The test (16 with `8 11 15`; reports in `docs/reports/topic_count_choice/`):

  | Period | 8 topics: mean cosine / stable | 11 topics | 15 topics |
  |---|---|---|---|
  | 1985/86–1993/94 | 0.70 / 4 of 8 (50%) | 0.63 / 4 of 11 (36%) | 0.55 / 4 of 15 (27%) |
  | 1994/95–2005/06 | 0.77 / 7 of 8 (88%) | 0.67 / 6 of 11 (55%) | 0.62 / 6 of 15 (40%) |
  | 2006/07–2013/14 | 0.80 / 6 of 8 (75%) | 0.65 / 4 of 11 (36%) | 0.58 / 6 of 15 (40%) |
  | 2014/15–2025/26 | 0.72 / 4 of 8 (50%) | 0.67 / 6 of 11 (55%) | 0.62 / 9 of 15 (60%) |
  | **All periods** | **21 of 32 (66%)** | **20 of 44 (45%)** | **25 of 60 (42%)** |

  The number of robust themes per period is about 4–9 at every count (8 → 15 adds 28 topics but only 4 stable ones), and the mean cosine falls with the topic count in every period. The test was run with the earlier global vocabulary (see *Vocabulary per period* below); with the per-period vocabularies the 8-topic models are as stable (21 of 32), and 11 and 15 were not re-tested. The 11- and 15-topic models were deleted after the choice; they can be refitted with `15_fit_period_lda.py <k>`. The whole-corpus model has the same total capacity as the four period models, as in Gordon (60 = 4 × 15)
- **Periods by electoral term, assigned by session** (see *Periods*): whole terms per period, as equal in size as the terms allow. They replaced four calendar-year bins of roughly equal size (1986–1993, 1994–2004, 2005–2014, 2015–2025, assigned by date); at 8 topics the period models became slightly more stable (21 against 19 of 32 topics stable) and the alignment stronger (all 8 chains pass Gordon's criterion, against 5). The differences are small, see seminar notes 2.9
- **Vocabulary per period, compared over shared words** (Gordon's method; see *Period models* and *Topic matching*). It replaced one global vocabulary for all models (the whole-corpus vectorizer). With 8 topics, stability stayed the same (21 of 32 topics stable) and the alignment became stronger (matched mean cosine 0.67, 0.78, 0.76 against 0.65, 0.69, 0.67; all 8 chains hold in both), as expected when words outside the shared vocabulary no longer count
- **Chain criterion:** Gordon's mean of the three links ≥ 0.50, so results are comparable with his; single weak links are shown as additional information

## Configuration Files

- **`config/boilerplate_phrases.txt`:** 440 explicit words/phrases, one per line, grouped by category with `#` headers. Matched against original word forms (body and title). An alternative file can be passed as the 3rd argument to `03_remove_boilerplate.py`. After editing, re-run steps 03–05 (no need to re-run Stanza)
- **`config/lemma_corrections.txt`:** corrections for known Stanza lemma errors, one `wrong correct` pair per line with `#` comments, applied in step 03 to body and title, case-insensitively. A wrong lemma with a leading `*` is also corrected at the end of a compound (`*kompet kompetens`: `gymnasiekompet` → `gymnasiekompetens`); mark an entry only after checking its compounds (`anslagen` must not be marked, because of *sammanslagen*). After editing, re-run steps 03–05
- **Stopwords:** hard-coded in `preprocessing/05_remove_stopwords.py` (NLTK base + supplementary list, including lemma forms)

## Data Summary

| Metric | Value | Note |
|--------|-------|------|
| Motions | 13,957 | All UbU motions, sessions 1985/86–2025/26; 13,953 with body text are modelled |
| Periods | 4 | 1985/86–1993/94, 1994/95–2005/06, 2006/07–2013/14, 2014/15–2025/26 (2,879–4,029 motions each) |
| Duplicates | 515 (3.69%) | Mostly resubmissions in later years; kept |
| Vocabulary | Period models: 4,926–7,981 per period | ≥ 10 and ≤ 50% of the period's motions (Gordon); whole-corpus model: 10,000 (≥ 5 motions, ≤ 50%) |
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
  - **Period explorer chains:** rows follow the Hungarian matches between adjacent periods (shuffled identical topics are linked correctly), a link below the threshold is reported as weak, and the seed-stability CSV is used only if its top words match the model
- **`tests/test_topic_matching.py`** — Hungarian matching on synthetic topic matrices: identical models match with cosine 1, a known permutation is recovered, mismatched or reordered vocabularies and mismatched topic counts are rejected, summary statistics equal the per-topic values. **Shared vocabulary:** the same topics in different vocabularies (other column order, extra words) match with cosine 1; weight on words outside the intersection does not change the cosine; vocabularies without common words are rejected
- **`tests/test_seed_stability.py`** — the seed-stability tests and the shared LDA code:
  - **Text loading:** body text only, motions without body text skipped, malformed lines counted
  - **No drift:** the model (07) and the stability test (09) use the very same functions from `lda_common.py`; no other script creates its own LDA model; the whole-corpus topic count is 4 × the period count; the reported seed is among the tested seeds
  - **Seeds:** the same seed reproduces the model exactly, a different seed changes it
  - **Planted topics:** on a synthetic corpus with three clearly separated topics, the full procedure finds cosine > 0.99 for every matched topic, so it can detect stability when it is there
  - **Report:** on a synthetic 5-seed, 44-topic setup, 10 pairs and 440 matched pairs; per-pair and pooled statistics equal those computed directly; the per-seed table and the notes on convergence and pooled statistics are present
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

1. **Place names** (keep, remove or downweight; seminar notes 2.7)
2. **Party analysis:** with the session and author metadata, which parties' motions carry each topic, per period (seminar notes 2.9)
3. **Algorithm and framing** (under discussion with the supervisor; seminar notes 0.4): the current plan is to keep scikit-learn and present the study as an adaptation of Gordon's workflow rather than a computational replication (MALLET, Gibbs sampling). If so, check convergence of the 50-pass fits (a 200-pass fit and a second seed)
4. **Alignment evidence:** Gordon's permutation null and z-scores for the period transitions (2.5)
5. **Rubric coding** (coherent, thematic, concentration) of the whole-corpus and period models (2.6), and a whole-corpus model with 8 topics as the counterpart of Gordon's k = 15 control
6. **Prominence analysis** with the whole-corpus model, restricted to stable topics (2.4)
7. **Checks:** the residual topics of the whole-corpus model (*mälardalens, sexualitet*; *riksrevision, hbt*: possibly a few motions); remaining small leftovers of the model review (`MODEL_REVIEW.md`); duplicates kept or dropped (2.10)
8. **Report writing**
