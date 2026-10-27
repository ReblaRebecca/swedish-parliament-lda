# Seed-Stability Analysis: Period 2006/07–2013/14, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2006/07–2013/14 (2026)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1182.32 | 50 |
| 123 | 1158.17 | 50 |
| 456 | 1154.61 | 50 |
| 789 | 1168.58 | 50 |
| 999 | 1149.17 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 2 |
| 2 of 4 | 1 |
| 1 of 4 | 1 |
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | student, kommun, elev, fristående, kommunal, friskola, regel, välja | 4/4 | 0.845 | 0.780 | 0.441 |
| 2 | förskola, kommun, elev, barn, verksamhet, skollag, skolverk, lärare | 2/4 | 0.672 | 0.530 | 0.412 |
| 3 | läkare, land, person, studie, vård, läkarutbildning, gammal, kunskap | 1/4 | 0.469 | 0.282 | 0.229 |
| 4 | ungdom, hälsa, fysisk, ung, barn, människa, aktivitet, mat | 3/4 | 0.773 | 0.688 | 0.469 |
| 5 | elev, lärare, kunskap, undervisning, svensk, ämne, gymnasieskola, nationell | 4/4 | 0.946 | 0.897 | 0.577 |
| 6 | forskning, högskola, universitet, svensk, lärosäte, utveckling, hög, land | 4/4 | 0.991 | 0.977 | 0.804 |
| 7 | barn, förälder, förskola, barnomsorg, kommun, behov, kvinna, arbeta | 3/4 | 0.811 | 0.535 | 0.382 |
| 8 | arbetsmarknad, högskola, vuxenutbildning, behov, hög, arbete, jobb, studie | 4/4 | 0.888 | 0.824 | 0.570 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7871
- Median: 0.8229
- Min: 0.5346
- Max: 0.9769
- Std Dev: 0.1559

**Jaccard Similarity (top 20 words):**
- Mean: 0.4664
- Median: 0.5143
- Min: 0.2121
- Max: 0.6667
- Std Dev: 0.1614

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8061
- Median: 0.9262
- Min: 0.2821
- Max: 0.9964
- Std Dev: 0.2324

**Jaccard Similarity (top 20 words):**
- Mean: 0.5068
- Median: 0.5385
- Min: 0.1111
- Max: 0.9048
- Std Dev: 0.2152

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8123
- Median: 0.8781
- Min: 0.5295
- Max: 0.9947
- Std Dev: 0.1438

**Jaccard Similarity (top 20 words):**
- Mean: 0.4777
- Median: 0.4550
- Min: 0.1765
- Max: 0.7391
- Std Dev: 0.1521

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7919
- Median: 0.8184
- Min: 0.3079
- Max: 0.9942
- Std Dev: 0.2017

**Jaccard Similarity (top 20 words):**
- Mean: 0.4908
- Median: 0.4815
- Min: 0.1111
- Max: 0.9048
- Std Dev: 0.2324

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7288
- Median: 0.8178
- Min: 0.2269
- Max: 0.9768
- Std Dev: 0.2568

**Jaccard Similarity (top 20 words):**
- Mean: 0.4240
- Median: 0.3810
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2704

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7034
- Median: 0.8257
- Min: 0.1397
- Max: 0.9815
- Std Dev: 0.2583

**Jaccard Similarity (top 20 words):**
- Mean: 0.3789
- Median: 0.3793
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2155

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8043
- Median: 0.8212
- Min: 0.6040
- Max: 0.9868
- Std Dev: 0.1728

**Jaccard Similarity (top 20 words):**
- Mean: 0.5062
- Median: 0.4897
- Min: 0.1765
- Max: 0.8182
- Std Dev: 0.2161

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8514
- Median: 0.9310
- Min: 0.3738
- Max: 0.9960
- Std Dev: 0.1904

**Jaccard Similarity (top 20 words):**
- Mean: 0.5154
- Median: 0.5741
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.2147

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7881
- Median: 0.8662
- Min: 0.3118
- Max: 0.9944
- Std Dev: 0.2350

**Jaccard Similarity (top 20 words):**
- Mean: 0.5281
- Median: 0.5143
- Min: 0.1111
- Max: 0.9048
- Std Dev: 0.2419

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7377
- Median: 0.8127
- Min: 0.2933
- Max: 0.9949
- Std Dev: 0.2327

**Jaccard Similarity (top 20 words):**
- Mean: 0.4082
- Median: 0.3810
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.2244

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7811
- Median: 0.8478
- Min: 0.1397
- Max: 0.9964
- Std Dev: 0.2158

### Jaccard Similarity (across all matches)
- Mean: 0.4702
- Median: 0.4550
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2222
