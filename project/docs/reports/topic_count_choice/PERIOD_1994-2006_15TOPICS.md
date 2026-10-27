# Seed-Stability Analysis: Period 1994/95–2005/06, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3055)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1537.95 | 50 |
| 123 | 1489.34 | 50 |
| 456 | 1525.98 | 50 |
| 789 | 1520.56 | 50 |
| 999 | 1544.46 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 4 |
| 2 of 4 | 1 |
| 1 of 4 | 2 |
| 0 of 4 | 4 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | mobbning, elev, barn, våld, arbete, problem, åtgärd, trakasseri | 4/4 | 0.927 | 0.882 | 0.636 |
| 2 | student, fristående, bidrag, studie, system, kommun, förslag, ekonomisk | 4/4 | 0.828 | 0.789 | 0.542 |
| 3 | barn, förskola, förälder, kommun, verksamhet, barnomsorg, personal, pedagogisk | 3/4 | 0.815 | 0.577 | 0.371 |
| 4 | forskning, universitet, svensk, utveckling, forskare, verksamhet, område, resurs | 4/4 | 0.826 | 0.751 | 0.502 |
| 5 | teknisk, luleå, basår, norrbotten, hus, civilingenjörsutbildning, konstfack, animation | 0/4 | 0.056 | 0.001 | 0.020 |
| 6 | region, land, län, utveckling, universitet, göteborg, område, högskola | 1/4 | 0.555 | 0.392 | 0.339 |
| 7 | lärare, kunskap, lärarutbildning, elev, samhälle, utveckla, undervisning, arbete | 3/4 | 0.786 | 0.592 | 0.426 |
| 8 | sexuell, samlevnad, körkort, fråga, homo, samlevnadsundervisning, homosexuell, hbt | 0/4 | 0.368 | 0.113 | 0.140 |
| 9 | elev, gymnasieskola, grundskola, kommun, betyg, nationell, undervisning, program | 4/4 | 0.949 | 0.919 | 0.572 |
| 10 | hälsa, ungdom, idrott, fysisk, barn, kvinna, ämne, aktivitet | 3/4 | 0.789 | 0.700 | 0.408 |
| 11 | högskola, student, universitet, forskning, kvalitet, lärosäte, anslag, forskarutbildning | 3/4 | 0.801 | 0.542 | 0.398 |
| 12 | yrkesutbildning, företag, arbetsliv, vuxenutbildning, kvalificerad, lärlingsutbildning, gymnasieskola, arbetsmarknad | 2/4 | 0.499 | 0.153 | 0.296 |
| 13 | språk, mälardalens, läromedel, bok, kristen, religiös, undervisning, religion | 0/4 | 0.253 | 0.005 | 0.053 |
| 14 | barn, funktionshind, specialskola, ekeskola, örebro, kommunal, kommun, synskadad | 1/4 | 0.319 | 0.158 | 0.172 |
| 15 | vårdnadsbidrag, småbarnsförälder, hotell, kväll, släkt, potentiell, serviceyrke, sekretariat | 0/4 | 0.007 | 0.003 | 0.000 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6061
- Median: 0.7836
- Min: 0.0033
- Max: 0.9721
- Std Dev: 0.3578

**Jaccard Similarity (top 20 words):**
- Mean: 0.3664
- Median: 0.4815
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2355

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5802
- Median: 0.6996
- Min: 0.0014
- Max: 0.9657
- Std Dev: 0.3031

**Jaccard Similarity (top 20 words):**
- Mean: 0.3323
- Median: 0.3333
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2246

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5902
- Median: 0.7890
- Min: 0.0093
- Max: 0.9817
- Std Dev: 0.3497

**Jaccard Similarity (top 20 words):**
- Mean: 0.3424
- Median: 0.3793
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2465

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5644
- Median: 0.7281
- Min: 0.0048
- Max: 0.9706
- Std Dev: 0.3329

**Jaccard Similarity (top 20 words):**
- Mean: 0.2586
- Median: 0.1765
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2173

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6583
- Median: 0.8302
- Min: 0.0028
- Max: 0.9824
- Std Dev: 0.3252

**Jaccard Similarity (top 20 words):**
- Mean: 0.4021
- Median: 0.3793
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.3016

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6646
- Median: 0.7625
- Min: 0.0026
- Max: 0.9748
- Std Dev: 0.2859

**Jaccard Similarity (top 20 words):**
- Mean: 0.3396
- Median: 0.3333
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2149

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6495
- Median: 0.7191
- Min: 0.0200
- Max: 0.9615
- Std Dev: 0.2803

**Jaccard Similarity (top 20 words):**
- Mean: 0.2907
- Median: 0.2500
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2009

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6119
- Median: 0.7404
- Min: 0.0383
- Max: 0.9406
- Std Dev: 0.2935

**Jaccard Similarity (top 20 words):**
- Mean: 0.3249
- Median: 0.3333
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2297

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5917
- Median: 0.6399
- Min: 0.0030
- Max: 0.9723
- Std Dev: 0.3171

**Jaccard Similarity (top 20 words):**
- Mean: 0.3337
- Median: 0.2903
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2311

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5976
- Median: 0.7032
- Min: 0.0025
- Max: 0.9516
- Std Dev: 0.3005

**Jaccard Similarity (top 20 words):**
- Mean: 0.2820
- Median: 0.2121
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2163

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6114
- Median: 0.7322
- Min: 0.0014
- Max: 0.9824
- Std Dev: 0.3173

### Jaccard Similarity (across all matches)
- Mean: 0.3273
- Median: 0.3333
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2366
