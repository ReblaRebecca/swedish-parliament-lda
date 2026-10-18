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
| 42 | 1701.60 | 50 |
| 123 | 1710.32 | 50 |
| 456 | 1736.38 | 50 |
| 789 | 1714.77 | 50 |
| 999 | 1716.44 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 7 |
| 3 of 4 | 5 |
| 2 of 4 | 7 |
| 1 of 4 | 5 |
| 0 of 4 | 8 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, förskola, förälder, barnomsorg, kommun, verksamhet, personal, pedagogisk | 4/4 | 0.903 | 0.773 | 0.507 |
| 2 | gymnasieskola, elev, program, kurs, gymnasium, ämne, betyg, ungdom | 4/4 | 0.895 | 0.840 | 0.497 |
| 3 | fristående, kommunal, friskola, elev, huvudma, kommun, skolinspektion, verksamhet | 2/4 | 0.735 | 0.584 | 0.456 |
| 4 | hög, många, problem, land, öka, utreda, minska, förutsättning | 3/4 | 0.734 | 0.657 | 0.222 |
| 5 | läkare, medicinsk, sjukvård, hälsa, vård, sjukdom, patient, läkarutbildning | 3/4 | 0.690 | 0.233 | 0.396 |
| 6 | ung, ungdom, hälsa, kunskap, psykisk, barn, många, ohälsa | 0/4 | 0.457 | 0.377 | 0.180 |
| 7 | lärare, lärarutbildning, pedagogisk, kvalitet, kompetens, rektor, läraryrke, stärka | 2/4 | 0.591 | 0.141 | 0.292 |
| 8 | ersättning, mälardalens, sexualitet, helårsstudent, musikhögskola, slopad, takbelopp, utbildningsvetenskaplig | 0/4 | 0.121 | 0.007 | 0.040 |
| 9 | teknisk, teknik, digital, it, område, kompetens, utveckling, utveckla | 1/4 | 0.376 | 0.002 | 0.211 |
| 10 | riksrevision, person, hbt, genusforskning, mitthögskola, bisexuell, homosexuell, skolavslutning | 0/4 | 0.141 | 0.090 | 0.090 |
| 11 | forskarnivå, miljö, hållbar, utveckling, kunskap, natur, ämne, alliansregering | 1/4 | 0.270 | 0.043 | 0.155 |
| 12 | idébur, kostnad, körkort, stat, avgift, procent, betala, bidrag | 0/4 | 0.444 | 0.391 | 0.273 |
| 13 | samhälle, människa, kunskap, rättighet, fråga, demokratisk, social, svensk | 4/4 | 0.844 | 0.814 | 0.512 |
| 14 | svensk, land, internationell, kunskap, sfi, eu, utländsk, invandrare | 3/4 | 0.784 | 0.541 | 0.265 |
| 15 | vuxenutbildning, arbetsmarknad, studie, lärande, folkhögskola, människa, studera, vuxen | 1/4 | 0.564 | 0.234 | 0.246 |
| 16 | student, högskola, hög, universitet, lärosäte, kvalitet, lärosäten, studie | 4/4 | 0.901 | 0.834 | 0.392 |
| 17 | kvinna, jämställdhet, flicka, pojke, kön, skolbibliotek, kvinnlig, uppdrag | 2/4 | 0.558 | 0.020 | 0.254 |
| 18 | anslag, högskola, nivå, forskning, grundnivå, medel, satsning, särskild | 1/4 | 0.660 | 0.599 | 0.283 |
| 19 | högskola, företag, region, län, hög, näringsliv, utveckling, land | 3/4 | 0.806 | 0.689 | 0.485 |
| 20 | skog, värmland, skåne, vatten, sverige, kulturskola, skogsbruk, jordbruk | 0/4 | 0.123 | 0.042 | 0.047 |
| 21 | stockholm, institutet, stiftelse, konstnärlig, stockholmsregionen, idrott, idrottshögskola, norrköping | 0/4 | 0.227 | 0.079 | 0.083 |
| 22 | barn, elev, stöd, behov, särskild, funktionshind, funktionsnedsättning, särskola | 4/4 | 0.839 | 0.729 | 0.529 |
| 23 | elev, mobbning, barn, lärare, våld, arbete, problem, åtgärd | 0/4 | 0.504 | 0.187 | 0.222 |
| 24 | fysisk, barn, aktivitet, idrott, ungdom, ämne, hälsa, fritid | 2/4 | 0.700 | 0.517 | 0.370 |
| 25 | universitet, avancerad, forskning, lund, umeå, göteborg, uppsala, malmö | 2/4 | 0.647 | 0.335 | 0.248 |
| 26 | kommun, verksamhet, kommunal, ansvar, lokal, stat, statlig, bidrag | 1/4 | 0.540 | 0.306 | 0.224 |
| 27 | högskola, linje, plats, stockholm, behov, lokal, högskoleutbildning, resurs | 3/4 | 0.858 | 0.666 | 0.410 |
| 28 | elev, grundskola, kunskap, undervisning, nationell, mål, lärare, betyg | 4/4 | 0.968 | 0.952 | 0.459 |
| 29 | yrkesutbildning, lärlingsutbildning, arbetsliv, yrke, praktik, praktisk, lärling, gymnasieexam | 0/4 | 0.064 | 0.034 | 0.053 |
| 30 | forskning, högskola, forskare, utveckling, universitet, område, resurs, internationell | 4/4 | 0.917 | 0.853 | 0.474 |
| 31 | språk, svenska, modersmål, undervisning, teckenspråk, modersmålsundervisning, svensk, nationell | 2/4 | 0.522 | 0.006 | 0.209 |
| 32 | behov, personal, vård, gammal, brist, landsting, öka, sjuksköterska | 2/4 | 0.624 | 0.401 | 0.350 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5746
- Median: 0.6177
- Min: 0.0066
- Max: 0.9835
- Std Dev: 0.3185

**Jaccard Similarity (top 20 words):**
- Mean: 0.2857
- Median: 0.2903
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1872

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6210
- Median: 0.7744
- Min: 0.0056
- Max: 0.9872
- Std Dev: 0.3312

**Jaccard Similarity (top 20 words):**
- Mean: 0.3258
- Median: 0.3793
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2176

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5785
- Median: 0.6609
- Min: 0.0199
- Max: 0.9609
- Std Dev: 0.3045

**Jaccard Similarity (top 20 words):**
- Mean: 0.2855
- Median: 0.2702
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1790

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6019
- Median: 0.7159
- Min: 0.0020
- Max: 0.9568
- Std Dev: 0.2967

**Jaccard Similarity (top 20 words):**
- Mean: 0.2819
- Median: 0.3118
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1785

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5497
- Median: 0.6210
- Min: 0.0014
- Max: 0.9850
- Std Dev: 0.3150

**Jaccard Similarity (top 20 words):**
- Mean: 0.2736
- Median: 0.2121
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2272

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6067
- Median: 0.6587
- Min: 0.0099
- Max: 0.9836
- Std Dev: 0.2729

**Jaccard Similarity (top 20 words):**
- Mean: 0.2929
- Median: 0.2500
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2006

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5427
- Median: 0.6148
- Min: 0.0016
- Max: 0.9801
- Std Dev: 0.3073

**Jaccard Similarity (top 20 words):**
- Mean: 0.2517
- Median: 0.2500
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1855

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5150
- Median: 0.6219
- Min: 0.0066
- Max: 0.9732
- Std Dev: 0.2984

**Jaccard Similarity (top 20 words):**
- Mean: 0.2252
- Median: 0.2121
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1609

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5280
- Median: 0.6111
- Min: 0.0003
- Max: 0.9734
- Std Dev: 0.3067

**Jaccard Similarity (top 20 words):**
- Mean: 0.2216
- Median: 0.1943
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1718

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5572
- Median: 0.6462
- Min: 0.0071
- Max: 0.9780
- Std Dev: 0.3067

**Jaccard Similarity (top 20 words):**
- Mean: 0.2595
- Median: 0.2311
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1659

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 320

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5675
- Median: 0.6398
- Min: 0.0003
- Max: 0.9872
- Std Dev: 0.3079

### Jaccard Similarity (across all matches)
- Mean: 0.2703
- Median: 0.2500
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.1909

## Key Change from Previous Analysis

Previous reports compared Topic 1 to Topic 1, Topic 2 to Topic 2, etc. across seeds.
This is methodologically invalid because topic indices are arbitrary.

This corrected analysis uses the Hungarian algorithm to find optimal topic correspondences
before computing similarities. The previous mean Jaccard value of ~0.02 reflected
invalid index-by-index comparison. The values above reflect matched topics.