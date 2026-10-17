# Seed-Stability Analysis: Period 2005-2014, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of 2005-2014 (3577)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1629.37 | 50 |
| 123 | 1553.54 | 50 |
| 456 | 1581.57 | 50 |
| 789 | 1595.34 | 50 |
| 999 | 1620.31 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 2 |
| 2 of 4 | 0 |
| 1 of 4 | 1 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, student, kommun, behov, förälder, barnomsorg, arbeta | 3/4 | 0.731 | 0.658 | 0.397 |
| 2 | högskola, student, hög, kunskap, gymnasieskola, arbetsmarknad, kurs, universitet | 3/4 | 0.771 | 0.674 | 0.273 |
| 3 | musik, kultur, konfessionell, religiös, person, punktskrift, undervisning, kristen | 0/4 | 0.133 | 0.082 | 0.047 |
| 4 | forskning, högskola, universitet, utveckling, hög, svensk, lärosäte, land | 4/4 | 0.941 | 0.798 | 0.702 |
| 5 | barn, ungdom, hälsa, många, fysisk, ung, kunskap, läkare | 4/4 | 0.766 | 0.718 | 0.332 |
| 6 | svensk, land, människa, samhälle, verksamhet, företag, politisk, använda | 1/4 | 0.590 | 0.441 | 0.213 |
| 7 | elev, lärare, nationell, kunskap, ämne, betyg, mål, grundskola | 4/4 | 0.916 | 0.772 | 0.669 |
| 8 | elev, barn, kommun, fristående, undervisning, kommunal, förälder, kunskap | 4/4 | 0.835 | 0.747 | 0.418 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7040
- Median: 0.7875
- Min: 0.1346
- Max: 0.9925
- Std Dev: 0.2697

**Jaccard Similarity (top 20 words):**
- Mean: 0.4073
- Median: 0.3594
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2771

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6945
- Median: 0.7454
- Min: 0.0824
- Max: 0.9791
- Std Dev: 0.2528

**Jaccard Similarity (top 20 words):**
- Mean: 0.3299
- Median: 0.3563
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.1770

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7230
- Median: 0.7427
- Min: 0.1833
- Max: 0.9955
- Std Dev: 0.2298

**Jaccard Similarity (top 20 words):**
- Mean: 0.4105
- Median: 0.3118
- Min: 0.1111
- Max: 0.9048
- Std Dev: 0.2613

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7203
- Median: 0.7982
- Min: 0.1304
- Max: 0.9687
- Std Dev: 0.2489

**Jaccard Similarity (top 20 words):**
- Mean: 0.3777
- Median: 0.3563
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2169

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8057
- Median: 0.8643
- Min: 0.3930
- Max: 0.9797
- Std Dev: 0.1879

**Jaccard Similarity (top 20 words):**
- Mean: 0.4666
- Median: 0.5385
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.1994

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7750
- Median: 0.7699
- Min: 0.3020
- Max: 0.9934
- Std Dev: 0.2166

**Jaccard Similarity (top 20 words):**
- Mean: 0.4618
- Median: 0.3810
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2817

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8642
- Median: 0.9142
- Min: 0.5795
- Max: 0.9846
- Std Dev: 0.1275

**Jaccard Similarity (top 20 words):**
- Mean: 0.5197
- Median: 0.5100
- Min: 0.2500
- Max: 0.7391
- Std Dev: 0.1589

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7218
- Median: 0.7204
- Min: 0.4594
- Max: 0.9803
- Std Dev: 0.1697

**Jaccard Similarity (top 20 words):**
- Mean: 0.3727
- Median: 0.3118
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.2057

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7489
- Median: 0.8078
- Min: 0.4628
- Max: 0.8849
- Std Dev: 0.1313

**Jaccard Similarity (top 20 words):**
- Mean: 0.3371
- Median: 0.3563
- Min: 0.0811
- Max: 0.4286
- Std Dev: 0.1036

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7598
- Median: 0.7448
- Min: 0.5006
- Max: 0.9932
- Std Dev: 0.1551

**Jaccard Similarity (top 20 words):**
- Mean: 0.3983
- Median: 0.3563
- Min: 0.1111
- Max: 0.9048
- Std Dev: 0.2228

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7517
- Median: 0.7897
- Min: 0.0824
- Max: 0.9955
- Std Dev: 0.2108

### Jaccard Similarity (across all matches)
- Mean: 0.4082
- Median: 0.3793
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2242
