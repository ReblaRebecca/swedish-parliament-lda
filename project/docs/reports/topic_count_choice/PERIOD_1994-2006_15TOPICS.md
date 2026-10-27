# Seed-Stability Analysis: Period 1994/95–2005/06, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3224)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1542.59 | 50 |
| 123 | 1512.17 | 50 |
| 456 | 1521.68 | 50 |
| 789 | 1551.70 | 50 |
| 999 | 1542.40 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 2 |
| 2 of 4 | 3 |
| 1 of 4 | 2 |
| 0 of 4 | 3 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | universitet, anslag, forskning, högskola, grundutbildning, medel, utgiftsområde, stockholm | 1/4 | 0.471 | 0.101 | 0.263 |
| 2 | lund, center, mus, historisk, universitet, samling, museum, ansvar | 0/4 | 0.091 | 0.003 | 0.027 |
| 3 | barn, mobbning, ungdom, arbete, kvinna, hälsa, ung, våld | 2/4 | 0.695 | 0.543 | 0.318 |
| 4 | elev, barn, lärare, kunskap, utveckla, förälder, stöd, samhälle | 2/4 | 0.697 | 0.424 | 0.368 |
| 5 | lärare, lärarutbildning, pedagogisk, kunskap, läsa, elev, undervisning, läraryrke | 4/4 | 0.829 | 0.730 | 0.406 |
| 6 | språk, svensk, invandrare, diskriminering, undervisning, samhälle, lag, sfi | 1/4 | 0.497 | 0.168 | 0.215 |
| 7 | student, studie, studerande, studiemedel, system, studera, ekonomisk, förslag | 4/4 | 0.970 | 0.947 | 0.741 |
| 8 | forskning, utveckling, svensk, universitet, område, land, internationell, verksamhet | 4/4 | 0.840 | 0.739 | 0.399 |
| 9 | student, högskola, yrkesutbildning, kurs, kunskap, studie, kvalificerad, person | 0/4 | 0.290 | 0.024 | 0.154 |
| 10 | barn, elev, funktionshind, särskola, specialskola, förälder, stöd, kommun | 3/4 | 0.729 | 0.344 | 0.290 |
| 11 | högskola, region, plats, land, universitet, län, utveckling, utveckla | 2/4 | 0.628 | 0.131 | 0.421 |
| 12 | högskola, forskning, student, universitet, forskarutbildning, kvalitet, kvinna, lärosäte | 4/4 | 0.894 | 0.822 | 0.401 |
| 13 | malmö, historia, undervisning, fråga, skåne, hbt, homosexuell, homo | 0/4 | 0.280 | 0.131 | 0.145 |
| 14 | elev, gymnasieskola, betyg, grundskola, nationell, program, kommun, kunskap | 4/4 | 0.895 | 0.757 | 0.452 |
| 15 | barn, förskola, kommun, fristående, verksamhet, förälder, kommunal, barnomsorg | 3/4 | 0.772 | 0.581 | 0.530 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6741
- Median: 0.8745
- Min: 0.0025
- Max: 0.9739
- Std Dev: 0.3394

**Jaccard Similarity (top 20 words):**
- Mean: 0.4174
- Median: 0.4286
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2504

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6096
- Median: 0.5809
- Min: 0.0403
- Max: 0.9875
- Std Dev: 0.2362

**Jaccard Similarity (top 20 words):**
- Mean: 0.2996
- Median: 0.2500
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.1943

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6534
- Median: 0.7303
- Min: 0.0239
- Max: 0.9722
- Std Dev: 0.2812

**Jaccard Similarity (top 20 words):**
- Mean: 0.3243
- Median: 0.3333
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1953

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6171
- Median: 0.8479
- Min: 0.0035
- Max: 0.9507
- Std Dev: 0.3515

**Jaccard Similarity (top 20 words):**
- Mean: 0.3261
- Median: 0.3333
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2235

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7427
- Median: 0.8743
- Min: 0.0311
- Max: 0.9893
- Std Dev: 0.2729

**Jaccard Similarity (top 20 words):**
- Mean: 0.4393
- Median: 0.4815
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2234

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6837
- Median: 0.8133
- Min: 0.0543
- Max: 0.9772
- Std Dev: 0.3124

**Jaccard Similarity (top 20 words):**
- Mean: 0.3473
- Median: 0.2903
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2350

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6467
- Median: 0.8036
- Min: 0.0199
- Max: 0.9866
- Std Dev: 0.3124

**Jaccard Similarity (top 20 words):**
- Mean: 0.3188
- Median: 0.2903
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2586

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7180
- Median: 0.8222
- Min: 0.0623
- Max: 0.9806
- Std Dev: 0.2594

**Jaccard Similarity (top 20 words):**
- Mean: 0.3870
- Median: 0.4286
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2025

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6923
- Median: 0.8133
- Min: 0.0261
- Max: 0.9683
- Std Dev: 0.3001

**Jaccard Similarity (top 20 words):**
- Mean: 0.3612
- Median: 0.4286
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2142

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6520
- Median: 0.7737
- Min: 0.0028
- Max: 0.9653
- Std Dev: 0.2778

**Jaccard Similarity (top 20 words):**
- Mean: 0.3090
- Median: 0.3333
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1872

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6690
- Median: 0.8075
- Min: 0.0025
- Max: 0.9893
- Std Dev: 0.2989

### Jaccard Similarity (across all matches)
- Mean: 0.3530
- Median: 0.3333
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2242
