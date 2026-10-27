# Deduplication Comparison

The same models fitted on four selections of the motions (`analysis/dedup_comparison.py`): *none* (length minimum only), *exact* (identical final texts removed), and two thresholds for revised resubmissions (Jaccard of three-word sequences): *near08* (≥ 0.8, the earlier setting) and *near* (≥ 0.6; the models' setting). Seeds 42, 123, 456, 789, 999; topic diagnostics from the seed-42 models.

Duplicates will probably make the models look more stable, since repeated texts are easy to reproduce with any seed; higher stability without deduplication is not by itself an argument for keeping duplicates.

## Motions

| Selection | Motions | 1985/86–1993/94 | 1994/95–2005/06 | 2006/07–2013/14 | 2014/15–2025/26 |
|---|---|---|---|---|---|
| No duplicates removed | 13,649 | 3,741 | 3,465 | 2,875 | 3,568 |
| Exact duplicates removed | 13,005 | 3,729 | 3,433 | 2,704 | 3,139 |
| Exact and near-duplicates (≥ 0.8) removed | 11,627 | 3,613 | 3,224 | 2,313 | 2,477 |
| Exact and near-duplicates (≥ 0.6) removed (the models) | 10,692 | 3,467 | 3,055 | 2,026 | 2,144 |

## Whole-corpus model (32 topics)

*Stable*: found again (matched cosine ≥ 0.7) in at least 3 of the 4 other seeds' models. *Small*: under 1% of the corpus. *Series-dominated*: the top 10 motions contain at least 5 related texts (linked by ≥ 0.3 of their three-word sequences, e.g. one author's yearly resubmissions). *One party*: at least 6 of the top 10 motions have a first signatory from the same party.

| Selection | Mean cosine (per-pair range) | Stable | Found in all / none | Small | Series-dominated | One party |
|---|---|---|---|---|---|---|
| No duplicates removed | 0.557 (0.532–0.592) | 11 of 32 | 6 / 12 | 10 | 10 | 14 |
| Exact duplicates removed | 0.567 (0.520–0.601) | 13 of 32 | 4 / 14 | 8 | 7 | 11 |
| Exact and near-duplicates (≥ 0.8) removed | 0.562 (0.536–0.610) | 10 of 32 | 5 / 12 | 10 | 2 | 13 |
| Exact and near-duplicates (≥ 0.6) removed (the models) | 0.542 (0.496–0.593) | 8 of 32 | 4 / 9 | 10 | 1 | 5 |

## Period models (8 topics per period)

Seed stability: mean cosine / stable topics per period. Alignment: matched mean cosine of adjacent periods (z of the permutation test). Chains: mean link ≥ 0.50 (all links ≥ 0.50).

| Selection | 1985/86–1993/94 | 1994/95–2005/06 | 2006/07–2013/14 | 2014/15–2025/26 | Stable in all | Alignment | Chains hold |
|---|---|---|---|---|---|---|---|
| No duplicates removed | 0.72 / 4 | 0.77 / 6 | 0.74 / 6 | 0.77 / 5 | 21 of 32 | 0.58 (4.0), 0.68 (4.0), 0.66 (4.4) | 6 of 8 (3) |
| Exact duplicates removed | 0.79 / 4 | 0.78 / 6 | 0.77 / 6 | 0.76 / 7 | 23 of 32 | 0.67 (4.4), 0.61 (4.0), 0.64 (4.1) | 8 of 8 (4) |
| Exact and near-duplicates (≥ 0.8) removed | 0.75 / 4 | 0.77 / 4 | 0.75 / 6 | 0.79 / 5 | 19 of 32 | 0.63 (4.3), 0.66 (4.8), 0.68 (5.4) | 6 of 8 (3) |
| Exact and near-duplicates (≥ 0.6) removed (the models) | 0.79 / 5 | 0.76 / 5 | 0.78 / 6 | 0.75 / 7 | 23 of 32 | 0.60 (4.3), 0.61 (4.3), 0.63 (4.0) | 6 of 8 (2) |

## How much the whole-corpus topics change

Each selection's seed-42 model matched one-to-one with the *near* model (cosine over the shared words). *Found*: matched cosine ≥ 0.7. The table lists, among the found topics, those whose share in a period changes most; shares per period in the selection and in the models.

### No duplicates removed against the models

Mean matched cosine 0.561; 11 of 32 topics found.

| Topic (top words, near model) | Cosine | Shares per period, none | Shares per period, near |
|---|---|---|---|
| högskola, län, jönköping | 0.87 | 19.6% / 5.8% / 1.6% / 1.1% | 1.1% / 0.9% / 0.6% / 0.4% |
| elev, gymnasieskola, ämne | 0.85 | 8.6% / 10.2% / 10.9% / 10.9% | 7.3% / 6.3% / 6.0% / 4.8% |
| universitet, göteborg, umeå | 0.83 | 1.8% / 1.1% / 0.5% / 0.5% | 5.9% / 3.3% / 1.4% / 1.1% |
| forskning, universitet, svensk | 0.98 | 7.8% / 6.2% / 3.9% / 4.6% | 7.1% / 7.4% / 5.6% / 6.5% |
| företag, land, hög | 0.92 | 6.0% / 5.6% / 5.0% / 6.1% | 4.2% / 4.3% / 4.0% / 4.9% |

### Exact duplicates removed against the models

Mean matched cosine 0.554; 15 of 32 topics found.

| Topic (top words, near model) | Cosine | Shares per period, exact | Shares per period, near |
|---|---|---|---|
| anslag, högskola, förslag | 0.72 | 27.0% / 9.7% / 2.6% / 1.8% | 8.6% / 3.6% / 1.1% / 1.0% |
| vuxenutbildning, behov, arbetsmarknad | 0.83 | 4.2% / 8.0% / 11.4% / 11.1% | 2.8% / 3.8% / 4.9% / 4.0% |
| kommun, elev, fristående | 0.95 | 5.2% / 9.8% / 10.6% / 10.8% | 3.6% / 5.2% / 6.1% / 5.2% |
| högskola, län, jönköping | 0.82 | 6.4% / 3.7% / 2.2% / 1.9% | 1.1% / 0.9% / 0.6% / 0.4% |
| student, högskola, hög | 0.92 | 1.5% / 3.4% / 3.1% / 2.7% | 4.3% / 7.3% / 6.7% / 6.5% |

### Exact and near-duplicates (≥ 0.8) removed against the models

Mean matched cosine 0.515; 13 of 32 topics found.

| Topic (top words, near model) | Cosine | Shares per period, near08 | Shares per period, near |
|---|---|---|---|
| högskola, län, jönköping | 0.75 | 13.1% / 4.2% / 1.6% / 1.4% | 1.1% / 0.9% / 0.6% / 0.4% |
| företag, land, hög | 0.79 | 13.6% / 9.9% / 6.2% / 6.2% | 4.2% / 4.3% / 4.0% / 4.9% |
| elev, lärare, undervisning | 0.97 | 3.1% / 4.6% / 5.4% / 7.7% | 4.5% / 8.4% / 9.8% / 14.1% |
| kommun, elev, fristående | 0.94 | 3.4% / 6.4% / 8.0% / 8.5% | 3.6% / 5.2% / 6.1% / 5.2% |
| elev, gymnasieskola, ämne | 0.89 | 4.4% / 5.7% / 6.4% / 6.3% | 7.3% / 6.3% / 6.0% / 4.8% |

