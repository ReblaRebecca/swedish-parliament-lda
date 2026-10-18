# Seed-Stability Analysis: Period 2014/15–2025/26, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2014/15–2025/26 (3572)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1454.54 | 50 |
| 123 | 1477.68 | 50 |
| 456 | 1505.23 | 50 |
| 789 | 1555.87 | 50 |
| 999 | 1476.10 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 2 |
| 3 of 4 | 7 |
| 2 of 4 | 2 |
| 1 of 4 | 0 |
| 0 of 4 | 4 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, pedagogisk, verksamhet, fritidshem, personal, omsorg, förälder | 3/4 | 0.812 | 0.411 | 0.393 |
| 2 | svensk, samhälle, elev, barn, människa, kunskap, läroplan, land | 3/4 | 0.710 | 0.445 | 0.296 |
| 3 | kommun, elev, kommunal, behov, kvalitet, fristående, förutsättning, land | 3/4 | 0.812 | 0.618 | 0.398 |
| 4 | elev, barn, lärare, stöd, nationell, rektor, kunskap, många | 3/4 | 0.821 | 0.684 | 0.288 |
| 5 | arbetsmarknad, företag, elev, jobb, ung, gymnasieskola, gymnasium, många | 3/4 | 0.686 | 0.419 | 0.303 |
| 6 | student, studie, studiemedel, studerande, studera, person, arbeta, fribelopp | 4/4 | 0.902 | 0.795 | 0.607 |
| 7 | forskning, nivå, högskola, avancerad, universitet, grundnivå, forskarnivå, anslag | 4/4 | 0.912 | 0.840 | 0.590 |
| 8 | friskola, konfessionell, religiös, våld, förtryck, hedersrelaterad, flicka, kristen | 0/4 | 0.487 | 0.075 | 0.254 |
| 9 | forskning, högskola, hög, universitet, lärosäte, student, svensk, land | 2/4 | 0.708 | 0.416 | 0.424 |
| 10 | försvar, yrkeshögskola, folkmord, ungdom, barn, totalförsvar, drogtest, seyfo | 0/4 | 0.362 | 0.286 | 0.105 |
| 11 | lärare, elev, ämne, lärarutbildning, undervisning, svensk, årskurs, grundskola | 3/4 | 0.644 | 0.263 | 0.263 |
| 12 | vård, forskning, hälsa, läkare, sjukvård, sjukdom, gammal, medicinsk | 3/4 | 0.756 | 0.628 | 0.395 |
| 13 | kunskap, hållbar, privatekonomi, ekonomisk, ung, många, natur, ämne | 0/4 | 0.361 | 0.184 | 0.115 |
| 14 | barn, kommun, förälder, barnomsorg, språk, kvinna, arbetstid, familj | 2/4 | 0.622 | 0.393 | 0.307 |
| 15 | sexuell, ung, politisk, relation, ungdom, fråga, undervisning, parti | 0/4 | 0.061 | 0.025 | 0.013 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7060
- Median: 0.7223
- Min: 0.1182
- Max: 0.9787
- Std Dev: 0.2263

**Jaccard Similarity (top 20 words):**
- Mean: 0.3872
- Median: 0.3793
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2075

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6244
- Median: 0.7551
- Min: 0.0330
- Max: 0.9553
- Std Dev: 0.3043

**Jaccard Similarity (top 20 words):**
- Mean: 0.2868
- Median: 0.2500
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1973

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5583
- Median: 0.6175
- Min: 0.0249
- Max: 0.9214
- Std Dev: 0.2683

**Jaccard Similarity (top 20 words):**
- Mean: 0.2538
- Median: 0.2500
- Min: 0.0000
- Max: 0.4815
- Std Dev: 0.1516

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6864
- Median: 0.7419
- Min: 0.0660
- Max: 0.9938
- Std Dev: 0.2727

**Jaccard Similarity (top 20 words):**
- Mean: 0.3397
- Median: 0.2903
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2590

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6323
- Median: 0.7106
- Min: 0.0249
- Max: 0.9645
- Std Dev: 0.3324

**Jaccard Similarity (top 20 words):**
- Mean: 0.3243
- Median: 0.2903
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2204

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5736
- Median: 0.5569
- Min: 0.0254
- Max: 0.9449
- Std Dev: 0.2824

**Jaccard Similarity (top 20 words):**
- Mean: 0.2454
- Median: 0.2121
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1518

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6260
- Median: 0.7152
- Min: 0.1268
- Max: 0.9196
- Std Dev: 0.2693

**Jaccard Similarity (top 20 words):**
- Mean: 0.3202
- Median: 0.3333
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1757

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5363
- Median: 0.5527
- Min: 0.0146
- Max: 0.9570
- Std Dev: 0.2473

**Jaccard Similarity (top 20 words):**
- Mean: 0.2604
- Median: 0.2121
- Min: 0.0256
- Max: 0.5385
- Std Dev: 0.1525

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6527
- Median: 0.7237
- Min: 0.0290
- Max: 0.9666
- Std Dev: 0.2522

**Jaccard Similarity (top 20 words):**
- Mean: 0.3176
- Median: 0.2500
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.1985

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5527
- Median: 0.6436
- Min: 0.1306
- Max: 0.8731
- Std Dev: 0.2080

**Jaccard Similarity (top 20 words):**
- Mean: 0.2424
- Median: 0.2500
- Min: 0.0526
- Max: 0.4286
- Std Dev: 0.1257

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6149
- Median: 0.6661
- Min: 0.0146
- Max: 0.9938
- Std Dev: 0.2741

### Jaccard Similarity (across all matches)
- Mean: 0.2978
- Median: 0.2903
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.1933
