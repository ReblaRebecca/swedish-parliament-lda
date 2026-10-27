# Seed-Stability Analysis: Period 2014/15–2025/26, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2014/15–2025/26 (2144)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1347.12 | 50 |
| 123 | 1356.01 | 50 |
| 456 | 1368.76 | 50 |
| 789 | 1353.43 | 50 |
| 999 | 1371.76 | 50 |

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
| 1 | barn, förskola, kommun, verksamhet, behov, kommunal, förälder, pedagogisk | 4/4 | 0.854 | 0.799 | 0.463 |
| 2 | student, studie, studera, studiemedel, arbetsmarknad, studerande, hög, person | 3/4 | 0.761 | 0.543 | 0.368 |
| 3 | forskning, lärosäte, högskola, universitet, hög, forskare, student, kvalitet | 4/4 | 0.912 | 0.873 | 0.572 |
| 4 | lärare, undervisning, ämne, svensk, nationell, betyg, grundskola, kunskap | 3/4 | 0.733 | 0.465 | 0.421 |
| 5 | land, hög, svensk, företag, stärka, utveckling, arbetsmarknad, samhälle | 0/4 | 0.483 | 0.213 | 0.169 |
| 6 | barn, kvinna, samhälle, kunskap, svensk, ung, rättighet, människa | 3/4 | 0.795 | 0.547 | 0.510 |
| 7 | barn, lärare, stöd, rektor, skolinspektion, behov, arbete, undervisning | 3/4 | 0.618 | 0.299 | 0.263 |
| 8 | forskning, nivå, avancerad, grundnivå, högskola, forskarnivå, universitet, anslag | 4/4 | 0.988 | 0.960 | 0.852 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7886
- Median: 0.7920
- Min: 0.5469
- Max: 0.9961
- Std Dev: 0.1473

**Jaccard Similarity (top 20 words):**
- Mean: 0.4932
- Median: 0.4835
- Min: 0.2500
- Max: 0.9048
- Std Dev: 0.2013

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7716
- Median: 0.8222
- Min: 0.4485
- Max: 0.9965
- Std Dev: 0.1782

**Jaccard Similarity (top 20 words):**
- Mean: 0.4836
- Median: 0.4835
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2648

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7857
- Median: 0.8718
- Min: 0.2986
- Max: 0.9982
- Std Dev: 0.2115

**Jaccard Similarity (top 20 words):**
- Mean: 0.4746
- Median: 0.4550
- Min: 0.0526
- Max: 1.0000
- Std Dev: 0.2638

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7259
- Median: 0.8293
- Min: 0.2134
- Max: 0.9597
- Std Dev: 0.2419

**Jaccard Similarity (top 20 words):**
- Mean: 0.3577
- Median: 0.3348
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.1785

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7348
- Median: 0.7543
- Min: 0.3064
- Max: 0.9985
- Std Dev: 0.2214

**Jaccard Similarity (top 20 words):**
- Mean: 0.4112
- Median: 0.3118
- Min: 0.0526
- Max: 1.0000
- Std Dev: 0.3027

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7408
- Median: 0.7984
- Min: 0.1878
- Max: 0.9947
- Std Dev: 0.2402

**Jaccard Similarity (top 20 words):**
- Mean: 0.4398
- Median: 0.3657
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2706

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7828
- Median: 0.8837
- Min: 0.4117
- Max: 0.9965
- Std Dev: 0.2091

**Jaccard Similarity (top 20 words):**
- Mean: 0.4234
- Median: 0.3793
- Min: 0.1429
- Max: 0.8182
- Std Dev: 0.2195

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7454
- Median: 0.8084
- Min: 0.4288
- Max: 0.9956
- Std Dev: 0.1927

**Jaccard Similarity (top 20 words):**
- Mean: 0.3867
- Median: 0.3147
- Min: 0.0811
- Max: 0.9048
- Std Dev: 0.2853

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7643
- Median: 0.9274
- Min: 0.2187
- Max: 0.9745
- Std Dev: 0.2963

**Jaccard Similarity (top 20 words):**
- Mean: 0.4848
- Median: 0.5692
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2663

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6927
- Median: 0.7794
- Min: 0.0899
- Max: 0.9753
- Std Dev: 0.2894

**Jaccard Similarity (top 20 words):**
- Mean: 0.3825
- Median: 0.3118
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2685

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7533
- Median: 0.8294
- Min: 0.0899
- Max: 0.9985
- Std Dev: 0.2290

### Jaccard Similarity (across all matches)
- Mean: 0.4337
- Median: 0.3793
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2591
