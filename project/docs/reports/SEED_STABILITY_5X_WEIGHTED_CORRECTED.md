# Seed-Stability Analysis: 5x Title-Weighted LDA (44 topics)

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Weighting:** Title words are appended five times to the body text

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 44 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 2114.68 | 50 |
| 123 | 2124.48 | 50 |
| 456 | 2084.49 | 50 |
| 789 | 2097.90 | 50 |
| 999 | 2104.91 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 7 |
| 3 of 4 | 7 |
| 2 of 4 | 6 |
| 1 of 4 | 6 |
| 0 of 4 | 18 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | arbetsmarknad, vuxenutbildning, behov, lärande, yrkesutbildning, människa, hög, arbete | 3/4 | 0.730 | 0.533 | 0.295 |
| 2 | arbetsmiljö, simundervisning, arbetsmiljölag, revisor, styck, elevskyddsombud, simkunnighet, definition | 0/4 | 0.117 | 0.001 | 0.042 |
| 3 | lärlingsutbildning, lärling, högskolebehörighet, skolavslutning, information, matchning, kvalitetsinstitut, nationell | 1/4 | 0.349 | 0.001 | 0.069 |
| 4 | kunskap, ung, ungdom, mat, hälsa, många, privatekonomi, hemkunskap | 2/4 | 0.730 | 0.571 | 0.492 |
| 5 | stat, statlig, kostnad, avgift, procent, finansiering, ekonomisk, verksamhet | 1/4 | 0.483 | 0.073 | 0.215 |
| 6 | universitet, göteborg, professur, lund, uppsala, stockholm, borås, institution | 1/4 | 0.585 | 0.334 | 0.252 |
| 7 | mälardalens, mittuniversitet, genusforskning, ant, mitthögskola, helårsstudent, gymnasiesärskolan, takbelopp | 0/4 | 0.451 | 0.276 | 0.106 |
| 8 | elev, stöd, behov, sexuell, särskola, särskild, funktionsnedsättning, funktionshind | 2/4 | 0.549 | 0.185 | 0.249 |
| 9 | högskola, behov, linje, plats, resurs, lokal, kurs, stockholm | 1/4 | 0.600 | 0.411 | 0.203 |
| 10 | student, anslag, studiemedel, studie, studiestöd, bidrag, utgiftsområde, fribelopp | 3/4 | 0.763 | 0.577 | 0.412 |
| 11 | digital, vård, sjuksköterska, behov, arbete, personal, kompetens, legitimation | 0/4 | 0.298 | 0.027 | 0.179 |
| 12 | ämne, idrott, fysisk, aktivitet, hälsa, grundskola, timme, ungdom | 2/4 | 0.652 | 0.445 | 0.313 |
| 13 | social, lärosäten, lag, lagstiftning, yrkesvägledning, myndighet, hbt, socialtjänst | 0/4 | 0.284 | 0.004 | 0.106 |
| 14 | företag, entreprenörskap, ung, starta, växjö, blekinge, kristianstad, ingenjörsutbildning | 0/4 | 0.352 | 0.001 | 0.085 |
| 15 | kommun, barnomsorg, förskola, verksamhet, behov, land, erbjuda, kvalitet | 0/4 | 0.478 | 0.362 | 0.274 |
| 16 | örebro, karlstad, västsverige, kårobligatorium, kränkning, stockholmsregionen, väst, värmland | 0/4 | 0.096 | 0.067 | 0.053 |
| 17 | språk, svensk, land, modersmål, utländsk, svenska, teckenspråk, undervisning | 2/4 | 0.698 | 0.569 | 0.371 |
| 18 | invandrare, sfi, svensk, undervisning, svenska, nyanländ, svenskundervisning, samisk | 3/4 | 0.783 | 0.655 | 0.422 |
| 19 | ansvar, system, krav, enskild, politisk, förändring, uppgift, problem | 3/4 | 0.762 | 0.671 | 0.229 |
| 20 | elev, gymnasieskola, program, kunskap, gymnasium, betyg, ungdom, kurs | 4/4 | 0.905 | 0.829 | 0.529 |
| 21 | skolbibliotek, bibliotek, tillgång, bok, utfärda, byggande, material, skoglig | 0/4 | 0.276 | 0.017 | 0.078 |
| 22 | barn, förälder, många, ungdom, vuxen, familj, personal, problem | 4/4 | 0.864 | 0.785 | 0.160 |
| 23 | finland, anläggning, norden, ess, marin, förstärkd, östersjön, hav | 0/4 | 0.060 | 0.000 | 0.026 |
| 24 | högskola, län, gävle, region, utveckling, kalmar, distansutbildning, högskoleutbildning | 3/4 | 0.748 | 0.261 | 0.201 |
| 25 | läkare, läkarutbildning, utbildningsplats, konstnärlig, landsting, land, musikhögskola, fritid | 0/4 | 0.506 | 0.328 | 0.271 |
| 26 | samhälle, människa, kunskap, undervisning, läroplan, rättighet, demokratisk, svensk | 4/4 | 0.818 | 0.730 | 0.487 |
| 27 | fristående, elev, kommun, kommunal, friskola, välja, bidrag, skollag | 3/4 | 0.845 | 0.560 | 0.509 |
| 28 | högskola, universitet, student, hög, lärosäte, kvalitet, nivå, forskning | 2/4 | 0.712 | 0.465 | 0.346 |
| 29 | styrelse, lokal, teologisk, verksamhet, akademi, akademin, förening, demokratisk | 0/4 | 0.161 | 0.008 | 0.080 |
| 30 | miljö, skövde, natur, kunskap, område, ekologisk, grön, utveckling | 0/4 | 0.402 | 0.044 | 0.124 |
| 31 | körkort, körkortsutbildning, entreprenör, examensrätt, högskoleverk, maskinskrivning, läsförståelse, många | 0/4 | 0.222 | 0.005 | 0.053 |
| 32 | mobbning, elev, arbete, skolinspektion, ung, våld, lärare, rektor | 1/4 | 0.593 | 0.342 | 0.238 |
| 33 | kvinna, jämställdhet, flicka, pojke, kön, kvinnlig, manlig, genusperspektiv | 4/4 | 0.913 | 0.815 | 0.425 |
| 34 | forskning, forskare, utveckling, svensk, område, satsning, internationell, medel | 4/4 | 0.926 | 0.863 | 0.474 |
| 35 | hälsa, sjukdom, medicinsk, psykisk, ohälsa, sjukvård, förebyggande, vård | 3/4 | 0.672 | 0.465 | 0.383 |
| 36 | lån, studielån, poäng, termin, alternativ, studerande, djurförsök, lång | 0/4 | 0.084 | 0.011 | 0.053 |
| 37 | nationell, kultur, historia, musik, svensk, historisk, land, kulturskola | 2/4 | 0.540 | 0.267 | 0.126 |
| 38 | ämne, bild, estetisk, lärarledd, digitalisering, yrkeshögskoleutbildning, undervisning, kritisk | 0/4 | 0.240 | 0.020 | 0.088 |
| 39 | regional, region, liten, jönköping, land, näringsliv, tillväxt, kompetensförsörjning | 0/4 | 0.412 | 0.182 | 0.183 |
| 40 | teknisk, företag, teknik, it, näringsliv, industri, samarbete, bransch | 0/4 | 0.398 | 0.325 | 0.168 |
| 41 | lärare, lärarutbildning, pedagogisk, läraryrke, kompetens, förskollärare, behörig, ämne | 4/4 | 0.898 | 0.833 | 0.371 |
| 42 | umeå, universitet, linköping, luleå, land, norrland, djur, ort | 1/4 | 0.493 | 0.313 | 0.138 |
| 43 | stockholm, malmö, södertörn, centrum, södra, region, hög, land | 0/4 | 0.449 | 0.214 | 0.212 |
| 44 | elev, förskola, lärare, grundskola, barn, kunskap, undervisning, nationell | 4/4 | 0.838 | 0.736 | 0.348 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5218
- Median: 0.5353
- Min: 0.0019
- Max: 0.9846
- Std Dev: 0.2994

**Jaccard Similarity (top 20 words):**
- Mean: 0.2133
- Median: 0.1765
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1623

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5733
- Median: 0.6523
- Min: 0.0010
- Max: 0.9278
- Std Dev: 0.2934

**Jaccard Similarity (top 20 words):**
- Mean: 0.2465
- Median: 0.2311
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1945

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5274
- Median: 0.5540
- Min: 0.0008
- Max: 0.9825
- Std Dev: 0.2900

**Jaccard Similarity (top 20 words):**
- Mean: 0.2309
- Median: 0.1943
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1689

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5353
- Median: 0.5472
- Min: 0.0002
- Max: 0.9720
- Std Dev: 0.3141

**Jaccard Similarity (top 20 words):**
- Mean: 0.2584
- Median: 0.2500
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1906

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5366
- Median: 0.6222
- Min: 0.0002
- Max: 0.9935
- Std Dev: 0.3362

**Jaccard Similarity (top 20 words):**
- Mean: 0.2529
- Median: 0.1597
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2169

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5056
- Median: 0.4814
- Min: 0.0004
- Max: 0.9807
- Std Dev: 0.3061

**Jaccard Similarity (top 20 words):**
- Mean: 0.2371
- Median: 0.1597
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2150

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5119
- Median: 0.5358
- Min: 0.0001
- Max: 0.9792
- Std Dev: 0.3018

**Jaccard Similarity (top 20 words):**
- Mean: 0.2327
- Median: 0.1429
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2065

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5685
- Median: 0.6011
- Min: 0.0034
- Max: 0.9796
- Std Dev: 0.2916

**Jaccard Similarity (top 20 words):**
- Mean: 0.2370
- Median: 0.1943
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1739

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5418
- Median: 0.5517
- Min: 0.0028
- Max: 0.9477
- Std Dev: 0.2681

**Jaccard Similarity (top 20 words):**
- Mean: 0.2286
- Median: 0.1765
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1848

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5709
- Median: 0.5732
- Min: 0.0231
- Max: 0.9787
- Std Dev: 0.2817

**Jaccard Similarity (top 20 words):**
- Mean: 0.2488
- Median: 0.2121
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2046

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 440

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5393
- Median: 0.5716
- Min: 0.0001
- Max: 0.9935
- Std Dev: 0.2997

### Jaccard Similarity (across all matches)
- Mean: 0.2386
- Median: 0.1765
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.1931

## Comparison to Baseline

Compare these values to the baseline 44-topic model (BASELINE_STABILITY_44TOPICS_CORRECTED.md)
to assess whether title weighting improves topic stability across random seeds.