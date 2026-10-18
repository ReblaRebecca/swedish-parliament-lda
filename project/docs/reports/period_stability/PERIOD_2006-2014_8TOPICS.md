# Seed-Stability Analysis: Period 2006/07–2013/14, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2006/07–2013/14 (2879)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1571.43 | 50 |
| 123 | 1569.21 | 50 |
| 456 | 1587.98 | 50 |
| 789 | 1600.46 | 50 |
| 999 | 1571.56 | 50 |

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
| 1 | barn, ungdom, fysisk, många, elev, ung, aktivitet, hälsa | 3/4 | 0.687 | 0.202 | 0.377 |
| 2 | elev, lärare, kunskap, undervisning, gymnasieskola, ämne, nationell, grundskola | 4/4 | 0.941 | 0.885 | 0.640 |
| 3 | kommun, barn, förskola, elev, förälder, kommunal, fristående, verksamhet | 4/4 | 0.886 | 0.710 | 0.538 |
| 4 | lärare, elev, kvinna, kunskap, arbete, verksamhet, flicka, rättighet | 3/4 | 0.740 | 0.575 | 0.309 |
| 5 | forskning, högskola, universitet, utveckling, svensk, hög, företag, land | 3/4 | 0.892 | 0.638 | 0.679 |
| 6 | student, högskola, arbetsmarknad, hög, studie, arbete, vuxenutbildning, studera | 4/4 | 0.908 | 0.836 | 0.542 |
| 7 | språk, läkare, land, svensk, behov, vård, gammal, läkarutbildning | 2/4 | 0.739 | 0.682 | 0.468 |
| 8 | högskola, forskning, universitet, lärosäte, forskarutbildning, kvalitet, medel, anslag | 2/4 | 0.693 | 0.488 | 0.234 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7909
- Median: 0.7958
- Min: 0.6381
- Max: 0.8871
- Std Dev: 0.0795

**Jaccard Similarity (top 20 words):**
- Mean: 0.3848
- Median: 0.4039
- Min: 0.2121
- Max: 0.4815
- Std Dev: 0.0849

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8246
- Median: 0.8791
- Min: 0.4876
- Max: 0.9700
- Std Dev: 0.1566

**Jaccard Similarity (top 20 words):**
- Mean: 0.5260
- Median: 0.5692
- Min: 0.1765
- Max: 0.7391
- Std Dev: 0.1814

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7670
- Median: 0.8690
- Min: 0.2021
- Max: 0.9682
- Std Dev: 0.2443

**Jaccard Similarity (top 20 words):**
- Mean: 0.4614
- Median: 0.4550
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.2141

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8612
- Median: 0.8804
- Min: 0.5754
- Max: 0.9924
- Std Dev: 0.1281

**Jaccard Similarity (top 20 words):**
- Mean: 0.5211
- Median: 0.5100
- Min: 0.1429
- Max: 0.9048
- Std Dev: 0.2207

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7410
- Median: 0.7873
- Min: 0.2298
- Max: 0.9724
- Std Dev: 0.2124

**Jaccard Similarity (top 20 words):**
- Mean: 0.4162
- Median: 0.4550
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.1775

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7642
- Median: 0.9046
- Min: 0.2132
- Max: 0.9732
- Std Dev: 0.2630

**Jaccard Similarity (top 20 words):**
- Mean: 0.4641
- Median: 0.5385
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.2267

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7526
- Median: 0.7494
- Min: 0.5515
- Max: 0.9522
- Std Dev: 0.1408

**Jaccard Similarity (top 20 words):**
- Mean: 0.3994
- Median: 0.3563
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.2342

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8279
- Median: 0.8799
- Min: 0.3562
- Max: 0.9883
- Std Dev: 0.1939

**Jaccard Similarity (top 20 words):**
- Mean: 0.5385
- Median: 0.5385
- Min: 0.1111
- Max: 0.8182
- Std Dev: 0.1973

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8513
- Median: 0.8760
- Min: 0.6556
- Max: 0.9793
- Std Dev: 0.1118

**Jaccard Similarity (top 20 words):**
- Mean: 0.5315
- Median: 0.6026
- Min: 0.2121
- Max: 0.7391
- Std Dev: 0.1767

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7905
- Median: 0.8794
- Min: 0.2978
- Max: 0.9768
- Std Dev: 0.2211

**Jaccard Similarity (top 20 words):**
- Mean: 0.5184
- Median: 0.5100
- Min: 0.1111
- Max: 0.8182
- Std Dev: 0.2495

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7971
- Median: 0.8371
- Min: 0.2021
- Max: 0.9924
- Std Dev: 0.1887

### Jaccard Similarity (across all matches)
- Mean: 0.4761
- Median: 0.4815
- Min: 0.0526
- Max: 0.9048
- Std Dev: 0.2089
