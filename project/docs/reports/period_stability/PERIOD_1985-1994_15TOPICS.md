# Seed-Stability Analysis: Period 1985/86–1993/94, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 1985/86–1993/94 (4025)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1775.73 | 50 |
| 123 | 1796.53 | 50 |
| 456 | 1797.44 | 50 |
| 789 | 1758.73 | 50 |
| 999 | 1765.40 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 2 |
| 3 of 4 | 2 |
| 2 of 4 | 3 |
| 1 of 4 | 3 |
| 0 of 4 | 5 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | huddinge, novum, helårsstudent, superdator, särvux, mitthögskola, mälardalens, samvetsklausul | 0/4 | 0.104 | 0.024 | 0.099 |
| 2 | anslag, gymnasieskola, bidrag, vuxenutbildning, särskild, verksamhet, budgetår, hög | 3/4 | 0.809 | 0.607 | 0.511 |
| 3 | elev, ämne, undervisning, grundskola, lärare, betyg, läroplan, förälder | 3/4 | 0.795 | 0.564 | 0.420 |
| 4 | elev, kommun, barn, lärare, många, ansvar, behov, kunskap | 1/4 | 0.631 | 0.474 | 0.225 |
| 5 | umeå, universitet, norrland, turism, läkare, finsk, läkarutbildning, norra | 0/4 | 0.317 | 0.083 | 0.131 |
| 6 | hälsa, kunskap, idrott, vård, ämne, medicinsk, människa, hemkunskap | 2/4 | 0.628 | 0.371 | 0.313 |
| 7 | lärare, poäng, lärarutbildning, plats, behov, studerande, universitet, tjänst | 1/4 | 0.641 | 0.587 | 0.240 |
| 8 | invandrare, svensk, undervisning, sfi, svenska, kommun, svenskundervisning, flykting | 2/4 | 0.662 | 0.370 | 0.305 |
| 9 | högskola, län, teknisk, region, utveckling, hög, behov, stockholm | 4/4 | 0.948 | 0.896 | 0.642 |
| 10 | fred, internationell, rättighet, mänsklig, handikappforskning, konflikt, säkerhetspolitisk, konfliktforskning | 0/4 | 0.161 | 0.005 | 0.096 |
| 11 | miljö, malmö, lund, ekologisk, södra, skåne, natur, skogsbruk | 0/4 | 0.226 | 0.139 | 0.068 |
| 12 | göteborg, statlig, kommun, stockholm, stat, statsbidrag, verksamhet, trädgård | 1/4 | 0.351 | 0.087 | 0.156 |
| 13 | forskning, högskola, universitet, område, verksamhet, resurs, utveckling, svensk | 4/4 | 0.926 | 0.835 | 0.662 |
| 14 | språk, elev, ämne, kunskap, gymnasieskola, barn, svensk, land | 2/4 | 0.634 | 0.475 | 0.275 |
| 15 | musikhögskola, facklig, cmf, miljövetenskaplig, klädformgivning, kulturvård, toxikologi, förnyelsefond | 0/4 | 0.042 | 0.010 | 0.033 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5153
- Median: 0.6008
- Min: 0.0113
- Max: 0.8956
- Std Dev: 0.3225

**Jaccard Similarity (top 20 words):**
- Mean: 0.2542
- Median: 0.3333
- Min: 0.0256
- Max: 0.5385
- Std Dev: 0.1746

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5356
- Median: 0.6120
- Min: 0.0047
- Max: 0.9628
- Std Dev: 0.3226

**Jaccard Similarity (top 20 words):**
- Mean: 0.3006
- Median: 0.2903
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2140

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5322
- Median: 0.5981
- Min: 0.0102
- Max: 0.9808
- Std Dev: 0.3325

**Jaccard Similarity (top 20 words):**
- Mean: 0.2937
- Median: 0.1765
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2547

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5167
- Median: 0.4737
- Min: 0.0057
- Max: 0.9698
- Std Dev: 0.3205

**Jaccard Similarity (top 20 words):**
- Mean: 0.2652
- Median: 0.2121
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2202

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5706
- Median: 0.7127
- Min: 0.0139
- Max: 0.9118
- Std Dev: 0.3097

**Jaccard Similarity (top 20 words):**
- Mean: 0.2528
- Median: 0.1765
- Min: 0.0256
- Max: 0.5385
- Std Dev: 0.1915

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5859
- Median: 0.6821
- Min: 0.0015
- Max: 0.9242
- Std Dev: 0.3191

**Jaccard Similarity (top 20 words):**
- Mean: 0.3226
- Median: 0.3333
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2099

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5519
- Median: 0.6680
- Min: 0.0012
- Max: 0.9491
- Std Dev: 0.3029

**Jaccard Similarity (top 20 words):**
- Mean: 0.2453
- Median: 0.2903
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1792

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6394
- Median: 0.7449
- Min: 0.0147
- Max: 0.9783
- Std Dev: 0.3164

**Jaccard Similarity (top 20 words):**
- Mean: 0.3814
- Median: 0.3793
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2343

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5138
- Median: 0.5191
- Min: 0.0289
- Max: 0.9639
- Std Dev: 0.3067

**Jaccard Similarity (top 20 words):**
- Mean: 0.2694
- Median: 0.2121
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2042

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5482
- Median: 0.5143
- Min: 0.0032
- Max: 0.9673
- Std Dev: 0.3632

**Jaccard Similarity (top 20 words):**
- Mean: 0.3284
- Median: 0.1765
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2797

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5510
- Median: 0.6330
- Min: 0.0012
- Max: 0.9808
- Std Dev: 0.3242

### Jaccard Similarity (across all matches)
- Mean: 0.2914
- Median: 0.2500
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2223
