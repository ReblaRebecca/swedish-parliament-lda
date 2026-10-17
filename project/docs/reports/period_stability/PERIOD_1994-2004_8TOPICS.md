# Seed-Stability Analysis: Period 1994-2004, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of 1994-2004 (3313)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1725.40 | 50 |
| 123 | 1709.50 | 50 |
| 456 | 1704.51 | 50 |
| 789 | 1685.27 | 50 |
| 999 | 1679.32 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 0 |
| 2 of 4 | 0 |
| 1 of 4 | 1 |
| 0 of 4 | 3 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | student, hög, gymnasieskola, studie, lärare, högskola, många, kunskap | 4/4 | 0.902 | 0.842 | 0.419 |
| 2 | elev, mobbning, lärare, betyg, kunskap, undervisning, barn, nationell | 4/4 | 0.883 | 0.835 | 0.537 |
| 3 | körkort, ungdom, homo, människa, folkhögskola, homosexuell, tv, fråga | 0/4 | 0.360 | 0.340 | 0.098 |
| 4 | län, land, region, företag, utveckling, område, kommun, teknik | 0/4 | 0.514 | 0.277 | 0.357 |
| 5 | forskning, kvinna, svensk, universitet, samhälle, kunskap, forskare, verksamhet | 1/4 | 0.567 | 0.403 | 0.232 |
| 6 | högskola, universitet, forskning, hög, anslag, student, utveckling, resurs | 4/4 | 0.918 | 0.881 | 0.524 |
| 7 | hälsa, fysisk, idrott, ungdom, aktivitet, ämne, stat, procent | 0/4 | 0.468 | 0.260 | 0.207 |
| 8 | barn, elev, kommun, förälder, förskola, fristående, behov, lärare | 4/4 | 0.910 | 0.876 | 0.484 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7302
- Median: 0.7965
- Min: 0.3663
- Max: 0.9400
- Std Dev: 0.2258

**Jaccard Similarity (top 20 words):**
- Mean: 0.4062
- Median: 0.5100
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2251

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6934
- Median: 0.8787
- Min: 0.2602
- Max: 0.9154
- Std Dev: 0.2628

**Jaccard Similarity (top 20 words):**
- Mean: 0.3578
- Median: 0.4039
- Min: 0.1111
- Max: 0.6000
- Std Dev: 0.1565

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7094
- Median: 0.7467
- Min: 0.3396
- Max: 0.9382
- Std Dev: 0.2072

**Jaccard Similarity (top 20 words):**
- Mean: 0.3330
- Median: 0.4039
- Min: 0.0526
- Max: 0.5385
- Std Dev: 0.1636

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6279
- Median: 0.6268
- Min: 0.2768
- Max: 0.9361
- Std Dev: 0.2640

**Jaccard Similarity (top 20 words):**
- Mean: 0.3319
- Median: 0.3348
- Min: 0.1765
- Max: 0.5385
- Std Dev: 0.1432

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7512
- Median: 0.8905
- Min: 0.3896
- Max: 0.9633
- Std Dev: 0.2334

**Jaccard Similarity (top 20 words):**
- Mean: 0.4083
- Median: 0.4589
- Min: 0.0811
- Max: 0.7391
- Std Dev: 0.2358

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8066
- Median: 0.8997
- Min: 0.3376
- Max: 0.9880
- Std Dev: 0.2137

**Jaccard Similarity (top 20 words):**
- Mean: 0.4831
- Median: 0.5100
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2577

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7491
- Median: 0.8150
- Min: 0.2531
- Max: 0.9695
- Std Dev: 0.2364

**Jaccard Similarity (top 20 words):**
- Mean: 0.3930
- Median: 0.4074
- Min: 0.0811
- Max: 0.6000
- Std Dev: 0.1823

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7779
- Median: 0.8788
- Min: 0.2554
- Max: 0.9750
- Std Dev: 0.2377

**Jaccard Similarity (top 20 words):**
- Mean: 0.4266
- Median: 0.3810
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2399

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6097
- Median: 0.6191
- Min: 0.2615
- Max: 0.8837
- Std Dev: 0.2326

**Jaccard Similarity (top 20 words):**
- Mean: 0.2373
- Median: 0.2166
- Min: 0.0526
- Max: 0.4286
- Std Dev: 0.1415

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6819
- Median: 0.6917
- Min: 0.2712
- Max: 0.9500
- Std Dev: 0.2248

**Jaccard Similarity (top 20 words):**
- Mean: 0.3208
- Median: 0.3118
- Min: 0.0811
- Max: 0.5385
- Std Dev: 0.1378

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7137
- Median: 0.8386
- Min: 0.2531
- Max: 0.9880
- Std Dev: 0.2419

### Jaccard Similarity (across all matches)
- Mean: 0.3698
- Median: 0.3793
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2041
