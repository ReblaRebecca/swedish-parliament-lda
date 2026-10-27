# Convergence Check of the LDA Fits

Each model fitted once with 200 passes (seed 42, otherwise the shared LDA settings), with a copy kept at 10, 25, 50, 100, 150 passes. Every checkpoint is compared with the 200-pass model: training perplexity, and the topics matched one-to-one (Hungarian, cosine over the full vocabulary). *Found*: topics with matched cosine at least 0.7 (as the seed-stability test). The reported models use 50 passes.

Data: the motions the models currently select (length minimum, no duplicates) from the preprocessed data at the time of the check.

## Whole-corpus model

10,692 motions, 13,860 words, 32 topics; 200 passes took 11.2 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,957.3 | – | 0.955 | 0.647 | 31/32 |
| 25 | 1,942.6 | -0.75% | 0.982 | 0.882 | 32/32 |
| 50 | 1,937.3 | -0.27% | 0.993 | 0.930 | 32/32 |
| 100 | 1,934.4 | -0.15% | 0.999 | 0.991 | 32/32 |
| 150 | 1,933.3 | -0.06% | 1.000 | 0.999 | 32/32 |
| 200 | 1,932.8 | -0.03% | 1.000 | 1.000 | 32/32 |

## Period model 1985/86–1993/94

3,467 motions, 6,875 words, 8 topics; 200 passes took 1.7 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,658.9 | – | 0.977 | 0.926 | 8/8 |
| 25 | 1,652.0 | -0.42% | 0.992 | 0.978 | 8/8 |
| 50 | 1,649.4 | -0.16% | 0.997 | 0.992 | 8/8 |
| 100 | 1,648.1 | -0.08% | 0.999 | 0.998 | 8/8 |
| 150 | 1,647.6 | -0.03% | 1.000 | 1.000 | 8/8 |
| 200 | 1,647.3 | -0.02% | 1.000 | 1.000 | 8/8 |

## Period model 1994/95–2005/06

3,055 motions, 7,344 words, 8 topics; 200 passes took 1.7 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,579.0 | – | 0.961 | 0.796 | 8/8 |
| 25 | 1,571.9 | -0.45% | 0.981 | 0.890 | 8/8 |
| 50 | 1,569.2 | -0.17% | 0.995 | 0.979 | 8/8 |
| 100 | 1,567.7 | -0.10% | 0.999 | 0.998 | 8/8 |
| 150 | 1,567.1 | -0.04% | 1.000 | 1.000 | 8/8 |
| 200 | 1,566.8 | -0.02% | 1.000 | 1.000 | 8/8 |

## Period model 2006/07–2013/14

2,026 motions, 3,952 words, 8 topics; 200 passes took 0.8 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,196.0 | – | 0.943 | 0.826 | 8/8 |
| 25 | 1,186.5 | -0.79% | 0.967 | 0.877 | 8/8 |
| 50 | 1,182.3 | -0.35% | 0.980 | 0.922 | 8/8 |
| 100 | 1,179.6 | -0.23% | 0.992 | 0.973 | 8/8 |
| 150 | 1,177.9 | -0.14% | 0.998 | 0.992 | 8/8 |
| 200 | 1,176.2 | -0.14% | 1.000 | 1.000 | 8/8 |

## Period model 2014/15–2025/26

2,144 motions, 5,107 words, 8 topics; 200 passes took 1.0 minutes.

| Passes | Perplexity | Change from previous | Mean cosine with 200 | Min cosine | Found |
|---|---|---|---|---|---|
| 10 | 1,367.5 | – | 0.974 | 0.919 | 8/8 |
| 25 | 1,353.2 | -1.05% | 0.989 | 0.964 | 8/8 |
| 50 | 1,347.1 | -0.45% | 0.996 | 0.988 | 8/8 |
| 100 | 1,343.5 | -0.27% | 0.999 | 0.998 | 8/8 |
| 150 | 1,342.2 | -0.09% | 1.000 | 1.000 | 8/8 |
| 200 | 1,341.6 | -0.05% | 1.000 | 1.000 | 8/8 |

