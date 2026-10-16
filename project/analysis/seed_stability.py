#!/usr/bin/env python3
"""
Shared seed-stability procedure for the baseline and title-weighted models.

Fits one LDA model per seed on the same document-term matrix and vocabulary, matches topics
between every pair of seeds with the Hungarian algorithm (topic indices are arbitrary between
runs), and writes a markdown report.
Used by 09_test_lda_stability.py and 13_seed_stability_{3x,5x}_weighted.py.
"""

import sys
from itertools import combinations
from pathlib import Path

import numpy as np

from topic_matching import match_and_evaluate

# Shared LDA settings live in modeling/lda_common.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'modeling'))
from lda_common import LDA_PARAMS, fit_lda_model  # noqa: E402

TOP_N = 20


def run_seed_stability(doc_term_matrix, vocab, seeds, num_topics):
    """Fit one model per seed and match every pair of seeds.

    Returns:
        seed_info: {seed: {'perplexity': float, 'n_iter': int}}
        pairwise_results: {(seed1, seed2): {'matches', 'summary', 'similarity_matrix'}}
    """
    print(f"\nFitting {len(seeds)} LDA models with different seeds...")
    models_by_seed = {}
    seed_info = {}
    for seed in seeds:
        print(f"   Seed {seed}...")
        lda = fit_lda_model(doc_term_matrix, num_topics, seed)
        models_by_seed[seed] = lda
        seed_info[seed] = {'perplexity': float(lda.perplexity(doc_term_matrix)), 'n_iter': int(lda.n_iter_)}
        print(f"     Perplexity: {seed_info[seed]['perplexity']:.2f}, Iterations: {lda.n_iter_}")

    seed_pairs = list(combinations(seeds, 2))
    print(f"\nComputing pairwise topic matching ({len(seed_pairs)} pairs)...")
    pairwise_results = {}
    for seed1, seed2 in seed_pairs:
        print(f"   Seeds {seed1} vs {seed2}...")
        matches, summary, similarity_matrix = match_and_evaluate(
            models_by_seed[seed1], models_by_seed[seed2], vocab, vocab, top_n=TOP_N)
        pairwise_results[(seed1, seed2)] = {
            'matches': matches,
            'summary': summary,
            'similarity_matrix': similarity_matrix,
        }

    return seed_info, pairwise_results


def stats_lines(values):
    return [
        f"- Mean: {np.mean(values):.4f}",
        f"- Median: {np.median(values):.4f}",
        f"- Min: {np.min(values):.4f}",
        f"- Max: {np.max(values):.4f}",
        f"- Std Dev: {np.std(values):.4f}",
    ]


def generate_report(title, weighting, num_topics, seed_info, pairwise_results, closing_lines=()):
    """Markdown report: method, per-seed fit, per-pair similarity, pooled summary."""
    seed_pairs = list(pairwise_results)
    lines = [
        f"# {title}",
        "",
        "## Methodology",
        "",
        "**Matching:** topics are optimally matched across models using the Hungarian algorithm,",
        "accounting for the fact that topic indices are arbitrary across LDA runs.",
        "",
        f"**Weighting:** {weighting}",
        "",
        "**Matching criterion:** Cosine similarity over normalized topic-word distributions",
        "",
        f"**Secondary metric:** Jaccard overlap of top {TOP_N} words (for interpretability)",
        "",
        f"**LDA settings:** {num_topics} topics, " + ', '.join(f"{k}={v}" for k, v in LDA_PARAMS.items()),
        "",
        "## Models per Seed",
        "",
        "Training perplexity is diagnostic only. sklearn's online LDA does not test for convergence",
        f"(evaluate_every=-1), so every fit runs exactly max_iter={LDA_PARAMS['max_iter']} passes;",
        "the iteration count confirms the setting, not convergence.",
        "",
        "| Seed | Training perplexity | Iterations |",
        "|---|---|---|",
    ]
    for seed, info in seed_info.items():
        lines.append(f"| {seed} | {info['perplexity']:.2f} | {info['n_iter']} |")
    lines += ["", "## Pairwise Comparisons", ""]

    all_cosine, all_jaccard = [], []
    for seed1, seed2 in seed_pairs:
        matches = pairwise_results[(seed1, seed2)]['matches']
        cosine = [m[2] for m in matches]
        jaccard = [m[3] for m in matches]
        all_cosine.extend(cosine)
        all_jaccard.extend(jaccard)
        lines += [f"### Seed {seed1} vs Seed {seed2}", "",
                  "**Cosine Similarity (full topic distributions):**", *stats_lines(cosine), "",
                  f"**Jaccard Similarity (top {TOP_N} words):**", *stats_lines(jaccard), ""]

    lines += [
        "## Overall Summary Statistics",
        "",
        f"**Total seed pairs tested:** {len(seed_pairs)}",
        f"**Total matched topic pairs:** {len(all_cosine)}",
        "",
        "**Note on the pooled values:** the matched topic pairs are not independent. Each seed's model",
        f"appears in {len(seed_info) - 1} of the {len(seed_pairs)} pairs, so the pooled values below reuse",
        "the same topics several times. The pooled mean is a fair summary, but the pooled standard",
        "deviation understates the real uncertainty. For spread across runs, compare the per-pair",
        "means above.",
        "",
        "### Cosine Similarity (across all matches)", *stats_lines(all_cosine), "",
        "### Jaccard Similarity (across all matches)", *stats_lines(all_jaccard), "",
        *closing_lines,
    ]
    return '\n'.join(lines)


def save_report(report, output_file):
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n✅ Report saved to: {output_file}")
