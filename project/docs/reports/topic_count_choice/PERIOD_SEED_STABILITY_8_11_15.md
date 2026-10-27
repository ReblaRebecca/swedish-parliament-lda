# Seed Stability of the Period Models

Seeds: 42, 123, 456, 789, 999. Reference model: seed 42. Each period's own
vocabulary (as the period models). *Stable* = found again (matched cosine ≥ 0.70) in at least
3 of the other 4 seeds' models. Mean cosine is the mean of the per-pair means.

The analysis uses 8 topics per period: the highest tested count (8, 11, 15) at which at least half
of the topics are stable in every period (reports of all three counts in topic_count_choice/).

| Period | Topics | Mean cosine | Per-pair range | Found in all | Found in none | Stable | Stable share |
|---|---|---|---|---|---|---|---|
| 1985/86–1993/94 | 8 | 0.722 | 0.659–0.806 | 2 | 0 | 4 | 50% |
| 1985/86–1993/94 | 11 | 0.696 | 0.650–0.760 | 3 | 3 | 5 | 45% |
| 1985/86–1993/94 | 15 | 0.623 | 0.564–0.679 | 3 | 4 | 4 | 27% |
| 1994/95–2005/06 | 8 | 0.782 | 0.730–0.858 | 5 | 0 | 6 | 75% |
| 1994/95–2005/06 | 11 | 0.754 | 0.708–0.804 | 5 | 1 | 6 | 55% |
| 1994/95–2005/06 | 15 | 0.696 | 0.632–0.803 | 5 | 3 | 9 | 60% |
| 2006/07–2013/14 | 8 | 0.797 | 0.712–0.865 | 3 | 0 | 5 | 62% |
| 2006/07–2013/14 | 11 | 0.729 | 0.627–0.785 | 5 | 0 | 8 | 73% |
| 2006/07–2013/14 | 15 | 0.657 | 0.594–0.716 | 5 | 4 | 8 | 53% |
| 2014/15–2025/26 | 8 | 0.745 | 0.677–0.807 | 3 | 0 | 5 | 62% |
| 2014/15–2025/26 | 11 | 0.708 | 0.620–0.785 | 3 | 0 | 6 | 55% |
| 2014/15–2025/26 | 15 | 0.648 | 0.602–0.701 | 4 | 3 | 8 | 53% |
