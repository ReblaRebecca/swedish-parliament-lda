# Seed-Stability Analysis: Period 2006/07–2013/14, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2006/07–2013/14 (2314)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1191.69 | 50 |
| 123 | 1181.89 | 50 |
| 456 | 1191.29 | 50 |
| 789 | 1197.82 | 50 |
| 999 | 1178.45 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 2 |
| 2 of 4 | 2 |
| 1 of 4 | 0 |
| 0 of 4 | 3 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, ungdom, förälder, ung, kommun, elev, barnomsorg, hälsa | 4/4 | 0.895 | 0.842 | 0.357 |
| 2 | elev, lärare, undervisning, nationell, stöd, kunskap, förslag, mål | 4/4 | 0.890 | 0.829 | 0.451 |
| 3 | student, studie, studiemedel, fribelopp, ekonomisk, studera, höja, studerande | 3/4 | 0.869 | 0.592 | 0.552 |
| 4 | lärlingsutbildning, läkare, behov, gymnasial, vård, läkarutbildning, arbetsgivare, gammal | 0/4 | 0.600 | 0.467 | 0.245 |
| 5 | forskning, högskola, universitet, svensk, utveckling, hög, land, företag | 4/4 | 0.974 | 0.961 | 0.723 |
| 6 | högskola, hög, arbetsmarknad, vuxenutbildning, kunskap, student, behov, arbete | 2/4 | 0.660 | 0.262 | 0.327 |
| 7 | svensk, samhälle, rättighet, minoritet, land, religiös, människa, konfessionell | 0/4 | 0.424 | 0.125 | 0.132 |
| 8 | elev, kommun, fristående, kommunal, gymnasieskola, friskola, program, verksamhet | 3/4 | 0.844 | 0.658 | 0.396 |
| 9 | förskola, barn, personal, fritidshem, verksamhet, kommun, pedagogisk, kvinna | 4/4 | 0.909 | 0.845 | 0.508 |
| 10 | språk, undervisning, ämne, svensk, elev, svenska, läsa, modersmål | 2/4 | 0.645 | 0.297 | 0.340 |
| 11 | medicinsk, sjukdom, sjukvård, patient, läkemedel, forskning, geriatrisk, diagnos | 0/4 | 0.133 | 0.021 | 0.049 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7232
- Median: 0.8727
- Min: 0.1253
- Max: 0.9829
- Std Dev: 0.2722

**Jaccard Similarity (top 20 words):**
- Mean: 0.3431
- Median: 0.3333
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2174

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6389
- Median: 0.6625
- Min: 0.0772
- Max: 0.9757
- Std Dev: 0.2931

**Jaccard Similarity (top 20 words):**
- Mean: 0.2971
- Median: 0.2500
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2023

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7413
- Median: 0.8657
- Min: 0.0316
- Max: 0.9840
- Std Dev: 0.2854

**Jaccard Similarity (top 20 words):**
- Mean: 0.4616
- Median: 0.5385
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2370

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7488
- Median: 0.8294
- Min: 0.0206
- Max: 0.9935
- Std Dev: 0.2610

**Jaccard Similarity (top 20 words):**
- Mean: 0.3817
- Median: 0.3793
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2088

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7104
- Median: 0.7870
- Min: 0.0706
- Max: 0.9659
- Std Dev: 0.2746

**Jaccard Similarity (top 20 words):**
- Mean: 0.3825
- Median: 0.3333
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2435

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7260
- Median: 0.8638
- Min: 0.1605
- Max: 0.9909
- Std Dev: 0.2751

**Jaccard Similarity (top 20 words):**
- Mean: 0.4250
- Median: 0.3793
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2554

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8135
- Median: 0.9095
- Min: 0.4058
- Max: 0.9641
- Std Dev: 0.1876

**Jaccard Similarity (top 20 words):**
- Mean: 0.4637
- Median: 0.4815
- Min: 0.1429
- Max: 0.8182
- Std Dev: 0.2104

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6016
- Median: 0.6844
- Min: 0.0714
- Max: 0.9425
- Std Dev: 0.2869

**Jaccard Similarity (top 20 words):**
- Mean: 0.2901
- Median: 0.3333
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1816

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7330
- Median: 0.8254
- Min: 0.1546
- Max: 0.9831
- Std Dev: 0.2408

**Jaccard Similarity (top 20 words):**
- Mean: 0.3679
- Median: 0.3333
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2343

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7722
- Median: 0.8938
- Min: 0.3104
- Max: 0.9655
- Std Dev: 0.2234

**Jaccard Similarity (top 20 words):**
- Mean: 0.4097
- Median: 0.4815
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.2152

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7209
- Median: 0.8367
- Min: 0.0206
- Max: 0.9935
- Std Dev: 0.2683

### Jaccard Similarity (across all matches)
- Mean: 0.3822
- Median: 0.3793
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2289
