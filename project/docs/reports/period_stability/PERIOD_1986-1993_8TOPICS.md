# Seed-Stability Analysis: Period 1986-1993, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of 1986-1993 (3766)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1825.43 | 50 |
| 123 | 1789.43 | 50 |
| 456 | 1799.19 | 50 |
| 789 | 1787.17 | 50 |
| 999 | 1804.68 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 2 |
| 3 of 4 | 2 |
| 2 of 4 | 1 |
| 1 of 4 | 2 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | högskola, län, linje, anslag, utveckling, behov, teknisk, hög | 4/4 | 0.974 | 0.972 | 0.782 |
| 2 | miljö, land, nordisk, ekologisk, stiftelse, finsk, kultur, språk | 0/4 | 0.281 | 0.102 | 0.095 |
| 3 | umeå, behov, poäng, landsting, stockholm, land, norrland, universitet | 1/4 | 0.619 | 0.414 | 0.261 |
| 4 | ämne, kunskap, elev, gymnasieskola, människa, undervisning, många, samhälle | 3/4 | 0.745 | 0.665 | 0.430 |
| 5 | forskning, högskola, universitet, svensk, område, utveckling, internationell, verksamhet | 4/4 | 0.982 | 0.978 | 0.842 |
| 6 | universitet, göteborg, stockholm, forskning, professur, lund, institution, område | 2/4 | 0.687 | 0.483 | 0.342 |
| 7 | lärare, lärarutbildning, pedagogisk, borås, årskurs, grundskollärarutbildning, plats, poäng | 1/4 | 0.431 | 0.147 | 0.145 |
| 8 | elev, undervisning, kommun, gymnasieskola, barn, lärare, grundskola, kunskap | 3/4 | 0.845 | 0.660 | 0.426 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6814
- Median: 0.7509
- Min: 0.1907
- Max: 0.9780
- Std Dev: 0.2730

**Jaccard Similarity (top 20 words):**
- Mean: 0.3935
- Median: 0.3348
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2475

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7075
- Median: 0.7796
- Min: 0.1023
- Max: 0.9831
- Std Dev: 0.2910

**Jaccard Similarity (top 20 words):**
- Mean: 0.3889
- Median: 0.2957
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2680

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6877
- Median: 0.7593
- Min: 0.1474
- Max: 0.9819
- Std Dev: 0.2752

**Jaccard Similarity (top 20 words):**
- Mean: 0.4434
- Median: 0.3859
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2928

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7053
- Median: 0.6940
- Min: 0.2444
- Max: 0.9832
- Std Dev: 0.2171

**Jaccard Similarity (top 20 words):**
- Mean: 0.4358
- Median: 0.3348
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2966

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7611
- Median: 0.8597
- Min: 0.1973
- Max: 0.9899
- Std Dev: 0.2470

**Jaccard Similarity (top 20 words):**
- Mean: 0.4689
- Median: 0.4835
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2545

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7621
- Median: 0.8493
- Min: 0.3448
- Max: 0.9884
- Std Dev: 0.2287

**Jaccard Similarity (top 20 words):**
- Mean: 0.4335
- Median: 0.4589
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.2231

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7478
- Median: 0.7678
- Min: 0.3341
- Max: 0.9925
- Std Dev: 0.2191

**Jaccard Similarity (top 20 words):**
- Mean: 0.4279
- Median: 0.4039
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2467

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7042
- Median: 0.7099
- Min: 0.1704
- Max: 0.9944
- Std Dev: 0.2572

**Jaccard Similarity (top 20 words):**
- Mean: 0.4003
- Median: 0.2957
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2756

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8086
- Median: 0.7718
- Min: 0.6872
- Max: 0.9959
- Std Dev: 0.1148

**Jaccard Similarity (top 20 words):**
- Mean: 0.4850
- Median: 0.3793
- Min: 0.2500
- Max: 0.9048
- Std Dev: 0.2266

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7257
- Median: 0.7454
- Min: 0.2462
- Max: 0.9945
- Std Dev: 0.2588

**Jaccard Similarity (top 20 words):**
- Mean: 0.4765
- Median: 0.3118
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.3399

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7291
- Median: 0.7715
- Min: 0.1023
- Max: 0.9959
- Std Dev: 0.2458

### Jaccard Similarity (across all matches)
- Mean: 0.4353
- Median: 0.3793
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2712
