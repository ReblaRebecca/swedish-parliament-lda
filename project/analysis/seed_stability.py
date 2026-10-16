#!/usr/bin/env python3
"""
Shared seed-stability procedure for the baseline and title-weighted models.

Fits one LDA model per seed on the same document-term matrix and vocabulary, matches topics
between every pair of seeds with the Hungarian algorithm (topic indices are arbitrary between
runs), and writes a markdown report. The report also gives the stability of each topic of the
reference model (the seed of the reported model, DEFAULT_SEED): how well it is found again in
the other seeds' models.
Used by 09_test_lda_stability.py and 13_seed_stability_{3x,5x}_weighted.py.
"""

import csv
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

from topic_matching import match_and_evaluate

# Shared LDA settings live in modeling/lda_common.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'modeling'))
from lda_common import DEFAULT_SEED, LDA_PARAMS, fit_lda_model  # noqa: E402

TOP_N = 20

# A reference topic counts as found again in another seed's model if its matched topic there
# has at least this cosine similarity. A judgement call: matched topics that are the same theme
# typically score well above it, chance matches well below.
FOUND_COSINE = 0.70

# Top words listed per topic in the per-topic table
TABLE_WORDS = 8


def run_seed_stability(doc_term_matrix, vocab, seeds, num_topics):
    """Fit one model per seed and match every pair of seeds.

    Returns:
        seed_info: {seed: {'perplexity': float, 'n_iter': int, 'top_words': [[word, ...] per topic]}}
        pairwise_results: {(seed1, seed2): {'matches', 'summary', 'similarity_matrix'}}
    """
    print(f"\nFitting {len(seeds)} LDA models with different seeds...")
    models_by_seed = {}
    seed_info = {}
    for seed in seeds:
        print(f"   Seed {seed}...")
        lda = fit_lda_model(doc_term_matrix, num_topics, seed)
        models_by_seed[seed] = lda
        seed_info[seed] = {
            'perplexity': float(lda.perplexity(doc_term_matrix)),
            'n_iter': int(lda.n_iter_),
            'top_words': [[vocab[i] for i in np.argsort(row)[::-1][:TABLE_WORDS]] for row in lda.components_],
        }
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


def per_topic_stability(pairwise_results, reference_seed, num_topics):
    """For each topic of the reference seed's model: its matches in every other seed's model.

    Returns a list (one row per reference topic, in topic order) of dicts with
    'topic' (1-based), 'cosines' and 'jaccards' (one value per other seed), 'found' (number of
    other seeds where the matched cosine is at least FOUND_COSINE), 'mean_cosine', 'min_cosine',
    'mean_jaccard'.
    """
    cosines = [[] for _ in range(num_topics)]
    jaccards = [[] for _ in range(num_topics)]
    for (seed1, seed2), result in pairwise_results.items():
        if reference_seed not in (seed1, seed2):
            continue
        for t1, t2, cosine, jaccard in result['matches']:
            ref_topic = t1 if seed1 == reference_seed else t2
            cosines[ref_topic].append(cosine)
            jaccards[ref_topic].append(jaccard)
    if not any(cosines):
        raise ValueError(f"Reference seed {reference_seed} is not among the compared seeds")

    return [{
        'topic': k + 1,
        'cosines': cosines[k],
        'jaccards': jaccards[k],
        'found': sum(c >= FOUND_COSINE for c in cosines[k]),
        'mean_cosine': float(np.mean(cosines[k])),
        'min_cosine': float(np.min(cosines[k])),
        'mean_jaccard': float(np.mean(jaccards[k])),
    } for k in range(num_topics)]


def per_topic_lines(rows, seed_info, reference_seed):
    """Markdown section with the stability of each reference topic."""
    others = len(rows[0]['cosines'])
    distribution = {n: sum(r['found'] == n for r in rows) for n in range(others, -1, -1)}
    top_words = seed_info[reference_seed]['top_words']
    lines = [
        f"## Stability per Topic (reference model: seed {reference_seed})",
        "",
        f"Each topic of the seed-{reference_seed} model (the seed of the reported model) is compared with",
        f"its matched topic in each of the other {others} models. *Found* counts the models where the",
        f"match has cosine similarity ≥ {FOUND_COSINE:.2f}; this threshold is a judgement call. Interpret",
        "topics that are found in all models with more confidence than the others.",
        "",
        "| Found in | Topics |",
        "|---|---|",
    ]
    lines += [f"| {n} of {others} | {count} |" for n, count in distribution.items()]
    lines += [
        "",
        "| Topic | Top words | Found | Mean cosine | Min cosine | Mean Jaccard |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        words = ', '.join(top_words[r['topic'] - 1])
        lines.append(f"| {r['topic']} | {words} | {r['found']}/{others} | {r['mean_cosine']:.3f} | "
                     f"{r['min_cosine']:.3f} | {r['mean_jaccard']:.3f} |")
    lines.append("")
    return lines


def save_topic_stability(rows, seed_info, reference_seed, output_file):
    """Per-topic stability of the reference model as CSV (e.g. for the topic explorer)."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    top_words = seed_info[reference_seed]['top_words']
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['topic', 'found', 'compared', 'mean_cosine', 'min_cosine', 'mean_jaccard', 'top_words'])
        for r in rows:
            writer.writerow([r['topic'], r['found'], len(r['cosines']), f"{r['mean_cosine']:.4f}",
                             f"{r['min_cosine']:.4f}", f"{r['mean_jaccard']:.4f}", ' '.join(top_words[r['topic'] - 1])])
    print(f"✅ Per-topic stability saved to: {output_file}")


def stats_lines(values):
    return [
        f"- Mean: {np.mean(values):.4f}",
        f"- Median: {np.median(values):.4f}",
        f"- Min: {np.min(values):.4f}",
        f"- Max: {np.max(values):.4f}",
        f"- Std Dev: {np.std(values):.4f}",
    ]


def generate_report(title, weighting, num_topics, seed_info, pairwise_results, closing_lines=(),
                    reference_seed=DEFAULT_SEED):
    """Markdown report: method, per-seed fit, per-topic stability of the reference model,
    per-pair similarity, pooled summary."""
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
    lines.append("")
    lines += per_topic_lines(per_topic_stability(pairwise_results, reference_seed, num_topics), seed_info, reference_seed)
    lines += ["## Pairwise Comparisons", ""]

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
