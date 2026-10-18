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
| 42 | 1606.33 | 50 |
| 123 | 1626.34 | 50 |
| 456 | 1598.89 | 50 |
| 789 | 1610.48 | 50 |
| 999 | 1616.75 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 0 |
| 2 of 4 | 1 |
| 1 of 4 | 2 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | forskning, universitet, område, land, professur, verksamhet, viktig, svensk | 1/4 | 0.571 | 0.209 | 0.280 |
| 2 | högskola, län, utveckling, region, hög, teknisk, universitet, land | 4/4 | 0.907 | 0.779 | 0.558 |
| 3 | ämne, gymnasieskola, elev, undervisning, språk, lärare, svensk, kunskap | 2/4 | 0.766 | 0.670 | 0.430 |
| 4 | barn, hälsa, kunskap, människa, idrott, samhälle, vård, många | 1/4 | 0.662 | 0.594 | 0.282 |
| 5 | skola, elev, barn, lärare, förälder, grundskola, undervisning, viktig | 4/4 | 0.853 | 0.725 | 0.414 |
| 6 | kommun, skola, gymnasieskola, bidrag, verksamhet, elev, kommunal, statsbidrag | 4/4 | 0.838 | 0.753 | 0.535 |
| 7 | högskola, forskning, universitet, förslag, hög, liten, medel, möjlighet | 4/4 | 0.923 | 0.897 | 0.542 |
| 8 | universitet, anslag, förslag, budgetår, poäng, linje, studerande, kurs | 0/4 | 0.626 | 0.551 | 0.273 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7614
- Median: 0.7394
- Min: 0.5976
- Max: 0.9857
- Std Dev: 0.1377

**Jaccard Similarity (top 20 words):**
- Mean: 0.3974
- Median: 0.3563
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.1824

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7873
- Median: 0.7897
- Min: 0.6074
- Max: 0.9545
- Std Dev: 0.1516

**Jaccard Similarity (top 20 words):**
- Mean: 0.4371
- Median: 0.4304
- Min: 0.2500
- Max: 0.6667
- Std Dev: 0.1470

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7935
- Median: 0.8771
- Min: 0.2093
- Max: 0.9843
- Std Dev: 0.2352

**Jaccard Similarity (top 20 words):**
- Mean: 0.4359
- Median: 0.4815
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.1812

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7303
- Median: 0.7722
- Min: 0.4774
- Max: 0.9534
- Std Dev: 0.1602

**Jaccard Similarity (top 20 words):**
- Mean: 0.3870
- Median: 0.4550
- Min: 0.1111
- Max: 0.6667
- Std Dev: 0.1843

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7581
- Median: 0.8352
- Min: 0.4410
- Max: 0.9387
- Std Dev: 0.1914

**Jaccard Similarity (top 20 words):**
- Mean: 0.4180
- Median: 0.4589
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.1883

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6814
- Median: 0.8007
- Min: 0.2110
- Max: 0.9310
- Std Dev: 0.2618

**Jaccard Similarity (top 20 words):**
- Mean: 0.4028
- Median: 0.4359
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.2174

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7111
- Median: 0.7485
- Min: 0.4805
- Max: 0.9116
- Std Dev: 0.1464

**Jaccard Similarity (top 20 words):**
- Mean: 0.3264
- Median: 0.2903
- Min: 0.1429
- Max: 0.6667
- Std Dev: 0.1486

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7802
- Median: 0.9348
- Min: 0.1278
- Max: 0.9886
- Std Dev: 0.2970

**Jaccard Similarity (top 20 words):**
- Mean: 0.5151
- Median: 0.5692
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2967

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7416
- Median: 0.8321
- Min: 0.2783
- Max: 0.9958
- Std Dev: 0.2466

**Jaccard Similarity (top 20 words):**
- Mean: 0.3935
- Median: 0.3793
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2444

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6835
- Median: 0.7624
- Min: 0.2519
- Max: 0.9863
- Std Dev: 0.2562

**Jaccard Similarity (top 20 words):**
- Mean: 0.3984
- Median: 0.4039
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2252

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7428
- Median: 0.8111
- Min: 0.1278
- Max: 0.9958
- Std Dev: 0.2189

### Jaccard Similarity (across all matches)
- Mean: 0.4112
- Median: 0.3793
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2111
