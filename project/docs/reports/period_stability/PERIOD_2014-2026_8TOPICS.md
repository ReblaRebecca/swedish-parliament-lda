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
| 42 | 1558.86 | 50 |
| 123 | 1554.70 | 50 |
| 456 | 1575.78 | 50 |
| 789 | 1552.06 | 50 |
| 999 | 1529.70 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 2 |
| 3 of 4 | 2 |
| 2 of 4 | 3 |
| 1 of 4 | 1 |
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, verksamhet, kommun, friskola, förälder, pedagogisk, personal | 4/4 | 0.830 | 0.804 | 0.273 |
| 2 | elev, svensk, barn, kunskap, undervisning, grundskola, ämne, språk | 2/4 | 0.625 | 0.235 | 0.245 |
| 3 | hög, land, svensk, kvalitet, behov, högskola, lärosäte, stärka | 3/4 | 0.805 | 0.689 | 0.516 |
| 4 | elev, lärare, barn, stöd, undervisning, behov, nationell, rektor | 3/4 | 0.876 | 0.646 | 0.440 |
| 5 | elev, ung, företag, arbetsmarknad, ungdom, gymnasieskola, gymnasium, jobb | 2/4 | 0.608 | 0.368 | 0.250 |
| 6 | student, kommun, studie, studiemedel, arbeta, barnomsorg, person, studera | 2/4 | 0.527 | 0.244 | 0.210 |
| 7 | forskning, högskola, universitet, nivå, avancerad, grundnivå, forskarnivå, anslag | 4/4 | 0.926 | 0.904 | 0.571 |
| 8 | kvinna, samhälle, kunskap, ung, människa, politisk, rättighet, våld | 1/4 | 0.606 | 0.471 | 0.228 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7519
- Median: 0.8450
- Min: 0.3685
- Max: 0.9829
- Std Dev: 0.2108

**Jaccard Similarity (top 20 words):**
- Mean: 0.3301
- Median: 0.2727
- Min: 0.1111
- Max: 0.6667
- Std Dev: 0.1837

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7028
- Median: 0.8440
- Min: 0.2348
- Max: 0.9706
- Std Dev: 0.2697

**Jaccard Similarity (top 20 words):**
- Mean: 0.3470
- Median: 0.3348
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2300

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7167
- Median: 0.7554
- Min: 0.2442
- Max: 0.9063
- Std Dev: 0.1999

**Jaccard Similarity (top 20 words):**
- Mean: 0.3540
- Median: 0.3563
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.1634

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7301
- Median: 0.7457
- Min: 0.4705
- Max: 0.9480
- Std Dev: 0.1611

**Jaccard Similarity (top 20 words):**
- Mean: 0.3350
- Median: 0.4039
- Min: 0.0811
- Max: 0.5385
- Std Dev: 0.1734

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6475
- Median: 0.5912
- Min: 0.3902
- Max: 0.9484
- Std Dev: 0.1916

**Jaccard Similarity (top 20 words):**
- Mean: 0.2904
- Median: 0.1943
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.2071

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6848
- Median: 0.6970
- Min: 0.2849
- Max: 0.9397
- Std Dev: 0.2203

**Jaccard Similarity (top 20 words):**
- Mean: 0.2685
- Median: 0.2702
- Min: 0.0256
- Max: 0.5385
- Std Dev: 0.1519

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6913
- Median: 0.7685
- Min: 0.2388
- Max: 0.9524
- Std Dev: 0.2348

**Jaccard Similarity (top 20 words):**
- Mean: 0.3150
- Median: 0.3147
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1782

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7273
- Median: 0.8038
- Min: 0.3895
- Max: 0.9808
- Std Dev: 0.2012

**Jaccard Similarity (top 20 words):**
- Mean: 0.3732
- Median: 0.3563
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2442

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7330
- Median: 0.7607
- Min: 0.3099
- Max: 0.9921
- Std Dev: 0.2270

**Jaccard Similarity (top 20 words):**
- Mean: 0.4302
- Median: 0.3118
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2919

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7726
- Median: 0.8437
- Min: 0.3655
- Max: 0.9804
- Std Dev: 0.1989

**Jaccard Similarity (top 20 words):**
- Mean: 0.5043
- Median: 0.4039
- Min: 0.1429
- Max: 0.8182
- Std Dev: 0.2569

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7158
- Median: 0.7841
- Min: 0.2348
- Max: 0.9921
- Std Dev: 0.2160

### Jaccard Similarity (across all matches)
- Mean: 0.3548
- Median: 0.3333
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2224
