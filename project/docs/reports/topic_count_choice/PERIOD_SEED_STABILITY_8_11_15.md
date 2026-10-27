# Seed Stability of the Period Models

Seeds: 42, 123, 456, 789, 999. Reference model: seed 42. Each period's own
vocabulary (as the period models). *Stable* = found again (matched cosine ≥ 0.70) in at least
3 of the other 4 seeds' models. Mean cosine is the mean of the per-pair means.

The analysis uses 8 topics per period: the highest tested count (8, 11, 15) at which at least half
of the topics are stable in every period (reports of all three counts in topic_count_choice/).

| Period | Topics | Mean cosine | Per-pair range | Found in all | Found in none | Stable | Stable share |
|---|---|---|---|---|---|---|---|
| 1985/86–1993/94 | 8 | 0.790 | 0.690–0.851 | 5 | 0 | 5 | 62% |
| 1985/86–1993/94 | 11 | 0.644 | 0.578–0.694 | 3 | 2 | 4 | 36% |
| 1985/86–1993/94 | 15 | 0.606 | 0.563–0.670 | 3 | 4 | 6 | 40% |
| 1994/95–2005/06 | 8 | 0.764 | 0.612–0.833 | 3 | 0 | 5 | 62% |
| 1994/95–2005/06 | 11 | 0.688 | 0.621–0.791 | 1 | 2 | 5 | 45% |
| 1994/95–2005/06 | 15 | 0.611 | 0.564–0.665 | 4 | 4 | 8 | 53% |
| 2006/07–2013/14 | 8 | 0.781 | 0.703–0.851 | 4 | 0 | 6 | 75% |
| 2006/07–2013/14 | 11 | 0.699 | 0.634–0.790 | 4 | 3 | 5 | 45% |
| 2006/07–2013/14 | 15 | 0.624 | 0.529–0.687 | 5 | 6 | 6 | 40% |
| 2014/15–2025/26 | 8 | 0.753 | 0.693–0.789 | 3 | 1 | 7 | 88% |
| 2014/15–2025/26 | 11 | 0.711 | 0.654–0.770 | 3 | 1 | 8 | 73% |
| 2014/15–2025/26 | 15 | 0.637 | 0.584–0.705 | 5 | 4 | 6 | 40% |
