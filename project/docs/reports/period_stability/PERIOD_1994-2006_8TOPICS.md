# Seed-Stability Analysis: Period 1994/95–2005/06, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3440)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1612.25 | 50 |
| 123 | 1603.43 | 50 |
| 456 | 1606.26 | 50 |
| 789 | 1621.10 | 50 |
| 999 | 1591.44 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 1 |
| 2 of 4 | 0 |
| 1 of 4 | 2 |
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | student, studie, system, studerande, studera, enskild, person, högskola | 4/4 | 0.879 | 0.786 | 0.473 |
| 2 | barn, mobbning, elev, förälder, arbete, våld, problem, kommun | 4/4 | 0.806 | 0.707 | 0.265 |
| 3 | kvinna, samhälle, jämställdhet, undervisning, människa, sexuell, flicka, fråga | 1/4 | 0.418 | 0.250 | 0.184 |
| 4 | forskning, högskola, universitet, svensk, student, utveckling, kvalitet, kunskap | 4/4 | 0.921 | 0.874 | 0.605 |
| 5 | elev, gymnasieskola, kommun, fristående, program, kommunal, betyg, nationell | 3/4 | 0.801 | 0.680 | 0.373 |
| 6 | ungdom, hälsa, fysisk, idrott, barn, ämne, aktivitet, kunskap | 1/4 | 0.604 | 0.408 | 0.286 |
| 7 | högskola, universitet, forskning, utveckling, anslag, region, land, plats | 4/4 | 0.920 | 0.772 | 0.611 |
| 8 | elev, barn, lärare, förskola, förälder, kunskap, kommun, grundskola | 4/4 | 0.768 | 0.729 | 0.423 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.8058
- Median: 0.8227
- Min: 0.4079
- Max: 0.9831
- Std Dev: 0.1812

**Jaccard Similarity (top 20 words):**
- Mean: 0.4566
- Median: 0.4039
- Min: 0.1429
- Max: 0.7391
- Std Dev: 0.2026

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7302
- Median: 0.7648
- Min: 0.2499
- Max: 0.9767
- Std Dev: 0.2157

**Jaccard Similarity (top 20 words):**
- Mean: 0.3622
- Median: 0.3348
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2193

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7783
- Median: 0.7797
- Min: 0.4204
- Max: 0.9290
- Std Dev: 0.1532

**Jaccard Similarity (top 20 words):**
- Mean: 0.3938
- Median: 0.4286
- Min: 0.1429
- Max: 0.4815
- Std Dev: 0.1015

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7447
- Median: 0.7756
- Min: 0.2812
- Max: 0.9634
- Std Dev: 0.2086

**Jaccard Similarity (top 20 words):**
- Mean: 0.3980
- Median: 0.4359
- Min: 0.1111
- Max: 0.6000
- Std Dev: 0.2008

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7714
- Median: 0.8256
- Min: 0.3746
- Max: 0.9767
- Std Dev: 0.2026

**Jaccard Similarity (top 20 words):**
- Mean: 0.4659
- Median: 0.5385
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.2254

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7907
- Median: 0.7963
- Min: 0.5510
- Max: 0.9654
- Std Dev: 0.1392

**Jaccard Similarity (top 20 words):**
- Mean: 0.4913
- Median: 0.4304
- Min: 0.2121
- Max: 0.7391
- Std Dev: 0.1876

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8578
- Median: 0.8730
- Min: 0.6584
- Max: 0.9787
- Std Dev: 0.1133

**Jaccard Similarity (top 20 words):**
- Mean: 0.5210
- Median: 0.4835
- Min: 0.2500
- Max: 0.9048
- Std Dev: 0.2023

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7661
- Median: 0.8425
- Min: 0.2473
- Max: 0.9598
- Std Dev: 0.2314

**Jaccard Similarity (top 20 words):**
- Mean: 0.4402
- Median: 0.4835
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2519

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8108
- Median: 0.8687
- Min: 0.3492
- Max: 0.9885
- Std Dev: 0.1940

**Jaccard Similarity (top 20 words):**
- Mean: 0.4142
- Median: 0.3563
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2499

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7626
- Median: 0.8139
- Min: 0.3134
- Max: 0.9357
- Std Dev: 0.1997

**Jaccard Similarity (top 20 words):**
- Mean: 0.4625
- Median: 0.4835
- Min: 0.0811
- Max: 0.7391
- Std Dev: 0.1905

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7818
- Median: 0.8206
- Min: 0.2473
- Max: 0.9885
- Std Dev: 0.1905

### Jaccard Similarity (across all matches)
- Mean: 0.4406
- Median: 0.4286
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2122
