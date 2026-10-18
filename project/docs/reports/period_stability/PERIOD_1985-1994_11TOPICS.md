# Seed-Stability Analysis: Period 1985/86–1993/94, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1985/86–1993/94 (4025)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1792.80 | 50 |
| 123 | 1773.21 | 50 |
| 456 | 1790.96 | 50 |
| 789 | 1790.78 | 50 |
| 999 | 1768.15 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 2 |
| 3 of 4 | 2 |
| 2 of 4 | 3 |
| 1 of 4 | 1 |
| 0 of 4 | 3 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | stiftelse, nordisk, verksamhet, psykoterapi, stockholm, statlig, lärlingsutbildning, gymnasium | 0/4 | 0.241 | 0.178 | 0.076 |
| 2 | högskola, anslag, forskning, universitet, medel, hög, liten, resurs | 2/4 | 0.614 | 0.233 | 0.273 |
| 3 | elev, ämne, undervisning, lärare, grundskola, kunskap, gymnasieskola, barn | 4/4 | 0.941 | 0.873 | 0.625 |
| 4 | kommun, elev, verksamhet, bidrag, behov, kommunal, gymnasieskola, vuxenutbildning | 2/4 | 0.796 | 0.674 | 0.422 |
| 5 | universitet, umeå, göteborg, stockholm, plats, högskola, borås, gävle | 1/4 | 0.669 | 0.542 | 0.298 |
| 6 | kunskap, barn, hälsa, människa, ämne, många, medicinsk, vård | 2/4 | 0.714 | 0.580 | 0.329 |
| 7 | lärare, lärarutbildning, poäng, behov, linje, studerande, inriktning, krav | 4/4 | 0.802 | 0.717 | 0.459 |
| 8 | forskning, universitet, område, professur, forskare, institution, land, kvinna | 3/4 | 0.741 | 0.391 | 0.295 |
| 9 | högskola, län, utveckling, teknisk, region, hög, behov, område | 3/4 | 0.815 | 0.421 | 0.520 |
| 10 | luleå, norrbotten, syo, konsulent, fred, sih, rättighet, internationell | 0/4 | 0.056 | 0.021 | 0.033 |
| 11 | miljö, malmö, lund, ekologisk, skåne, natur, skoglig, södra | 0/4 | 0.157 | 0.056 | 0.047 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6236
- Median: 0.6936
- Min: 0.0962
- Max: 0.9585
- Std Dev: 0.2873

**Jaccard Similarity (top 20 words):**
- Mean: 0.3187
- Median: 0.3333
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.1978

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5725
- Median: 0.6336
- Min: 0.0341
- Max: 0.9734
- Std Dev: 0.3366

**Jaccard Similarity (top 20 words):**
- Mean: 0.2881
- Median: 0.2121
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2490

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5648
- Median: 0.6618
- Min: 0.0725
- Max: 0.9048
- Std Dev: 0.2771

**Jaccard Similarity (top 20 words):**
- Mean: 0.2509
- Median: 0.2903
- Min: 0.0526
- Max: 0.4815
- Std Dev: 0.1371

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6201
- Median: 0.8204
- Min: 0.0210
- Max: 0.9587
- Std Dev: 0.3599

**Jaccard Similarity (top 20 words):**
- Mean: 0.3703
- Median: 0.4815
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2454

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6100
- Median: 0.6169
- Min: 0.0744
- Max: 0.9658
- Std Dev: 0.2834

**Jaccard Similarity (top 20 words):**
- Mean: 0.2988
- Median: 0.2903
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.1923

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6298
- Median: 0.6856
- Min: 0.1015
- Max: 0.8978
- Std Dev: 0.2360

**Jaccard Similarity (top 20 words):**
- Mean: 0.3079
- Median: 0.3333
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1792

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7118
- Median: 0.8665
- Min: 0.1567
- Max: 0.9829
- Std Dev: 0.2977

**Jaccard Similarity (top 20 words):**
- Mean: 0.4507
- Median: 0.4815
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2446

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5960
- Median: 0.5281
- Min: 0.2656
- Max: 0.9544
- Std Dev: 0.2238

**Jaccard Similarity (top 20 words):**
- Mean: 0.2968
- Median: 0.2903
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.1712

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6704
- Median: 0.6178
- Min: 0.0289
- Max: 0.9677
- Std Dev: 0.2641

**Jaccard Similarity (top 20 words):**
- Mean: 0.3459
- Median: 0.2500
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2006

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6705
- Median: 0.7033
- Min: 0.1031
- Max: 0.9405
- Std Dev: 0.2352

**Jaccard Similarity (top 20 words):**
- Mean: 0.3682
- Median: 0.3333
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1852

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6270
- Median: 0.6902
- Min: 0.0210
- Max: 0.9829
- Std Dev: 0.2865

### Jaccard Similarity (across all matches)
- Mean: 0.3296
- Median: 0.2903
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2101
