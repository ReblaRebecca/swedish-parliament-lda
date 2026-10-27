# Seed-Stability Analysis: Period 1994/95–2005/06, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1994/95–2005/06 (3055)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1559.58 | 50 |
| 123 | 1520.21 | 50 |
| 456 | 1512.17 | 50 |
| 789 | 1557.89 | 50 |
| 999 | 1554.99 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 1 |
| 3 of 4 | 4 |
| 2 of 4 | 3 |
| 1 of 4 | 1 |
| 0 of 4 | 2 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | mobbning, våld, barn, arbete, åtgärd, problem, trakasseri, lärare | 3/4 | 0.608 | 0.117 | 0.345 |
| 2 | student, fristående, bidrag, studie, system, ekonomisk, förslag, studerande | 3/4 | 0.766 | 0.519 | 0.495 |
| 3 | kvinna, jämställdhet, forskning, förslag, arbete, samhälle, forskare, forskarutbildning | 1/4 | 0.701 | 0.647 | 0.273 |
| 4 | forskning, universitet, utveckling, svensk, område, verksamhet, land, internationell | 4/4 | 0.874 | 0.762 | 0.398 |
| 5 | gymnasieskola, program, yrkesutbildning, kurs, kunskap, lärlingsutbildning, företag, arbetsliv | 2/4 | 0.770 | 0.566 | 0.458 |
| 6 | region, län, land, göteborg, kommun, specialskola, ekeskola, kompetens | 0/4 | 0.468 | 0.371 | 0.211 |
| 7 | lärare, elev, kunskap, lärarutbildning, pedagogisk, ämne, utveckla, undervisning | 3/4 | 0.754 | 0.598 | 0.453 |
| 8 | stockholm, universitet, linköping, jönköping, södertörn, land, uppsala, norrköping | 0/4 | 0.199 | 0.091 | 0.089 |
| 9 | elev, barn, kommun, förälder, förskola, grundskola, skolverk, fristående | 2/4 | 0.710 | 0.633 | 0.318 |
| 10 | ungdom, barn, hälsa, samhälle, ämne, fysisk, ung, idrott | 2/4 | 0.590 | 0.261 | 0.291 |
| 11 | högskola, student, universitet, forskning, kvalitet, lärosäte, anslag, plats | 3/4 | 0.838 | 0.553 | 0.431 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6931
- Median: 0.7413
- Min: 0.2545
- Max: 0.9332
- Std Dev: 0.2177

**Jaccard Similarity (top 20 words):**
- Mean: 0.3845
- Median: 0.3333
- Min: 0.0811
- Max: 0.7391
- Std Dev: 0.2187

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7102
- Median: 0.8176
- Min: 0.2612
- Max: 0.9622
- Std Dev: 0.2610

**Jaccard Similarity (top 20 words):**
- Mean: 0.3777
- Median: 0.3793
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2057

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6213
- Median: 0.6327
- Min: 0.1175
- Max: 0.9901
- Std Dev: 0.2662

**Jaccard Similarity (top 20 words):**
- Mean: 0.2920
- Median: 0.2500
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1800

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6218
- Median: 0.6498
- Min: 0.0910
- Max: 0.7975
- Std Dev: 0.1949

**Jaccard Similarity (top 20 words):**
- Mean: 0.3138
- Median: 0.3333
- Min: 0.0526
- Max: 0.5385
- Std Dev: 0.1419

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7912
- Median: 0.8894
- Min: 0.2760
- Max: 0.9955
- Std Dev: 0.2348

**Jaccard Similarity (top 20 words):**
- Mean: 0.4074
- Median: 0.4286
- Min: 0.1111
- Max: 0.8182
- Std Dev: 0.2293

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7054
- Median: 0.7942
- Min: 0.2050
- Max: 0.8962
- Std Dev: 0.2109

**Jaccard Similarity (top 20 words):**
- Mean: 0.3703
- Median: 0.3793
- Min: 0.0811
- Max: 0.6667
- Std Dev: 0.1476

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6545
- Median: 0.7608
- Min: 0.0419
- Max: 0.9121
- Std Dev: 0.2736

**Jaccard Similarity (top 20 words):**
- Mean: 0.3704
- Median: 0.3793
- Min: 0.0526
- Max: 0.6000
- Std Dev: 0.1916

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.7354
- Median: 0.7943
- Min: 0.1292
- Max: 0.9437
- Std Dev: 0.2154

**Jaccard Similarity (top 20 words):**
- Mean: 0.3828
- Median: 0.3793
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.1823

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7100
- Median: 0.8839
- Min: 0.0897
- Max: 0.9820
- Std Dev: 0.3114

**Jaccard Similarity (top 20 words):**
- Mean: 0.4298
- Median: 0.4286
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2510

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6359
- Median: 0.7764
- Min: 0.0564
- Max: 0.9911
- Std Dev: 0.3089

**Jaccard Similarity (top 20 words):**
- Mean: 0.3819
- Median: 0.3793
- Min: 0.0526
- Max: 0.8182
- Std Dev: 0.2337

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6879
- Median: 0.7762
- Min: 0.0419
- Max: 0.9955
- Std Dev: 0.2578

### Jaccard Similarity (across all matches)
- Mean: 0.3711
- Median: 0.3793
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2048
