# Seed-Stability Analysis: Period 1994/95–2005/06, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3062)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1567.49 | 50 |
| 123 | 1565.54 | 50 |
| 456 | 1566.65 | 50 |
| 789 | 1559.27 | 50 |
| 999 | 1561.49 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 3 |
| 2 of 4 | 1 |
| 1 of 4 | 0 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | land, svensk, kommun, ungdom, människa, språk, region, samhälle | 0/4 | 0.458 | 0.350 | 0.211 |
| 2 | elev, lärare, kunskap, undervisning, grundskola, ämne, barn, mål | 3/4 | 0.843 | 0.533 | 0.428 |
| 3 | lärare, lärarutbildning, kvinna, pedagogisk, kunskap, kompetens, yrke, läraryrke | 3/4 | 0.666 | 0.214 | 0.262 |
| 4 | kommun, fristående, elev, kommunal, skolverk, barn, friskola, verksamhet | 4/4 | 0.794 | 0.748 | 0.496 |
| 5 | högskola, forskning, universitet, utveckling, forskarutbildning, anslag, område, verksamhet | 4/4 | 0.950 | 0.849 | 0.706 |
| 6 | gymnasieskola, elev, program, yrkesutbildning, kurs, kunskap, betyg, lärlingsutbildning | 2/4 | 0.637 | 0.242 | 0.303 |
| 7 | student, högskola, studie, förslag, system, studerande, enskild, universitet | 4/4 | 0.954 | 0.910 | 0.671 |
| 8 | barn, förskola, mobbning, förälder, barnomsorg, arbete, verksamhet, samhälle | 3/4 | 0.819 | 0.696 | 0.459 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7738
- Median: 0.8804
- Min: 0.3659
- Max: 0.9914
- Std Dev: 0.2258

**Jaccard Similarity (top 20 words):**
- Mean: 0.3889
- Median: 0.3118
- Min: 0.1111
- Max: 0.8182
- Std Dev: 0.2634

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8017
- Median: 0.8782
- Min: 0.4871
- Max: 0.9861
- Std Dev: 0.1825

**Jaccard Similarity (top 20 words):**
- Mean: 0.4677
- Median: 0.4835
- Min: 0.2500
- Max: 0.7391
- Std Dev: 0.1714

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7150
- Median: 0.8310
- Min: 0.2142
- Max: 0.9676
- Std Dev: 0.2636

**Jaccard Similarity (top 20 words):**
- Mean: 0.4599
- Median: 0.5692
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.2161

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7701
- Median: 0.8355
- Min: 0.2418
- Max: 0.9814
- Std Dev: 0.2346

**Jaccard Similarity (top 20 words):**
- Mean: 0.4521
- Median: 0.4815
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.1898

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7934
- Median: 0.9124
- Min: 0.1648
- Max: 0.9831
- Std Dev: 0.2583

**Jaccard Similarity (top 20 words):**
- Mean: 0.4424
- Median: 0.4304
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2294

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7507
- Median: 0.8361
- Min: 0.1378
- Max: 0.9675
- Std Dev: 0.2532

**Jaccard Similarity (top 20 words):**
- Mean: 0.4309
- Median: 0.4304
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2263

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7838
- Median: 0.8745
- Min: 0.1377
- Max: 0.9965
- Std Dev: 0.2735

**Jaccard Similarity (top 20 words):**
- Mean: 0.5113
- Median: 0.6333
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2491

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8665
- Median: 0.8998
- Min: 0.6074
- Max: 0.9743
- Std Dev: 0.1043

**Jaccard Similarity (top 20 words):**
- Mean: 0.5149
- Median: 0.5385
- Min: 0.2903
- Max: 0.7391
- Std Dev: 0.1375

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8238
- Median: 0.9021
- Min: 0.2953
- Max: 0.9871
- Std Dev: 0.2059

**Jaccard Similarity (top 20 words):**
- Mean: 0.4628
- Median: 0.5100
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2173

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8506
- Median: 0.9257
- Min: 0.4012
- Max: 0.9916
- Std Dev: 0.1818

**Jaccard Similarity (top 20 words):**
- Mean: 0.5632
- Median: 0.5692
- Min: 0.2121
- Max: 0.9048
- Std Dev: 0.2194

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7929
- Median: 0.8925
- Min: 0.1377
- Max: 0.9965
- Std Dev: 0.2279

### Jaccard Similarity (across all matches)
- Mean: 0.4694
- Median: 0.4815
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2198
