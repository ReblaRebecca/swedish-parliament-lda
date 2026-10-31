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
| 42 | 1958.69 | 50 |
| 123 | 1952.12 | 50 |
| 456 | 1956.00 | 50 |
| 789 | 1938.99 | 50 |
| 999 | 1975.54 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 7 |
| 3 of 4 | 3 |
| 2 of 4 | 1 |
| 1 of 4 | 6 |
| 0 of 4 | 15 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | kvinna, jämställdhet, flicka, pojke, kön, kvinnlig, manlig, kvinnoforskning | 3/4 | 0.862 | 0.612 | 0.321 |
| 2 | adhd, hjärt, autism, diabetes, kärlsjukdom, indikator, stamning, hemundervisning | 0/4 | 0.004 | 0.001 | 0.006 |
| 3 | forskning, högskola, universitet, anslag, forskarutbildning, medel, förslag, verksamhet | 4/4 | 0.861 | 0.746 | 0.454 |
| 4 | ämne, kunskap, undervisning, elev, grundskola, ungdom, läroplan, ung | 1/4 | 0.684 | 0.592 | 0.302 |
| 5 | läkare, sjukvård, vård, medicinsk, hälsa, läkarutbildning, klinisk, patient | 1/4 | 0.571 | 0.407 | 0.294 |
| 6 | gymnasieskola, program, elev, kurs, yrkesutbildning, gymnasium, kunskap, krav | 1/4 | 0.715 | 0.614 | 0.389 |
| 7 | forskning, utveckling, svensk, lärosäte, hög, internationell, kvalitet, stärka | 2/4 | 0.663 | 0.373 | 0.306 |
| 8 | åtgärd, lag, skolverk, lärare, uppdrag, rektor, problem, myndighet | 0/4 | 0.310 | 0.202 | 0.106 |
| 9 | kommun, fristående, kommunal, skolverk, verksamhet, bidrag, förslag, stat | 4/4 | 0.868 | 0.844 | 0.471 |
| 10 | samhälle, människa, kunskap, svensk, land, utveckling, arbete, social | 1/4 | 0.713 | 0.627 | 0.282 |
| 11 | land, arbetsmarknad, hög, företag, jobb, ung, kompetens, person | 1/4 | 0.602 | 0.548 | 0.293 |
| 12 | stockholm, uppsala, teologisk, lokal, södertälje, anläggning, verksamhet, hyra | 0/4 | 0.272 | 0.076 | 0.061 |
| 13 | lärare, lärarutbildning, pedagogisk, undervisning, ämne, fortbildning, läraryrke, kunskap | 4/4 | 0.878 | 0.798 | 0.336 |
| 14 | mat, läromedel, allians, äta, ungdom, skolmat, skolsköterska, bok | 0/4 | 0.385 | 0.183 | 0.188 |
| 15 | språk, svensk, undervisning, svenska, invandrare, sfi, modersmål, nyanländ | 3/4 | 0.721 | 0.174 | 0.329 |
| 16 | elev, lärare, grundskola, betyg, undervisning, nationell, kunskap, stöd | 4/4 | 0.896 | 0.836 | 0.355 |
| 17 | behov, stöd, särskild, särskola, funktionshind, barngrupp, kompetens, specialskola | 0/4 | 0.367 | 0.255 | 0.112 |
| 18 | social, vård, landsting, omsorg, vårdutbildning, vårdhögskola, huvudmannaskap, sjuksköterska | 0/4 | 0.213 | 0.011 | 0.105 |
| 19 | lärcentrum, rekryteringsbidrag, hbt, homosexuell, bisexuell, transperson, östersjön, marin | 0/4 | 0.121 | 0.015 | 0.047 |
| 20 | barn, förskola, förälder, kommun, verksamhet, personal, barnomsorg, behov | 4/4 | 0.909 | 0.762 | 0.589 |
| 21 | högskola, län, region, plats, utveckling, teknisk, hög, behov | 4/4 | 0.915 | 0.878 | 0.611 |
| 22 | förskoleklass, validering, kvalitetsinstitut, lovskola, skolavslutning, simundervisning, svensk, transparent | 0/4 | 0.217 | 0.005 | 0.091 |
| 23 | student, högskola, hög, studie, förslag, studerande, studiemedel, system | 4/4 | 0.897 | 0.855 | 0.440 |
| 24 | entreprenörskap, kalmar, bibliotek, företagande, turism, starta, kooperativ, natt | 0/4 | 0.120 | 0.013 | 0.066 |
| 25 | psykisk, sjukdom, arbetsmiljö, problem, ohälsa, kränkning, drabba, behandling | 0/4 | 0.409 | 0.279 | 0.191 |
| 26 | göteborg, skövde, konstnärlig, västsverige, skaraborg, region, fjärrundervisning, trollhättan | 0/4 | 0.290 | 0.144 | 0.083 |
| 27 | skolinspektion, elevhälsa, alkohol, handlingsplan, tuff, ant, fetma, tobak | 3/4 | 0.745 | 0.343 | 0.154 |
| 28 | mälardalens, riksrevision, etisk, djur, djurförsök, alternativ, fn, metod | 0/4 | 0.228 | 0.086 | 0.072 |
| 29 | nivå, universitet, forskarnivå, lund, linköping, nordisk, högskolebehörighet, poäng | 0/4 | 0.278 | 0.154 | 0.112 |
| 30 | vuxenutbildning, folkhögskola, vuxen, komvux, studieförbund, folkbildning, verksamhet, bidrag | 1/4 | 0.545 | 0.151 | 0.228 |
| 31 | örebro, barn, hörselskadad, ekeskola, synskadad, uf, hjälpmedel, rörelsehindrad | 0/4 | 0.217 | 0.000 | 0.033 |
| 32 | mobbning, barn, fysisk, idrott, ungdom, våld, aktivitet, hälsa | 0/4 | 0.542 | 0.425 | 0.233 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5252
- Median: 0.5554
- Min: 0.0049
- Max: 0.9919
- Std Dev: 0.3134

**Jaccard Similarity (top 20 words):**
- Mean: 0.2475
- Median: 0.2121
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2120

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5551
- Median: 0.6191
- Min: 0.0006
- Max: 0.9564
- Std Dev: 0.3101

**Jaccard Similarity (top 20 words):**
- Mean: 0.2419
- Median: 0.1765
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1928

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5433
- Median: 0.6086
- Min: 0.0004
- Max: 0.9735
- Std Dev: 0.3219

**Jaccard Similarity (top 20 words):**
- Mean: 0.2667
- Median: 0.2500
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2143

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5036
- Median: 0.5422
- Min: 0.0014
- Max: 0.9510
- Std Dev: 0.3149

**Jaccard Similarity (top 20 words):**
- Mean: 0.2016
- Median: 0.1765
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1622

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5469
- Median: 0.6186
- Min: 0.0272
- Max: 0.9449
- Std Dev: 0.2881

**Jaccard Similarity (top 20 words):**
- Mean: 0.2386
- Median: 0.2500
- Min: 0.0256
- Max: 0.5385
- Std Dev: 0.1574

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5584
- Median: 0.6280
- Min: 0.0029
- Max: 0.9322
- Std Dev: 0.3150

**Jaccard Similarity (top 20 words):**
- Mean: 0.2420
- Median: 0.2121
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1906

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5242
- Median: 0.5062
- Min: 0.0009
- Max: 0.9463
- Std Dev: 0.2946

**Jaccard Similarity (top 20 words):**
- Mean: 0.1985
- Median: 0.1765
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1540

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5248
- Median: 0.6202
- Min: 0.0038
- Max: 0.9779
- Std Dev: 0.3530

**Jaccard Similarity (top 20 words):**
- Mean: 0.2217
- Median: 0.1943
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1933

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5540
- Median: 0.6314
- Min: 0.0060
- Max: 0.9752
- Std Dev: 0.2986

**Jaccard Similarity (top 20 words):**
- Mean: 0.2181
- Median: 0.2121
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.1703

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5917
- Median: 0.6922
- Min: 0.0010
- Max: 0.9760
- Std Dev: 0.3398

**Jaccard Similarity (top 20 words):**
- Mean: 0.2478
- Median: 0.2121
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1848

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 320

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5427
- Median: 0.6129
- Min: 0.0004
- Max: 0.9919
- Std Dev: 0.3164

### Jaccard Similarity (across all matches)
- Mean: 0.2324
- Median: 0.2121
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.1855
