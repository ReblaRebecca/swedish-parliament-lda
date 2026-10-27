# Seed-Stability Analysis: Period 2006/07–2013/14, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2006/07–2013/14 (2026)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1151.66 | 50 |
| 123 | 1118.01 | 50 |
| 456 | 1143.91 | 50 |
| 789 | 1121.86 | 50 |
| 999 | 1169.02 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 1 |
| 2 of 4 | 3 |
| 1 of 4 | 0 |
| 0 of 4 | 3 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | högskola, hög, arbetsmarknad, gymnasieskola, kunskap, student, elev, vuxenutbildning | 3/4 | 0.830 | 0.672 | 0.515 |
| 2 | barn, förskola, förälder, kommun, barnomsorg, personal, behov, fritidshem | 4/4 | 0.945 | 0.868 | 0.605 |
| 3 | studie, förslag, heltid, högskola, studerande, studentkår, stipendium, prisbasbelopp | 0/4 | 0.170 | 0.051 | 0.042 |
| 4 | nationell, prov, myndighet, språk, diskriminering, lag, bedömning, svensk | 0/4 | 0.339 | 0.259 | 0.114 |
| 5 | elev, barn, kunskap, ungdom, undervisning, ämne, grundskola, ung | 2/4 | 0.733 | 0.670 | 0.392 |
| 6 | forskning, högskola, universitet, utveckling, svensk, lärosäte, hög, företag | 4/4 | 0.985 | 0.971 | 0.820 |
| 7 | land, läkare, svensk, vård, läkarutbildning, gammal, behov, kultur | 2/4 | 0.685 | 0.556 | 0.369 |
| 8 | anslag, satsning, högskola, stöd, grundutbildning, plats, forskarutbildning, universitet | 2/4 | 0.598 | 0.461 | 0.264 |
| 9 | elev, kommun, kommunal, fristående, verksamhet, friskola, förslag, skollag | 4/4 | 0.888 | 0.728 | 0.544 |
| 10 | student, studiemedel, fribelopp, studie, lån, arbeta, ekonomisk, studera | 4/4 | 0.926 | 0.887 | 0.359 |
| 11 | lärare, elev, lärarutbildning, it, undervisning, använda, kompetens, tillgång | 0/4 | 0.596 | 0.494 | 0.187 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7901
- Median: 0.8587
- Min: 0.4112
- Max: 0.9940
- Std Dev: 0.2032

**Jaccard Similarity (top 20 words):**
- Mean: 0.4555
- Median: 0.4286
- Min: 0.1429
- Max: 0.8182
- Std Dev: 0.2329

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6520
- Median: 0.6759
- Min: 0.1278
- Max: 0.9942
- Std Dev: 0.2602

**Jaccard Similarity (top 20 words):**
- Mean: 0.3240
- Median: 0.2500
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2613

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7132
- Median: 0.8395
- Min: 0.0653
- Max: 0.9967
- Std Dev: 0.2825

**Jaccard Similarity (top 20 words):**
- Mean: 0.4388
- Median: 0.4286
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2684

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6430
- Median: 0.6717
- Min: 0.0508
- Max: 0.9806
- Std Dev: 0.2823

**Jaccard Similarity (top 20 words):**
- Mean: 0.3133
- Median: 0.2903
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2171

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7146
- Median: 0.7816
- Min: 0.1339
- Max: 0.9913
- Std Dev: 0.2589

**Jaccard Similarity (top 20 words):**
- Mean: 0.3903
- Median: 0.4286
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2365

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7517
- Median: 0.9208
- Min: 0.0872
- Max: 0.9715
- Std Dev: 0.2880

**Jaccard Similarity (top 20 words):**
- Mean: 0.4981
- Median: 0.4815
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2825

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6571
- Median: 0.6854
- Min: 0.1882
- Max: 0.9661
- Std Dev: 0.2710

**Jaccard Similarity (top 20 words):**
- Mean: 0.3600
- Median: 0.3333
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2190

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7317
- Median: 0.9016
- Min: 0.1810
- Max: 0.9905
- Std Dev: 0.2741

**Jaccard Similarity (top 20 words):**
- Mean: 0.4037
- Median: 0.4286
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2553

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6341
- Median: 0.6569
- Min: 0.2192
- Max: 0.9866
- Std Dev: 0.2529

**Jaccard Similarity (top 20 words):**
- Mean: 0.3090
- Median: 0.3333
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.1893

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7065
- Median: 0.8111
- Min: 0.0946
- Max: 0.9767
- Std Dev: 0.2472

**Jaccard Similarity (top 20 words):**
- Mean: 0.3526
- Median: 0.3793
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.1770

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6994
- Median: 0.7634
- Min: 0.0508
- Max: 0.9967
- Std Dev: 0.2676

### Jaccard Similarity (across all matches)
- Mean: 0.3845
- Median: 0.3793
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2439
