# Seed-Stability Analysis: Period 1994-2004, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of 1994-2004 (3313)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1658.60 | 50 |
| 123 | 1664.48 | 50 |
| 456 | 1623.42 | 50 |
| 789 | 1636.82 | 50 |
| 999 | 1639.93 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 2 |
| 2 of 4 | 1 |
| 1 of 4 | 2 |
| 0 of 4 | 5 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | lärare, elev, gymnasieskola, mobbning, program, kunskap, arbete, lärarutbildning | 3/4 | 0.776 | 0.682 | 0.365 |
| 2 | svensk, språk, invandrare, undervisning, svenska, samhälle, sfi, utländsk | 3/4 | 0.804 | 0.625 | 0.358 |
| 3 | musik, tfhs, etikprövning, gram, kulturskola, hantverkare, hovrätt, ambulanssjukvård | 0/4 | 0.055 | 0.004 | 0.020 |
| 4 | bidrag, örebro, teologisk, statsbidrag, konfessionell, fristående, kostnad, cancerfond | 0/4 | 0.280 | 0.043 | 0.137 |
| 5 | lund, körkort, land, skåne, historisk, it, nordisk, historia | 0/4 | 0.298 | 0.103 | 0.169 |
| 6 | läkare, läkarutbildning, sjukvård, medicinsk, umeå, vård, landsting, behov | 1/4 | 0.534 | 0.221 | 0.279 |
| 7 | ungdom, fysisk, hälsa, idrott, ämne, aktivitet, barn, undervisning | 1/4 | 0.571 | 0.386 | 0.331 |
| 8 | barn, förälder, elev, funktionshind, behov, kommun, problem, ungdom | 4/4 | 0.835 | 0.754 | 0.315 |
| 9 | högskola, student, universitet, forskning, hög, anslag, kvalitet, forskarutbildning | 4/4 | 0.861 | 0.778 | 0.549 |
| 10 | högskola, universitet, region, hög, utveckling, land, län, plats | 2/4 | 0.711 | 0.367 | 0.488 |
| 11 | göteborg, konstnärlig, bibliotek, universitet, design, institution, professur, film | 0/4 | 0.032 | 0.014 | 0.006 |
| 12 | forskning, universitet, utveckling, verksamhet, område, svensk, internationell, forskare | 4/4 | 0.865 | 0.734 | 0.503 |
| 13 | student, studie, system, studiemedel, studerande, studera, csn, ekonomisk | 4/4 | 0.871 | 0.765 | 0.651 |
| 14 | kvinna, jämställdhet, sexuell, flicka, kön, pojke, trakasseri, kvinnlig | 0/4 | 0.321 | 0.178 | 0.060 |
| 15 | elev, barn, kommun, förskola, fristående, grundskola, förälder, lärare | 4/4 | 0.891 | 0.847 | 0.596 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5471
- Median: 0.6354
- Min: 0.0274
- Max: 0.9104
- Std Dev: 0.2899

**Jaccard Similarity (top 20 words):**
- Mean: 0.2904
- Median: 0.3333
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2014

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6302
- Median: 0.7536
- Min: 0.0038
- Max: 0.9652
- Std Dev: 0.3114

**Jaccard Similarity (top 20 words):**
- Mean: 0.3542
- Median: 0.3793
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2417

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5823
- Median: 0.8078
- Min: 0.0273
- Max: 0.9456
- Std Dev: 0.3547

**Jaccard Similarity (top 20 words):**
- Mean: 0.3529
- Median: 0.2903
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2821

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5615
- Median: 0.6184
- Min: 0.0140
- Max: 0.9626
- Std Dev: 0.3361

**Jaccard Similarity (top 20 words):**
- Mean: 0.2897
- Median: 0.3333
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2202

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5502
- Median: 0.5404
- Min: 0.0239
- Max: 0.9603
- Std Dev: 0.3187

**Jaccard Similarity (top 20 words):**
- Mean: 0.2736
- Median: 0.2121
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1978

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5903
- Median: 0.7161
- Min: 0.0316
- Max: 0.9580
- Std Dev: 0.2924

**Jaccard Similarity (top 20 words):**
- Mean: 0.3131
- Median: 0.3333
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2078

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5821
- Median: 0.6063
- Min: 0.0084
- Max: 0.9547
- Std Dev: 0.3098

**Jaccard Similarity (top 20 words):**
- Mean: 0.3068
- Median: 0.2500
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2353

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6704
- Median: 0.8353
- Min: 0.0438
- Max: 0.9813
- Std Dev: 0.3276

**Jaccard Similarity (top 20 words):**
- Mean: 0.3967
- Median: 0.4286
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2468

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6124
- Median: 0.6976
- Min: 0.0629
- Max: 0.9802
- Std Dev: 0.3457

**Jaccard Similarity (top 20 words):**
- Mean: 0.3418
- Median: 0.3333
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2454

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6080
- Median: 0.7423
- Min: 0.0150
- Max: 0.9517
- Std Dev: 0.3343

**Jaccard Similarity (top 20 words):**
- Mean: 0.2976
- Median: 0.2903
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.2076

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5934
- Median: 0.7250
- Min: 0.0038
- Max: 0.9813
- Std Dev: 0.3247

### Jaccard Similarity (across all matches)
- Mean: 0.3217
- Median: 0.3333
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2329
