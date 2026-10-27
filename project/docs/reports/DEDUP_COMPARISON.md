# Deduplication Comparison

The same models fitted on three selections of the motions (`analysis/dedup_comparison.py`): *none* (length minimum only), *exact* (identical final texts removed) and *near* (also revised resubmissions, Jaccard of three-word sequences ≥ 0.8; the models' setting). Seeds 42, 123, 456, 789, 999; topic diagnostics from the seed-42 models.

Duplicates will probably make the models look more stable, since repeated texts are easy to reproduce with any seed; higher stability without deduplication is not by itself an argument for keeping duplicates.

## Motions

| Selection | Motions | 1985/86–1993/94 | 1994/95–2005/06 | 2006/07–2013/14 | 2014/15–2025/26 |
|---|---|---|---|---|---|
| No duplicates removed | 13,649 | 3,741 | 3,465 | 2,875 | 3,568 |
| Exact duplicates removed | 13,007 | 3,729 | 3,433 | 2,704 | 3,141 |
| Exact and near-duplicates removed (the models) | 11,628 | 3,613 | 3,224 | 2,314 | 2,477 |

## Whole-corpus model (32 topics)

*Stable*: found again (matched cosine ≥ 0.7) in at least 3 of the 4 other seeds' models. *Small*: under 1% of the corpus. *Series-dominated*: the top 10 motions contain at least 5 related texts (linked by ≥ 0.3 of their three-word sequences, e.g. one author's yearly resubmissions). *One party*: at least 6 of the top 10 motions have a first signatory from the same party.

| Selection | Mean cosine (per-pair range) | Stable | Found in all / none | Small | Series-dominated | One party |
|---|---|---|---|---|---|---|
| No duplicates removed | 0.544 (0.528–0.579) | 9 of 32 | 5 / 12 | 9 | 10 | 13 |
| Exact duplicates removed | 0.558 (0.482–0.641) | 12 of 32 | 6 / 7 | 10 | 4 | 12 |
| Exact and near-duplicates removed (the models) | 0.533 (0.485–0.588) | 9 of 32 | 8 / 12 | 11 | 2 | 9 |

## Period models (8 topics per period)

Seed stability: mean cosine / stable topics per period. Alignment: matched mean cosine of adjacent periods (z of the permutation test). Chains: mean link ≥ 0.50 (all links ≥ 0.50).

| Selection | 1985/86–1993/94 | 1994/95–2005/06 | 2006/07–2013/14 | 2014/15–2025/26 | Stable in all | Alignment | Chains hold |
|---|---|---|---|---|---|---|---|
| No duplicates removed | 0.78 / 6 | 0.80 / 6 | 0.76 / 4 | 0.76 / 6 | 22 of 32 | 0.64 (4.1), 0.72 (4.3), 0.75 (5.5) | 8 of 8 (4) |
| Exact duplicates removed | 0.73 / 4 | 0.82 / 6 | 0.80 / 5 | 0.75 / 6 | 21 of 32 | 0.62 (4.1), 0.70 (4.7), 0.69 (5.1) | 7 of 8 (5) |
| Exact and near-duplicates removed (the models) | 0.73 / 5 | 0.82 / 6 | 0.77 / 5 | 0.77 / 6 | 22 of 32 | 0.62 (4.2), 0.67 (4.8), 0.61 (4.3) | 6 of 8 (2) |

## How much the whole-corpus topics change

Each selection's seed-42 model matched one-to-one with the *near* model (cosine over the shared words). *Found*: matched cosine ≥ 0.7. The table lists, among the found topics, those whose share in a period changes most; shares per period in the selection and in the models.

### No duplicates removed against the models

Mean matched cosine 0.568; 14 of 32 topics found.

| Topic (top words, near model) | Cosine | Shares per period, none | Shares per period, near |
|---|---|---|---|
| förslag, kommun, verksamhet | 0.88 | 8.3% / 3.7% / 1.9% / 1.7% | 18.2% / 6.5% / 2.8% / 2.6% |
| högskola, universitet, forskning | 0.74 | 14.4% / 4.5% / 1.7% / 1.2% | 6.3% / 6.2% / 3.1% / 2.5% |
| forskning, forskare, svensk | 0.75 | 12.1% / 9.2% / 5.1% / 3.9% | 5.0% / 4.6% / 4.1% / 5.8% |
| barn, förälder, ungdom | 0.77 | 6.7% / 13.4% / 15.9% / 15.2% | 3.7% / 7.8% / 10.2% / 8.8% |
| student, hög, studie | 0.80 | 7.1% / 12.3% / 11.7% / 11.6% | 1.7% / 6.7% / 7.7% / 6.2% |

### Exact duplicates removed against the models

Mean matched cosine 0.575; 17 of 32 topics found.

| Topic (top words, near model) | Cosine | Shares per period, exact | Shares per period, near |
|---|---|---|---|
| barn, förälder, ungdom | 0.78 | 1.1% / 1.4% / 1.1% / 1.1% | 3.7% / 7.8% / 10.2% / 8.8% |
| student, hög, studie | 0.79 | 1.5% / 3.1% / 3.1% / 2.7% | 1.7% / 6.7% / 7.7% / 6.2% |
| högskola, universitet, forskning | 0.85 | 3.5% / 1.8% / 0.9% / 0.7% | 6.3% / 6.2% / 3.1% / 2.5% |
| förslag, kommun, verksamhet | 0.80 | 14.5% / 3.3% / 0.9% / 0.6% | 18.2% / 6.5% / 2.8% / 2.6% |
| lärare, lärarutbildning, kompetens | 0.94 | 2.9% / 2.5% / 3.2% / 4.5% | 6.6% / 4.5% / 4.6% / 5.7% |

