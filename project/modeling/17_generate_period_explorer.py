#!/usr/bin/env python3
"""
Generate the period explorer: one self-contained HTML page with four word clouds per topic, one
for each period, for the period models with the chosen number of topics (PERIOD_TOPICS in lda_common.py).

Each period model has its own topics, so "topic 3" in one period is not topic 3 in the next. The
rows are therefore chains: topics of adjacent periods are matched one-to-one with the Hungarian
algorithm on cosine similarity over the words both periods' vocabularies contain (topic_matching.py, as Gordon), and each row follows the matches from the first
period to the last. A chain holds if the mean cosine of its links is at least CHAIN_COSINE (Gordon);
the cosine of every link is shown, and single links below CHAIN_COSINE are marked weak.
Gordon's permutation test of the alignment is in analysis/18_alignment_null.py.
Words: the TOP_WORDS most relevant words of each topic (relevance with λ = RELEVANCE_LAMBDA, Sievert &
Shirley 2014; P(word) from the period's own motions); size is P(word | topic).
Word colour shows persistence: in how many of the chain's periods the word is among the words shown
(computed on the page).

Input:  models/period_lda_<k>/ (15_fit_period_lda.py: models and vectorizers), data/output/stopword_removed/,
        config/period_topic_names_<k>.tsv and config/chain_names_<k>.tsv (names; optional),
        results/period_stability/PERIOD_<period>_<k>TOPICS_PER_TOPIC.csv (16_seed_stability_periods.py; optional;
        shown only for the model it was run on)
        (k = PERIOD_TOPICS)
Output: visualizations/period_explorer.html (open in a browser; needs internet for the fonts)

Usage: python modeling/17_generate_period_explorer.py
"""

import json
import pickle
import sys
from pathlib import Path

import numpy as np

from lda_common import (
    PERIOD_TOPICS, RELEVANCE_LAMBDA, load_period_body_texts, load_seed_stability, load_topic_names, most_probable_words,
    period_display,
    relevant_words, topic_word_distributions, word_marginal,
)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'analysis'))
from topic_matching import match_and_evaluate  # noqa: E402

TOP_WORDS = 20
# Gordon's chain criterion: a chain holds if the mean cosine of its links is at least this.
# The page also marks each single link below it as weak.
CHAIN_COSINE = 0.50


def build_chains(models, vocabs):
    """Rows of topic indices, one per topic of the first period, following adjacent Hungarian matches.

    models: list of fitted LDA models in period order (same number of topics); vocabs: each model's
    vocabulary. Adjacent models are compared over the words both vocabularies contain.
    Returns (chains, links): chains[r][p] is the topic index of row r in period p;
    links[r][p] is the cosine between period p and p+1 in row r.
    """
    num_topics = models[0].n_components
    chains = [[t] for t in range(num_topics)]
    links = [[] for _ in range(num_topics)]
    for p in range(len(models) - 1):
        matches, _, _ = match_and_evaluate(models[p], models[p + 1], vocabs[p], vocabs[p + 1], shared_vocabulary=True)
        next_topic = {t1: (t2, cosine) for t1, t2, cosine, _ in matches}
        for r in range(num_topics):
            t2, cosine = next_topic[chains[r][-1]]
            chains[r].append(t2)
            links[r].append(round(float(cosine), 3))
    return chains, links


def topic_words(topic_word, marginal, vocab):
    """The TOP_WORDS most relevant words of one topic, with P(word | topic)."""
    return [[vocab[i], round(float(topic_word[i]), 5)] for i in relevant_words(topic_word, marginal, TOP_WORDS)]


def model_set_data(num_topics, periods, model_dir, names_path=None, chain_names_path=None, stability_dir=None):
    """Chains, clouds, shares, names and seed stability for the period models with num_topics topics."""
    labels = list(periods)
    models, vocabs, shares, topic_word_dists, marginals, stabilities = [], [], [], [], [], []
    for period in labels:
        with open(model_dir / f'period_{period}_lda.pkl', 'rb') as f:
            lda = pickle.load(f)
        with open(model_dir / f'period_{period}_vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        vocab = vectorizer.get_feature_names_out()
        if lda.n_components != num_topics or lda.components_.shape[1] != len(vocab):
            raise ValueError(f"{model_dir}: model for {period} does not match {num_topics} topics and its vocabulary")
        texts, _ = periods[period]
        doc_term = vectorizer.transform(texts)
        theta = lda.transform(doc_term)
        theta = theta / theta.sum(axis=1, keepdims=True)
        models.append(lda)
        vocabs.append(vocab)
        shares.append(theta.mean(axis=0))
        topic_word_dists.append(topic_word_distributions(lda))
        marginals.append(word_marginal(doc_term))
        stabilities.append(load_seed_stability(stability_dir / f'PERIOD_{period}_{num_topics}TOPICS_PER_TOPIC.csv',
                                               topic_word_dists[-1], vocab) if stability_dir else None)

    chains, links = build_chains(models, vocabs)
    top3 = {(period, str(t + 1)): most_probable_words(topic_word_dists[p][t], vocabs[p])
            for p, period in enumerate(labels) for t in range(num_topics)}
    names = load_topic_names(names_path, top3) if names_path else {}
    print(f"Topic names: {len(names)} of {len(top3)}")
    # A chain is identified by its topic numbers in the four periods
    signatures = {(str(r + 1),): ' '.join(str(t + 1) for t in chain) for r, chain in enumerate(chains)}
    chain_names = load_topic_names(chain_names_path, signatures) if chain_names_path else {}
    print(f"Chain names: {len(chain_names)} of {len(signatures)}")
    rows = []
    for r, chain in enumerate(chains):
        cells = []
        for p, t in enumerate(chain):
            cells.append({'topic': t + 1, 'words': topic_words(topic_word_dists[p][t], marginals[p], vocabs[p]),
                          'share': round(float(shares[p][t]), 4),
                          'name': names.get((labels[p], str(t + 1)), ''),
                          'stability': stabilities[p][t] if stabilities[p] else None})
        rows.append({'row': r + 1, 'cells': cells, 'links': links[r], 'name': chain_names.get((str(r + 1),), '')})
    available = sum(s is not None for s in stabilities)
    print(f"Seed stability: shown for {available} of {len(labels)} periods"
          + ("" if available == len(labels) else " (missing or for another model; run 16_seed_stability_periods.py)"))
    return {'rows': rows}


def main():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
    TEMPLATE = Path(__file__).resolve().parent / 'period_explorer_template.html'
    OUTPUT = PROJECT_ROOT / 'visualizations' / 'period_explorer.html'

    periods, _ = load_period_body_texts(INPUT_DIR)

    data = {
        'periods': [period_display(p) for p in periods],
        'periodCounts': [len(texts) for texts, _ in periods.values()],
        'chainCosine': CHAIN_COSINE,
        'numTopics': PERIOD_TOPICS,
        'relevanceLambda': RELEVANCE_LAMBDA,
    }
    k = PERIOD_TOPICS
    model_dir = PROJECT_ROOT / 'models' / f'period_lda_{k}'
    if not model_dir.exists():
        print(f"Error: {model_dir} not found. Run: python modeling/15_fit_period_lda.py")
        sys.exit(1)
    print(f"{k} topics: inferring topic shares and matching adjacent periods...")
    data.update(model_set_data(k, periods, model_dir,
                              PROJECT_ROOT / 'config' / f'period_topic_names_{k}.tsv',
                              PROJECT_ROOT / 'config' / f'chain_names_{k}.tsv',
                              PROJECT_ROOT / 'results' / 'period_stability'))

    html = TEMPLATE.read_text(encoding='utf-8')
    assert html.count('__PERIOD_DATA__') == 1, 'template must contain the data placeholder once'
    html = html.replace('__PERIOD_DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding='utf-8')
    print(f"✅ Period explorer saved to: {OUTPUT} ({OUTPUT.stat().st_size / 1024:.0f} KB)")


if __name__ == '__main__':
    main()
