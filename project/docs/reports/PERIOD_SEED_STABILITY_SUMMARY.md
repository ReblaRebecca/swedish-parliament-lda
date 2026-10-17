# Seed Stability of the Period Models

Seeds: 42, 123, 456, 789, 999. Reference model: seed 42. Global vocabulary
(baseline vectorizer). *Stable* = found again (matched cosine ≥ 0.70) in at least
3 of the other 4 seeds' models. Mean cosine is the mean of the per-pair means.

Choose the highest topic count at which most topics are still stable and interpretable,
the same count in every period.

| Period | Topics | Mean cosine | Per-pair range | Found in all | Found in none | Stable | Stable share |
|---|---|---|---|---|---|---|---|
| 1986-1993 | 8 | 0.729 | 0.681–0.809 | 2 | 1 | 4 | 50% |
| 1986-1993 | 11 | 0.625 | 0.569–0.680 | 4 | 5 | 4 | 36% |
| 1986-1993 | 15 | 0.524 | 0.464–0.595 | 3 | 6 | 5 | 33% |
| 1994-2004 | 8 | 0.714 | 0.610–0.807 | 4 | 3 | 4 | 50% |
| 1994-2004 | 11 | 0.645 | 0.580–0.715 | 4 | 4 | 7 | 64% |
| 1994-2004 | 15 | 0.593 | 0.547–0.670 | 5 | 5 | 7 | 47% |
| 2005-2014 | 8 | 0.752 | 0.694–0.864 | 4 | 1 | 6 | 75% |
| 2005-2014 | 11 | 0.701 | 0.636–0.823 | 2 | 2 | 6 | 55% |
| 2005-2014 | 15 | 0.621 | 0.600–0.649 | 3 | 4 | 6 | 40% |
| 2015-2025 | 8 | 0.757 | 0.699–0.792 | 5 | 2 | 5 | 62% |
| 2015-2025 | 11 | 0.704 | 0.668–0.792 | 4 | 3 | 4 | 36% |
| 2015-2025 | 15 | 0.613 | 0.575–0.658 | 3 | 5 | 6 | 40% |
