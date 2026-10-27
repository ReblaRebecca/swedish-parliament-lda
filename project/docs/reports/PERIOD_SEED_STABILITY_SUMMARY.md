# Seed Stability of the Period Models

Seeds: 42, 123, 456, 789, 999. Reference model: seed 42. Each period's own
vocabulary (as the period models). *Stable* = found again (matched cosine ≥ 0.70) in at least
3 of the other 4 seeds' models. Mean cosine is the mean of the per-pair means.

The analysis uses 8 topics per period: the highest tested count (8, 11, 15) at which at least half
of the topics are stable in every period (reports of all three counts in topic_count_choice/).

| Period | Topics | Mean cosine | Per-pair range | Found in all | Found in none | Stable | Stable share |
|---|---|---|---|---|---|---|---|
| 1985/86–1993/94 | 8 | 0.722 | 0.659–0.806 | 2 | 0 | 4 | 50% |
| 1994/95–2005/06 | 8 | 0.782 | 0.730–0.858 | 5 | 0 | 6 | 75% |
| 2006/07–2013/14 | 8 | 0.797 | 0.712–0.865 | 3 | 0 | 5 | 62% |
| 2014/15–2025/26 | 8 | 0.745 | 0.677–0.807 | 3 | 0 | 5 | 62% |
