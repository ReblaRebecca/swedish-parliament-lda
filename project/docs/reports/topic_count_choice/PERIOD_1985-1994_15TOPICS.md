# Seed-Stability Analysis: Period 1985/86–1993/94, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1985/86–1993/94 (3737)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1604.90 | 50 |
| 123 | 1624.48 | 50 |
| 456 | 1599.68 | 50 |
| 789 | 1593.87 | 50 |
| 999 | 1606.51 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 1 |
| 2 of 4 | 4 |
| 1 of 4 | 3 |
| 0 of 4 | 4 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | svensk, kunskap, hög, land, utveckling, internationell, företag, samhälle | 2/4 | 0.678 | 0.401 | 0.391 |
| 2 | kvinna, flicka, bild, kvinnlig, kvinnoforskning, teknik, pojke, teknisk | 1/4 | 0.354 | 0.024 | 0.132 |
| 3 | forskning, högskola, universitet, resurs, förslag, område, verksamhet, liten | 4/4 | 0.971 | 0.962 | 0.689 |
| 4 | barn, örebro, döv, handikapp, hörselskadad, teckenspråk, förälder, stöd | 0/4 | 0.399 | 0.110 | 0.164 |
| 5 | anslag, förslag, vuxenutbildning, budgetår, bidrag, medel, verksamhet, kommun | 2/4 | 0.738 | 0.444 | 0.396 |
| 6 | högskola, poäng, studerande, linje, lärare, plats, kurs, förslag | 2/4 | 0.698 | 0.538 | 0.362 |
| 7 | göteborg, malmö, landsting, statlig, stockholm, konstnärlig, lund, trädgård | 0/4 | 0.442 | 0.343 | 0.187 |
| 8 | högskola, län, region, hög, utveckling, teknisk, regional, plats | 4/4 | 0.874 | 0.790 | 0.397 |
| 9 | ämne, lärare, undervisning, grundskola, läroplan, årskurs, kunskap, samhälle | 2/4 | 0.682 | 0.586 | 0.592 |
| 10 | folkhögskola, verksamhet, kommun, härnösand, syo, distansutbildning, hls, elev | 1/4 | 0.347 | 0.069 | 0.077 |
| 11 | barn, kunskap, elev, skola, många, samhälle, människa, arbete | 1/4 | 0.593 | 0.397 | 0.231 |
| 12 | gymnasieskola, elev, språk, undervisning, ämne, linje, svensk, försöksverksamhet | 3/4 | 0.705 | 0.418 | 0.358 |
| 13 | medicinsk, hälsa, läkare, sjukvård, vård, sjukdom, fysisk, patient | 0/4 | 0.501 | 0.184 | 0.214 |
| 14 | umeå, norrland, miljö, område, ekologisk, norra, livsmedelsindustri, luleå | 0/4 | 0.328 | 0.178 | 0.106 |
| 15 | skola, elev, kommun, lärare, grundskola, barn, förälder, betyg | 4/4 | 0.908 | 0.792 | 0.484 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5637
- Median: 0.6091
- Min: 0.0243
- Max: 0.9688
- Std Dev: 0.2546

**Jaccard Similarity (top 20 words):**
- Mean: 0.2537
- Median: 0.1765
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1992

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6390
- Median: 0.7506
- Min: 0.1100
- Max: 0.9845
- Std Dev: 0.3082

**Jaccard Similarity (top 20 words):**
- Mean: 0.3635
- Median: 0.2903
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2438

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6303
- Median: 0.6573
- Min: 0.2129
- Max: 0.9865
- Std Dev: 0.2233

**Jaccard Similarity (top 20 words):**
- Mean: 0.3002
- Median: 0.2903
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.1705

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6256
- Median: 0.6658
- Min: 0.0689
- Max: 0.9831
- Std Dev: 0.2630

**Jaccard Similarity (top 20 words):**
- Mean: 0.3572
- Median: 0.3793
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2437

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5749
- Median: 0.6643
- Min: 0.0194
- Max: 0.9146
- Std Dev: 0.2702

**Jaccard Similarity (top 20 words):**
- Mean: 0.2696
- Median: 0.2500
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1912

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6531
- Median: 0.8090
- Min: 0.1503
- Max: 0.9483
- Std Dev: 0.2733

**Jaccard Similarity (top 20 words):**
- Mean: 0.3285
- Median: 0.3793
- Min: 0.0256
- Max: 0.5385
- Std Dev: 0.1745

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5827
- Median: 0.5713
- Min: 0.0119
- Max: 0.9616
- Std Dev: 0.2997

**Jaccard Similarity (top 20 words):**
- Mean: 0.3135
- Median: 0.2121
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2581

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6789
- Median: 0.7111
- Min: 0.0310
- Max: 0.9723
- Std Dev: 0.2448

**Jaccard Similarity (top 20 words):**
- Mean: 0.3805
- Median: 0.3793
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.1900

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6442
- Median: 0.6324
- Min: 0.1215
- Max: 0.9750
- Std Dev: 0.2691

**Jaccard Similarity (top 20 words):**
- Mean: 0.3647
- Median: 0.2903
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2284

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6400
- Median: 0.5584
- Min: 0.1891
- Max: 0.9782
- Std Dev: 0.2599

**Jaccard Similarity (top 20 words):**
- Mean: 0.3494
- Median: 0.3793
- Min: 0.0526
- Max: 0.9048
- Std Dev: 0.2208

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6232
- Median: 0.6587
- Min: 0.0119
- Max: 0.9865
- Std Dev: 0.2700

### Jaccard Similarity (across all matches)
- Mean: 0.3281
- Median: 0.2903
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2179
