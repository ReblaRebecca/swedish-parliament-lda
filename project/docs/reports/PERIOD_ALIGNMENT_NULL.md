# Cross-Period Alignment: Permutation Test

Period models with 8 topics, each with its own vocabulary; adjacent periods compared over the
words both vocabularies contain. *Matched* is the mean cosine of the one-to-one Hungarian matching;
the null is the mean cosine of 1,000 random one-to-one matchings of the same topics
(seed 0). z = (matched − null mean) / null SD; p one-sided, from the standard normal distribution,
as Gordon (2026, 3.4).

| Transition | Shared words | Matched | Null mean | Null SD | z | p |
|---|---|---|---|---|---|---|
| 1985/86–1993/94 → 1994/95–2005/06 | 5,458 | 0.633 | 0.341 | 0.070 | 4.2 | 1.6e-05 |
| 1994/95–2005/06 → 2006/07–2013/14 | 4,377 | 0.676 | 0.339 | 0.075 | 4.5 | 3.3e-06 |
| 2006/07–2013/14 → 2014/15–2025/26 | 4,164 | 0.618 | 0.365 | 0.063 | 4.0 | 3.3e-05 |

Gordon (15 topics per period): matched 0.44–0.59 against null means 0.22–0.25, z = 7–9.

The test shows that the matched topics are more similar than random pairings of the same topics,
i.e. continuity above chance. It does not show that every matched pair is the same theme: single
links can still be weak (see the period explorer).
