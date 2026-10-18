# Seed Stability of the Period Models

Seeds: 42, 123, 456, 789, 999. Reference model: seed 42. Global vocabulary
(baseline vectorizer). *Stable* = found again (matched cosine ≥ 0.70) in at least
3 of the other 4 seeds' models. Mean cosine is the mean of the per-pair means.

The analysis uses 8 topics per period: the highest tested count (8, 11, 15) at which at least half
of the topics are stable in every period (reports of all three counts in topic_count_choice/).

| Period | Topics | Mean cosine | Per-pair range | Found in all | Found in none | Stable | Stable share |
|---|---|---|---|---|---|---|---|
| 1985/86–1993/94 | 8 | 0.697 | 0.637–0.771 | 2 | 1 | 4 | 50% |
| 1994/95–2005/06 | 8 | 0.769 | 0.688–0.835 | 3 | 1 | 7 | 88% |
| 2006/07–2013/14 | 8 | 0.797 | 0.741–0.861 | 3 | 0 | 6 | 75% |
| 2014/15–2025/26 | 8 | 0.716 | 0.647–0.773 | 2 | 0 | 4 | 50% |
