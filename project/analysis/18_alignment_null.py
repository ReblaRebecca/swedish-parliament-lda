#!/usr/bin/env python3
"""
Permutation test of the cross-period alignment, as Gordon (2026, 3.4 and Table 4).

For each pair of adjacent periods: the topics are matched one-to-one (Hungarian algorithm on cosine over the
words both periods' vocabularies contain, as in 17_generate_period_explorer.py), and the matched mean
similarity is compared with the mean similarity of 1,000 random one-to-one matchings of the same topics.
z = (matched mean - null mean) / null SD; p is one-sided, from the standard normal distribution (as Gordon).

Input:  models/period_lda_<k>/ (15_fit_period_lda.py: models and vectorizers), k = PERIOD_TOPICS
Output: docs/reports/PERIOD_ALIGNMENT_NULL.md

Usage: python analysis/18_alignment_null.py [num_topics]   (default: PERIOD_TOPICS)
"""

import pickle
import sys
from pathlib import Path

from topic_matching import match_and_evaluate, permutation_null

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'modeling'))
from lda_common import PERIOD_TOPICS, period_display  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from periods import PERIODS, period_key  # noqa: E402

N_PERMUTATIONS = 1000
NULL_SEED = 0


def load_period_models(model_dir):
    """[(period, lda, vocabulary)] in period order, from the output of 15_fit_period_lda.py."""
    models = []
    for stem, _, _ in PERIODS:
        period = period_key(stem)
        with open(model_dir / f'period_{period}_lda.pkl', 'rb') as f:
            lda = pickle.load(f)
        with open(model_dir / f'period_{period}_vectorizer.pkl', 'rb') as f:
            vocab = pickle.load(f).get_feature_names_out()
        models.append((period, lda, vocab))
    return models


def transition_tests(models, n_permutations=N_PERMUTATIONS, seed=NULL_SEED):
    """One result per pair of adjacent periods: shared words and the permutation test."""
    results = []
    for (p1, lda1, vocab1), (p2, lda2, vocab2) in zip(models, models[1:]):
        _, _, similarity = match_and_evaluate(lda1, lda2, vocab1, vocab2, shared_vocabulary=True)
        result = permutation_null(similarity, n_permutations, seed)
        result.update({'from': p1, 'to': p2, 'shared_words': len(set(vocab1) & set(vocab2))})
        results.append(result)
    return results


def format_p(p):
    return f"{p:.1e}" if p >= 1e-300 else "< 1e-300"


def report(results, num_topics):
    lines = [
        "# Cross-Period Alignment: Permutation Test",
        "",
        f"Period models with {num_topics} topics, each with its own vocabulary; adjacent periods compared over the",
        "words both vocabularies contain. *Matched* is the mean cosine of the one-to-one Hungarian matching;",
        f"the null is the mean cosine of {results[0]['n_permutations']:,} random one-to-one matchings of the same topics",
        f"(seed {NULL_SEED}). z = (matched − null mean) / null SD; p one-sided, from the standard normal distribution,",
        "as Gordon (2026, 3.4).",
        "",
        "| Transition | Shared words | Matched | Null mean | Null SD | z | p |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(f"| {period_display(r['from'])} → {period_display(r['to'])} | {r['shared_words']:,} | "
                     f"{r['matched_mean']:.3f} | {r['null_mean']:.3f} | {r['null_sd']:.3f} | {r['z']:.1f} | {format_p(r['p'])} |")
    lines += [
        "",
        "Gordon (15 topics per period): matched 0.44–0.59 against null means 0.22–0.25, z = 7–9.",
        "",
        "The test shows that the matched topics are more similar than random pairings of the same topics,",
        "i.e. continuity above chance. It does not show that every matched pair is the same theme: single",
        "links can still be weak (see the period explorer).",
        "",
    ]
    return '\n'.join(lines)


def main():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    num_topics = int(sys.argv[1]) if len(sys.argv) > 1 else PERIOD_TOPICS
    model_dir = PROJECT_ROOT / 'models' / f'period_lda_{num_topics}'
    if not model_dir.exists():
        print(f"Error: {model_dir} not found. Run: python modeling/15_fit_period_lda.py {num_topics}")
        sys.exit(1)

    results = transition_tests(load_period_models(model_dir))
    for r in results:
        print(f"{period_display(r['from'])} → {period_display(r['to'])}: matched {r['matched_mean']:.3f}, "
              f"null {r['null_mean']:.3f} ± {r['null_sd']:.3f}, z = {r['z']:.1f}")

    output = PROJECT_ROOT / 'docs' / 'reports' / 'PERIOD_ALIGNMENT_NULL.md'
    output.write_text(report(results, num_topics), encoding='utf-8')
    print(f"✅ Report saved to: {output}")


if __name__ == '__main__':
    main()
