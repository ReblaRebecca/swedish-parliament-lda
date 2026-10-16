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

1. Status
2. Decisions to make
   - 2.1 Title weighting
   - 2.2 Shared vocabulary for cross-period alignment
   - 2.3 Comparing the whole-corpus model with the period models
   - 2.4 What "thematic change" means: vocabulary, prominence, or both
   - 2.5 Statistical evidence for cross-period alignment
   - 2.6 Manual evaluation rubric
   - 2.7 Proper names and place names
   - 2.8 Number of topics
   - 2.9 Temporal bins
   - 2.10 Departures from the proposal and from Gordon
   - 2.11 Smaller open points
3. Questions for the seminar (summary)
4. Next steps

---

## 1. Status

### 1.1 Corpus

13,917 motions referred to the Committee on Education (UbU), 1986–2025, from Riksdagens öppna data, in four bins of roughly equal size:

| Period | Motions |
|---|---|
| 1986–1993 | 3,770 |
| 1994–2004 | 3,313 |
| 2005–2014 | 3,577 |
| 2015–2025 | 3,257 |

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
  - a **title-weighted** model, with title words appended 5 times.
- Both use the same 13,913 motions (4 withdrawn motions titled *Utgår* have no text) and the same 10,000-word vocabulary.
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

- Seed-stability runs (code ready).
- The period (binned) models.
- Cross-period alignment and topic chains.
- Manual evaluation.

---

## 2. Decisions to Make

### 2.1 Title weighting

**Question:** should title words be given extra weight, and if so how much?

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

So the weighting is **moderate for a typical motion but strong for short motions**, and almost irrelevant for very long ones. The effect is not uniform. It depends on body length, which also differs between periods (median body length 182, 200, 146 and 159 words in the four periods), though without a simple trend.

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
- Each period's model is built on its own most relevant words. A word typical of 2015–2025 (*digitalisering*, *nyanländ*) is not crowded out by thresholds computed over 40 years.
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

- Our whole-corpus 44 topics ≈ 4 bins × 11 topics. That is the same logic as Gordon's k = 60 = 4 × 15: equal total capacity.
- To mirror him fully we would also fit a whole-corpus model at k = 11, matching one bin.
- We code all topics with the same rubric and report a table like his: whole-corpus k = 44, whole-corpus k = 11, and the four period models.
- **Our addition:** seed stability for every configuration. Gordon reports it only for the initial whole-corpus runs and lists it as a limitation.

**What it answers:**

- Does binning cost topic quality? (If the period topics are much less coherent, the bins may be too small.)
- Is the whole-corpus model a reasonable reference?

**What it does not answer:** whether the models found the **same themes**. Two models can be equally good and still find different things. That is what the extension addresses.

#### 2.3.2 Extension: map each period topic to the whole-corpus topics

**Idea:** the whole-corpus model has one fixed set of 44 topics for 1986–2025. Each period model has its own 11. Mapping every period topic to its most similar whole-corpus topics relates the two descriptions of the same corpus.

**How it would be done:**

1. **Common vocabulary.** The period topics and the whole-corpus topics must be compared over the same words in the same order, as in 2.2. With option A they share the global vocabulary directly. With option B we use the intersection of each period's vocabulary with the whole-corpus vocabulary.
2. **Similarity matrix.** For each period, compute the cosine similarity between each of its 11 topics and each of the 44 whole-corpus topics, giving an 11 × 44 matrix.
3. **Record the matches.** For each period topic, record its best-matching whole-corpus topic and the cosine, plus the second- and third-best.
4. **Threshold.** A match counts only if the cosine is at least a threshold, e.g. 0.50 (the value Gordon uses for chains), or a value calibrated against a permutation null as in 2.5.

This is **not** one-to-one matching: several period topics may map to the same whole-corpus topic. That is intended, because the granularities differ (11 against 44).

**What it shows:**

1. **Presence over time.** A table of whole-corpus topics × periods, marking where a matching period topic exists. It shows which themes are present in every period and which only in some.
2. **Period-specific themes.** A period topic with no whole-corpus match above the threshold is a theme the whole-corpus model did not capture as its own topic, because it was too short-lived or absorbed into broader topics. Each such case is direct evidence for binning, in addition to Gordon's argument.
3. **Granularity.** A broad period topic often spreads over two or three narrower whole-corpus topics. The second- and third-best matches show this, e.g. a 1986–1993 topic covering both *barnomsorg* and *förskola* might match the preschool topic and the family-policy topic.
4. **A check on the chains.** If a chain (2.5) is a real recurring theme, its topics in the four periods should map to the same or closely related whole-corpus topics. A chain whose links map to unrelated whole-corpus topics suggests the alignment joined different themes, and should be read with caution.
5. **A bridge to prominence (2.4).** Prominence is measured with the whole-corpus topics. The mapping connects a chain (from the period models) to the whole-corpus topic whose prevalence curve shows how large the theme was in each period. Vocabulary change and prominence can then be reported for the same theme.

**Example from the current model:** the whole-corpus model has a clear preschool topic (*barn, förskola, förälder, barnomsorg, verksamhet, kommun, pedagogisk, personal, fritidshem, förskollärare*).

- We would expect each period to have a matching childcare/preschool topic.
- The cosine against the whole-corpus topic, and the words that differ, would show how the vocabulary moved. For example, from *barnomsorg* and *daghem* towards *förskola*, *läroplan* and *förskollärare* after preschool got its own curriculum in 1998.
- (This is an expectation to test, not a result.)

**Caveats:**

- Because the granularities differ, cosine values between an 11-topic and a 44-topic model are generally lower than between two models of the same size. The threshold should be set with that in mind, ideally from a null distribution.
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

**Which model θ comes from:** title weighting (2.1) changes θ, especially for short motions. The prominence analysis should use the model chosen in 2.1, and state it.

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

- 44 was chosen on the earlier pipeline by **topic-concentration testing** (how concentrated documents are on few topics), not by semantic coherence. Several values from 6 to 64 were tested.
- 44 ÷ 4 = 11 per period, matching total capacity as in Gordon's design (2.3.1).
- Gordon uses 15 per bin, and his bins are similar in size to ours (2,000–5,000 chunks against our 3,250–3,770 motions).
- About 10 of the 44 whole-corpus topics are mixed. That may mean 44 is too many for this corpus, or it may be the normal long tail of a heterogeneous corpus where some topics collect rare subjects.
- The proposal time-boxes model evaluation to four weeks and treats unstable or uninterpretable topics as a finding if time runs out.

**Options:**

- Keep 44/11.
- Test a small range per period (e.g. 8, 11, 15) with the seed-stability and rubric results.
- Use Gordon's 15 per period (and 60 for the whole corpus).

**Question:** how many values can be tested within the time box?

---

### 2.9 Temporal bins

**Question:** keep four bins of roughly equal size, or use political periods?

**Current bins:** 1986–1993, 1994–2004, 2005–2014, 2015–2025, chosen for roughly equal numbers of motions (3,257–3,770), as in the proposal.

Gordon chose literary-historical periods (the Verne era, scientific romance, Edwardian SF, the early pulp era) and accepted unequal sizes.

**A political alternative** would follow:

- **changes of government:** 1991, 1994, 2006, 2014, 2022;
- **major school reforms:** municipalization of schools (1991), the independent-school reform (1992), the preschool curriculum (1998), Lgr11 (2011).

The current boundaries already roughly follow 1994, 2006 and 2014. The 1986–1993 bin spans the 1991–1992 reforms.

**Trade-off:**

- Political periods make results easier to interpret historically.
- Equal sizes make the period models comparable in quality: a much smaller bin gives noisier topics. Gordon's weakest alignment was from his smallest bin.

**Options:**

- Keep the current bins.
- Shift one boundary, e.g. 1986–1991 / 1992–…, at the cost of unequal sizes.
- Report the current bins and test one alternative as a sensitivity check. Gordon lists untested binning schemes as a limitation.

---

### 2.10 Departures from the proposal and from Gordon

These should be stated explicitly in the methods section.

| Choice | Proposal / Gordon | Current | Status |
|---|---|---|---|
| Lemmatization | Proposal: initially follow Bruinsma & Johansson (no stemming, lemmatization not discussed). Gordon: none | Stanza lemmatization, with a small table correcting known Stanza errors | Decided. Justification: Swedish inflection splits one word into many forms (*skola, skolan, skolor, skolornas*), which fragments topics. Gordon's English corpus does not have this problem to the same degree |
| LDA implementation | Gordon: MALLET (Gibbs sampling), 1,000 iterations, asymmetric hyperparameter optimization | scikit-learn, online variational inference, 50 passes, symmetric priors; no convergence check (always 50 passes) | **Open:** keep (simpler; stability is tested directly) or switch (closer replication; requires Java and MALLET) |
| Document unit | Gordon: 1,000-word chunks of books | Whole motions | Decided: motions are natural units of meaning, and most are shorter than 1,000 words |
| Proper names | Gordon: removed | Kept | Open (2.7) |
| Duplicates | Proposal: investigate and monitor | Counted for the report, not removed (133 on the earlier pipeline; to recount) | **Open:** keep or drop. Duplicates are typically identical motions submitted in several years, or by several MPs |
| Title weighting | Not in Gordon | 5× (3× tested) | Open (2.1) |
| Seed stability | Gordon: whole-corpus runs only | Hungarian-matched stability for every model, period models included | Extension |
| Prominence | Not in Gordon | Mean topic proportion per period from the whole-corpus model | Proposed extension (2.4) |

---

### 2.11 Smaller open points

- **Billions:** *miljard/miljarder* (about 1,300 occurrences) is the same kind of amount word as *miljoner*, which is removed. Remove it too, or keep it as a signal of budget motions?
- **Leftover fragments:** some remain from line-end hyphenation in older scanned motions (*utbild- Mot. 1988/89 ningsmoment* gives `utbild` and `ning`, in 75–180 motions), and from Swedish compound ellipsis (*skol- och språkexpertis* gives `skol`). Accepted for now; none reach the top words of any topic.
- **Party abbreviations:** a few remain in 59–109 motions (`fp`, `kd`, `mp`, probably from forms like *kd-ledamöter*).

---

## 3. Questions for the Seminar (Summary)

1. **Title weighting:** is weighting defensible as a departure from Gordon? Weighted as primary, as a robustness check, or not at all? (2.1)
2. **Shared vocabulary:** one global vocabulary, or Gordon's per-period vocabularies compared over shared words? (2.2)
3. **Baseline comparison:** is Gordon's quality comparison (same rubric for whole-corpus and period models) enough, or should the topic mapping be added? (2.3)
4. **Thematic change:** vocabulary only (as Gordon), or vocabulary and prominence? Is the mean topic proportion per period the right summary? (2.4)
5. **Evidence:** adopt Gordon's permutation null, z-scores and chain criterion? Add the seed-stability ceiling? (2.5)
6. **Rubric:** adopt Gordon's three dimensions with party/MP concentration instead of author concentration? A second annotator? (2.6)
7. **Place names:** keep, remove, or merge? (2.7)
8. **Topic numbers and bins:** keep 44/11 and the equal-size bins? (2.8, 2.9)
9. **LDA implementation:** keep scikit-learn or switch to MALLET? (2.10)
10. **Duplicates:** keep or drop? (2.10)

---

## 4. Next Steps

1. Run the seed-stability tests (baseline, 3×, 5×) and decide on title weighting (2.1).
2. Settle the alignment design (2.2, 2.5) and the definition of thematic change (2.4).
3. Implement the period models with the agreed vocabulary design, the alignment with permutation null, and the chains.
4. If agreed: the topic mapping (2.3.2) and the prevalence analysis (2.4).
5. Manual evaluation with the rubric (2.6), within the proposal's four-week time box.
6. Report writing (Nov.–Dec.).
