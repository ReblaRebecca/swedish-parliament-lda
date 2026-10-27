# Seed-Stability Analysis: Period 1994/95–2005/06, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3440)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1569.37 | 50 |
| 123 | 1574.55 | 50 |
| 456 | 1576.26 | 50 |
| 789 | 1579.82 | 50 |
| 999 | 1547.24 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 1 |
| 2 of 4 | 3 |
| 1 of 4 | 1 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | student, högskola, studie, system, studerande, studera, enskild, studiemedel | 4/4 | 0.901 | 0.858 | 0.514 |
| 2 | hbt, homo, homosexuell, bisexuell, skolmat, fråga, transperson, bisexualitet | 0/4 | 0.152 | 0.069 | 0.093 |
| 3 | kvinna, jämställdhet, samhälle, flicka, sexuell, kön, pojke, undervisning | 1/4 | 0.600 | 0.341 | 0.376 |
| 4 | forskning, högskola, universitet, svensk, utveckling, forskarutbildning, forskare, kvalitet | 4/4 | 0.951 | 0.914 | 0.674 |
| 5 | elev, gymnasieskola, betyg, program, nationell, grundskola, undervisning, kunskap | 4/4 | 0.891 | 0.769 | 0.447 |
| 6 | hälsa, fysisk, barn, ungdom, idrott, ämne, aktivitet, svensk | 2/4 | 0.664 | 0.334 | 0.328 |
| 7 | högskola, universitet, forskning, anslag, region, utveckling, plats, område | 4/4 | 0.907 | 0.808 | 0.498 |
| 8 | lärare, barn, elev, förskola, förälder, kunskap, lärarutbildning, pedagogisk | 2/4 | 0.758 | 0.585 | 0.504 |
| 9 | barn, kommun, fristående, kommunal, förälder, friskola, barnomsorg, funktionshind | 4/4 | 0.801 | 0.752 | 0.482 |
| 10 | företag, land, kunskap, yrkesutbildning, människa, svensk, arbete, ungdom | 2/4 | 0.695 | 0.622 | 0.254 |
| 11 | mobbning, barn, elev, arbete, problem, våld, förälder, ansvar | 3/4 | 0.869 | 0.549 | 0.504 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7077
- Median: 0.7519
- Min: 0.1776
- Max: 0.9672
- Std Dev: 0.2152

**Jaccard Similarity (top 20 words):**
- Mean: 0.4283
- Median: 0.4286
- Min: 0.1765
- Max: 0.7391
- Std Dev: 0.1804

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7376
- Median: 0.8581
- Min: 0.2415
- Max: 0.9867
- Std Dev: 0.2575

**Jaccard Similarity (top 20 words):**
- Mean: 0.4098
- Median: 0.4286
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2528

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7284
- Median: 0.7803
- Min: 0.0690
- Max: 0.9797
- Std Dev: 0.2716

**Jaccard Similarity (top 20 words):**
- Mean: 0.4027
- Median: 0.3793
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2186

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8040
- Median: 0.8972
- Min: 0.1187
- Max: 0.9863
- Std Dev: 0.2432

**Jaccard Similarity (top 20 words):**
- Mean: 0.4590
- Median: 0.5385
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2175

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7565
- Median: 0.8471
- Min: 0.2620
- Max: 0.9766
- Std Dev: 0.2332

**Jaccard Similarity (top 20 words):**
- Mean: 0.4133
- Median: 0.3793
- Min: 0.1429
- Max: 0.6667
- Std Dev: 0.1890

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7408
- Median: 0.8342
- Min: 0.2546
- Max: 0.9799
- Std Dev: 0.2319

**Jaccard Similarity (top 20 words):**
- Mean: 0.3978
- Median: 0.3793
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.2067

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8010
- Median: 0.8041
- Min: 0.5129
- Max: 0.9908
- Std Dev: 0.1685

**Jaccard Similarity (top 20 words):**
- Mean: 0.4987
- Median: 0.5385
- Min: 0.1765
- Max: 0.8182
- Std Dev: 0.2139

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7515
- Median: 0.8219
- Min: 0.3652
- Max: 0.9731
- Std Dev: 0.2197

**Jaccard Similarity (top 20 words):**
- Mean: 0.3686
- Median: 0.3333
- Min: 0.1111
- Max: 0.6667
- Std Dev: 0.2215

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7496
- Median: 0.7767
- Min: 0.1891
- Max: 0.9628
- Std Dev: 0.2212

**Jaccard Similarity (top 20 words):**
- Mean: 0.3843
- Median: 0.4286
- Min: 0.0811
- Max: 0.6000
- Std Dev: 0.1497

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7599
- Median: 0.7786
- Min: 0.3118
- Max: 0.9868
- Std Dev: 0.1886

**Jaccard Similarity (top 20 words):**
- Mean: 0.3984
- Median: 0.3793
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.1929

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7537
- Median: 0.8212
- Min: 0.0690
- Max: 0.9908
- Std Dev: 0.2287

### Jaccard Similarity (across all matches)
- Mean: 0.4161
- Median: 0.4286
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2091
