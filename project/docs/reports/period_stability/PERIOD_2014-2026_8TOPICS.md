# Seed-Stability Analysis: Period 2014/15–2025/26, 8 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2014/15–2025/26 (2477)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 8 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1403.31 | 50 |
| 123 | 1411.73 | 50 |
| 456 | 1419.46 | 50 |
| 789 | 1399.16 | 50 |
| 999 | 1493.03 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 3 |
| 2 of 4 | 0 |
| 1 of 4 | 2 |
| 0 of 4 | 0 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | kunskap, samhälle, svensk, ung, språk, lära, ämne, människa | 1/4 | 0.557 | 0.274 | 0.254 |
| 2 | barn, förälder, ung, stöd, hälsa, psykisk, fysisk, behov | 4/4 | 0.836 | 0.751 | 0.258 |
| 3 | forskning, högskola, lärosäte, hög, universitet, svensk, land, forskare | 4/4 | 0.975 | 0.928 | 0.842 |
| 4 | lärare, undervisning, svensk, nationell, grundskola, rektor, kunskap, betyg | 3/4 | 0.738 | 0.204 | 0.491 |
| 5 | kvinna, barn, våld, flicka, utsatt, arbete, konfessionell, sexuell | 1/4 | 0.455 | 0.150 | 0.101 |
| 6 | forskning, nivå, avancerad, grundnivå, högskola, forskarnivå, universitet, anslag | 3/4 | 0.917 | 0.698 | 0.710 |
| 7 | förskola, kommun, barn, verksamhet, kommunal, fristående, pedagogisk, förslag | 3/4 | 0.695 | 0.173 | 0.508 |
| 8 | arbetsmarknad, student, hög, behov, studie, jobb, land, studera | 4/4 | 0.866 | 0.834 | 0.497 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.8001
- Median: 0.8702
- Min: 0.2744
- Max: 0.9970
- Std Dev: 0.2201

**Jaccard Similarity (top 20 words):**
- Mean: 0.4944
- Median: 0.5741
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.3177

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7366
- Median: 0.8712
- Min: 0.1727
- Max: 0.9889
- Std Dev: 0.3037

**Jaccard Similarity (top 20 words):**
- Mean: 0.4266
- Median: 0.4286
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2857

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8112
- Median: 0.9109
- Min: 0.1503
- Max: 0.9939
- Std Dev: 0.2676

**Jaccard Similarity (top 20 words):**
- Mean: 0.5696
- Median: 0.6388
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2858

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6718
- Median: 0.7400
- Min: 0.2045
- Max: 0.9279
- Std Dev: 0.2233

**Jaccard Similarity (top 20 words):**
- Mean: 0.3396
- Median: 0.2779
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2468

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.8355
- Median: 0.9175
- Min: 0.2740
- Max: 0.9846
- Std Dev: 0.2186

**Jaccard Similarity (top 20 words):**
- Mean: 0.5174
- Median: 0.5143
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2401

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8935
- Median: 0.9142
- Min: 0.7670
- Max: 0.9932
- Std Dev: 0.0872

**Jaccard Similarity (top 20 words):**
- Mean: 0.6172
- Median: 0.7391
- Min: 0.2121
- Max: 0.8182
- Std Dev: 0.2169

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7276
- Median: 0.7476
- Min: 0.4676
- Max: 0.9365
- Std Dev: 0.1773

**Jaccard Similarity (top 20 words):**
- Mean: 0.3318
- Median: 0.2702
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2129

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.8111
- Median: 0.8583
- Min: 0.4333
- Max: 0.9863
- Std Dev: 0.1925

**Jaccard Similarity (top 20 words):**
- Mean: 0.5249
- Median: 0.4589
- Min: 0.1111
- Max: 0.9048
- Std Dev: 0.2752

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7117
- Median: 0.7717
- Min: 0.2573
- Max: 0.9291
- Std Dev: 0.2208

**Jaccard Similarity (top 20 words):**
- Mean: 0.3435
- Median: 0.2917
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.1938

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6707
- Median: 0.6880
- Min: 0.4701
- Max: 0.8835
- Std Dev: 0.1211

**Jaccard Similarity (top 20 words):**
- Mean: 0.2692
- Median: 0.2311
- Min: 0.1429
- Max: 0.6000
- Std Dev: 0.1441

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 80

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.7670
- Median: 0.8366
- Min: 0.1503
- Max: 0.9970
- Std Dev: 0.2234

### Jaccard Similarity (across all matches)
- Mean: 0.4434
- Median: 0.4039
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2709
