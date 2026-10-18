# Progress Seminar 1 (2026-10-19)

**Project:** Tracing Thematic Change in Swedish Parliamentary Motions on Education, 1986–2025
**Supervisor:** Murathan Kurfalı
**Main reference:** Gordon (2026), *Tracing Thematic Change in Early English-Language Science Fiction, 1818–1930* (NLP4DH 2026)

This document summarizes where the project stands and sets out the decisions that need to be made before the period models are fitted. Each decision has:

- the background;
- the options, explained;
- what each option would mean for the results;
- a suggestion where I have one;
- the questions to discuss.

Technical detail is in `PIPELINE_DOCUMENTATION.md` and `MODEL_REVIEW.md`.

**Contents**

0. Att få svar på under seminariet
1. Status
2. Decisions to make
   - 2.1 Title weighting (decided: not used)
   - 2.2 Shared vocabulary for cross-period alignment (decided: per period, as Gordon)
   - 2.3 Comparing the whole-corpus model with the period models
   - 2.4 What "thematic change" means: vocabulary, prominence, or both
   - 2.5 Statistical evidence for cross-period alignment
   - 2.6 Manual evaluation rubric
   - 2.7 Proper names and place names
   - 2.8 Number of topics (decided: 8 per period, 32 for the whole corpus)
   - 2.9 Temporal bins (decided: electoral terms, by session)
   - 2.10 Departures from the proposal and from Gordon
   - 2.11 Smaller open points
3. Questions for the seminar (summary)
4. Next steps

---

## 0. Att få svar på under seminariet

The questions below are the ones to settle at the seminar: 0.2 and 0.3 decide whether the period models have to be re-fitted again (0.1 is decided), and 0.4 decides how the study relates to Gordon. Everything else in section 2 can be settled later. For each: what has to be decided, what each answer means in practice, and what I would do by default if there is no clear answer.

### 0.1 Vocabulary for the period models (details in 2.2)

**Decided 2026-10-18: Gordon's method.** Each period model has its own vocabulary, built within the period (words in at least 10 and at most 50% of the period's motions, no size cap: 4,926–7,981 words). Adjacent periods are compared over the words both vocabularies contain (4,236–5,464 per transition).

- **Effect, at 8 topics:** stability unchanged (21 of 32 topics stable); the alignment is stronger (matched mean cosine 0.67, 0.78, 0.76 against 0.65, 0.69, 0.67 with one global vocabulary), as expected when words outside the shared vocabulary no longer count. All 8 chains hold, 4 with every link ≥ 0.50.
- **Vocabulary change outside the shared words** is reported separately: on average 3.5–9.8% of a topic's weight falls on words outside the vocabulary shared with the neighbouring period.
- **At Gordon's 15 topics** (fitted once for the comparison): 0.43, 0.60, 0.62 against his 0.44–0.59; 9 of 15 chains hold against his 7.
- **Question:** is the share of weight outside the shared words a sufficient report of vocabulary change?

### 0.2 Place names (details in 2.7)

**To decide:** what to do with place names such as *Skövde, Umeå, Karlstad, Södertörn*.

- **Why it matters:** about 8 of 44 whole-corpus topics are organized around places, coming from motions about universities and programmes in a particular region. They are also among the least stable topics across seeds. In the period models (8 topics each) such topics would take a larger share, and cross-period chains could follow towns rather than themes.
- **Options:**
  1. **Keep** (current). Regional distribution of higher education stays visible, including which regions were discussed.
  2. **Drop all proper nouns** (`PROPN`). Simplest (one line in step 03), closest to Gordon, but also removes *Sverige*, *EU*, *SOU*, *UHÄ* and organization names.
  3. **Drop only place names**, from a list of municipalities, regions and towns. Keeps *Sverige*, *EU* and organizations.
  4. **Merge place names into one token** (e.g. `ort`). The model still sees that a motion is regional, without splitting the theme by town.
- **In practice:** options 2–4 change step 03 and require re-running 03–05 (minutes) and the models; option 3 or 4 needs a place-name list.
- **Default without a clear answer:** option 4, which keeps the regional theme as one theme. Option 3 as the second choice.
- **Questions:** Are place-name topics a theme (regional higher-education policy) or noise (constituency representation, like Gordon's author signal)? Is removing or merging place names a departure from Gordon worth making?

### 0.3 Remaining vocabulary leftovers (details in 2.11)

**To decide:** two small cleaning questions, best settled before the period models so the models do not have to be re-fitted.

- ***miljard/miljarder*** (about 1,300 occurrences). *miljon* and its abbreviations are already removed as boilerplate, since an amount says nothing about the theme.
  - *Remove:* consistent with *miljon*.
  - *Keep:* it may signal budget motions, which can be a theme of their own.
  - *Default:* remove, for consistency with *miljon*.
- **Party abbreviations `fp`, `kd`, `mp`** remaining in 59–109 motions, probably from compounds such as *kd-ledamöter*. The standalone abbreviations are already removed as boilerplate.
  - *Remove:* party is not a theme, and party names are already removed.
  - *Keep:* the counts are small and none reaches a topic's top words.
  - *Default:* remove, by adding them as stopwords at step 05.
- **In practice:** both are one-line changes to the boilerplate or stopword list followed by re-running 03–05 (minutes).
- **Question:** remove both, as with *miljon* and the party names?

### 0.4 Implementation: adaptation or replication of Gordon? (details in 2.10)

**To decide:** whether the study keeps scikit-learn and is presented as an adaptation of Gordon's workflow, or switches to MALLET to replicate his computation.

- **Current plan: keep scikit-learn and frame the study as an adaptation.** Proposed wording:
  > The study follows Gordon's (2026) framework of temporally binned LDA and cross-period topic alignment, but adapts its implementation. Models are fitted with scikit-learn's online variational Bayes rather than MALLET's Gibbs sampling, and with symmetric rather than optimised asymmetric priors. The results should therefore be read as an adaptation of the workflow to Swedish parliamentary text, not as a direct computational replication. Differences from Gordon's results may reflect the implementation as well as the corpus.
- **What the adaptation means:** the study can show that the workflow transfers to political text, but not whether Gordon's method itself gives the same kind of results there, since differences may come from the corpus or from the implementation. Gordon's own reason for MALLET is practical: his Authorless step is a MALLET transform (`DownsampleLabelWords`), and he optimises asymmetric priors, which scikit-learn does not offer.
- **Related choices:** the vocabulary now follows Gordon (0.1), so the algorithm is the main remaining difference. Convergence of the 50-pass fits is not checked; with scikit-learn kept, a convergence check (a 200-pass fit and a second seed, about 30 minutes) would answer the obvious examiner question.
- **Alternatives:** switch to MALLET with Gordon's settings (refit all models and stability tests, a few days), or keep scikit-learn and fit MALLET once for the 8-topic period models as a sensitivity check.
- **Questions:** Is the adaptation framing acceptable for the thesis? Is the convergence check needed?

---

## 1. Status

### 1.1 Corpus

13,957 motions referred to the Committee on Education (UbU), parliamentary sessions 1985/86–2025/26, from Riksdagens öppna data, in four periods of complete electoral terms (2.9):

| Period | Sessions | Motions |
|---|---|---|
| 1 | 1985/86–1993/94 | 4,029 |
| 2 | 1994/95–2005/06 | 3,477 |
| 3 | 2006/07–2013/14 | 2,879 |
| 4 | 2014/15–2025/26 | 3,572 |

4 withdrawn motions (titled *Utgår*) have no text, so the models use 13,953.

### 1.2 Preprocessing pipeline (done)

1. **Extraction** from the XML: body text and title. Signatures, headers, the title heading, motion numbers and the motion's own author names are removed.
   - **Bug found and fixed:** the source HTML often splits single words across `<span>` elements (*uppföljni*/*ng*), and the old extraction joined the pieces with a space. That produced word fragments (`ning`, `skol`, `utbild`) in 4,431 motions.
   - Soft hyphens and broken diacritics (*ma°ste*) are repaired.
2. **Lemmatization with Stanza** (Swedish Talbanken model), run once and saved. It took about 5 hours on a laptop.
   - Every word is stored with its original form, lemma and part of speech, so the later steps can be re-run in minutes.
   - **Auxiliaries are dropped,** because Stanza lemmatizes the modal *ska/skall* to `skola`, which would merge with the noun *skola* (school).
3. **Boilerplate removal:** 440 parliamentary phrases (*med anledning av*, *hemställs*, party names, …), matched on the original word forms.
   - Abbreviations that Stanza expands into multi-word lemmas (*t.ex.* → `till_exempel`) are dropped and counted for review.
   - A short table corrects known Stanza lemma errors (*kompetens* → `kompet` → corrected to `kompetens`).
4. **Normalization:** lowercase; no digits, punctuation or single letters.
5. **Stopwords:** NLTK's Swedish list (114) plus 85 supplementary words, including their lemma forms.

### 1.3 Whole-corpus models (first version, done)

- **Two models, 44 topics each:**
  - a **baseline** on body text only;
  - a **title-weighted** model, with title words appended 5 times. Title weighting was dropped after the seed-stability runs (2.1); the model used from now on is the baseline.
- Both use the same motions and the same 10,000-word vocabulary.
- **First review** (`MODEL_REVIEW.md`): roughly 32–34 of 44 topics in each model are clear education-policy topics, and about 10 are mixed. This is my reading, not a measured score.
  - **Clear topics** include teachers and teacher education, independent schools and school choice, preschool, upper secondary and vocational education, student finance (CSN), SFI and mother-tongue teaching, research and doctoral education, physical education, special needs, values and the curriculum, and bullying.
  - **Mixed topics** collect rare words from unrelated motions, e.g. *homosexuell, helårsstudent, folkmord, takbelopp, cancerfond*.
- **Vocabulary problems** found in the review were fixed and the models refitted. Leftover procedural words (*hemställa*, *anförd*, *motent* from *Mot.*) dropped from 1,500–5,000 motions each to almost none.

### 1.4 Quality assurance

- **81 unit tests:**
  - preprocessing rules;
  - topic matching;
  - the seed-stability code, including a check that the models and the stability tests can never use different settings.
- **A sanity check of every pipeline stage:** same motions in every stage, no leftover stopwords or punctuation.

### 1.5 Not yet done

- The period (binned) models.
- Cross-period alignment and topic chains.
- Manual evaluation.

---

## 2. Decisions to Make

### 2.1 Title weighting

**Question:** should title words be given extra weight, and if so how much?

**Decided 2026-10-16: no title weighting.** The seed-stability runs (5 seeds, 10 matched pairs each) gave:

| | Body text only | Title ×5 | Title ×3 |
|---|---|---|---|
| Mean matched cosine | 0.525 | 0.539 | 0.539 |
| Range of the 10 per-pair means | 0.486–0.566 | 0.506–0.573 | 0.521–0.554 |
| Mean Jaccard (top 20) | 0.24 | 0.24 | 0.23 |
| Topics found in all 4 other seeds (cosine ≥ 0.70) | 5 | 7 | 10 |

Weighting raises stability only slightly, and the ranges overlap, so it is not clearly better (step 3 of *How to decide* below). Option (a) was chosen: the model uses body text only, which follows Gordon and removes a free parameter. Titles are still separated at extraction, preprocessed and kept in the data (`title_processed`) for later use. The weighting code was removed and is in the git history. Full results: `PIPELINE_DOCUMENTATION.md`, *Design Decisions*; full results in `docs/reports/`. The background and arguments below are kept as the reasoning behind the decision.

**For the seminar:** is dropping weighting acceptable, or should the weighted model be reported as a robustness check after all?

#### Background

A motion's title states its intent in a few words (*Högskoleutbildning i Gävle*, *Lärarnas löner*, *Simundervisning i skolan*). The body is longer and often covers several subjects: background, arguments, related reforms, budget. LDA treats every word equally, so a motion whose body discusses many things gets a spread-out topic mixture even when its purpose is narrow.

**Current setup:**

- The processed title is appended **5 times** to the body before the document is counted.
- The title heading that opens every motion body is removed at extraction, so the title counts exactly 5 times (plus any genuine mentions of the title phrase in the argument).
- A 3× variant is prepared for comparison.

#### How large the effect is

After preprocessing, a title has a median of **3 words** and a body a median of **169 words** (mean 331).

| | Title share of the document's words |
|---|---|
| No weighting | about 1.7% (median) |
| 5× weighting, median motion | 7% |
| 5× weighting, mean | 9% |
| 5× weighting, shortest bodies (top 10%) | 17% or more |
| 5× weighting, longest bodies (bottom 10%) | 1.6% or less |

So the weighting is **moderate for a typical motion but strong for short motions**, and almost irrelevant for very long ones. The effect is not uniform. It depends on body length, which also differs between periods (median body length 183, 196, 143 and 159 words in the four periods), though without a simple trend.

#### What we have observed

- The two models' topics are of similar quality.
- Both have several topics organized around places, about 8 each, e.g. *Skövde, Västsverige, Skaraborg* and *Örebro, Karlstad, Värmland*. Titles often name a place (*Högskoleutbildning i Gävle*). In the first version the weighted model had more of these, but after the vocabulary fixes the difference is small.
- The decisive evidence, seed stability, has not been run yet.

#### Arguments

| For weighting | Against weighting |
|---|---|
| Pulls each motion's topic mixture towards its stated purpose | Gordon does not weight titles (his documents are 1,000-word book chunks without titles), so it is a departure from the reference method |
| Parliamentary titles are written by the authors as a summary, a strong signal | The weight (3× or 5×) is a free parameter with no theoretical anchor; it must be justified empirically |
| May stabilize topics across seeds (to be tested) | Effect varies with body length, which differs between periods, a possible confound for diachronic comparison |
| | Changes θ (document-topic proportions), so any prominence measure (2.4) depends on it |
| | 16–34 motions have no title words left after preprocessing and get no weighting |

#### Options

- **(a) No weighting.** Follows Gordon and is simplest to justify. The weighted models become a reported sensitivity check, or are dropped.
- **(b) Weighted model as the primary model** (3× or 5×), chosen on evidence.
- **(c) Baseline as primary, weighting as a robustness check.** Results are reported for the baseline, and the weighted model shows whether conclusions change.

#### How to decide

1. Run the seed-stability tests: baseline, 3×, 5×, each with 5 seeds and 10 matched pairs. Higher matched cosine and Jaccard means more stable topics.
2. Compare manual topic quality with the rubric in 2.6.
3. If weighting is not clearly better on both, choose (a) or (c).

**Also to decide:** if weighting is kept, whether the period models are weighted the same way. They should be, for consistency.

**Suggestion:** decide after the stability runs. Lean towards (c) unless weighting is clearly more stable, since (c) keeps the main analysis close to Gordon.

---

### 2.2 Shared vocabulary for cross-period alignment

**Question (supervisor):** how to guarantee that topic-word vectors from separately trained period models refer to the same words in the same order before computing cosine similarities?

**Decided 2026-10-18: option B, Gordon's method** (results in 0.1). Implemented in `topic_matching.py` (`shared_vocabulary=True`): both topic vectors are restricted to the words in both vocabularies and put in the same order before cosine is computed; covered by unit tests (the same topics in different vocabularies and column orders match with cosine 1; weight outside the intersection does not change the cosine). Seed stability still compares models with one vectorizer, and different vocabularies remain an error there. The options below are kept as the reasoning.

#### Why it matters

A topic is a vector of word probabilities. Cosine similarity compares two vectors position by position. If position 512 is *lärare* in one model and *elev* in the other, the similarity is meaningless, and nothing in the arithmetic would show it. Separately trained models build their own vocabularies, so their columns do not line up by default.

**Already guaranteed in code:** the matching module refuses to compute similarities unless both models have an identical vocabulary in identical order. Different or reordered vocabularies raise an error, and both cases are covered by unit tests. A misaligned comparison cannot pass silently. The question is which design produces aligned vectors.

#### Option A: one global vocabulary

- One vectorizer is built on the whole corpus.
- Every period's motions are converted with that same vectorizer before its LDA model is fitted.
- All period models therefore have exactly the same columns.

**Consequences:**

- Simple, and works with the existing code.
- Frequency thresholds (a word must occur in at least 5 motions and at most 50%) apply to the **whole corpus**:
  - A word frequent in one period but rare overall is still included.
  - A word in more than half of all motions is excluded everywhere.
- A word that does not occur in a period still has a column in that period's model, with near-zero weight (only the LDA prior). Period-specific words therefore lower the cosine between periods. That is a correct reflection of vocabulary change, but it should be kept in mind when interpreting the values.

#### Option B: per-period vocabularies, compared over shared words (Gordon's method)

- Each period model gets its own vocabulary, with the frequency thresholds applied **within the period**.
- When two adjacent periods are compared, both topic vectors are restricted to the **intersection**: the words present in both vocabularies, put in the same order, and re-normalized. Gordon uses L2 normalization over the shared vocabulary.

**Consequences:**

- Replicates Gordon, which is what the proposal promises.
- Each period's model is built on its own most relevant words. A word typical of 2014/15–2025/26 (*digitalisering*, *nyanländ*) is not crowded out by thresholds computed over 40 years.
- The comparison only uses words both periods know, so similarity measures **how the shared vocabulary is used**, not whether new words appeared. Vocabulary that appears or disappears has to be reported separately (e.g. the share of a topic's probability mass outside the intersection).
- It needs a small extra step that builds the intersection and reorders both vectors. The existing safety check still applies at the moment cosine is computed.

**Suggestion:** **B**, since the proposal follows Gordon. Report the share of each topic's mass that falls outside the shared vocabulary, so that vocabulary change is not hidden.

---

### 2.3 Comparing the whole-corpus model with the period models

**Question (supervisor):** the proposal lists "baseline comparison" as one of three evaluation criteria. How exactly will the whole-corpus model be compared with the binned models?

There are two complementary answers. The first is Gordon's, and it compares **quality**. The second is an extension that compares **content**.

#### 2.3.1 Gordon's way: compare model quality on the same rubric

**What Gordon fits:**

| Configuration | Topics | Purpose |
|---|---|---|
| Binned: four period models, k = 15 each | 60 | The main analysis |
| Binned with Authorless preprocessing | 60 | Reduces author-specific vocabulary |
| Full corpus, k = 15 | 15 | Same number of topics as **one** bin |
| Full corpus, k = 60 | 60 | Same **total** number of topics as all four bins |

Fitting the full corpus at two sizes separates two questions: "is binning better?" and "is the comparison just about having more topics?" The k = 60 model gives the full corpus the same total capacity as the four bins together.

**How he compares them:**

- **Same rubric for all models.** All 195 topic instances are coded on the three dimensions described in 2.6 (coherent, thematic, author concentration), with the same procedure and the same annotator.
- **Table of shares.** The result is a table of shares per configuration:

| Model | Coherent | Thematic | Author concentration |
|---|---|---|---|
| Full corpus k = 15 | 80% | 47% | 0.680 |
| Full corpus k = 60 | 80% | 62% | 0.707 |
| Binned | 85% | 60% | 0.807 |
| Binned + Authorless | 83% | 65% | 0.727 |

**His conclusion:**

- **Binning does not produce better topics.** A full-corpus model with enough topics (k = 60) is about as coherent and thematic as the binned models.
- **Binning has a different value: temporal structure.** A single full-corpus model has one set of topics for the whole period, so it cannot show a theme emerging, changing its vocabulary, or receding. Only the binned models can be aligned across periods.
- **His initial whole-corpus runs were also unstable** across random seeds (mean Jaccard 0.26–0.31), which further motivated binning.

**What this means for us:**

- Our whole-corpus 32 topics = 4 bins × 8 topics (44 = 4 × 11 before 2.8 was decided). That is the same logic as Gordon's k = 60 = 4 × 15: equal total capacity.
- To mirror him fully we would also fit a whole-corpus model at k = 8, matching one bin.
- We code all topics with the same rubric and report a table like his: whole-corpus k = 32, whole-corpus k = 8, and the four period models.
- **Our addition:** seed stability for every configuration. Gordon reports it only for the initial whole-corpus runs and lists it as a limitation.

**What it answers:**

- Does binning cost topic quality? (If the period topics are much less coherent, the bins may be too small.)
- Is the whole-corpus model a reasonable reference?

**What it does not answer:** whether the models found the **same themes**. Two models can be equally good and still find different things. That is what the extension addresses.

#### 2.3.2 Extension: map each period topic to the whole-corpus topics

**Idea:** the whole-corpus model has one fixed set of 32 topics for all sessions. Each period model has its own 8. Mapping every period topic to its most similar whole-corpus topics relates the two descriptions of the same corpus.

**How it would be done:**

1. **Common vocabulary.** The period topics and the whole-corpus topics must be compared over the same words in the same order, as in 2.2: the intersection of each period's vocabulary with the whole-corpus vocabulary.
2. **Similarity matrix.** For each period, compute the cosine similarity between each of its 8 topics and each of the 32 whole-corpus topics, giving an 8 × 32 matrix.
3. **Record the matches.** For each period topic, record its best-matching whole-corpus topic and the cosine, plus the second- and third-best.
4. **Threshold.** A match counts only if the cosine is at least a threshold, e.g. 0.50 (the value Gordon uses for chains), or a value calibrated against a permutation null as in 2.5.

This is **not** one-to-one matching: several period topics may map to the same whole-corpus topic. That is intended, because the granularities differ (8 against 32).

**What it shows:**

1. **Presence over time.** A table of whole-corpus topics × periods, marking where a matching period topic exists. It shows which themes are present in every period and which only in some.
2. **Period-specific themes.** A period topic with no whole-corpus match above the threshold is a theme the whole-corpus model did not capture as its own topic, because it was too short-lived or absorbed into broader topics. Each such case is direct evidence for binning, in addition to Gordon's argument.
3. **Granularity.** A broad period topic often spreads over two or three narrower whole-corpus topics. The second- and third-best matches show this, e.g. a 1985/86–1993/94 topic covering both *barnomsorg* and *förskola* might match the preschool topic and the family-policy topic.
4. **A check on the chains.** If a chain (2.5) is a real recurring theme, its topics in the four periods should map to the same or closely related whole-corpus topics. A chain whose links map to unrelated whole-corpus topics suggests the alignment joined different themes, and should be read with caution.
5. **A bridge to prominence (2.4).** Prominence is measured with the whole-corpus topics. The mapping connects a chain (from the period models) to the whole-corpus topic whose prevalence curve shows how large the theme was in each period. Vocabulary change and prominence can then be reported for the same theme.

**Example from the current model:** the whole-corpus model has a clear preschool topic (*barn, förskola, förälder, barnomsorg, verksamhet, kommun, pedagogisk, personal, fritidshem, förskollärare*).

- We would expect each period to have a matching childcare/preschool topic.
- The cosine against the whole-corpus topic, and the words that differ, would show how the vocabulary moved. For example, from *barnomsorg* and *daghem* towards *förskola*, *läroplan* and *förskollärare* after preschool got its own curriculum in 1998.
- (This is an expectation to test, not a result.)

**Caveats:**

- Because the granularities differ, cosine values between an 8-topic and a 32-topic model are generally lower than between two models of the same size. The threshold should be set with that in mind, ideally from a null distribution.
- The whole-corpus topics are themselves averages over 40 years. A theme whose vocabulary changed strongly may be split across several whole-corpus topics, or represented by a mix.
- **Effort:** small. The existing similarity function already handles models with different numbers of topics.

**Suggestion:** do both. Gordon's quality comparison is the main "baseline comparison" and keeps the study comparable with his. The mapping is a modest extension that strengthens the argument for binning and connects the two halves of 2.4.

---

### 2.4 What "thematic change" means: vocabulary, prominence, or both

**Question (supervisor):** does thematic change mean changes in topic vocabulary, in how prominent a theme is, or both? If prominence, how are the document-topic proportions summarized within each period?

#### Two different kinds of change

- **Vocabulary change:** a theme persists but is talked about differently. School choice in the 1990s might be framed with *valfrihet, friskola, skolpeng*, and in the 2010s with *vinst, huvudman, skolinspektion*.
- **Prominence change:** a theme takes up more or less of parliament's attention. Motions about the theme become more or fewer, or the theme fills a larger part of each motion.

The two are independent. A theme can keep its vocabulary while growing, or keep its share while its vocabulary changes. Reporting only one can mislead.

#### What Gordon measures

Gordon measures **vocabulary change only.** He aligns topics across periods, follows the chains, and interprets how their top words and highest-loading documents shift (e.g. *vessel, sea, shore* → *ship, air, plane, speed*). He does not measure how prominent a theme is in each period. Prominence would therefore be an extension.

#### Proposal: both, as two separate measures from two different models

1. **Vocabulary change, from the period models.**
   - Follow the aligned chains (2.5).
   - For each transition, report the cosine similarity of the linked topics: high means stable vocabulary, lower means change.
   - Report the words that gain and lose the most probability.
   - Read the top 5 highest-loading motions in each period.
2. **Prominence, from the whole-corpus model.**
   - The whole-corpus model has the same 44 topic definitions for all years, so a topic's share can be compared across time.
   - The period models' shares **cannot** be compared across periods directly. Each period's shares sum to 1 over its own 11 topics, so a theme's share in one period depends on what the other 10 topics in that period are.
   - The mapping in 2.3.2 links each chain to the whole-corpus topic(s) whose prevalence describes it.

#### How the document-topic proportions are summarized

For each motion d, the model gives θ_d, its topic mixture: a probability for each topic, summing to 1.

**Main measure: mean topic proportion per period.**

  prevalence(k, p) = (1 / N_p) × Σ θ_dk, summed over the N_p motions d in period p

- This is the average share of topic k across the period's motions.
- Every motion counts equally, whatever its length. I suggest this because a motion is one political act: a 2-page and a 20-page motion each represent one proposal to parliament.
- The alternative is to weight each motion by its number of words, which measures the share of all **text** devoted to the topic. Long motions, such as party motions covering a whole policy area, would then dominate.

**Supplementary measures** (robustness):

- **Dominant-topic share:** the share of the period's motions in which topic k is the largest. This is easier to read ("12% of motions are mainly about preschool") but ignores motions where the topic is second.
- **Threshold share:** the share of motions where θ_dk is at least 0.10 or 0.20. This counts motions that substantially address the topic.

**Uncertainty:**

- **Across seeds:** the 5 seed models give 5 prevalence estimates for each matched topic. Their range shows how much of a change could be model noise.
- **Optionally a bootstrap over motions,** which resamples the period's motions to give an interval for each mean.

**Resolution:**

- The whole-corpus model allows **yearly** prevalence curves as well as the four periods.
- Yearly curves show when a change happened, e.g. around a reform. The periods give the summary.
- The number of motions per year varies from 218 (1998) to 602 (1990), so yearly values are noisier, especially in the late 1990s.

**Which model θ comes from:** the body-text model (no title weighting, 2.1).

**Suggestion:** both measures, clearly separated in the report. Vocabulary change is the core, following Gordon. Prominence is the extension, measured with the whole-corpus model as the mean topic proportion per period, with yearly curves and seed ranges.

---

### 2.5 Statistical evidence for cross-period alignment

**Question:** how do we show that aligned topics are more similar than chance, and which chains do we interpret?

#### Gordon's procedure

1. **Adjacent periods only.** Topics are matched between period 1 and 2, 2 and 3, and 3 and 4, not between distant periods.
2. **One-to-one matching.** The Hungarian algorithm pairs each topic with exactly one topic in the next period so that the total cosine similarity is as high as possible. This is conservative: it cannot represent a topic splitting into two or two merging. Both Gordon and our proposal note this as a limitation.
3. **Permutation null.** For each transition, the topics are paired at random 1,000 times, and the mean cosine of each random pairing is recorded. This gives the distribution of mean similarity under "no real correspondence".
   - The z-score is (matched mean − null mean) / null standard deviation.
   - **Gordon's results:** matched 0.44–0.59 against null 0.22–0.25, z = 7–9.
4. **Chains.** Following the matches across all four periods gives chains. Gordon found 15 chains spanning all four periods. He interprets those with a mean cosine of at least 0.50 over all three transitions that are thematic in every period: 7 met the threshold, 4 of them thematic throughout.

**Proposal:** adopt all four steps, so our results are directly comparable with Gordon's. None of this is implemented yet. The matching code exists, and the null and the chains are small additions.

#### Possible extension: a ceiling from seed stability

The permutation null gives a **floor**: what random pairing achieves. The seed-stability runs give a **ceiling**: how similar the same period's topics are across random seeds, i.e. how much similarity is lost to model noise alone.

- A cross-period cosine close to the within-period seed ceiling means the theme is as stable across time as the model is across runs: no detectable change.
- A cosine well below the ceiling but well above the null indicates real change in a continuing theme.

Placing each transition between floor and ceiling makes the cosine values interpretable, instead of comparing them to an arbitrary 0.50.

---

### 2.6 Manual evaluation rubric

**Question:** how do we make the proposal's "manual assessment of coherence and interpretability" systematic and reportable?

#### Gordon's rubric

Each topic is coded on three separate dimensions, using its top words **and** its top 5 highest-loading documents:

1. **Coherent (yes/no):** the top words form a recognizable semantic field, words that belong together because they refer to related things.
2. **Thematic (yes/no, only for coherent topics):** the semantic field is about **subject matter** (settings, entities, situations, domains) rather than a register, style or paratext. A topic of archaic poetic diction can be coherent without being thematic.
3. **Author concentration (computed):** the share of the topic's top 5 documents that come from its single most frequent author, from 0.2 (five different authors) to 1.0 (one author). It shows whether a topic is a genre-wide pattern or one author's idiom.

Coding is done in one pass, before chain selection, so that the coding is not influenced by which chains look interesting.

#### Examples from our current baseline model

| Topic top words | Coherent | Thematic | Comment |
|---|---|---|---|
| *förskola, barn, förälder, barnomsorg, fritidshem, förskollärare* | yes | yes | Clear policy domain |
| *ansvar, uppgift, verksamhet, mål, förändring, form, enskild, fråga* | yes, as a register | no | Bureaucratic language, not a subject |
| *homosexuell, helårsstudent, folkmord, takbelopp, cancerfond* | no | – | Rare words from unrelated motions |

#### Parliamentary analogue of author concentration: party or MP concentration

- In parliament the risk is that a topic reflects **who** writes rather than **what** is discussed: one party's recurring framing, or one MP's repeated motions on a pet issue (e.g. swimming lessons, a regional university).
- The data contain each motion's signatories and their parties, so the measure is straightforward:
  - **Party concentration:** share of the top 5 motions whose (first) signatory belongs to the topic's most frequent party.
  - **MP concentration:** the same with individual MPs. Repeated motions by one MP are common.
- **Interpretation needs a reference point.** Party shares of all motions (first signatory) are very unequal: S 32%, M 23%, C 11%, FP 10%, KD 6%, SD 5%, MP 4%, V 4%. A party concentration of 0.4 for S may simply reflect its size. Compare with the party's share of all motions in the period.
- **Decision:** use the first signatory or all signatories (multi-party motions exist).

#### Further questions

- Use the top 5 documents, as Gordon does, or more? Our documents are whole motions, fewer and more varied than his chunks.
- A second annotator on a sample of topics? Gordon lists a single annotator as a limitation. The proposal mentions consulting someone familiar with Swedish education policy.

---

### 2.7 Proper names and place names

**Question:** should proper names be removed, as Gordon does?

#### Background

Gordon removes proper names (capitalized words in mid-sentence) because character and place names tie topics to individual books rather than themes.

In our corpus, Stanza tags proper nouns as `PROPN`. They make up **1.3% of all words**. The most frequent:

- **Places:** *Sverige* (21,459), *Stockholm*, *Göteborg*, *Umeå*, *Lund*, *Örebro*, *Uppsala*, *Linköping*, *Borås*, *Jönköping*, *Malmö*, *Karlstad*, *Skövde*, *Luleå*, *Kalmar*, *Södertörn*, *Norrland*.
- **Organizations and acronyms:** *UHÄ*, *SOU*, *EU*, *Europa*.

Both current models have about 8 topics organized around places (e.g. *Skövde, Västsverige, Skaraborg*; *Örebro, Karlstad, Värmland*; *Umeå, Uppsala, Borås*). These come from motions about locating or expanding universities and university colleges in a region.

#### Arguments

- **For removal:** these topics are close to Gordon's author signal. MPs propose universities, programmes and funding for **their own constituency**, so the topic reflects regional representation as much as an education-policy theme. Place-name topics also make cross-period alignment depend on which towns were discussed.
- **Against removal:** regional distribution of higher education is a real and long-running education-policy theme in Sweden. Removing place names keeps the theme (*högskola, utbyggnad, utbildningsplats*) but loses which regions it concerned.

#### Options

1. **Keep all proper names** (current).
2. **Drop all `PROPN`.** This is one line in step 03, but it also removes *Sverige*, *EU*, *SOU*, *UHÄ* and organization names, which may matter (EU membership 1995 is an education-policy event).
3. **Drop only place names** (municipalities, regions, towns), using a list. This keeps organizations and *Sverige/EU*.
4. **Merge place names into one token** (e.g. `ORT`). The model then learns "this is a regional motion" without splitting by town.

**Suggestion:** test option 3 or 4 against the current models, and see whether the regional topics become one coherent "regional higher education" topic.

---

### 2.8 Number of topics

**Question:** keep 44 topics for the whole corpus and about 11 per period?

**Decided 2026-10-17: 8 topics per period, 32 = 4 × 8 for the whole corpus.** The period models were fitted and seed-tested at 8, 11 and 15 topics (5 seeds, global vocabulary; *stable* = found again with cosine ≥ 0.70 in at least 3 of the 4 other seeds):

| Period | 8 topics: mean cosine / stable | 11 topics | 15 topics |
|---|---|---|---|
| 1985/86–1993/94 | 0.70 / 4 of 8 (50%) | 0.63 / 4 of 11 (36%) | 0.55 / 4 of 15 (27%) |
| 1994/95–2005/06 | 0.77 / 7 of 8 (88%) | 0.67 / 6 of 11 (55%) | 0.62 / 6 of 15 (40%) |
| 2006/07–2013/14 | 0.80 / 6 of 8 (75%) | 0.65 / 4 of 11 (36%) | 0.58 / 6 of 15 (40%) |
| 2014/15–2025/26 | 0.72 / 4 of 8 (50%) | 0.67 / 6 of 11 (55%) | 0.62 / 9 of 15 (60%) |
| **All periods** | **21 of 32 (66%)** | **20 of 44 (45%)** | **25 of 60 (42%)** |

- 8 is the only count at which at least half of the topics are stable in every period, and it has the highest mean cosine everywhere.
- The margin is small in periods 1 and 4, which are exactly at half stable at 8 topics. Period 4 is the only period whose stable share rises with the topic count (50%, 55%, 60%).
- The number of robust themes per period is about 4–9 at every count, so more topics mainly add seed-dependent ones (8 → 15 adds 28 topics but only 4 stable ones).
- All period models are more stable than the 44-topic whole-corpus model of the first version (mean cosine 0.525, about 27% stable), which supports Gordon's case for period models.
- The whole-corpus model follows the period count, as in Gordon (60 = 4 × 15), so the two designs have the same total capacity. 32 also coincides with the original topic-concentration choice on the earlier pipeline.
- Caveats: one set of seeds, the 0.70 threshold, and the global vocabulary used at the time. With the per-period vocabularies chosen later (2.2), the 8-topic models are as stable (21 of 32 topics); 11 and 15 were not re-tested.
- **The 32-topic whole-corpus model** is more stable than the 44-topic one: mean cosine 0.568 against 0.525, and 12 of 32 topics stable (38%) against 12 of 44 (27%); 7 topics are found in all four other seeds (compulsory school and grades, research, preschool, universities and students, upper secondary school, special support, society and democracy). It remains less stable than the 8-topic period models (0.70–0.80, 66%), as Gordon's argument for period models expects. Found in no other seed: youth and mental health, bullying, costs and fees, vocational and apprenticeship education, Stockholm institutions, and three residual topics of unrelated words (possibly a few motions each).

The original question and options are kept below for reference.

- 44 was chosen on the earlier pipeline by **topic-concentration testing** (how concentrated documents are on few topics), not by semantic coherence. Several values from 6 to 64 were tested.
- 44 ÷ 4 = 11 per period, matching total capacity as in Gordon's design (2.3.1).
- Gordon uses 15 per bin, and his bins are similar in size to ours (2,000–5,000 chunks against our 2,879–4,029 motions).
- About 10 of the 44 whole-corpus topics are mixed. That may mean 44 is too many for this corpus, or it may be the normal long tail of a heterogeneous corpus where some topics collect rare subjects.
- The proposal time-boxes model evaluation to four weeks and treats unstable or uninterpretable topics as a finding if time runs out.

**Options:**

- Keep 44/11.
- Test a small range per period (e.g. 8, 11, 15) with the seed-stability and rubric results.
- Use Gordon's 15 per period (and 60 for the whole corpus).

**Question:** how many values can be tested within the time box?

---

### 2.9 Temporal bins

**Question:** four bins of roughly equal size, or political periods?

**Decided: four periods of complete electoral terms, as equal in size as the terms allow, with motions assigned by parliamentary session.**

| Period | Sessions | Electoral terms beginning | UbU motions |
|---|---|---|---|
| 1 | 1985/86–1993/94 | 1985, 1988, 1991 | 4,029 |
| 2 | 1994/95–2005/06 | 1994, 1998, 2002 | 3,477 |
| 3 | 2006/07–2013/14 | 2006, 2010 | 2,879 |
| 4 | 2014/15–2025/26 | 2014, 2018, 2022 | 3,572 |

- **Electoral terms:** every period covers whole terms of the Riksdag, so no term, and no government formed after an election, is split between two periods. The boundaries fall at the elections of 1994, 2006 and 2014, which are also changes of government.
- **Equal size within that constraint:** of the possible groupings of the 11 terms into four consecutive periods, this one has the most even sizes (largest / smallest = 1.40). Equal sizes keep the period models comparable in quality: a much smaller bin gives noisier topics, and Gordon's weakest alignment was from his smallest bin. The smallest period here (period 3) is not less stable than the others (2.8).
- **Assigned by session (riksmöte), not by date:** the session is the unit of parliamentary work, and some motions carry a placeholder date (motions of 1985/86 dated 1985-01-01).
- **Coverage:** UbU motions start in January 1986 (motions of autumn 1985 are not tagged with the committee), so period 1 effectively starts then. Period 4 runs to the end of session 2025/26, the last session before the 2026 election.
- **Uneven sessions:** session 1995/96 has only 44 UbU motions (735 motions in all that session), probably because of the change to the new budget process; the other sessions have 187–594.
- **Compared with the earlier bins:** the models were first fitted on four calendar-year bins of roughly equal size (1986–1993, 1994–2004, 2005–2014, 2015–2025, assigned by date). With the electoral-term periods, at the chosen 8 topics:
  - more period topics are stable: 21 of 32 (66%) against 19 of 32 (59%), with mean cosine 0.70–0.80 per period against 0.71–0.76;
  - the alignment is stronger: matched mean cosine 0.65, 0.69 and 0.67 for the three transitions against 0.53, 0.62 and 0.68, and all 8 chains pass Gordon's criterion against 5 (every link ≥ 0.50: 4 against 3);
  - 8 remains the only tested count with at least half of the topics stable in every period. At 11 and 15 topics there is no gain (20 of 44 against 21; 25 of 60 against 24).
  - The differences are small (one to three stable topics per period, one set of seeds), so they show that the electoral-term periods are at least as stable as the earlier bins, not that they are clearly better. The stronger alignment may partly come from the boundaries falling at elections, which can make adjacent periods more alike without making the topics within a period more stable.

Gordon chose literary-historical periods (the Verne era, scientific romance, Edwardian SF, the early pulp era) and accepted unequal sizes. Electoral terms are the political counterpart, without giving up comparable sizes.

**What the periods do not follow:**

- **Major school reforms** fall inside periods: municipalization of schools (1991) and the independent-school reform (1992) in period 1, the preschool curriculum (1998) in period 2, Lgr11 (2011) in period 3.
- **Government and opposition are not held fixed.** Periods 2 and 3 each have one government side throughout (Social Democratic governments 1994–2006, the Alliance 2006–2014), so the opposition, which writes most motions, is largely the same parties within each of them; periods 1 and 4 include changes of government (1991, 2022). A change between periods can therefore reflect who was in opposition as well as a change in the debate. This is a confound for the interpretation of the chains, to be examined with the party analysis below.

**Planned later:** a party analysis with the session and author metadata: which parties' motions carry each topic, per period, compared with each party's share of all motions in the period (2.6).

---

### 2.10 Departures from the proposal and from Gordon

These should be stated explicitly in the methods section.

| Choice | Proposal / Gordon | Current | Status |
|---|---|---|---|
| Lemmatization | Proposal: initially follow Bruinsma & Johansson (no stemming, lemmatization not discussed). Gordon: none | Stanza lemmatization, with a small table correcting known Stanza errors | Decided. Justification: Swedish inflection splits one word into many forms (*skola, skolan, skolor, skolornas*), which fragments topics. Gordon's English corpus does not have this problem to the same degree |
| LDA implementation | Gordon: MALLET (Gibbs sampling), 1,000 iterations, asymmetric hyperparameter optimization | scikit-learn, online variational inference, 50 passes, symmetric priors; no convergence check (always 50 passes) | **Open, for the supervisor (0.4):** current plan is to keep scikit-learn and present the study as an adaptation of Gordon's workflow, not a computational replication |
| Vocabulary | Gordon: per period (≥ 10 documents, ≤ 50%), adjacent periods compared over shared words | The same for the period models; the whole-corpus model has its own (≥ 5 motions, ≤ 50%, 10,000 words) | Decided (0.1, 2.2): follows Gordon |
| Document unit | Gordon: 1,000-word chunks of books | Whole motions | Decided: motions are natural units of meaning, and most are shorter than 1,000 words |
| Proper names | Gordon: removed | Kept | Open (2.7) |
| Duplicates | Proposal: investigate and monitor | Counted for the report, not removed (515, 3.69%; mostly the same motion resubmitted in a later session) | **Open:** keep or drop. Duplicates are typically identical motions submitted in several years, or by several MPs |
| Title weighting | Not in Gordon | Not used (3× and 5× tested) | Decided (2.1): stability gain too small |
| Topic count | Gordon: 15 per period, 60 for the whole corpus. Earlier plan: 44 / 11 | 8 per period, 32 for the whole corpus | Decided (2.8): highest tested count at which at least half of the topics are stable in every period; same total-capacity logic as Gordon |
| Seed stability | Gordon: whole-corpus runs only | Hungarian-matched stability for every model, period models included | Extension |
| Prominence | Not in Gordon | Mean topic proportion per period from the whole-corpus model | Proposed extension (2.4) |

---

**How the results compare with Gordon so far** (details in `PIPELINE_DOCUMENTATION.md`, *Comparison with Gordon*):

- Whole-corpus seed instability is of the same size as his (mean Jaccard 0.270 against his 0.26–0.31).
- At his 15 topics per period, with his vocabulary design, our adjacent-period alignment is close to his (matched mean cosine 0.43, 0.60, 0.62 against 0.44–0.59; 9 of 15 chains pass his criterion against his 7). At our 8 topics: 0.67–0.78, and all 8 chains pass.
- His chain criterion is the mean of the three links ≥ 0.50, and it is the main criterion in the period explorer. Requiring every link ≥ 0.50 is stricter: 4 of the 8 chains. Single weak links are marked in the explorer.
- Not yet comparable: permutation null and z-scores (2.5), rubric coding (2.6), a whole-corpus model with 8 topics (his k = 15 control). Convergence of our 50-pass fits is not checked.

### 2.11 Smaller open points

- **Billions:** *miljard/miljarder* (about 1,300 occurrences) is the same kind of amount word as *miljoner*, which is removed. Remove it too, or keep it as a signal of budget motions?
- **Leftover fragments:** some remain from line-end hyphenation in older scanned motions (*utbild- Mot. 1988/89 ningsmoment* gives `utbild` and `ning`, in 75–180 motions), and from Swedish compound ellipsis (*skol- och språkexpertis* gives `skol`). Accepted for now; none reach the top words of any topic.
- **Party abbreviations:** a few remain in 59–109 motions (`fp`, `kd`, `mp`, probably from forms like *kd-ledamöter*).
- **Truncated lemmas in compounds:** Stanza truncates *kompetens* to `kompet` also inside compounds (*gymnasiekompetens* → `gymnasiekompet`, *IT-kompetens* → `it-kompet`), where the whole-word correction table does not apply. Fixed for `kompet` and `bibliotekarium` by corrections that also apply to the end of a lemma, enabled per entry after checking its compounds (a general suffix rule would have turned *sammanslagen* into `sammanslag`); see `MODEL_REVIEW.md`, *After the Fixes*.

---

## 3. Questions for the Seminar (Summary)

1. **Title weighting:** dropped after the stability runs (small gain). Is that acceptable, or report the weighted model as a robustness check? (2.1)
2. **Shared vocabulary:** decided, Gordon's per-period vocabularies compared over shared words. Is the share of weight outside the shared words enough to report vocabulary change? (0.1, 2.2)
3. **Baseline comparison:** is Gordon's quality comparison (same rubric for whole-corpus and period models) enough, or should the topic mapping be added? (2.3)
4. **Thematic change:** vocabulary only (as Gordon), or vocabulary and prominence? Is the mean topic proportion per period the right summary? (2.4)
5. **Evidence:** adopt Gordon's permutation null, z-scores and chain criterion? Add the seed-stability ceiling? (2.5)
6. **Rubric:** adopt Gordon's three dimensions with party/MP concentration instead of author concentration? A second annotator? (2.6)
7. **Place names:** keep, remove, or merge? (2.7)
8. **Topic numbers and periods:** 8 per period and 32 for the whole corpus, chosen by seed stability (decided, 2.8); periods of complete electoral terms, assigned by session (decided, 2.9). Is the confound of a largely fixed opposition in periods 2 and 3 acceptable, given the planned party analysis? (2.9)
9. **LDA implementation:** keep scikit-learn and present the study as an adaptation of Gordon's workflow, or switch to MALLET? Is a convergence check needed? (0.4, 2.10)
10. **Duplicates:** keep or drop? (2.10)

---

## 4. Next Steps

1. ✅ Seed-stability tests run (baseline, 3×, 5×); title weighting dropped (2.1). About 12 of 44 topics are found again in 3–4 of the other 4 seeds and about 19 in none; the per-topic table lets unstable topics be flagged before interpretation, and the many seed-dependent topics are an argument for reconsidering the topic count (2.8).
2. ✅ Period models fitted and seed-tested at 8, 11 and 15 topics (global vocabulary); topic count set to 8 per period and 32 for the whole corpus (2.8). Only the 8-topic models are kept; the period explorer shows 8 topics only. ✅ Whole-corpus model re-fitted and seed-tested at 32 (mean cosine 0.568, 12 of 32 topics stable).
3. ✅ Periods set to complete electoral terms, motions assigned by session (2.9).
4. Settle the alignment design (2.2, 2.5) and the definition of thematic change (2.4).
5. ✅ Period models re-fitted with per-period vocabularies, compared over shared words (2.2). Next: the permutation null for the alignment (2.5).
6. If agreed: the topic mapping (2.3.2) and the prevalence analysis (2.4).
7. Party analysis per topic and period (2.9).
8. Manual evaluation with the rubric (2.6), within the proposal's four-week time box.
9. Report writing (Nov.–Dec.).
