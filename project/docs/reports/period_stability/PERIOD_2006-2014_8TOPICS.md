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
| 42 | 1253.79 | 50 |
| 123 | 1255.98 | 50 |
| 456 | 1257.99 | 50 |
| 789 | 1241.69 | 50 |
| 999 | 1278.72 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 2 |
| 3 of 4 | 4 |
| 2 of 4 | 1 |
| 1 of 4 | 1 |
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | kunskap, undervisning, samhälle, människa, ungdom, annan, ung, svensk | 3/4 | 0.825 | 0.621 | 0.546 |
| 2 | barn, förskola, förälder, kommun, barnomsorg, behov, ungdom, personal | 4/4 | 0.923 | 0.790 | 0.528 |
| 3 | forskning, svensk, läkare, område, forskare, medel, universitet, hälsa | 1/4 | 0.512 | 0.188 | 0.232 |
| 4 | arbetsmarknad, gymnasieskola, kunskap, vuxenutbildning, behov, hög, studie, program | 3/4 | 0.786 | 0.513 | 0.514 |
| 5 | elev, lärare, kunskap, undervisning, nationell, grundskola, svensk, ämne | 3/4 | 0.863 | 0.671 | 0.454 |
| 6 | kommun, elev, fristående, kommunal, friskola, verksamhet, välja, fribelopp | 3/4 | 0.692 | 0.300 | 0.310 |
| 7 | högskola, universitet, hög, forskning, utveckling, land, företag, svensk | 4/4 | 0.913 | 0.892 | 0.569 |
| 8 | student, högskola, universitet, arbete, studie, lärosäte, verksamhet, avskaffa | 2/4 | 0.565 | 0.274 | 0.240 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.8015
- Median: 0.8587
- Min: 0.5127
- Max: 0.9961
- Std Dev: 0.1797

**Jaccard Similarity (top 20 words):**
- Mean: 0.4924
- Median: 0.5100
- Min: 0.1429
- Max: 0.9048
- Std Dev: 0.2172

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7703
- Median: 0.8783
- Min: 0.3005
- Max: 0.9658
- Std Dev: 0.2325

**Jaccard Similarity (top 20 words):**
- Mean: 0.4012
- Median: 0.3348
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2224

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7243
- Median: 0.7770
- Min: 0.2743
- Max: 0.9541
- Std Dev: 0.2217

**Jaccard Similarity (top 20 words):**
- Mean: 0.4179
- Median: 0.4144
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.2114

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7436
- Median: 0.8417
- Min: 0.1877
- Max: 0.9524
- Std Dev: 0.2310

**Jaccard Similarity (top 20 words):**
- Mean: 0.3854
- Median: 0.4039
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.1469

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6999
- Median: 0.7418
- Min: 0.4451
- Max: 0.9803
- Std Dev: 0.1747

**Jaccard Similarity (top 20 words):**
- Mean: 0.3875
- Median: 0.3810
- Min: 0.1111
- Max: 0.8182
- Std Dev: 0.2160

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7956
- Median: 0.8370
- Min: 0.5121
- Max: 0.9965
- Std Dev: 0.1662

**Jaccard Similarity (top 20 words):**
- Mean: 0.4463
- Median: 0.4589
- Min: 0.2121
- Max: 0.8182
- Std Dev: 0.1906

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7506
- Median: 0.8701
- Min: 0.2914
- Max: 0.9939
- Std Dev: 0.2458

**Jaccard Similarity (top 20 words):**
- Mean: 0.3873
- Median: 0.3793
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2267

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8128
- Median: 0.8903
- Min: 0.2012
- Max: 0.9946
- Std Dev: 0.2434

**Jaccard Similarity (top 20 words):**
- Mean: 0.5931
- Median: 0.6696
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2649

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7040
- Median: 0.7553
- Min: 0.2413
- Max: 0.9750
- Std Dev: 0.2151

**Jaccard Similarity (top 20 words):**
- Mean: 0.3758
- Median: 0.3793
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.1699

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7453
- Median: 0.8709
- Min: 0.2565
- Max: 0.9956
- Std Dev: 0.2570

**Jaccard Similarity (top 20 words):**
- Mean: 0.4160
- Median: 0.4815
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2594

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7548
- Median: 0.8330
- Min: 0.1877
- Max: 0.9965
- Std Dev: 0.2221

### Jaccard Similarity (across all matches)
- Mean: 0.4303
- Median: 0.4286
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2245
