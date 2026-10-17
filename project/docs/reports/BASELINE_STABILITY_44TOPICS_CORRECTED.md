# Seed-Stability Analysis: 44-Topic Baseline LDA

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Weighting:** None (body text only)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 44 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 2165.68 | 50 |
| 123 | 2161.05 | 50 |
| 456 | 2158.60 | 50 |
| 789 | 2153.37 | 50 |
| 999 | 2168.17 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 7 |
| 2 of 4 | 7 |
| 1 of 4 | 6 |
| 0 of 4 | 19 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | arbetsmarknad, vuxenutbildning, behov, lärande, människa, yrkesutbildning, arbetsliv, hög | 1/4 | 0.599 | 0.376 | 0.206 |
| 2 | lag, lagstiftning, kränkning, mitthögskolan, huvudman, lagförslag, ändring, definition | 0/4 | 0.277 | 0.086 | 0.079 |
| 3 | lärlingsutbildning, lärling, stiftelse, företagare, matchning, skolavslutning, yrkesexam, yrke | 0/4 | 0.184 | 0.028 | 0.099 |
| 4 | hälsa, ungdom, ung, barn, aktivitet, kunskap, fysisk, ämne | 2/4 | 0.642 | 0.429 | 0.331 |
| 5 | kostnad, stat, procent, statsbidrag, ekonomisk, bidrag, avgift, lån | 1/4 | 0.352 | 0.024 | 0.216 |
| 6 | universitet, göteborg, umeå, lund, uppsala, stockholm, professur, malmö | 2/4 | 0.671 | 0.349 | 0.166 |
| 7 | skolinspektion, mälardalens, mittuniversitet, helårsstudent, ant, mitthögskola, implementera, takbelopp | 0/4 | 0.208 | 0.018 | 0.061 |
| 8 | barn, förälder, behov, stöd, många, sexuell, ungdom, familj | 2/4 | 0.734 | 0.665 | 0.262 |
| 9 | högskola, teknisk, högskoleutbildning, behov, resurs, plats, kurs, lokal | 4/4 | 0.879 | 0.767 | 0.310 |
| 10 | student, studie, studiemedel, studerande, studera, högskola, hög, studiestöd | 3/4 | 0.822 | 0.631 | 0.502 |
| 11 | nivå, högskola, avancerad, forskning, grundnivå, forskarnivå, universitet, körkort | 1/4 | 0.464 | 0.004 | 0.139 |
| 12 | elev, gymnasieskola, program, gymnasium, ämne, ungdom, grundskola, betyg | 3/4 | 0.771 | 0.412 | 0.342 |
| 13 | natur, ekologisk, grön, turism, skog, kunskap, jord, kooperativ | 0/4 | 0.343 | 0.001 | 0.229 |
| 14 | borås, kristianstad, blekinge, växjö, idrottshögskola, ingenjörsutbildning, tuff, karlskrona | 0/4 | 0.194 | 0.000 | 0.026 |
| 15 | många, land, öka, svensk, problem, hög, system, minska | 0/4 | 0.475 | 0.377 | 0.113 |
| 16 | gävle, kårobligatorium, studentinflytande, sandviken, medlem, förening, testa, skyddad | 0/4 | 0.215 | 0.000 | 0.061 |
| 17 | språk, svensk, svenska, undervisning, sfi, invandrare, land, modersmål | 3/4 | 0.806 | 0.644 | 0.427 |
| 18 | eu, läkemedel, finland, samisk, danmark, finsk, norge, svensk | 0/4 | 0.090 | 0.000 | 0.103 |
| 19 | hög, kvalitet, krav, politisk, mål, nationell, betyg, system | 1/4 | 0.535 | 0.206 | 0.160 |
| 20 | kunskap, ämne, kurs, många, läsa, hög, svensk, studie | 0/4 | 0.381 | 0.325 | 0.139 |
| 21 | idrott, fysisk, dalarna, falun, borlänge, slu, träning, idrottsämne | 2/4 | 0.538 | 0.134 | 0.161 |
| 22 | problem, många, använda, miljö, åtgärd, arbetsmiljö, skolbibliotek, brott | 0/4 | 0.333 | 0.213 | 0.054 |
| 23 | anläggning, kulturskola, svensk, ess, plattform, lund, marin, tfhs | 0/4 | 0.155 | 0.021 | 0.047 |
| 24 | lärare, lärarutbildning, pedagogisk, läraryrke, fortbildning, kompetens, undervisning, behörig | 3/4 | 0.701 | 0.005 | 0.266 |
| 25 | forskning, digital, medicinsk, sjukdom, hälsa, klinisk, sjukvård, vård | 0/4 | 0.544 | 0.388 | 0.330 |
| 26 | samhälle, människa, kunskap, undervisning, läroplan, svensk, ämne, demokratisk | 3/4 | 0.719 | 0.470 | 0.403 |
| 27 | kommun, fristående, elev, kommunal, friskola, välja, förälder, skollag | 4/4 | 0.967 | 0.935 | 0.622 |
| 28 | forskning, högskola, universitet, forskare, hög, lärosäte, svensk, utveckling | 4/4 | 0.883 | 0.811 | 0.381 |
| 29 | styrelse, bild, lokal, digitalisering, akademi, estetisk, intern, tillstånd | 0/4 | 0.150 | 0.007 | 0.123 |
| 30 | verksamhet, särskild, förändring, föreslå, allmän, emellertid, uppfattning, stockholm | 2/4 | 0.665 | 0.503 | 0.300 |
| 31 | hbt, avvikelse, bisexuell, homosexuell, transperson, examensrätt, kvalitetsredovisning, dygn | 0/4 | 0.463 | 0.321 | 0.213 |
| 32 | mobbning, våld, elev, arbete, utsatt, lärare, rektor, ung | 2/4 | 0.679 | 0.488 | 0.368 |
| 33 | kvinna, jämställdhet, flicka, pojke, kön, kvinnlig, manlig, arbeta | 3/4 | 0.739 | 0.028 | 0.458 |
| 34 | myndighet, verksamhet, nationell, yrkeshögskola, uppdrag, ansvar, organisation, stat | 0/4 | 0.160 | 0.104 | 0.067 |
| 35 | skövde, industri, område, utveckling, västsverige, produktion, kompetens, bransch | 0/4 | 0.389 | 0.238 | 0.112 |
| 36 | poäng, plats, linje, dimensionering, social, budgetproposition, nybörjarplats, jönköping | 0/4 | 0.366 | 0.001 | 0.127 |
| 37 | kultur, historia, musik, konstnärlig, historisk, kulturell, tv, film | 0/4 | 0.263 | 0.010 | 0.119 |
| 38 | anslag, medel, bidrag, anvisa, anslå, budgetår, utgiftsområde, avsätta | 4/4 | 0.845 | 0.760 | 0.427 |
| 39 | län, region, regional, hög, utveckling, land, högskola, näringsliv | 2/4 | 0.685 | 0.462 | 0.377 |
| 40 | företag, teknik, teknisk, it, driva, starta, näringsliv, egen | 1/4 | 0.443 | 0.007 | 0.120 |
| 41 | förskola, barn, barnomsorg, verksamhet, personal, pedagogisk, kommun, fritidshem | 4/4 | 0.914 | 0.882 | 0.556 |
| 42 | läkare, vård, omsorg, barngrupp, landsting, behov, läkarutbildning, örebro | 1/4 | 0.513 | 0.314 | 0.212 |
| 43 | stockholm, land, område, centrum, verksamhet, samarbete, kommun, södertörn | 0/4 | 0.421 | 0.276 | 0.153 |
| 44 | elev, lärare, grundskola, kunskap, undervisning, mål, nationell, betyg | 3/4 | 0.865 | 0.600 | 0.487 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5191
- Median: 0.5405
- Min: 0.0024
- Max: 0.9767
- Std Dev: 0.2979

**Jaccard Similarity (top 20 words):**
- Mean: 0.2293
- Median: 0.2121
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1806

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5189
- Median: 0.5437
- Min: 0.0001
- Max: 0.9866
- Std Dev: 0.3072

**Jaccard Similarity (top 20 words):**
- Mean: 0.2260
- Median: 0.1765
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1859

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5197
- Median: 0.4817
- Min: 0.0002
- Max: 0.9791
- Std Dev: 0.3223

**Jaccard Similarity (top 20 words):**
- Mean: 0.2409
- Median: 0.1943
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2073

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5371
- Median: 0.5992
- Min: 0.0001
- Max: 0.9771
- Std Dev: 0.3083

**Jaccard Similarity (top 20 words):**
- Mean: 0.2540
- Median: 0.2702
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1920

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5193
- Median: 0.5557
- Min: 0.0002
- Max: 0.9827
- Std Dev: 0.3140

**Jaccard Similarity (top 20 words):**
- Mean: 0.2444
- Median: 0.2500
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1905

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5658
- Median: 0.6453
- Min: 0.0007
- Max: 0.9908
- Std Dev: 0.3191

**Jaccard Similarity (top 20 words):**
- Mean: 0.2596
- Median: 0.1943
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2143

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5030
- Median: 0.5253
- Min: 0.0001
- Max: 0.9892
- Std Dev: 0.3151

**Jaccard Similarity (top 20 words):**
- Mean: 0.2249
- Median: 0.2121
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1815

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5549
- Median: 0.6499
- Min: 0.0002
- Max: 0.9901
- Std Dev: 0.3449

**Jaccard Similarity (top 20 words):**
- Mean: 0.2687
- Median: 0.2500
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2150

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.4855
- Median: 0.4758
- Min: 0.0025
- Max: 0.9806
- Std Dev: 0.3012

**Jaccard Similarity (top 20 words):**
- Mean: 0.2126
- Median: 0.1765
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1716

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5311
- Median: 0.5149
- Min: 0.0037
- Max: 0.9864
- Std Dev: 0.3200

**Jaccard Similarity (top 20 words):**
- Mean: 0.2487
- Median: 0.2121
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2012

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 440

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5254
- Median: 0.5615
- Min: 0.0001
- Max: 0.9908
- Std Dev: 0.3160

### Jaccard Similarity (across all matches)
- Mean: 0.2409
- Median: 0.2121
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.1952

## Key Change from Previous Analysis

Previous reports compared Topic 1 to Topic 1, Topic 2 to Topic 2, etc. across seeds.
This is methodologically invalid because topic indices are arbitrary.

This corrected analysis uses the Hungarian algorithm to find optimal topic correspondences
before computing similarities. The previous mean Jaccard value of ~0.02 reflected
invalid index-by-index comparison. The values above reflect matched topics.