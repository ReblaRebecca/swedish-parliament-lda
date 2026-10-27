# Seed-Stability Analysis: Period 1985/86–1993/94, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1985/86–1993/94 (3737)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1657.60 | 50 |
| 123 | 1684.90 | 50 |
| 456 | 1642.97 | 50 |
| 789 | 1638.64 | 50 |
| 999 | 1642.02 | 50 |

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
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | kunskap, skola, elev, svensk, samhälle, betyg, barn, många | 2/4 | 0.667 | 0.478 | 0.269 |
| 2 | lärare, lärarutbildning, kvinna, umeå, plats, tjänst, universitet, grundskollärarutbildning | 1/4 | 0.522 | 0.351 | 0.247 |
| 3 | forskning, högskola, universitet, område, förslag, verksamhet, resurs, internationell | 3/4 | 0.846 | 0.548 | 0.591 |
| 4 | människa, kunskap, samhälle, barn, hälsa, många, social, problem | 2/4 | 0.595 | 0.394 | 0.242 |
| 5 | anslag, förslag, budgetår, vuxenutbildning, verksamhet, folkhögskola, medel, bidrag | 3/4 | 0.815 | 0.611 | 0.492 |
| 6 | elev, ämne, gymnasieskola, linje, undervisning, språk, kunskap, årskurs | 2/4 | 0.501 | 0.148 | 0.204 |
| 7 | skola, elev, kommun, lärare, barn, förälder, grundskola, fristående | 4/4 | 0.965 | 0.961 | 0.549 |
| 8 | högskola, län, hög, utveckling, region, teknisk, linje, land | 4/4 | 0.903 | 0.776 | 0.592 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6749
- Median: 0.7353
- Min: 0.1483
- Max: 0.9667
- Std Dev: 0.2575

**Jaccard Similarity (top 20 words):**
- Mean: 0.3222
- Median: 0.3563
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1821

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7482
- Median: 0.8603
- Min: 0.2458
- Max: 0.9863
- Std Dev: 0.2644

**Jaccard Similarity (top 20 words):**
- Mean: 0.4411
- Median: 0.4039
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2639

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7837
- Median: 0.8048
- Min: 0.3511
- Max: 0.9621
- Std Dev: 0.1798

**Jaccard Similarity (top 20 words):**
- Mean: 0.4525
- Median: 0.4039
- Min: 0.2121
- Max: 0.7391
- Std Dev: 0.1628

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7000
- Median: 0.6790
- Min: 0.3532
- Max: 0.9853
- Std Dev: 0.2266

**Jaccard Similarity (top 20 words):**
- Mean: 0.3774
- Median: 0.2917
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.2368

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8057
- Median: 0.9261
- Min: 0.3499
- Max: 0.9894
- Std Dev: 0.2040

**Jaccard Similarity (top 20 words):**
- Mean: 0.4901
- Median: 0.5100
- Min: 0.1111
- Max: 0.8182
- Std Dev: 0.1993

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6592
- Median: 0.6639
- Min: 0.3487
- Max: 0.9204
- Std Dev: 0.1993

**Jaccard Similarity (top 20 words):**
- Mean: 0.2593
- Median: 0.2166
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1785

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6629
- Median: 0.7152
- Min: 0.1833
- Max: 0.9935
- Std Dev: 0.2503

**Jaccard Similarity (top 20 words):**
- Mean: 0.3289
- Median: 0.3348
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.1774

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6731
- Median: 0.7157
- Min: 0.3632
- Max: 0.8895
- Std Dev: 0.1842

**Jaccard Similarity (top 20 words):**
- Mean: 0.3196
- Median: 0.3563
- Min: 0.0526
- Max: 0.5385
- Std Dev: 0.1707

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7728
- Median: 0.7994
- Min: 0.4408
- Max: 0.9877
- Std Dev: 0.1756

**Jaccard Similarity (top 20 words):**
- Mean: 0.3826
- Median: 0.3348
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.2165

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7370
- Median: 0.8465
- Min: 0.2913
- Max: 0.9708
- Std Dev: 0.2295

**Jaccard Similarity (top 20 words):**
- Mean: 0.3614
- Median: 0.2917
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2244

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7218
- Median: 0.7903
- Min: 0.1483
- Max: 0.9935
- Std Dev: 0.2254

### Jaccard Similarity (across all matches)
- Mean: 0.3735
- Median: 0.3793
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2145
