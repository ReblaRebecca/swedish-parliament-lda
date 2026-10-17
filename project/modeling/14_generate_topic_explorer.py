#!/usr/bin/env python3
"""
Generate the topic explorer: one self-contained HTML page with a word cloud per topic of the
whole-corpus model (body text only), each topic's share overall and per period, its
highest-loading motions, and the party concentration among its top 5 motions.

Reads the fitted model directly (not the CSV export), so the page always shows the model
in models/. Replaces the earlier word cloud scripts and their template.

Input:  models/baseline_lda_44/, data/output/stopword_removed/
Output: visualizations/topic_explorer.html (open in a browser; needs internet for the fonts)

Definitions used on the page:
- Word size: P(word | topic), square-root scaled, top 30 words.
- Share: mean topic proportion over the motions (every motion counts equally).
- Party concentration: share of the topic's top 5 motions whose first signatory belongs to
  the most frequent party among them (parliamentary analogue of Gordon's author concentration).
"""

import json
import pickle
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import numpy as np

from lda_common import NUM_TOPICS, load_baseline_vectorizer, load_body_texts

PERIODS = [('1986–1993', 1986, 1993), ('1994–2004', 1994, 2004), ('2005–2014', 2005, 2014), ('2015–2025', 2015, 2025)]
TOP_WORDS = 30
TOP_MOTIONS = 8
CONCENTRATION_TOP = 5


def load_first_signatory_parties(input_dir):
    """dok_id -> party of the first signatory ('' if unknown)."""
    parties = {}
    for bin_file in sorted(input_dir.glob('group*.jsonl')):
        with open(bin_file, 'r', encoding='utf-8') as f:
            for line in f:
                motion = json.loads(line)
                authors = motion.get('authors') or []
                parties[motion.get('dok_id')] = (authors[0].get('party') or '').upper() if authors else ''
    return parties


def period_index(year):
    for i, (_, start, end) in enumerate(PERIODS):
        if start <= int(year) <= end:
            return i
    return None


def model_data(lda, vocab, theta, metadata, parties):
    """Per-topic words, shares and top motions for one model."""
    periods = np.array([period_index(m['year']) for m in metadata])
    topic_word = lda.components_ / lda.components_.sum(axis=1, keepdims=True)
    topics = []
    for k in range(lda.n_components):
        top_word_ids = np.argsort(topic_word[k])[::-1][:TOP_WORDS]
        top_doc_ids = np.argsort(theta[:, k])[::-1][:TOP_MOTIONS]
        motions = [{
            'id': metadata[d]['doc_id'],
            'title': metadata[d]['title'],
            'year': metadata[d]['year'],
            'party': parties.get(metadata[d]['doc_id'], ''),
            'theta': round(float(theta[d, k]), 3),
        } for d in top_doc_ids]
        top_parties = Counter(m['party'] or '?' for m in motions[:CONCENTRATION_TOP])
        party, count = top_parties.most_common(1)[0]
        topics.append({
            'num': k + 1,
            'words': [[vocab[i], round(float(topic_word[k, i]), 5)] for i in top_word_ids],
            'share': round(float(theta[:, k].mean()), 5),
            'periods': [round(float(theta[periods == p, k].mean()), 5) for p in range(len(PERIODS))],
            'motions': motions,
            'party': party,
            'partyCount': count,
        })
    return topics


def main():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
    BASELINE_DIR = PROJECT_ROOT / 'models' / 'baseline_lda_44'
    TEMPLATE = Path(__file__).resolve().parent / 'topic_explorer_template.html'
    OUTPUT = PROJECT_ROOT / 'visualizations' / 'topic_explorer.html'

    vectorizer = load_baseline_vectorizer(BASELINE_DIR / 'baseline_vectorizer.pkl')
    vocab = vectorizer.get_feature_names_out()
    parties = load_first_signatory_parties(INPUT_DIR)

    model_path = BASELINE_DIR / f'baseline_lda_{NUM_TOPICS}_topics.pkl'
    if not model_path.exists():
        print(f"Error: {model_path} not found. Run 07_fit_baseline_lda.py first.")
        sys.exit(1)
    with open(model_path, 'rb') as f:
        lda = pickle.load(f)
    texts, metadata, _ = load_body_texts(INPUT_DIR)
    print(f"Inferring topic proportions for {len(texts)} motions...")
    theta = lda.transform(vectorizer.transform(texts))
    theta = theta / theta.sum(axis=1, keepdims=True)
    data = {
        'periods': [p[0] for p in PERIODS],
        'topicList': model_data(lda, vocab, theta, metadata, parties),
        'motions': len(texts),
        'periodCounts': [int(sum(1 for m in metadata if period_index(m['year']) == p)) for p in range(len(PERIODS))],
    }

    all_parties = Counter(p or '?' for p in parties.values())
    total = sum(all_parties.values())
    data['partyShares'] = [[p, round(n / total, 3)] for p, n in all_parties.most_common(8)]
    data['generated'] = date.today().isoformat()
    data['topics'] = NUM_TOPICS

    html = TEMPLATE.read_text(encoding='utf-8')
    assert html.count('__TOPIC_DATA__') == 1, 'template must contain the data placeholder once'
    html = html.replace('__TOPIC_DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding='utf-8')
    print(f"✅ Topic explorer saved to: {OUTPUT} ({OUTPUT.stat().st_size / 1024:.0f} KB)")


if __name__ == '__main__':
    main()
