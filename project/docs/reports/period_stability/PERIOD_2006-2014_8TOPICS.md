# Seed-Stability Analysis: Period 2006/07–2013/14, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2006/07–2013/14 (2314)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1219.94 | 50 |
| 123 | 1205.94 | 50 |
| 456 | 1226.81 | 50 |
| 789 | 1225.38 | 50 |
| 999 | 1216.26 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 2 |
| 2 of 4 | 2 |
| 1 of 4 | 0 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, förälder, kommun, ungdom, behov, personal, barnomsorg | 4/4 | 0.876 | 0.778 | 0.380 |
| 2 | elev, lärare, kommun, fristående, nationell, stöd, förslag, undervisning | 3/4 | 0.832 | 0.565 | 0.425 |
| 3 | student, studie, studiemedel, ekonomisk, fribelopp, studera, lån, höja | 4/4 | 0.879 | 0.803 | 0.489 |
| 4 | lärlingsutbildning, läkare, behov, gymnasial, vård, läkarutbildning, gammal, arbetsgivare | 2/4 | 0.567 | 0.135 | 0.298 |
| 5 | forskning, högskola, universitet, svensk, utveckling, hög, företag, land | 4/4 | 0.986 | 0.982 | 0.739 |
| 6 | högskola, hög, student, vuxenutbildning, arbetsmarknad, behov, kunskap, plats | 2/4 | 0.671 | 0.306 | 0.393 |
| 7 | svensk, kunskap, undervisning, människa, samhälle, land, rättighet, kultur | 0/4 | 0.397 | 0.136 | 0.179 |
| 8 | elev, gymnasieskola, kommun, program, kunskap, språk, gymnasium, ungdom | 3/4 | 0.699 | 0.436 | 0.263 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7411
- Median: 0.7815
- Min: 0.4231
- Max: 0.9844
- Std Dev: 0.1778

**Jaccard Similarity (top 20 words):**
- Mean: 0.4201
- Median: 0.3333
- Min: 0.2500
- Max: 0.7391
- Std Dev: 0.1866

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7144
- Median: 0.7878
- Min: 0.1346
- Max: 0.9918
- Std Dev: 0.2718

**Jaccard Similarity (top 20 words):**
- Mean: 0.3973
- Median: 0.3793
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2254

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7435
- Median: 0.8896
- Min: 0.1363
- Max: 0.9878
- Std Dev: 0.2827

**Jaccard Similarity (top 20 words):**
- Mean: 0.4199
- Median: 0.4039
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2302

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7544
- Median: 0.7918
- Min: 0.3061
- Max: 0.9819
- Std Dev: 0.2060

**Jaccard Similarity (top 20 words):**
- Mean: 0.3465
- Median: 0.3348
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.1850

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7735
- Median: 0.8592
- Min: 0.3507
- Max: 0.9924
- Std Dev: 0.2259

**Jaccard Similarity (top 20 words):**
- Mean: 0.3943
- Median: 0.3468
- Min: 0.0526
- Max: 0.9048
- Std Dev: 0.2730

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8786
- Median: 0.9089
- Min: 0.6995
- Max: 0.9935
- Std Dev: 0.1075

**Jaccard Similarity (top 20 words):**
- Mean: 0.5929
- Median: 0.6000
- Min: 0.2903
- Max: 0.8182
- Std Dev: 0.1566

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8285
- Median: 0.8478
- Min: 0.4303
- Max: 0.9927
- Std Dev: 0.1627

**Jaccard Similarity (top 20 words):**
- Mean: 0.4663
- Median: 0.4039
- Min: 0.1111
- Max: 0.9048
- Std Dev: 0.2188

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7229
- Median: 0.8591
- Min: 0.2356
- Max: 0.9914
- Std Dev: 0.2626

**Jaccard Similarity (top 20 words):**
- Mean: 0.3764
- Median: 0.3594
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2327

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7336
- Median: 0.8172
- Min: 0.4796
- Max: 0.9893
- Std Dev: 0.1816

**Jaccard Similarity (top 20 words):**
- Mean: 0.3327
- Median: 0.2702
- Min: 0.1111
- Max: 0.9048
- Std Dev: 0.2319

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7723
- Median: 0.8021
- Min: 0.3492
- Max: 0.9893
- Std Dev: 0.2009

**Jaccard Similarity (top 20 words):**
- Mean: 0.3942
- Median: 0.2702
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.2394

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7663
- Median: 0.8322
- Min: 0.1346
- Max: 0.9935
- Std Dev: 0.2197

### Jaccard Similarity (across all matches)
- Mean: 0.4141
- Median: 0.3793
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2310
