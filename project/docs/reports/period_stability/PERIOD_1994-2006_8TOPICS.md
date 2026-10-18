# Seed-Stability Analysis: Period 1994/95–2005/06, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3477)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1609.60 | 50 |
| 123 | 1610.34 | 50 |
| 456 | 1628.69 | 50 |
| 789 | 1628.76 | 50 |
| 999 | 1620.71 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 3 |
| 2 of 4 | 2 |
| 1 of 4 | 0 |
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | student, högskola, studie, system, studerande, enskild, yrkesutbildning, studera | 4/4 | 0.921 | 0.870 | 0.526 |
| 2 | barn, mobbning, elev, arbete, ungdom, samhälle, fysisk, kunskap | 3/4 | 0.874 | 0.642 | 0.600 |
| 3 | högskola, universitet, forskning, anslag, forskarutbildning, grundutbildning, medel, kvalitet | 3/4 | 0.763 | 0.390 | 0.329 |
| 4 | barn, förskola, förälder, kommun, elev, verksamhet, barnomsorg, funktionshind | 4/4 | 0.915 | 0.860 | 0.498 |
| 5 | forskning, högskola, universitet, svensk, utveckling, forskare, kvinna, kunskap | 3/4 | 0.748 | 0.292 | 0.425 |
| 6 | högskola, land, utveckling, företag, region, universitet, utveckla, område | 2/4 | 0.739 | 0.459 | 0.364 |
| 7 | elev, lärare, gymnasieskola, kunskap, betyg, grundskola, undervisning, ämne | 4/4 | 0.960 | 0.911 | 0.659 |
| 8 | kommun, fristående, elev, kommunal, friskola, skolverket, verksamhet, bidrag | 2/4 | 0.552 | 0.205 | 0.189 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.8025
- Median: 0.8991
- Min: 0.3748
- Max: 0.9902
- Std Dev: 0.2277

**Jaccard Similarity (top 20 words):**
- Mean: 0.4661
- Median: 0.4835
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2656

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8674
- Median: 0.8741
- Min: 0.8047
- Max: 0.9212
- Std Dev: 0.0435

**Jaccard Similarity (top 20 words):**
- Mean: 0.4501
- Median: 0.4039
- Min: 0.2903
- Max: 0.6667
- Std Dev: 0.1138

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7987
- Median: 0.9542
- Min: 0.2046
- Max: 0.9851
- Std Dev: 0.2934

**Jaccard Similarity (top 20 words):**
- Mean: 0.5384
- Median: 0.6667
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2502

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7678
- Median: 0.8525
- Min: 0.2917
- Max: 0.9540
- Std Dev: 0.2093

**Jaccard Similarity (top 20 words):**
- Mean: 0.3406
- Median: 0.3333
- Min: 0.0526
- Max: 0.5385
- Std Dev: 0.1523

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8050
- Median: 0.8349
- Min: 0.5661
- Max: 0.9871
- Std Dev: 0.1328

**Jaccard Similarity (top 20 words):**
- Mean: 0.4621
- Median: 0.4550
- Min: 0.2121
- Max: 0.7391
- Std Dev: 0.1989

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7736
- Median: 0.9190
- Min: 0.2849
- Max: 0.9674
- Std Dev: 0.2611

**Jaccard Similarity (top 20 words):**
- Mean: 0.4673
- Median: 0.5385
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2765

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7896
- Median: 0.8480
- Min: 0.5268
- Max: 0.9542
- Std Dev: 0.1493

**Jaccard Similarity (top 20 words):**
- Mean: 0.4437
- Median: 0.4589
- Min: 0.1765
- Max: 0.6667
- Std Dev: 0.1742

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7042
- Median: 0.8140
- Min: 0.1659
- Max: 0.9530
- Std Dev: 0.2378

**Jaccard Similarity (top 20 words):**
- Mean: 0.3695
- Median: 0.3563
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1750

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7504
- Median: 0.8306
- Min: 0.4915
- Max: 0.9447
- Std Dev: 0.1743

**Jaccard Similarity (top 20 words):**
- Mean: 0.4272
- Median: 0.4304
- Min: 0.1765
- Max: 0.7391
- Std Dev: 0.1846

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7352
- Median: 0.8117
- Min: 0.1689
- Max: 0.9733
- Std Dev: 0.2548

**Jaccard Similarity (top 20 words):**
- Mean: 0.3512
- Median: 0.3594
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1912

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7794
- Median: 0.8649
- Min: 0.1659
- Max: 0.9902
- Std Dev: 0.2148

### Jaccard Similarity (across all matches)
- Mean: 0.4316
- Median: 0.4286
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2123
