#!/usr/bin/env python3
"""
Deduplication comparison: the same models fitted on three selections of the motions, to show what removing
duplicates changes.

    none   length minimum only (every submission counts)
    exact  also identical final texts removed
    near   also near-duplicates removed (revised resubmissions; the models' setting)

For each selection, with the reported settings (lda_common) and the stability seeds:
- Whole-corpus model (NUM_TOPICS): seed stability (mean of the per-pair mean cosines, stable topics);
  of the seed-42 model, topics under 1% of the corpus, topics whose top 10 motions contain a series of
  related texts (SERIES_MIN or more motions linked by at least SERIES_JACCARD of their three-word
  sequences), and topics whose top 10 motions have at least PARTY_MIN of one party.
- Period models (PERIOD_TOPICS per period): seed stability per period; of the seed-42 models, the
  alignment of adjacent periods (matched cosine, permutation test) and the chains (mean link >= 0.50).
- The whole-corpus models of 'none' and 'exact' compared with 'near': topics matched one-to-one, and among
  the topics found in both, those whose shares per period change most.

Duplicates will probably make the models look more stable (repeated texts are easy to reproduce with any
seed), so higher stability without deduplication is not by itself an argument for keeping duplicates.

Runtime: about 30-40 minutes per selection (5 whole-corpus and 20 period fits each).

Usage: python analysis/dedup_comparison.py
Output: docs/reports/DEDUP_COMPARISON.md, results/dedup_comparison.json
"""

import importlib
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

from seed_stability import FOUND_COSINE, per_topic_stability, run_seed_stability
from topic_matching import match_and_evaluate, permutation_null

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'modeling'))
from lda_common import (  # noqa: E402
    DEDUP_LEVELS, DEFAULT_SEED, NEAR_DUPLICATE_JACCARD, NUM_TOPICS, PERIOD_TOPICS, SHINGLE_WORDS, STABILITY_SEEDS,
    fit_period_vectorizer, load_body_texts, period_display,
)

period_explorer = importlib.import_module('17_generate_period_explorer')
topic_explorer = importlib.import_module('14_generate_topic_explorer')

CHAIN_COSINE = period_explorer.CHAIN_COSINE
TOP_MOTIONS = 10
SERIES_JACCARD = 0.3   # texts this similar count as one series (revisions of the same motion)
SERIES_MIN = 5         # a topic is series-dominated if its top motions hold a series this long
PARTY_MIN = 6   # a topic is a one-party topic if at least this many of its top motions share the first signatory's party
SMALL_SHARE = 0.01
CHANGED_TOPICS = 5


def stability_summary(seed_info, pairwise, num_topics):
    """Mean of the per-pair mean cosines, its range, and topics found in 3-4 of the 4 other seeds."""
    pair_means = [float(np.mean([m[2] for m in r['matches']])) for r in pairwise.values()]
    rows = per_topic_stability(pairwise, DEFAULT_SEED, num_topics)
    others = len(STABILITY_SEEDS) - 1
    return {
        'mean_cosine': float(np.mean(pair_means)),
        'min_pair': min(pair_means),
        'max_pair': max(pair_means),
        'stable': sum(r['found'] >= others - 1 for r in rows),
        'found_all': sum(r['found'] == others for r in rows),
        'found_none': sum(r['found'] == 0 for r in rows),
        'topics': num_topics,
    }


def longest_series(texts):
    """Size of the largest group of texts linked (directly or through others) by SERIES_JACCARD of shingles."""
    shingles = CountVectorizer(ngram_range=(SHINGLE_WORDS, SHINGLE_WORDS), binary=True,
                               token_pattern=r'\S+').fit_transform(texts).astype(np.float32)
    shared = (shingles @ shingles.T).toarray()
    sizes = np.diag(shared)
    union = sizes[:, None] + sizes[None, :] - shared
    linked = np.divide(shared, union, out=np.zeros_like(shared), where=union > 0) >= SERIES_JACCARD
    group = list(range(len(texts)))  # union-find over the links

    def root(i):
        while group[i] != i:
            group[i] = group[group[i]]
            i = group[i]
        return i
    for i, j in zip(*np.nonzero(linked)):
        group[root(i)] = root(j)
    return max(np.bincount([root(i) for i in range(len(texts))]))


def whole_corpus(texts, metadata, parties):
    """Seed stability and the seed-42 model's topic diagnostics."""
    vectorizer = fit_period_vectorizer(texts)
    matrix = vectorizer.transform(texts)
    vocab = vectorizer.get_feature_names_out()
    seed_info, pairwise = run_seed_stability(matrix, vocab, STABILITY_SEEDS, NUM_TOPICS, keep_models=True)
    lda = seed_info[DEFAULT_SEED]['model']
    theta = lda.transform(matrix)
    theta = theta / theta.sum(axis=1, keepdims=True)
    periods = sorted({m['period'] for m in metadata})
    period_of = np.array([m['period'] for m in metadata])
    topics = []
    for k in range(NUM_TOPICS):
        top = np.argsort(theta[:, k])[::-1][:TOP_MOTIONS]
        party_counts = {}
        for d in top:
            party = topic_explorer.party_as_counted(parties.get(metadata[d]['doc_id'], ''))
            party_counts[party] = party_counts.get(party, 0) + 1
        topics.append({
            'words': [vocab[i] for i in np.argsort(lda.components_[k])[::-1][:3]],
            'share': float(theta[:, k].mean()),
            'periods': [float(theta[period_of == p, k].mean()) for p in periods],
            'series': int(longest_series([texts[d] for d in top])),
            'party_top': max(party_counts.values()),
        })
    return {
        'stability': stability_summary(seed_info, pairwise, NUM_TOPICS),
        'small': sum(t['share'] < SMALL_SHARE for t in topics),
        'series_topics': sum(t['series'] >= SERIES_MIN for t in topics),
        'party_topics': sum(t['party_top'] >= PARTY_MIN for t in topics),
        'topics': topics,
    }, lda, vocab


def period_models(texts, metadata):
    """Seed stability per period, and alignment and chains of the seed-42 models."""
    periods = sorted({m['period'] for m in metadata})
    stability, models, vocabs = {}, [], []
    for period in periods:
        period_texts = [t for t, m in zip(texts, metadata) if m['period'] == period]
        print(f"\n--- Period {period_display(period)}: {len(period_texts)} motions")
        vectorizer = fit_period_vectorizer(period_texts)
        vocab = vectorizer.get_feature_names_out()
        seed_info, pairwise = run_seed_stability(vectorizer.transform(period_texts), vocab, STABILITY_SEEDS,
                                                 PERIOD_TOPICS, keep_models=True)
        stability[period] = stability_summary(seed_info, pairwise, PERIOD_TOPICS)
        models.append(seed_info[DEFAULT_SEED]['model'])
        vocabs.append(vocab)
    transitions = []
    for p in range(len(models) - 1):
        _, _, similarity = match_and_evaluate(models[p], models[p + 1], vocabs[p], vocabs[p + 1],
                                              shared_vocabulary=True)
        result = permutation_null(similarity)
        transitions.append({'matched': result['matched_mean'], 'null': result['null_mean'], 'z': result['z']})
    _, links = period_explorer.build_chains(models, vocabs)
    means = [float(np.mean(link)) for link in links]
    return {
        'stability': stability,
        'transitions': transitions,
        'chains_hold': sum(m >= CHAIN_COSINE for m in means),
        'chains_all_strong': sum(min(link) >= CHAIN_COSINE for link in links),
    }


def compare_with(model, vocab, topics, reference_model, reference_vocab, reference_topics):
    """Topics of a model matched one-to-one with the reference model's, and the largest share changes."""
    matches, _, _ = match_and_evaluate(model, reference_model, vocab, reference_vocab, shared_vocabulary=True)
    cosines = [m[2] for m in matches]
    changes = []
    for t, r, cosine, _ in matches:
        diff = [a - b for a, b in zip(topics[t]['periods'], reference_topics[r]['periods'])]
        changes.append({'words': reference_topics[r]['words'], 'cosine': cosine,
                        'periods': topics[t]['periods'], 'reference_periods': reference_topics[r]['periods'],
                        'max_change': max(diff, key=abs)})
    # Share changes only for topics that are the same in both models; other matches pair different topics
    changes = sorted((c for c in changes if c['cosine'] >= FOUND_COSINE), key=lambda c: -abs(c['max_change']))
    return {'mean_cosine': float(np.mean(cosines)), 'found': sum(c >= FOUND_COSINE for c in cosines),
            'largest_changes': changes[:CHANGED_TOPICS]}


def pct(value):
    return f"{value * 100:.1f}%"


def report(results, periods):
    labels = {'none': 'No duplicates removed', 'exact': 'Exact duplicates removed',
              'near': 'Exact and near-duplicates removed (the models)'}
    lines = [
        '# Deduplication Comparison',
        '',
        'The same models fitted on three selections of the motions (`analysis/dedup_comparison.py`): '
        '*none* (length minimum only), *exact* (identical final texts removed) and *near* (also revised '
        f'resubmissions, Jaccard of three-word sequences ≥ {NEAR_DUPLICATE_JACCARD}; the models\' setting). Seeds '
        f'{", ".join(map(str, STABILITY_SEEDS))}; topic diagnostics from the seed-{DEFAULT_SEED} models.',
        '',
        'Duplicates will probably make the models look more stable, since repeated texts are easy to '
        'reproduce with any seed; higher stability without deduplication is not by itself an argument '
        'for keeping duplicates.',
        '',
        '## Motions',
        '',
        '| Selection | Motions | ' + ' | '.join(period_display(p) for p in periods) + ' |',
        '|---|---|' + '---|' * len(periods),
    ]
    for level in DEDUP_LEVELS:
        r = results[level]
        lines.append(f"| {labels[level]} | {r['motions']:,} | " + ' | '.join(f"{n:,}" for n in r['per_period']) + ' |')
    lines += [
        '',
        f'## Whole-corpus model ({NUM_TOPICS} topics)',
        '',
        f'*Stable*: found again (matched cosine ≥ {FOUND_COSINE}) in at least 3 of the 4 other seeds\' models. '
        f'*Small*: under {SMALL_SHARE:.0%} of the corpus. *Series-dominated*: the top {TOP_MOTIONS} motions '
        f'contain at least {SERIES_MIN} related texts (linked by ≥ {SERIES_JACCARD} of their three-word sequences, '
        f'e.g. one author\'s yearly resubmissions). *One party*: at least {PARTY_MIN} of the top {TOP_MOTIONS} '
        'motions have a first signatory from the same party.',
        '',
        '| Selection | Mean cosine (per-pair range) | Stable | Found in all / none | Small | Series-dominated | One party |',
        '|---|---|---|---|---|---|---|',
    ]
    for level in DEDUP_LEVELS:
        w = results[level]['whole']
        s = w['stability']
        lines.append(f"| {labels[level]} | {s['mean_cosine']:.3f} ({s['min_pair']:.3f}–{s['max_pair']:.3f}) | "
                     f"{s['stable']} of {s['topics']} | {s['found_all']} / {s['found_none']} | {w['small']} | "
                     f"{w['series_topics']} | {w['party_topics']} |")
    lines += [
        '',
        f'## Period models ({PERIOD_TOPICS} topics per period)',
        '',
        'Seed stability: mean cosine / stable topics per period. Alignment: matched mean cosine of adjacent '
        'periods (z of the permutation test). Chains: mean link ≥ 0.50 (all links ≥ 0.50).',
        '',
        '| Selection | ' + ' | '.join(period_display(p) for p in periods) + ' | Stable in all | Alignment | Chains hold |',
        '|---|' + '---|' * len(periods) + '---|---|---|',
    ]
    for level in DEDUP_LEVELS:
        pm = results[level]['periods']
        cells = [f"{pm['stability'][p]['mean_cosine']:.2f} / {pm['stability'][p]['stable']}" for p in periods]
        stable = sum(pm['stability'][p]['stable'] for p in periods)
        alignment = ', '.join(f"{t['matched']:.2f} ({t['z']:.1f})" for t in pm['transitions'])
        lines.append(f"| {labels[level]} | " + ' | '.join(cells) +
                     f" | {stable} of {PERIOD_TOPICS * len(periods)} | {alignment} | "
                     f"{pm['chains_hold']} of {PERIOD_TOPICS} ({pm['chains_all_strong']}) |")
    lines += [
        '',
        '## How much the whole-corpus topics change',
        '',
        'Each selection\'s seed-42 model matched one-to-one with the *near* model (cosine over the shared words). '
        f'*Found*: matched cosine ≥ {FOUND_COSINE}. The table lists, among the found topics, those whose share in a '
        'period changes most; shares per period in the selection and in the models.',
        '',
    ]
    for level in ('none', 'exact'):
        c = results[level]['compared_with_near']
        lines += [
            f"### {labels[level]} against the models",
            '',
            f"Mean matched cosine {c['mean_cosine']:.3f}; {c['found']} of {NUM_TOPICS} topics found.",
            '',
            '| Topic (top words, near model) | Cosine | Shares per period, ' + level + ' | Shares per period, near |',
            '|---|---|---|---|',
        ]
        for ch in c['largest_changes']:
            lines.append(f"| {', '.join(ch['words'])} | {ch['cosine']:.2f} | "
                         f"{' / '.join(pct(v) for v in ch['periods'])} | {' / '.join(pct(v) for v in ch['reference_periods'])} |")
        lines.append('')
    return '\n'.join(lines)


def main():
    input_dir = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
    parties = topic_explorer.load_first_signatory_parties(input_dir)
    results, fitted = {}, {}
    periods = None
    for level in DEDUP_LEVELS:
        print(f"\n{'=' * 80}\nSelection: {level}\n{'=' * 80}")
        texts, metadata, _ = load_body_texts(input_dir, dedup=level)
        periods = sorted({m['period'] for m in metadata})
        print(f"{len(texts)} motions")
        whole, lda, vocab = whole_corpus(texts, metadata, parties)
        results[level] = {
            'motions': len(texts),
            'per_period': [sum(1 for m in metadata if m['period'] == p) for p in periods],
            'whole': whole,
            'periods': period_models(texts, metadata),
        }
        fitted[level] = (lda, vocab)
    for level in ('none', 'exact'):
        results[level]['compared_with_near'] = compare_with(
            *fitted[level], results[level]['whole']['topics'], *fitted['near'], results['near']['whole']['topics'])

    (PROJECT_ROOT / 'results').mkdir(exist_ok=True)
    with open(PROJECT_ROOT / 'results' / 'dedup_comparison.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    output = PROJECT_ROOT / 'docs' / 'reports' / 'DEDUP_COMPARISON.md'
    output.write_text(report(results, periods) + '\n', encoding='utf-8')
    print(f"\n✅ Report saved to: {output}")


if __name__ == '__main__':
    main()
