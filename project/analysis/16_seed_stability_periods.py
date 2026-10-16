#!/usr/bin/env python3
"""
Seed-stability test of the period models, for several topic counts, to choose the number of
topics per period (PIPELINE_DOCUMENTATION.md, Plan: Period Models, Topic count per period).

For every period and topic count: fit one model per seed on the period's motions with the global
vocabulary (as 15_fit_period_lda.py), match every pair of seeds and count how many topics of the
seed-42 model are found again in the other seeds' models. Writes a full report per period and
count (as 09_test_lda_stability.py) and one summary over all of them.

Runtime: 4 periods x 3 counts x 5 seeds = 60 fits; roughly 1-3 hours.

Usage: python analysis/16_seed_stability_periods.py [num_topics ...]   (default: 8 11 15)
Output: results/period_stability/PERIOD_<period>_<k>TOPICS.md and _PER_TOPIC.csv,
        results/PERIOD_SEED_STABILITY_SUMMARY.md
"""

import sys
from pathlib import Path

import numpy as np

from seed_stability import (
    generate_report, per_topic_stability, run_seed_stability, save_report, save_topic_stability,
)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'modeling'))
from lda_common import (  # noqa: E402
    DEFAULT_SEED, STABILITY_SEEDS, load_baseline_vectorizer, load_period_body_texts,
)

TOPIC_COUNTS = [8, 11, 15]


def summarize(pairwise_results, rows):
    """Summary of one period and topic count: per-pair mean cosines and the found distribution."""
    pair_means = [float(np.mean([m[2] for m in r['matches']])) for r in pairwise_results.values()]
    others = len(rows[0]['cosines'])
    num_topics = len(rows)
    stable = sum(r['found'] >= others - 1 for r in rows)
    return {
        'num_topics': num_topics,
        'mean_cosine': float(np.mean(pair_means)),
        'min_pair': min(pair_means),
        'max_pair': max(pair_means),
        'found_all': sum(r['found'] == others for r in rows),
        'found_none': sum(r['found'] == 0 for r in rows),
        'stable': stable,
        'stable_share': stable / num_topics,
        'others': others,
    }


def summary_report(summaries):
    """Markdown summary: one row per period and topic count."""
    others = next(iter(summaries.values()))['others']
    lines = [
        "# Seed Stability of the Period Models",
        "",
        f"Seeds: {', '.join(map(str, STABILITY_SEEDS))}. Reference model: seed {DEFAULT_SEED}. Global vocabulary",
        "(baseline vectorizer). *Stable* = found again (matched cosine ≥ 0.70) in at least",
        f"{others - 1} of the other {others} seeds' models. Mean cosine is the mean of the per-pair means.",
        "",
        "Choose the highest topic count at which most topics are still stable and interpretable,",
        "the same count in every period.",
        "",
        "| Period | Topics | Mean cosine | Per-pair range | Found in all | Found in none | Stable | Stable share |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for (period, k), s in summaries.items():
        lines.append(f"| {period} | {k} | {s['mean_cosine']:.3f} | {s['min_pair']:.3f}–{s['max_pair']:.3f} | "
                     f"{s['found_all']} | {s['found_none']} | {s['stable']} | {s['stable_share']:.0%} |")
    lines.append("")
    return '\n'.join(lines)


def main():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
    VECTORIZER_PATH = PROJECT_ROOT / 'models' / 'baseline_lda_44' / 'baseline_vectorizer.pkl'
    REPORT_DIR = PROJECT_ROOT / 'results' / 'period_stability'
    topic_counts = [int(a) for a in sys.argv[1:]] or TOPIC_COUNTS

    periods, malformed = load_period_body_texts(INPUT_DIR)
    if malformed:
        print(f"⚠️  {malformed} malformed JSON lines skipped")
    if not periods or not all(texts for texts, _ in periods.values()):
        print(f"Error: no texts loaded for some period in {INPUT_DIR}")
        sys.exit(1)
    vectorizer = load_baseline_vectorizer(VECTORIZER_PATH)
    vocab = vectorizer.get_feature_names_out()

    summaries = {}
    for period, (texts, _) in periods.items():
        doc_term_matrix = vectorizer.transform(texts)
        for k in topic_counts:
            print("=" * 80)
            print(f"Period {period}: {len(texts)} motions, {k} topics")
            print("=" * 80)
            seed_info, pairwise = run_seed_stability(doc_term_matrix, vocab, STABILITY_SEEDS, k)
            rows = per_topic_stability(pairwise, DEFAULT_SEED, k)
            name = f"PERIOD_{period}_{k}TOPICS"
            save_report(generate_report(f"Seed-Stability Analysis: Period {period}, {k} Topics",
                                        f"Body text only, motions of {period} ({len(texts)})", k, seed_info, pairwise),
                        REPORT_DIR / f"{name}.md")
            save_topic_stability(rows, seed_info, DEFAULT_SEED, REPORT_DIR / f"{name}_PER_TOPIC.csv")
            summaries[(period, k)] = summarize(pairwise, rows)

    save_report(summary_report(summaries), PROJECT_ROOT / 'results' / 'PERIOD_SEED_STABILITY_SUMMARY.md')


if __name__ == '__main__':
    main()
