#!/usr/bin/env python3
"""
Fit one LDA model per period (the four temporal bins), for cross-period topic alignment.

Vocabulary: one per period, as Gordon (2026, 3.3): built on the period's motions only, keeping words in at
least 10 and at most 50% of them (VECTORIZER_PARAMS in lda_common.py). Each period model is therefore
built on its own most relevant words; adjacent periods are compared over the words both vocabularies contain
(topic_matching.match_and_evaluate with shared_vocabulary=True).

Input:  data/output/stopword_removed/ (body text, the same motions as the whole-corpus model)
Output: models/period_lda_<k>/period_<period>_lda.pkl and period_<period>_vectorizer.pkl (one each per period),
        models/period_lda_<k>/vocabulary_<period>.txt, results/period_<k>_topics.csv (top 20 words per topic and period)

Usage: python modeling/15_fit_period_lda.py [num_topics]   (default: PERIOD_TOPICS in lda_common.py)
"""

import csv
import pickle
import sys
from pathlib import Path

import numpy as np

from lda_common import (
    DEFAULT_SEED, PERIOD_TOPICS, fit_lda_model, fit_period_vectorizer, load_period_body_texts,
)

TOP_WORDS = 20


def period_vectorizers(periods):
    """Vectorizer per period, each fitted on that period's motions only."""
    return {period: fit_period_vectorizer(texts) for period, (texts, _) in periods.items()}


def fit_period_models(periods, vectorizers, num_topics, seed=DEFAULT_SEED):
    """Fit one LDA model per period with the shared settings.

    periods: {period: (texts, metadata)}; vectorizers: {period: fitted vectorizer}
    Returns {period: (lda, vocabulary)} in period order.
    """
    models = {}
    for period, (texts, _) in periods.items():
        vectorizer = vectorizers[period]
        doc_term_matrix = vectorizer.transform(texts)
        print(f"   {period}: {len(texts)} motions, {len(vectorizer.vocabulary_)} words in its vocabulary...")
        lda = fit_lda_model(doc_term_matrix, num_topics, seed)
        print(f"      Training perplexity: {lda.perplexity(doc_term_matrix):.2f}")
        models[period] = (lda, vectorizer.get_feature_names_out())
    return models


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

    vectorizers = period_vectorizers(periods)
    models = fit_period_models(periods, vectorizers, num_topics)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for period, (lda, vocab) in models.items():
        with open(OUTPUT_DIR / f'period_{period}_lda.pkl', 'wb') as f:
            pickle.dump(lda, f)
        with open(OUTPUT_DIR / f'period_{period}_vectorizer.pkl', 'wb') as f:
            pickle.dump(vectorizers[period], f)
        (OUTPUT_DIR / f'vocabulary_{period}.txt').write_text('\n'.join(vocab) + '\n', encoding='utf-8')
    print(f"✅ {len(models)} period models and their vocabularies saved to: {OUTPUT_DIR}")

    save_top_words(models, num_topics, PROJECT_ROOT / 'results' / f'period_{num_topics}_topics.csv')


if __name__ == '__main__':
    main()
