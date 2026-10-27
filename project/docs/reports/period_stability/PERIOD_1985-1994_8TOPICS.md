# Seed-Stability Analysis: Period 1985/86–1993/94, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1985/86–1993/94 (3613)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1649.16 | 50 |
| 123 | 1655.35 | 50 |
| 456 | 1651.23 | 50 |
| 789 | 1624.72 | 50 |
| 999 | 1646.95 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 2 |
| 2 of 4 | 1 |
| 1 of 4 | 1 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | forskning, högskola, universitet, förslag, område, verksamhet, utveckling, resurs | 4/4 | 0.946 | 0.822 | 0.794 |
| 2 | elev, gymnasieskola, lärare, ämne, kunskap, skola, betyg, förslag | 0/4 | 0.485 | 0.096 | 0.189 |
| 3 | kunskap, hälsa, människa, barn, samhälle, miljö, problem, ämne | 3/4 | 0.755 | 0.509 | 0.370 |
| 4 | högskola, län, universitet, region, hög, plats, land, stockholm | 3/4 | 0.749 | 0.481 | 0.425 |
| 5 | skola, elev, kommun, barn, förälder, fristående, grundskola, ansvar | 4/4 | 0.952 | 0.928 | 0.539 |
| 6 | anslag, folkhögskola, vuxenutbildning, verksamhet, bidrag, studieförbund, budgetår, medel | 2/4 | 0.745 | 0.575 | 0.534 |
| 7 | ämne, språk, svensk, undervisning, land, invandrare, kunskap, samhälle | 1/4 | 0.424 | 0.148 | 0.181 |
| 8 | högskola, teknisk, linje, poäng, kurs, karlstad, utveckling, område | 4/4 | 0.828 | 0.710 | 0.348 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7231
- Median: 0.7413
- Min: 0.5089
- Max: 0.9362
- Std Dev: 0.1408

**Jaccard Similarity (top 20 words):**
- Mean: 0.3570
- Median: 0.3810
- Min: 0.1429
- Max: 0.5385
- Std Dev: 0.1277

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7146
- Median: 0.8601
- Min: 0.0960
- Max: 0.9750
- Std Dev: 0.3144

**Jaccard Similarity (top 20 words):**
- Mean: 0.4083
- Median: 0.4286
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2463

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7803
- Median: 0.8256
- Min: 0.4811
- Max: 0.9921
- Std Dev: 0.1804

**Jaccard Similarity (top 20 words):**
- Mean: 0.5085
- Median: 0.4039
- Min: 0.1765
- Max: 0.8182
- Std Dev: 0.2511

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7237
- Median: 0.7701
- Min: 0.1478
- Max: 0.9933
- Std Dev: 0.2546

**Jaccard Similarity (top 20 words):**
- Mean: 0.4165
- Median: 0.3594
- Min: 0.0526
- Max: 1.0000
- Std Dev: 0.2626

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6954
- Median: 0.6861
- Min: 0.4475
- Max: 0.9935
- Std Dev: 0.1813

**Jaccard Similarity (top 20 words):**
- Mean: 0.3460
- Median: 0.2727
- Min: 0.1111
- Max: 1.0000
- Std Dev: 0.2647

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7665
- Median: 0.7404
- Min: 0.6150
- Max: 0.9636
- Std Dev: 0.1356

**Jaccard Similarity (top 20 words):**
- Mean: 0.3962
- Median: 0.3859
- Min: 0.1765
- Max: 0.7391
- Std Dev: 0.1827

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7008
- Median: 0.7574
- Min: 0.2103
- Max: 0.9932
- Std Dev: 0.2424

**Jaccard Similarity (top 20 words):**
- Mean: 0.4147
- Median: 0.4074
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2418

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7740
- Median: 0.8249
- Min: 0.3555
- Max: 0.9848
- Std Dev: 0.2007

**Jaccard Similarity (top 20 words):**
- Mean: 0.4762
- Median: 0.5100
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2190

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7155
- Median: 0.8742
- Min: 0.0997
- Max: 0.9917
- Std Dev: 0.3157

**Jaccard Similarity (top 20 words):**
- Mean: 0.4470
- Median: 0.4359
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2920

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7499
- Median: 0.7874
- Min: 0.3150
- Max: 0.9925
- Std Dev: 0.2293

**Jaccard Similarity (top 20 words):**
- Mean: 0.3970
- Median: 0.2957
- Min: 0.1111
- Max: 0.8182
- Std Dev: 0.2476

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7344
- Median: 0.8070
- Min: 0.0960
- Max: 0.9935
- Std Dev: 0.2296

### Jaccard Similarity (across all matches)
- Mean: 0.4167
- Median: 0.3793
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2424
