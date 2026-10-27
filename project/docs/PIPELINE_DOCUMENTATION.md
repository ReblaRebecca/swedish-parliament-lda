# Swedish Parliamentary Education Motions: NLP Pipeline

## Overview

13,957 motions to the Swedish parliament's Education Committee (Utbildningsutskottet, UbU), parliamentary sessions 1985/86–2025/26 (13,943 with text of their own; 10,692 modelled, see *Models*), processed into lemmatized body text and modelled with Latent Dirichlet Allocation (LDA), following the temporally binned design of Gordon (2026):

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

- All motions to all committees; extraction finds the 13,957 referred to the Committee on Education (UbU) in sessions 1985/86–2025/26 (see *Periods*). The earliest UbU motions are in `mot-1980-1989` (session 1985/86, from January 1986)
- **The corpus is defined by committee, not by content:** every motion referred to UbU is kept, with no filtering by subject. The corpus therefore covers what parliament handled as education and research policy, including university facilities and research funding, and some motions are only partly about education. Example: *Göteborgs botaniska trädgård* (1986/87, GA02Ub569) asks for a new state funding agreement for the university's botanical garden; teaching and research are one argument among public visitors, conservation and costs. The rule is reproducible and avoids case-by-case judgements of what counts as education; the price is a few topics organized around such motions (the botanical-garden motions are 3 of the top 6 motions of a residual topic of the whole-corpus model). A limitation to state in the report
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
            ├── modeling/14_generate_topic_explorer.py  → visualizations/topic_explorer.html
            └── analysis/09_test_lda_stability.py       → docs/reports/BASELINE_STABILITY_32TOPICS.md
    └── modeling/15_fit_period_lda.py [k]       → models/period_lda_<k>/ (one model and vocabulary per period), results/period_<k>_topics.csv
            ├── modeling/17_generate_period_explorer.py → visualizations/period_explorer.html
            ├── analysis/16_seed_stability_periods.py   → docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md, results/period_stability/
            ├── analysis/18_alignment_null.py           → docs/reports/PERIOD_ALIGNMENT_NULL.md
            └── analysis/convergence_check.py           → docs/reports/CONVERGENCE_CHECK.md
            (analysis/corpus_statistics.py: words and different words per step, for the report)
```

Every data stage stores one JSONL file per period: `group1_1985-1994.jsonl`, `group2_1994-2006.jsonl`, `group3_2006-2014.jsonl`, `group4_2014-2026.jsonl` (named after the calendar years the period's sessions span). Each stage adds fields and keeps earlier ones, so metadata (`dok_id`, session, title, date, author names) is carried through to the models. Every stage counts and reports malformed JSON lines per period, so no data is lost silently.

**Why this order:** Stanza is the only slow step, so it runs once, right after extraction, and saves every word with its original form, lemma and part of speech. Everything after it works from that saved output and takes minutes, so the boilerplate list and stopwords can be changed and re-run without running Stanza again.

### Periods (`periods.py`)

The four periods are defined once, in `periods.py`, and imported by every script. They follow **complete electoral terms** (mandatperioder), grouped so that the periods are as equal in size as the terms allow:

| Period | Sessions | Electoral terms beginning | UbU motions | Modelled |
|---|---|---|---|---|
| 1 | 1985/86–1993/94 | 1985, 1988, 1991 | 4,029 | 3,467 |
| 2 | 1994/95–2005/06 | 1994, 1998, 2002 | 3,477 | 3,055 |
| 3 | 2006/07–2013/14 | 2006, 2010 | 2,879 | 2,026 |
| 4 | 2014/15–2025/26 | 2014, 2018, 2022 | 3,572 | 2,144 |

*UbU motions*: all motions referred to the committee; *Modelled*: without placeholders, motions under 20 words, later copies of duplicates and near-duplicates (see *Extraction* and *Models*).

- **Why electoral terms:** a period then covers whole terms of the Riksdag and its governments, so no term is split between two periods. Of the possible groupings of the 11 terms into four consecutive periods, this one has the most even sizes (largest / smallest = 1.40)
- **Assigned by session, not by date:** a motion belongs to the period of its parliamentary session (riksmöte, XML field `rm`, e.g. `1993/94`; session 1999/2000 is written with four digits). The session is the unit of parliamentary work, and some motions carry a placeholder date (motions of 1985/86 dated 1985-01-01)
- **Coverage:** the first session in the data is 1985/86, but UbU motions start in January 1986 (motions of autumn 1985 are not tagged with the committee); the last period runs to the end of session 2025/26, the last session before the 2026 election
- Pages and reports name the periods by their sessions (1985/86–1993/94); file and model names use the calendar years (`1985-1994`)
- The electoral terms themselves are also defined in `periods.py` (`TERM_STARTS`; a session belongs to the term of the last election before it). The topic explorer shows each topic's share per term

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
- **Placeholders skipped (`is_placeholder`):** motions with no text of their own: a text under 30 words with the riksdag's notice that the document is missing (*Dokument saknas*) or not yet converted (*konvertering pågår*), or a withdrawal notice (*Motionen utgår*, *återtagen*) in the text or the title. 14 motions: 6 missing documents, 1 unfinished conversion, 7 withdrawn (4 of which were previously dropped only at modelling, having no body text after preprocessing). The real shortest motions (formal requests of 25–27 words referring to another motion) are kept here; most of them fall under the models' length minimum (*Models*). Skipped per period: 11 / 2 / 0 / 1
- **Period:** assigned from the motion's session (`rm`), see *Periods*
- **Output:** 13,943 motions in `data/input/extracted_text_xml/`. Fields: `session`, `text` (cleaned body), `title` (original title, for display), `title_text` (cleaned title, for processing). The files are JSONL; the folder name means "text extracted from XML"

### 2. Tagging and Lemmatization (`preprocessing/02_lemmatize.py`) — run once
- **Tool:** [Stanza](https://stanfordnlp.github.io/stanza/) Swedish pipeline (`tokenize,pos,lemma`, default Talbanken model), stored in `SU/stanza_resources/` and downloaded there automatically if missing
- Runs on the running text of body and title, so the tagger sees full sentences and can use context
- **Saves every word** as `[word, lemma, upos]`, grouped by sentence, in `tokens` (body) and `title_tokens` (title). Nothing is removed at this step
- **Resumable:** motions already in the output file are skipped, so an interrupted run continues where it stopped
- **Runtime:** CPU-heavy; about 3¾ hours for the full corpus

### 3. Boilerplate Removal (`preprocessing/03_remove_boilerplate.py`)
- **Phrases:** `config/boilerplate_phrases.txt` (467 entries, one explicit word or phrase per line, no wildcards), matched case-insensitively against the **original word forms** saved by step 2, so the list keeps its surface forms (`riksdagen`, `med anledning av`). A word is removed only if a phrase match covers the whole word, apart from trailing punctuation (Stanza keeps the full stop in abbreviations, so the phrase `mot` removes `Mot.`); phrases never match across sentences
- **Categories:** OCR/scanning artifacts, government and parliamentary institutions, parliamentary document/reference terms, procedural language, party names, etc.
- **Output is lemmas** of the remaining words, one sentence per line
- **Dropped tokens:** auxiliary verbs (UPOS `AUX`), punctuation and symbols. Stanza lemmatizes the modal *ska/skall/skulle* to `skola`, which would merge with the noun *skola* (school); all auxiliaries are stopwords anyway
- **Dropped abbreviation lemmas:** words whose lemma contains an underscore. Stanza expands abbreviations into multi-word lemmas (`t.ex.` → `till_exempel`, `bl.a.` → `bland_annat`, `s.k.` → `så_kallad`, `m.fl.` → `med_flera`), sometimes garbled (`få_cetera`). Every dropped word is counted in `data/output/boilerplate_removed/underscore_lemmas.json` (lemma → count and word forms) for manual review
- **Lemma corrections:** known Stanza lemma errors are corrected from `config/lemma_corrections.txt` (`kompet` → `kompetens`, `lärosät` → `lärosäte`, `anslagen` → `anslag`, …). Stanza guesses lemmas for words it has not seen in training, and some guesses are truncated or repeat a stem (*Universitetskanslersämbetet* → `universitetskanslersämbetsämbets…`, corrected to `universitetskanslersämbete`); it also leaves some definite or plural forms as the lemma, so one word is split in two (*skolverket* 4,854 times against *skolverk* 1,563; *lärosätena* → `lärosäten`; *huvudman/huvudmän* → `huvudma`, 2,422). Such pairs were found by listing final-text words that are another frequent word plus an inflection ending and checking their word forms; 25 are corrected (e.g. `*verket` → `verk` for Skolverket, Högskoleverket, regelverket); the list corrects the errors found by inspecting the models, it does not replace the lemmatizer
- **Speed:** a phrase's regex is run only if its text occurs in the lowercased motion at all (`pattern_literal()`); most of the 467 phrases occur in few motions. Same output as running every regex (checked on 1,600 motions), about 3× faster (some 2½ minutes for the corpus)
- **Output fields:** `text_no_boilerplate`, `title_no_boilerplate`

### 4. Normalization (`preprocessing/04_normalize_text.py`)
- Lowercase, remove numbers and punctuation, collapse whitespace
- Drops single-character words; preserves line breaks
- **Output fields:** `text_normalized`, `title_normalized`

### 5. Stopword Removal (`preprocessing/05_remove_stopwords.py`)
- **Base list:** NLTK Swedish stop words (114)
- **Supplementary (129, hard-coded):** parliamentary abbreviations (ub, dvs, osv, …), the scanner misreading `sorn` (for *som*), generic words in more than 30% of the motions (få, också, därför, annan, många, viktig, möjlighet, lite, ske, egen, god, grund) the generic language of political argument (öka, ökad, skapa, kräva, förutsättning) and of the motion's request (föreslå, överväga, konstatera, angelägen), function words in 10–30% of the motions (därmed, således, alltså, emellertid, …), the lemmas `circa` (of *ca*) and `procent` (of *%*, which the boilerplate list cannot match), auxiliary verbs (ska, skall, blir, …), generic connectors, verbs and adjectives identified from LDA inspection (kommer, enligt, olika, göra, …), and the **lemma forms** of inflected entries (behöva, vilja, kunna, ny, stor, olik, mången, …), since the text is lemmatized. Content abbreviations such as `fn`, `eg`, `ky`, `ib` are deliberately not stopwords (education-policy terms)
- **Output fields:** `text_no_stopwords` (final body text, used by the models) and `title_processed` (final title text)

### Duplicates (`analysis/count_duplicates.py` lists them; the models skip them)
- **The models skip duplicates:** of identical final texts only the first is modelled (`text_key()` and `read_bin_body_texts()` in `lda_common.py`; period files read in order, so a copy in a later period is skipped there too, in the whole-corpus and the period models alike). Reason: identical texts weight their words several times in the topics and count a recurring proposal once per session in the shares, mostly in the last period. The cost, that resubmission itself signals a persistent issue, is reported with the count below
- `count_duplicates.py` uses the same key: MD5 hash of the whitespace-normalized final text; one hash dictionary across all periods, so duplicates are found across periods. Prints duplicates per period, the total and each duplicate → original `dok_id`; writes no data
- The count depends on the final text, so re-run it after changing the boilerplate or stopword lists
- **Current result: 655 duplicates of 13,943 motions (4.70%)**; per period 23 / 32 / 171 / 429. More than before the latest stopword and boilerplate additions (551): with the template headings and generic words removed, more resubmitted motions become identical
  - Almost all are the **same motion resubmitted in a later session**, e.g. *Forskningsreaktor i Oskarshamn* 2015–2017. Motion numbers and author names are removed at extraction, so a resubmitted motion is identical to its original
  - Most are full-length texts (310 copies over 100 words, 334 of 21–100 words); 11 are short formal requests of 20 words or fewer
  - Kept, a resubmitted motion would count once per year it was submitted, weighting recurring proposals in prominence; hence only the first copy is modelled
  - The 11 short ones are under the 20-word minimum and skipped for that reason already, so the models skip 644 motions as duplicates (per period 12 / 32 / 171 / 429). Most are in the last two periods: 12% of the motions of 2014/15–2025/26 are copies of an earlier text

### Near-duplicates (`near_duplicates()` in `lda_common.py`; counted by `count_duplicates.py`)
- **Rule:** a motion is not modelled if its final text shares at least 60% of its three-word sequences (Jaccard similarity of the sets of word 3-grams, `NEAR_DUPLICATE_JACCARD = 0.6`) with an earlier motion (earlier session; within a session, earlier in the data). Applied after the length minimum and exact duplicates, over all periods at once; the period models use the same motions
- **Why:** many motions are the same proposal resubmitted year after year with small edits (a new year, a reworded sentence), so they are not exact duplicates. Such series can hold up topics of their own (the top motions of a topic are one author's series, e.g. *Naturkunskap i skolan* 1988–2001) and count a recurring proposal once per session in the shares. As with exact duplicates, a near-copy adds no new text; a motion revised more than that is kept as a new motion
- **Threshold:** checked on the data after the earlier filters (13,005 motions after the length minimum and exact duplicates), the share of motions with at least this similarity to an earlier one: 0.9 → 739 (5.7%), 0.8 → 1,378 (10.6%), 0.7 → 1,892, **0.6 → 2,313 (17.8%)**, 0.5 → 2,715 (20.9%), 0.3 → 3,545 (27.3%) (0.9, 0.7, 0.5 and 0.3 counted before the last boilerplate change, on 13,007 motions). Random pairs: from 0.6 up almost always the same motion with small edits; 0.4–0.6 mostly the same motion rewritten more (including parties' yearly budget motions, which reuse about half their text); 0.3–0.4 mixed. 98% of the pairs at 0.8 have a first signatory of the same party. **0.6 chosen** (first 0.8): in a sample of 20 pairs between 0.6 and 0.8 every pair is one proposal resubmitted by the same party, one to three sessions later, with the same or a similar title; the 0.6–0.7 pairs look like the 0.7–0.8 ones. Borderline: long yearly party programmes (e.g. C's *Utbildning för livslångt lärande* 2021/22 → 2022/23, about 5,500 words, 0.61), of which about a third is new text each year; the later year is skipped. A lower threshold would treat substantially rewritten motions, arguably new political acts, as copies. Lowering the threshold does not remove all series: the same demand written anew each year (e.g. *Biologi/ekologi i gymnasieskolan*, 0.49) stays
- **Result:** 2,313 motions skipped (per period 262 / 378 / 678 / 995), leaving 10,692 (3,467 / 3,055 / 2,026 / 2,144). At 0.8: 1,378 skipped, 11,627 left. Resubmission grows over time: the last period loses 40% of its motions to exact and near copies together (1,424 of 3,571), the first 7%. This is itself a finding about the genre; the shares count distinct texts, not submissions
- **Runtime:** about 12 seconds per loading of the corpus
- **Deduplication comparison (`analysis/dedup_comparison.py`; report `docs/reports/DEDUP_COMPARISON.md`):** the whole-corpus and period models fitted with the stability seeds on four selections, *none* (length minimum only; 13,649 motions), *exact* (13,005), *0.8* (exact and near-duplicates at the earlier threshold; 11,627) and *0.6* (the models' setting, 10,692; `dedup` argument of `load_body_texts()`: `none`, `exact`, `near08`, `near`), compared on seed stability, small topics, topics whose top 10 motions are a series of related texts (≥ 5 linked by ≥ 0.3 of their three-word sequences), one-party topics (≥ 6 of the top 10 motions), alignment and chains, and how the matched topics' shares per period change. About 1.5 hours

  | Selection | Whole corpus: mean cosine / stable | Series-dominated topics | One-party topics | Periods: stable | Alignment (matched mean cosine) | Chains hold (all links strong) |
  |---|---|---|---|---|---|---|
  | None | 0.557 / 11 of 32 | 10 | 14 | 21 of 32 | 0.58, 0.68, 0.66 | 6 of 8 (3) |
  | Exact | 0.567 / 13 of 32 | 7 | 11 | 23 of 32 | 0.67, 0.61, 0.64 | 8 of 8 (4) |
  | Near, ≥ 0.8 | 0.562 / 10 of 32 | 2 | 13 | 19 of 32 | 0.63, 0.66, 0.68 | 6 of 8 (3) |
  | **Near, ≥ 0.6 (the models)** | 0.542 / 8 of 32 | **1** | **5** | 23 of 32 | 0.60, 0.61, 0.63 | 6 of 8 (2) |

  - **The filter does what it is for:** topics held up by one author's or one party's series of resubmissions fall from 10 (none) to 7 (exact), 2 (0.8) and 1 (0.6). One-party topics fall mainly with the step from 0.8 to 0.6 (13 → 5): the pairs between 0.6 and 0.8 are same-party resubmissions (*Threshold*), so at 0.8 a party's yearly series could still hold up a topic
  - **Seed stability barely changes** (whole corpus 8–13 stable topics, periods 19–23), with no direction: duplicates do not make the models much more or less reproducible. The 0.6 selection has the fewest stable whole-corpus topics and the most stable period topics (with *exact*)
  - **Alignment and chains do not change in one direction:** the matched cosines lie between 0.58 and 0.68 in every selection, and 6 of 8 chains hold in all but *exact* (8 of 8). The differences are of the size of the differences between seeds. Every selection is far above chance (*Permutation test*)
  - **Shares change:** matched topics' shares per period differ by up to about 18 percentage points between the selections (report; e.g. grants to higher education, 27.0% of the first period with exact duplicates removed, 8.6% at 0.6), so prominence over time depends on whether a resubmission counts once or once per session

### Relation to Gordon's author signal
Resubmission is treated as the parliamentary counterpart of Gordon's (2026) author signal, with three differences.

- **Where it fits:** both are source-specific patterns that can make a topic reflect one source rather than a pattern shared across the corpus. In Gordon's corpus one author's vocabulary (Verne) can hold up a topic; here one MP's yearly resubmissions did (*Naturkunskap i skolan*, *Stiftelsen Skånehantverk*). Both are reduced before modelling: Gordon with *Authorless* preprocessing, here with the exact and near-duplicate filters. Both are measured: Gordon reports author concentration; the deduplication comparison counts series-dominated and one-party topics. The effects point the same way: Authorless lowered author concentration and modestly raised thematic content; deduplication cut series-dominated topics from 10 to 1 and one-party topics from 14 to 5 without changing seed stability much
- **Repetition, not style:** Gordon's author signal is an author's idiom across *different* texts; resubmission is largely the *same* text submitted again. Hence a different remedy: copies are removed, whereas Authorless down-weights author-typical words and keeps every document
- **The closer counterpart of style is kept:** the constituency signal, place names in one MP's motions (*Gävle-Sandviken*, *Skövde*), shapes topics across different motions as an author's idiom does. Place names are not removed or down-weighted (a limitation; see *Open Points*)
- **Party is not a confound:** in fiction an author's idiom is noise for a study of genre themes; in parliament a party's ownership of an issue is part of the politics studied. Party concentration is therefore reported as a property of each topic (the rubric's third dimension), not removed

## Models

### Shared settings (`modeling/lda_common.py`)
Topic counts (`NUM_TOPICS = 32`, `PERIOD_TOPICS = 8`), the model folder name (`BASELINE_MODEL_DIR`), the vocabulary rule of every model (`VECTORIZER_PARAMS`), LDA settings, the reported seed (42), the stability seeds (42, 123, 456, 789, 999) and text loading live in this one module. Every model, stability test and explorer imports them from there, so the stability tests always measure the same models that are reported. A test checks that no other script creates its own LDA model.

- **LDA:** scikit-learn `LatentDirichletAllocation`, `learning_method='online'`, `max_iter=50`, `random_state=42`, `n_jobs=2`; symmetric default priors
- **No convergence test during fitting:** with online learning and sklearn's default `evaluate_every=-1`, every fit runs exactly 50 passes. The motions are processed in mini-batches of 128 (about 109 updates per pass) with a step size that decays with every update, so topics stop changing towards the end whether or not they have converged. The iteration count in the reports (always 50) confirms the setting, not convergence
- **Convergence check (`analysis/convergence_check.py`; report `docs/reports/CONVERGENCE_CHECK.md`):** each model (whole corpus and the four periods, seed 42) fitted once with 200 passes, compared at 10, 25, 50, 100 and 150 passes with the 200-pass model. At 50 passes the topics match the 200-pass topics with mean cosine 0.993 (whole corpus; lowest single topic 0.930) and 0.980–0.997 (periods; lowest 0.922), every topic found; perplexity falls by 0.1–0.5% from 50 to 200 passes. More passes would not change the topics: the differences between seeds (mean cosine 0.54 whole corpus, 0.75–0.79 periods) are not due to unfinished fits. This shows that the fits have settled, not that online variational Bayes reaches the same topics as Gibbs sampling
- **Input:** `text_no_stopwords` (body text only) of the 13,943 extracted motions, without motions under 20 words, later copies of duplicates and near-duplicates: **10,692 motions** (per period 3,467 / 3,055 / 2,026 / 2,144)
- **Minimum length (`MIN_WORDS = 20`, `is_modelled()` in `lda_common.py`):** motions with fewer than 20 words in the final text are not modelled. Almost all are short formal requests (*hemställan*) referring to another motion: too short for a reliable topic mix, and since every motion counts equally in a topic's share they would add noise to the shares. 294 motions skipped (per period 277 / 10 / 4 / 3), almost all in 1985/86–1993/94
- **Duplicates:** of identical final texts only the first copy is modelled, in the whole-corpus and the period models alike: 644 motions skipped (see *Duplicates*)
- **Near-duplicates:** revised resubmissions (≥ 60% of three-word sequences shared with an earlier motion) are skipped as well: 2,313 motions, leaving 10,692 (see *Near-duplicates*)
- **Diagnostic:** training perplexity, reported as a diagnostic only, not evidence of generalization

### Whole-corpus model (`modeling/07_fit_baseline_lda.py`)
- **Vectorizer:** `CountVectorizer(min_df=10, max_df=0.5)`, default token pattern: the same rule as the period models (`VECTORIZER_PARAMS` in `lda_common.py`; Gordon 2026, 3.3), applied to all motions: words in at least 10 and at most 50% of the motions, no cap on the vocabulary size. 13,860 words. The vocabulary of the whole-corpus model, its stability test and the topic explorer
- **Model:** 32 topics
- **Output:** `models/baseline_lda_32/baseline_lda_32_topics.pkl`, `models/baseline_lda_32/baseline_vectorizer.pkl`, and `results/document_topic_distribution.csv` (doc_id, title, year, session, period and the probability of every topic for every motion, for prevalence analysis)
- *Baseline* in script and file names means the whole-corpus model

### Period models (`modeling/15_fit_period_lda.py [k]`)
- One model per period, 8 topics each (`k` overrides the count), with the shared LDA settings
- **Vocabulary per period, as Gordon (2026, 3.3):** each period's vectorizer is built on that period's motions only, keeping words in at least 10 and at most 50% of them, with no cap on the vocabulary size (`VECTORIZER_PARAMS`, `fit_period_vectorizer()` in `lda_common.py`; the whole-corpus model uses the same rule over all motions). Vocabularies: 6,875 / 7,344 / 3,952 / 5,107 words. Each period model is built on its own most relevant words: a word typical of one period is not crowded out by frequencies over 40 years, and a word frequent in one period is excluded only there
- **Output:** `models/period_lda_<k>/` (per period: the model, its vectorizer and `vocabulary_<period>.txt`), `results/period_<k>_topics.csv` (top 20 words per topic and period). k = 8 (`PERIOD_TOPICS`); another count can be passed to reproduce the topic-count choice

### Topic matching (`analysis/topic_matching.py`)
Hungarian-algorithm one-to-one matching between two models' topics on cosine similarity over the full topic-word distributions, with Jaccard overlap of the top words as a secondary measure. Used for seed stability (matching models with different seeds) and for alignment across periods (matching adjacent periods). One-to-one matching cannot represent a topic splitting or merging.

- **Seed stability:** the models share one vectorizer; cosine is computed over the full, identical vocabularies, and different or reordered vocabularies are an error
- **Adjacent periods (`shared_vocabulary=True`), as Gordon (2026, 3.4):** cosine over the words both periods' vocabularies contain (3,450–5,195 words per transition), put in the same order. Cosine does not depend on the scale of the vectors, so this equals Gordon's cosine on L2-normalized distributions over the shared words. Words outside the intersection do not count: so that vocabulary change is not hidden, the share of each topic's weight outside the shared words is reported (*Current Results*)

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
Report: `docs/reports/BASELINE_STABILITY_32TOPICS.md`. Vocabulary: the same rule as the period models (13,860 words).

| | 32 topics |
|---|---|
| Mean cosine (mean of the 10 per-pair means) | 0.542 |
| Range of the 10 per-pair means | 0.496–0.593 |
| Mean Jaccard (top 20) | 0.251 (per-pair 0.19–0.28) |
| Seed-42 topics found in 4 / 3 / 2 / 1 / 0 of the other 4 models | 4 / 4 / 8 / 7 / 9 |
| Stable (3–4 of 4) | 8 of 32 (25%) |
| Training perplexity, 5 seeds | 1934–1955 |

- **Found in all four other models (4):** preschool and childcare (mean cosine 0.92), higher education: admission and quality (0.92), research policy and research training (0.91), upper secondary school, grades and choice of subjects (0.86). **In 3 of 4 (4):** independent schools, municipalities and school choice (0.87), languages, mother tongue and sign language (0.78), grants to higher education and research (0.72), regional higher education institutions and economics programmes (0.60; found in three seeds, split in the fourth)
- **Found in no other model (9):** some clear themes whose words other seeds spread over other topics (special schools, disability and teaching materials 0.58; responsibilities, regulation and compulsory student union membership 0.52; health, diet and medical teaching 0.51; national governance and inspection 0.39; technology, IT and natural science 0.24), and small topics held together by a few motions or place names (0.06–0.18: pharmacy and medical education; foundations and botanical gardens; school-leaving ceremonies, KY and harassment; ANT and LGBT issues)
- **Use:** prominence trends and any mapping of period topics onto whole-corpus topics should rely on the stable topics, or report the range over seeds

### Period models
Report: `docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md`.

| Period | Mean cosine | Stable (3–4 of 4) |
|---|---|---|
| 1985/86–1993/94 | 0.79 | 5 of 8 (62%) |
| 1994/95–2005/06 | 0.76 | 5 of 8 (62%) |
| 2006/07–2013/14 | 0.78 | 6 of 8 (75%) |
| 2014/15–2025/26 | 0.75 | 7 of 8 (88%) |
| **All periods** | | **23 of 32 (72%)** |

- The period models are more stable than the whole-corpus model (25%), with the same vocabulary rule. Part of the difference is the topic count: at 15 topics per period, 43% of the period topics are stable (*Design Decisions*), still more than the whole-corpus model's 25%. The comparison supports Gordon's case for period models only together with the choice of 8 topics
- Every period has at least 5 of its 8 topics stable; the mean cosines are close (0.75–0.79)
- **How 8 was chosen:** see *Design Decisions*

**Alignment across periods (8 topics):** matched mean cosine 0.60, 0.61 and 0.63 for the three transitions. 6 of the 8 chains hold by Gordon's criterion (mean link ≥ 0.50), 2 of them with every link ≥ 0.50: research and research policy (mean link 0.89) and grades, teaching and the governance of schools (0.87). Four hold on the mean but have weak links: adult education and study support (0.61; 0.41 at the first link), vocational education, adult education and the labour market (0.59; 0.49 at the first link), teacher education, the Education Act and preschool (0.59; 0.31 at the second link) and preschool, bullying and safety (0.57; 0.27 at the first link). Two do not hold: regional higher education, health and democracy (0.49; links 0.89, 0.10, 0.47) and medicine, care and medical education (0.30; 0.35, 0.41, 0.13). With exact duplicates only removed, all 8 chains hold (*Near-duplicates*).

**Permutation test (Gordon's, `analysis/18_alignment_null.py`; report `docs/reports/PERIOD_ALIGNMENT_NULL.md`):** for each transition, the matched mean cosine is compared with 1,000 random one-to-one pairings of the same topics; z = (matched − null mean) / null SD, p one-sided from the standard normal distribution, as Gordon.

| Transition | Matched | Null mean (SD) | z |
|---|---|---|---|
| 1985/86–1993/94 → 1994/95–2005/06 | 0.601 | 0.316 (0.067) | 4.3 |
| 1994/95–2005/06 → 2006/07–2013/14 | 0.614 | 0.318 (0.069) | 4.3 |
| 2006/07–2013/14 → 2014/15–2025/26 | 0.626 | 0.340 (0.071) | 4.0 |

- Every transition is far above chance (p < 0.0001): the alignment shows continuity, not forced matches. It does not show that every single link is the same theme
- The z-scores are lower than Gordon's 7–9 although the matched cosines are higher: with 8 topics the mean of a random pairing varies more than with 15 (larger null SD), and the null mean is higher (0.32–0.34 against his 0.22–0.25), since 8 broad topics share more general education vocabulary
- The weak links (below 0.50) are most frequent at the first transition (4, 3 and 2 per transition); the matched cosine rises slightly from the first transition to the last
- **Against the seed-stability ceiling:** the period models' mean seed cosine is 0.75–0.79. All three transitions (0.60–0.63) are below it, so across periods the topics change more than between seeds of one period. Seed cosine is over the full vocabulary and alignment over shared words, so the comparison is approximate

**Vocabulary outside the shared words:** on average 2.7–10.3% of a topic's weight falls on words outside the vocabulary it shares with the neighbouring period (range per topic 1.7–15.8%). The share is highest for the second period against the third (10.3%), and for the last against the third and the first against the second (7.4% and 7.3%).

### Comparison with Gordon (2026)

*Tracing Thematic Change in Early English-Language Science Fiction, 1818–1930* (`../../swedish-parliament-instructions/tracing_thematic_change.pdf`).

| | Gordon | This study |
|---|---|---|
| Whole-corpus seed stability (mean Jaccard of the top words) | 0.26–0.31 | 0.251, per-pair range 0.19–0.28 (32 topics) |
| Matched mean cosine between adjacent periods, 8 topics per period | — | 0.60, 0.61, 0.63 |
| Same, at Gordon's 15 topics per period (fitted once for this comparison) | 0.44–0.59 | 0.43, 0.43, 0.46 |
| Chains with mean cosine ≥ 0.50 over the three transitions | 7 of 15 | 6 of 8 (8 topics); 8 of 15 at 15 topics |
| Permutation test: null mean, z (per transition) | 0.22–0.25, z = 7–9 (15 topics) | 0.32–0.34, z = 4.0–4.3 (8 topics); 0.15–0.18, z = 7.7–8.0 (15 topics) |

- **Seed instability is of the same size as Gordon's** (slightly below his range on average: 0.251 against 0.26–0.31), so it is not a weakness of this pipeline; Gordon uses the same finding as part of his argument for period models
- **At Gordon's topic count (15 per period), with his vocabulary design, the alignment is at the low end of his:** matched cosine 0.43–0.46, at or just below his lowest transition (0.44); the permutation test is of the same size (null mean 0.15–0.18, z = 7.7–8.0, against his 0.22–0.25 and 7–9): lower matched cosines, but also lower null means. About as many chains pass his criterion (8 of 15 against his 7). Before the final run (0.8 threshold, earlier boilerplate and lemma corrections) the matched cosines at 15 topics were 0.52–0.58; which change lowered them was not tested at 15 topics (at 8 topics the duplicate filter has no clear effect, *Near-duplicates*). At 8 topics the links are stronger, as expected with fewer, broader topics
- Different corpora and algorithms: the agreement shows results of the same order, not equivalent methods

| Point | Gordon | This study | Assessment |
|---|---|---|---|
| Algorithm | MALLET, Gibbs sampling, 1,000 iterations, asymmetric hyperparameter optimization every 10 iterations | scikit-learn, online variational Bayes, 50 passes, symmetric priors | Probably the largest difference; 50 passes checked against 200 (*Convergence check*) |
| Vocabulary | Per period (≥ 10 documents, ≤ 50%), adjacent periods compared over their shared words | The same; the whole-corpus model uses the same rule over all motions (13,860 words) | Followed |
| Author signal | Authorless preprocessing (MALLET `DownsampleLabelWords`): author-typical words down-weighted, all documents kept; author concentration reported | Resubmission treated as the counterpart: exact and near-copies removed before modelling; party concentration reported (rubric). Constituency place names, the closer counterpart of authorial style, kept | Adapted (see *Relation to Gordon's author signal*) |
| Documents | 1,000-word book chunks | Whole motions | Natural units, most shorter than 1,000 words |
| Proper names | Removed | Kept | Open |
| Lemmatization | None | Stanza | Swedish inflection |
| Topics | 15 per period, 60 whole corpus | 8 per period, 32 whole corpus | Chosen by seed stability (8, 11 and 15 tested) |
| Seed stability | Whole-corpus runs only | Every model | Extension |

**Not yet comparable:** the rubric coding (coherent, thematic, concentration) of all models, and a whole-corpus model with 8 topics (the counterpart of Gordon's k = 15 control).

## Visualizations

| Script | Reads | Writes |
|---|---|---|
| `modeling/14_generate_topic_explorer.py` | `models/baseline_lda_32/`, `data/output/stopword_removed/`, `config/topic_names_32.tsv`, template `modeling/topic_explorer_template.html` | `visualizations/topic_explorer.html` |
| `modeling/17_generate_period_explorer.py` | `models/period_lda_8/` (models and vectorizers), `data/output/stopword_removed/`, the per-topic CSVs of 16, `config/period_topic_names_8.tsv`, `config/chain_names_8.tsv`, template `modeling/period_explorer_template.html` | `visualizations/period_explorer.html` |

Both pages are self-contained HTML (open in a browser; internet needed only for the fonts). They are published with `visualizations/index.html` (a landing page linking both) on GitHub Pages by `.github/workflows/pages.yml`, which runs when anything in `project/visualizations/` changes on `main` (one-time setup: Settings → Pages → Source: GitHub Actions; Pages needs a public repository on a free GitHub plan). **Words shown: the 20 most relevant words of each topic** (relevance, Sievert & Shirley 2014, as in LDAvis: λ log P(word | topic) + (1 − λ) log(P(word | topic) / P(word)), λ = 0.6, `RELEVANCE_LAMBDA` and `relevant_words()` in `lda_common.py`; P(word) is the word's share of all words in the model's motions, per period for the period models). Ranked by probability alone, words frequent in many topics (*behov, stöd, förslag, hög, kvalitet*) fill the top of most clouds; relevance brings up the words specific to the topic (*csn, fribelopp* in study support, *funktionsnedsättning* in support for children). Central words such as *lärare, elev, barn* stay at the top of their own topics. λ = 0.6 is the value Sievert & Shirley found best for interpretation; lower values favour rare words of a few motions. Only the display changes: models, seed tests and alignment use the full distributions, and the seed-stability Jaccard uses the 20 most probable words. Word size is P(word | topic). Topics have Swedish names, an interpretation of each topic's top words and top motions: `config/topic_names_32.tsv` for the whole-corpus model (*Restämne* marks residual topics: unrelated words held together by a few motions) and `config/period_topic_names_8.tsv` for the period models, one name per period topic (*Blandat* marks broad topics without one clear theme). A name is shown only if the topic's three most probable words (not the most relevant ones shown) still match the file (`load_topic_names()`, `most_probable_words()` in `lda_common.py`), so a refitted model gets no wrong names. Named topics and chains are shown without their numbers.

### Topic explorer (whole-corpus model)
- **Per topic, two columns:** the word cloud (the 20 most relevant words, as in the period explorer) with the chart of its average share in each of the 11 electoral terms (1985–88 … 2022–26; `TERM_STARTS`, `term_of_session()` in `periods.py`; the tooltip gives the number of motions in the term) under it on the left; the top 10 motions (session, party, id, θ) on the right; stacked on narrow screens. The heading gives the overall share and the topic's **seed stability**: *high* if it is found again (matched cosine ≥ 0.70) in all 4 other seeds' models, *medium* in 3, *low* (gold) in 2 or fewer, with the count (e.g. *stability high (4/4)*). It is read from `results/BASELINE_STABILITY_32TOPICS_PER_TOPIC.csv` (09) and shown only if that test was run on the model shown: the CSV's topics must have the same 8 most probable words (`load_seed_stability()` in `lda_common.py`), so after a refit without 09 (`run_explorers.sh`) the chip is left out rather than shown for another model. Each top motion is shown with the party of its first signatory, under the party's name at the time. No party concentration on the page (it is counted in the deduplication comparison). No footer
- **Word size:** square root of P(word | topic), on **one scale for all clouds**, so sizes can be compared between topics; if a word does not fit, all clouds shrink together. A topic spread over many words has a smaller, sparser cloud. The tooltip gives the exact probability
- **Order:** most stable first (found again in 4, 3, 2 … of the other seeds' models), within the same stability by largest overall share; by share alone if the chip is not shown (topic numbers are arbitrary); no sorting or search controls and no explanation block on the page; this section describes what it shows

### Period explorer (period models)
- **8 topics per period,** the chosen count
- **Rows are chains.** The page has no explanation block; this section describes what it shows. Each period model has its own topics, so topic numbers do not correspond across periods. Topics of adjacent periods are matched one-to-one (Hungarian algorithm on cosine over the words both periods' vocabularies contain) and each row follows the matches from a topic of the first period to the last The chains have Swedish names from `config/chain_names_8.tsv`, shown only if the chain still consists of the same four topics
- **Chain heading:** the chain's name (no chain number) and the mean of its three links (*Average similarity*; Gordon's criterion: the chain holds if it is at least 0.50); no continuity label, weakest link or link summary, since the weak links are visible in the row. The similarity has two decimals, or three where two would round across 0.50
- **Weak links (additional information):** a single link below 0.50 breaks the row: the accent bar over the clouds stops, a dashed gold rule separates the cells and the cell reads *Alignment uncertain*. A chain can hold on the mean and still have one weak link
- **Per cloud:** the period, the topic's name (its number in the period model only in the tooltip), its share in percent (mean θ over the period's motions; explained in the introduction). Seed stability as a chip, as in the topic explorer (high / medium / low, from `results/period_stability/PERIOD_<period>_8TOPICS_PER_TOPIC.csv` of 16; shown only for the model the test was run on). The cosine of each link is not shown: a link is either strong or weak (below 0.50), and a weak one is marked in the row
- **Word colour = persistence within the chain:** in how many of the chain's four periods the word is among the 20 words shown: dark blue all four, medium blue three, light blue two, grey one. With 8 topics, 7% of the words shown are in all four periods and 54% in only one (with the 20 most probable words: 10% and 44%; relevance favours period-specific words). Bold marks the three most relevant words of each cloud
- **Word size:** square root of P(word | topic), on **one scale per chain**, so sizes can be compared across a chain's periods but not between chains; if a word does not fit, the chain's four clouds shrink together. The tooltip gives the exact probability
- **Order:** strongest chain first (mean link, high to low, ties by the weakest link); no sorting or search controls
- **Limitations:** the matching gives every topic a partner, so a topic that exists in only one period still sits in a chain, joined by weak links, and a topic that appears in a later period cannot start its own row. The permutation test (`18_alignment_null.py`) shows that each transition is far above chance, not that every link is the same theme

## Design Decisions

- **Stopwords vs. boilerplate.** Stopwords are general Swedish words, applied to the lemmatized, normalized text; boilerplate is parliamentary and domain-specific language (institutions, procedure, references), matched on the original word forms. Keeping them apart lets the stopword list be reused for other Swedish texts
- **Stanza lemmatization.** Swedish inflection splits one word into many forms (*skola, skolan, skolor, skolornas*), which fragments topics. Stanza is a general, context-aware lemmatizer run once on full sentences, with a small table of corrections for known errors. Known trade-offs: comparatives are reduced to the positive (*högre utbildning* → `hög utbildning`), rare compounds can get wrong lemmas (*arbetsvillkor* → `arbetsvillka`), and modal *ska* gets the lemma `skola` (handled by dropping auxiliaries). spaCy's `sv_core_news_sm` and a hand-made lookup table of education terms were tried and rejected
- **Body text only.** Appending the title 3× or 5× to the body gave only a small stability gain in an early test (earlier data, 44 topics), too small to justify an extra modelling choice. Titles are kept in the data
- **Topic count: 8 per period, 32 for the whole corpus.** 8 is the only tested count (8, 11, 15) at which at least half of the topics are stable in every period, and it has the highest mean cosine in every period; since the number of robust themes is about the same at every count, 8 loses little substance and avoids many chance topics. 11 topics fail the rule in three periods (36–45%), 15 in three periods (40%). The test (16 with `8 11 15`; reports in `docs/reports/topic_count_choice/`):

  | Period | 8 topics: mean cosine / stable | 11 topics | 15 topics |
  |---|---|---|---|
  | 1985/86–1993/94 | 0.79 / 5 of 8 (62%) | 0.64 / 4 of 11 (36%) | 0.61 / 6 of 15 (40%) |
  | 1994/95–2005/06 | 0.76 / 5 of 8 (62%) | 0.69 / 5 of 11 (45%) | 0.61 / 8 of 15 (53%) |
  | 2006/07–2013/14 | 0.78 / 6 of 8 (75%) | 0.70 / 5 of 11 (45%) | 0.62 / 6 of 15 (40%) |
  | 2014/15–2025/26 | 0.75 / 7 of 8 (88%) | 0.71 / 8 of 11 (73%) | 0.64 / 6 of 15 (40%) |
  | **All periods** | **23 of 32 (72%)** | **22 of 44 (50%)** | **26 of 60 (43%)** |

  The number of robust themes per period is about 4–8 at every count (8 → 15 adds 28 topics but only 3 stable ones), and the mean cosine falls with the topic count in every period. The test uses the per-period vocabularies, as the reported models. The 11- and 15-topic models are not kept; they can be refitted with `15_fit_period_lda.py <k>`. The whole-corpus model has the same total capacity as the four period models, as in Gordon (60 = 4 × 15)
- **Periods by electoral term, assigned by session** (see *Periods*): whole terms per period, as equal in size as the terms allow. In an early test (earlier data) four calendar-year bins of roughly equal size gave slightly less stable models and a weaker alignment; the differences were small
- **Vocabulary per period, compared over shared words** (Gordon's method; see *Period models* and *Topic matching*). In an early test (earlier data) one global vocabulary for all periods gave the same stability and a weaker alignment, as expected when words outside the shared vocabulary do not count
- **Whole-corpus vocabulary by the same rule:** words in at least 10 and at most 50% of all motions, no cap (13,860 words), as the period models, so that the two designs differ only in the time split and the topic count
- **Chain criterion:** Gordon's mean of the three links ≥ 0.50, so results are comparable with his; single weak links are shown as additional information

## Configuration Files

- **`config/boilerplate_phrases.txt`:** 467 explicit words/phrases, one per line, grouped by category with `#` headers. Matched against original word forms (body and title). An alternative file can be passed as the 3rd argument to `03_remove_boilerplate.py`. After editing, re-run steps 03–05 (no need to re-run Stanza)
- **`config/lemma_corrections.txt`:** corrections for known Stanza lemma errors, one `wrong correct` pair per line with `#` comments, applied in step 03 to body and title, case-insensitively. A wrong lemma with a leading `*` is also corrected at the end of a compound (`*kompet kompetens`: `gymnasiekompet` → `gymnasiekompetens`); mark an entry only after checking its compounds (`anslagen` must not be marked, because of *sammanslagen*). After editing, re-run steps 03–05
- **Stopwords:** hard-coded in `preprocessing/05_remove_stopwords.py` (NLTK base + supplementary list, including lemma forms)

## Corpus Size per Step

Body text of all 13,943 extracted motions (`analysis/corpus_statistics.py`, read-only); the vocabulary rows count the 10,692 modelled motions. Words are Stanza's tokens throughout, so every step is counted the same way: step 02 runs Stanza on the extracted text, so its word forms are the extracted text as Stanza splits it. A word is a token with at least one letter (punctuation and pure numbers are not counted); different words are counted case-insensitively.

| Step | Words | Different words | Words per motion (median / mean) |
|---|---|---|---|
| 01 Extraction (word forms) | 10,360,449 | 137,917 | 383 / 743 |
| 02 Lemmatization (lemmas) | 10,360,449 | 96,875 | 383 / 743 |
| 03 Boilerplate removed | 8,687,191 | 95,739 | 319 / 623 |
| 04 Normalized | 8,381,384 | 84,149 | 307 / 601 |
| 05 Stopwords removed (final text) | 4,205,154 | 83,939 | 152 / 302 |
| Whole-corpus model vocabulary (modelled motions) | 3,198,963 | 13,860 | 145 / 299 |
| Period models' vocabularies (together) | 3,044,432 | 9,954 | – |

- **Extraction:** Stanza keeps punctuation inside and next to some tokens, so the extracted text has spelling variants of the same word among its different words: abbreviations (*t.ex.*, *bl.a.*, *mot.*), party letters from "(m)" (*m)*, *s)*), and compound ellipsis (*läs-* in "läs- och skrivförmåga"). Steps 03 and 04 remove them
- **Lemmatization** reduces the number of different words by 30% (137,917 word forms to 96,875 lemmas) without removing any words: each word is replaced by its lemma (*skolan*, *skolorna*, *skolor* → *skola*), so word forms and lemmas are the same tokens and have the same count
- **Boilerplate removal** (with auxiliaries and multi-word abbreviation lemmas) removes 16% of the words but few different ones: the removed words are a small set of frequent parliamentary phrases
- **Normalization** removes digits, turns punctuation inside tokens into spaces (hyphenated lemmas are split: *it-kompetens* → *it*, *kompetens*; *1990-talet* → *talet*) and drops single characters: −3.5% words, −12% different words
- **Stopword removal** halves the number of words (−50%) but removes only 210 different words: stopwords are few and very frequent
- **The models' vocabularies** keep 87–91% of the words of the modelled motions' final text (3,498,931 words; whole corpus: 13,860 of 83,939 different words, 91% of the words; periods together 87%); most of the 83,939 are rare. Per period: 918,092 / 1,082,379 / 396,122 / 647,839 words in vocabularies of 6,875 / 7,344 / 3,952 / 5,107 different words

## Data Summary

| Metric | Value | Note |
|--------|-------|------|
| Motions | 13,957 | All UbU motions, sessions 1985/86–2025/26; 13,943 after the 14 placeholders |
| Modelled motions | 10,692 | Without 294 motions under 20 words, 644 later copies of duplicates and 2,313 near-duplicates |
| Periods | 4 | 1985/86–1993/94, 1994/95–2005/06, 2006/07–2013/14, 2014/15–2025/26 (2,026–3,467 modelled motions each) |
| Duplicates | 655 (4.70%) | Mostly resubmissions in later years; only the first copy modelled |
| Near-duplicates | 2,313 | ≥ 60% of three-word sequences shared with an earlier motion; mostly revised resubmissions |
| Vocabulary | Period models: 3,952–7,344 per period; whole-corpus model: 13,860 | ≥ 10 and ≤ 50% of the model's motions, no cap (Gordon) |
| Stopwords | NLTK (114) + 129 supplementary | |
| Boilerplate phrases | 467 | Explicit phrases, no wildcards |
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

**Fast rebuild (`run_explorers.sh`):** after a change to the preprocessing, refits both models and regenerates both explorers and the alignment test, skipping the seed tests, convergence check, topic-count test and deduplication comparison (a full run takes about 4½ hours; those belong in it once the preprocessing is settled). The start point depends on what changed; the whole-corpus and period models are fitted in parallel; stops at the first failing step; runs under `caffeinate`:

```bash
cd project
./run_explorers.sh 03          # boilerplate list or lemma corrections changed (~8 min)
./run_explorers.sh 05          # stopwords changed (~5 min)
./run_explorers.sh models      # data unchanged (~4 min)
./run_explorers.sh explorers   # only names or page design changed (~1 min)
```

A refit gives new topics, so names match only where the generators report it ("Topic names: 32 of 32"); the documentation's numbers stay those of the last full run.

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
python analysis/convergence_check.py          # 50 vs 200 passes; about 25 minutes
python analysis/corpus_statistics.py          # words per step, for the report (a few minutes; after 15)

# Whole-corpus model
python modeling/07_fit_baseline_lda.py        # about 3 minutes
python modeling/14_generate_topic_explorer.py
python analysis/09_test_lda_stability.py      # 5 seeds; under an hour

# Period models (each with its own vocabulary; independent of 07)
python modeling/15_fit_period_lda.py          # 8 topics; about 2 minutes
python analysis/16_seed_stability_periods.py  # 4 periods x 5 seeds = 20 fits; about 10 minutes
                                              # (with 8 11 15: the topic-count choice, about 35 minutes)
python modeling/17_generate_period_explorer.py
python analysis/18_alignment_null.py          # permutation test; seconds

# Deduplication comparison: no / exact / near duplicates removed (about 1.5 hours; independent of 07 and 15)
python analysis/dedup_comparison.py
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
  - **Relevance:** a word specific to a topic ranks above a more probable word that is just as frequent in the whole corpus; λ = 1 gives plain probability; the explorers show the relevant words while names match on the most probable ones; P(word) from word counts
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
├── run_explorers.sh                      (fast rebuild: preprocessing, models, explorers)
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
│   ├── count_duplicates.py               (duplicate and near-duplicate counts for the report)
│   ├── dedup_comparison.py               (models with no / exact / near duplicates removed, compared)
│   ├── convergence_check.py              (50-pass fits against 200 passes)
│   ├── corpus_statistics.py              (words and different words per step, for the report)
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
│   └── reports/                           (seed-stability reports of 09 and 16; period_stability/ per period; topic_count_choice/ the 8/11/15 test)
├── visualizations/                        (in git, published on GitHub Pages: index.html, topic_explorer.html, period_explorer.html)
├── results/                               (not in git: generated CSV tables)
├── data/                                  (not in git)
│   ├── input/extracted_text_xml/
│   └── output/{lemmatized,boilerplate_removed,normalized,stopword_removed}/
└── models/                                (not in git)
    ├── baseline_lda_32/
    └── period_lda_8/
```

## Open Points and Next Steps

**Preprocessing frozen (2026-10-27):** no further changes to stopwords, boilerplate, lemma corrections or the duplicate filters, so that the report, the explorers and this document describe one state.

**Plan to finish:**

1. **Final full run** from step 03 (2026-10-27, about 3 hours): the 0.6 near-duplicate threshold, the boilerplate *med anledning av* and *utgiftsområde* and the 25 lemma corrections for split words (*skolverket*/*skolverk* etc.); all models, seed tests (09, 16), convergence check, topic-count test (8 / 11 / 15), 15-topic alignment, and the deduplication comparison with four levels (none / exact / 0.8 / 0.6). **Done**
2. **After the run:** new topic and chain names; every number in this document updated; the stability chips appear in the explorers. **Done**; to be committed, after review, as the final version the report refers to
3. **Rubric coding, as Gordon (2026, §3.3):** every topic of the whole-corpus model (32) and the period models (4 × 8) coded by hand on
   - **coherence** (yes/no): the top words form a recognizable semantic field;
   - **thematic content** (yes/no, coherent topics only): the field is recurring subject matter, not a register, procedure or paratext;
   - **party concentration** (computed; Gordon's author concentration): share of the topic's top 5 motions whose first signatory belongs to the most frequent party among them (0.2–1.0).
   A script writes a **coding sheet** (one row per topic: model, period, number, name, the 20 most probable words, the titles of the top 5 motions, party concentration, empty columns for coherent and thematic). Coded by Rebecca as single annotator in one pass, before choosing chains for close reading (Gordon's procedure); the topic names are not part of the judgement. A second script reads the coded sheet and computes the shares (coherent, thematic, mean party concentration) per model, to compare with Gordon's Table 2 (coherence 80–85%; thematic 47% full corpus k = 15, 60–65% binned, 62% full corpus k = 60). No inter-annotator agreement: a limitation, as in Gordon
4. **Readability of the explorers** (display only, no effect on results)
5. **Report writing**

**Out of scope, to be stated as limitations or future work:**
- **Place names** are kept (Gordon removes proper names); some topics are organized around places (constituency signal)
- **Party analysis** beyond party concentration: which parties carry each topic, per period
- **Prominence trends** with the whole-corpus model (would rely on the stable topics only)
- **A whole-corpus model with 8 topics** as the counterpart of Gordon's k = 15 control
- **Algorithm:** scikit-learn online variational Bayes, not MALLET's Gibbs sampling; the study is an adaptation of Gordon's workflow, not a computational replication (to be confirmed with the supervisor). The 50-pass fits are checked against 200 passes (*Convergence check*)
- **Corpus defined by committee** (see *Data Source*): some motions are only partly about education
- **Residual topics:** a few topics of the whole-corpus model are held together by a few motions (*Restämne*)
