# Seed-Stability Analysis: Period 1985/86–1993/94, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1985/86–1993/94 (3613)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1618.09 | 50 |
| 123 | 1630.41 | 50 |
| 456 | 1620.34 | 50 |
| 789 | 1609.97 | 50 |
| 999 | 1607.23 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 1 |
| 2 of 4 | 1 |
| 1 of 4 | 3 |
| 0 of 4 | 3 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | forskning, högskola, universitet, förslag, resurs, verksamhet, liten, medel | 4/4 | 0.884 | 0.789 | 0.570 |
| 2 | förslag, anslag, kommun, bidrag, budgetår, kommunal, medel, verksamhet | 3/4 | 0.767 | 0.482 | 0.575 |
| 3 | hälsa, kunskap, vård, medicinsk, landsting, kvinna, hemkunskap, problem | 1/4 | 0.666 | 0.550 | 0.295 |
| 4 | högskola, län, region, universitet, plats, hög, teknisk, högskoleutbildning | 4/4 | 0.944 | 0.907 | 0.621 |
| 5 | utveckling, land, kunskap, område, hög, samhälle, utveckla, svensk | 2/4 | 0.649 | 0.485 | 0.315 |
| 6 | barn, elev, handikapp, särskola, hemspråksundervisning, förälder, handikappad, döv | 1/4 | 0.418 | 0.015 | 0.139 |
| 7 | språk, lund, land, malmö, internationell, svensk, stiftelse, bild | 0/4 | 0.364 | 0.285 | 0.175 |
| 8 | ämne, lärare, poäng, linje, lärarutbildning, teknisk, idrott, årskurs | 0/4 | 0.507 | 0.376 | 0.181 |
| 9 | gymnasieskola, elev, hög, krav, kurs, förslag, linje, studie | 0/4 | 0.384 | 0.179 | 0.119 |
| 10 | folkhögskola, invandrare, studieförbund, vuxenutbildning, svensk, undervisning, folkbildning, svenska | 1/4 | 0.641 | 0.518 | 0.334 |
| 11 | skola, elev, lärare, undervisning, grundskola, barn, ämne, kunskap | 4/4 | 0.954 | 0.906 | 0.553 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5999
- Median: 0.7308
- Min: 0.0151
- Max: 0.9829
- Std Dev: 0.2998

**Jaccard Similarity (top 20 words):**
- Mean: 0.3254
- Median: 0.3333
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1988

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6634
- Median: 0.6736
- Min: 0.3199
- Max: 0.9892
- Std Dev: 0.2231

**Jaccard Similarity (top 20 words):**
- Mean: 0.3796
- Median: 0.3793
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2290

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6625
- Median: 0.6544
- Min: 0.2854
- Max: 0.9752
- Std Dev: 0.2007

**Jaccard Similarity (top 20 words):**
- Mean: 0.3470
- Median: 0.3333
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.1784

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6847
- Median: 0.6642
- Min: 0.3244
- Max: 0.9914
- Std Dev: 0.2222

**Jaccard Similarity (top 20 words):**
- Mean: 0.3578
- Median: 0.2903
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2495

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6680
- Median: 0.7529
- Min: 0.0469
- Max: 0.9819
- Std Dev: 0.2684

**Jaccard Similarity (top 20 words):**
- Mean: 0.3614
- Median: 0.3793
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1907

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5974
- Median: 0.6523
- Min: 0.0628
- Max: 0.9542
- Std Dev: 0.2905

**Jaccard Similarity (top 20 words):**
- Mean: 0.3042
- Median: 0.3333
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1927

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6311
- Median: 0.7269
- Min: 0.0643
- Max: 0.9853
- Std Dev: 0.2918

**Jaccard Similarity (top 20 words):**
- Mean: 0.3240
- Median: 0.3333
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2167

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6555
- Median: 0.6913
- Min: 0.2244
- Max: 0.8881
- Std Dev: 0.2223

**Jaccard Similarity (top 20 words):**
- Mean: 0.2716
- Median: 0.2500
- Min: 0.0811
- Max: 0.5385
- Std Dev: 0.1542

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6572
- Median: 0.8012
- Min: 0.0128
- Max: 0.9092
- Std Dev: 0.2835

**Jaccard Similarity (top 20 words):**
- Mean: 0.3531
- Median: 0.4286
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2123

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6693
- Median: 0.6068
- Min: 0.3602
- Max: 0.9544
- Std Dev: 0.2236

**Jaccard Similarity (top 20 words):**
- Mean: 0.3411
- Median: 0.2903
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.2092

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6489
- Median: 0.7079
- Min: 0.0128
- Max: 0.9914
- Std Dev: 0.2566

### Jaccard Similarity (across all matches)
- Mean: 0.3365
- Median: 0.3333
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2069
