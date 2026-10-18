# Seed-Stability Analysis: Period 1994/95–2005/06, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3477)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1640.14 | 50 |
| 123 | 1616.32 | 50 |
| 456 | 1651.68 | 50 |
| 789 | 1616.99 | 50 |
| 999 | 1640.49 | 50 |

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
| 1 | hälsa, fysisk, barn, ungdom, idrott, ämne, aktivitet, elev | 2/4 | 0.740 | 0.561 | 0.410 |
| 2 | högskola, universitet, hög, land, utveckling, forskning, student, region | 4/4 | 0.935 | 0.911 | 0.457 |
| 3 | elev, barn, kommun, förskola, förälder, fristående, grundskola, kommunal | 4/4 | 0.848 | 0.807 | 0.525 |
| 4 | lärare, elev, kunskap, gymnasieskola, program, många, lärarutbildning, hög | 3/4 | 0.769 | 0.589 | 0.449 |
| 5 | forskning, högskola, universitet, anslag, forskarutbildning, kvalitet, hög, grundutbildning | 3/4 | 0.847 | 0.693 | 0.431 |
| 6 | barn, mobbning, elev, arbete, förälder, problem, ungdom, funktionshind | 3/4 | 0.763 | 0.575 | 0.342 |
| 7 | svensk, utveckling, verksamhet, forskning, universitet, behov, samhälle, område | 1/4 | 0.503 | 0.249 | 0.208 |
| 8 | kvinna, jämställdhet, sexuell, diskriminering, flicka, samhälle, kön, pojke | 2/4 | 0.643 | 0.240 | 0.340 |
| 9 | student, hög, studie, system, studerande, ekonomisk, enskild, studera | 3/4 | 0.866 | 0.614 | 0.595 |
| 10 | språk, tv, bok, råd, bibliotek, skolbibliotek, svensk, folkhögskola | 0/4 | 0.278 | 0.080 | 0.130 |
| 11 | företag, län, körkort, kalmar, mitthögskolan, ungdom, mitthögskola, område | 0/4 | 0.374 | 0.139 | 0.193 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7678
- Median: 0.8809
- Min: 0.1389
- Max: 0.9876
- Std Dev: 0.2544

**Jaccard Similarity (top 20 words):**
- Mean: 0.5015
- Median: 0.5385
- Min: 0.1111
- Max: 0.8182
- Std Dev: 0.1851

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6581
- Median: 0.7571
- Min: 0.1266
- Max: 0.9236
- Std Dev: 0.2243

**Jaccard Similarity (top 20 words):**
- Mean: 0.3010
- Median: 0.2903
- Min: 0.0526
- Max: 0.4815
- Std Dev: 0.1341

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6263
- Median: 0.7369
- Min: 0.0803
- Max: 0.9106
- Std Dev: 0.2839

**Jaccard Similarity (top 20 words):**
- Mean: 0.3253
- Median: 0.4286
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.2117

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6997
- Median: 0.6228
- Min: 0.2491
- Max: 0.9689
- Std Dev: 0.2331

**Jaccard Similarity (top 20 words):**
- Mean: 0.3561
- Median: 0.2903
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2347

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6704
- Median: 0.7847
- Min: 0.1917
- Max: 0.9719
- Std Dev: 0.2913

**Jaccard Similarity (top 20 words):**
- Mean: 0.3895
- Median: 0.4286
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2160

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6854
- Median: 0.7504
- Min: 0.0349
- Max: 0.9538
- Std Dev: 0.2652

**Jaccard Similarity (top 20 words):**
- Mean: 0.3708
- Median: 0.3333
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2088

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6620
- Median: 0.7315
- Min: 0.1428
- Max: 0.9735
- Std Dev: 0.2753

**Jaccard Similarity (top 20 words):**
- Mean: 0.3936
- Median: 0.3333
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2678

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6277
- Median: 0.7194
- Min: 0.0159
- Max: 0.9267
- Std Dev: 0.2858

**Jaccard Similarity (top 20 words):**
- Mean: 0.2846
- Median: 0.3333
- Min: 0.0000
- Max: 0.4815
- Std Dev: 0.1392

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6644
- Median: 0.7118
- Min: 0.1595
- Max: 0.9372
- Std Dev: 0.2280

**Jaccard Similarity (top 20 words):**
- Mean: 0.3330
- Median: 0.3333
- Min: 0.0811
- Max: 0.6000
- Std Dev: 0.1449

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6549
- Median: 0.7314
- Min: 0.0237
- Max: 0.9469
- Std Dev: 0.2666

**Jaccard Similarity (top 20 words):**
- Mean: 0.3444
- Median: 0.3333
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2155

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6717
- Median: 0.7537
- Min: 0.0159
- Max: 0.9876
- Std Dev: 0.2647

### Jaccard Similarity (across all matches)
- Mean: 0.3600
- Median: 0.3333
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2084
