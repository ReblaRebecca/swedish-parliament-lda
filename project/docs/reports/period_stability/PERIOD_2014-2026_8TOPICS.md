# Seed-Stability Analysis: Period 2014/15–2025/26, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2014/15–2025/26 (3222)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1517.80 | 50 |
| 123 | 1524.08 | 50 |
| 456 | 1541.75 | 50 |
| 789 | 1538.42 | 50 |
| 999 | 1501.77 | 50 |

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
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, förälder, ung, samhälle, svensk, språk, verksamhet | 4/4 | 0.919 | 0.860 | 0.420 |
| 2 | forskning, högskola, universitet, nivå, avancerad, grundnivå, forskarnivå, lärosäte | 4/4 | 0.901 | 0.866 | 0.555 |
| 3 | kommun, friskola, kommunal, verksamhet, fristående, skolinspektion, likvärdig, svensk | 3/4 | 0.770 | 0.389 | 0.374 |
| 4 | behov, arbetsmarknad, hög, kommun, student, studie, öka, yrkeshögskola | 2/4 | 0.703 | 0.616 | 0.312 |
| 5 | barn, stöd, lärare, nationell, betyg, behov, särskild, kunskap | 2/4 | 0.574 | 0.235 | 0.243 |
| 6 | student, kunskap, ung, företag, gymnasieskola, ungdom, arbetsmarknad, gymnasium | 1/4 | 0.530 | 0.224 | 0.142 |
| 7 | lärare, förskola, barn, svensk, undervisning, pedagogisk, kvalitet, stärka | 4/4 | 0.899 | 0.877 | 0.459 |
| 8 | forskning, svensk, land, hög, utveckling, stärka, internationell, forskare | 3/4 | 0.719 | 0.490 | 0.355 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7869
- Median: 0.8270
- Min: 0.4984
- Max: 0.9490
- Std Dev: 0.1475

**Jaccard Similarity (top 20 words):**
- Mean: 0.3805
- Median: 0.3810
- Min: 0.1429
- Max: 0.5385
- Std Dev: 0.1310

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6775
- Median: 0.6930
- Min: 0.3891
- Max: 0.9354
- Std Dev: 0.1928

**Jaccard Similarity (top 20 words):**
- Mean: 0.2719
- Median: 0.2702
- Min: 0.1111
- Max: 0.6000
- Std Dev: 0.1536

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7737
- Median: 0.8588
- Min: 0.2236
- Max: 0.9437
- Std Dev: 0.2260

**Jaccard Similarity (top 20 words):**
- Mean: 0.4119
- Median: 0.4815
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1742

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7691
- Median: 0.8440
- Min: 0.2348
- Max: 0.9241
- Std Dev: 0.2110

**Jaccard Similarity (top 20 words):**
- Mean: 0.3661
- Median: 0.4039
- Min: 0.0526
- Max: 0.5385
- Std Dev: 0.1628

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7385
- Median: 0.8335
- Min: 0.2613
- Max: 0.9213
- Std Dev: 0.2054

**Jaccard Similarity (top 20 words):**
- Mean: 0.3492
- Median: 0.2917
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.1926

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7144
- Median: 0.8603
- Min: 0.2123
- Max: 0.9352
- Std Dev: 0.2737

**Jaccard Similarity (top 20 words):**
- Mean: 0.3920
- Median: 0.4039
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2534

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7377
- Median: 0.7407
- Min: 0.5197
- Max: 0.9907
- Std Dev: 0.1532

**Jaccard Similarity (top 20 words):**
- Mean: 0.3774
- Median: 0.2903
- Min: 0.1429
- Max: 0.9048
- Std Dev: 0.2322

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7150
- Median: 0.7441
- Min: 0.3612
- Max: 0.9926
- Std Dev: 0.2278

**Jaccard Similarity (top 20 words):**
- Mean: 0.3802
- Median: 0.2903
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2694

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7257
- Median: 0.7003
- Min: 0.4223
- Max: 0.9557
- Std Dev: 0.1752

**Jaccard Similarity (top 20 words):**
- Mean: 0.3832
- Median: 0.3563
- Min: 0.1429
- Max: 0.6667
- Std Dev: 0.1747

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8066
- Median: 0.8556
- Min: 0.3813
- Max: 0.9683
- Std Dev: 0.1742

**Jaccard Similarity (top 20 words):**
- Mean: 0.4391
- Median: 0.4286
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.1789

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7445
- Median: 0.8128
- Min: 0.2123
- Max: 0.9926
- Std Dev: 0.2054

### Jaccard Similarity (across all matches)
- Mean: 0.3751
- Median: 0.3563
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2013
