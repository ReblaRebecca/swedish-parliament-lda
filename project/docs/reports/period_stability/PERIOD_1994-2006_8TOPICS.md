# Seed-Stability Analysis: Period 1994/95–2005/06, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3477)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1683.46 | 50 |
| 123 | 1666.72 | 50 |
| 456 | 1670.65 | 50 |
| 789 | 1649.44 | 50 |
| 999 | 1658.91 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 4 |
| 2 of 4 | 0 |
| 1 of 4 | 0 |
| 0 of 4 | 1 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | hälsa, barn, ungdom, fysisk, ämne, idrott, elev, aktivitet | 4/4 | 0.838 | 0.734 | 0.660 |
| 2 | högskola, student, universitet, hög, land, utveckling, region, forskning | 4/4 | 0.900 | 0.851 | 0.590 |
| 3 | elev, barn, kommun, förskola, förälder, fristående, grundskola, behov | 4/4 | 0.895 | 0.813 | 0.608 |
| 4 | lärare, gymnasieskola, kunskap, elev, hög, många, program, krav | 3/4 | 0.804 | 0.674 | 0.398 |
| 5 | forskning, högskola, universitet, anslag, forskarutbildning, hög, kvalitet, grundutbildning | 3/4 | 0.767 | 0.288 | 0.485 |
| 6 | barn, mobbning, elev, arbete, lärare, förälder, problem, funktionshind | 3/4 | 0.765 | 0.323 | 0.448 |
| 7 | svensk, utveckling, verksamhet, land, behov, samhälle, universitet, område | 0/4 | 0.555 | 0.404 | 0.278 |
| 8 | student, bidrag, studiemedel, studerande, ekonomisk, system, stat, csn | 3/4 | 0.797 | 0.693 | 0.507 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.8350
- Median: 0.8675
- Min: 0.6003
- Max: 0.9650
- Std Dev: 0.1232

**Jaccard Similarity (top 20 words):**
- Mean: 0.5081
- Median: 0.5692
- Min: 0.2121
- Max: 0.8182
- Std Dev: 0.1968

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8328
- Median: 0.9034
- Min: 0.5161
- Max: 0.9980
- Std Dev: 0.1579

**Jaccard Similarity (top 20 words):**
- Mean: 0.5696
- Median: 0.6333
- Min: 0.1429
- Max: 0.8182
- Std Dev: 0.2320

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7061
- Median: 0.7937
- Min: 0.2877
- Max: 0.9171
- Std Dev: 0.2136

**Jaccard Similarity (top 20 words):**
- Mean: 0.3997
- Median: 0.4815
- Min: 0.0526
- Max: 0.5385
- Std Dev: 0.1563

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7863
- Median: 0.8497
- Min: 0.3235
- Max: 0.9269
- Std Dev: 0.1872

**Jaccard Similarity (top 20 words):**
- Mean: 0.5093
- Median: 0.5385
- Min: 0.1111
- Max: 0.7391
- Std Dev: 0.1929

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8111
- Median: 0.8589
- Min: 0.6129
- Max: 0.9640
- Std Dev: 0.1264

**Jaccard Similarity (top 20 words):**
- Mean: 0.4501
- Median: 0.4815
- Min: 0.1765
- Max: 0.7391
- Std Dev: 0.1735

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6882
- Median: 0.7946
- Min: 0.2968
- Max: 0.9761
- Std Dev: 0.2436

**Jaccard Similarity (top 20 words):**
- Mean: 0.3870
- Median: 0.4074
- Min: 0.0526
- Max: 0.9048
- Std Dev: 0.2511

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.8327
- Median: 0.8486
- Min: 0.5294
- Max: 0.9909
- Std Dev: 0.1401

**Jaccard Similarity (top 20 words):**
- Mean: 0.5988
- Median: 0.6000
- Min: 0.2903
- Max: 1.0000
- Std Dev: 0.1930

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7405
- Median: 0.8573
- Min: 0.2625
- Max: 0.9406
- Std Dev: 0.2493

**Jaccard Similarity (top 20 words):**
- Mean: 0.4026
- Median: 0.5385
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.2072

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7216
- Median: 0.7571
- Min: 0.4854
- Max: 0.8982
- Std Dev: 0.1603

**Jaccard Similarity (top 20 words):**
- Mean: 0.3712
- Median: 0.3594
- Min: 0.1429
- Max: 0.6000
- Std Dev: 0.1701

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7317
- Median: 0.8657
- Min: 0.2305
- Max: 0.9795
- Std Dev: 0.2819

**Jaccard Similarity (top 20 words):**
- Mean: 0.4465
- Median: 0.4550
- Min: 0.0526
- Max: 0.9048
- Std Dev: 0.2787

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7686
- Median: 0.8466
- Min: 0.2305
- Max: 0.9980
- Std Dev: 0.2031

### Jaccard Similarity (across all matches)
- Mean: 0.4643
- Median: 0.4815
- Min: 0.0526
- Max: 1.0000
- Std Dev: 0.2215
