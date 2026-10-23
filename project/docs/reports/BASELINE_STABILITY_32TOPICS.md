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
| 42 | 2013.67 | 50 |
| 123 | 2007.30 | 50 |
| 456 | 1987.44 | 50 |
| 789 | 2011.15 | 50 |
| 999 | 1998.94 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 3 |
| 3 of 4 | 8 |
| 2 of 4 | 4 |
| 1 of 4 | 4 |
| 0 of 4 | 13 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | svensk, språk, land, internationell, konfessionell, utomlands, välja, engelsk | 3/4 | 0.787 | 0.684 | 0.163 |
| 2 | ung, ungdom, psykisk, sexuell, ohälsa, barn, sjukdom, person | 0/4 | 0.395 | 0.091 | 0.192 |
| 3 | förskola, barn, kommun, förälder, barnomsorg, verksamhet, personal, pedagogisk | 3/4 | 0.759 | 0.259 | 0.512 |
| 4 | lärare, lärarutbildning, pedagogisk, rektor, fortbildning, kompetens, undervisa, arbeta | 3/4 | 0.860 | 0.619 | 0.261 |
| 5 | samhälle, människa, undervisning, idébur, läroplan, kultur, demokratisk, fråga | 3/4 | 0.840 | 0.649 | 0.651 |
| 6 | elev, mobbning, betyg, prov, nationell, våld, arbete, lärare | 1/4 | 0.530 | 0.119 | 0.313 |
| 7 | gymnasieskola, kurs, program, krav, behov, poäng, hög, arbetsmarknad | 2/4 | 0.629 | 0.400 | 0.266 |
| 8 | mat, ämne, hälsa, kost, kunskap, hemkunskap, skolmat, äta | 0/4 | 0.579 | 0.493 | 0.242 |
| 9 | elev, kunskap, grundskola, undervisning, mål, ämne, lärare, många | 4/4 | 0.960 | 0.934 | 0.523 |
| 10 | lund, kalmar, professur, dalarna, turism, falun, skåne, mittuniversitet | 0/4 | 0.229 | 0.095 | 0.117 |
| 11 | ersättning, alliansregering, merkostnad, tillstånd, natt, prövning, samtycke, offentlighetsprincip | 0/4 | 0.015 | 0.002 | 0.028 |
| 12 | svensk, undervisning, ämne, svenska, stärka, sfi, årskurs, invandrare | 0/4 | 0.461 | 0.211 | 0.150 |
| 13 | kvinna, många, problem, samhälle, kunskap, arbete, handla, använda | 1/4 | 0.617 | 0.480 | 0.218 |
| 14 | barn, förälder, familj, teckenspråk, social, döv, språk, många | 3/4 | 0.590 | 0.007 | 0.136 |
| 15 | skolinspektion, elevhälsa, utreda, friskolesektor, validering, gymnasieprogram, högskolebehörighet, tillsyn | 1/4 | 0.219 | 0.004 | 0.026 |
| 16 | fysisk, idrott, aktivitet, hälsa, barn, ungdom, rörelse, fritid | 3/4 | 0.837 | 0.578 | 0.473 |
| 17 | forskning, svensk, eu, område, stärka, miljö, teknik, sverige | 0/4 | 0.495 | 0.352 | 0.248 |
| 18 | län, högskola, region, universitet, stockholm, behov, utveckling, land | 2/4 | 0.688 | 0.646 | 0.397 |
| 19 | högskola, anslag, plats, avancerad, nivå, teknisk, örebro, budgetår | 3/4 | 0.721 | 0.338 | 0.174 |
| 20 | hbt, undervisning, ant, bisexuell, homosexuell, transperson, adhd, folkmord | 0/4 | 0.257 | 0.001 | 0.121 |
| 21 | it, digitalisering, utanförskap, allians, lärcentrum, stork, myndighet, kvalitetsinstitut | 0/4 | 0.072 | 0.053 | 0.032 |
| 22 | ung, företag, vinstdrivande, musik, starta, uf, skolkoncern, kulturskola | 0/4 | 0.164 | 0.015 | 0.093 |
| 23 | malmö, nordisk, land, minoritet, samisk, finsk, nationell, finland | 0/4 | 0.163 | 0.096 | 0.068 |
| 24 | vinst, stat, statlig, göteborg, privat, verksamhet, avtal, huvudmannaskap | 0/4 | 0.359 | 0.130 | 0.141 |
| 25 | kommun, elev, fristående, kommunal, verksamhet, friskola, huvudma, skolverket | 4/4 | 0.919 | 0.857 | 0.494 |
| 26 | utgiftsområde, vetenskapsråd, riksrevision, avvikelse, genusforskning, science, genusperspektiv, fritidsverksamhet | 0/4 | 0.206 | 0.073 | 0.040 |
| 27 | forskning, högskola, universitet, lärosäte, student, hög, anslag, forskare | 4/4 | 0.895 | 0.838 | 0.532 |
| 28 | vård, hälsa, läkare, sjukvård, medicinsk, landsting, behov, gammal | 2/4 | 0.674 | 0.491 | 0.380 |
| 29 | utveckling, hög, land, företag, utveckla, öka, nationell, svensk | 2/4 | 0.700 | 0.544 | 0.339 |
| 30 | elev, stöd, behov, särskild, funktionshind, särskola, digital, specialskola | 1/4 | 0.370 | 0.168 | 0.153 |
| 31 | student, studie, hög, studera, vuxenutbildning, människa, studiemedel, studerande | 3/4 | 0.741 | 0.635 | 0.383 |
| 32 | yrkesutbildning, lärlingsutbildning, företag, kvalificerad, yrke, lärling, eftergymnasial, företagare | 0/4 | 0.299 | 0.133 | 0.152 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.5364
- Median: 0.5811
- Min: 0.0006
- Max: 0.9554
- Std Dev: 0.3116

**Jaccard Similarity (top 20 words):**
- Mean: 0.2280
- Median: 0.1597
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1993

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5352
- Median: 0.5905
- Min: 0.0041
- Max: 0.9834
- Std Dev: 0.3081

**Jaccard Similarity (top 20 words):**
- Mean: 0.2542
- Median: 0.2500
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2064

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5197
- Median: 0.5511
- Min: 0.0022
- Max: 0.9443
- Std Dev: 0.3230

**Jaccard Similarity (top 20 words):**
- Mean: 0.2416
- Median: 0.2121
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1714

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5374
- Median: 0.5704
- Min: 0.0082
- Max: 0.9785
- Std Dev: 0.3304

**Jaccard Similarity (top 20 words):**
- Mean: 0.2784
- Median: 0.2500
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2232

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.5766
- Median: 0.6776
- Min: 0.0067
- Max: 0.9770
- Std Dev: 0.3069

**Jaccard Similarity (top 20 words):**
- Mean: 0.2854
- Median: 0.2121
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.2098

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.4962
- Median: 0.4780
- Min: 0.0066
- Max: 0.9784
- Std Dev: 0.3076

**Jaccard Similarity (top 20 words):**
- Mean: 0.2043
- Median: 0.1765
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1534

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5387
- Median: 0.5702
- Min: 0.0020
- Max: 0.9787
- Std Dev: 0.2997

**Jaccard Similarity (top 20 words):**
- Mean: 0.2270
- Median: 0.1943
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.1920

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5777
- Median: 0.6566
- Min: 0.0256
- Max: 0.9681
- Std Dev: 0.3015

**Jaccard Similarity (top 20 words):**
- Mean: 0.2540
- Median: 0.2311
- Min: 0.0000
- Max: 0.6000
- Std Dev: 0.1580

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6214
- Median: 0.7489
- Min: 0.0021
- Max: 0.9905
- Std Dev: 0.3043

**Jaccard Similarity (top 20 words):**
- Mean: 0.3037
- Median: 0.2702
- Min: 0.0000
- Max: 0.7391
- Std Dev: 0.1908

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.5533
- Median: 0.5658
- Min: 0.0194
- Max: 0.9821
- Std Dev: 0.2988

**Jaccard Similarity (top 20 words):**
- Mean: 0.2516
- Median: 0.1765
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1924

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 320

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.5493
- Median: 0.5939
- Min: 0.0006
- Max: 0.9905
- Std Dev: 0.3111

### Jaccard Similarity (across all matches)
- Mean: 0.2528
- Median: 0.2121
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.1930
