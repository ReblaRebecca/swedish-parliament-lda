# Seed-Stability Analysis: Period 2005-2014, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of 2005-2014 (3577)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1556.78 | 50 |
| 123 | 1522.86 | 50 |
| 456 | 1557.62 | 50 |
| 789 | 1532.73 | 50 |
| 999 | 1549.38 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 2 |
| 3 of 4 | 4 |
| 2 of 4 | 2 |
| 1 of 4 | 1 |
| 0 of 4 | 2 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | student, studie, arbetsmarknad, gymnasieskola, många, vuxenutbildning, behov, arbete | 3/4 | 0.692 | 0.476 | 0.334 |
| 2 | elev, mobbning, lag, arbete, våld, lärare, förälder, åtgärd | 0/4 | 0.500 | 0.335 | 0.098 |
| 3 | konfessionell, undervisning, religiös, musik, friskola, person, punktskrift, kristen | 0/4 | 0.098 | 0.052 | 0.033 |
| 4 | forskning, svensk, utveckling, område, forskare, företag, internationell, utveckla | 3/4 | 0.708 | 0.340 | 0.410 |
| 5 | barn, hälsa, ungdom, fysisk, många, läkare, aktivitet, ung | 3/4 | 0.728 | 0.653 | 0.380 |
| 6 | svensk, land, it, företag, utveckling, människa, verksamhet, använda | 1/4 | 0.586 | 0.457 | 0.197 |
| 7 | elev, lärare, nationell, betyg, mål, kunskap, lärarutbildning, stöd | 4/4 | 0.918 | 0.868 | 0.471 |
| 8 | elev, kunskap, undervisning, barn, språk, samhälle, ämne, svensk | 3/4 | 0.714 | 0.680 | 0.359 |
| 9 | barn, kommun, förskola, elev, förälder, fristående, kommunal, verksamhet | 4/4 | 0.840 | 0.755 | 0.460 |
| 10 | högskola, universitet, forskning, hög, region, län, regional, land | 2/4 | 0.637 | 0.159 | 0.210 |
| 11 | högskola, student, hög, kvalitet, anslag, universitet, lärosäte, öka | 2/4 | 0.652 | 0.399 | 0.157 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6484
- Median: 0.7220
- Min: 0.0818
- Max: 0.9580
- Std Dev: 0.2391

**Jaccard Similarity (top 20 words):**
- Mean: 0.2831
- Median: 0.2903
- Min: 0.0526
- Max: 0.5385
- Std Dev: 0.1559

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6472
- Median: 0.7431
- Min: 0.0592
- Max: 0.9207
- Std Dev: 0.2413

**Jaccard Similarity (top 20 words):**
- Mean: 0.2670
- Median: 0.2121
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1767

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6405
- Median: 0.6799
- Min: 0.1588
- Max: 0.9001
- Std Dev: 0.2431

**Jaccard Similarity (top 20 words):**
- Mean: 0.3070
- Median: 0.2903
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.1936

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6361
- Median: 0.7339
- Min: 0.0516
- Max: 0.9478
- Std Dev: 0.2568

**Jaccard Similarity (top 20 words):**
- Mean: 0.2732
- Median: 0.3333
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1788

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6989
- Median: 0.8815
- Min: 0.0401
- Max: 0.9785
- Std Dev: 0.2876

**Jaccard Similarity (top 20 words):**
- Mean: 0.3667
- Median: 0.3793
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2088

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8235
- Median: 0.9319
- Min: 0.1851
- Max: 0.9875
- Std Dev: 0.2338

**Jaccard Similarity (top 20 words):**
- Mean: 0.4925
- Median: 0.4815
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2868

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8189
- Median: 0.8934
- Min: 0.3937
- Max: 0.9759
- Std Dev: 0.1744

**Jaccard Similarity (top 20 words):**
- Mean: 0.5184
- Median: 0.5385
- Min: 0.0811
- Max: 0.8182
- Std Dev: 0.2297

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7108
- Median: 0.8254
- Min: 0.1264
- Max: 0.9922
- Std Dev: 0.2910

**Jaccard Similarity (top 20 words):**
- Mean: 0.4637
- Median: 0.4286
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2426

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6720
- Median: 0.7301
- Min: 0.2665
- Max: 0.8754
- Std Dev: 0.1766

**Jaccard Similarity (top 20 words):**
- Mean: 0.3353
- Median: 0.3793
- Min: 0.0526
- Max: 0.5385
- Std Dev: 0.1489

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7104
- Median: 0.8165
- Min: 0.1633
- Max: 0.9627
- Std Dev: 0.2326

**Jaccard Similarity (top 20 words):**
- Mean: 0.4183
- Median: 0.3793
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2323

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7007
- Median: 0.7590
- Min: 0.0401
- Max: 0.9922
- Std Dev: 0.2493

### Jaccard Similarity (across all matches)
- Mean: 0.3725
- Median: 0.3793
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2279
