#!/usr/bin/env python3
"""
Fit one LDA model per period (the four temporal bins), for cross-period topic alignment.

Vocabulary: option A of the seminar notes (PROGRESS_SEMINAR_1.md, 0.1/2.2): one global vocabulary,
the vectorizer saved by 07_fit_baseline_lda.py. Every period model therefore has the same columns in
the same order, so its topics can be compared directly with topic_matching.py. If option B (per-period
vocabularies compared over shared words, as Gordon) is chosen, only period_vectorizers() changes.

Input:  data/output/stopword_removed/ (body text, as the whole-corpus model), models/baseline_lda_44/baseline_vectorizer.pkl
Output: models/period_lda_<k>/period_<period>_lda.pkl (one per period), models/period_lda_<k>/vocabulary.txt,
        results/period_<k>_topics.csv (top 20 words per topic and period)

Usage: python modeling/15_fit_period_lda.py [num_topics]   (default: PERIOD_TOPICS in lda_common.py)
"""

import csv
import pickle
import sys
from pathlib import Path

import numpy as np

from lda_common import (
    DEFAULT_SEED, PERIOD_TOPICS, fit_lda_model, load_baseline_vectorizer, load_period_body_texts,
)

TOP_WORDS = 20


def period_vectorizers(periods, vectorizer):
    """Vectorizer per period. Option A: the same global vectorizer for every period."""
    return {period: vectorizer for period in periods}


def fit_period_models(periods, vectorizers, num_topics, seed=DEFAULT_SEED):
    """Fit one LDA model per period with the shared settings.

    periods: {period: (texts, metadata)}; vectorizers: {period: fitted vectorizer}
    Returns {period: (lda, vocabulary)} in period order.
    """
    models = {}
    for period, (texts, _) in periods.items():
        vectorizer = vectorizers[period]
        doc_term_matrix = vectorizer.transform(texts)
        print(f"   {period}: {len(texts)} motions...")
        lda = fit_lda_model(doc_term_matrix, num_topics, seed)
        print(f"      Training perplexity: {lda.perplexity(doc_term_matrix):.2f}")
        models[period] = (lda, vectorizer.get_feature_names_out())
    return models


def check_same_vocabulary(models):
    """Raise ValueError unless every period model has the same vocabulary in the same order (option A)."""
    vocabularies = [vocab for _, vocab in models.values()]
    for period, (lda, vocab) in models.items():
        if lda.components_.shape[1] != len(vocab):
            raise ValueError(f"{period}: model columns do not match its vocabulary")
        if not np.array_equal(vocab, vocabularies[0]):
            raise ValueError(f"{period}: vocabulary differs from {next(iter(models))}")


def save_top_words(models, num_topics, output_file):
    """Top words per topic and period, as P(word | topic)."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['period', 'topic'] + [f'word_{i + 1}' for i in range(TOP_WORDS)])
        for period, (lda, vocab) in models.items():
            topic_word = lda.components_ / lda.components_.sum(axis=1, keepdims=True)
            for k in range(num_topics):
                top = np.argsort(topic_word[k])[::-1][:TOP_WORDS]
                writer.writerow([period, k + 1] + [f"{vocab[i]} ({topic_word[k, i]:.4f})" for i in top])
    print(f"✅ Top words saved to: {output_file}")


def main():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
    VECTORIZER_PATH = PROJECT_ROOT / 'models' / 'baseline_lda_44' / 'baseline_vectorizer.pkl'
    num_topics = int(sys.argv[1]) if len(sys.argv) > 1 else PERIOD_TOPICS
    OUTPUT_DIR = PROJECT_ROOT / 'models' / f'period_lda_{num_topics}'

    print("=" * 60)
    print(f"Fitting period LDA models ({num_topics} topics per period, seed {DEFAULT_SEED})")
    print("=" * 60)

    periods, malformed = load_period_body_texts(INPUT_DIR)
    if malformed:
        print(f"⚠️  {malformed} malformed JSON lines skipped")
    if not periods or not all(texts for texts, _ in periods.values()):
        print(f"Error: no texts loaded for some period in {INPUT_DIR}")
        sys.exit(1)

    vectorizer = load_baseline_vectorizer(VECTORIZER_PATH)
    models = fit_period_models(periods, period_vectorizers(periods, vectorizer), num_topics)
    check_same_vocabulary(models)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for period, (lda, _) in models.items():
        with open(OUTPUT_DIR / f'period_{period}_lda.pkl', 'wb') as f:
            pickle.dump(lda, f)
    vocab = next(iter(models.values()))[1]
    (OUTPUT_DIR / 'vocabulary.txt').write_text('\n'.join(vocab) + '\n', encoding='utf-8')
    print(f"✅ {len(models)} period models and the shared vocabulary saved to: {OUTPUT_DIR}")

    save_top_words(models, num_topics, PROJECT_ROOT / 'results' / f'period_{num_topics}_topics.csv')


if __name__ == '__main__':
    main()
