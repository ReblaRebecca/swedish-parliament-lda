# Seed-Stability Analysis: Period 2006/07–2013/14, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2006/07–2013/14 (2725)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1192.74 | 50 |
| 123 | 1229.81 | 50 |
| 456 | 1216.77 | 50 |
| 789 | 1250.01 | 50 |
| 999 | 1219.67 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 3 |
| 2 of 4 | 2 |
| 1 of 4 | 1 |
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | kommun, fristående, elev, kommunal, friskola, verksamhet, skolinspektion, barn | 4/4 | 0.886 | 0.768 | 0.510 |
| 2 | kunskap, ungdom, ung, undervisning, gammal, öka, ämne, människa | 2/4 | 0.653 | 0.516 | 0.312 |
| 3 | elev, lärare, nationell, undervisning, stöd, kunskap, grundskola, betyg | 3/4 | 0.785 | 0.439 | 0.347 |
| 4 | läkare, vård, land, läkarutbildning, körkort, landsting, behov, sjukvård | 2/4 | 0.676 | 0.582 | 0.445 |
| 5 | högskola, forskning, universitet, hög, utveckling, svensk, företag, land | 4/4 | 0.890 | 0.786 | 0.588 |
| 6 | språk, svensk, undervisning, kunskap, samhälle, annan, människa, kvinna | 1/4 | 0.493 | 0.283 | 0.266 |
| 7 | arbetsmarknad, gymnasieskola, vuxenutbildning, kunskap, högskola, hög, behov, program | 4/4 | 0.881 | 0.783 | 0.511 |
| 8 | förskola, barn, förälder, kommun, barnomsorg, personal, behov, fritidshem | 3/4 | 0.736 | 0.102 | 0.510 |
| 9 | student, studie, studiemedel, fribelopp, lite, ekonomisk, studera, högskola | 4/4 | 0.900 | 0.730 | 0.594 |
| 10 | barn, ungdom, elev, fysisk, ung, aktivitet, hälsa, vuxen | 4/4 | 0.858 | 0.755 | 0.336 |
| 11 | forskning, svensk, annan, myndighet, politisk, hälsa, område, forskare | 3/4 | 0.628 | 0.155 | 0.259 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7562
- Median: 0.8314
- Min: 0.2826
- Max: 0.9605
- Std Dev: 0.2002

**Jaccard Similarity (top 20 words):**
- Mean: 0.3437
- Median: 0.3793
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.1749

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7847
- Median: 0.7829
- Min: 0.3830
- Max: 0.9909
- Std Dev: 0.1788

**Jaccard Similarity (top 20 words):**
- Mean: 0.4725
- Median: 0.4815
- Min: 0.1765
- Max: 0.8182
- Std Dev: 0.2095

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7443
- Median: 0.8429
- Min: 0.1023
- Max: 0.9711
- Std Dev: 0.2408

**Jaccard Similarity (top 20 words):**
- Mean: 0.4481
- Median: 0.4815
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2003

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7643
- Median: 0.7757
- Min: 0.1548
- Max: 0.9928
- Std Dev: 0.2465

**Jaccard Similarity (top 20 words):**
- Mean: 0.4369
- Median: 0.3793
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2662

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7805
- Median: 0.8552
- Min: 0.3626
- Max: 0.9641
- Std Dev: 0.1984

**Jaccard Similarity (top 20 words):**
- Mean: 0.3817
- Median: 0.3793
- Min: 0.1429
- Max: 0.6667
- Std Dev: 0.1641

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7059
- Median: 0.8378
- Min: 0.0814
- Max: 0.9802
- Std Dev: 0.2697

**Jaccard Similarity (top 20 words):**
- Mean: 0.3411
- Median: 0.3333
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2055

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6957
- Median: 0.8366
- Min: 0.0879
- Max: 0.9702
- Std Dev: 0.2814

**Jaccard Similarity (top 20 words):**
- Mean: 0.4009
- Median: 0.4286
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.2260

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6799
- Median: 0.7353
- Min: 0.1214
- Max: 0.9515
- Std Dev: 0.2297

**Jaccard Similarity (top 20 words):**
- Mean: 0.3082
- Median: 0.3333
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1671

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7478
- Median: 0.8321
- Min: 0.1281
- Max: 0.9913
- Std Dev: 0.2485

**Jaccard Similarity (top 20 words):**
- Mean: 0.4298
- Median: 0.4815
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2267

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6272
- Median: 0.7339
- Min: 0.0658
- Max: 0.9445
- Std Dev: 0.3083

**Jaccard Similarity (top 20 words):**
- Mean: 0.3315
- Median: 0.3333
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2101

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7287
- Median: 0.8198
- Min: 0.0658
- Max: 0.9928
- Std Dev: 0.2479

### Jaccard Similarity (across all matches)
- Mean: 0.3894
- Median: 0.3793
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2140
