#!/usr/bin/env python3
"""
Corpus size at each step of the pipeline: number of words (tokens) and number of different words (types)
in the body text of all motions. For the report; read-only, writes nothing.

Words are Stanza's tokens throughout, so that every step is counted the same way: step 02 runs Stanza on
the extracted text, so its word forms are the extracted text as Stanza splits it, and its lemmas are the
same tokens after lemmatization. A word is a token with at least one letter (punctuation and pure numbers
are not words); different words are counted case-insensitively.

    Extraction (01)      tokens, word forms     the extracted running text ('text'), split into tokens by Stanza
    Lemmatization (02)   tokens, lemmas         one lemma per word form, so the same number of words
    Boilerplate (03)     text_no_boilerplate    lemmas left after boilerplate, auxiliaries, punctuation
    Normalization (04)   text_normalized        lowercase, no digits or punctuation, no single characters
    Stopwords (05)       text_no_stopwords      final text
    Model vocabulary     the words of the final text that are in the models' vocabularies
                         (whole-corpus vectorizer; each period's own vectorizer)

Usage: python analysis/corpus_statistics.py
"""

import json
import pickle
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from periods import PERIOD_FILES, PERIODS, period_key  # noqa: E402

sys.path.insert(0, str(PROJECT_ROOT / 'modeling'))
from lda_common import BASELINE_MODEL_DIR, PERIOD_TOPICS, is_modelled  # noqa: E402

HAS_LETTER = re.compile(r'[^\W\d_]')

# Step label, stage directory under data/, field, how to get the words of a motion
LEMMA_STEPS = [
    ('03 Boilerplate removed (lemmas)', 'output/boilerplate_removed', 'text_no_boilerplate'),
    ('04 Normalized', 'output/normalized', 'text_normalized'),
    ('05 Stopwords removed (final text)', 'output/stopword_removed', 'text_no_stopwords'),
]


def is_word(token):
    return bool(HAS_LETTER.search(token))


def stanza_words(tokens):
    """(word forms, lemmas) of Stanza's tokens (steps 01 and 02): every token whose word form is a word, and its lemma.

    The lemma is counted even if it has no letter (Stanza lemmatizes the ordinal '6:e' to '6:'), so that
    word forms and lemmas are the same tokens and have the same count.
    """
    words = [t for sentence in tokens or [] for t in sentence if is_word(t[0])]
    return [t[0] for t in words], [t[1] for t in words]


def lemma_text_words(text):
    """Words of a space-separated lemma text (steps 03-05)."""
    return [w for w in (text or '').split() if is_word(w)]


def read_stage(stage_dir):
    """Yield (period file, motion) for every motion of a stage, in period order."""
    for name in PERIOD_FILES:
        with open(stage_dir / name, encoding='utf-8') as f:
            for line in f:
                yield name, json.loads(line)


class Count:
    """Words, different words (case-insensitive) and words per motion for one step."""

    def __init__(self):
        self.types = Counter()
        self.per_motion = []

    def add(self, words):
        self.types.update(w.lower() for w in words)
        self.per_motion.append(len(words))

    def row(self, label):
        tokens = sum(self.per_motion)
        return {'step': label, 'words': tokens, 'different': len(self.types),
                'median': statistics.median(self.per_motion), 'mean': tokens / len(self.per_motion)}


def step_counts(data_dir):
    """One row per step 01-05: words, different words, median and mean words per motion."""
    forms, lemmas = Count(), Count()
    for _, m in read_stage(data_dir / 'output' / 'lemmatized'):
        motion_forms, motion_lemmas = stanza_words(m.get('tokens'))
        forms.add(motion_forms)
        lemmas.add(motion_lemmas)

    rows = [forms.row('01 Extraction (Stanza tokens, word forms)'), lemmas.row('02 Lemmatization (lemmas)')]
    for label, stage, field in LEMMA_STEPS:
        count = Count()
        for _, m in read_stage(data_dir / stage):
            count.add(lemma_text_words(m.get(field)))
        rows.append(count.row(label))
    return rows


def vocabulary_counts(final_texts, whole_vectorizer, period_vectorizers):
    """Words of the final text inside the models' vocabularies.

    final_texts: {period file: [text, ...]} (the motions the models use); period_vectorizers: {period file: vectorizer}.
    Returns (whole-corpus row, period-models row, [(period file, motions, words, vocabulary size)]).
    """
    texts = [t for name in final_texts for t in final_texts[name]]
    counts = whole_vectorizer.transform(texts).sum(axis=1).A1
    whole = {'step': 'Whole-corpus model vocabulary', 'words': int(counts.sum()),
             'different': len(whole_vectorizer.vocabulary_), 'median': statistics.median(counts),
             'mean': float(counts.mean())}
    per_period, types = [], set()
    for name, vectorizer in period_vectorizers.items():
        n = int(vectorizer.transform(final_texts[name]).sum())
        per_period.append((name, len(final_texts[name]), n, len(vectorizer.vocabulary_)))
        types |= set(vectorizer.vocabulary_)
    periods = {'step': "Period models' vocabularies (together)", 'words': sum(p[2] for p in per_period),
               'different': len(types), 'median': None, 'mean': None}
    return whole, periods, per_period


def main():
    data_dir = PROJECT_ROOT / 'data'
    rows = step_counts(data_dir)

    # The motions the models use: final text with at least MIN_WORDS words (lda_common.is_modelled)
    final_texts = {name: [] for name in PERIOD_FILES}
    for name, m in read_stage(data_dir / 'output' / 'stopword_removed'):
        text = m.get('text_no_stopwords') or ''
        if is_modelled(text):
            final_texts[name].append(text)
    with open(PROJECT_ROOT / 'models' / BASELINE_MODEL_DIR / 'baseline_vectorizer.pkl', 'rb') as f:
        whole_vectorizer = pickle.load(f)
    period_vectorizers = {}
    for (stem, _, _), name in zip(PERIODS, PERIOD_FILES):
        with open(PROJECT_ROOT / 'models' / f'period_lda_{PERIOD_TOPICS}' / f'period_{period_key(stem)}_vectorizer.pkl', 'rb') as f:
            period_vectorizers[name] = pickle.load(f)
    whole, periods, per_period = vocabulary_counts(final_texts, whole_vectorizer, period_vectorizers)
    rows += [whole, periods]

    print(f"{'Step':42} {'Words':>12} {'Different':>10} {'Median/motion':>14} {'Mean/motion':>12}")
    for r in rows:
        med = f"{r['median']:,.0f}" if r['median'] is not None else '–'
        avg = f"{r['mean']:,.0f}" if r['mean'] is not None else '–'
        print(f"{r['step']:42} {r['words']:>12,} {r['different']:>10,} {med:>14} {avg:>12}")
    print()
    print(f"{'Period':24} {'Motions':>8} {'Words in its vocabulary':>24} {'Vocabulary':>11}")
    for name, motions, words, types in per_period:
        print(f"{name:24} {motions:>8,} {words:>24,} {types:>11,}")


if __name__ == '__main__':
    main()
