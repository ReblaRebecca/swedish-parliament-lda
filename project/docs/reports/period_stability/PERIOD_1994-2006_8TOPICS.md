# Seed-Stability Analysis: Period 1994/95–2005/06, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3224)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1587.40 | 50 |
| 123 | 1598.39 | 50 |
| 456 | 1586.59 | 50 |
| 789 | 1579.60 | 50 |
| 999 | 1597.90 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 1 |
| 2 of 4 | 1 |
| 1 of 4 | 0 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | högskola, universitet, forskning, utveckling, land, region, område, företag | 4/4 | 0.895 | 0.811 | 0.443 |
| 2 | lärare, lärarutbildning, kvinna, pedagogisk, jämställdhet, undervisning, läraryrke, fortbildning | 0/4 | 0.278 | 0.094 | 0.147 |
| 3 | barn, hälsa, ungdom, fysisk, idrott, ämne, aktivitet, kunskap | 2/4 | 0.665 | 0.279 | 0.365 |
| 4 | elev, gymnasieskola, kunskap, betyg, lärare, program, grundskola, ämne | 3/4 | 0.898 | 0.690 | 0.564 |
| 5 | barn, kommun, förskola, elev, förälder, fristående, kommunal, verksamhet | 4/4 | 0.974 | 0.915 | 0.750 |
| 6 | elev, mobbning, barn, arbete, samhälle, lärare, ansvar, människa | 4/4 | 0.948 | 0.902 | 0.706 |
| 7 | student, studie, högskola, förslag, studerande, system, studera, enskild | 4/4 | 0.962 | 0.923 | 0.785 |
| 8 | forskning, högskola, universitet, forskarutbildning, svensk, utveckling, kvalitet, anslag | 4/4 | 0.939 | 0.907 | 0.612 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.8145
- Median: 0.9152
- Min: 0.4097
- Max: 0.9973
- Std Dev: 0.2080

**Jaccard Similarity (top 20 words):**
- Mean: 0.5206
- Median: 0.5839
- Min: 0.1111
- Max: 0.9048
- Std Dev: 0.2954

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8586
- Median: 0.9608
- Min: 0.1456
- Max: 0.9902
- Std Dev: 0.2703

**Jaccard Similarity (top 20 words):**
- Mean: 0.6424
- Median: 0.7029
- Min: 0.1111
- Max: 0.9048
- Std Dev: 0.2373

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7648
- Median: 0.8976
- Min: 0.2791
- Max: 0.9966
- Std Dev: 0.2470

**Jaccard Similarity (top 20 words):**
- Mean: 0.4898
- Median: 0.5692
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2608

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8416
- Median: 0.9553
- Min: 0.0941
- Max: 0.9706
- Std Dev: 0.2834

**Jaccard Similarity (top 20 words):**
- Mean: 0.5329
- Median: 0.6000
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.1871

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8289
- Median: 0.9263
- Min: 0.2104
- Max: 0.9936
- Std Dev: 0.2460

**Jaccard Similarity (top 20 words):**
- Mean: 0.5256
- Median: 0.6026
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2776

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8136
- Median: 0.8893
- Min: 0.4393
- Max: 0.9969
- Std Dev: 0.1780

**Jaccard Similarity (top 20 words):**
- Mean: 0.5222
- Median: 0.5143
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2615

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7702
- Median: 0.8705
- Min: 0.3736
- Max: 0.9965
- Std Dev: 0.2186

**Jaccard Similarity (top 20 words):**
- Mean: 0.3958
- Median: 0.3859
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2465

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8234
- Median: 0.9253
- Min: 0.2141
- Max: 0.9905
- Std Dev: 0.2434

**Jaccard Similarity (top 20 words):**
- Mean: 0.5594
- Median: 0.6388
- Min: 0.0526
- Max: 0.9048
- Std Dev: 0.2602

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8816
- Median: 0.9714
- Min: 0.2896
- Max: 0.9958
- Std Dev: 0.2253

**Jaccard Similarity (top 20 words):**
- Mean: 0.6275
- Median: 0.6667
- Min: 0.1429
- Max: 0.9048
- Std Dev: 0.2196

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7572
- Median: 0.9137
- Min: 0.1988
- Max: 0.9696
- Std Dev: 0.2902

**Jaccard Similarity (top 20 words):**
- Mean: 0.4567
- Median: 0.4815
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2437

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.8154
- Median: 0.9235
- Min: 0.0941
- Max: 0.9973
- Std Dev: 0.2464

### Jaccard Similarity (across all matches)
- Mean: 0.5273
- Median: 0.6000
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2600
