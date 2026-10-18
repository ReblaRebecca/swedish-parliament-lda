# Seed-Stability Analysis: Period 2014/15–2025/26, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2014/15–2025/26 (3572)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1510.87 | 50 |
| 123 | 1495.04 | 50 |
| 456 | 1523.54 | 50 |
| 789 | 1528.13 | 50 |
| 999 | 1529.94 | 50 |

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
| 1 of 4 | 0 |
| 0 of 4 | 2 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | kommun, friskola, svensk, kommunal, verksamhet, språk, land, samhälle | 0/4 | 0.611 | 0.572 | 0.215 |
| 2 | lärare, undervisning, svensk, nationell, stöd, kunskap, grundskola, betyg | 4/4 | 0.929 | 0.864 | 0.679 |
| 3 | barn, förskola, förälder, kommun, pedagogisk, verksamhet, fritidshem, personal | 2/4 | 0.668 | 0.210 | 0.297 |
| 4 | forskning, högskola, universitet, nivå, avancerad, hög, grundnivå, forskarnivå | 4/4 | 0.882 | 0.830 | 0.468 |
| 5 | barn, ung, stöd, psykisk, våld, kunskap, arbete, samhälle | 3/4 | 0.797 | 0.622 | 0.351 |
| 6 | svensk, kunskap, ämne, land, aktivitet, hälsa, idrott, utveckling | 0/4 | 0.506 | 0.422 | 0.204 |
| 7 | student, hög, studie, lärosäte, universitet, högskola, studiemedel, studera | 3/4 | 0.772 | 0.625 | 0.411 |
| 8 | arbetsmarknad, företag, ung, behov, kunskap, jobb, hög, kompetens | 4/4 | 0.908 | 0.857 | 0.457 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.8173
- Median: 0.8705
- Min: 0.4415
- Max: 0.9738
- Std Dev: 0.1772

**Jaccard Similarity (top 20 words):**
- Mean: 0.4551
- Median: 0.4550
- Min: 0.2121
- Max: 0.8182
- Std Dev: 0.1761

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7464
- Median: 0.7912
- Min: 0.4224
- Max: 0.9783
- Std Dev: 0.1693

**Jaccard Similarity (top 20 words):**
- Mean: 0.3455
- Median: 0.2917
- Min: 0.1765
- Max: 0.8182
- Std Dev: 0.1949

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6962
- Median: 0.7486
- Min: 0.2100
- Max: 0.9040
- Std Dev: 0.2293

**Jaccard Similarity (top 20 words):**
- Mean: 0.3687
- Median: 0.3594
- Min: 0.1111
- Max: 0.6000
- Std Dev: 0.1578

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7759
- Median: 0.8210
- Min: 0.5652
- Max: 0.9715
- Std Dev: 0.1326

**Jaccard Similarity (top 20 words):**
- Mean: 0.3719
- Median: 0.3563
- Min: 0.1429
- Max: 0.6667
- Std Dev: 0.1731

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8313
- Median: 0.8738
- Min: 0.6069
- Max: 0.9860
- Std Dev: 0.1476

**Jaccard Similarity (top 20 words):**
- Mean: 0.4757
- Median: 0.4074
- Min: 0.2121
- Max: 0.9048
- Std Dev: 0.2324

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7666
- Median: 0.8367
- Min: 0.4213
- Max: 0.9823
- Std Dev: 0.2099

**Jaccard Similarity (top 20 words):**
- Mean: 0.3911
- Median: 0.4250
- Min: 0.0811
- Max: 0.7391
- Std Dev: 0.2681

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7937
- Median: 0.8597
- Min: 0.6364
- Max: 0.9024
- Std Dev: 0.1064

**Jaccard Similarity (top 20 words):**
- Mean: 0.3769
- Median: 0.3793
- Min: 0.2121
- Max: 0.6000
- Std Dev: 0.1450

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7729
- Median: 0.8514
- Min: 0.3634
- Max: 0.9733
- Std Dev: 0.2024

**Jaccard Similarity (top 20 words):**
- Mean: 0.3946
- Median: 0.2903
- Min: 0.1429
- Max: 0.7391
- Std Dev: 0.2402

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7707
- Median: 0.8284
- Min: 0.5828
- Max: 0.9380
- Std Dev: 0.1266

**Jaccard Similarity (top 20 words):**
- Mean: 0.3372
- Median: 0.3563
- Min: 0.1429
- Max: 0.4815
- Std Dev: 0.1108

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7054
- Median: 0.7222
- Min: 0.3426
- Max: 0.9670
- Std Dev: 0.1812

**Jaccard Similarity (top 20 words):**
- Mean: 0.3192
- Median: 0.3333
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.1608

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7676
- Median: 0.8296
- Min: 0.2100
- Max: 0.9860
- Std Dev: 0.1772

### Jaccard Similarity (across all matches)
- Mean: 0.3836
- Median: 0.3333
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.1971
