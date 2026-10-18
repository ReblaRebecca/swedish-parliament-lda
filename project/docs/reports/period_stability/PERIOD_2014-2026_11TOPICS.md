# Seed-Stability Analysis: Period 2014/15–2025/26, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2014/15–2025/26 (3572)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1504.02 | 50 |
| 123 | 1514.93 | 50 |
| 456 | 1530.86 | 50 |
| 789 | 1519.37 | 50 |
| 999 | 1514.59 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 2 |
| 2 of 4 | 2 |
| 1 of 4 | 1 |
| 0 of 4 | 2 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, verksamhet, pedagogisk, fritidshem, personal, förälder, omsorg | 4/4 | 0.878 | 0.780 | 0.385 |
| 2 | svensk, elev, samhälle, kunskap, barn, politisk, människa, ung | 2/4 | 0.591 | 0.244 | 0.256 |
| 3 | elev, lärare, kommun, svensk, kvalitet, förutsättning, stärka, behov | 4/4 | 0.877 | 0.747 | 0.472 |
| 4 | elev, barn, lärare, stöd, kunskap, nationell, betyg, undervisning | 4/4 | 0.878 | 0.775 | 0.509 |
| 5 | elev, företag, arbetsmarknad, ung, gymnasieskola, ungdom, gymnasium, kunskap | 3/4 | 0.757 | 0.672 | 0.375 |
| 6 | student, studie, person, studiemedel, arbetsmarknad, studera, arbeta, arbete | 3/4 | 0.796 | 0.588 | 0.406 |
| 7 | forskning, högskola, nivå, universitet, avancerad, grundnivå, forskarnivå, anslag | 4/4 | 0.942 | 0.864 | 0.690 |
| 8 | friskola, konfessionell, religiös, läkare, svensk, kristen, undervisning, kyrka | 1/4 | 0.438 | 0.223 | 0.164 |
| 9 | forskning, högskola, hög, lärosäte, universitet, student, land, svensk | 2/4 | 0.732 | 0.466 | 0.448 |
| 10 | språk, nationell, samisk, svensk, försvar, land, djurförsök, kultur | 0/4 | 0.513 | 0.311 | 0.234 |
| 11 | barn, förälder, kommun, barnomsorg, hälsa, fysisk, aktivitet, idrott | 0/4 | 0.354 | 0.060 | 0.174 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7186
- Median: 0.8437
- Min: 0.2442
- Max: 0.9450
- Std Dev: 0.2216

**Jaccard Similarity (top 20 words):**
- Mean: 0.3400
- Median: 0.3333
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.1574

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7026
- Median: 0.8114
- Min: 0.2287
- Max: 0.9740
- Std Dev: 0.2556

**Jaccard Similarity (top 20 words):**
- Mean: 0.3722
- Median: 0.3793
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2200

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6679
- Median: 0.7473
- Min: 0.0605
- Max: 0.9725
- Std Dev: 0.2636

**Jaccard Similarity (top 20 words):**
- Mean: 0.3780
- Median: 0.3793
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2479

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7315
- Median: 0.8426
- Min: 0.0941
- Max: 0.9856
- Std Dev: 0.2618

**Jaccard Similarity (top 20 words):**
- Mean: 0.4058
- Median: 0.3793
- Min: 0.0256
- Max: 1.0000
- Std Dev: 0.2709

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7363
- Median: 0.7424
- Min: 0.3381
- Max: 0.9707
- Std Dev: 0.1946

**Jaccard Similarity (top 20 words):**
- Mean: 0.3867
- Median: 0.3333
- Min: 0.1429
- Max: 0.7391
- Std Dev: 0.2072

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6026
- Median: 0.7488
- Min: 0.1027
- Max: 0.8850
- Std Dev: 0.2563

**Jaccard Similarity (top 20 words):**
- Mean: 0.2401
- Median: 0.2121
- Min: 0.0000
- Max: 0.4286
- Std Dev: 0.1307

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6606
- Median: 0.5941
- Min: 0.4124
- Max: 0.9146
- Std Dev: 0.1655

**Jaccard Similarity (top 20 words):**
- Mean: 0.3235
- Median: 0.3333
- Min: 0.2121
- Max: 0.4815
- Std Dev: 0.0900

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6035
- Median: 0.7229
- Min: 0.0435
- Max: 0.8987
- Std Dev: 0.2913

**Jaccard Similarity (top 20 words):**
- Mean: 0.2619
- Median: 0.2500
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1713

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5807
- Median: 0.6437
- Min: 0.0861
- Max: 0.8980
- Std Dev: 0.2656

**Jaccard Similarity (top 20 words):**
- Mean: 0.2653
- Median: 0.2500
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.1576

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6476
- Median: 0.7740
- Min: 0.1584
- Max: 0.9943
- Std Dev: 0.2813

**Jaccard Similarity (top 20 words):**
- Mean: 0.3602
- Median: 0.3333
- Min: 0.0256
- Max: 1.0000
- Std Dev: 0.2577

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6652
- Median: 0.7448
- Min: 0.0435
- Max: 0.9943
- Std Dev: 0.2543

### Jaccard Similarity (across all matches)
- Mean: 0.3334
- Median: 0.3333
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2068
