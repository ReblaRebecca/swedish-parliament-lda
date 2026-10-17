#!/usr/bin/env python3
"""
Generate the period explorer: one self-contained HTML page with four word clouds per topic, one
for each period, for the period models with 8, 11 and 15 topics (switchable on the page).

Each period model has its own topics, so "topic 3" in one period is not topic 3 in the next. The
rows are therefore chains: topics of adjacent periods are matched one-to-one with the Hungarian
algorithm on cosine similarity (topic_matching.py), and each row follows the matches from the first
period to the last. The cosine of every link is shown; links below CHAIN_COSINE are marked weak.
This is a provisional alignment for inspection, without Gordon's permutation null.

Input:  models/period_lda_<k>/ (15_fit_period_lda.py), baseline vectorizer, data/output/stopword_removed/,
        results/period_stability/PERIOD_<period>_<k>TOPICS_PER_TOPIC.csv (16_seed_stability_periods.py; optional)
Output: visualizations/period_explorer.html (open in a browser; needs internet for the fonts)

Usage: python modeling/17_generate_period_explorer.py [num_topics ...]   (default: 8 11 15)
"""

import csv
import json
import pickle
import sys
from datetime import date
from pathlib import Path

import numpy as np

from lda_common import load_baseline_vectorizer, load_period_body_texts

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'analysis'))
from topic_matching import match_and_evaluate  # noqa: E402

TOPIC_COUNTS = [8, 11, 15]
TOP_WORDS = 20
# Gordon's chain criterion: adjacent topics with cosine at least this are linked
CHAIN_COSINE = 0.50
# Top words compared with the stability CSV to make sure it describes the same model
STABILITY_CHECK_WORDS = 8


def build_chains(models, vocab):
    """Rows of topic indices, one per topic of the first period, following adjacent Hungarian matches.

    models: list of fitted LDA models in period order (same number of topics, same vocabulary).
    Returns (chains, links): chains[r][p] is the topic index of row r in period p;
    links[r][p] is the cosine between period p and p+1 in row r.
    """
    num_topics = models[0].n_components
    chains = [[t] for t in range(num_topics)]
    links = [[] for _ in range(num_topics)]
    for p in range(len(models) - 1):
        matches, _, _ = match_and_evaluate(models[p], models[p + 1], vocab, vocab)
        next_topic = {t1: (t2, cosine) for t1, t2, cosine, _ in matches}
        for r in range(num_topics):
            t2, cosine = next_topic[chains[r][-1]]
            chains[r].append(t2)
            links[r].append(round(float(cosine), 3))
    return chains, links


def load_stability(csv_path, lda, vocab):
    """{topic index: found} from the per-topic stability CSV, or None if missing or for another model."""
    if not csv_path.exists():
        return None
    with open(csv_path, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    if len(rows) != lda.n_components:
        return None
    stability = {}
    for k, row in enumerate(rows):
        top = [vocab[i] for i in np.argsort(lda.components_[k])[::-1][:STABILITY_CHECK_WORDS]]
        if row['top_words'].split() != top:
            return None
        stability[k] = {'found': int(row['found']), 'of': int(row['compared'])}
    return stability


def topic_words(lda, k, vocab):
    topic_word = lda.components_[k] / lda.components_[k].sum()
    return [[vocab[i], round(float(topic_word[i]), 5)] for i in np.argsort(topic_word)[::-1][:TOP_WORDS]]


def model_set_data(num_topics, periods, vectorizer, vocab, model_dir, stability_dir):
    """Chains, clouds, shares and stability for the period models with num_topics topics."""
    labels = list(periods)
    models, shares, stabilities = [], [], []
    for period in labels:
        with open(model_dir / f'period_{period}_lda.pkl', 'rb') as f:
            lda = pickle.load(f)
        if lda.n_components != num_topics or lda.components_.shape[1] != len(vocab):
            raise ValueError(f"{model_dir}: model for {period} does not match {num_topics} topics and the vocabulary")
        texts, _ = periods[period]
        theta = lda.transform(vectorizer.transform(texts))
        theta = theta / theta.sum(axis=1, keepdims=True)
        models.append(lda)
        shares.append(theta.mean(axis=0))
        stabilities.append(load_stability(stability_dir / f'PERIOD_{period}_{num_topics}TOPICS_PER_TOPIC.csv', lda, vocab))

    chains, links = build_chains(models, vocab)
    rows = []
    for r, chain in enumerate(chains):
        cells = []
        for p, t in enumerate(chain):
            stability = stabilities[p][t] if stabilities[p] else None
            cells.append({'topic': t + 1, 'words': topic_words(models[p], t, vocab),
                          'share': round(float(shares[p][t]), 4), 'stability': stability})
        rows.append({'row': r + 1, 'cells': cells, 'links': links[r]})
    return {'rows': rows, 'stabilityAvailable': [s is not None for s in stabilities]}


def main():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
    VECTORIZER_PATH = PROJECT_ROOT / 'models' / 'baseline_lda_44' / 'baseline_vectorizer.pkl'
    STABILITY_DIR = PROJECT_ROOT / 'results' / 'period_stability'
    TEMPLATE = Path(__file__).resolve().parent / 'period_explorer_template.html'
    OUTPUT = PROJECT_ROOT / 'visualizations' / 'period_explorer.html'
    topic_counts = [int(a) for a in sys.argv[1:]] or TOPIC_COUNTS

    vectorizer = load_baseline_vectorizer(VECTORIZER_PATH)
    vocab = vectorizer.get_feature_names_out()
    periods, _ = load_period_body_texts(INPUT_DIR)

    data = {
        'periods': list(periods),
        'periodCounts': [len(texts) for texts, _ in periods.values()],
        'chainCosine': CHAIN_COSINE,
        'generated': date.today().isoformat(),
        'sets': {},
    }
    for k in topic_counts:
        model_dir = PROJECT_ROOT / 'models' / f'period_lda_{k}'
        if not model_dir.exists():
            print(f"Error: {model_dir} not found. Run: python modeling/15_fit_period_lda.py {k}")
            sys.exit(1)
        print(f"{k} topics: inferring topic shares and matching adjacent periods...")
        data['sets'][str(k)] = model_set_data(k, periods, vectorizer, vocab, model_dir, STABILITY_DIR)
        if not all(data['sets'][str(k)]['stabilityAvailable']):
            print(f"   ⚠️  seed stability missing or for another model in some periods (run 16_seed_stability_periods.py {k})")

    html = TEMPLATE.read_text(encoding='utf-8')
    assert html.count('__PERIOD_DATA__') == 1, 'template must contain the data placeholder once'
    html = html.replace('__PERIOD_DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding='utf-8')
    print(f"✅ Period explorer saved to: {OUTPUT} ({OUTPUT.stat().st_size / 1024:.0f} KB)")


if __name__ == '__main__':
    main()
