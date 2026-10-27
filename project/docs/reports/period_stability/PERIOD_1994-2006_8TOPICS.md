# Seed-Stability Analysis: Period 1994/95–2005/06, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3055)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1569.22 | 50 |
| 123 | 1559.63 | 50 |
| 456 | 1565.93 | 50 |
| 789 | 1558.92 | 50 |
| 999 | 1597.90 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 2 |
| 2 of 4 | 1 |
| 1 of 4 | 2 |
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | student, förslag, studie, system, studerande, bidrag, högskola, studera | 4/4 | 0.898 | 0.824 | 0.511 |
| 2 | elev, kommun, fristående, lärare, grundskola, skolverk, gymnasieskola, betyg | 3/4 | 0.809 | 0.659 | 0.410 |
| 3 | barn, förskola, mobbning, förälder, elev, arbete, kommun, samhälle | 4/4 | 0.857 | 0.806 | 0.375 |
| 4 | forskning, universitet, högskola, svensk, forskarutbildning, anslag, utveckling, forskare | 3/4 | 0.738 | 0.191 | 0.478 |
| 5 | gymnasieskola, kunskap, yrkesutbildning, företag, lärlingsutbildning, ungdom, program, arbetsliv | 1/4 | 0.622 | 0.370 | 0.374 |
| 6 | barn, funktionshind, språk, särskola, specialskola, ekeskola, undervisning, invandrare | 2/4 | 0.714 | 0.617 | 0.277 |
| 7 | lärare, högskola, student, lärarutbildning, kvalitet, kunskap, pedagogisk, lärosäte | 1/4 | 0.512 | 0.318 | 0.234 |
| 8 | högskola, universitet, forskning, region, land, utveckling, plats, område | 4/4 | 0.915 | 0.837 | 0.585 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.8193
- Median: 0.8744
- Min: 0.4797
- Max: 0.9682
- Std Dev: 0.1593

**Jaccard Similarity (top 20 words):**
- Mean: 0.4905
- Median: 0.5407
- Min: 0.2121
- Max: 0.8182
- Std Dev: 0.2068

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7970
- Median: 0.8681
- Min: 0.5338
- Max: 0.9840
- Std Dev: 0.1749

**Jaccard Similarity (top 20 words):**
- Mean: 0.4529
- Median: 0.4039
- Min: 0.2903
- Max: 0.7391
- Std Dev: 0.1659

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8045
- Median: 0.8560
- Min: 0.3700
- Max: 0.9711
- Std Dev: 0.1850

**Jaccard Similarity (top 20 words):**
- Mean: 0.4523
- Median: 0.4144
- Min: 0.1765
- Max: 0.7391
- Std Dev: 0.2095

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6116
- Median: 0.6612
- Min: 0.1909
- Max: 0.8367
- Std Dev: 0.2253

**Jaccard Similarity (top 20 words):**
- Mean: 0.2269
- Median: 0.2121
- Min: 0.0256
- Max: 0.3793
- Std Dev: 0.1098

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7954
- Median: 0.8649
- Min: 0.4475
- Max: 0.9819
- Std Dev: 0.1812

**Jaccard Similarity (top 20 words):**
- Mean: 0.4733
- Median: 0.4286
- Min: 0.2500
- Max: 0.8182
- Std Dev: 0.1727

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8333
- Median: 0.9021
- Min: 0.5497
- Max: 0.9765
- Std Dev: 0.1545

**Jaccard Similarity (top 20 words):**
- Mean: 0.4857
- Median: 0.4550
- Min: 0.2121
- Max: 0.8182
- Std Dev: 0.1915

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7370
- Median: 0.7943
- Min: 0.2794
- Max: 0.9604
- Std Dev: 0.2036

**Jaccard Similarity (top 20 words):**
- Mean: 0.3863
- Median: 0.4550
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1714

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8317
- Median: 0.8376
- Min: 0.5623
- Max: 0.9851
- Std Dev: 0.1247

**Jaccard Similarity (top 20 words):**
- Mean: 0.4957
- Median: 0.4304
- Min: 0.1765
- Max: 0.9048
- Std Dev: 0.2521

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7224
- Median: 0.8083
- Min: 0.1796
- Max: 0.9572
- Std Dev: 0.2512

**Jaccard Similarity (top 20 words):**
- Mean: 0.3948
- Median: 0.3810
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2299

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6924
- Median: 0.7262
- Min: 0.1994
- Max: 0.9557
- Std Dev: 0.2292

**Jaccard Similarity (top 20 words):**
- Mean: 0.3815
- Median: 0.3793
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2245

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7645
- Median: 0.8236
- Min: 0.1796
- Max: 0.9851
- Std Dev: 0.2043

### Jaccard Similarity (across all matches)
- Mean: 0.4240
- Median: 0.4039
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2120
