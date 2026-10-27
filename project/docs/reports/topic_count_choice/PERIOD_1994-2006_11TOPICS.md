# Seed-Stability Analysis: Period 1994/95–2005/06, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3224)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1563.16 | 50 |
| 123 | 1545.42 | 50 |
| 456 | 1555.87 | 50 |
| 789 | 1566.81 | 50 |
| 999 | 1559.52 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 3 |
| 2 of 4 | 1 |
| 1 of 4 | 2 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | högskola, universitet, forskning, anslag, område, grundutbildning, satsning, utveckling | 2/4 | 0.716 | 0.611 | 0.256 |
| 2 | kvinna, sexuell, jämställdhet, diskriminering, flicka, lag, arbete, kön | 1/4 | 0.594 | 0.426 | 0.270 |
| 3 | barn, elev, mobbning, ungdom, förälder, arbete, problem, fysisk | 4/4 | 0.847 | 0.785 | 0.398 |
| 4 | elev, gymnasieskola, kunskap, lärare, betyg, ämne, grundskola, program | 4/4 | 0.931 | 0.790 | 0.664 |
| 5 | barn, förskola, lärare, lärarutbildning, kommun, förälder, barnomsorg, verksamhet | 3/4 | 0.715 | 0.388 | 0.369 |
| 6 | svensk, samhälle, språk, undervisning, människa, kunskap, invandrare, land | 0/4 | 0.360 | 0.201 | 0.167 |
| 7 | student, studie, studerande, system, förslag, studera, studiemedel, ekonomisk | 4/4 | 0.948 | 0.910 | 0.741 |
| 8 | forskning, högskola, universitet, utveckling, svensk, forskarutbildning, kvalitet, forskare | 4/4 | 0.867 | 0.767 | 0.474 |
| 9 | kommun, elev, fristående, kommunal, skolverket, friskola, verksamhet, förslag | 3/4 | 0.786 | 0.399 | 0.472 |
| 10 | student, högskola, lokal, social, universitet, styrelse, distansutbildning, studentkår | 1/4 | 0.491 | 0.084 | 0.122 |
| 11 | högskola, företag, land, yrkesutbildning, plats, kvalificerad, utveckling, region | 3/4 | 0.778 | 0.546 | 0.366 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7397
- Median: 0.7982
- Min: 0.3994
- Max: 0.9737
- Std Dev: 0.2008

**Jaccard Similarity (top 20 words):**
- Mean: 0.3978
- Median: 0.3333
- Min: 0.1429
- Max: 0.7391
- Std Dev: 0.1988

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7288
- Median: 0.8480
- Min: 0.0837
- Max: 0.9978
- Std Dev: 0.3004

**Jaccard Similarity (top 20 words):**
- Mean: 0.4159
- Median: 0.5385
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2887

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7055
- Median: 0.7851
- Min: 0.3883
- Max: 0.9104
- Std Dev: 0.1611

**Jaccard Similarity (top 20 words):**
- Mean: 0.3328
- Median: 0.3333
- Min: 0.1429
- Max: 0.6667
- Std Dev: 0.1491

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7462
- Median: 0.8251
- Min: 0.2007
- Max: 0.9868
- Std Dev: 0.2355

**Jaccard Similarity (top 20 words):**
- Mean: 0.4171
- Median: 0.3793
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2313

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7226
- Median: 0.8529
- Min: 0.1264
- Max: 0.9559
- Std Dev: 0.2619

**Jaccard Similarity (top 20 words):**
- Mean: 0.3835
- Median: 0.3793
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2303

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7352
- Median: 0.7784
- Min: 0.2551
- Max: 0.9368
- Std Dev: 0.2227

**Jaccard Similarity (top 20 words):**
- Mean: 0.4368
- Median: 0.4815
- Min: 0.1111
- Max: 0.8182
- Std Dev: 0.2089

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6996
- Median: 0.8874
- Min: 0.2934
- Max: 0.9883
- Std Dev: 0.2871

**Jaccard Similarity (top 20 words):**
- Mean: 0.4084
- Median: 0.4286
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2587

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7848
- Median: 0.8152
- Min: 0.3251
- Max: 0.9644
- Std Dev: 0.1799

**Jaccard Similarity (top 20 words):**
- Mean: 0.3973
- Median: 0.3793
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2011

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8127
- Median: 0.9175
- Min: 0.0541
- Max: 0.9915
- Std Dev: 0.2549

**Jaccard Similarity (top 20 words):**
- Mean: 0.4735
- Median: 0.5385
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2550

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7818
- Median: 0.8182
- Min: 0.4813
- Max: 0.9659
- Std Dev: 0.1348

**Jaccard Similarity (top 20 words):**
- Mean: 0.4356
- Median: 0.4286
- Min: 0.0811
- Max: 0.7391
- Std Dev: 0.1895

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7457
- Median: 0.8217
- Min: 0.0541
- Max: 0.9978
- Std Dev: 0.2324

### Jaccard Similarity (across all matches)
- Mean: 0.4099
- Median: 0.4039
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2272
