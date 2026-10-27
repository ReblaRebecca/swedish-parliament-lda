# Seed-Stability Analysis: Period 1985/86–1993/94, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1985/86–1993/94 (3613)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1600.40 | 50 |
| 123 | 1602.70 | 50 |
| 456 | 1595.29 | 50 |
| 789 | 1585.10 | 50 |
| 999 | 1615.07 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 4 |
| 2 of 4 | 3 |
| 1 of 4 | 3 |
| 0 of 4 | 2 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | forskning, högskola, universitet, område, verksamhet, medel, resurs, professur | 4/4 | 0.939 | 0.872 | 0.728 |
| 2 | förslag, gymnasieskola, anslag, särskild, hög, resurs, budgetår, medel | 3/4 | 0.704 | 0.334 | 0.378 |
| 3 | kunskap, hälsa, problem, flicka, människa, vård, hemkunskap, medicinsk | 1/4 | 0.534 | 0.184 | 0.178 |
| 4 | umeå, norrland, skogslän, regionalpolitisk, region, vårdlärarutbildning, regional, fortbildning | 0/4 | 0.309 | 0.001 | 0.040 |
| 5 | kunskap, hög, samhälle, utveckling, land, svensk, utveckla, människa | 3/4 | 0.607 | 0.204 | 0.226 |
| 6 | barn, elev, handikapp, särskola, förälder, handikappad, döv, utvecklingsstörd | 1/4 | 0.398 | 0.118 | 0.114 |
| 7 | språk, svensk, undervisning, invandrare, svenska, land, internationell, hemspråksundervisning | 2/4 | 0.462 | 0.088 | 0.217 |
| 8 | ämne, samhälle, undervisning, läroplan, skola, religionskunskap, barn, människa | 1/4 | 0.515 | 0.034 | 0.199 |
| 9 | lärare, ämne, gymnasieskola, elev, kunskap, lärarutbildning, grundskola, årskurs | 2/4 | 0.604 | 0.429 | 0.239 |
| 10 | vuxenutbildning, folkhögskola, verksamhet, studieförbund, komvux, kommun, bidrag, vuxen | 3/4 | 0.675 | 0.408 | 0.349 |
| 11 | skola, elev, kommun, barn, lärare, grundskola, undervisning, förälder | 4/4 | 0.928 | 0.858 | 0.464 |
| 12 | högskola, universitet, plats, förslag, studerande, kurs, hög, student | 3/4 | 0.770 | 0.603 | 0.344 |
| 13 | lund, landsting, tjänst, läkare, universitet, stiftelse, sjukgymnast, läkarutbildning | 0/4 | 0.348 | 0.141 | 0.053 |
| 14 | högskola, teknisk, linje, karlstad, poäng, teknik, kompetens, inriktning | 2/4 | 0.487 | 0.104 | 0.183 |
| 15 | län, högskola, region, utveckling, regional, näringsliv, hög, land | 4/4 | 0.864 | 0.775 | 0.556 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5984
- Median: 0.7281
- Min: 0.0344
- Max: 0.9850
- Std Dev: 0.3118

**Jaccard Similarity (top 20 words):**
- Mean: 0.3025
- Median: 0.2500
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2207

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6515
- Median: 0.7523
- Min: 0.0013
- Max: 0.9403
- Std Dev: 0.2700

**Jaccard Similarity (top 20 words):**
- Mean: 0.3001
- Median: 0.2903
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2042

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6342
- Median: 0.7345
- Min: 0.1038
- Max: 0.9869
- Std Dev: 0.2698

**Jaccard Similarity (top 20 words):**
- Mean: 0.2926
- Median: 0.2500
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2191

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5548
- Median: 0.6357
- Min: 0.0880
- Max: 0.9888
- Std Dev: 0.2821

**Jaccard Similarity (top 20 words):**
- Mean: 0.2431
- Median: 0.2121
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2202

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6228
- Median: 0.7253
- Min: 0.0049
- Max: 0.9573
- Std Dev: 0.3012

**Jaccard Similarity (top 20 words):**
- Mean: 0.3214
- Median: 0.3333
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2166

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5526
- Median: 0.6967
- Min: 0.0143
- Max: 0.8990
- Std Dev: 0.3000

**Jaccard Similarity (top 20 words):**
- Mean: 0.2432
- Median: 0.1765
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1737

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6226
- Median: 0.7340
- Min: 0.0081
- Max: 0.9811
- Std Dev: 0.2961

**Jaccard Similarity (top 20 words):**
- Mean: 0.3285
- Median: 0.3793
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2157

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5988
- Median: 0.7027
- Min: 0.0273
- Max: 0.9806
- Std Dev: 0.2931

**Jaccard Similarity (top 20 words):**
- Mean: 0.3046
- Median: 0.2500
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2592

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5773
- Median: 0.6305
- Min: 0.0192
- Max: 0.9563
- Std Dev: 0.3199

**Jaccard Similarity (top 20 words):**
- Mean: 0.3042
- Median: 0.2500
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2198

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6399
- Median: 0.7189
- Min: 0.1033
- Max: 0.9745
- Std Dev: 0.3057

**Jaccard Similarity (top 20 words):**
- Mean: 0.3935
- Median: 0.3333
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2553

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6053
- Median: 0.7167
- Min: 0.0013
- Max: 0.9888
- Std Dev: 0.2972

### Jaccard Similarity (across all matches)
- Mean: 0.3034
- Median: 0.2903
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2253
