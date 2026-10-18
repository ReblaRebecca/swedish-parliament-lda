# Seed-Stability Analysis: Period 2006/07–2013/14, 11 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2006/07–2013/14 (2879)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 11 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1567.82 | 50 |
| 123 | 1551.98 | 50 |
| 456 | 1545.95 | 50 |
| 789 | 1585.12 | 50 |
| 999 | 1547.33 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 1 |
| 2 of 4 | 3 |
| 1 of 4 | 0 |
| 0 of 4 | 4 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, ungdom, förälder, fysisk, många, personal, aktivitet | 3/4 | 0.866 | 0.684 | 0.455 |
| 2 | elev, kunskap, gymnasieskola, behov, hög, program, vuxenutbildning, ungdom | 2/4 | 0.742 | 0.604 | 0.354 |
| 3 | elev, kommun, barn, fristående, kommunal, förälder, skollag, behov | 4/4 | 0.837 | 0.743 | 0.428 |
| 4 | lärare, kunskap, elev, undervisning, samhälle, människa, kvinna, svensk | 4/4 | 0.774 | 0.723 | 0.329 |
| 5 | forskning, högskola, universitet, utveckling, hög, svensk, företag, land | 2/4 | 0.686 | 0.373 | 0.370 |
| 6 | it, lärare, tillgång, skolbibliotek, använda, digital, svensk, elev | 0/4 | 0.327 | 0.257 | 0.096 |
| 7 | språk, läkare, svensk, land, behov, vård, sfi, läkarutbildning | 0/4 | 0.615 | 0.536 | 0.353 |
| 8 | forskning, högskola, universitet, lärosäte, kvalitet, forskarutbildning, medel, anslag | 2/4 | 0.650 | 0.366 | 0.143 |
| 9 | student, studie, högskola, hög, studera, studiemedel, ekonomisk, lite | 4/4 | 0.968 | 0.960 | 0.711 |
| 10 | gammal, läkemedel, punktskrift, klinisk, person, geriatrisk, schack, synskadad | 0/4 | 0.394 | 0.269 | 0.187 |
| 11 | funktionsnedsättning, hållbar, utomhuspedagogik, lärande, förståelse, assistent, funktionshind, natur | 0/4 | 0.172 | 0.095 | 0.062 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6298
- Median: 0.7234
- Min: 0.2686
- Max: 0.9645
- Std Dev: 0.2610

**Jaccard Similarity (top 20 words):**
- Mean: 0.3057
- Median: 0.3333
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2055

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6755
- Median: 0.6558
- Min: 0.0947
- Max: 0.9720
- Std Dev: 0.2627

**Jaccard Similarity (top 20 words):**
- Mean: 0.2975
- Median: 0.2500
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1866

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6098
- Median: 0.6568
- Min: 0.1992
- Max: 0.9597
- Std Dev: 0.2481

**Jaccard Similarity (top 20 words):**
- Mean: 0.2954
- Median: 0.2500
- Min: 0.1111
- Max: 0.6000
- Std Dev: 0.1653

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6419
- Median: 0.6840
- Min: 0.1154
- Max: 0.9788
- Std Dev: 0.2686

**Jaccard Similarity (top 20 words):**
- Mean: 0.3700
- Median: 0.3333
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2678

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6896
- Median: 0.7273
- Min: 0.1114
- Max: 0.9858
- Std Dev: 0.2447

**Jaccard Similarity (top 20 words):**
- Mean: 0.3938
- Median: 0.3793
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2382

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6135
- Median: 0.5599
- Min: 0.2434
- Max: 0.9850
- Std Dev: 0.2898

**Jaccard Similarity (top 20 words):**
- Mean: 0.3373
- Median: 0.1765
- Min: 0.0526
- Max: 0.7391
- Std Dev: 0.2581

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6221
- Median: 0.6262
- Min: 0.1406
- Max: 0.9770
- Std Dev: 0.2379

**Jaccard Similarity (top 20 words):**
- Mean: 0.3370
- Median: 0.2903
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2301

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6797
- Median: 0.8039
- Min: 0.1726
- Max: 0.9860
- Std Dev: 0.2780

**Jaccard Similarity (top 20 words):**
- Mean: 0.3733
- Median: 0.3333
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2322

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6897
- Median: 0.6911
- Min: 0.1447
- Max: 0.9823
- Std Dev: 0.2066

**Jaccard Similarity (top 20 words):**
- Mean: 0.3002
- Median: 0.2903
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.1678

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6402
- Median: 0.6848
- Min: 0.2004
- Max: 0.9674
- Std Dev: 0.2541

**Jaccard Similarity (top 20 words):**
- Mean: 0.2943
- Median: 0.3333
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1736

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 110

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6492
- Median: 0.6880
- Min: 0.0947
- Max: 0.9860
- Std Dev: 0.2578

### Jaccard Similarity (across all matches)
- Mean: 0.3305
- Median: 0.2903
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2185
