# Seed-Stability Analysis: Period 1994/95–2005/06, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3477)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1615.59 | 50 |
| 123 | 1607.75 | 50 |
| 456 | 1625.69 | 50 |
| 789 | 1611.53 | 50 |
| 999 | 1612.20 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 6 |
| 3 of 4 | 0 |
| 2 of 4 | 2 |
| 1 of 4 | 2 |
| 0 of 4 | 5 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | läkare, medicinsk, läkarutbildning, land, sjukvård, vård, alkohol, landsting | 2/4 | 0.629 | 0.465 | 0.349 |
| 2 | student, högskola, hög, universitet, kvalitet, svensk, akademisk, lärosäte | 4/4 | 0.840 | 0.766 | 0.363 |
| 3 | barn, elev, kommun, förskola, förälder, fristående, verksamhet, kommunal | 4/4 | 0.888 | 0.785 | 0.556 |
| 4 | elev, gymnasieskola, kunskap, betyg, program, lärare, ämne, många | 4/4 | 0.922 | 0.876 | 0.609 |
| 5 | kvinna, diskriminering, jämställdhet, lag, flicka, kön, arbete, kvinnlig | 1/4 | 0.687 | 0.535 | 0.356 |
| 6 | barn, mobbning, elev, arbete, förälder, problem, lärare, våld | 4/4 | 0.902 | 0.852 | 0.514 |
| 7 | lärare, lärarutbildning, pedagogisk, verksamhet, behov, undervisning, krav, utveckling | 0/4 | 0.443 | 0.231 | 0.218 |
| 8 | rättighet, svensk, samhälle, demokrati, kristen, teologisk, mänsklig, värde | 0/4 | 0.256 | 0.083 | 0.077 |
| 9 | bidrag, kommun, ekonomisk, student, system, studie, studerande, stat | 2/4 | 0.547 | 0.037 | 0.336 |
| 10 | tv, film, råd, bok, svensk, eu, läromedel, bibliotek | 0/4 | 0.203 | 0.060 | 0.102 |
| 11 | företag, län, näringsliv, region, kvalificerad, land, behov, gävle | 0/4 | 0.334 | 0.152 | 0.138 |
| 12 | hälsa, fysisk, barn, ungdom, idrott, ämne, aktivitet, mat | 1/4 | 0.568 | 0.340 | 0.305 |
| 13 | forskning, universitet, forskare, utveckling, svensk, område, forskarutbildning, internationell | 4/4 | 0.868 | 0.734 | 0.430 |
| 14 | högskola, universitet, forskning, hög, anslag, plats, utveckling, satsning | 4/4 | 0.900 | 0.777 | 0.574 |
| 15 | fråga, sexuell, homo, hbt, homosexuell, människa, undervisning, bisexuell | 0/4 | 0.330 | 0.003 | 0.126 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6493
- Median: 0.7660
- Min: 0.0879
- Max: 0.9581
- Std Dev: 0.2741

**Jaccard Similarity (top 20 words):**
- Mean: 0.3714
- Median: 0.3793
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2395

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6167
- Median: 0.7380
- Min: 0.0029
- Max: 0.9803
- Std Dev: 0.3325

**Jaccard Similarity (top 20 words):**
- Mean: 0.3104
- Median: 0.2903
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2112

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6320
- Median: 0.6629
- Min: 0.0827
- Max: 0.9349
- Std Dev: 0.2610

**Jaccard Similarity (top 20 words):**
- Mean: 0.3560
- Median: 0.2903
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2042

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5863
- Median: 0.5978
- Min: 0.0371
- Max: 0.9564
- Std Dev: 0.3133

**Jaccard Similarity (top 20 words):**
- Mean: 0.3100
- Median: 0.2500
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2239

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5627
- Median: 0.6678
- Min: 0.0077
- Max: 0.9330
- Std Dev: 0.2927

**Jaccard Similarity (top 20 words):**
- Mean: 0.2305
- Median: 0.2500
- Min: 0.0000
- Max: 0.4815
- Std Dev: 0.1599

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6273
- Median: 0.7167
- Min: 0.1110
- Max: 0.9473
- Std Dev: 0.2565

**Jaccard Similarity (top 20 words):**
- Mean: 0.2987
- Median: 0.2903
- Min: 0.0256
- Max: 0.5385
- Std Dev: 0.1672

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6079
- Median: 0.7183
- Min: 0.0486
- Max: 0.9869
- Std Dev: 0.3098

**Jaccard Similarity (top 20 words):**
- Mean: 0.3440
- Median: 0.2903
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2488

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6483
- Median: 0.7055
- Min: 0.0096
- Max: 0.9775
- Std Dev: 0.2996

**Jaccard Similarity (top 20 words):**
- Mean: 0.3463
- Median: 0.3333
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2381

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5935
- Median: 0.6715
- Min: 0.0166
- Max: 0.9861
- Std Dev: 0.3145

**Jaccard Similarity (top 20 words):**
- Mean: 0.2924
- Median: 0.2121
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2268

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6295
- Median: 0.6542
- Min: 0.1564
- Max: 0.9627
- Std Dev: 0.2712

**Jaccard Similarity (top 20 words):**
- Mean: 0.3127
- Median: 0.2500
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2280

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6153
- Median: 0.6883
- Min: 0.0029
- Max: 0.9869
- Std Dev: 0.2947

### Jaccard Similarity (across all matches)
- Mean: 0.3172
- Median: 0.2903
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2200
