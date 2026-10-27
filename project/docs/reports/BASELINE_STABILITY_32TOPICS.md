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
| 42 | 1982.24 | 50 |
| 123 | 1994.40 | 50 |
| 456 | 2014.59 | 50 |
| 789 | 1995.08 | 50 |
| 999 | 1990.38 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 4 |
| 3 of 4 | 8 |
| 2 of 4 | 5 |
| 1 of 4 | 5 |
| 0 of 4 | 10 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | kommun, fristående, kommunal, verksamhet, lag, offentlig, regel, bidrag | 3/4 | 0.766 | 0.604 | 0.350 |
| 2 | lärare, lärarutbildning, pedagogisk, fortbildning, ämne, läraryrke, kompetens, undervisning | 3/4 | 0.727 | 0.162 | 0.325 |
| 3 | vuxenutbildning, läsa, svensk, sfi, invandrare, digital, undervisning, svenska | 0/4 | 0.540 | 0.477 | 0.295 |
| 4 | elev, gymnasieskola, program, betyg, ämne, kurs, gymnasium, kunskap | 2/4 | 0.707 | 0.495 | 0.332 |
| 5 | forskning, utveckling, område, teknik, miljö, nationell, svensk, forskare | 3/4 | 0.732 | 0.263 | 0.208 |
| 6 | yrkesutbildning, lärlingsutbildning, yrke, företag, eftergymnasial, lärling, arbetsplats, akademin | 1/4 | 0.415 | 0.009 | 0.189 |
| 7 | barn, behov, förälder, stöd, särskild, funktionshind, funktionsnedsättning, särskola | 2/4 | 0.593 | 0.035 | 0.259 |
| 8 | idrott, aktivitet, fritid, professur, turism, fysisk, gymnastik, falun | 0/4 | 0.361 | 0.000 | 0.117 |
| 9 | barn, förskola, barnomsorg, förälder, verksamhet, pedagogisk, kommun, personal | 4/4 | 0.960 | 0.931 | 0.625 |
| 10 | borås, malmö, bibliotek, tandläkare, lund, konstfack, historisk, mus | 0/4 | 0.074 | 0.016 | 0.020 |
| 11 | digitalisering, vinst, miljard, resursskola, person, dans, införa, pandemin | 0/4 | 0.117 | 0.050 | 0.026 |
| 12 | fysisk, hälsa, psykisk, sjukdom, ung, ohälsa, forskning, ungdom | 3/4 | 0.606 | 0.279 | 0.292 |
| 13 | kommun, stockholm, region, södertörn, land, hög, län, södra | 0/4 | 0.460 | 0.038 | 0.169 |
| 14 | samhälle, människa, svensk, kultur, värdegrund, rättighet, värde, värdering | 3/4 | 0.772 | 0.426 | 0.490 |
| 15 | läromedel, elev, tillgång, skolbibliotek, bok, dator, använda, hjälpmedel | 0/4 | 0.162 | 0.003 | 0.033 |
| 16 | vård, läkare, sjukvård, landsting, medicinsk, läkarutbildning, hälsa, patient | 2/4 | 0.688 | 0.454 | 0.429 |
| 17 | språk, modersmål, svensk, svenska, omsorg, barn, undervisning, nationell | 4/4 | 0.832 | 0.752 | 0.470 |
| 18 | högskola, behov, plats, resurs, teknisk, län, liten, utveckling | 3/4 | 0.807 | 0.667 | 0.370 |
| 19 | umeå, universitet, region, gävle, län, norrland, luleå, land | 0/4 | 0.361 | 0.053 | 0.134 |
| 20 | tv, ant, information, vatten, okunskap, brottslighet, avstängning, superdator | 0/4 | 0.139 | 0.014 | 0.026 |
| 21 | bidrag, studie, anslag, ekonomisk, studerande, studiemedel, kostnad, folkhögskola | 2/4 | 0.638 | 0.404 | 0.426 |
| 22 | elevhälsa, körkort, uf, skolinspektion, körkortsutbildning, simundervisning, ungdom, simma | 0/4 | 0.113 | 0.058 | 0.060 |
| 23 | ämne, kunskap, elev, ungdom, mat, grundskola, hälsa, undervisning | 1/4 | 0.591 | 0.304 | 0.252 |
| 24 | universitet, göteborg, lund, stockholm, uppsala, linköping, institution, institutet | 2/4 | 0.743 | 0.566 | 0.266 |
| 25 | elev, kommun, grundskola, nationell, lärare, undervisning, skolverket, stöd | 4/4 | 0.857 | 0.772 | 0.316 |
| 26 | högskola, forskning, student, universitet, hög, lärosäte, kvalitet, anslag | 4/4 | 0.872 | 0.821 | 0.497 |
| 27 | svensk, land, internationell, språk, eu, utländsk, värld, nordisk | 3/4 | 0.738 | 0.220 | 0.306 |
| 28 | kvinna, undervisning, flicka, jämställdhet, pojke, kunskap, sexuell, elev | 1/4 | 0.672 | 0.511 | 0.207 |
| 29 | kunskap, arbete, samhälle, ansvar, utveckling, uppgift, social, egen | 1/4 | 0.660 | 0.429 | 0.283 |
| 30 | hög, behov, arbetsmarknad, företag, land, öka, utveckla, kompetens | 1/4 | 0.660 | 0.601 | 0.388 |
| 31 | it, mälardalens, utanförskap, lärcentrum, mitthögskolan, blekinge, mittuniversitet, mitthögskola | 0/4 | 0.076 | 0.000 | 0.034 |
| 32 | elev, mobbning, barn, lärare, arbete, våld, rektor, utsatt | 3/4 | 0.781 | 0.634 | 0.351 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5815
- Median: 0.6759
- Min: 0.0004
- Max: 0.9823
- Std Dev: 0.3362

**Jaccard Similarity (top 20 words):**
- Mean: 0.2929
- Median: 0.3118
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2183

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5569
- Median: 0.6063
- Min: 0.0092
- Max: 0.9773
- Std Dev: 0.3123

**Jaccard Similarity (top 20 words):**
- Mean: 0.2507
- Median: 0.2121
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2049

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5858
- Median: 0.6250
- Min: 0.0031
- Max: 0.9308
- Std Dev: 0.2891

**Jaccard Similarity (top 20 words):**
- Mean: 0.2661
- Median: 0.2500
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1673

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5529
- Median: 0.6177
- Min: 0.0001
- Max: 0.9844
- Std Dev: 0.3197

**Jaccard Similarity (top 20 words):**
- Mean: 0.2583
- Median: 0.2500
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1987

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5478
- Median: 0.6651
- Min: 0.0024
- Max: 0.9779
- Std Dev: 0.3010

**Jaccard Similarity (top 20 words):**
- Mean: 0.2079
- Median: 0.1597
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1754

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5635
- Median: 0.5814
- Min: 0.0004
- Max: 0.9589
- Std Dev: 0.2944

**Jaccard Similarity (top 20 words):**
- Mean: 0.2703
- Median: 0.2903
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2061

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5930
- Median: 0.6820
- Min: 0.0012
- Max: 0.9645
- Std Dev: 0.3085

**Jaccard Similarity (top 20 words):**
- Mean: 0.2578
- Median: 0.1943
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2003

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5215
- Median: 0.5377
- Min: 0.0063
- Max: 0.9845
- Std Dev: 0.2660

**Jaccard Similarity (top 20 words):**
- Mean: 0.2333
- Median: 0.2500
- Min: 0.0000
- Max: 0.4815
- Std Dev: 0.1524

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5107
- Median: 0.5596
- Min: 0.0003
- Max: 0.9863
- Std Dev: 0.2778

**Jaccard Similarity (top 20 words):**
- Mean: 0.1873
- Median: 0.1597
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1436

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5783
- Median: 0.6633
- Min: 0.0077
- Max: 0.9719
- Std Dev: 0.3050

**Jaccard Similarity (top 20 words):**
- Mean: 0.2570
- Median: 0.2500
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1821

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 320

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5592
- Median: 0.6209
- Min: 0.0001
- Max: 0.9863
- Std Dev: 0.3027

### Jaccard Similarity (across all matches)
- Mean: 0.2482
- Median: 0.2121
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1887
