# Convergence Check of the LDA Fits

Each model fitted once with 200 passes (seed 42, otherwise the shared LDA settings), with a copy kept at 10, 25, 50, 100, 150 passes. Every checkpoint is compared with the 200-pass model: training perplexity, and the topics matched one-to-one (Hungarian, cosine over the full vocabulary). *Found*: topics with matched cosine at least 0.7 (as the seed-stability test). The reported models use 50 passes.

Data: the motions the models currently select (length minimum, no duplicates) from the preprocessed data at the time of the check.

## Whole-corpus model

10,929 motions, 13,982 words, 32 topics; 200 passes took 11.0 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,980.0 | – | 0.955 | 0.701 | 32/32 |
| 25 | 1,964.4 | -0.79% | 0.987 | 0.918 | 32/32 |
| 50 | 1,958.7 | -0.29% | 0.996 | 0.970 | 32/32 |
| 100 | 1,955.6 | -0.16% | 0.999 | 0.993 | 32/32 |
| 150 | 1,954.4 | -0.06% | 1.000 | 0.999 | 32/32 |
| 200 | 1,953.7 | -0.04% | 1.000 | 1.000 | 32/32 |

## Period model 1985/86–1993/94

3,467 motions, 6,875 words, 8 topics; 200 passes took 1.8 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,658.9 | – | 0.977 | 0.926 | 8/8 |
| 25 | 1,652.0 | -0.42% | 0.992 | 0.978 | 8/8 |
| 50 | 1,649.4 | -0.16% | 0.997 | 0.992 | 8/8 |
| 100 | 1,648.1 | -0.08% | 0.999 | 0.998 | 8/8 |
| 150 | 1,647.6 | -0.03% | 1.000 | 1.000 | 8/8 |
| 200 | 1,647.3 | -0.02% | 1.000 | 1.000 | 8/8 |

## Period model 1994/95–2005/06

3,062 motions, 7,350 words, 8 topics; 200 passes took 7.1 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,577.7 | – | 0.987 | 0.966 | 8/8 |
| 25 | 1,570.2 | -0.47% | 0.994 | 0.980 | 8/8 |
| 50 | 1,567.5 | -0.17% | 0.997 | 0.989 | 8/8 |
| 100 | 1,565.7 | -0.11% | 0.999 | 0.997 | 8/8 |
| 150 | 1,565.0 | -0.05% | 1.000 | 1.000 | 8/8 |
| 200 | 1,564.6 | -0.02% | 1.000 | 1.000 | 8/8 |

## Period model 2006/07–2013/14

2,122 motions, 4,076 words, 8 topics; 200 passes took 17.1 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,181.5 | – | 0.987 | 0.966 | 8/8 |
| 25 | 1,172.2 | -0.79% | 0.997 | 0.992 | 8/8 |
| 50 | 1,169.6 | -0.23% | 0.999 | 0.997 | 8/8 |
| 100 | 1,168.3 | -0.11% | 1.000 | 0.999 | 8/8 |
| 150 | 1,167.8 | -0.04% | 1.000 | 1.000 | 8/8 |
| 200 | 1,167.5 | -0.02% | 1.000 | 1.000 | 8/8 |

## Period model 2014/15–2025/26

2,278 motions, 5,223 words, 8 topics; 200 passes took 0.9 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,396.2 | – | 0.980 | 0.947 | 8/8 |
| 25 | 1,386.5 | -0.69% | 0.993 | 0.984 | 8/8 |
| 50 | 1,383.3 | -0.23% | 0.997 | 0.993 | 8/8 |
| 100 | 1,381.6 | -0.12% | 0.999 | 0.998 | 8/8 |
| 150 | 1,381.0 | -0.05% | 1.000 | 0.999 | 8/8 |
| 200 | 1,380.6 | -0.03% | 1.000 | 1.000 | 8/8 |

