# Seed-Stability Analysis: Period 1985/86–1993/94, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1985/86–1993/94 (3737)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1630.59 | 50 |
| 123 | 1629.56 | 50 |
| 456 | 1618.09 | 50 |
| 789 | 1618.12 | 50 |
| 999 | 1612.47 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 2 |
| 2 of 4 | 2 |
| 1 of 4 | 1 |
| 0 of 4 | 3 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | svensk, kunskap, land, samhälle, hög, många, språk, människa | 2/4 | 0.715 | 0.583 | 0.360 |
| 2 | lärare, lärarutbildning, kvinna, ämne, flicka, årskurs, grundskola, grundskollärarutbildning | 0/4 | 0.319 | 0.119 | 0.077 |
| 3 | forskning, högskola, universitet, område, resurs, verksamhet, förslag, liten | 4/4 | 0.952 | 0.877 | 0.689 |
| 4 | problem, människa, hälsa, invandrare, många, kunskap, barn, medicinsk | 1/4 | 0.575 | 0.451 | 0.280 |
| 5 | anslag, förslag, budgetår, vuxenutbildning, medel, verksamhet, bidrag, kommun | 3/4 | 0.845 | 0.633 | 0.578 |
| 6 | högskola, linje, poäng, studerande, kurs, student, social, förslag | 2/4 | 0.721 | 0.595 | 0.300 |
| 7 | göteborg, kommun, statlig, stat, statsbidrag, skola, verksamhet, malmö | 0/4 | 0.345 | 0.091 | 0.128 |
| 8 | högskola, län, region, utveckling, hög, teknisk, universitet, land | 4/4 | 0.883 | 0.815 | 0.473 |
| 9 | ämne, undervisning, kunskap, språk, elev, barn, gymnasieskola, läroplan | 3/4 | 0.719 | 0.414 | 0.323 |
| 10 | folkhögskola, idrott, elev, verksamhet, fritid, fysisk, härnösand, läsa | 0/4 | 0.340 | 0.155 | 0.126 |
| 11 | skola, elev, barn, kommun, lärare, grundskola, undervisning, förälder | 4/4 | 0.977 | 0.940 | 0.746 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6937
- Median: 0.6933
- Min: 0.0909
- Max: 0.9960
- Std Dev: 0.2619

**Jaccard Similarity (top 20 words):**
- Mean: 0.3834
- Median: 0.2903
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.3008

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6689
- Median: 0.7935
- Min: 0.1553
- Max: 0.9892
- Std Dev: 0.3080

**Jaccard Similarity (top 20 words):**
- Mean: 0.4208
- Median: 0.3793
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2888

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6749
- Median: 0.7644
- Min: 0.2351
- Max: 0.9838
- Std Dev: 0.2201

**Jaccard Similarity (top 20 words):**
- Mean: 0.3734
- Median: 0.3793
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.1776

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6503
- Median: 0.5952
- Min: 0.1194
- Max: 0.9835
- Std Dev: 0.2582

**Jaccard Similarity (top 20 words):**
- Mean: 0.3059
- Median: 0.2903
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.1967

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7039
- Median: 0.6907
- Min: 0.2682
- Max: 0.9901
- Std Dev: 0.2181

**Jaccard Similarity (top 20 words):**
- Mean: 0.4144
- Median: 0.3333
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2290

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6752
- Median: 0.7040
- Min: 0.3647
- Max: 0.9812
- Std Dev: 0.2228

**Jaccard Similarity (top 20 words):**
- Mean: 0.3424
- Median: 0.3793
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2175

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7599
- Median: 0.9050
- Min: 0.2513
- Max: 0.9792
- Std Dev: 0.2306

**Jaccard Similarity (top 20 words):**
- Mean: 0.4281
- Median: 0.4286
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2317

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7214
- Median: 0.7762
- Min: 0.3292
- Max: 0.9702
- Std Dev: 0.2014

**Jaccard Similarity (top 20 words):**
- Mean: 0.4121
- Median: 0.4286
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2296

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7143
- Median: 0.7675
- Min: 0.3977
- Max: 0.9820
- Std Dev: 0.2030

**Jaccard Similarity (top 20 words):**
- Mean: 0.4216
- Median: 0.4286
- Min: 0.0811
- Max: 0.7391
- Std Dev: 0.2155

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6956
- Median: 0.7795
- Min: 0.0824
- Max: 0.9808
- Std Dev: 0.2556

**Jaccard Similarity (top 20 words):**
- Mean: 0.4010
- Median: 0.4286
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2261

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6958
- Median: 0.7659
- Min: 0.0824
- Max: 0.9960
- Std Dev: 0.2419

### Jaccard Similarity (across all matches)
- Mean: 0.3903
- Median: 0.3793
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2371
