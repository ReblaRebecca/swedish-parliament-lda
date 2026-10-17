# Seed-Stability Analysis: Period 2015-2025, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of 2015-2025 (3257)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1565.04 | 50 |
| 123 | 1523.87 | 50 |
| 456 | 1547.77 | 50 |
| 789 | 1550.13 | 50 |
| 999 | 1524.68 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 0 |
| 2 of 4 | 0 |
| 1 of 4 | 1 |
| 0 of 4 | 2 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | student, hög, arbetsmarknad, behov, kommun, studie, öka, land | 4/4 | 0.866 | 0.802 | 0.433 |
| 2 | elev, barn, ung, stöd, hälsa, behov, psykisk, ungdom | 0/4 | 0.615 | 0.464 | 0.256 |
| 3 | våld, friskola, elev, konfessionell, kvinna, undervisning, skolinspektion, samhälle | 1/4 | 0.683 | 0.565 | 0.324 |
| 4 | land, högskola, svensk, utveckling, forskning, universitet, hög, utveckla | 4/4 | 0.786 | 0.724 | 0.368 |
| 5 | forskning, högskola, universitet, nivå, avancerad, grundnivå, anslag, forskarnivå | 4/4 | 0.922 | 0.896 | 0.608 |
| 6 | barn, förskola, kommun, förälder, verksamhet, svensk, pedagogisk, personal | 4/4 | 0.867 | 0.772 | 0.445 |
| 7 | kunskap, ämne, elev, lära, samhälle, barn, djur, många | 0/4 | 0.372 | 0.205 | 0.124 |
| 8 | elev, lärare, undervisning, svensk, kunskap, nationell, grundskola, rektor | 4/4 | 0.967 | 0.925 | 0.657 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7923
- Median: 0.8404
- Min: 0.5650
- Max: 0.9849
- Std Dev: 0.1538

**Jaccard Similarity (top 20 words):**
- Mean: 0.4022
- Median: 0.3793
- Min: 0.1429
- Max: 0.7391
- Std Dev: 0.1821

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7104
- Median: 0.7870
- Min: 0.2971
- Max: 0.9252
- Std Dev: 0.2060

**Jaccard Similarity (top 20 words):**
- Mean: 0.3744
- Median: 0.3793
- Min: 0.1111
- Max: 0.5385
- Std Dev: 0.1265

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7727
- Median: 0.8466
- Min: 0.2048
- Max: 0.9833
- Std Dev: 0.2446

**Jaccard Similarity (top 20 words):**
- Mean: 0.4377
- Median: 0.4039
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2396

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7637
- Median: 0.7947
- Min: 0.3896
- Max: 0.9793
- Std Dev: 0.1727

**Jaccard Similarity (top 20 words):**
- Mean: 0.3934
- Median: 0.3563
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.1628

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7874
- Median: 0.8236
- Min: 0.3520
- Max: 0.9874
- Std Dev: 0.1983

**Jaccard Similarity (top 20 words):**
- Mean: 0.4804
- Median: 0.4359
- Min: 0.1111
- Max: 0.8182
- Std Dev: 0.2402

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7337
- Median: 0.7506
- Min: 0.2394
- Max: 0.9642
- Std Dev: 0.2209

**Jaccard Similarity (top 20 words):**
- Mean: 0.3634
- Median: 0.3810
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.1991

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7863
- Median: 0.9016
- Min: 0.1815
- Max: 0.9918
- Std Dev: 0.2587

**Jaccard Similarity (top 20 words):**
- Mean: 0.4918
- Median: 0.4550
- Min: 0.0526
- Max: 0.9048
- Std Dev: 0.2872

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6990
- Median: 0.7647
- Min: 0.2767
- Max: 0.9574
- Std Dev: 0.2397

**Jaccard Similarity (top 20 words):**
- Mean: 0.3683
- Median: 0.3810
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2350

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7615
- Median: 0.8960
- Min: 0.3463
- Max: 0.9844
- Std Dev: 0.2466

**Jaccard Similarity (top 20 words):**
- Mean: 0.5149
- Median: 0.5839
- Min: 0.1429
- Max: 0.8182
- Std Dev: 0.2782

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7626
- Median: 0.7402
- Min: 0.4732
- Max: 0.9664
- Std Dev: 0.1553

**Jaccard Similarity (top 20 words):**
- Mean: 0.3840
- Median: 0.3118
- Min: 0.1765
- Max: 0.6667
- Std Dev: 0.1791

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7570
- Median: 0.8046
- Min: 0.1815
- Max: 0.9918
- Std Dev: 0.2151

### Jaccard Similarity (across all matches)
- Mean: 0.4210
- Median: 0.3793
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2249
