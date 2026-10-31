#!/usr/bin/env python3
"""
Generate the topic explorer: one self-contained HTML page with a word cloud per topic of the
whole-corpus model (body text only), each topic's share overall and per period, its
highest-loading motions, and its seed stability.

Reads the fitted model directly (not the CSV export), so the page always shows the model
in models/.

Input:  models/<BASELINE_MODEL_DIR>/, data/output/stopword_removed/, config/topic_names_<k>.tsv,
        results/BASELINE_STABILITY_<k>TOPICS_PER_TOPIC.csv (optional)
Output: visualizations/topic_explorer.html (open in a browser; needs internet for the fonts)

Definitions used on the page:
- Words: the 20 most relevant words of the topic (relevance with λ = RELEVANCE_LAMBDA, Sievert & Shirley 2014;
  see lda_common.py), so that words frequent in every topic do not crowd out the distinctive ones.
- Word size: P(word | topic), square-root scaled, on one scale for all clouds (comparable between topics).
- Share: mean topic proportion over the motions (every motion counts equally).
- Stability: in how many of the other seeds' models the topic is found again (09_test_lda_stability.py,
  results/BASELINE_STABILITY_<k>TOPICS_PER_TOPIC.csv); shown only if that test was run on this model.
- Each top motion is shown with the party of its first signatory at the time.
"""

import json
import pickle
import sys
from pathlib import Path

import numpy as np

from lda_common import (
    BASELINE_MODEL_DIR, NUM_TOPICS, RELEVANCE_LAMBDA, load_baseline_vectorizer, load_body_texts, load_seed_stability,
    load_topic_names, most_probable_words, period_display, relevant_words, topic_word_distributions, word_marginal,
)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from periods import PERIODS, TERM_STARTS, period_key, term_name, term_of_session  # noqa: E402

# Period keys in order ('1985-1994', ...); a motion's period is the file it is stored in
PERIOD_KEYS = [period_key(stem) for stem, _, _ in PERIODS]
TOP_WORDS = 20
TOP_MOTIONS = 10

# Party code in the data -> (party it is counted as, name at the time). Folkpartiet became Liberalerna
# (2015), Kristen demokratisk samling became Kristdemokraterna (1996) and Vänsterpartiet kommunisterna
# became Vänsterpartiet (1990): the same parties, counted together (party_as_counted; used by
# analysis/rubric_coding_sheet.py). The page shows each motion's party under its name at the time.
PARTIES = {
    'S': ('S', 'Socialdemokraterna'),
    'M': ('M', 'Moderaterna'),
    'C': ('C', 'Centerpartiet'),
    'FP': ('L', 'Folkpartiet'),
    'L': ('L', 'Liberalerna'),
    'KDS': ('KD', 'Kristen demokratisk samling'),
    'KD': ('KD', 'Kristdemokraterna'),
    'VPK': ('V', 'Vänsterpartiet kommunisterna'),
    'V': ('V', 'Vänsterpartiet'),
    'MP': ('MP', 'Miljöpartiet'),
    'SD': ('SD', 'Sverigedemokraterna'),
    'NYD': ('NYD', 'Ny demokrati'),
}

def party_as_counted(code):
    """Party a code is counted as ('?' if not given); codes not in PARTIES count as themselves."""
    if code in ('', '-'):
        return '?'
    return PARTIES[code][0] if code in PARTIES else code


def party_name(code):
    """Name of the party at the time, for a motion; the code itself if not in PARTIES."""
    if code in ('', '-'):
        return 'party not given'
    return PARTIES[code][1] if code in PARTIES else code


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


def period_index(period):
    return PERIOD_KEYS.index(period)


def model_data(lda, vocab, theta, metadata, parties, marginal, stability=None):
    """Per-topic words, shares, top motions and seed stability (or None) for one model
    (marginal: P(word) in the corpus)."""
    periods = np.array([period_index(m['period']) for m in metadata])
    terms = np.array([term_of_session(m['session']) for m in metadata])
    topic_word = topic_word_distributions(lda)
    topics = []
    for k in range(lda.n_components):
        top_word_ids = relevant_words(topic_word[k], marginal, TOP_WORDS)
        top_doc_ids = np.argsort(theta[:, k])[::-1][:TOP_MOTIONS]
        motions = [{
            'id': metadata[d]['doc_id'],
            'title': metadata[d]['title'],
            'year': metadata[d]['year'],
            'session': metadata[d]['session'],
            'party': parties.get(metadata[d]['doc_id'], ''),
            'partyName': party_name(parties.get(metadata[d]['doc_id'], '')),
            'theta': round(float(theta[d, k]), 3),
        } for d in top_doc_ids]
        topics.append({
            'num': k + 1,
            'top3': most_probable_words(topic_word[k], vocab),
            'words': [[vocab[i], round(float(topic_word[k, i]), 5)] for i in top_word_ids],
            'share': round(float(theta[:, k].mean()), 5),
            'periods': [round(float(theta[periods == p, k].mean()), 5) for p in range(len(PERIOD_KEYS))],
            'terms': [round(float(theta[terms == s, k].mean()), 5) for s in TERM_STARTS],
            'motions': motions,
            'stability': stability[k] if stability else None,
        })
    return topics


def main():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
    BASELINE_DIR = PROJECT_ROOT / 'models' / BASELINE_MODEL_DIR
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
    doc_term = vectorizer.transform(texts)
    theta = lda.transform(doc_term)
    theta = theta / theta.sum(axis=1, keepdims=True)
    outside = [m['doc_id'] for m in metadata if term_of_session(m['session']) is None]
    if outside:
        raise ValueError(f"{len(outside)} motions without an electoral term, e.g. {outside[:3]}")
    stability = load_seed_stability(PROJECT_ROOT / 'results' / f'BASELINE_STABILITY_{NUM_TOPICS}TOPICS_PER_TOPIC.csv',
                                    topic_word_distributions(lda), vocab)
    print("Seed stability: " + ("shown" if stability else "not shown (missing or for another model; run 09_test_lda_stability.py)"))
    topic_list = model_data(lda, vocab, theta, metadata, parties, word_marginal(doc_term), stability)
    top3 = {(str(t['num']),): t.pop('top3') for t in topic_list}
    names = load_topic_names(PROJECT_ROOT / 'config' / f'topic_names_{NUM_TOPICS}.tsv', top3)
    for t in topic_list:
        t['name'] = names.get((str(t['num']),), '')
    print(f"Topic names: {len(names)} of {len(topic_list)}")
    data = {
        'periods': [period_display(p) for p in PERIOD_KEYS],
        'topicList': topic_list,
        'motions': len(texts),
        'periodCounts': [sum(1 for m in metadata if m['period'] == p) for p in PERIOD_KEYS],
        'terms': [term_name(s) for s in TERM_STARTS],
        'termCounts': [sum(1 for m in metadata if term_of_session(m['session']) == s) for s in TERM_STARTS],
    }

    data['topics'] = NUM_TOPICS
    data['relevanceLambda'] = RELEVANCE_LAMBDA

    html = TEMPLATE.read_text(encoding='utf-8')
    assert html.count('__TOPIC_DATA__') == 1, 'template must contain the data placeholder once'
    html = html.replace('__TOPIC_DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding='utf-8')
    print(f"✅ Topic explorer saved to: {OUTPUT} ({OUTPUT.stat().st_size / 1024:.0f} KB)")


if __name__ == '__main__':
    main()
