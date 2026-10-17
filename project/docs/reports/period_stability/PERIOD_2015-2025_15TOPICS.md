# Seed-Stability Analysis: Period 2015-2025, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of 2015-2025 (3257)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1475.47 | 50 |
| 123 | 1514.67 | 50 |
| 456 | 1480.24 | 50 |
| 789 | 1480.88 | 50 |
| 999 | 1473.91 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 3 |
| 2 of 4 | 3 |
| 1 of 4 | 1 |
| 0 of 4 | 5 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | student, arbetsmarknad, studie, hög, person, studera, arbete, många | 3/4 | 0.756 | 0.693 | 0.290 |
| 2 | ung, elev, barn, ungdom, företag, hälsa, psykisk, kunskap | 2/4 | 0.694 | 0.567 | 0.305 |
| 3 | estetisk, drogtest, konkurrens, prao, drog, elev, arbetsplats, konst | 0/4 | 0.158 | 0.055 | 0.046 |
| 4 | privatekonomi, djurförsök, folkmord, metod, språk, ekonomi, seyfo, ekonomisk | 0/4 | 0.400 | 0.380 | 0.177 |
| 5 | forskning, forskare, kvinna, anslag, svensk, mål, samhälle, område | 1/4 | 0.564 | 0.441 | 0.170 |
| 6 | svensk, samhälle, språk, barn, kultur, politisk, människa, elev | 2/4 | 0.709 | 0.486 | 0.276 |
| 7 | försvar, djur, fjärrundervisning, medborgare, totalförsvar, teckenspråk, militär, samhällsviktig | 0/4 | 0.301 | 0.244 | 0.093 |
| 8 | elev, lärare, kunskap, svensk, undervisning, nationell, betyg, grundskola | 4/4 | 0.924 | 0.867 | 0.532 |
| 9 | forskning, nivå, avancerad, grundnivå, högskola, forskarnivå, universitet, anslag | 4/4 | 0.879 | 0.831 | 0.513 |
| 10 | barnomsorg, kommun, arbetstid, obekväm, förälder, kvinna, erbjuda, hög | 0/4 | 0.323 | 0.078 | 0.135 |
| 11 | högskola, hög, forskning, lärosäte, land, universitet, svensk, kvalitet | 3/4 | 0.747 | 0.676 | 0.380 |
| 12 | förskola, barn, pedagogisk, svensk, personal, verksamhet, god, mat | 4/4 | 0.837 | 0.701 | 0.241 |
| 13 | sfi, våld, vuxenutbildning, friskola, undervisning, komvux, förtryck, hedersrelaterad | 0/4 | 0.331 | 0.267 | 0.162 |
| 14 | vård, läkare, gammal, brist, patient, region, sjukvård, behov | 2/4 | 0.578 | 0.142 | 0.301 |
| 15 | barn, elev, kommun, förskola, förälder, stöd, behov, verksamhet | 3/4 | 0.783 | 0.677 | 0.285 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5750
- Median: 0.6927
- Min: 0.0548
- Max: 0.9017
- Std Dev: 0.2695

**Jaccard Similarity (top 20 words):**
- Mean: 0.2422
- Median: 0.2500
- Min: 0.0256
- Max: 0.4815
- Std Dev: 0.1373

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5829
- Median: 0.6729
- Min: 0.0698
- Max: 0.9301
- Std Dev: 0.2762

**Jaccard Similarity (top 20 words):**
- Mean: 0.2585
- Median: 0.2500
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.1653

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6570
- Median: 0.7114
- Min: 0.1413
- Max: 0.9586
- Std Dev: 0.2261

**Jaccard Similarity (top 20 words):**
- Mean: 0.2877
- Median: 0.2903
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.1214

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5811
- Median: 0.5669
- Min: 0.1417
- Max: 0.9701
- Std Dev: 0.2755

**Jaccard Similarity (top 20 words):**
- Mean: 0.2529
- Median: 0.1765
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2167

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6033
- Median: 0.6270
- Min: 0.0136
- Max: 0.9077
- Std Dev: 0.2508

**Jaccard Similarity (top 20 words):**
- Mean: 0.2908
- Median: 0.2500
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1681

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6128
- Median: 0.6635
- Min: 0.0151
- Max: 0.9810
- Std Dev: 0.2501

**Jaccard Similarity (top 20 words):**
- Mean: 0.3089
- Median: 0.2903
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2152

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6165
- Median: 0.7172
- Min: 0.0432
- Max: 0.9571
- Std Dev: 0.2632

**Jaccard Similarity (top 20 words):**
- Mean: 0.2924
- Median: 0.3333
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1649

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6104
- Median: 0.6786
- Min: 0.1552
- Max: 0.9440
- Std Dev: 0.2805

**Jaccard Similarity (top 20 words):**
- Mean: 0.3147
- Median: 0.2903
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.1846

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6585
- Median: 0.6820
- Min: 0.1727
- Max: 0.9232
- Std Dev: 0.2367

**Jaccard Similarity (top 20 words):**
- Mean: 0.3402
- Median: 0.3333
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2229

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6362
- Median: 0.6725
- Min: 0.1792
- Max: 0.9862
- Std Dev: 0.2699

**Jaccard Similarity (top 20 words):**
- Mean: 0.3300
- Median: 0.2903
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2211

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6134
- Median: 0.6764
- Min: 0.0136
- Max: 0.9862
- Std Dev: 0.2620

### Jaccard Similarity (across all matches)
- Mean: 0.2918
- Median: 0.2903
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.1876
