# Seed-Stability Analysis: Period 1994/95–2005/06, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3440)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1540.50 | 50 |
| 123 | 1552.29 | 50 |
| 456 | 1537.73 | 50 |
| 789 | 1553.91 | 50 |
| 999 | 1525.69 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 4 |
| 2 of 4 | 3 |
| 1 of 4 | 0 |
| 0 of 4 | 3 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | student, högskola, studie, system, studerande, studera, enskild, studiemedel | 4/4 | 0.839 | 0.805 | 0.297 |
| 2 | hbt, homo, bisexuell, tandsköterska, bisexualitet, tandvård, fördom, kompetens | 0/4 | 0.270 | 0.012 | 0.106 |
| 3 | kvinna, sexuell, jämställdhet, flicka, samhälle, kön, diskriminering, pojke | 2/4 | 0.674 | 0.182 | 0.382 |
| 4 | forskning, högskola, universitet, forskarutbildning, forskare, svensk, utveckling, kvalitet | 4/4 | 0.942 | 0.923 | 0.689 |
| 5 | elev, fristående, kommun, betyg, nationell, grundskola, kommunal, undervisning | 4/4 | 0.824 | 0.780 | 0.347 |
| 6 | universitet, göteborg, språk, lund, västsverige, svensk, land, historia | 0/4 | 0.508 | 0.394 | 0.217 |
| 7 | högskola, universitet, forskning, anslag, plats, region, utveckling, satsning | 4/4 | 0.944 | 0.930 | 0.528 |
| 8 | lärare, elev, förskola, kunskap, barn, lärarutbildning, pedagogisk, ansvar | 2/4 | 0.681 | 0.381 | 0.311 |
| 9 | barn, funktionshind, särskola, elev, specialskola, förälder, kommun, välja | 3/4 | 0.731 | 0.217 | 0.396 |
| 10 | land, svensk, människa, kunskap, samhälle, utveckling, kommun, område | 2/4 | 0.743 | 0.647 | 0.306 |
| 11 | gymnasieskola, program, yrkesutbildning, elev, lärlingsutbildning, företag, kurs, arbetsliv | 3/4 | 0.867 | 0.634 | 0.567 |
| 12 | hälsa, fysisk, ungdom, idrott, barn, ämne, aktivitet, elev | 3/4 | 0.684 | 0.025 | 0.371 |
| 13 | mobbning, barn, elev, våld, arbete, problem, förälder, åtgärd | 4/4 | 0.973 | 0.945 | 0.689 |
| 14 | barn, förälder, barnomsorg, kommun, verksamhet, familj, omsorg, kommunal | 3/4 | 0.715 | 0.567 | 0.207 |
| 15 | csn, stat, procent, betala, studielån, lån, låne, miljard | 0/4 | 0.288 | 0.031 | 0.106 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6781
- Median: 0.8169
- Min: 0.0246
- Max: 0.9762
- Std Dev: 0.2840

**Jaccard Similarity (top 20 words):**
- Mean: 0.3348
- Median: 0.2121
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2249

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7181
- Median: 0.8427
- Min: 0.0120
- Max: 0.9903
- Std Dev: 0.2596

**Jaccard Similarity (top 20 words):**
- Mean: 0.3793
- Median: 0.3333
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2266

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6496
- Median: 0.7565
- Min: 0.0305
- Max: 0.9696
- Std Dev: 0.3195

**Jaccard Similarity (top 20 words):**
- Mean: 0.3106
- Median: 0.2500
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2249

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8029
- Median: 0.8907
- Min: 0.0351
- Max: 0.9860
- Std Dev: 0.2356

**Jaccard Similarity (top 20 words):**
- Mean: 0.4468
- Median: 0.4286
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2159

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6815
- Median: 0.7980
- Min: 0.0218
- Max: 0.9821
- Std Dev: 0.3136

**Jaccard Similarity (top 20 words):**
- Mean: 0.3720
- Median: 0.2903
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2501

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6321
- Median: 0.6303
- Min: 0.0302
- Max: 0.9628
- Std Dev: 0.3154

**Jaccard Similarity (top 20 words):**
- Mean: 0.4246
- Median: 0.3793
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2734

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7021
- Median: 0.8330
- Min: 0.0457
- Max: 0.9894
- Std Dev: 0.3038

**Jaccard Similarity (top 20 words):**
- Mean: 0.3955
- Median: 0.4286
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2227

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7058
- Median: 0.7244
- Min: 0.2508
- Max: 0.9906
- Std Dev: 0.2428

**Jaccard Similarity (top 20 words):**
- Mean: 0.4068
- Median: 0.4815
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2366

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7183
- Median: 0.8836
- Min: 0.0155
- Max: 0.9846
- Std Dev: 0.3193

**Jaccard Similarity (top 20 words):**
- Mean: 0.4249
- Median: 0.3793
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2560

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6674
- Median: 0.7352
- Min: 0.1009
- Max: 0.9868
- Std Dev: 0.3252

**Jaccard Similarity (top 20 words):**
- Mean: 0.3990
- Median: 0.3333
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2840

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6956
- Median: 0.8203
- Min: 0.0120
- Max: 0.9906
- Std Dev: 0.2971

### Jaccard Similarity (across all matches)
- Mean: 0.3894
- Median: 0.3793
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2458
