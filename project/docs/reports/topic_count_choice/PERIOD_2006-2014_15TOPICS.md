# Seed-Stability Analysis: Period 2006/07–2013/14, 15 Topics

## Methodology

**Matching:** topics are optimally matched across models using the Hungarian algorithm,
accounting for the fact that topic indices are arbitrary across LDA runs.

**Text:** Body text only, motions of sessions 2006/07–2013/14 (2725)

**Matching criterion:** Cosine similarity over normalized topic-word distributions

**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)

**LDA settings:** 15 topics, max_iter=50, learning_method=online, n_jobs=2, verbose=0

## Models per Seed

Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence
(evaluate_every=-1), so every fit runs exactly max_iter=50 passes;
the iteration count confirms the setting, not convergence.

| Seed | Training perplexity | Iterations |
|---|---|---|
| 42 | 1181.98 | 50 |
| 123 | 1191.61 | 50 |
| 456 | 1185.09 | 50 |
| 789 | 1212.53 | 50 |
| 999 | 1190.85 | 50 |

## Stability per Topic (reference model: seed 42)

Each topic of the seed-42 model (the seed of the reported model) is compared with
its matched topic in each of the other 4 models. *Found* counts the models where the
match has cosine similarity ≥ 0.70; this threshold is a judgement call. Interpret
topics that are found in all models with more confidence than the others.

| Found in | Topics |
|---|---|
| 4 of 4 | 5 |
| 3 of 4 | 3 |
| 2 of 4 | 2 |
| 1 of 4 | 1 |
| 0 of 4 | 4 |

| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |
|---|---|---|---|---|---|
| 1 | barn, ungdom, fysisk, aktivitet, hälsa, ung, idrott, liv | 4/4 | 0.890 | 0.777 | 0.421 |
| 2 | ungdom, kunskap, undervisning, ung, samlevnadsundervisning, lycka, ämne, öka | 1/4 | 0.556 | 0.379 | 0.275 |
| 3 | elev, lärare, kunskap, undervisning, grundskola, språk, svensk, stöd | 4/4 | 0.951 | 0.925 | 0.529 |
| 4 | ungdom, elevhälsa, rättighet, demokrati, demokratisk, samhälle, psykisk, skolhälsovård | 0/4 | 0.316 | 0.099 | 0.133 |
| 5 | högskola, forskning, universitet, hög, utveckling, företag, lärosäte, näringsliv | 3/4 | 0.863 | 0.674 | 0.529 |
| 6 | kvinna, samhälle, flicka, människa, person, jämställdhet, kunskap, annan | 3/4 | 0.730 | 0.625 | 0.319 |
| 7 | arbetsmarknad, vuxenutbildning, behov, människa, hög, yrkesutbildning, jobb, arbete | 3/4 | 0.769 | 0.567 | 0.430 |
| 8 | barnomsorg, förälder, kommun, barn, arbetstid, obekväm, arbeta, erbjuda | 2/4 | 0.523 | 0.089 | 0.382 |
| 9 | student, studie, studiemedel, fribelopp, lite, ekonomisk, anslag, studera | 4/4 | 0.913 | 0.710 | 0.681 |
| 10 | förskola, barn, personal, fritidshem, verksamhet, pedagogisk, behov, kommun | 4/4 | 0.953 | 0.936 | 0.651 |
| 11 | gymnasieskola, program, högskola, elev, behörighet, kurs, regel, grundläggande | 0/4 | 0.312 | 0.047 | 0.111 |
| 12 | forskning, svensk, land, annan, område, utveckling, läkare, internationell | 0/4 | 0.477 | 0.381 | 0.223 |
| 13 | student, verksamhet, högskola, studentkår, studentinflytande, inflytande, styrelse, universitet | 0/4 | 0.429 | 0.287 | 0.106 |
| 14 | lärare, nationell, lärarutbildning, legitimation, prov, statlig, svensk, lärarlegitimation | 2/4 | 0.477 | 0.027 | 0.128 |
| 15 | kommun, elev, fristående, kommunal, friskola, verksamhet, skolinspektion, skollag | 4/4 | 0.980 | 0.961 | 0.728 |

## Pairwise Comparisons

### Seed 42 vs Seed 123

**Cosine Similarity (full topic distributions):**
- Mean: 0.7106
- Median: 0.7783
- Min: 0.2950
- Max: 0.9798
- Std Dev: 0.2557

**Jaccard Similarity (top 20 words):**
- Mean: 0.4192
- Median: 0.4286
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2590

### Seed 42 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.7029
- Median: 0.7773
- Min: 0.0468
- Max: 0.9902
- Std Dev: 0.2835

**Jaccard Similarity (top 20 words):**
- Mean: 0.4235
- Median: 0.3793
- Min: 0.0000
- Max: 0.8182
- Std Dev: 0.2579

### Seed 42 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6176
- Median: 0.7103
- Min: 0.0272
- Max: 0.9615
- Std Dev: 0.3063

**Jaccard Similarity (top 20 words):**
- Mean: 0.3187
- Median: 0.2903
- Min: 0.0256
- Max: 0.6000
- Std Dev: 0.2013

### Seed 42 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6727
- Median: 0.7360
- Min: 0.0987
- Max: 0.9945
- Std Dev: 0.3065

**Jaccard Similarity (top 20 words):**
- Mean: 0.3445
- Median: 0.2903
- Min: 0.0256
- Max: 0.9048
- Std Dev: 0.2683

### Seed 123 vs Seed 456

**Cosine Similarity (full topic distributions):**
- Mean: 0.6925
- Median: 0.8427
- Min: 0.1296
- Max: 0.9653
- Std Dev: 0.2722

**Jaccard Similarity (top 20 words):**
- Mean: 0.3803
- Median: 0.4286
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2431

### Seed 123 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.6181
- Median: 0.7130
- Min: 0.0142
- Max: 0.9779
- Std Dev: 0.2894

**Jaccard Similarity (top 20 words):**
- Mean: 0.3111
- Median: 0.3333
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.1853

### Seed 123 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6375
- Median: 0.6916
- Min: 0.0184
- Max: 0.9837
- Std Dev: 0.2999

**Jaccard Similarity (top 20 words):**
- Mean: 0.2976
- Median: 0.2500
- Min: 0.0000
- Max: 0.6667
- Std Dev: 0.2157

### Seed 456 vs Seed 789

**Cosine Similarity (full topic distributions):**
- Mean: 0.5938
- Median: 0.6158
- Min: 0.0681
- Max: 0.9598
- Std Dev: 0.2932

**Jaccard Similarity (top 20 words):**
- Mean: 0.2584
- Median: 0.2121
- Min: 0.0000
- Max: 0.5385
- Std Dev: 0.1925

### Seed 456 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.7157
- Median: 0.8504
- Min: 0.2031
- Max: 0.9859
- Std Dev: 0.2780

**Jaccard Similarity (top 20 words):**
- Mean: 0.3874
- Median: 0.3793
- Min: 0.0256
- Max: 0.8182
- Std Dev: 0.2337

### Seed 789 vs Seed 999

**Cosine Similarity (full topic distributions):**
- Mean: 0.6106
- Median: 0.6143
- Min: 0.1178
- Max: 0.9808
- Std Dev: 0.2672

**Jaccard Similarity (top 20 words):**
- Mean: 0.2977
- Median: 0.2903
- Min: 0.0256
- Max: 0.7391
- Std Dev: 0.2220

## Overall Summary Statistics

**Total seed pairs tested:** 10
**Total matched topic pairs:** 150

**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model
appears in 4 of the 10 pairs, so the pooled values below reuse
the same topics several times. The pooled mean is a fair summary, but the pooled standard
deviation understates the real uncertainty. For spread across runs, compare the per-pair
means above.

### Cosine Similarity (across all matches)
- Mean: 0.6572
- Median: 0.7313
- Min: 0.0142
- Max: 0.9945
- Std Dev: 0.2890

### Jaccard Similarity (across all matches)
- Mean: 0.3438
- Median: 0.3333
- Min: 0.0000
- Max: 0.9048
- Std Dev: 0.2357
