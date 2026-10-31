# Seed-Stability Analysis: Period 2014/15–2025/26, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2014/15–2025/26 (2278)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1383.30 | 50 |
| 123 | 1373.33 | 50 |
| 456 | 1394.56 | 50 |
| 789 | 1371.99 | 50 |
| 999 | 1370.89 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 0 |
| 2 of 4 | 2 |
| 1 of 4 | 0 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | lärare, svensk, undervisning, nationell, kunskap, grundskola, betyg, ämne | 4/4 | 0.920 | 0.867 | 0.498 |
| 2 | forskning, nivå, avancerad, grundnivå, högskola, forskarnivå, universitet, anslag | 4/4 | 0.989 | 0.986 | 0.800 |
| 3 | forskning, lärosäte, hög, högskola, land, universitet, svensk, kvalitet | 4/4 | 0.909 | 0.849 | 0.657 |
| 4 | anslag, studiemedel, studiestöd, förslag, skolbibliotek, studiestartsstöd, bidrag, csn | 2/4 | 0.582 | 0.150 | 0.332 |
| 5 | barn, förskola, kommun, förälder, verksamhet, stöd, behov, personal | 4/4 | 0.881 | 0.788 | 0.317 |
| 6 | arbetsmarknad, student, jobb, studie, företag, person, ung, arbete | 2/4 | 0.690 | 0.409 | 0.351 |
| 7 | barn, ung, samhälle, kunskap, svensk, kvinna, undervisning, hälsa | 4/4 | 0.828 | 0.703 | 0.411 |
| 8 | djurförsök, studium, djur, yrkesvägledning, försvar, totalförsvar, eu, metod | 0/4 | 0.176 | 0.109 | 0.019 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7374
- Median: 0.9054
- Min: 0.1499
- Max: 0.9858
- Std Dev: 0.3064

**Jaccard Similarity (top 20 words):**
- Mean: 0.4188
- Median: 0.4815
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2562

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6994
- Median: 0.7820
- Min: 0.1170
- Max: 0.9958
- Std Dev: 0.2762

**Jaccard Similarity (top 20 words):**
- Mean: 0.3789
- Median: 0.3393
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2753

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7855
- Median: 0.8748
- Min: 0.1086
- Max: 0.9856
- Std Dev: 0.2681

**Jaccard Similarity (top 20 words):**
- Mean: 0.4729
- Median: 0.4835
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2215

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7649
- Median: 0.8581
- Min: 0.2018
- Max: 0.9903
- Std Dev: 0.2441

**Jaccard Similarity (top 20 words):**
- Mean: 0.4221
- Median: 0.4039
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2239

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7613
- Median: 0.7544
- Min: 0.5054
- Max: 0.9927
- Std Dev: 0.1338

**Jaccard Similarity (top 20 words):**
- Mean: 0.3446
- Median: 0.3118
- Min: 0.1111
- Max: 0.9048
- Std Dev: 0.2337

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7993
- Median: 0.8114
- Min: 0.6522
- Max: 0.9732
- Std Dev: 0.1087

**Jaccard Similarity (top 20 words):**
- Mean: 0.4063
- Median: 0.3563
- Min: 0.1765
- Max: 0.7391
- Std Dev: 0.1770

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8168
- Median: 0.8633
- Min: 0.5263
- Max: 0.9767
- Std Dev: 0.1497

**Jaccard Similarity (top 20 words):**
- Mean: 0.4531
- Median: 0.4835
- Min: 0.2500
- Max: 0.6000
- Std Dev: 0.1282

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7308
- Median: 0.7246
- Min: 0.2943
- Max: 0.9825
- Std Dev: 0.1993

**Jaccard Similarity (top 20 words):**
- Mean: 0.3366
- Median: 0.2500
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2340

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7485
- Median: 0.8215
- Min: 0.4418
- Max: 0.9868
- Std Dev: 0.1769

**Jaccard Similarity (top 20 words):**
- Mean: 0.3951
- Median: 0.3468
- Min: 0.1765
- Max: 0.6667
- Std Dev: 0.1979

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8431
- Median: 0.8909
- Min: 0.6132
- Max: 0.9965
- Std Dev: 0.1335

**Jaccard Similarity (top 20 words):**
- Mean: 0.5291
- Median: 0.5385
- Min: 0.2500
- Max: 0.8182
- Std Dev: 0.2030

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7687
- Median: 0.8301
- Min: 0.1086
- Max: 0.9965
- Std Dev: 0.2143

### Jaccard Similarity (across all matches)
- Mean: 0.4158
- Median: 0.3793
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2256
