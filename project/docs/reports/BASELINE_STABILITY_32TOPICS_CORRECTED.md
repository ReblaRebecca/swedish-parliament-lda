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
| 42 | 1702.46 | 50 |
| 123 | 1693.53 | 50 |
| 456 | 1690.70 | 50 |
| 789 | 1704.46 | 50 |
| 999 | 1700.92 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 8 |
| 3 of 4 | 4 |
| 2 of 4 | 2 |
| 1 of 4 | 7 |
| 0 of 4 | 11 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, förälder, kommun, barnomsorg, verksamhet, personal, pedagogisk | 4/4 | 0.983 | 0.974 | 0.742 |
| 2 | lärare, lärarutbildning, forskarnivå, pedagogisk, fortbildning, undervisning, läsa, skolinspektion | 4/4 | 0.940 | 0.879 | 0.204 |
| 3 | idrott, it, västerås, lärarstudent, institutet, eskilstuna, data, aktiebolag | 0/4 | 0.173 | 0.000 | 0.039 |
| 4 | hälsa, fysisk, ungdom, ung, barn, aktivitet, kunskap, ämne | 1/4 | 0.668 | 0.593 | 0.340 |
| 5 | stat, statlig, verksamhet, bedriva, ansvar, stiftelse, avtal, huvudmannaskap | 0/4 | 0.134 | 0.040 | 0.027 |
| 6 | göteborg, universitet, lund, malmö, stockholm, professur, institution, centrum | 1/4 | 0.483 | 0.244 | 0.214 |
| 7 | betyg, godkänd, betygssystem, mälardalens, slutbetyg, betygsättning, ant, utvecklingssamtal | 0/4 | 0.015 | 0.000 | 0.020 |
| 8 | barn, elev, stöd, behov, sexuell, särskild, funktionshind, funktionsnedsättning | 2/4 | 0.761 | 0.557 | 0.388 |
| 9 | behov, stockholm, linje, högskola, resurs, procent, teknisk, lokal | 3/4 | 0.782 | 0.694 | 0.488 |
| 10 | anslag, forskning, medel, grundnivå, satsning, särskild, nivå, öka | 0/4 | 0.396 | 0.034 | 0.245 |
| 11 | universitet, avancerad, umeå, nivå, örebro, stockholm, linköping, uppsala | 2/4 | 0.716 | 0.680 | 0.281 |
| 12 | kommun, elev, fristående, kommunal, friskola, välja, skolinspektion, bidrag | 4/4 | 0.956 | 0.921 | 0.555 |
| 13 | miljö, natur, kunskap, ekologisk, grön, landsbygd, skog, trafik | 0/4 | 0.373 | 0.117 | 0.199 |
| 14 | företag, yrkeshögskola, digital, teknik, teknisk, starta, företagande, näringsliv | 0/4 | 0.267 | 0.212 | 0.100 |
| 15 | hög, arbetsmarknad, många, arbete, vuxenutbildning, studie, behov, öka | 3/4 | 0.744 | 0.676 | 0.370 |
| 16 | utveckling, land, region, hög, regional, utveckla, näringsliv, län | 3/4 | 0.750 | 0.581 | 0.471 |
| 17 | språk, svensk, modersmål, svenska, teckenspråk, undervisning, nationell, döv | 1/4 | 0.519 | 0.123 | 0.241 |
| 18 | svensk, land, internationell, utländsk, värld, eu, utomlands, europa | 1/4 | 0.532 | 0.021 | 0.111 |
| 19 | nationell, kvalitet, mål, lärare, ansvar, förutsättning, tydlig, resurs | 1/4 | 0.597 | 0.368 | 0.248 |
| 20 | elev, gymnasieskola, ämne, grundskola, kunskap, program, undervisning, gymnasium | 4/4 | 0.874 | 0.819 | 0.407 |
| 21 | student, studiemedel, studie, studerande, folkhögskola, studera, studiestöd, ekonomisk | 3/4 | 0.742 | 0.352 | 0.344 |
| 22 | många, problem, barn, elev, dålig, svår, åtgärd, situation | 1/4 | 0.633 | 0.475 | 0.146 |
| 23 | läkare, jönköping, landsting, vård, läkarutbildning, gävle, utbildningsplats, plats | 0/4 | 0.476 | 0.373 | 0.243 |
| 24 | högskola, student, universitet, hög, liten, högskoleutbildning, plats, kvalitet | 4/4 | 0.842 | 0.785 | 0.225 |
| 25 | kultur, musik, bibliotek, driva, konstnärlig, bild, akademi, verksamhet | 0/4 | 0.328 | 0.012 | 0.114 |
| 26 | samhälle, människa, kunskap, undervisning, läroplan, svensk, ämne, värde | 4/4 | 0.854 | 0.793 | 0.471 |
| 27 | sfi, svensk, invandrare, kommun, undervisning, lag, nyanländ, svenska | 0/4 | 0.155 | 0.098 | 0.039 |
| 28 | forskning, universitet, lärosäte, forskare, utveckling, område, hög, vetenskaplig | 4/4 | 0.894 | 0.859 | 0.416 |
| 29 | myndighet, skolverket, läromedel, verksamhet, tillstånd, skolverk, tillsyn, utreda | 0/4 | 0.243 | 0.044 | 0.068 |
| 30 | elev, ansvar, inflytande, lokal, politisk, verksamhet, skollag, arbete | 0/4 | 0.561 | 0.457 | 0.169 |
| 31 | sjukdom, vård, medicinsk, sjukvård, patient, klinisk, gammal, forskning | 4/4 | 0.727 | 0.704 | 0.540 |
| 32 | kvinna, mobbning, flicka, arbete, våld, jämställdhet, pojke, ung | 1/4 | 0.679 | 0.627 | 0.343 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5960
- Median: 0.6711
- Min: 0.0003
- Max: 0.9896
- Std Dev: 0.2912

**Jaccard Similarity (top 20 words):**
- Mean: 0.2825
- Median: 0.2311
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.1967

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5599
- Median: 0.5951
- Min: 0.0115
- Max: 0.9743
- Std Dev: 0.2867

**Jaccard Similarity (top 20 words):**
- Mean: 0.2612
- Median: 0.2500
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1785

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6055
- Median: 0.6583
- Min: 0.0004
- Max: 0.9899
- Std Dev: 0.2946

**Jaccard Similarity (top 20 words):**
- Mean: 0.2783
- Median: 0.2311
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2135

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5884
- Median: 0.6909
- Min: 0.0003
- Max: 0.9793
- Std Dev: 0.3173

**Jaccard Similarity (top 20 words):**
- Mean: 0.2789
- Median: 0.2903
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2012

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6455
- Median: 0.7502
- Min: 0.0015
- Max: 0.9893
- Std Dev: 0.2805

**Jaccard Similarity (top 20 words):**
- Mean: 0.3471
- Median: 0.3333
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2264

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5537
- Median: 0.5908
- Min: 0.0028
- Max: 0.9854
- Std Dev: 0.2897

**Jaccard Similarity (top 20 words):**
- Mean: 0.2516
- Median: 0.1943
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1944

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5902
- Median: 0.6558
- Min: 0.0026
- Max: 0.9831
- Std Dev: 0.3189

**Jaccard Similarity (top 20 words):**
- Mean: 0.3126
- Median: 0.3333
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1914

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5898
- Median: 0.5896
- Min: 0.0061
- Max: 0.9673
- Std Dev: 0.2767

**Jaccard Similarity (top 20 words):**
- Mean: 0.2702
- Median: 0.1765
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2174

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5911
- Median: 0.5981
- Min: 0.0068
- Max: 0.9886
- Std Dev: 0.2732

**Jaccard Similarity (top 20 words):**
- Mean: 0.2752
- Median: 0.2132
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1770

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5910
- Median: 0.6710
- Min: 0.0172
- Max: 0.9863
- Std Dev: 0.2970

**Jaccard Similarity (top 20 words):**
- Mean: 0.2709
- Median: 0.2500
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1964

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 320

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5911
- Median: 0.6610
- Min: 0.0003
- Max: 0.9899
- Std Dev: 0.2939

### Jaccard Similarity (across all matches)
- Mean: 0.2828
- Median: 0.2500
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2016

## Key Change from Previous Analysis

Previous reports compared Topic 1 to Topic 1, Topic 2 to Topic 2, etc. across seeds.
This is methodologically invalid because topic indices are arbitrary.

This corrected analysis uses the Hungarian algorithm to find optimal topic correspondences
before computing similarities. The previous mean Jaccard value of ~0.02 reflected
invalid index-by-index comparison. The values above reflect matched topics.