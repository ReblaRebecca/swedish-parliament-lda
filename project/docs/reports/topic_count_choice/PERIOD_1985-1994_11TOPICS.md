# Seed-Stability Analysis: Period 1985/86–1993/94, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1985/86–1993/94 (3467)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1622.69 | 50 |
| 123 | 1626.25 | 50 |
| 456 | 1621.66 | 50 |
| 789 | 1599.64 | 50 |
| 999 | 1617.61 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 1 |
| 2 of 4 | 1 |
| 1 of 4 | 4 |
| 0 of 4 | 2 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | stockholm, handikapp, barn, döv, stiftelse, hörselskadad, handikappad, hls | 0/4 | 0.174 | 0.090 | 0.082 |
| 2 | gymnasieskola, linje, förslag, poäng, kurs, krav, social, hög | 2/4 | 0.615 | 0.399 | 0.325 |
| 3 | umeå, medicinsk, läkare, landsting, sjukvård, vård, hälsa, tjänst | 1/4 | 0.516 | 0.263 | 0.275 |
| 4 | högskola, län, teknisk, utveckling, region, plats, hög, linje | 4/4 | 0.908 | 0.861 | 0.435 |
| 5 | forskning, högskola, universitet, område, verksamhet, resurs, utveckling, förslag | 4/4 | 0.885 | 0.771 | 0.666 |
| 6 | ämne, språk, undervisning, idrott, kunskap, svensk, lärare, samhälle | 1/4 | 0.649 | 0.481 | 0.273 |
| 7 | anslag, bidrag, kommun, verksamhet, förslag, statsbidrag, budgetår, medel | 1/4 | 0.547 | 0.367 | 0.282 |
| 8 | kunskap, människa, elev, barn, problem, flicka, samhälle, undervisning | 1/4 | 0.561 | 0.385 | 0.178 |
| 9 | vuxenutbildning, kunskap, samhälle, folkhögskola, kvinna, hög, arbetsliv, folkbildning | 3/4 | 0.813 | 0.647 | 0.383 |
| 10 | göteborg, lund, borås, stockholm, universitet, malmö, jönköping, södra | 0/4 | 0.430 | 0.291 | 0.153 |
| 11 | skola, elev, kommun, barn, lärare, grundskola, förälder, undervisning | 4/4 | 0.955 | 0.911 | 0.633 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6554
- Median: 0.7706
- Min: 0.2620
- Max: 0.9904
- Std Dev: 0.2621

**Jaccard Similarity (top 20 words):**
- Mean: 0.3572
- Median: 0.3793
- Min: 0.0526
- Max: 0.9048
- Std Dev: 0.2438

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6381
- Median: 0.6348
- Min: 0.2305
- Max: 0.9692
- Std Dev: 0.2211

**Jaccard Similarity (top 20 words):**
- Mean: 0.3421
- Median: 0.3333
- Min: 0.1111
- Max: 0.9048
- Std Dev: 0.2367

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6452
- Median: 0.7086
- Min: 0.0897
- Max: 0.9925
- Std Dev: 0.2692

**Jaccard Similarity (top 20 words):**
- Mean: 0.3481
- Median: 0.2903
- Min: 0.0256
- Max: 1.0000
- Std Dev: 0.2511

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6259
- Median: 0.6104
- Min: 0.1154
- Max: 0.9424
- Std Dev: 0.2521

**Jaccard Similarity (top 20 words):**
- Mean: 0.2928
- Median: 0.2903
- Min: 0.0811
- Max: 0.5385
- Std Dev: 0.1507

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5785
- Median: 0.6512
- Min: 0.0564
- Max: 0.9402
- Std Dev: 0.2650

**Jaccard Similarity (top 20 words):**
- Mean: 0.2889
- Median: 0.2903
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1616

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6172
- Median: 0.6920
- Min: 0.2150
- Max: 0.9641
- Std Dev: 0.2548

**Jaccard Similarity (top 20 words):**
- Mean: 0.2688
- Median: 0.2500
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2155

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6672
- Median: 0.7612
- Min: 0.0082
- Max: 0.9720
- Std Dev: 0.2978

**Jaccard Similarity (top 20 words):**
- Mean: 0.3775
- Median: 0.4286
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2478

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6760
- Median: 0.6762
- Min: 0.1886
- Max: 0.9750
- Std Dev: 0.2245

**Jaccard Similarity (top 20 words):**
- Mean: 0.3744
- Median: 0.2903
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2243

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6416
- Median: 0.7239
- Min: 0.1829
- Max: 0.8984
- Std Dev: 0.2221

**Jaccard Similarity (top 20 words):**
- Mean: 0.2991
- Median: 0.3333
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1748

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6940
- Median: 0.7659
- Min: 0.2246
- Max: 0.9742
- Std Dev: 0.2350

**Jaccard Similarity (top 20 words):**
- Mean: 0.3220
- Median: 0.3333
- Min: 0.0811
- Max: 0.6000
- Std Dev: 0.1622

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6439
- Median: 0.7042
- Min: 0.0082
- Max: 0.9925
- Std Dev: 0.2534

### Jaccard Similarity (across all matches)
- Mean: 0.3271
- Median: 0.2903
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2134
