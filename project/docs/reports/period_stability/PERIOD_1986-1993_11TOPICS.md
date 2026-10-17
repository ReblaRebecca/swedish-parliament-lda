# Seed-Stability Analysis: Period 1986-1993, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of 1986-1993 (3766)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1803.92 | 50 |
| 123 | 1771.20 | 50 |
| 456 | 1799.23 | 50 |
| 789 | 1786.23 | 50 |
| 999 | 1788.08 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 0 |
| 2 of 4 | 1 |
| 1 of 4 | 1 |
| 0 of 4 | 5 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | kommun, anslag, verksamhet, gymnasieskola, bidrag, kommunal, vuxenutbildning, resurs | 4/4 | 0.922 | 0.851 | 0.672 |
| 2 | konstnärlig, språk, luleå, land, svensk, kultur, finsk, norrbotten | 0/4 | 0.286 | 0.196 | 0.121 |
| 3 | västerås, eskilstuna, superdator, västmanland, civilingenjörsutbildning, södermanland, he, nyköping | 0/4 | 0.144 | 0.025 | 0.033 |
| 4 | hälsa, kunskap, vård, behov, hemkunskap, social, landsting, sjukvård | 1/4 | 0.631 | 0.459 | 0.261 |
| 5 | idrott, stockholm, verksamhet, stiftelse, statsbidrag, statlig, fristående, hög | 0/4 | 0.375 | 0.250 | 0.127 |
| 6 | göteborg, stockholm, malmö, trädgård, behov, medicinsk, lund, stat | 0/4 | 0.547 | 0.479 | 0.214 |
| 7 | borås, barn, förskola, barnomsorg, förskollärare, plats, förskollärarutbildning, kommun | 0/4 | 0.293 | 0.182 | 0.112 |
| 8 | elev, lärare, undervisning, grundskola, barn, kunskap, ämne, gymnasieskola | 4/4 | 0.980 | 0.973 | 0.731 |
| 9 | högskola, län, linje, behov, universitet, hög, teknisk, plats | 4/4 | 0.921 | 0.858 | 0.503 |
| 10 | forskning, universitet, högskola, område, utveckling, professur, resurs, verksamhet | 4/4 | 0.893 | 0.767 | 0.584 |
| 11 | ämne, kunskap, människa, samhälle, kvinna, undervisning, svensk, fråga | 2/4 | 0.666 | 0.499 | 0.352 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6323
- Median: 0.7887
- Min: 0.0245
- Max: 0.9883
- Std Dev: 0.3321

**Jaccard Similarity (top 20 words):**
- Mean: 0.4099
- Median: 0.4286
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.3156

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6032
- Median: 0.6425
- Min: 0.0247
- Max: 0.9804
- Std Dev: 0.3195

**Jaccard Similarity (top 20 words):**
- Mean: 0.3500
- Median: 0.2903
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2499

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6162
- Median: 0.5405
- Min: 0.2504
- Max: 0.9819
- Std Dev: 0.2751

**Jaccard Similarity (top 20 words):**
- Mean: 0.3081
- Median: 0.1765
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.2272

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5689
- Median: 0.4986
- Min: 0.1969
- Max: 0.9774
- Std Dev: 0.2611

**Jaccard Similarity (top 20 words):**
- Mean: 0.2813
- Median: 0.2121
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.1983

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6804
- Median: 0.6994
- Min: 0.3065
- Max: 0.9838
- Std Dev: 0.2483

**Jaccard Similarity (top 20 words):**
- Mean: 0.3813
- Median: 0.3793
- Min: 0.0811
- Max: 0.7391
- Std Dev: 0.2351

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6209
- Median: 0.6262
- Min: 0.1201
- Max: 0.9782
- Std Dev: 0.2802

**Jaccard Similarity (top 20 words):**
- Mean: 0.3336
- Median: 0.2903
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.1941

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6784
- Median: 0.6722
- Min: 0.3391
- Max: 0.9726
- Std Dev: 0.1700

**Jaccard Similarity (top 20 words):**
- Mean: 0.3188
- Median: 0.2903
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.1501

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6153
- Median: 0.6420
- Min: 0.2175
- Max: 0.9661
- Std Dev: 0.2386

**Jaccard Similarity (top 20 words):**
- Mean: 0.2617
- Median: 0.2500
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.1896

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6232
- Median: 0.6652
- Min: 0.1774
- Max: 0.9756
- Std Dev: 0.2503

**Jaccard Similarity (top 20 words):**
- Mean: 0.2460
- Median: 0.2121
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1798

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6123
- Median: 0.5954
- Min: 0.1389
- Max: 0.9675
- Std Dev: 0.2348

**Jaccard Similarity (top 20 words):**
- Mean: 0.3032
- Median: 0.2500
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.1834

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6251
- Median: 0.6275
- Min: 0.0245
- Max: 0.9883
- Std Dev: 0.2664

### Jaccard Similarity (across all matches)
- Mean: 0.3194
- Median: 0.2500
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2223
