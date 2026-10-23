#!/usr/bin/env python3
"""
Seed-stability test of the period models (docs/PIPELINE_DOCUMENTATION.md, Design Decisions and
Current Results). By default for the chosen topic count (PERIOD_TOPICS in lda_common.py); the count
was chosen by running it at 8, 11 and 15 topics (`16_seed_stability_periods.py 8 11 15`; reports kept
in docs/reports/topic_count_choice/).

For every period and topic count: fit one model per seed on the period's motions with the period's own
vocabulary (as 15_fit_period_lda.py), match every pair of seeds and count how many topics of the
seed-42 model are found again in the other seeds' models. Writes a full report per period and
count (as 09_test_lda_stability.py) and one summary over all of them.

Runtime: 4 periods x 5 seeds = 20 fits per topic count; about 10 minutes at 8 topics.

Usage: python analysis/16_seed_stability_periods.py [num_topics ...]   (default: PERIOD_TOPICS)
Output: docs/reports/period_stability/PERIOD_<period>_<k>TOPICS.md (report),
        results/period_stability/PERIOD_<period>_<k>TOPICS_PER_TOPIC.csv,
        docs/reports/PERIOD_SEED_STABILITY_SUMMARY.md
"""

import sys
from pathlib import Path

import numpy as np

from seed_stability import (
    generate_report, per_topic_stability, run_seed_stability, save_report, save_topic_stability,
)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'modeling'))
from lda_common import (  # noqa: E402
    DEFAULT_SEED, PERIOD_TOPICS, STABILITY_SEEDS, fit_period_vectorizer, load_period_body_texts, period_display,
)


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
        f"Seeds: {', '.join(map(str, STABILITY_SEEDS))}. Reference model: seed {DEFAULT_SEED}. Each period's own",
        "vocabulary (as the period models). *Stable* = found again (matched cosine ≥ 0.70) in at least",
        f"{others - 1} of the other {others} seeds' models. Mean cosine is the mean of the per-pair means.",
        "",
        f"The analysis uses {PERIOD_TOPICS} topics per period: the highest tested count (8, 11, 15) at which at least half",
        "of the topics are stable in every period (reports of all three counts in topic_count_choice/).",
        "",
        "| Period | Topics | Mean cosine | Per-pair range | Found in all | Found in none | Stable | Stable share |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for (period, k), s in summaries.items():
        lines.append(f"| {period_display(period)} | {k} | {s['mean_cosine']:.3f} | {s['min_pair']:.3f}–{s['max_pair']:.3f} | "
                     f"{s['found_all']} | {s['found_none']} | {s['stable']} | {s['stable_share']:.0%} |")
    lines.append("")
    return '\n'.join(lines)


def main():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
    REPORT_DIR = PROJECT_ROOT / 'docs' / 'reports' / 'period_stability'
    CSV_DIR = PROJECT_ROOT / 'results' / 'period_stability'
    topic_counts = [int(a) for a in sys.argv[1:]] or [PERIOD_TOPICS]

    periods, malformed = load_period_body_texts(INPUT_DIR)
    if malformed:
        print(f"⚠️  {malformed} malformed JSON lines skipped")
    if not periods or not all(texts for texts, _ in periods.values()):
        print(f"Error: no texts loaded for some period in {INPUT_DIR}")
        sys.exit(1)

    summaries = {}
    for period, (texts, _) in periods.items():
        # The period's own vocabulary, as 15_fit_period_lda.py (same texts and settings, so the same vocabulary)
        vectorizer = fit_period_vectorizer(texts)
        vocab = vectorizer.get_feature_names_out()
        doc_term_matrix = vectorizer.transform(texts)
        for k in topic_counts:
            print("=" * 80)
            print(f"Period {period_display(period)}: {len(texts)} motions, {k} topics")
            print("=" * 80)
            seed_info, pairwise = run_seed_stability(doc_term_matrix, vocab, STABILITY_SEEDS, k)
            rows = per_topic_stability(pairwise, DEFAULT_SEED, k)
            name = f"PERIOD_{period}_{k}TOPICS"
            save_report(generate_report(f"Seed-Stability Analysis: Period {period_display(period)}, {k} Topics",
                                        f"Body text only, motions of sessions {period_display(period)} ({len(texts)})", k, seed_info, pairwise),
                        REPORT_DIR / f"{name}.md")
            save_topic_stability(rows, seed_info, DEFAULT_SEED, CSV_DIR / f"{name}_PER_TOPIC.csv")
            summaries[(period, k)] = summarize(pairwise, rows)

    save_report(summary_report(summaries), PROJECT_ROOT / 'docs' / 'reports' / 'PERIOD_SEED_STABILITY_SUMMARY.md')


if __name__ == '__main__':
    main()
