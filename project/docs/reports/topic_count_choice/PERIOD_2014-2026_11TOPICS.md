# Seed-Stability Analysis: Period 2014/15–2025/26, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2014/15–2025/26 (2477)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1370.20 | 50 |
| 123 | 1380.16 | 50 |
| 456 | 1394.61 | 50 |
| 789 | 1386.49 | 50 |
| 999 | 1422.61 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 2 |
| 3 of 4 | 5 |
| 2 of 4 | 1 |
| 1 of 4 | 3 |
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | svensk, kunskap, språk, undervisning, samhälle, lära, ämne, läroplan | 1/4 | 0.452 | 0.252 | 0.188 |
| 2 | barn, ung, hälsa, psykisk, funktionsnedsättning, fysisk, ohälsa, elevhälsa | 1/4 | 0.388 | 0.025 | 0.198 |
| 3 | forskning, hög, högskola, lärosäte, svensk, forskare, utveckling, land | 3/4 | 0.861 | 0.558 | 0.564 |
| 4 | förslag, lärare, stöd, kommun, behov, svensk, nationell, resurs | 3/4 | 0.814 | 0.688 | 0.353 |
| 5 | barn, kvinna, våld, ung, arbete, rättighet, utsatt, samhälle | 3/4 | 0.782 | 0.537 | 0.326 |
| 6 | studiemedel, studie, anslag, student, studiestöd, studerande, förslag, studera | 3/4 | 0.845 | 0.662 | 0.575 |
| 7 | förskola, barn, kommun, verksamhet, friskola, förälder, pedagogisk, personal | 4/4 | 0.864 | 0.844 | 0.260 |
| 8 | arbetsmarknad, hög, behov, land, jobb, gymnasieskola, stärka, kompetens | 2/4 | 0.739 | 0.457 | 0.358 |
| 9 | forskning, nivå, avancerad, högskola, grundnivå, forskarnivå, universitet, anslag | 4/4 | 0.960 | 0.856 | 0.833 |
| 10 | student, högskola, universitet, lärosäte, hög, lärosäten, land, kvalitet | 1/4 | 0.469 | 0.028 | 0.239 |
| 11 | lärare, barn, förskola, stöd, behov, rektor, undervisning, förälder | 3/4 | 0.757 | 0.622 | 0.360 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7248
- Median: 0.8403
- Min: 0.0280
- Max: 0.9954
- Std Dev: 0.2856

**Jaccard Similarity (top 20 words):**
- Mean: 0.4296
- Median: 0.4286
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2722

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6918
- Median: 0.6876
- Min: 0.3058
- Max: 0.9970
- Std Dev: 0.1952

**Jaccard Similarity (top 20 words):**
- Mean: 0.3193
- Median: 0.2903
- Min: 0.0811
- Max: 1.0000
- Std Dev: 0.2478

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7471
- Median: 0.8934
- Min: 0.2517
- Max: 0.9907
- Std Dev: 0.2528

**Jaccard Similarity (top 20 words):**
- Mean: 0.4252
- Median: 0.3793
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2518

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7196
- Median: 0.8044
- Min: 0.0253
- Max: 0.9784
- Std Dev: 0.2579

**Jaccard Similarity (top 20 words):**
- Mean: 0.3736
- Median: 0.3333
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2138

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7526
- Median: 0.9018
- Min: 0.1220
- Max: 0.9961
- Std Dev: 0.2707

**Jaccard Similarity (top 20 words):**
- Mean: 0.4447
- Median: 0.4286
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2999

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8108
- Median: 0.9110
- Min: 0.1403
- Max: 0.9932
- Std Dev: 0.2627

**Jaccard Similarity (top 20 words):**
- Mean: 0.5883
- Median: 0.6667
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2847

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7041
- Median: 0.7855
- Min: 0.2552
- Max: 0.9213
- Std Dev: 0.2071

**Jaccard Similarity (top 20 words):**
- Mean: 0.3740
- Median: 0.3793
- Min: 0.1429
- Max: 0.5385
- Std Dev: 0.1258

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7428
- Median: 0.7144
- Min: 0.4074
- Max: 0.9916
- Std Dev: 0.1814

**Jaccard Similarity (top 20 words):**
- Mean: 0.4408
- Median: 0.3333
- Min: 0.1111
- Max: 0.9048
- Std Dev: 0.2588

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6403
- Median: 0.7427
- Min: 0.1390
- Max: 0.9332
- Std Dev: 0.2399

**Jaccard Similarity (top 20 words):**
- Mean: 0.3005
- Median: 0.3333
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.1664

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6881
- Median: 0.8460
- Min: 0.1350
- Max: 0.9057
- Std Dev: 0.2696

**Jaccard Similarity (top 20 words):**
- Mean: 0.3695
- Median: 0.4286
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1980

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7222
- Median: 0.8230
- Min: 0.0253
- Max: 0.9970
- Std Dev: 0.2485

### Jaccard Similarity (across all matches)
- Mean: 0.4066
- Median: 0.3793
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2499
