# Seed Stability of the Period Models

Seeds: 42, 123, 456, 789, 999. Reference model: seed 42. Each period's own
vocabulary (as the period models). *Stable* = found again (matched cosine ≥ 0.70) in at least
3 of the other 4 seeds' models. Mean cosine is the mean of the per-pair means.

The analysis uses 8 topics per period: the highest tested count (8, 11, 15) at which at least half
of the topics are stable in every period (reports of all three counts in topic_count_choice/).

| Period | Topics | Mean cosine | Per-pair range | Found in all | Found in none | Stable | Stable share |
|---|---|---|---|---|---|---|---|
| 1985/86–1993/94 | 8 | 0.734 | 0.695–0.780 | 3 | 1 | 5 | 62% |
| 1985/86–1993/94 | 11 | 0.649 | 0.597–0.685 | 3 | 3 | 4 | 36% |
| 1985/86–1993/94 | 15 | 0.605 | 0.553–0.651 | 3 | 2 | 7 | 47% |
| 1994/95–2005/06 | 8 | 0.815 | 0.757–0.882 | 5 | 1 | 6 | 75% |
| 1994/95–2005/06 | 11 | 0.746 | 0.700–0.813 | 4 | 1 | 7 | 64% |
| 1994/95–2005/06 | 15 | 0.669 | 0.610–0.743 | 5 | 3 | 7 | 47% |
| 2006/07–2013/14 | 8 | 0.766 | 0.714–0.879 | 3 | 1 | 5 | 62% |
| 2006/07–2013/14 | 11 | 0.721 | 0.602–0.813 | 4 | 3 | 6 | 55% |
| 2006/07–2013/14 | 15 | 0.665 | 0.595–0.752 | 5 | 4 | 7 | 47% |
| 2014/15–2025/26 | 8 | 0.767 | 0.671–0.894 | 3 | 0 | 6 | 75% |
| 2014/15–2025/26 | 11 | 0.722 | 0.640–0.811 | 2 | 0 | 7 | 64% |
| 2014/15–2025/26 | 15 | 0.623 | 0.564–0.691 | 3 | 2 | 7 | 47% |
