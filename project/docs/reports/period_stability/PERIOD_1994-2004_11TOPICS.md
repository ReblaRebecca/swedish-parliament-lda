# Seed-Stability Analysis: Period 1994-2004, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of 1994-2004 (3313)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1680.09 | 50 |
| 123 | 1675.54 | 50 |
| 456 | 1651.62 | 50 |
| 789 | 1666.42 | 50 |
| 999 | 1664.11 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 3 |
| 2 of 4 | 0 |
| 1 of 4 | 0 |
| 0 of 4 | 4 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | elev, lärare, gymnasieskola, kunskap, program, behov, många, lärarutbildning | 4/4 | 0.828 | 0.721 | 0.438 |
| 2 | elev, förskola, grundskola, barn, kommun, undervisning, betyg, nationell | 4/4 | 0.861 | 0.814 | 0.437 |
| 3 | folkhögskola, folkbildning, rekryteringsbidrag, musik, statsbidrag, tfhs, dramapedagog, betyg | 0/4 | 0.143 | 0.013 | 0.034 |
| 4 | körkort, teologisk, cancerfond, körkortsutbildning, kostnad, civilingenjörsutbildning, västerås, poäng | 0/4 | 0.233 | 0.167 | 0.060 |
| 5 | forskning, universitet, utveckling, verksamhet, forskarutbildning, forskare, område, svensk | 3/4 | 0.723 | 0.442 | 0.375 |
| 6 | svensk, land, hälsa, läkare, kunskap, medicinsk, vård, öka | 0/4 | 0.483 | 0.241 | 0.184 |
| 7 | fysisk, idrott, ungdom, hälsa, aktivitet, csn, ämne, studiemedel | 0/4 | 0.479 | 0.119 | 0.143 |
| 8 | barn, elev, kommun, mobbning, förälder, fristående, behov, kommunal | 4/4 | 0.887 | 0.799 | 0.463 |
| 9 | högskola, student, hög, universitet, kvalitet, forskning, system, anslag | 4/4 | 0.884 | 0.842 | 0.445 |
| 10 | högskola, universitet, hög, region, utveckling, land, forskning, plats | 3/4 | 0.824 | 0.506 | 0.504 |
| 11 | kvinna, samhälle, jämställdhet, flicka, sexuell, undervisning, kunskap, människa | 3/4 | 0.693 | 0.441 | 0.343 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6652
- Median: 0.7787
- Min: 0.1194
- Max: 0.9392
- Std Dev: 0.2600

**Jaccard Similarity (top 20 words):**
- Mean: 0.3318
- Median: 0.3333
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1952

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7152
- Median: 0.8541
- Min: 0.0563
- Max: 0.9864
- Std Dev: 0.2929

**Jaccard Similarity (top 20 words):**
- Mean: 0.3907
- Median: 0.4815
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2207

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5983
- Median: 0.7093
- Min: 0.0126
- Max: 0.9267
- Std Dev: 0.3066

**Jaccard Similarity (top 20 words):**
- Mean: 0.2809
- Median: 0.3793
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1949

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5802
- Median: 0.5062
- Min: 0.1389
- Max: 0.9349
- Std Dev: 0.2635

**Jaccard Similarity (top 20 words):**
- Mean: 0.2428
- Median: 0.2500
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1876

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6917
- Median: 0.7360
- Min: 0.0333
- Max: 0.9859
- Std Dev: 0.2874

**Jaccard Similarity (top 20 words):**
- Mean: 0.3706
- Median: 0.4286
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2108

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5925
- Median: 0.7306
- Min: 0.0158
- Max: 0.9671
- Std Dev: 0.3194

**Jaccard Similarity (top 20 words):**
- Mean: 0.3022
- Median: 0.3793
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2209

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6347
- Median: 0.6770
- Min: 0.2096
- Max: 0.9849
- Std Dev: 0.2465

**Jaccard Similarity (top 20 words):**
- Mean: 0.3328
- Median: 0.2903
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2249

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6911
- Median: 0.8156
- Min: 0.0721
- Max: 0.9863
- Std Dev: 0.2839

**Jaccard Similarity (top 20 words):**
- Mean: 0.4011
- Median: 0.3793
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2369

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6386
- Median: 0.6090
- Min: 0.2262
- Max: 0.9944
- Std Dev: 0.2528

**Jaccard Similarity (top 20 words):**
- Mean: 0.3334
- Median: 0.2903
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2801

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6405
- Median: 0.6586
- Min: 0.1230
- Max: 0.8996
- Std Dev: 0.2269

**Jaccard Similarity (top 20 words):**
- Mean: 0.3141
- Median: 0.2903
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1762

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6448
- Median: 0.7255
- Min: 0.0126
- Max: 0.9944
- Std Dev: 0.2788

### Jaccard Similarity (across all matches)
- Mean: 0.3300
- Median: 0.3333
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2216
