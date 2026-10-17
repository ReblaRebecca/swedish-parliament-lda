# Seed-Stability Analysis: Period 1986-1993, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of 1986-1993 (3766)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1787.89 | 50 |
| 123 | 1774.17 | 50 |
| 456 | 1774.11 | 50 |
| 789 | 1762.50 | 50 |
| 999 | 1783.83 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 2 |
| 2 of 4 | 2 |
| 1 of 4 | 2 |
| 0 of 4 | 6 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | kommun, gymnasieskola, verksamhet, anslag, vuxenutbildning, bidrag, kommunal, folkhögskola | 4/4 | 0.831 | 0.790 | 0.505 |
| 2 | styrelse, marin, arbetsmiljö, elevskyddsombud, djur, rekommendation, östersjön, hav | 0/4 | 0.067 | 0.017 | 0.026 |
| 3 | västerås, eskilstuna, västmanland, institutet, södermanland, he, nyköping, skinnskatteberg | 0/4 | 0.087 | 0.001 | 0.027 |
| 4 | hälsa, kunskap, hemkunskap, flicka, behov, vård, ämne, många | 2/4 | 0.660 | 0.440 | 0.268 |
| 5 | kommun, invandrare, svensk, statsbidrag, stockholm, undervisning, kostnad, sfi | 1/4 | 0.535 | 0.317 | 0.267 |
| 6 | göteborg, örebro, trädgård, social, stat, stockholm, döv, handikapp | 2/4 | 0.554 | 0.247 | 0.228 |
| 7 | syo, konsulent, ant, landsarkiv, sameskola, musiklinje, yrkesorientering, stödorganisation | 0/4 | 0.160 | 0.023 | 0.061 |
| 8 | elev, lärare, undervisning, barn, grundskola, betyg, förälder, kunskap | 3/4 | 0.870 | 0.689 | 0.467 |
| 9 | högskola, län, behov, linje, hög, utveckling, universitet, teknisk | 4/4 | 0.923 | 0.811 | 0.604 |
| 10 | forskning, högskola, universitet, anslag, medel, resurs, forskarutbildning, verksamhet | 4/4 | 0.936 | 0.920 | 0.547 |
| 11 | universitet, forskning, umeå, område, stockholm, professur, lund, land | 0/4 | 0.581 | 0.517 | 0.213 |
| 12 | ämne, gymnasieskola, språk, elev, idrott, linje, årskurs, engelsk | 1/4 | 0.563 | 0.165 | 0.273 |
| 13 | skövde, län, skaraborg, livsmedelsindustri, skogsbruk, kooperativ, ekologisk, jordbruk | 0/4 | 0.185 | 0.018 | 0.055 |
| 14 | borås, barnomsorg, förskola, förskollärare, barn, plats, förskollärarutbildning, förskollärarlinj | 0/4 | 0.232 | 0.026 | 0.093 |
| 15 | svensk, kunskap, samhälle, människa, land, många, undervisning, betydelse | 3/4 | 0.725 | 0.554 | 0.246 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.4905
- Median: 0.4765
- Min: 0.0014
- Max: 0.9339
- Std Dev: 0.3490

**Jaccard Similarity (top 20 words):**
- Mean: 0.2270
- Median: 0.2121
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1985

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5465
- Median: 0.6391
- Min: 0.0035
- Max: 0.9806
- Std Dev: 0.3118

**Jaccard Similarity (top 20 words):**
- Mean: 0.2781
- Median: 0.2500
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2555

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5702
- Median: 0.7265
- Min: 0.0201
- Max: 0.9726
- Std Dev: 0.3373

**Jaccard Similarity (top 20 words):**
- Mean: 0.3027
- Median: 0.2500
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2314

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5022
- Median: 0.5965
- Min: 0.0180
- Max: 0.9200
- Std Dev: 0.3252

**Jaccard Similarity (top 20 words):**
- Mean: 0.2265
- Median: 0.1765
- Min: 0.0256
- Max: 0.5385
- Std Dev: 0.1562

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.4695
- Median: 0.4293
- Min: 0.0030
- Max: 0.9500
- Std Dev: 0.3487

**Jaccard Similarity (top 20 words):**
- Mean: 0.2628
- Median: 0.2121
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2259

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.4640
- Median: 0.5169
- Min: 0.0044
- Max: 0.9074
- Std Dev: 0.3378

**Jaccard Similarity (top 20 words):**
- Mean: 0.2504
- Median: 0.1765
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2186

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.4759
- Median: 0.3908
- Min: 0.0067
- Max: 0.9472
- Std Dev: 0.3256

**Jaccard Similarity (top 20 words):**
- Mean: 0.2320
- Median: 0.1765
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1789

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5779
- Median: 0.6114
- Min: 0.0376
- Max: 0.9710
- Std Dev: 0.2711

**Jaccard Similarity (top 20 words):**
- Mean: 0.2846
- Median: 0.2500
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1777

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5950
- Median: 0.6415
- Min: 0.0136
- Max: 0.9583
- Std Dev: 0.3197

**Jaccard Similarity (top 20 words):**
- Mean: 0.3059
- Median: 0.2903
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2149

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5467
- Median: 0.5977
- Min: 0.0322
- Max: 0.9280
- Std Dev: 0.2925

**Jaccard Similarity (top 20 words):**
- Mean: 0.2607
- Median: 0.2500
- Min: 0.0526
- Max: 0.6667
- Std Dev: 0.1964

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5239
- Median: 0.5958
- Min: 0.0014
- Max: 0.9806
- Std Dev: 0.3261

### Jaccard Similarity (across all matches)
- Mean: 0.2631
- Median: 0.2500
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2092
