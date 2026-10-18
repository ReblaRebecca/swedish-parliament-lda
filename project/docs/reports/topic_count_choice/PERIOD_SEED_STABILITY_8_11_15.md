# Seed Stability of the Period Models

Seeds: 42, 123, 456, 789, 999. Reference model: seed 42. Global vocabulary
(baseline vectorizer). *Stable* = found again (matched cosine ≥ 0.70) in at least
3 of the other 4 seeds' models. Mean cosine is the mean of the per-pair means.

Run at 8, 11 and 15 topics to choose the number of topics per period. Chosen: 8, the highest count at which
at least half of the topics are stable in every period.

| Period | Topics | Mean cosine | Per-pair range | Found in all | Found in none | Stable | Stable share |
|---|---|---|---|---|---|---|---|
| 1985/86–1993/94 | 8 | 0.697 | 0.637–0.771 | 2 | 1 | 4 | 50% |
| 1985/86–1993/94 | 11 | 0.627 | 0.565–0.712 | 2 | 3 | 4 | 36% |
| 1985/86–1993/94 | 15 | 0.551 | 0.514–0.639 | 2 | 5 | 4 | 27% |
| 1994/95–2005/06 | 8 | 0.769 | 0.688–0.835 | 3 | 1 | 7 | 88% |
| 1994/95–2005/06 | 11 | 0.672 | 0.626–0.768 | 2 | 2 | 6 | 55% |
| 1994/95–2005/06 | 15 | 0.615 | 0.563–0.649 | 6 | 5 | 6 | 40% |
| 2006/07–2013/14 | 8 | 0.797 | 0.741–0.861 | 3 | 0 | 6 | 75% |
| 2006/07–2013/14 | 11 | 0.649 | 0.610–0.690 | 3 | 4 | 4 | 36% |
| 2006/07–2013/14 | 15 | 0.580 | 0.518–0.629 | 3 | 7 | 6 | 40% |
| 2014/15–2025/26 | 8 | 0.716 | 0.647–0.773 | 2 | 0 | 4 | 50% |
| 2014/15–2025/26 | 11 | 0.665 | 0.581–0.736 | 4 | 2 | 6 | 55% |
| 2014/15–2025/26 | 15 | 0.615 | 0.536–0.706 | 2 | 4 | 9 | 60% |
