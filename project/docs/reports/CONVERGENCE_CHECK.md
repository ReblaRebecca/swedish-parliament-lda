# Convergence Check of the LDA Fits

Each model fitted once with 200 passes (seed 42, otherwise the shared LDA settings), with a copy kept at 10, 25, 50, 100, 150 passes. Every checkpoint is compared with the 200-pass model: training perplexity, and the topics matched one-to-one (Hungarian, cosine over the full vocabulary). *Found*: topics with matched cosine at least 0.7 (as the seed-stability test). The reported models use 50 passes.

Data: the motions the models currently select (length minimum, no duplicates) from the preprocessed data at the time of the check.

## Whole-corpus model

13,124 motions, 15,763 words, 32 topics; 200 passes took 13.9 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,999.0 | – | 0.965 | 0.774 | 32/32 |
| 25 | 1,986.7 | -0.61% | 0.984 | 0.875 | 32/32 |
| 50 | 1,982.2 | -0.23% | 0.995 | 0.969 | 32/32 |
| 100 | 1,979.3 | -0.15% | 0.999 | 0.997 | 32/32 |
| 150 | 1,978.3 | -0.05% | 1.000 | 1.000 | 32/32 |
| 200 | 1,977.7 | -0.03% | 1.000 | 1.000 | 32/32 |

## Period model 1985/86–1993/94

3,737 motions, 7,270 words, 8 topics; 200 passes took 1.9 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,668.5 | – | 0.989 | 0.966 | 8/8 |
| 25 | 1,660.6 | -0.47% | 0.996 | 0.990 | 8/8 |
| 50 | 1,657.6 | -0.18% | 0.999 | 0.996 | 8/8 |
| 100 | 1,655.7 | -0.11% | 1.000 | 0.999 | 8/8 |
| 150 | 1,654.9 | -0.05% | 1.000 | 1.000 | 8/8 |
| 200 | 1,654.4 | -0.03% | 1.000 | 1.000 | 8/8 |

## Period model 1994/95–2005/06

3,440 motions, 7,956 words, 8 topics; 200 passes took 2.2 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,619.4 | – | 0.991 | 0.967 | 8/8 |
| 25 | 1,614.1 | -0.33% | 0.997 | 0.989 | 8/8 |
| 50 | 1,612.2 | -0.11% | 0.999 | 0.996 | 8/8 |
| 100 | 1,611.1 | -0.07% | 1.000 | 0.999 | 8/8 |
| 150 | 1,610.8 | -0.02% | 1.000 | 1.000 | 8/8 |
| 200 | 1,610.6 | -0.01% | 1.000 | 1.000 | 8/8 |

## Period model 2006/07–2013/14

2,725 motions, 4,819 words, 8 topics; 200 passes took 1.1 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,260.7 | – | 0.992 | 0.985 | 8/8 |
| 25 | 1,254.6 | -0.49% | 0.998 | 0.996 | 8/8 |
| 50 | 1,252.4 | -0.17% | 0.999 | 0.999 | 8/8 |
| 100 | 1,251.4 | -0.08% | 1.000 | 1.000 | 8/8 |
| 150 | 1,251.1 | -0.03% | 1.000 | 1.000 | 8/8 |
| 200 | 1,250.9 | -0.01% | 1.000 | 1.000 | 8/8 |

## Period model 2014/15–2025/26

3,222 motions, 6,672 words, 8 topics; 200 passes took 1.5 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,536.0 | – | 0.981 | 0.949 | 8/8 |
| 25 | 1,522.1 | -0.90% | 0.995 | 0.986 | 8/8 |
| 50 | 1,517.8 | -0.29% | 0.998 | 0.995 | 8/8 |
| 100 | 1,515.6 | -0.15% | 1.000 | 0.999 | 8/8 |
| 150 | 1,514.7 | -0.06% | 1.000 | 1.000 | 8/8 |
| 200 | 1,514.2 | -0.03% | 1.000 | 1.000 | 8/8 |

