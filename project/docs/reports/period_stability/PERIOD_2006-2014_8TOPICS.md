# Seed-Stability Analysis: Period 2006/07–2013/14, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2006/07–2013/14 (2122)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1169.57 | 50 |
| 123 | 1215.61 | 50 |
| 456 | 1199.84 | 50 |
| 789 | 1191.18 | 50 |
| 999 | 1191.59 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 1 |
| 2 of 4 | 1 |
| 1 of 4 | 1 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, förälder, kommun, barnomsorg, behov, personal, fritidshem | 4/4 | 0.942 | 0.806 | 0.714 |
| 2 | elev, lärare, undervisning, kunskap, nationell, grundskola, ämne, mål | 4/4 | 0.934 | 0.857 | 0.490 |
| 3 | land, svensk, kunskap, samhälle, människa, ungdom, person, läkare | 0/4 | 0.534 | 0.333 | 0.194 |
| 4 | ungdom, barn, fysisk, mat, elev, hälsa, kunskap, idrott | 2/4 | 0.710 | 0.583 | 0.318 |
| 5 | student, högskola, studie, hög, anslag, studiemedel, studera, förslag | 4/4 | 0.864 | 0.841 | 0.535 |
| 6 | gymnasieskola, arbetsmarknad, hög, behov, program, vuxenutbildning, ung, ungdom | 1/4 | 0.484 | 0.225 | 0.187 |
| 7 | kommun, elev, fristående, kommunal, verksamhet, friskola, enskild, kostnad | 3/4 | 0.712 | 0.331 | 0.352 |
| 8 | forskning, högskola, universitet, utveckling, svensk, lärosäte, hög, internationell | 4/4 | 0.943 | 0.922 | 0.726 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7770
- Median: 0.8637
- Min: 0.4450
- Max: 0.9910
- Std Dev: 0.1984

**Jaccard Similarity (top 20 words):**
- Mean: 0.4537
- Median: 0.4897
- Min: 0.1765
- Max: 0.8182
- Std Dev: 0.2342

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7421
- Median: 0.8231
- Min: 0.2251
- Max: 0.9697
- Std Dev: 0.2275

**Jaccard Similarity (top 20 words):**
- Mean: 0.4322
- Median: 0.4550
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2206

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7382
- Median: 0.8074
- Min: 0.3309
- Max: 0.9907
- Std Dev: 0.2331

**Jaccard Similarity (top 20 words):**
- Mean: 0.3678
- Median: 0.3793
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.2225

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8037
- Median: 0.8732
- Min: 0.3333
- Max: 0.9790
- Std Dev: 0.1916

**Jaccard Similarity (top 20 words):**
- Mean: 0.5040
- Median: 0.4589
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2438

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6748
- Median: 0.7495
- Min: 0.3301
- Max: 0.9345
- Std Dev: 0.1958

**Jaccard Similarity (top 20 words):**
- Mean: 0.3224
- Median: 0.3563
- Min: 0.0811
- Max: 0.4815
- Std Dev: 0.1149

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7217
- Median: 0.8989
- Min: 0.1308
- Max: 0.9886
- Std Dev: 0.2944

**Jaccard Similarity (top 20 words):**
- Mean: 0.4072
- Median: 0.4835
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2240

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7356
- Median: 0.7936
- Min: 0.3511
- Max: 0.9810
- Std Dev: 0.2141

**Jaccard Similarity (top 20 words):**
- Mean: 0.3864
- Median: 0.4550
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.2167

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7322
- Median: 0.8248
- Min: 0.1662
- Max: 0.9006
- Std Dev: 0.2315

**Jaccard Similarity (top 20 words):**
- Mean: 0.4048
- Median: 0.4286
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.1816

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7691
- Median: 0.8810
- Min: 0.2139
- Max: 0.9818
- Std Dev: 0.2509

**Jaccard Similarity (top 20 words):**
- Mean: 0.4388
- Median: 0.4589
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2599

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7762
- Median: 0.8898
- Min: 0.1537
- Max: 0.9840
- Std Dev: 0.2729

**Jaccard Similarity (top 20 words):**
- Mean: 0.4819
- Median: 0.5385
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2430

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7471
- Median: 0.8469
- Min: 0.1308
- Max: 0.9910
- Std Dev: 0.2358

### Jaccard Similarity (across all matches)
- Mean: 0.4199
- Median: 0.4286
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2255
