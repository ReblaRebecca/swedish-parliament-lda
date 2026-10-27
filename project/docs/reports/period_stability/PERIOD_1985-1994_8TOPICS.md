# Seed-Stability Analysis: Period 1985/86–1993/94, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1985/86–1993/94 (3467)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1649.42 | 50 |
| 123 | 1637.28 | 50 |
| 456 | 1634.23 | 50 |
| 789 | 1627.00 | 50 |
| 999 | 1649.81 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 0 |
| 2 of 4 | 2 |
| 1 of 4 | 1 |
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | göteborg, umeå, medicinsk, hälsa, lund, stockholm, landsting, vård | 4/4 | 0.773 | 0.725 | 0.339 |
| 2 | kommun, skola, gymnasieskola, elev, förslag, kommunal, fristående, social | 1/4 | 0.572 | 0.311 | 0.295 |
| 3 | högskola, län, teknisk, region, utveckling, plats, linje, land | 4/4 | 0.945 | 0.896 | 0.645 |
| 4 | lärare, lärarutbildning, ämne, linje, poäng, årskurs, elev, undervisning | 2/4 | 0.539 | 0.322 | 0.234 |
| 5 | forskning, högskola, universitet, förslag, område, resurs, verksamhet, utveckling | 4/4 | 0.933 | 0.847 | 0.694 |
| 6 | ämne, undervisning, svensk, språk, människa, kunskap, samhälle, timme | 2/4 | 0.603 | 0.234 | 0.239 |
| 7 | anslag, vuxenutbildning, kunskap, folkhögskola, hög, verksamhet, budgetår, medel | 4/4 | 0.845 | 0.802 | 0.431 |
| 8 | skola, elev, barn, kunskap, grundskola, förälder, undervisning, lärare | 4/4 | 0.961 | 0.932 | 0.541 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7518
- Median: 0.7934
- Min: 0.2341
- Max: 0.9758
- Std Dev: 0.2340

**Jaccard Similarity (top 20 words):**
- Mean: 0.4065
- Median: 0.3810
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2039

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8380
- Median: 0.8182
- Min: 0.6873
- Max: 0.9891
- Std Dev: 0.1189

**Jaccard Similarity (top 20 words):**
- Mean: 0.5049
- Median: 0.4304
- Min: 0.2500
- Max: 0.9048
- Std Dev: 0.2234

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8068
- Median: 0.8644
- Min: 0.3216
- Max: 0.9787
- Std Dev: 0.1984

**Jaccard Similarity (top 20 words):**
- Mean: 0.4733
- Median: 0.4815
- Min: 0.1765
- Max: 0.8182
- Std Dev: 0.1943

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6896
- Median: 0.7632
- Min: 0.3106
- Max: 0.9317
- Std Dev: 0.2253

**Jaccard Similarity (top 20 words):**
- Mean: 0.3242
- Median: 0.2903
- Min: 0.1765
- Max: 0.5385
- Std Dev: 0.1339

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7981
- Median: 0.9194
- Min: 0.2570
- Max: 0.9590
- Std Dev: 0.2276

**Jaccard Similarity (top 20 words):**
- Mean: 0.4764
- Median: 0.5692
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2257

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7642
- Median: 0.8111
- Min: 0.3362
- Max: 0.9724
- Std Dev: 0.2159

**Jaccard Similarity (top 20 words):**
- Mean: 0.4757
- Median: 0.5230
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2696

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7594
- Median: 0.8309
- Min: 0.2208
- Max: 0.9756
- Std Dev: 0.2387

**Jaccard Similarity (top 20 words):**
- Mean: 0.4361
- Median: 0.4550
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2430

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8514
- Median: 0.8882
- Min: 0.6489
- Max: 0.9932
- Std Dev: 0.1246

**Jaccard Similarity (top 20 words):**
- Mean: 0.5492
- Median: 0.6026
- Min: 0.1765
- Max: 0.8182
- Std Dev: 0.1892

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8077
- Median: 0.8929
- Min: 0.4877
- Max: 0.9808
- Std Dev: 0.1625

**Jaccard Similarity (top 20 words):**
- Mean: 0.4688
- Median: 0.5385
- Min: 0.1429
- Max: 0.7391
- Std Dev: 0.1928

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8299
- Median: 0.8690
- Min: 0.3709
- Max: 0.9835
- Std Dev: 0.1811

**Jaccard Similarity (top 20 words):**
- Mean: 0.4530
- Median: 0.4286
- Min: 0.1765
- Max: 0.7391
- Std Dev: 0.1613

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7897
- Median: 0.8509
- Min: 0.2208
- Max: 0.9932
- Std Dev: 0.2026

### Jaccard Similarity (across all matches)
- Mean: 0.4568
- Median: 0.4815
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2148
