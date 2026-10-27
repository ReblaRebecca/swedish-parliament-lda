# Seed-Stability Analysis: Period 2006/07–2013/14, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2006/07–2013/14 (2725)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1252.44 | 50 |
| 123 | 1240.54 | 50 |
| 456 | 1247.31 | 50 |
| 789 | 1251.87 | 50 |
| 999 | 1253.08 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 2 |
| 2 of 4 | 3 |
| 1 of 4 | 0 |
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, elev, ungdom, fysisk, ung, lära, aktivitet, förälder | 3/4 | 0.767 | 0.504 | 0.360 |
| 2 | kunskap, ungdom, ämne, undervisning, ung, människa, annan, öka | 2/4 | 0.664 | 0.549 | 0.266 |
| 3 | elev, lärare, kommun, fristående, kommunal, nationell, undervisning, stöd | 4/4 | 0.928 | 0.840 | 0.572 |
| 4 | läkare, vård, behov, land, sjukvård, läkarutbildning, körkort, patient | 2/4 | 0.631 | 0.330 | 0.334 |
| 5 | forskning, högskola, universitet, utveckling, hög, svensk, land, företag | 4/4 | 0.996 | 0.995 | 0.818 |
| 6 | språk, svensk, undervisning, samhälle, annan, kunskap, land, person | 2/4 | 0.599 | 0.286 | 0.291 |
| 7 | student, studie, högskola, arbetsmarknad, hög, vuxenutbildning, studera, arbete | 4/4 | 0.919 | 0.839 | 0.561 |
| 8 | förskola, barn, kommun, förälder, barnomsorg, personal, behov, fritidshem | 3/4 | 0.851 | 0.607 | 0.663 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.8399
- Median: 0.8633
- Min: 0.5489
- Max: 0.9958
- Std Dev: 0.1349

**Jaccard Similarity (top 20 words):**
- Mean: 0.5106
- Median: 0.4550
- Min: 0.1429
- Max: 0.8182
- Std Dev: 0.2055

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7656
- Median: 0.8143
- Min: 0.2858
- Max: 0.9956
- Std Dev: 0.2218

**Jaccard Similarity (top 20 words):**
- Mean: 0.4806
- Median: 0.4286
- Min: 0.1111
- Max: 0.8182
- Std Dev: 0.2209

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7569
- Median: 0.7884
- Min: 0.4095
- Max: 0.9965
- Std Dev: 0.2031

**Jaccard Similarity (top 20 words):**
- Mean: 0.4533
- Median: 0.3594
- Min: 0.1429
- Max: 0.8182
- Std Dev: 0.2376

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8148
- Median: 0.8710
- Min: 0.3296
- Max: 0.9953
- Std Dev: 0.2101

**Jaccard Similarity (top 20 words):**
- Mean: 0.4876
- Median: 0.4304
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2596

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7986
- Median: 0.8734
- Min: 0.4151
- Max: 0.9930
- Std Dev: 0.1742

**Jaccard Similarity (top 20 words):**
- Mean: 0.4393
- Median: 0.4286
- Min: 0.1765
- Max: 0.9048
- Std Dev: 0.2151

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8130
- Median: 0.7903
- Min: 0.6509
- Max: 0.9974
- Std Dev: 0.1327

**Jaccard Similarity (top 20 words):**
- Mean: 0.4555
- Median: 0.4039
- Min: 0.2121
- Max: 0.9048
- Std Dev: 0.2107

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8649
- Median: 0.9603
- Min: 0.3512
- Max: 0.9963
- Std Dev: 0.2033

**Jaccard Similarity (top 20 words):**
- Mean: 0.6300
- Median: 0.7787
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2692

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8350
- Median: 0.9639
- Min: 0.2188
- Max: 0.9910
- Std Dev: 0.2489

**Jaccard Similarity (top 20 words):**
- Mean: 0.5422
- Median: 0.5741
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2577

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7115
- Median: 0.7515
- Min: 0.3165
- Max: 0.9940
- Std Dev: 0.1920

**Jaccard Similarity (top 20 words):**
- Mean: 0.3519
- Median: 0.3118
- Min: 0.0526
- Max: 0.9048
- Std Dev: 0.2364

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7652
- Median: 0.8406
- Min: 0.5042
- Max: 0.9934
- Std Dev: 0.1781

**Jaccard Similarity (top 20 words):**
- Mean: 0.4443
- Median: 0.3793
- Min: 0.1765
- Max: 0.8182
- Std Dev: 0.2299

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7965
- Median: 0.8524
- Min: 0.2188
- Max: 0.9974
- Std Dev: 0.1980

### Jaccard Similarity (across all matches)
- Mean: 0.4795
- Median: 0.4286
- Min: 0.0526
- Max: 0.9048
- Std Dev: 0.2452
