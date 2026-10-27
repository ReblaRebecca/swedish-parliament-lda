# Seed-Stability Analysis: Period 2006/07–2013/14, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2006/07–2013/14 (2314)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1186.34 | 50 |
| 123 | 1164.84 | 50 |
| 456 | 1185.82 | 50 |
| 789 | 1177.11 | 50 |
| 999 | 1138.43 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 2 |
| 2 of 4 | 3 |
| 1 of 4 | 1 |
| 0 of 4 | 4 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förälder, kommun, barnomsorg, ungdom, samhälle, behov, arbetstid | 4/4 | 0.872 | 0.803 | 0.407 |
| 2 | elev, lärare, stöd, nationell, fristående, undervisning, skollag, mål | 4/4 | 0.939 | 0.919 | 0.557 |
| 3 | student, studie, studiemedel, fribelopp, ekonomisk, studera, höja, studerande | 4/4 | 0.977 | 0.968 | 0.732 |
| 4 | kommun, kommunal, verksamhet, friskola, förslag, fristående, enskild, lag | 3/4 | 0.715 | 0.563 | 0.251 |
| 5 | forskning, högskola, universitet, utveckling, svensk, hög, internationell, land | 4/4 | 0.904 | 0.840 | 0.616 |
| 6 | högskola, hög, arbetsmarknad, vuxenutbildning, behov, student, kunskap, människa | 2/4 | 0.770 | 0.554 | 0.410 |
| 7 | land, svensk, människa, it, kultur, använda, demokrati, rättighet | 0/4 | 0.518 | 0.361 | 0.244 |
| 8 | elev, gymnasieskola, program, gymnasium, lärlingsutbildning, kunskap, ung, ämne | 1/4 | 0.655 | 0.523 | 0.312 |
| 9 | förskola, barn, personal, lärare, pedagogisk, fritidshem, lärarutbildning, verksamhet | 3/4 | 0.719 | 0.178 | 0.410 |
| 10 | språk, elev, svensk, svenska, undervisning, modersmål, ämne, läsa | 2/4 | 0.612 | 0.095 | 0.349 |
| 11 | symptom, kasta, kvinna, extrem, amerikansk, missförhållande, avvikande, genomgående | 0/4 | 0.090 | 0.012 | 0.006 |
| 12 | funktionsnedsättning, person, intellektuell, utveckla, tillgänglighet, uppdrag, förmåga, kompetens | 0/4 | 0.191 | 0.018 | 0.066 |
| 13 | ungdom, hälsa, fysisk, elev, ung, barn, aktivitet, psykisk | 2/4 | 0.717 | 0.669 | 0.302 |
| 14 | kunskap, företag, fråga, undervisning, sexuell, ung, samlevnad, entreprenörskap | 0/4 | 0.375 | 0.189 | 0.131 |
| 15 | läkare, land, läkarutbildning, vård, behov, gammal, sjukvård, patient | 4/4 | 0.863 | 0.754 | 0.593 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6241
- Median: 0.6847
- Min: 0.0125
- Max: 0.9836
- Std Dev: 0.2787

**Jaccard Similarity (top 20 words):**
- Mean: 0.3051
- Median: 0.2500
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2307

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5947
- Median: 0.6777
- Min: 0.0175
- Max: 0.9677
- Std Dev: 0.3269

**Jaccard Similarity (top 20 words):**
- Mean: 0.3233
- Median: 0.3793
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2227

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7237
- Median: 0.7678
- Min: 0.0436
- Max: 0.9826
- Std Dev: 0.2729

**Jaccard Similarity (top 20 words):**
- Mean: 0.3751
- Median: 0.3333
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2171

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7019
- Median: 0.8616
- Min: 0.0178
- Max: 0.9850
- Std Dev: 0.3269

**Jaccard Similarity (top 20 words):**
- Mean: 0.4332
- Median: 0.4815
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.3002

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6293
- Median: 0.7081
- Min: 0.0037
- Max: 0.9725
- Std Dev: 0.2836

**Jaccard Similarity (top 20 words):**
- Mean: 0.2950
- Median: 0.2903
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1957

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6295
- Median: 0.7447
- Min: 0.0259
- Max: 0.9763
- Std Dev: 0.3311

**Jaccard Similarity (top 20 words):**
- Mean: 0.3677
- Median: 0.3793
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2208

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7101
- Median: 0.8430
- Min: 0.0693
- Max: 0.9865
- Std Dev: 0.2699

**Jaccard Similarity (top 20 words):**
- Mean: 0.4164
- Median: 0.3333
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2672

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6296
- Median: 0.7784
- Min: 0.1191
- Max: 0.9759
- Std Dev: 0.2830

**Jaccard Similarity (top 20 words):**
- Mean: 0.3460
- Median: 0.3333
- Min: 0.0811
- Max: 0.7391
- Std Dev: 0.2158

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6518
- Median: 0.8068
- Min: 0.0510
- Max: 0.9653
- Std Dev: 0.3066

**Jaccard Similarity (top 20 words):**
- Mean: 0.3043
- Median: 0.3333
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1856

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7517
- Median: 0.8178
- Min: 0.1415
- Max: 0.9788
- Std Dev: 0.2528

**Jaccard Similarity (top 20 words):**
- Mean: 0.4055
- Median: 0.4286
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.1815

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6646
- Median: 0.7778
- Min: 0.0037
- Max: 0.9865
- Std Dev: 0.2986

### Jaccard Similarity (across all matches)
- Mean: 0.3572
- Median: 0.3333
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2313
