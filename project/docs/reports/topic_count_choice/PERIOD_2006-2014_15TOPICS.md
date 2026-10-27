# Seed-Stability Analysis: Period 2006/07–2013/14, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2006/07–2013/14 (2026)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1149.61 | 50 |
| 123 | 1106.47 | 50 |
| 456 | 1158.61 | 50 |
| 789 | 1109.83 | 50 |
| 999 | 1111.36 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 1 |
| 2 of 4 | 2 |
| 1 of 4 | 1 |
| 0 of 4 | 6 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | student, högskola, hög, studie, studera, studiemedel, fribelopp, lärosäte | 4/4 | 0.909 | 0.896 | 0.447 |
| 2 | svensk, land, skolbibliotek, demokratisk, rättighet, demokrati, sexuell, nordisk | 0/4 | 0.456 | 0.383 | 0.197 |
| 3 | anslag, studie, förslag, satsning, bidrag, heltid, prisbasbelopp, höja | 1/4 | 0.509 | 0.198 | 0.231 |
| 4 | sund, maskin, anamma, godis, sända, arbetare, läsk, sälja | 0/4 | 0.031 | 0.018 | 0.000 |
| 5 | gymnasieskola, arbetsmarknad, kunskap, människa, behov, ung, ungdom, hög | 4/4 | 0.907 | 0.847 | 0.658 |
| 6 | forskning, högskola, universitet, utveckling, svensk, lärosäte, hög, företag | 4/4 | 0.938 | 0.846 | 0.823 |
| 7 | legitimation, lärarlegitimation, musik, kultur, utbilda, lärarutbildning, kulturskola, läkare | 0/4 | 0.142 | 0.069 | 0.067 |
| 8 | lag, ändring, avslå, förslag, fortsätta, avisera, studiesocial, vuxenstuderande | 0/4 | 0.113 | 0.001 | 0.056 |
| 9 | kommun, kommunal, fristående, friskola, elev, förälder, barnomsorg, verksamhet | 3/4 | 0.746 | 0.421 | 0.313 |
| 10 | läkare, vård, gammal, läkarutbildning, sjukvård, hälsa, patient, örebro | 2/4 | 0.683 | 0.133 | 0.517 |
| 11 | yrkeshögskola, land, person, myndighet, validering, teckenspråk, svensk, skolmat | 0/4 | 0.316 | 0.149 | 0.139 |
| 12 | elev, lärare, nationell, förslag, skolverk, undervisning, betyg, mål | 4/4 | 0.926 | 0.899 | 0.429 |
| 13 | ungdom, mat, ung, kunskap, privatekonomi, hälsa, lån, ekonomi | 0/4 | 0.521 | 0.439 | 0.183 |
| 14 | barn, förskola, förälder, personal, behov, fritidshem, fysisk, kommun | 4/4 | 0.901 | 0.854 | 0.338 |
| 15 | elev, kunskap, undervisning, lärare, språk, ämne, svensk, grundskola | 2/4 | 0.677 | 0.600 | 0.335 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6251
- Median: 0.5996
- Min: 0.0470
- Max: 0.9856
- Std Dev: 0.3263

**Jaccard Similarity (top 20 words):**
- Mean: 0.3455
- Median: 0.2500
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2634

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5287
- Median: 0.4441
- Min: 0.0012
- Max: 0.9943
- Std Dev: 0.3370

**Jaccard Similarity (top 20 words):**
- Mean: 0.3050
- Median: 0.1765
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2915

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5836
- Median: 0.6244
- Min: 0.0140
- Max: 0.9571
- Std Dev: 0.3439

**Jaccard Similarity (top 20 words):**
- Mean: 0.3316
- Median: 0.3333
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2766

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6032
- Median: 0.7578
- Min: 0.0314
- Max: 0.9325
- Std Dev: 0.3261

**Jaccard Similarity (top 20 words):**
- Mean: 0.2800
- Median: 0.2903
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1869

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6186
- Median: 0.6283
- Min: 0.0033
- Max: 0.9829
- Std Dev: 0.2793

**Jaccard Similarity (top 20 words):**
- Mean: 0.3049
- Median: 0.2903
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2309

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6875
- Median: 0.8043
- Min: 0.0264
- Max: 0.9820
- Std Dev: 0.3136

**Jaccard Similarity (top 20 words):**
- Mean: 0.4229
- Median: 0.4286
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.3019

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6835
- Median: 0.7317
- Min: 0.0802
- Max: 0.9856
- Std Dev: 0.2567

**Jaccard Similarity (top 20 words):**
- Mean: 0.3611
- Median: 0.3333
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2095

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6309
- Median: 0.7123
- Min: 0.0685
- Max: 0.9891
- Std Dev: 0.2943

**Jaccard Similarity (top 20 words):**
- Mean: 0.3157
- Median: 0.2121
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2695

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5959
- Median: 0.6559
- Min: 0.1289
- Max: 0.9812
- Std Dev: 0.2798

**Jaccard Similarity (top 20 words):**
- Mean: 0.2660
- Median: 0.2121
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2001

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6871
- Median: 0.8441
- Min: 0.0047
- Max: 0.9863
- Std Dev: 0.3233

**Jaccard Similarity (top 20 words):**
- Mean: 0.3899
- Median: 0.4286
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2193

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6244
- Median: 0.7131
- Min: 0.0012
- Max: 0.9943
- Std Dev: 0.3130

### Jaccard Similarity (across all matches)
- Mean: 0.3323
- Median: 0.2903
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2522
