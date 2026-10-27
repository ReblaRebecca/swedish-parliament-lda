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
| 42 | 1988.00 | 50 |
| 123 | 2003.19 | 50 |
| 456 | 1957.99 | 50 |
| 789 | 1988.17 | 50 |
| 999 | 1970.52 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 8 |
| 3 of 4 | 1 |
| 2 of 4 | 7 |
| 1 of 4 | 4 |
| 0 of 4 | 12 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | sexuell, it, sexualitet, samlevnadsundervisning, person, använda, allians, må | 0/4 | 0.116 | 0.020 | 0.041 |
| 2 | förslag, kommun, verksamhet, resurs, lokal, medel, särskild, anslag | 0/4 | 0.540 | 0.451 | 0.195 |
| 3 | kunskap, mat, elev, ämne, hälsa, hemkunskap, ekonomi, kost | 2/4 | 0.564 | 0.320 | 0.283 |
| 4 | kränkning, djur, rekommendation, djurförsök, försvar, konvention, hyra, sverige | 0/4 | 0.163 | 0.050 | 0.104 |
| 5 | högskola, universitet, forskning, anslag, forskarutbildning, nivå, hög, kvalitet | 4/4 | 0.873 | 0.816 | 0.312 |
| 6 | simundervisning, tfhs, simkunnighet, tilläggsbelopp, simma, programmering, aren, superdator | 0/4 | 0.193 | 0.071 | 0.152 |
| 7 | lärare, lärarutbildning, kompetens, behov, pedagogisk, krav, brist, yrke | 2/4 | 0.740 | 0.591 | 0.217 |
| 8 | arbetsmarknad, vuxenutbildning, behov, hög, yrkesutbildning, lärande, arbetsliv, människa | 3/4 | 0.787 | 0.626 | 0.499 |
| 9 | lärlingsutbildning, lärling, akademin, stiftelse, företagare, gymnasieexam, yrkesexam, yrke | 0/4 | 0.392 | 0.197 | 0.264 |
| 10 | universitet, göteborg, umeå, lund, land, uppsala, borås, stockholm | 1/4 | 0.544 | 0.340 | 0.161 |
| 11 | barn, förälder, ungdom, behov, stöd, grupp, ung, problem | 4/4 | 0.820 | 0.703 | 0.246 |
| 12 | gymnasieskola, ämne, program, kurs, språk, gymnasium, ungdom, linje | 2/4 | 0.657 | 0.571 | 0.323 |
| 13 | samhälle, människa, undervisning, värde, religiös, etisk, läroplan, kunskap | 1/4 | 0.633 | 0.587 | 0.343 |
| 14 | skolverket, skolverk, förskoleklass, gymnasieprogram, utvärdering, kvalitetsinstitut, ant, kvalitetsredovisning | 0/4 | 0.180 | 0.000 | 0.033 |
| 15 | kvinna, mobbning, flicka, arbete, våld, jämställdhet, pojke, åtgärd | 1/4 | 0.645 | 0.534 | 0.195 |
| 16 | hälsa, vård, läkare, sjukvård, sjukdom, medicinsk, ohälsa, landsting | 4/4 | 0.757 | 0.719 | 0.326 |
| 17 | stockholm, örebro, institutet, mälardalens, västerås, karolinsk, högskola, stockholmsregionen | 0/4 | 0.401 | 0.265 | 0.112 |
| 18 | högskola, län, region, utveckling, företag, teknisk, hög, regional | 4/4 | 0.817 | 0.719 | 0.590 |
| 19 | forskning, forskare, svensk, utveckling, område, internationell, grundnivå, universitet | 4/4 | 0.890 | 0.810 | 0.440 |
| 20 | läsa, betyg, prov, svenska, elev, modersmål, svensk, andraspråk | 0/4 | 0.295 | 0.185 | 0.130 |
| 21 | lag, ersättning, lagstiftning, kostnad, bestämmelse, regel, körkort, avtal | 0/4 | 0.276 | 0.112 | 0.124 |
| 22 | fysisk, idrott, aktivitet, hälsa, ämne, timme, fritid, ungdom | 4/4 | 0.838 | 0.757 | 0.368 |
| 23 | förskola, kommun, barn, fristående, kommunal, verksamhet, förälder, friskola | 2/4 | 0.624 | 0.177 | 0.310 |
| 24 | svensk, språk, undervisning, sfi, invandrare, svenska, digital, jobb | 2/4 | 0.583 | 0.097 | 0.235 |
| 25 | kultur, jobba, bild, digitalisering, medie, tuff, konstfack, tv | 0/4 | 0.099 | 0.010 | 0.034 |
| 26 | land, kunskap, svensk, samhälle, hög, utveckling, människa, utveckla | 0/4 | 0.587 | 0.511 | 0.262 |
| 27 | elev, särskola, specialskola, stöd, behov, läromedel, hörselskadad, särskild | 2/4 | 0.555 | 0.192 | 0.207 |
| 28 | falun, turism, borlänge, trafik, läkemedel, dalarna, skoglig, högskolelektor | 0/4 | 0.136 | 0.057 | 0.061 |
| 29 | avancerad, satsning, särskild, myndighet, specialpedagogisk, neuropsykiatrisk, följd, utanförskapsområde | 2/4 | 0.411 | 0.001 | 0.055 |
| 30 | elev, lärare, grundskola, undervisning, kunskap, nationell, betyg, mål | 4/4 | 0.894 | 0.786 | 0.435 |
| 31 | skolinspektion, elevhälsa, riksrevision, uf, hbt, handlingsplan, homosexuell, bisexuell | 1/4 | 0.245 | 0.014 | 0.135 |
| 32 | student, hög, studie, studiemedel, studerande, studera, system, förslag | 4/4 | 0.885 | 0.763 | 0.488 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5499
- Median: 0.7031
- Min: 0.0001
- Max: 0.9664
- Std Dev: 0.2845

**Jaccard Similarity (top 20 words):**
- Mean: 0.2512
- Median: 0.1943
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1913

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5692
- Median: 0.5977
- Min: 0.0142
- Max: 0.9647
- Std Dev: 0.2889

**Jaccard Similarity (top 20 words):**
- Mean: 0.2648
- Median: 0.2500
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.1746

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5128
- Median: 0.6011
- Min: 0.0007
- Max: 0.9571
- Std Dev: 0.3067

**Jaccard Similarity (top 20 words):**
- Mean: 0.2104
- Median: 0.1943
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1515

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5105
- Median: 0.5888
- Min: 0.0001
- Max: 0.9669
- Std Dev: 0.3230

**Jaccard Similarity (top 20 words):**
- Mean: 0.2339
- Median: 0.2121
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1719

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5883
- Median: 0.6086
- Min: 0.0005
- Max: 0.9787
- Std Dev: 0.2836

**Jaccard Similarity (top 20 words):**
- Mean: 0.2728
- Median: 0.2311
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1935

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.4856
- Median: 0.5454
- Min: 0.0007
- Max: 0.9215
- Std Dev: 0.2807

**Jaccard Similarity (top 20 words):**
- Mean: 0.2085
- Median: 0.1943
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1517

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5654
- Median: 0.6575
- Min: 0.0074
- Max: 0.9643
- Std Dev: 0.2977

**Jaccard Similarity (top 20 words):**
- Mean: 0.2561
- Median: 0.2121
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1785

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.4852
- Median: 0.4623
- Min: 0.0133
- Max: 0.9151
- Std Dev: 0.3008

**Jaccard Similarity (top 20 words):**
- Mean: 0.1995
- Median: 0.1597
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1750

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5755
- Median: 0.6876
- Min: 0.0171
- Max: 0.9847
- Std Dev: 0.3160

**Jaccard Similarity (top 20 words):**
- Mean: 0.2811
- Median: 0.2702
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2036

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.4883
- Median: 0.5636
- Min: 0.0005
- Max: 0.9123
- Std Dev: 0.2884

**Jaccard Similarity (top 20 words):**
- Mean: 0.2057
- Median: 0.1765
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1418

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 320

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5331
- Median: 0.6032
- Min: 0.0001
- Max: 0.9847
- Std Dev: 0.2999

### Jaccard Similarity (across all matches)
- Mean: 0.2384
- Median: 0.2121
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1768
