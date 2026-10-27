# Seed-Stability Analysis: Period 2014/15–2025/26, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2014/15–2025/26 (3222)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1469.39 | 50 |
| 123 | 1458.82 | 50 |
| 456 | 1478.46 | 50 |
| 789 | 1470.15 | 50 |
| 999 | 1478.99 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 3 |
| 2 of 4 | 3 |
| 1 of 4 | 2 |
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, ung, samhälle, våld, kvinna, arbete, psykisk, kunskap | 2/4 | 0.721 | 0.595 | 0.245 |
| 2 | forskning, högskola, hög, lärosäte, universitet, svensk, kvalitet, land | 4/4 | 0.916 | 0.857 | 0.730 |
| 3 | kommun, friskola, kommunal, skolinspektion, fristående, konfessionell, svensk, verksamhet | 2/4 | 0.701 | 0.467 | 0.350 |
| 4 | arbetsmarknad, student, behov, studie, hög, jobb, arbete, person | 2/4 | 0.762 | 0.593 | 0.468 |
| 5 | lärare, svensk, undervisning, nationell, stöd, kunskap, betyg, rektor | 3/4 | 0.829 | 0.590 | 0.498 |
| 6 | barn, förskola, förälder, språk, kommun, pedagogisk, verksamhet, svensk | 4/4 | 0.875 | 0.784 | 0.457 |
| 7 | lärare, förutsättning, likvärdig, kvalitet, resurs, behov, land, digital | 3/4 | 0.641 | 0.242 | 0.302 |
| 8 | hälsa, vård, fysisk, forskning, aktivitet, idrott, sjukvård, läkare | 1/4 | 0.616 | 0.477 | 0.336 |
| 9 | student, svensk, land, universitet, hög, kunskap, funktionsnedsättning, kostnad | 1/4 | 0.521 | 0.320 | 0.185 |
| 10 | forskning, nivå, högskola, avancerad, grundnivå, universitet, forskarnivå, anslag | 4/4 | 0.965 | 0.924 | 0.871 |
| 11 | gymnasieskola, ungdom, kunskap, ung, gymnasium, företag, ämne, program | 3/4 | 0.683 | 0.458 | 0.260 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7852
- Median: 0.8428
- Min: 0.3680
- Max: 0.9947
- Std Dev: 0.2071

**Jaccard Similarity (top 20 words):**
- Mean: 0.5089
- Median: 0.4815
- Min: 0.0811
- Max: 1.0000
- Std Dev: 0.2885

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7296
- Median: 0.7884
- Min: 0.2421
- Max: 0.9962
- Std Dev: 0.2061

**Jaccard Similarity (top 20 words):**
- Mean: 0.4489
- Median: 0.3793
- Min: 0.1111
- Max: 1.0000
- Std Dev: 0.2489

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7435
- Median: 0.8035
- Min: 0.4672
- Max: 0.9528
- Std Dev: 0.1666

**Jaccard Similarity (top 20 words):**
- Mean: 0.3706
- Median: 0.2903
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.2066

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7346
- Median: 0.7444
- Min: 0.3196
- Max: 0.9408
- Std Dev: 0.1800

**Jaccard Similarity (top 20 words):**
- Mean: 0.3815
- Median: 0.3793
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2087

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7039
- Median: 0.7130
- Min: 0.3353
- Max: 0.9926
- Std Dev: 0.1920

**Jaccard Similarity (top 20 words):**
- Mean: 0.3982
- Median: 0.2500
- Min: 0.0811
- Max: 1.0000
- Std Dev: 0.2875

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7260
- Median: 0.8367
- Min: 0.4680
- Max: 0.9453
- Std Dev: 0.1775

**Jaccard Similarity (top 20 words):**
- Mean: 0.3592
- Median: 0.3333
- Min: 0.0811
- Max: 0.7391
- Std Dev: 0.2173

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6908
- Median: 0.6996
- Min: 0.2305
- Max: 0.9343
- Std Dev: 0.2198

**Jaccard Similarity (top 20 words):**
- Mean: 0.3479
- Median: 0.3333
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2204

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6832
- Median: 0.6708
- Min: 0.0997
- Max: 0.9710
- Std Dev: 0.2607

**Jaccard Similarity (top 20 words):**
- Mean: 0.3557
- Median: 0.3333
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.2053

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6197
- Median: 0.5330
- Min: 0.3194
- Max: 0.9311
- Std Dev: 0.2165

**Jaccard Similarity (top 20 words):**
- Mean: 0.3262
- Median: 0.2500
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2329

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6637
- Median: 0.7793
- Min: 0.0996
- Max: 0.9629
- Std Dev: 0.2875

**Jaccard Similarity (top 20 words):**
- Mean: 0.3277
- Median: 0.3793
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1926

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7080
- Median: 0.7698
- Min: 0.0996
- Max: 0.9962
- Std Dev: 0.2189

### Jaccard Similarity (across all matches)
- Mean: 0.3825
- Median: 0.3333
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2393
