# Model Review: First Models on the Stanza Pipeline (2026-10-16)

First baseline and title-weighted 44-topic models fitted on the re-extracted, Stanza-lemmatized text. This review covers the run itself, the topics and the vocabulary. Fixes 1–4 at the end were made the same day, and steps 03–05 and both models were re-run; see **After the Fixes**.

> **Note (2026-10-16, later):** title weighting was dropped after the seed-stability runs and the weighted model's scripts (`10`, `11`) were removed; see `PIPELINE_DOCUMENTATION.md`, *Seed-Stability Results*. This review is kept as a record of both models.

## Run

| | Baseline (`07`) | Title-weighted 5× (`10`) |
|---|---|---|
| Motions | 13,913 | 13,913 (same motions) |
| Skipped | 4 withdrawn motions (title *Utgår*, no body text): GA02Ub336, GA02Ub352, GA02Ub619, GB02Ub665 | same 4 |
| Motions with a title | — | 13,897 (16 have no title words left after preprocessing) |
| Vocabulary | 10,000 words (baseline vectorizer, shared) | same vocabulary |
| Iterations | 50 / 50 | 50 / 50 |
| Training perplexity | not recorded (log overwritten, see below) | 2,096 |
| Fitting time | about 4 minutes | about 4 minutes |

- Both models were fitted on exactly the same motions after aligning the selection rule: motions whose final body text has no words are skipped in both (previously the weighted model kept them if they had a title).
- The baseline's perplexity line was lost from `data/logs/models.log`: the background process of an interrupted earlier run wrote its shutdown warnings into the same log file. The model itself was saved normally. Training perplexity is diagnostic only.
- Output: `results/44_TOPICS_FINAL.csv` (baseline), `results/weighted_44_TOPICS_FINAL.csv` (weighted), `results/document_topic_distribution.csv` (weighted; overwrites the baseline's, as documented).

## Topics

Most topics are clearly interpretable in both models. My reading of the top words (a judgement, not a measured score):

| | Baseline | Weighted |
|---|---|---|
| Clear education-policy topics | about 32 | about 32 |
| Mixed topics (rare words from unrelated motions, or procedural leftovers) | about 12 | about 12 |

**Clear topics found in both models** include teachers and teacher education, gender equality, bullying and children's wellbeing, independent schools and school choice, compulsory school and grades, upper secondary school, preschool and childcare, SFI and mother-tongue teaching, physical education and sport, adult and vocational education, student finance (CSN, studiemedel), research and doctoral education, health-care education, values and democracy in the curriculum, and budget appropriations.

**Weighted vs baseline:** the weighted model has more topics organized around **places** (Gävle/Sandviken, Kalmar/Härnösand, Karlstad/Värmland, Lund/Skåne, Göteborg/Umeå). Titles often name the place (*Högskoleutbildning i Gävle*), so 5× title weighting pulls these motions together. Whether that is useful depends on the research question: it separates regional higher-education localization motions well, but place names now dominate several topics.

**Mixed topics** (examples): weighted 12 (*prövning, bisexuell, mobiltelefon, registerutdrag, hörselskada*), 31 (*funktionshindrad, kd, treterminssystem, rymdstyrelse, vegansk*), 33 (*mälardalens, kränkning, kårobligatorium, rut*); baseline 12, 13, 23, 31, 32, 33, 37. These collect rare words from small groups of motions and are typical for a 44-topic model on this corpus. The seed-stability tests will show whether they are stable.

## Vocabulary Findings

### 1. Procedural words that slip through the boilerplate list

| Word in model | Comes from | Motions (final text) | Cause |
|---|---|---|---|
| `hemställa` | *hemställs* (5,020×), *hemställan* | 5,022 | *hemställs* is missing from `config/boilerplate_phrases.txt` |
| `anförd` | *anförda* (*det i motionen anförda*) | 4,346 | *anförda* is missing from the list |
| `motent` | *Mot.* (page header *Mot. 1988/89*) | 1,513 | *mot* is in the list, but the word form is *mot.*; see below |
| `propessor` | *prop.* | 215 | same: *prop* is listed, the form is *prop.* |
| `milj` | *milj.* (millions) | 415 | same: *milj* is listed, the form is *milj.* |
| `fp`, `mp`, `kd`, `sd` | party abbreviations | 796, 213, 164, 37 | party names are in the list, abbreviations are not; single-letter ones (*s*, *m*, *c*, *v*) are already removed as single characters |

The abbreviation cases (`mot.`, `prop.`, `milj.`) are a matching bug in step 03: Stanza keeps the full stop in the word form, and a word is only removed if the phrase match covers the **whole** word. *mot* matches but leaves the *.* uncovered, so the word stays and Stanza's guessed lemma (*motent*, *propessor*) ends up in the model.

### 2. Stanza lemmatizer errors on unknown words

Stanza guesses lemmas for words it has not seen in training, and some guesses are truncated. The mapping is consistent (every *kompetens* becomes `kompet`), so the model still groups the right documents, but the words look odd in topic lists, and in one case two forms of the same word are split:

| Lemma | From | Count |
|---|---|---|
| `kompet` | kompetens | 6,555 |
| `lärosät` | lärosäten, lärosätet | 3,037 |
| `anslagen` | anslaget (but *anslag* stays `anslag`: **split into two words**) | 2,827 |
| `läraryrk` | läraryrket | 1,096 |
| `trakasserie` | trakasserier | 949 |
| `handlingspla` | handlingsplan | 366 |
| `kåre` | kåren, kårerna | 230 |
| `spelregl` | spelregler | 98 |
| `barnsköta` | barnskötarna | 85 |
| `bibliotekarium` | bibliotekarier | 69 |

(Counts are word occurrences in the lemmatized text.)

### 3. Artifact stopwords (open item from `PREPROCESSING_ARTIFACTS.md`)

The extra stopwords added in `05_remove_stopwords.py` to hide extraction fragments were checked against the new text (motions containing each word, before stopword removal):

- **Fragment stopwords are no longer needed:** almost all occur in 0–6 motions (`ggare`, `ttre`, `rns`, `ngd`, `fj`, `jd`, `rb`, …: 0). The extraction fix removed the fragments.
- **Some remove real content words:** `fn` (FN, 336 motions), `eg` (EG, 213), `ky` (kvalificerad yrkesutbildning, 151), `ib` (International Baccalaureate, 34). These are relevant to education policy and are currently lost.
- **Correctly removed:** `de` (pronoun, also an NLTK stopword), `te` (*te sig*), `ub` (committee code), `ds` (government publication series), `of`, `osv`, `dvs`.

### 4. Remaining extraction fragments (accepted for now)

`skol` (189 motions), `ning` (180) and `utbild` (75) remain: line-end hyphenation in older motions (*utbild- Mot. 1988/89 ningsmoment*) and Swedish compound ellipsis (*skol- och språkexpertis*). None reach the top words of any topic. Left as is (decision 2026-10-16).

### 5. Output format

`08_display_lda_topics.py` and `11_display_weighted_lda_topics.py` write different CSV layouts: the baseline file labels topics `Topic 1` and interleaves word/probability columns; the weighted file labels topics `1` and lists all words, then all probabilities. Scripts reading both need to handle each format.

## Proposed Fixes (1–4 done 2026-10-16, 5 open)

1. **Boilerplate list:** add *hemställs*, *anförda*, and the party abbreviations (*fp*, *mp*, *kd*, *sd*, …).
2. **Step 03 matching:** let a word count as covered when the match covers it except for trailing punctuation, so *mot.*, *prop.* and *milj.* are removed. Add a unit test.
3. **Artifact stopwords:** remove the fragment stopwords that no longer occur, and take `fn`, `eg`, `ky`, `ib` off the list.
4. **Lemma corrections:** a small correction table for the most frequent Stanza errors (`kompet` → `kompetens`, `lärosät` → `lärosäte`, `anslagen` → `anslag`, …), applied in step 03. This is a deliberate, documented exception to "no hand-made lemma table": it corrects known errors of the general lemmatizer rather than replacing it.
5. **Display formats:** make 08 and 11 write the same CSV layout.

After 1–4, re-run steps 03–05 (minutes) and refit the models (about 10 minutes) before the stability tests.

## After the Fixes (2026-10-16)

Fixes 1–4 were made and the pipeline re-run twice (steps 03–05, sanity check, both models). The second run added the boilerplate phrase *milj.kr* (*miljoner kronor* written as one word: *milj.kr.* 227×, *milj.kr* 152×) and made the lemma corrections case-insensitive.

### Run

| | Baseline | Title-weighted 5× |
|---|---|---|
| Motions | 13,913 | 13,913 |
| Training perplexity | 2,174 | 2,105 |
| Sanity check | 0 failed, 3 warnings (4 withdrawn motions with no text; 34 motions with no title words; known hyphenation fragments) | |

The number of motions with no title words rose from 16 to 34. These titles were truncated in the source (*med anledning av prop. 1988/89:90 om*); the only word left before was Stanza's guess `propessor` for *prop.*, which is now removed. Body only is correct for them.

### Effect on the vocabulary

Motions containing each word in the final text:

| Word | Before fixes | After |
|---|---|---|
| `hemställa` | 5,022 | 6 |
| `anförd` | 4,346 | 2 |
| `motent` / `propessor` | 1,513 / 215 | 0 / 0 |
| `milj` | 415 | 0 |
| `fp` / `kd` / `mp` | 796 / 164 / 213 | 109 / 95 / 59 |
| `kompet` | 3,160 | 75 (`kompetens`: 3,429) |
| `fn` / `eg` / `ky` / `ib` | 0 (stopwords) | 336 / 213 / 151 / 34 |

None of `hemställa`, `anförd`, `motent`, `propessor`, `fp`, `kd`, `kompet` is among the top 20 words of any topic any more; the corrected forms (`kompetens`, `lärosäte`, `läraryrke`, `anslag`, `handlingsplan`) and the restored `fn`, `eg` are.

### Remaining: truncated lemmas inside compounds

The 75 remaining `kompet` were first attributed to sentence-initial capitals (*Kompetens*). That was wrong: Stanza already lemmatizes *Kompetens* to lowercase `kompet`, which the table corrects. The case-insensitive lookup is harmless but was not needed.

The real source is **compounds**, where the correction table (which matches whole lemmas) does not apply:

| Word form | Stanza lemma | Occurrences | Result in final text |
|---|---|---|---|
| *gymnasiekompetens* | `gymnasiekompet` | 195 | truncated word in the vocabulary |
| *lärarkompetens* | `lärarkompet` | 173 | truncated word |
| *yrkeskompetens* | `yrkeskompet` | 120 | truncated word |
| *HBT-kompetens*, *IT-kompetens*, *it-kompetens*, … | `hbt-kompet`, `it-kompet`, … | about 120 | split by normalization into `hbt`/`it` + `kompet` (the 75 motions) |

The same truncation probably affects compounds of the other corrected words (e.g. *-lärosäten*, *-handlingsplan*); not yet checked.

**Fix (done 2026-10-16):** corrections can now also apply to the **end** of a lemma, but only for entries marked with `*` in `config/lemma_corrections.txt`. An earlier version of this review claimed a suffix rule would be safe for every entry. A scan of all lemmas showed it is not: `anslagen` → `anslag` would turn *sammanslagen* (merged) into `sammanslag`. The compounds of each entry were therefore checked before marking it:

| Entry | Compounds found (tokens) | Marked `*` |
|---|---|---|
| `kompet` | 123 lemmas, 1,258 tokens (*gymnasie-, lärar-, yrkes-, högskole-, forsknings-, IT-, HBT-kompetens*) | yes |
| `bibliotekarium` | 4 lemmas, 51 tokens (*skol-, folk-, lärarbibliotekarier*) | yes |
| `anslagen` | *sammanslagen* (8): would be wrong | no |
| `stärk` | 8 lemmas, 11 tokens, mostly garbled forms (*.2stärk*, *•stärkt*) | no |
| `läraryrk` | 1 garbled token | no |
| other entries | none | no |

Steps 03–05 and both models were re-run with the fix, followed by the seed-stability tests.
