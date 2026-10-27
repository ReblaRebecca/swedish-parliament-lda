# Seed-Stability Analysis: Period 1985/86–1993/94, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1985/86–1993/94 (3467)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1603.07 | 50 |
| 123 | 1594.67 | 50 |
| 456 | 1599.18 | 50 |
| 789 | 1588.54 | 50 |
| 999 | 1596.25 | 50 |

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
| 0 of 4 | 4 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | dans, etisk, gymnasium, alkohol, djur, rekommendation, byggnadsstyrelse, djurförsök | 0/4 | 0.048 | 0.003 | 0.020 |
| 2 | skola, elev, kommun, gymnasieskola, fristående, förslag, kommunal, grundskola | 4/4 | 0.974 | 0.961 | 0.764 |
| 3 | falun, västerås, borlänge, finsk, nordisk, eskilstuna, finland, finskspråkig | 0/4 | 0.084 | 0.056 | 0.040 |
| 4 | högskola, linje, teknisk, län, plats, utveckling, hög, region | 4/4 | 0.908 | 0.871 | 0.431 |
| 5 | forskning, universitet, högskola, område, verksamhet, utveckling, resurs, land | 3/4 | 0.864 | 0.548 | 0.594 |
| 6 | ämne, språk, undervisning, årskurs, grundskola, lärare, läroplan, gymnasieskola | 1/4 | 0.546 | 0.208 | 0.247 |
| 7 | anslag, bidrag, verksamhet, budgetår, förslag, statsbidrag, medel, kommun | 3/4 | 0.692 | 0.340 | 0.379 |
| 8 | kunskap, miljö, människa, flicka, samhälle, hälsa, kvinna, hemkunskap | 2/4 | 0.702 | 0.606 | 0.333 |
| 9 | vuxenutbildning, folkhögskola, kunskap, kompetensutveckling, komvux, kompetens, folkbildning, arbetsliv | 3/4 | 0.726 | 0.387 | 0.353 |
| 10 | län, skövde, jönköping, skaraborg, kristianstad, turism, livsmedelsindustri, skogsbruk | 0/4 | 0.319 | 0.113 | 0.121 |
| 11 | skola, barn, svensk, kunskap, undervisning, land, samhälle, förälder | 0/4 | 0.419 | 0.245 | 0.213 |
| 12 | universitet, stockholm, umeå, göteborg, borås, land, kommun, lund | 2/4 | 0.589 | 0.373 | 0.222 |
| 13 | elev, lärare, skola, betyg, gymnasieskola, undervisning, kunskap, grundskola | 4/4 | 0.808 | 0.738 | 0.306 |
| 14 | landsting, vård, poäng, medicinsk, social, hälsa, läkare, sjukvård | 2/4 | 0.598 | 0.313 | 0.285 |
| 15 | högskola, förslag, hög, student, social, studerande, krav, budgetår | 1/4 | 0.634 | 0.507 | 0.215 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5710
- Median: 0.7315
- Min: 0.0100
- Max: 0.9758
- Std Dev: 0.3513

**Jaccard Similarity (top 20 words):**
- Mean: 0.3256
- Median: 0.2500
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2736

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6067
- Median: 0.7336
- Min: 0.0624
- Max: 0.9755
- Std Dev: 0.2995

**Jaccard Similarity (top 20 words):**
- Mean: 0.3215
- Median: 0.3333
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.1964

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6168
- Median: 0.6795
- Min: 0.0031
- Max: 0.9846
- Std Dev: 0.2594

**Jaccard Similarity (top 20 words):**
- Mean: 0.2533
- Median: 0.2121
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2058

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5818
- Median: 0.5671
- Min: 0.0525
- Max: 0.9755
- Std Dev: 0.2964

**Jaccard Similarity (top 20 words):**
- Mean: 0.3054
- Median: 0.1765
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2387

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6258
- Median: 0.6840
- Min: 0.0150
- Max: 0.9921
- Std Dev: 0.2926

**Jaccard Similarity (top 20 words):**
- Mean: 0.3456
- Median: 0.2903
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2376

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5635
- Median: 0.6541
- Min: 0.0011
- Max: 0.9942
- Std Dev: 0.2951

**Jaccard Similarity (top 20 words):**
- Mean: 0.3052
- Median: 0.2121
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2647

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6234
- Median: 0.6663
- Min: 0.0345
- Max: 0.9869
- Std Dev: 0.2800

**Jaccard Similarity (top 20 words):**
- Mean: 0.3247
- Median: 0.2903
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2206

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6702
- Median: 0.7782
- Min: 0.0728
- Max: 0.9837
- Std Dev: 0.2828

**Jaccard Similarity (top 20 words):**
- Mean: 0.3749
- Median: 0.3333
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2181

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6039
- Median: 0.6579
- Min: 0.0956
- Max: 0.9786
- Std Dev: 0.2828

**Jaccard Similarity (top 20 words):**
- Mean: 0.3195
- Median: 0.2903
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2086

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5920
- Median: 0.7204
- Min: 0.0224
- Max: 0.9886
- Std Dev: 0.3220

**Jaccard Similarity (top 20 words):**
- Mean: 0.3170
- Median: 0.3333
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2398

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6055
- Median: 0.6716
- Min: 0.0011
- Max: 0.9942
- Std Dev: 0.2986

### Jaccard Similarity (across all matches)
- Mean: 0.3193
- Median: 0.2903
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2335
