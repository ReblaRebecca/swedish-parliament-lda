# Convergence Check of the LDA Fits

Each model fitted once with 200 passes (seed 42, otherwise the shared LDA settings), with a copy kept at 10, 25, 50, 100, 150 passes. Every checkpoint is compared with the 200-pass model: training perplexity, and the topics matched one-to-one (Hungarian, cosine over the full vocabulary). *Found*: topics with matched cosine at least 0.7 (as the seed-stability test). The reported models use 50 passes.

Data: the motions the models currently select (length minimum, no duplicates) from the preprocessed data at the time of the check.

## Whole-corpus model

11,628 motions, 14,772 words, 32 topics; 200 passes took 11.7 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 2,006.5 | – | 0.977 | 0.780 | 32/32 |
| 25 | 1,992.8 | -0.68% | 0.991 | 0.864 | 32/32 |
| 50 | 1,988.0 | -0.24% | 0.996 | 0.942 | 32/32 |
| 100 | 1,985.2 | -0.14% | 0.999 | 0.990 | 32/32 |
| 150 | 1,984.2 | -0.05% | 1.000 | 0.999 | 32/32 |
| 200 | 1,983.5 | -0.03% | 1.000 | 1.000 | 32/32 |

## Period model 1985/86–1993/94

3,613 motions, 7,098 words, 8 topics; 200 passes took 1.6 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,659.2 | – | 0.992 | 0.980 | 8/8 |
| 25 | 1,651.7 | -0.45% | 0.997 | 0.995 | 8/8 |
| 50 | 1,649.2 | -0.15% | 0.999 | 0.998 | 8/8 |
| 100 | 1,647.7 | -0.09% | 1.000 | 1.000 | 8/8 |
| 150 | 1,647.1 | -0.04% | 1.000 | 1.000 | 8/8 |
| 200 | 1,646.7 | -0.02% | 1.000 | 1.000 | 8/8 |

## Period model 1994/95–2005/06

3,224 motions, 7,665 words, 8 topics; 200 passes took 1.7 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,595.7 | – | 0.995 | 0.991 | 8/8 |
| 25 | 1,589.5 | -0.39% | 0.998 | 0.996 | 8/8 |
| 50 | 1,587.4 | -0.13% | 0.999 | 0.999 | 8/8 |
| 100 | 1,586.2 | -0.07% | 1.000 | 1.000 | 8/8 |
| 150 | 1,585.9 | -0.02% | 1.000 | 1.000 | 8/8 |
| 200 | 1,585.7 | -0.01% | 1.000 | 1.000 | 8/8 |

## Period model 2006/07–2013/14

2,314 motions, 4,368 words, 8 topics; 200 passes took 1.0 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,227.7 | – | 0.988 | 0.966 | 8/8 |
| 25 | 1,222.2 | -0.45% | 0.995 | 0.980 | 8/8 |
| 50 | 1,219.9 | -0.18% | 0.998 | 0.989 | 8/8 |
| 100 | 1,218.5 | -0.12% | 0.999 | 0.997 | 8/8 |
| 150 | 1,217.8 | -0.05% | 1.000 | 1.000 | 8/8 |
| 200 | 1,217.4 | -0.03% | 1.000 | 1.000 | 8/8 |

## Period model 2014/15–2025/26

2,477 motions, 5,778 words, 8 topics; 200 passes took 1.1 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,414.2 | – | 0.986 | 0.939 | 8/8 |
| 25 | 1,406.0 | -0.58% | 0.996 | 0.983 | 8/8 |
| 50 | 1,403.3 | -0.19% | 0.998 | 0.995 | 8/8 |
| 100 | 1,401.8 | -0.10% | 1.000 | 0.999 | 8/8 |
| 150 | 1,401.3 | -0.04% | 1.000 | 1.000 | 8/8 |
| 200 | 1,401.0 | -0.02% | 1.000 | 1.000 | 8/8 |

