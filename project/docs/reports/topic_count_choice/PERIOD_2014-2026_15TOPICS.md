# Seed-Stability Analysis: Period 2014/15–2025/26, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2014/15–2025/26 (3222)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1425.29 | 50 |
| 123 | 1454.96 | 50 |
| 456 | 1440.55 | 50 |
| 789 | 1440.81 | 50 |
| 999 | 1412.35 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 4 |
| 2 of 4 | 2 |
| 1 of 4 | 2 |
| 0 of 4 | 3 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, förälder, ung, pedagogisk, hälsa, kommun, verksamhet | 4/4 | 0.939 | 0.874 | 0.430 |
| 2 | forskning, högskola, universitet, nivå, avancerad, grundnivå, forskarnivå, anslag | 4/4 | 0.904 | 0.886 | 0.524 |
| 3 | kommun, friskola, kommunal, fristående, skolinspektion, verksamhet, konfessionell, huvudma | 4/4 | 0.847 | 0.760 | 0.395 |
| 4 | kommun, kvinna, sfi, barnomsorg, förälder, arbeta, erbjuda, arbetstid | 0/4 | 0.196 | 0.120 | 0.054 |
| 5 | barn, stöd, lärare, våld, särskild, arbete, ung, behov | 3/4 | 0.794 | 0.684 | 0.381 |
| 6 | förutsättning, behov, resurs, skapa, utreda, hög, barn, liten | 0/4 | 0.361 | 0.207 | 0.084 |
| 7 | lärare, lärarutbildning, förskola, pedagogisk, kunskap, kvalitet, undervisning, stärka | 3/4 | 0.774 | 0.471 | 0.292 |
| 8 | forskning, land, vård, svensk, nationell, utveckling, område, läkare | 2/4 | 0.657 | 0.592 | 0.250 |
| 9 | student, lärosäte, hög, svensk, lärosäten, högskola, universitet, forskare | 1/4 | 0.640 | 0.458 | 0.311 |
| 10 | hög, arbetsmarknad, behov, land, stärka, kompetens, högskola, öka | 4/4 | 0.800 | 0.716 | 0.410 |
| 11 | körkort, djur, försvar, djurförsök, ökad, totalförsvar, öka, barn | 0/4 | 0.325 | 0.095 | 0.131 |
| 12 | lärare, svensk, ämne, betyg, nationell, grundskola, undervisning, årskurs | 1/4 | 0.500 | 0.171 | 0.304 |
| 13 | företag, ung, kunskap, ungdom, entreprenörskap, driva, egen, uf | 3/4 | 0.769 | 0.687 | 0.370 |
| 14 | svensk, samhälle, politisk, kunskap, språk, människa, utveckling, kultur | 3/4 | 0.643 | 0.289 | 0.294 |
| 15 | student, studie, studiemedel, studerande, fribelopp, studera, anslag, studiestöd | 2/4 | 0.644 | 0.037 | 0.434 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6380
- Median: 0.7159
- Min: 0.1679
- Max: 0.9291
- Std Dev: 0.2588

**Jaccard Similarity (top 20 words):**
- Mean: 0.2918
- Median: 0.3333
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1705

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6416
- Median: 0.7108
- Min: 0.0368
- Max: 0.9380
- Std Dev: 0.2728

**Jaccard Similarity (top 20 words):**
- Mean: 0.2993
- Median: 0.3333
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1796

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6306
- Median: 0.6359
- Min: 0.1199
- Max: 0.9669
- Std Dev: 0.2467

**Jaccard Similarity (top 20 words):**
- Mean: 0.2828
- Median: 0.2500
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1896

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7010
- Median: 0.7997
- Min: 0.0947
- Max: 0.9754
- Std Dev: 0.2653

**Jaccard Similarity (top 20 words):**
- Mean: 0.3697
- Median: 0.3333
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.1955

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6340
- Median: 0.6952
- Min: 0.2341
- Max: 0.9824
- Std Dev: 0.2365

**Jaccard Similarity (top 20 words):**
- Mean: 0.3057
- Median: 0.2903
- Min: 0.0256
- Max: 1.0000
- Std Dev: 0.2407

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6018
- Median: 0.5587
- Min: 0.0079
- Max: 0.9897
- Std Dev: 0.2648

**Jaccard Similarity (top 20 words):**
- Mean: 0.2780
- Median: 0.2121
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2024

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6821
- Median: 0.7654
- Min: 0.2491
- Max: 0.9945
- Std Dev: 0.2563

**Jaccard Similarity (top 20 words):**
- Mean: 0.3940
- Median: 0.3793
- Min: 0.0256
- Max: 1.0000
- Std Dev: 0.2658

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6469
- Median: 0.6461
- Min: 0.0545
- Max: 0.9738
- Std Dev: 0.2736

**Jaccard Similarity (top 20 words):**
- Mean: 0.3339
- Median: 0.2903
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2239

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6385
- Median: 0.6675
- Min: 0.1008
- Max: 0.9720
- Std Dev: 0.2859

**Jaccard Similarity (top 20 words):**
- Mean: 0.3451
- Median: 0.3333
- Min: 0.0526
- Max: 1.0000
- Std Dev: 0.2667

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6674
- Median: 0.7625
- Min: 0.0217
- Max: 0.9899
- Std Dev: 0.2915

**Jaccard Similarity (top 20 words):**
- Mean: 0.3458
- Median: 0.3333
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2255

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6482
- Median: 0.7156
- Min: 0.0079
- Max: 0.9945
- Std Dev: 0.2670

### Jaccard Similarity (across all matches)
- Mean: 0.3246
- Median: 0.2903
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2216
