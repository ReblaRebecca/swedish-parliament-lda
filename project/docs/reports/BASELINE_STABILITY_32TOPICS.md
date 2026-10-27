# Seed-Stability Analysis: 32-Topic Baseline LDA

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only (titles are not added)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 32 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1937.30 | 50 |
| 123 | 1934.21 | 50 |
| 456 | 1942.25 | 50 |
| 789 | 1934.20 | 50 |
| 999 | 1954.68 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 4 |
| 2 of 4 | 8 |
| 1 of 4 | 7 |
| 0 of 4 | 9 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | vetenskapsråd, riksrevision, vinnova, statlig, tfhs, ämnesråd, pandemin, holdingbolag | 1/4 | 0.344 | 0.065 | 0.180 |
| 2 | forskning, universitet, svensk, forskare, utveckling, område, internationell, avancerad | 4/4 | 0.914 | 0.870 | 0.606 |
| 3 | teknik, yrkeshögskola, it, teknisk, kärnämne, akademi, naturvetenskap, använda | 0/4 | 0.237 | 0.077 | 0.110 |
| 4 | studie, ekonomisk, student, studiemedel, system, kostnad, studera, studerande | 1/4 | 0.574 | 0.208 | 0.299 |
| 5 | elev, gymnasieskola, ämne, betyg, program, kunskap, grundskola, gymnasium | 4/4 | 0.864 | 0.777 | 0.432 |
| 6 | kommun, elev, fristående, kommunal, friskola, förälder, verksamhet, välja | 3/4 | 0.872 | 0.674 | 0.408 |
| 7 | anslag, högskola, förslag, medel, resurs, liten, särskild, verksamhet | 3/4 | 0.716 | 0.568 | 0.350 |
| 8 | läkare, läkarutbildning, land, fn, utbildningsplats, läkemedel, plats, sjukvård | 0/4 | 0.057 | 0.000 | 0.044 |
| 9 | hälsa, kunskap, sjukdom, mat, hemkunskap, ämne, psykisk, dålig | 0/4 | 0.514 | 0.083 | 0.220 |
| 10 | sfi, invandrare, svensk, nyanländ, undervisning, timme, svenska, arbetsmarknad | 1/4 | 0.509 | 0.121 | 0.347 |
| 11 | barn, förälder, ungdom, ung, social, samhälle, problem, vuxen | 1/4 | 0.563 | 0.450 | 0.219 |
| 12 | universitet, göteborg, umeå, lund, örebro, stockholm, institution, uppsala | 2/4 | 0.612 | 0.027 | 0.246 |
| 13 | kvinna, kunskap, samhälle, människa, jämställdhet, flicka, arbete, pojke | 2/4 | 0.572 | 0.248 | 0.268 |
| 14 | förslag, verksamhet, uppgift, ansvar, politisk, krav, enskild, återkomma | 0/4 | 0.516 | 0.447 | 0.143 |
| 15 | nationell, uppdrag, kvalitet, myndighet, tydlig, stärka, skolverk, stat | 0/4 | 0.393 | 0.198 | 0.169 |
| 16 | vuxenutbildning, behov, arbetsmarknad, lärande, folkhögskola, människa, yrkesutbildning, samhälle | 2/4 | 0.658 | 0.542 | 0.357 |
| 17 | elev, lärare, undervisning, kunskap, grundskola, lärarutbildning, mobbning, stöd | 1/4 | 0.724 | 0.552 | 0.311 |
| 18 | nivå, konstnärlig, mälardalens, malmö, musik, borås, kultur, stockholm | 2/4 | 0.460 | 0.003 | 0.242 |
| 19 | idrott, fysisk, aktivitet, hälsa, fritid, rörelse, ämne, friluftsliv | 2/4 | 0.719 | 0.590 | 0.276 |
| 20 | kränkning, ky, utbildningsvetenskaplig, vfu, skolavslutning, rektorsutbildning, otrygg, kill | 0/4 | 0.146 | 0.013 | 0.026 |
| 21 | svensk, språk, land, svenska, undervisning, modersmål, internationell, teckenspråk | 3/4 | 0.782 | 0.606 | 0.340 |
| 22 | högskola, län, jönköping, gävle, kristianstad, sandviken, halmstad, gävleborg | 3/4 | 0.599 | 0.060 | 0.067 |
| 23 | högskola, linje, plats, behov, teknisk, län, kurs, högskoleutbildning | 2/4 | 0.604 | 0.344 | 0.274 |
| 24 | företag, land, hög, utveckling, region, näringsliv, regional, utveckla | 2/4 | 0.664 | 0.361 | 0.349 |
| 25 | elev, behov, särskola, funktionshind, stöd, specialskola, särskild, läromedel | 0/4 | 0.579 | 0.499 | 0.314 |
| 26 | narkotika, hbt, ant, fråga, undervisning, bisexuell, barnkunskap, indikator | 0/4 | 0.141 | 0.129 | 0.067 |
| 27 | skolinspektion, huvudman, elevhälsa, utreda, alliansregering, tillstånd, befogenhet, neuropsykiatrisk | 1/4 | 0.349 | 0.022 | 0.067 |
| 28 | läroplan, ämne, undervisning, samhälle, människa, värde, värdegrund, religiös | 1/4 | 0.606 | 0.356 | 0.367 |
| 29 | vård, behov, landsting, sjukvård, hälsa, ohälsa, sjuksköterska, patient | 2/4 | 0.754 | 0.625 | 0.394 |
| 30 | student, högskola, hög, universitet, lärosäte, kvalitet, lärare, akademisk | 4/4 | 0.920 | 0.863 | 0.459 |
| 31 | stockholm, linköping, stiftelse, stockholmsregionen, beräknad, södertälje, trädgård, kommun | 0/4 | 0.175 | 0.039 | 0.040 |
| 32 | förskola, barn, pedagogisk, verksamhet, barnomsorg, förälder, personal, behov | 4/4 | 0.923 | 0.905 | 0.650 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5753
- Median: 0.6494
- Min: 0.0245
- Max: 0.9733
- Std Dev: 0.2920

**Jaccard Similarity (top 20 words):**
- Mean: 0.2841
- Median: 0.2311
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2179

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5452
- Median: 0.6322
- Min: 0.0004
- Max: 0.9617
- Std Dev: 0.3088

**Jaccard Similarity (top 20 words):**
- Mean: 0.2544
- Median: 0.1765
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2084

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5444
- Median: 0.6251
- Min: 0.0030
- Max: 0.9626
- Std Dev: 0.3066

**Jaccard Similarity (top 20 words):**
- Mean: 0.2626
- Median: 0.2500
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1937

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5929
- Median: 0.6391
- Min: 0.0128
- Max: 0.9558
- Std Dev: 0.2805

**Jaccard Similarity (top 20 words):**
- Mean: 0.2791
- Median: 0.2702
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.1763

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5373
- Median: 0.6192
- Min: 0.0031
- Max: 0.9826
- Std Dev: 0.3468

**Jaccard Similarity (top 20 words):**
- Mean: 0.2672
- Median: 0.2121
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2275

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5251
- Median: 0.6002
- Min: 0.0010
- Max: 0.9768
- Std Dev: 0.3005

**Jaccard Similarity (top 20 words):**
- Mean: 0.2381
- Median: 0.1765
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.2231

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.4965
- Median: 0.5450
- Min: 0.0018
- Max: 0.9735
- Std Dev: 0.2941

**Jaccard Similarity (top 20 words):**
- Mean: 0.1897
- Median: 0.1429
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1617

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5035
- Median: 0.5073
- Min: 0.0083
- Max: 0.9876
- Std Dev: 0.3077

**Jaccard Similarity (top 20 words):**
- Mean: 0.2403
- Median: 0.2121
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1853

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5565
- Median: 0.5563
- Min: 0.0021
- Max: 0.9881
- Std Dev: 0.3121

**Jaccard Similarity (top 20 words):**
- Mean: 0.2648
- Median: 0.2311
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2025

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5459
- Median: 0.5722
- Min: 0.0023
- Max: 0.9761
- Std Dev: 0.2697

**Jaccard Similarity (top 20 words):**
- Mean: 0.2296
- Median: 0.1943
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1610

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 320

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5423
- Median: 0.5988
- Min: 0.0004
- Max: 0.9881
- Std Dev: 0.3038

### Jaccard Similarity (across all matches)
- Mean: 0.2510
- Median: 0.2121
- Min: 0.0000
- Max: 1.0000
- Std Dev: 0.1989
