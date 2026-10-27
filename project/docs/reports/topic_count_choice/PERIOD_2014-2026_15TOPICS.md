# Seed-Stability Analysis: Period 2014/15–2025/26, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2014/15–2025/26 (2144)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1317.08 | 50 |
| 123 | 1301.44 | 50 |
| 456 | 1286.62 | 50 |
| 789 | 1320.51 | 50 |
| 999 | 1330.32 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 1 |
| 2 of 4 | 2 |
| 1 of 4 | 3 |
| 0 of 4 | 4 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, kommun, verksamhet, förälder, pedagogisk, personal, fritidshem | 2/4 | 0.755 | 0.562 | 0.470 |
| 2 | student, studiemedel, studie, anslag, studerande, studera, studiestöd, funktionsnedsättning | 4/4 | 0.888 | 0.762 | 0.605 |
| 3 | djurförsök, djur, alternativ, flykting, ukrainsk, väst, djurfri, levande | 1/4 | 0.548 | 0.381 | 0.210 |
| 4 | ämne, aktivitet, grundskola, fysisk, barn, timme, idrott, hälsa | 0/4 | 0.306 | 0.054 | 0.113 |
| 5 | kunskap, ung, utveckling, samhälle, barn, psykisk, hälsa, stärka | 0/4 | 0.533 | 0.407 | 0.163 |
| 6 | svensk, religiös, rättighet, politisk, samhälle, demokratisk, demokrati, konfessionell | 1/4 | 0.502 | 0.029 | 0.303 |
| 7 | lärare, stöd, undervisning, svensk, nationell, skolinspektion, behov, förslag | 4/4 | 0.836 | 0.771 | 0.364 |
| 8 | gymnasieskola, gymnasium, ämne, program, betyg, ungdom, ung, läsa | 0/4 | 0.341 | 0.048 | 0.148 |
| 9 | kvinna, våld, flicka, arbete, utsatt, sexuell, barn, jämställdhet | 3/4 | 0.593 | 0.012 | 0.299 |
| 10 | forskning, högskola, lärosäte, hög, land, svensk, universitet, forskare | 4/4 | 0.894 | 0.773 | 0.579 |
| 11 | sfi, undervisning, ung, svenska, kunskap, privatekonomi, nyanländ, lära | 0/4 | 0.306 | 0.057 | 0.179 |
| 12 | barn, förälder, trygghet, rektor, brott, mobbning, trygg, hot | 1/4 | 0.691 | 0.647 | 0.245 |
| 13 | lärosäte, forskning, student, kvalitet, universitet, hög, högskola, svensk | 2/4 | 0.484 | 0.038 | 0.188 |
| 14 | forskning, nivå, avancerad, grundnivå, högskola, forskarnivå, universitet, anslag | 4/4 | 0.996 | 0.994 | 0.883 |
| 15 | arbetsmarknad, behov, hög, stärka, lärare, kvalitet, jobb, vuxenutbildning | 4/4 | 0.812 | 0.734 | 0.407 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6303
- Median: 0.7137
- Min: 0.0291
- Max: 0.9944
- Std Dev: 0.2690

**Jaccard Similarity (top 20 words):**
- Mean: 0.3669
- Median: 0.3333
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2496

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6386
- Median: 0.7714
- Min: 0.0480
- Max: 0.9972
- Std Dev: 0.2784

**Jaccard Similarity (top 20 words):**
- Mean: 0.3363
- Median: 0.3333
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2650

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6173
- Median: 0.6974
- Min: 0.0123
- Max: 0.9962
- Std Dev: 0.3372

**Jaccard Similarity (top 20 words):**
- Mean: 0.3461
- Median: 0.2500
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2496

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6433
- Median: 0.6761
- Min: 0.0379
- Max: 0.9968
- Std Dev: 0.2440

**Jaccard Similarity (top 20 words):**
- Mean: 0.3260
- Median: 0.2903
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2224

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7049
- Median: 0.8270
- Min: 0.0111
- Max: 0.9959
- Std Dev: 0.2976

**Jaccard Similarity (top 20 words):**
- Mean: 0.4312
- Median: 0.4286
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2707

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6126
- Median: 0.6528
- Min: 0.0134
- Max: 0.9971
- Std Dev: 0.2847

**Jaccard Similarity (top 20 words):**
- Mean: 0.3343
- Median: 0.2903
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2591

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6603
- Median: 0.7561
- Min: 0.0085
- Max: 0.9942
- Std Dev: 0.2906

**Jaccard Similarity (top 20 words):**
- Mean: 0.3775
- Median: 0.3333
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2906

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6464
- Median: 0.7522
- Min: 0.0227
- Max: 0.9966
- Std Dev: 0.3210

**Jaccard Similarity (top 20 words):**
- Mean: 0.3146
- Median: 0.2903
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2523

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6351
- Median: 0.7458
- Min: 0.0060
- Max: 0.9957
- Std Dev: 0.3007

**Jaccard Similarity (top 20 words):**
- Mean: 0.3411
- Median: 0.2500
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2618

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5843
- Median: 0.7407
- Min: 0.0045
- Max: 0.9948
- Std Dev: 0.3339

**Jaccard Similarity (top 20 words):**
- Mean: 0.3414
- Median: 0.2903
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2763

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6373
- Median: 0.7204
- Min: 0.0045
- Max: 0.9972
- Std Dev: 0.2985

### Jaccard Similarity (across all matches)
- Mean: 0.3516
- Median: 0.3118
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2623
