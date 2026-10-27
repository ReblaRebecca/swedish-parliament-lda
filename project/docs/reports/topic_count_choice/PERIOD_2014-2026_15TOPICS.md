# Seed-Stability Analysis: Period 2014/15–2025/26, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2014/15–2025/26 (2477)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1352.41 | 50 |
| 123 | 1421.30 | 50 |
| 456 | 1345.39 | 50 |
| 789 | 1361.28 | 50 |
| 999 | 1382.38 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 4 |
| 2 of 4 | 3 |
| 1 of 4 | 3 |
| 0 of 4 | 2 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | svensk, kunskap, samhälle, undervisning, lära, läroplan, politisk, kultur | 1/4 | 0.589 | 0.471 | 0.226 |
| 2 | barn, stöd, hälsa, psykisk, funktionsnedsättning, ung, fysisk, elevhälsa | 1/4 | 0.435 | 0.127 | 0.174 |
| 3 | högskola, student, lärosäte, universitet, hög, forskning, lärosäten, kvalitet | 3/4 | 0.775 | 0.530 | 0.385 |
| 4 | förslag, lärare, nationell, svensk, stöd, behov, likvärdig, resurs | 4/4 | 0.809 | 0.739 | 0.359 |
| 5 | kvinna, barn, våld, ung, utsatt, arbete, sexuell, flicka | 3/4 | 0.748 | 0.652 | 0.306 |
| 6 | studiemedel, student, anslag, studerande, studie, studiestöd, förslag, fribelopp | 2/4 | 0.612 | 0.017 | 0.440 |
| 7 | kommun, friskola, kommunal, fristående, förskola, konfessionell, barn, skolinspektion | 1/4 | 0.400 | 0.012 | 0.150 |
| 8 | arbetsmarknad, land, behov, hög, jobb, kommun, person, arbete | 4/4 | 0.871 | 0.840 | 0.435 |
| 9 | forskning, nivå, avancerad, grundnivå, högskola, forskarnivå, universitet, anslag | 4/4 | 0.993 | 0.985 | 0.931 |
| 10 | vård, region, läkare, universitet, land, sjuksköterska, läkarutbildning, sjukvård | 2/4 | 0.490 | 0.150 | 0.366 |
| 11 | barn, lärare, förskola, förälder, kommun, pedagogisk, behov, rektor | 2/4 | 0.578 | 0.134 | 0.270 |
| 12 | förskola, barn, personal, verksamhet, språk, svensk, alternativ, slöja | 3/4 | 0.649 | 0.098 | 0.172 |
| 13 | lärare, ämne, gymnasieskola, digital, lärarutbildning, gymnasium, svensk, undervisning | 0/4 | 0.497 | 0.382 | 0.161 |
| 14 | yrkeshögskola, högskola, komvux, arbetsmarknad, regional, behov, vuxenutbildning, kvalitet | 0/4 | 0.146 | 0.029 | 0.062 |
| 15 | forskning, svensk, utveckling, land, innovation, forskare, stärka, satsning | 3/4 | 0.702 | 0.193 | 0.341 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5725
- Median: 0.6449
- Min: 0.0294
- Max: 0.9849
- Std Dev: 0.2971

**Jaccard Similarity (top 20 words):**
- Mean: 0.2998
- Median: 0.2500
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2351

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6906
- Median: 0.7864
- Min: 0.1928
- Max: 0.9978
- Std Dev: 0.2274

**Jaccard Similarity (top 20 words):**
- Mean: 0.3468
- Median: 0.3333
- Min: 0.0256
- Max: 1.0000
- Std Dev: 0.2556

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6371
- Median: 0.7774
- Min: 0.0125
- Max: 0.9972
- Std Dev: 0.2982

**Jaccard Similarity (top 20 words):**
- Mean: 0.3447
- Median: 0.3333
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2559

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5781
- Median: 0.7388
- Min: 0.0174
- Max: 0.9934
- Std Dev: 0.3352

**Jaccard Similarity (top 20 words):**
- Mean: 0.2829
- Median: 0.2500
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2363

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5970
- Median: 0.6477
- Min: 0.0135
- Max: 0.9892
- Std Dev: 0.2914

**Jaccard Similarity (top 20 words):**
- Mean: 0.3464
- Median: 0.2903
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2657

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5638
- Median: 0.5559
- Min: 0.0761
- Max: 0.9850
- Std Dev: 0.3230

**Jaccard Similarity (top 20 words):**
- Mean: 0.2766
- Median: 0.2500
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2211

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5835
- Median: 0.5795
- Min: 0.0106
- Max: 0.9763
- Std Dev: 0.3226

**Jaccard Similarity (top 20 words):**
- Mean: 0.3154
- Median: 0.2500
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2610

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6887
- Median: 0.7596
- Min: 0.0944
- Max: 0.9972
- Std Dev: 0.2830

**Jaccard Similarity (top 20 words):**
- Mean: 0.3863
- Median: 0.3793
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2955

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6412
- Median: 0.7274
- Min: 0.0056
- Max: 0.9924
- Std Dev: 0.3099

**Jaccard Similarity (top 20 words):**
- Mean: 0.3699
- Median: 0.3333
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.3000

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6726
- Median: 0.8280
- Min: 0.0037
- Max: 0.9912
- Std Dev: 0.3329

**Jaccard Similarity (top 20 words):**
- Mean: 0.4066
- Median: 0.3793
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2706

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6225
- Median: 0.7316
- Min: 0.0037
- Max: 0.9978
- Std Dev: 0.3072

### Jaccard Similarity (across all matches)
- Mean: 0.3375
- Median: 0.2903
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2640
