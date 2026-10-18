# Seed-Stability Analysis: Period 2006/07–2013/14, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2006/07–2013/14 (2879)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1538.19 | 50 |
| 123 | 1540.30 | 50 |
| 456 | 1537.17 | 50 |
| 789 | 1539.49 | 50 |
| 999 | 1499.25 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 3 |
| 2 of 4 | 2 |
| 1 of 4 | 0 |
| 0 of 4 | 7 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, fysisk, personal, aktivitet, ungdom, många, fritidshem | 4/4 | 0.865 | 0.704 | 0.408 |
| 2 | elev, lärare, kunskap, undervisning, gymnasieskola, ämne, grundskola, nationell | 3/4 | 0.824 | 0.500 | 0.453 |
| 3 | elev, kommun, fristående, kommunal, verksamhet, friskola, skollag, barn | 3/4 | 0.864 | 0.689 | 0.449 |
| 4 | kunskap, lärare, ungdom, arbete, ung, samhälle, många, kvinna | 0/4 | 0.468 | 0.366 | 0.179 |
| 5 | människa, svensk, samhälle, lycka, kultur, läromedel, värde, diskriminering | 0/4 | 0.428 | 0.155 | 0.131 |
| 6 | språk, körkort, svensk, teckenspråk, elev, mat, modersmålsundervisning, barn | 2/4 | 0.543 | 0.143 | 0.349 |
| 7 | läkare, hälsa, vård, läkarutbildning, sjukvård, gammal, patient, medicinsk | 3/4 | 0.700 | 0.438 | 0.399 |
| 8 | högskola, forskarutbildning, lärarutbildning, lärare, anslag, universitet, kvalitet, nivå | 0/4 | 0.587 | 0.503 | 0.135 |
| 9 | student, studie, arbetsmarknad, hög, studera, vuxenutbildning, många, studiemedel | 4/4 | 0.882 | 0.853 | 0.422 |
| 10 | person, funktionsnedsättning, punktskrift, undervisning, synskadad, personlig, konvention, assistent | 2/4 | 0.474 | 0.080 | 0.250 |
| 11 | avgift, hjälpmedel, karriärtjänst, kostnad, grundskola, avgiftsfri, dyslexi, skollag | 0/4 | 0.095 | 0.005 | 0.033 |
| 12 | anläggning, ess, rymdverksamhet, hemundervisning, dansk, svensk, max, rymdforskning | 0/4 | 0.154 | 0.048 | 0.069 |
| 13 | forskning, högskola, universitet, hög, utveckling, svensk, företag, land | 4/4 | 0.887 | 0.700 | 0.609 |
| 14 | förälder, kommun, barnomsorg, barn, arbetstid, obekväm, erbjuda, behov | 0/4 | 0.507 | 0.148 | 0.427 |
| 15 | land, behov, hållbar, yrkesutbildning, svensk, utveckling, kvalificerad, nordisk | 0/4 | 0.257 | 0.171 | 0.081 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6000
- Median: 0.6559
- Min: 0.0476
- Max: 0.9335
- Std Dev: 0.2828

**Jaccard Similarity (top 20 words):**
- Mean: 0.2981
- Median: 0.3333
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.1977

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5179
- Median: 0.5657
- Min: 0.0801
- Max: 0.9656
- Std Dev: 0.3007

**Jaccard Similarity (top 20 words):**
- Mean: 0.2306
- Median: 0.1765
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1972

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5617
- Median: 0.5779
- Min: 0.0048
- Max: 0.9551
- Std Dev: 0.3194

**Jaccard Similarity (top 20 words):**
- Mean: 0.2806
- Median: 0.1429
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.2104

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5963
- Median: 0.6763
- Min: 0.0261
- Max: 0.9861
- Std Dev: 0.3072

**Jaccard Similarity (top 20 words):**
- Mean: 0.3621
- Median: 0.3333
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2724

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6169
- Median: 0.5755
- Min: 0.0995
- Max: 0.9727
- Std Dev: 0.3096

**Jaccard Similarity (top 20 words):**
- Mean: 0.3275
- Median: 0.2500
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2472

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5746
- Median: 0.7320
- Min: 0.0620
- Max: 0.9531
- Std Dev: 0.3271

**Jaccard Similarity (top 20 words):**
- Mean: 0.2767
- Median: 0.3793
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1914

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6218
- Median: 0.7119
- Min: 0.0361
- Max: 0.9441
- Std Dev: 0.2940

**Jaccard Similarity (top 20 words):**
- Mean: 0.2889
- Median: 0.2903
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1924

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5424
- Median: 0.5609
- Min: 0.0567
- Max: 0.9594
- Std Dev: 0.3215

**Jaccard Similarity (top 20 words):**
- Mean: 0.2355
- Median: 0.2500
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1788

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6288
- Median: 0.7917
- Min: 0.0071
- Max: 0.9864
- Std Dev: 0.3227

**Jaccard Similarity (top 20 words):**
- Mean: 0.3439
- Median: 0.2903
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2616

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5355
- Median: 0.6061
- Min: 0.1107
- Max: 0.9661
- Std Dev: 0.3098

**Jaccard Similarity (top 20 words):**
- Mean: 0.2554
- Median: 0.2500
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.1642

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5796
- Median: 0.6146
- Min: 0.0048
- Max: 0.9864
- Std Dev: 0.3120

### Jaccard Similarity (across all matches)
- Mean: 0.2899
- Median: 0.2903
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2182
