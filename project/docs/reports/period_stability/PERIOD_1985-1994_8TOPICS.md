# Seed-Stability Analysis: Period 1985/86–1993/94, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1985/86–1993/94 (4025)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1801.61 | 50 |
| 123 | 1803.57 | 50 |
| 456 | 1809.23 | 50 |
| 789 | 1816.13 | 50 |
| 999 | 1815.88 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 2 |
| 3 of 4 | 2 |
| 2 of 4 | 2 |
| 1 of 4 | 1 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | göteborg, barn, barnomsorg, förskola, förskollärare, kommun, läkare, finsk | 0/4 | 0.322 | 0.262 | 0.112 |
| 2 | högskola, anslag, gymnasieskola, budgetår, hög, verksamhet, kurs, medel | 3/4 | 0.734 | 0.692 | 0.382 |
| 3 | elev, undervisning, ämne, lärare, grundskola, gymnasieskola, språk, kunskap | 4/4 | 0.934 | 0.859 | 0.656 |
| 4 | kommun, elev, samhälle, behov, verksamhet, många, ansvar, kunskap | 2/4 | 0.575 | 0.288 | 0.195 |
| 5 | högskola, län, utveckling, region, hög, teknisk, behov, land | 4/4 | 0.894 | 0.843 | 0.552 |
| 6 | kunskap, ämne, människa, hälsa, barn, samhälle, många, undervisning | 2/4 | 0.685 | 0.565 | 0.279 |
| 7 | lärare, poäng, universitet, behov, linje, umeå, lärarutbildning, stockholm | 1/4 | 0.645 | 0.413 | 0.302 |
| 8 | forskning, universitet, högskola, område, internationell, professur, svensk, land | 3/4 | 0.834 | 0.565 | 0.504 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7389
- Median: 0.7675
- Min: 0.2808
- Max: 0.9495
- Std Dev: 0.2042

**Jaccard Similarity (top 20 words):**
- Mean: 0.4009
- Median: 0.3563
- Min: 0.1111
- Max: 0.6000
- Std Dev: 0.1715

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7711
- Median: 0.8477
- Min: 0.2883
- Max: 0.9852
- Std Dev: 0.2484

**Jaccard Similarity (top 20 words):**
- Mean: 0.5160
- Median: 0.4815
- Min: 0.0526
- Max: 0.9048
- Std Dev: 0.2953

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6627
- Median: 0.6913
- Min: 0.2620
- Max: 0.8590
- Std Dev: 0.1809

**Jaccard Similarity (top 20 words):**
- Mean: 0.3044
- Median: 0.2917
- Min: 0.0526
- Max: 0.5385
- Std Dev: 0.1591

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6393
- Median: 0.6362
- Min: 0.3133
- Max: 0.9459
- Std Dev: 0.2229

**Jaccard Similarity (top 20 words):**
- Mean: 0.2693
- Median: 0.1964
- Min: 0.1429
- Max: 0.6667
- Std Dev: 0.1697

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6796
- Median: 0.7122
- Min: 0.3568
- Max: 0.9417
- Std Dev: 0.2043

**Jaccard Similarity (top 20 words):**
- Mean: 0.3642
- Median: 0.4144
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.2004

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7367
- Median: 0.8073
- Min: 0.4727
- Max: 0.9119
- Std Dev: 0.1667

**Jaccard Similarity (top 20 words):**
- Mean: 0.4101
- Median: 0.4815
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.2249

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7216
- Median: 0.7431
- Min: 0.4201
- Max: 0.8974
- Std Dev: 0.1702

**Jaccard Similarity (top 20 words):**
- Mean: 0.3657
- Median: 0.3563
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.1645

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6370
- Median: 0.6397
- Min: 0.3369
- Max: 0.8435
- Std Dev: 0.1682

**Jaccard Similarity (top 20 words):**
- Mean: 0.3079
- Median: 0.2311
- Min: 0.1111
- Max: 0.5385
- Std Dev: 0.1546

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6987
- Median: 0.7752
- Min: 0.2531
- Max: 0.9769
- Std Dev: 0.2255

**Jaccard Similarity (top 20 words):**
- Mean: 0.2957
- Median: 0.2903
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.1709

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6801
- Median: 0.7348
- Min: 0.3098
- Max: 0.9282
- Std Dev: 0.2314

**Jaccard Similarity (top 20 words):**
- Mean: 0.3664
- Median: 0.3810
- Min: 0.1111
- Max: 0.6000
- Std Dev: 0.1920

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6966
- Median: 0.7704
- Min: 0.2531
- Max: 0.9852
- Std Dev: 0.2086

### Jaccard Similarity (across all matches)
- Mean: 0.3600
- Median: 0.3333
- Min: 0.0526
- Max: 0.9048
- Std Dev: 0.2062
