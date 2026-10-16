# Progress Seminar 1 (2026-10-19)

**Project:** Tracing Thematic Change in Swedish Parliamentary Motions on Education, 1986–2025
**Supervisor:** Murathan Kurfalı
**Main reference:** Gordon (2026), *Tracing Thematic Change in Early English-Language Science Fiction, 1818–1930*

This document summarizes where the project stands and lists the decisions that need to be made before the period models are fitted. Technical detail is in `PIPELINE_DOCUMENTATION.md` and `MODEL_REVIEW.md`.

---

## 1. Status

| Step | Status |
|---|---|
| Corpus | 13,917 UbU motions, 1986–2025, extracted from Riksdagens öppna data in four bins (3,770 / 3,313 / 3,577 / 3,257) |
| Extraction | Fixed: words split across HTML `<span>` elements had produced fragments (*uppföljni ng*) in 4,431 motions |
| Lemmatization | Stanza (Swedish, Talbanken), run once and saved; auxiliaries dropped so modal *ska* does not merge with the noun *skola* |
| Boilerplate and stopwords | 440 boilerplate phrases matched on original word forms; NLTK stopwords + 85 supplementary; known Stanza lemma errors corrected (`kompet` → `kompetens`) |
| Whole-corpus models | Baseline (body only) and title-weighted (titles 5×), 44 topics each, fitted on the same 13,913 motions (4 withdrawn motions have no text) |
| First review | About 32 of 44 topics clearly interpretable in both models (my reading); vocabulary fixes made and models refitted (`MODEL_REVIEW.md`) |
| Tests | 81 unit tests (preprocessing, topic matching, seed-stability code) and a sanity check of every pipeline stage |
| Not yet done | Seed-stability runs, period (binned) models, cross-period alignment |

---

## 2. Decisions to Make

### 2.1 Title weighting

**Question:** should title words be weighted, and if so how much?

- **Current setup:** the processed title is appended **5 times** to the body text. The title heading is removed from the body at extraction, so the title counts exactly 5×. A 3× variant is prepared for comparison.
- **Rationale:** a motion's title states its intent concisely (*Högskoleutbildning i Gävle*, *Lärarnas löner*), while bodies are long and mix many subjects. Weighting pulls document-topic inference towards the stated intent.
- **Observed effect:** the weighted model has more topics organized around **places** (Gävle/Sandviken, Kalmar/Härnösand, Karlstad/Värmland), because titles often name the place. Otherwise the two models' topics are of similar quality.
- **Concerns:**
  - Gordon does not weight titles (his documents are book chunks without titles), so this is a departure from the reference method.
  - The weight (3× or 5×) is a free parameter with no theoretical anchor.
  - Weighting changes the document-topic proportions θ, so any measure of prominence depends on it.
  - Titles are short, and 16–34 have no words left after preprocessing.
- **How to decide:** compare seed stability (baseline vs 3× vs 5×, tests ready) and manual topic quality. Options:
  - (a) no weighting, following Gordon;
  - (b) weighted model as primary;
  - (c) baseline as primary, weighted as a robustness check.
- **Also to decide:** whether the period models are weighted the same way.

### 2.2 Shared vocabulary for cross-period alignment

**Question:** how to guarantee that topic-word vectors from different period models refer to the same words in the same order (supervisor's comment)?

- **Already guaranteed in code:** the matching code refuses to compare models whose vocabularies differ or are ordered differently (tested).
- **Option A, one global vocabulary:** one vectorizer built on the whole corpus and used for every period model. Simple and works with the existing code. Frequency thresholds apply to the whole corpus.
- **Option B, Gordon's method:** each period model has its own vocabulary (thresholds per period). Adjacent periods are compared over the **intersection** of their vocabularies, re-normalized. This replicates Gordon and keeps period-specific words in each period's model, but needs a small extra alignment step.
- **Leaning:** B, since the proposal follows Gordon.

### 2.3 Comparing the whole-corpus baseline with the binned models

**Question:** what does "baseline comparison" (one of the proposal's three evaluation criteria) mean concretely?

- **Gordon's approach:** compare full-corpus and binned models on the same quality dimensions (coherence, thematic content, author concentration). He fits the full corpus at k = 15 (per-bin count) and k = 60 (4 × 15). His conclusion is that binning does not give better topics, but it is the only way to do diachronic alignment. Our 44 ≈ 4 × 11 follows the same logic.
- **Possible extension:** map each period topic to its most similar whole-corpus topic (cosine). This shows which whole-corpus themes appear in which period, and which period topics have no counterpart.
- **To decide:** quality comparison only (as Gordon), or also the mapping.

### 2.4 What "thematic change" means

**Question (supervisor):** does thematic change mean changes in topic vocabulary, in how prominent a theme is, or both?

- **Vocabulary change:** how the words of an aligned topic chain shift across periods. This is what Gordon measures (cosine along chains, top words, top documents).
- **Prominence:** how much of the motions' attention a theme receives in each period. Gordon does not measure this.
- **Proposal:** both, kept as two separate measures. A theme can keep its vocabulary and grow, or keep its share and change its vocabulary.
  - **Vocabulary change** from the period models.
  - **Prominence** from the whole-corpus model, whose topic definitions are fixed over 1986–2025. Period models' proportions are not comparable across periods, because each period's topics sum to 1 over its own topics.
- **If prominence is included,** decide how θ is summarized per period:
  - **Main measure:** the mean topic proportion over the period's motions, prevalence(k, p) = (1/N_p) Σ_d θ_dk. Every motion counts equally (a motion is one political act), rather than weighting by length.
  - **Robustness:** the share of motions where the topic is dominant, and the spread across random seeds.
  - **Resolution:** per period, or per year (the whole-corpus model allows yearly curves).
  - **Model:** state which model θ comes from (weighted or not, see 2.1).

### 2.5 Statistical evidence for alignment

**Question:** how to show that cross-period alignments are more than chance?

- **Gordon:** compares the matched mean cosine with a null distribution of 1,000 random permutation matchings per transition, reported as z-scores. Chains are kept if mean cosine is at least 0.50 across all transitions and the topic is thematic in every bin.
- **Proposal:** adopt both, so that results are comparable with Gordon. Not implemented yet.

### 2.6 Manual evaluation rubric

**Question:** how to make the "manual assessment of coherence and interpretability" systematic?

- **Gordon's rubric:** each topic coded as **coherent** (top words form a semantic field), **thematic** (coherent and about subject matter rather than register or paratext), and **author concentration** (share of the topic's top 5 documents from its dominant author). The coding uses top words plus the top 5 highest-loading documents.
- **Parliamentary analogue of author concentration:** **party or MP concentration** among a topic's top 5 motions. This separates genuine policy themes from one party's or one MP's signature. Author and party metadata are in the data.
- **To decide:** adopt the rubric; whether a second annotator codes a sample (Gordon lists the single annotator as a limitation).

### 2.7 Proper names and place names

**Question:** remove proper names, as Gordon does?

- In the weighted model several topics are dominated by place names. In parliament these are partly real content (where universities are located), but they are also close to Gordon's author signal: MPs propose things for their own constituency.
- Stanza tags proper nouns (`PROPN`), so removing them, or keeping them, is a one-line choice in step 03 and can be tested.

### 2.8 Number of topics

**Question:** keep 44 for the whole corpus and about 11 per period?

- 44 was chosen from topic-concentration testing (not semantic coherence) on the earlier pipeline. 44 ÷ 4 = 11 per bin. Gordon uses 15 per bin and tests the full corpus at 15 and 60.
- About 12 of the 44 whole-corpus topics are mixed (rare words from unrelated motions). This may argue for fewer topics, or it may simply be the long tail of a heterogeneous corpus.
- The proposal time-boxes topic-number testing; to decide how many values to try.

### 2.9 Temporal bins

**Question:** keep bins of roughly equal size?

- **Current bins:** 1986–1993, 1994–2004, 2005–2014, 2015–2025, chosen for roughly equal numbers of motions, as in the proposal.
- Gordon chose literary-historical periods. A political alternative would follow changes of government (1991, 1994, 2006, 2014, 2022) or major school reforms (kommunalisering 1991, friskolereformen 1992, Lgr11 2011).
- The current bins already roughly follow 1994, 2006 and 2014; 1986–1993 spans the 1991 shift.

### 2.10 Departures from the proposal and from Gordon (to state in the methods)

| Choice | Proposal / Gordon | Now | Status |
|---|---|---|---|
| Lemmatization | Proposal: follow Bruinsma & Johansson (no stemming); Gordon: none | Stanza lemmatization; a small table corrects known Stanza errors | Decided; needs justification (Swedish morphology) |
| LDA implementation | Gordon: MALLET, Gibbs sampling, 1,000 iterations, asymmetric priors | scikit-learn, online variational, 50 passes, symmetric priors, no convergence check | Open: keep or switch |
| Document unit | Gordon: 1,000-word chunks | Whole motions | Decided (motions are natural units) |
| Duplicates | Proposal: investigate and monitor | Counted for the report, not removed (133 on the earlier pipeline; to recount) | Decide: keep or drop |
| Seed stability | Gordon: whole-corpus runs only | Hungarian-matched stability for every model, binned included | Extension |

### 2.11 Smaller open points

- **Billions:** whether *miljard/miljarder* (about 1,300 occurrences) should be removed like *miljoner*.
- **Leftover fragments:** some remain from line-end hyphenation in older motions (`ning`, `utbild`). Accepted for now.
- **Party abbreviations:** a few remain in 59–109 motions (`fp`, `kd`, `mp`, probably from forms like *kd-ledamöter*).

---

## 3. Next Steps

1. Run the seed-stability tests (baseline, 3×, 5×) and decide on title weighting (2.1).
2. Settle the alignment design (2.2, 2.5) and the definition of thematic change (2.4).
3. Implement and fit the period models, the alignment with permutation null, and the chains.
4. Manual evaluation with the rubric (2.6) within the proposal's four-week time box.
5. Report writing (Nov.–Dec.).
