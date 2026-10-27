# Seed Stability of the Period Models

Seeds: 42, 123, 456, 789, 999. Reference model: seed 42. Each period's own
vocabulary (as the period models). *Stable* = found again (matched cosine ≥ 0.70) in at least
3 of the other 4 seeds' models. Mean cosine is the mean of the per-pair means.

The analysis uses 8 topics per period: the highest tested count (8, 11, 15) at which at least half
of the topics are stable in every period (reports of all three counts in topic_count_choice/).

| Period | Topics | Mean cosine | Per-pair range | Found in all | Found in none | Stable | Stable share |
|---|---|---|---|---|---|---|---|
| 1985/86–1993/94 | 8 | 0.790 | 0.690–0.851 | 5 | 0 | 5 | 62% |
| 1994/95–2005/06 | 8 | 0.764 | 0.612–0.833 | 3 | 0 | 5 | 62% |
| 2006/07–2013/14 | 8 | 0.781 | 0.703–0.851 | 4 | 0 | 6 | 75% |
| 2014/15–2025/26 | 8 | 0.753 | 0.693–0.789 | 3 | 1 | 7 | 88% |
