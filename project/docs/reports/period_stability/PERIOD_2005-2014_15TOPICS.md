# Seed-Stability Analysis: Period 2005-2014, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of 2005-2014 (3577)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1517.33 | 50 |
| 123 | 1537.69 | 50 |
| 456 | 1522.25 | 50 |
| 789 | 1522.88 | 50 |
| 999 | 1518.26 | 50 |

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
| 1 of 4 | 2 |
| 0 of 4 | 4 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | student, studie, studiemedel, ekonomisk, studera, många, arbeta, studerande | 4/4 | 0.935 | 0.861 | 0.611 |
| 2 | drog, narkotika, ungdom, alkohol, schack, elev, ant, drogtest | 0/4 | 0.173 | 0.110 | 0.055 |
| 3 | person, funktionshind, punktskrift, undervisning, synskadad, specialskola, konvention, grav | 0/4 | 0.164 | 0.018 | 0.062 |
| 4 | forskning, svensk, utveckling, forskare, område, internationell, land, nationell | 3/4 | 0.848 | 0.590 | 0.392 |
| 5 | barn, hälsa, fysisk, läkare, ungdom, aktivitet, många, vård | 2/4 | 0.730 | 0.616 | 0.348 |
| 6 | företag, land, svensk, lycka, människa, entreprenörskap, starta, verksamhet | 0/4 | 0.432 | 0.274 | 0.149 |
| 7 | lärare, elev, nationell, betyg, lärarutbildning, mål, ämne, prov | 4/4 | 0.844 | 0.775 | 0.472 |
| 8 | elev, kunskap, barn, undervisning, mobbning, flicka, ungdom, lärare | 2/4 | 0.697 | 0.429 | 0.385 |
| 9 | elev, kunskap, språk, undervisning, utveckla, lärande, barn, svensk | 1/4 | 0.599 | 0.433 | 0.240 |
| 10 | högskola, universitet, forskning, hög, region, land, regional, län | 2/4 | 0.522 | 0.120 | 0.182 |
| 11 | högskola, student, hög, universitet, kvalitet, anslag, lärosäte, kunskap | 3/4 | 0.699 | 0.171 | 0.401 |
| 12 | svensk, politisk, samhälle, skolbibliotek, stiftelse, rättighet, nationell, minoritetsspråk | 1/4 | 0.537 | 0.436 | 0.183 |
| 13 | gymnasieskola, program, vuxenutbildning, arbetsmarknad, behov, elev, yrkesutbildning, ungdom | 3/4 | 0.762 | 0.641 | 0.373 |
| 14 | barn, musik, kultur, miljö, estetisk, lek, lärande, trafik | 0/4 | 0.436 | 0.296 | 0.113 |
| 15 | barn, förskola, kommun, elev, förälder, fristående, kommunal, verksamhet | 4/4 | 0.848 | 0.778 | 0.469 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.6020
- Median: 0.6161
- Min: 0.0482
- Max: 0.9709
- Std Dev: 0.2655

**Jaccard Similarity (top 20 words):**
- Mean: 0.2810
- Median: 0.2500
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2069

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6219
- Median: 0.6456
- Min: 0.1215
- Max: 0.9798
- Std Dev: 0.2644

**Jaccard Similarity (top 20 words):**
- Mean: 0.2609
- Median: 0.2500
- Min: 0.0256
- Max: 0.5385
- Std Dev: 0.1541

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6142
- Median: 0.7689
- Min: 0.0184
- Max: 0.9626
- Std Dev: 0.3165

**Jaccard Similarity (top 20 words):**
- Mean: 0.3469
- Median: 0.3793
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2400

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6225
- Median: 0.7529
- Min: 0.2741
- Max: 0.9683
- Std Dev: 0.2662

**Jaccard Similarity (top 20 words):**
- Mean: 0.2940
- Median: 0.3793
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2080

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6396
- Median: 0.6538
- Min: 0.0286
- Max: 0.9728
- Std Dev: 0.2728

**Jaccard Similarity (top 20 words):**
- Mean: 0.3033
- Median: 0.2500
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2002

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6000
- Median: 0.7110
- Min: 0.1210
- Max: 0.9695
- Std Dev: 0.2776

**Jaccard Similarity (top 20 words):**
- Mean: 0.2713
- Median: 0.2500
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.2060

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6235
- Median: 0.6761
- Min: 0.0837
- Max: 0.9171
- Std Dev: 0.2517

**Jaccard Similarity (top 20 words):**
- Mean: 0.2742
- Median: 0.2903
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1523

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6180
- Median: 0.7208
- Min: 0.0389
- Max: 0.9920
- Std Dev: 0.3172

**Jaccard Similarity (top 20 words):**
- Mean: 0.3361
- Median: 0.2500
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2470

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6492
- Median: 0.7383
- Min: 0.0598
- Max: 0.9797
- Std Dev: 0.2917

**Jaccard Similarity (top 20 words):**
- Mean: 0.3119
- Median: 0.2903
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2097

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6208
- Median: 0.7406
- Min: 0.1049
- Max: 0.9557
- Std Dev: 0.2886

**Jaccard Similarity (top 20 words):**
- Mean: 0.2955
- Median: 0.2121
- Min: 0.0256
- Max: 0.6667
- Std Dev: 0.1982

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6212
- Median: 0.6806
- Min: 0.0184
- Max: 0.9920
- Std Dev: 0.2824

### Jaccard Similarity (across all matches)
- Mean: 0.2975
- Median: 0.2903
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2060
