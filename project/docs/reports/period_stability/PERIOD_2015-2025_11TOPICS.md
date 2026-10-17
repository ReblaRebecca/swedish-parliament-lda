# Seed-Stability Analysis: Period 2015-2025, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of 2015-2025 (3257)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1505.35 | 50 |
| 123 | 1490.47 | 50 |
| 456 | 1520.40 | 50 |
| 789 | 1508.01 | 50 |
| 999 | 1485.36 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 0 |
| 2 of 4 | 2 |
| 1 of 4 | 2 |
| 0 of 4 | 3 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | kommun, student, hög, land, studie, kommunal, många, välja | 1/4 | 0.715 | 0.632 | 0.339 |
| 2 | elev, barn, ung, stöd, ungdom, många, hälsa, psykisk | 2/4 | 0.777 | 0.673 | 0.295 |
| 3 | elev, estetisk, skolavslutning, musik, genomföra, ungdom, prao, drogtest | 0/4 | 0.311 | 0.197 | 0.060 |
| 4 | språk, kristen, svensk, djurförsök, sverige, folkmord, historia, människa | 0/4 | 0.488 | 0.333 | 0.284 |
| 5 | kvinna, våld, kunskap, samhälle, ung, arbete, person, vård | 2/4 | 0.631 | 0.414 | 0.235 |
| 6 | barn, förskola, förälder, svensk, verksamhet, kommun, pedagogisk, friskola | 4/4 | 0.913 | 0.893 | 0.442 |
| 7 | mat, försvar, god, djur, ämne, skolmat, ökad, kost | 0/4 | 0.335 | 0.292 | 0.096 |
| 8 | elev, lärare, undervisning, svensk, kunskap, rektor, grundskola, nationell | 4/4 | 0.947 | 0.923 | 0.600 |
| 9 | arbetsmarknad, behov, vuxenutbildning, kvalitet, sfi, kompetens, yrkeshögskola, kommun | 1/4 | 0.649 | 0.562 | 0.254 |
| 10 | forskning, nivå, avancerad, grundnivå, universitet, högskola, forskarnivå, anslag | 4/4 | 0.920 | 0.838 | 0.611 |
| 11 | forskning, högskola, hög, lärosäte, universitet, svensk, land, student | 4/4 | 0.866 | 0.775 | 0.556 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7071
- Median: 0.6951
- Min: 0.2922
- Max: 0.9970
- Std Dev: 0.2374

**Jaccard Similarity (top 20 words):**
- Mean: 0.4118
- Median: 0.4286
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2768

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6692
- Median: 0.7628
- Min: 0.1972
- Max: 0.9436
- Std Dev: 0.2411

**Jaccard Similarity (top 20 words):**
- Mean: 0.2824
- Median: 0.2500
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1537

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6677
- Median: 0.7753
- Min: 0.3332
- Max: 0.9435
- Std Dev: 0.2274

**Jaccard Similarity (top 20 words):**
- Mean: 0.2984
- Median: 0.3333
- Min: 0.0811
- Max: 0.6000
- Std Dev: 0.1587

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7026
- Median: 0.6953
- Min: 0.3396
- Max: 0.9870
- Std Dev: 0.2290

**Jaccard Similarity (top 20 words):**
- Mean: 0.3791
- Median: 0.3333
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2361

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6737
- Median: 0.6882
- Min: 0.2436
- Max: 0.9780
- Std Dev: 0.2234

**Jaccard Similarity (top 20 words):**
- Mean: 0.3094
- Median: 0.2903
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.1872

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7210
- Median: 0.8193
- Min: 0.2556
- Max: 0.9571
- Std Dev: 0.2150

**Jaccard Similarity (top 20 words):**
- Mean: 0.3396
- Median: 0.3333
- Min: 0.0811
- Max: 0.5385
- Std Dev: 0.1351

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7922
- Median: 0.8725
- Min: 0.4132
- Max: 0.9915
- Std Dev: 0.1865

**Jaccard Similarity (top 20 words):**
- Mean: 0.4886
- Median: 0.4286
- Min: 0.2500
- Max: 1.0000
- Std Dev: 0.2354

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7119
- Median: 0.7337
- Min: 0.3201
- Max: 0.9950
- Std Dev: 0.2500

**Jaccard Similarity (top 20 words):**
- Mean: 0.4455
- Median: 0.3333
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2832

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6882
- Median: 0.7470
- Min: 0.2941
- Max: 0.9408
- Std Dev: 0.2211

**Jaccard Similarity (top 20 words):**
- Mean: 0.3111
- Median: 0.3333
- Min: 0.0256
- Max: 0.5385
- Std Dev: 0.1614

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7112
- Median: 0.8681
- Min: 0.2301
- Max: 0.9611
- Std Dev: 0.2308

**Jaccard Similarity (top 20 words):**
- Mean: 0.3615
- Median: 0.3333
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2015

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7045
- Median: 0.7626
- Min: 0.1972
- Max: 0.9970
- Std Dev: 0.2294

### Jaccard Similarity (across all matches)
- Mean: 0.3627
- Median: 0.3333
- Min: 0.0256
- Max: 1.0000
- Std Dev: 0.2188
