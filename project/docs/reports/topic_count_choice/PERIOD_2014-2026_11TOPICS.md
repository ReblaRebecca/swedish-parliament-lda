# Seed-Stability Analysis: Period 2014/15–2025/26, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2014/15–2025/26 (2144)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1312.44 | 50 |
| 123 | 1327.14 | 50 |
| 456 | 1321.65 | 50 |
| 789 | 1325.23 | 50 |
| 999 | 1345.65 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 5 |
| 2 of 4 | 2 |
| 1 of 4 | 0 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, kommun, förälder, verksamhet, pedagogisk, personal, fritidshem | 4/4 | 0.901 | 0.822 | 0.390 |
| 2 | student, studie, studiemedel, studera, studerande, anslag, studiestöd, förslag | 4/4 | 0.869 | 0.767 | 0.539 |
| 3 | forskning, högskola, universitet, lärosäte, forskare, hög, student, land | 2/4 | 0.606 | 0.362 | 0.206 |
| 4 | lärare, undervisning, ämne, lärarutbildning, kunskap, grundskola, rektor, stärka | 3/4 | 0.694 | 0.176 | 0.318 |
| 5 | forskning, lärosäte, svensk, hög, kvalitet, utveckling, stärka, land | 3/4 | 0.662 | 0.108 | 0.396 |
| 6 | svensk, samhälle, kunskap, språk, undervisning, rättighet, religiös, kultur | 2/4 | 0.671 | 0.489 | 0.375 |
| 7 | lärare, stöd, förslag, behov, betyg, svensk, särskild, nationell | 3/4 | 0.702 | 0.202 | 0.354 |
| 8 | forskning, nivå, avancerad, grundnivå, högskola, forskarnivå, universitet, anslag | 4/4 | 0.985 | 0.952 | 0.869 |
| 9 | barn, ung, kvinna, psykisk, våld, arbete, kunskap, hälsa | 3/4 | 0.825 | 0.602 | 0.534 |
| 10 | arbetsmarknad, företag, behov, hög, land, jobb, ung, gymnasieskola | 3/4 | 0.775 | 0.526 | 0.346 |
| 11 | sfi, vuxenutbildning, komvux, svenska, nyanländ, språk, kvalitet, svensk | 0/4 | 0.350 | 0.091 | 0.152 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6973
- Median: 0.8027
- Min: 0.1046
- Max: 0.9945
- Std Dev: 0.2732

**Jaccard Similarity (top 20 words):**
- Mean: 0.4002
- Median: 0.2903
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2790

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7540
- Median: 0.8435
- Min: 0.0912
- Max: 0.9950
- Std Dev: 0.2676

**Jaccard Similarity (top 20 words):**
- Mean: 0.4420
- Median: 0.4286
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2516

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7699
- Median: 0.8276
- Min: 0.2016
- Max: 0.9980
- Std Dev: 0.2108

**Jaccard Similarity (top 20 words):**
- Mean: 0.4051
- Median: 0.2903
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2583

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7025
- Median: 0.8404
- Min: 0.1075
- Max: 0.9820
- Std Dev: 0.2917

**Jaccard Similarity (top 20 words):**
- Mean: 0.3811
- Median: 0.3333
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2436

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7414
- Median: 0.8012
- Min: 0.3240
- Max: 0.9926
- Std Dev: 0.2200

**Jaccard Similarity (top 20 words):**
- Mean: 0.4280
- Median: 0.3793
- Min: 0.1429
- Max: 0.9048
- Std Dev: 0.2367

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6815
- Median: 0.8055
- Min: 0.0140
- Max: 0.9938
- Std Dev: 0.2970

**Jaccard Similarity (top 20 words):**
- Mean: 0.3810
- Median: 0.4286
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2703

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6872
- Median: 0.7656
- Min: 0.2203
- Max: 0.9894
- Std Dev: 0.2475

**Jaccard Similarity (top 20 words):**
- Mean: 0.4062
- Median: 0.3793
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2545

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6993
- Median: 0.7631
- Min: 0.1033
- Max: 0.9949
- Std Dev: 0.2355

**Jaccard Similarity (top 20 words):**
- Mean: 0.3701
- Median: 0.3793
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2700

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7251
- Median: 0.8664
- Min: 0.1386
- Max: 0.9859
- Std Dev: 0.2816

**Jaccard Similarity (top 20 words):**
- Mean: 0.4639
- Median: 0.4815
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2746

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6537
- Median: 0.7696
- Min: 0.1417
- Max: 0.9581
- Std Dev: 0.2667

**Jaccard Similarity (top 20 words):**
- Mean: 0.3222
- Median: 0.3333
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2213

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7112
- Median: 0.8028
- Min: 0.0140
- Max: 0.9980
- Std Dev: 0.2629

### Jaccard Similarity (across all matches)
- Mean: 0.4000
- Median: 0.3333
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2594
