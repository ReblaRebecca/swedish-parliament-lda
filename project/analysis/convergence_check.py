#!/usr/bin/env python3
"""
Convergence check of the 50-pass LDA fits (LDA_PARAMS in modeling/lda_common.py).

sklearn's online LDA runs exactly max_iter passes and does not test for convergence. This script fits
each model once with MAX_PASSES passes and the reported seed, keeping a copy of the model at each
checkpoint, and compares every checkpoint with the final model: training perplexity, and the matched
mean cosine of the topics (Hungarian matching, as the seed-stability test). If the topics after 50
passes match the final ones much more closely than two seeds' models match each other, more passes
would not change the results.

Fitting pass by pass with partial_fit (total_samples = number of motions) gives exactly the model that
fit() gives with the same number of passes, so the checkpoint at 50 is the reported model's setting.

Models: the whole-corpus model (NUM_TOPICS) and the four period models (PERIOD_TOPICS), on the motions
the models currently select (lda_common: length minimum, no duplicates) from the preprocessed data.

Runtime: about 25 minutes (5 fits of 200 passes, perplexity at every checkpoint).

Usage: python analysis/convergence_check.py
Output: docs/reports/CONVERGENCE_CHECK.md
"""

import copy
import sys
import time
from pathlib import Path

import numpy as np

from seed_stability import FOUND_COSINE
from topic_matching import match_and_evaluate

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'modeling'))
from lda_common import (  # noqa: E402
    DEFAULT_SEED, NUM_TOPICS, PERIOD_TOPICS, fit_period_vectorizer,
    load_body_texts, load_period_body_texts, new_lda_model, period_display,
)

MAX_PASSES = 200
CHECKPOINTS = [10, 25, 50, 100, 150, 200]


def fit_with_checkpoints(doc_term_matrix, num_topics):
    """Fit pass by pass; return ({passes: model copy}, seconds)."""
    lda = new_lda_model(num_topics, DEFAULT_SEED, max_iter=MAX_PASSES, total_samples=doc_term_matrix.shape[0])
    snapshots = {}
    start = time.time()
    for done in range(1, MAX_PASSES + 1):
        lda.partial_fit(doc_term_matrix)
        if done in CHECKPOINTS:
            snapshots[done] = copy.deepcopy(lda)
    return snapshots, time.time() - start


def compare_checkpoints(snapshots, doc_term_matrix, vocab):
    """One row per checkpoint: perplexity and the matched cosine with the final model."""
    final = snapshots[MAX_PASSES]
    rows = []
    for passes, model in snapshots.items():
        matches, _, _ = match_and_evaluate(model, final, vocab, vocab)
        cosines = np.array([m[2] for m in matches])
        rows.append({
            'passes': passes,
            'perplexity': model.perplexity(doc_term_matrix),
            'mean_cosine': float(cosines.mean()),
            'min_cosine': float(cosines.min()),
            'found': int((cosines >= FOUND_COSINE).sum()),
            'topics': len(cosines),
        })
    return rows


def check(label, texts, num_topics):
    print(f"{label}: {len(texts)} motions, {num_topics} topics, {MAX_PASSES} passes...", flush=True)
    # The vocabulary rule of every model (VECTORIZER_PARAMS), built on these motions
    vectorizer = fit_period_vectorizer(texts)
    doc_term_matrix = vectorizer.transform(texts)
    vocab = vectorizer.get_feature_names_out()
    snapshots, seconds = fit_with_checkpoints(doc_term_matrix, num_topics)
    rows = compare_checkpoints(snapshots, doc_term_matrix, vocab)
    at50 = next(r for r in rows if r['passes'] == 50)
    print(f"   {seconds / 60:.1f} min; at 50 passes: mean cosine with {MAX_PASSES} passes {at50['mean_cosine']:.3f}, "
          f"{at50['found']}/{at50['topics']} topics >= {FOUND_COSINE}", flush=True)
    return {'label': label, 'motions': len(texts), 'vocabulary': len(vocab), 'topics': num_topics,
            'minutes': seconds / 60, 'rows': rows}


def report(results):
    lines = [
        '# Convergence Check of the LDA Fits',
        '',
        f'Each model fitted once with {MAX_PASSES} passes (seed {DEFAULT_SEED}, otherwise the shared LDA settings), '
        f'with a copy kept at {", ".join(map(str, CHECKPOINTS[:-1]))} passes. Every checkpoint is compared with '
        f'the {MAX_PASSES}-pass model: training perplexity, and the topics matched one-to-one (Hungarian, cosine '
        f'over the full vocabulary). *Found*: topics with matched cosine at least {FOUND_COSINE} (as the '
        'seed-stability test). The reported models use 50 passes.',
        '',
        'Data: the motions the models currently select (length minimum, no duplicates) from the preprocessed '
        'data at the time of the check.',
        '',
    ]
    for r in results:
        lines += [
            f"## {r['label']}",
            '',
            f"{r['motions']:,} motions, {r['vocabulary']:,} words, {r['topics']} topics; "
            f"{MAX_PASSES} passes took {r['minutes']:.1f} minutes.",
            '',
            f"| Passes | Perplexity | Change from previous | Mean cosine with {MAX_PASSES} | Min cosine | Found |",
            '|---|---|---|---|---|---|',
        ]
        previous = None
        for row in r['rows']:
            change = f"{(row['perplexity'] / previous - 1) * 100:+.2f}%" if previous else '–'
            lines.append(f"| {row['passes']} | {row['perplexity']:,.1f} | {change} | {row['mean_cosine']:.3f} | "
                         f"{row['min_cosine']:.3f} | {row['found']}/{row['topics']} |")
            previous = row['perplexity']
        lines.append('')
    return '\n'.join(lines)


def main():
    project_root = Path(__file__).resolve().parent.parent
    input_dir = project_root / 'data' / 'output' / 'stopword_removed'
    output = project_root / 'docs' / 'reports' / 'CONVERGENCE_CHECK.md'

    texts, _, _ = load_body_texts(input_dir)
    results = [check('Whole-corpus model', texts, NUM_TOPICS)]
    periods, _ = load_period_body_texts(input_dir)
    for period, (period_texts, _) in periods.items():
        results.append(check(f'Period model {period_display(period)}', period_texts, PERIOD_TOPICS))

    output.write_text(report(results) + '\n', encoding='utf-8')
    print(f"✅ Report saved to: {output}")


if __name__ == '__main__':
    main()
