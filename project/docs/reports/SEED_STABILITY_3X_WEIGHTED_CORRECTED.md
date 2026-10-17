# Seed-Stability Analysis: 3x Title-Weighted LDA (44 topics)

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Weighting:** Title words are appended three times to the body text

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 44 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 2152.39 | 50 |
| 123 | 2138.88 | 50 |
| 456 | 2120.67 | 50 |
| 789 | 2133.56 | 50 |
| 999 | 2119.41 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 10 |
| 3 of 4 | 3 |
| 2 of 4 | 6 |
| 1 of 4 | 4 |
| 0 of 4 | 21 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | arbetsmarknad, vuxenutbildning, behov, lärande, yrkesutbildning, arbete, arbetsliv, människa | 3/4 | 0.729 | 0.648 | 0.352 |
| 2 | arbetsmiljö, huvudman, styck, lagförslag, arbetsmiljölag, uppdrag, revisor, stänga | 0/4 | 0.064 | 0.001 | 0.049 |
| 3 | högskolebehörighet, sverige, försvar, skolavslutning, slu, offentlighetsprincip, samtycke, försvarshögskolan | 0/4 | 0.128 | 0.056 | 0.040 |
| 4 | hälsa, ung, kunskap, ungdom, mat, familj, många, samhälle | 2/4 | 0.758 | 0.665 | 0.523 |
| 5 | stat, statlig, kostnad, avgift, lån, finansiering, procent, ekonomisk | 0/4 | 0.394 | 0.091 | 0.191 |
| 6 | göteborg, universitet, borås, uppsala, västsverige, stockholm, institution, väst | 2/4 | 0.661 | 0.437 | 0.241 |
| 7 | mälardalens, mittuniversitet, genusforskning, ant, mitthögskola, gymnasiesärskolan, helårsstudent, implementera | 0/4 | 0.499 | 0.317 | 0.097 |
| 8 | barn, elev, stöd, behov, förälder, sexuell, funktionshind, särskild | 4/4 | 0.804 | 0.738 | 0.186 |
| 9 | högskola, behov, linje, resurs, liten, högskoleutbildning, kurs, lokal | 1/4 | 0.584 | 0.500 | 0.196 |
| 10 | student, studie, studiemedel, studiestöd, studerande, anslag, studera, fribelopp | 3/4 | 0.851 | 0.690 | 0.544 |
| 11 | vård, landsting, social, sjuksköterska, nordisk, behov, arbete, omsorg | 0/4 | 0.456 | 0.303 | 0.199 |
| 12 | fysisk, idrott, aktivitet, ämne, barn, ungdom, timme, rörelse | 4/4 | 0.802 | 0.718 | 0.329 |
| 13 | skövde, natur, miljö, grön, akademin, ekologisk, skaraborg, kooperativ | 0/4 | 0.395 | 0.317 | 0.194 |
| 14 | växjö, kristianstad, blekinge, ingenjörsutbildning, tuff, teknisk, karlskrona, fetma | 0/4 | 0.102 | 0.002 | 0.033 |
| 15 | land, svensk, hög, öka, många, ökad, förutsättning, låg | 0/4 | 0.602 | 0.541 | 0.170 |
| 16 | it, kränkning, kårobligatorium, studentinflytande, simundervisning, förening, medlem, kår | 0/4 | 0.319 | 0.049 | 0.190 |
| 17 | språk, svensk, svenska, undervisning, sfi, invandrare, modersmål, barngrupp | 4/4 | 0.822 | 0.703 | 0.392 |
| 18 | läkare, läkarutbildning, digital, läkemedel, samisk, finsk, behov, utbildningsplats | 0/4 | 0.178 | 0.025 | 0.075 |
| 19 | krav, enskild, ansvar, system, politisk, uppgift, mål, förändring | 2/4 | 0.689 | 0.456 | 0.194 |
| 20 | elev, gymnasieskola, betyg, ämne, kunskap, program, gymnasium, grundskola | 4/4 | 0.881 | 0.800 | 0.603 |
| 21 | karlstad, skolbibliotek, bibliotek, läromedel, tillgång, värmland, kostnadsfri, litteratur | 0/4 | 0.271 | 0.075 | 0.082 |
| 22 | barn, många, problem, dålig, brott, lag, vuxen, personal | 1/4 | 0.540 | 0.267 | 0.114 |
| 23 | lund, skåne, anläggning, gotland, ess, juridisk, marin, utrikes | 0/4 | 0.109 | 0.001 | 0.063 |
| 24 | högskola, gävle, distansutbildning, kalmar, län, kompetensförsörjning, härnösand, teologisk | 4/4 | 0.810 | 0.782 | 0.068 |
| 25 | lärlingsutbildning, professur, konstnärlig, lärling, musikhögskola, område, turism, inrättande | 0/4 | 0.221 | 0.035 | 0.081 |
| 26 | samhälle, kunskap, människa, undervisning, läroplan, ämne, rättighet, demokratisk | 4/4 | 0.830 | 0.748 | 0.485 |
| 27 | kommun, elev, fristående, kommunal, friskola, välja, förälder, skollag | 4/4 | 0.939 | 0.891 | 0.657 |
| 28 | högskola, universitet, forskning, student, hög, lärosäte, kvalitet, nivå | 3/4 | 0.750 | 0.272 | 0.344 |
| 29 | lokal, styrelse, bok, använda, digitalisering, information, akademi, gammal | 0/4 | 0.204 | 0.140 | 0.082 |
| 30 | verksamhet, anslag, grundskola, särskild, gymnasieskola, undervisning, statsbidrag, bidrag | 0/4 | 0.530 | 0.302 | 0.233 |
| 31 | körkort, körkortsutbildning, examensrätt, maskinskrivning, många, programmering, kostnad, arbete | 0/4 | 0.127 | 0.009 | 0.083 |
| 32 | mobbning, elev, skolinspektion, arbete, våld, ung, rektor, lärare | 2/4 | 0.643 | 0.405 | 0.298 |
| 33 | kvinna, jämställdhet, flicka, pojke, kön, kvinnlig, manlig, jämställdhetsarbete | 4/4 | 0.929 | 0.803 | 0.442 |
| 34 | forskning, forskare, utveckling, område, svensk, medel, resurs, nationell | 4/4 | 0.959 | 0.940 | 0.510 |
| 35 | hälsa, sjukdom, psykisk, medicinsk, ohälsa, vård, sjukvård, klinisk | 1/4 | 0.611 | 0.476 | 0.226 |
| 36 | plats, poäng, studielån, utbildningsplats, dimensionering, termin, sökande, exam | 0/4 | 0.451 | 0.245 | 0.162 |
| 37 | kultur, historia, musik, svensk, historisk, nationell, kulturarv, kulturell | 0/4 | 0.405 | 0.215 | 0.139 |
| 38 | bild, lärarledd, ämne, yrkeshögskoleutbildning, kritisk, tänkande, konstfack, undervisning | 0/4 | 0.133 | 0.000 | 0.059 |
| 39 | regional, län, region, näringsliv, utveckling, hög, företag, jönköping | 0/4 | 0.476 | 0.040 | 0.179 |
| 40 | företag, teknik, teknisk, industri, näringsliv, samarbete, utveckla, driva | 1/4 | 0.508 | 0.074 | 0.229 |
| 41 | lärare, lärarutbildning, pedagogisk, barnomsorg, läraryrke, kompetens, förskollärare, arbetstid | 4/4 | 0.929 | 0.906 | 0.292 |
| 42 | universitet, umeå, örebro, linköping, land, norrland, institutet, stockholm | 2/4 | 0.728 | 0.668 | 0.255 |
| 43 | stockholm, malmö, södertörn, centrum, södra, region, land, kommun | 0/4 | 0.303 | 0.032 | 0.108 |
| 44 | elev, barn, förskola, lärare, förälder, nationell, grundskola, utveckla | 2/4 | 0.695 | 0.652 | 0.325 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5332
- Median: 0.5885
- Min: 0.0002
- Max: 0.9666
- Std Dev: 0.2833

**Jaccard Similarity (top 20 words):**
- Mean: 0.2222
- Median: 0.2121
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1579

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5299
- Median: 0.5884
- Min: 0.0011
- Max: 0.9818
- Std Dev: 0.3019

**Jaccard Similarity (top 20 words):**
- Mean: 0.2345
- Median: 0.1943
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1923

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5508
- Median: 0.6480
- Min: 0.0101
- Max: 0.9840
- Std Dev: 0.3096

**Jaccard Similarity (top 20 words):**
- Mean: 0.2493
- Median: 0.2121
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.1831

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5514
- Median: 0.5734
- Min: 0.0013
- Max: 0.9829
- Std Dev: 0.3067

**Jaccard Similarity (top 20 words):**
- Mean: 0.2316
- Median: 0.1765
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2034

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5378
- Median: 0.5118
- Min: 0.0073
- Max: 0.9919
- Std Dev: 0.3340

**Jaccard Similarity (top 20 words):**
- Mean: 0.2427
- Median: 0.1429
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2294

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5279
- Median: 0.5445
- Min: 0.0029
- Max: 0.9914
- Std Dev: 0.3047

**Jaccard Similarity (top 20 words):**
- Mean: 0.2540
- Median: 0.1943
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2083

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5213
- Median: 0.5790
- Min: 0.0017
- Max: 0.9601
- Std Dev: 0.3066

**Jaccard Similarity (top 20 words):**
- Mean: 0.2315
- Median: 0.1429
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2079

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5473
- Median: 0.5884
- Min: 0.0099
- Max: 0.9943
- Std Dev: 0.3091

**Jaccard Similarity (top 20 words):**
- Mean: 0.2207
- Median: 0.1429
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1995

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5407
- Median: 0.6061
- Min: 0.0057
- Max: 0.9273
- Std Dev: 0.2851

**Jaccard Similarity (top 20 words):**
- Mean: 0.2387
- Median: 0.1765
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1885

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5541
- Median: 0.5961
- Min: 0.0016
- Max: 0.9799
- Std Dev: 0.3169

**Jaccard Similarity (top 20 words):**
- Mean: 0.2379
- Median: 0.1597
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2131

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 440

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5394
- Median: 0.5909
- Min: 0.0002
- Max: 0.9943
- Std Dev: 0.3063

### Jaccard Similarity (across all matches)
- Mean: 0.2363
- Median: 0.1765
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.1995

## Comparison to Baseline

Compare these values to the baseline 44-topic model (BASELINE_STABILITY_44TOPICS_CORRECTED.md)
to assess whether title weighting improves topic stability across random seeds.