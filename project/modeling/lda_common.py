#!/usr/bin/env python3
"""
Shared LDA configuration and helpers.

Every script that fits an LDA model imports from here, so the fitted model and the stability
test cannot drift apart:
    modeling/07_fit_baseline_lda.py, analysis/09_test_lda_stability.py,
    modeling/14_generate_topic_explorer.py, modeling/15_fit_period_lda.py,
    analysis/16_seed_stability_periods.py

The model uses body text only. Titles are kept as a separate field (title_processed) in the
data for later use; title weighting was tested and dropped (2026-10-16, see docs/PIPELINE_DOCUMENTATION.md).
"""

import csv
import hashlib
import json
import pickle
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from periods import DISPLAY_NAMES, period_key, session_start_year  # noqa: E402

try:
    from sklearn.decomposition import LatentDirichletAllocation
    from sklearn.feature_extraction.text import CountVectorizer
except ImportError:
    print("Error: scikit-learn not installed. Install with: pip install scikit-learn")
    sys.exit(1)


# Number of topics in each period model, chosen with the seed-stability test per period
# (16_seed_stability_periods.py, 2026-10-17): 8 is the only tested count with at least half of the
# topics stable in every period (docs/PIPELINE_DOCUMENTATION.md, Design Decisions).
PERIOD_TOPICS = 8

# Number of topics in the whole-corpus model: 32 = 4 periods x 8, the same total capacity as the
# period models together (as Gordon's 60 = 4 x 15)
NUM_TOPICS = 32

# Directory of the whole-corpus model under models/ (model and its vectorizer)
BASELINE_MODEL_DIR = f'baseline_lda_{NUM_TOPICS}'

# Vocabulary rule of every model, as Gordon (2026, 3.3): words in at least 10 and at most 50% of the model's
# motions, with no cap on the vocabulary size. Each period model builds its vocabulary within its period, the
# whole-corpus model over all motions. Adjacent periods are compared over the words both vocabularies contain
# (topic_matching.match_and_evaluate with shared_vocabulary=True).
VECTORIZER_PARAMS = {
    'min_df': 10,
    'max_df': 0.5,
}

# Seed of the reported models
DEFAULT_SEED = 42

# Seeds compared in the stability tests (DEFAULT_SEED included, so the reported model is one of them)
STABILITY_SEEDS = [42, 123, 456, 789, 999]

# LDA settings shared by every model and stability test (n_components and random_state are passed separately).
# With learning_method='online' and evaluate_every=-1 (the default), sklearn does not test for convergence:
# every fit runs exactly max_iter passes over the data.
LDA_PARAMS = {
    'max_iter': 50,
    'learning_method': 'online',
    'n_jobs': 2,
    'verbose': 0,
}


def motion_metadata(motion, period):
    """Fields kept next to each document for the document-topic output."""
    return {
        'doc_id': motion.get('dok_id', 'unknown'),
        'title': motion.get('title', ''),
        'year': motion.get('date', '')[:4] if motion.get('date') else 'unknown',
        'session': motion.get('session', ''),
        'period': period,
    }


# Motions with fewer words than this in the final text are not modelled: almost all are short formal
# requests (hemställan) that refer to another motion, too short for a reliable topic mix, and since every
# motion counts equally in a topic's share they would add noise to the shares.
MIN_WORDS = 20


def is_modelled(text):
    """True if a final text is long enough to be modelled (at least MIN_WORDS words)."""
    return len((text or '').split()) >= MIN_WORDS


def text_key(text):
    """Duplicate key of a final text: MD5 of the text with whitespace collapsed."""
    return hashlib.md5(' '.join((text or '').split()).encode()).hexdigest()


# Near-duplicates: a motion whose final text shares at least this share of its three-word sequences
# (Jaccard of word 3-gram sets) with an earlier motion is a revised resubmission of it and is not modelled,
# as exact duplicates. Revisions below the threshold count as new motions.
NEAR_DUPLICATE_JACCARD = 0.6
SHINGLE_WORDS = 3


def near_duplicates(texts, sessions, threshold=None, chunk=400):
    """Indices of texts that are near-copies of an earlier text.

    A text is a near-copy if the Jaccard similarity of its set of SHINGLE_WORDS-word sequences with the
    set of any earlier text is at least threshold (default NEAR_DUPLICATE_JACCARD). Earlier means an
    earlier session, or the same session and earlier in the list. Compared with every earlier text, so
    each revision in a series of resubmissions is caught by its predecessor.
    """
    threshold = NEAR_DUPLICATE_JACCARD if threshold is None else threshold
    n = len(texts)
    if n < 2:
        return set()
    try:
        shingles = CountVectorizer(ngram_range=(SHINGLE_WORDS, SHINGLE_WORDS), binary=True,
                                   token_pattern=r'\S+').fit_transform(texts).astype(np.float32).tocsr()
    except ValueError:  # no text has SHINGLE_WORDS words
        return set()
    sizes = np.asarray(shingles.sum(axis=1)).ravel()
    years = np.array([session_start_year(s) or 0 for s in sessions])
    rank = np.empty(n, dtype=int)
    rank[np.lexsort((np.arange(n), years))] = np.arange(n)
    copies = set()
    for start in range(0, n, chunk):
        rows = np.arange(start, min(start + chunk, n))
        shared = (shingles[rows] @ shingles.T).toarray()
        union = sizes[rows, None] + sizes[None, :] - shared
        jaccard = np.divide(shared, union, out=np.zeros_like(shared), where=union > 0)
        jaccard[rank[None, :] >= rank[rows, None]] = 0  # only earlier texts count as originals
        copies.update(int(r) for r in rows[jaccard.max(axis=1) >= threshold])
    return copies


def read_bin_body_texts(bin_file, seen=None, skip_duplicates=True):
    """Load final body text (titles not added) from one temporal-bin file.

    Input field: text_no_stopwords (output of 05_remove_stopwords.py). Texts with fewer than MIN_WORDS
    words are skipped (is_modelled), among them any text with no words left. Duplicates are skipped:
    a text identical to one already in seen (text_key; shared across the period files, read in period
    order) is a later copy, mostly the same motion resubmitted in a later session; the first is kept.
    skip_duplicates=False keeps them (for the deduplication comparison).
    Returns: texts (list), metadata (list, same order), malformed_count (int)
    """
    if seen is None:
        seen = set()
    texts = []
    metadata = []
    malformed_count = 0
    period = period_label(bin_file)
    with open(bin_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                motion = json.loads(line.strip())
            except json.JSONDecodeError:
                malformed_count += 1
                continue
            text = motion.get('text_no_stopwords', '')
            if is_modelled(text):
                key = text_key(text)
                if skip_duplicates and key in seen:
                    continue
                seen.add(key)
                texts.append(text)
                metadata.append(motion_metadata(motion, period))
    return texts, metadata, malformed_count


def period_label(bin_file):
    """Period key of a period file: 'group2_1994-2006.jsonl' -> '1994-2006' (used in file and model names)."""
    return period_key(Path(bin_file).stem)


def period_display(period):
    """Name of a period on pages and in reports, by its sessions: '1985-1994' -> '1985/86–1993/94'."""
    return DISPLAY_NAMES.get(period, period)


# Duplicate filters, from none to the models' setting: 'none' (length minimum only), 'exact' (also identical
# texts), 'near' (also near-duplicates; the default, used by every model). The other two are for the
# deduplication comparison (analysis/dedup_comparison.py).
DEDUP_LEVELS = ('none', 'exact', 'near')


def load_body_texts(input_dir, dedup='near'):
    """Load final body text from all temporal bins combined, for the whole-corpus model.

    Selection: read_bin_body_texts (length minimum, exact duplicates), then near-duplicates of an earlier
    motion are dropped (near_duplicates). The period models use the same motions (load_period_body_texts).
    dedup: one of DEDUP_LEVELS; anything but the default only for the deduplication comparison.
    Returns: texts (list), metadata (list, same order), malformed_count (int)
    """
    if dedup not in DEDUP_LEVELS:
        raise ValueError(f"dedup must be one of {DEDUP_LEVELS}, not {dedup!r}")
    texts = []
    metadata = []
    malformed_count = 0
    seen = set()
    for bin_file in sorted(input_dir.glob('group*.jsonl')):
        bin_texts, bin_metadata, bin_malformed = read_bin_body_texts(bin_file, seen, skip_duplicates=dedup != 'none')
        texts += bin_texts
        metadata += bin_metadata
        malformed_count += bin_malformed
    if dedup != 'near':
        return texts, metadata, malformed_count
    copies = near_duplicates(texts, [m['session'] for m in metadata])
    keep = [i for i in range(len(texts)) if i not in copies]
    return [texts[i] for i in keep], [metadata[i] for i in keep], malformed_count


def load_period_body_texts(input_dir, dedup='near'):
    """Load final body text per period, for the period models: the motions of load_body_texts, split by period.

    Returns: {period label: (texts, metadata)} in period order, and the total malformed count.
    """
    texts, metadata, malformed_count = load_body_texts(input_dir, dedup)
    periods = {period_label(bin_file): ([], []) for bin_file in sorted(input_dir.glob('group*.jsonl'))}
    for text, meta in zip(texts, metadata):
        periods[meta['period']][0].append(text)
        periods[meta['period']][1].append(meta)
    return periods, malformed_count


def fit_period_vectorizer(texts):
    """The vocabulary of one period model, built on that period's motions only."""
    return CountVectorizer(**VECTORIZER_PARAMS).fit(texts)


def load_baseline_vectorizer(vectorizer_path):
    """Load the vectorizer saved by 07_fit_baseline_lda.py, or exit with a clear message if it is missing."""
    if not vectorizer_path.exists():
        print(f"Error: baseline vectorizer not found at {vectorizer_path}")
        print("Run modeling/07_fit_baseline_lda.py first.")
        sys.exit(1)
    with open(vectorizer_path, 'rb') as f:
        return pickle.load(f)


def new_lda_model(num_topics=NUM_TOPICS, random_state=DEFAULT_SEED, **overrides):
    """An unfitted LDA model with the shared settings; overrides only for checks of the settings themselves."""
    return LatentDirichletAllocation(n_components=num_topics, random_state=random_state, **{**LDA_PARAMS, **overrides})


def fit_lda_model(doc_term_matrix, num_topics=NUM_TOPICS, random_state=DEFAULT_SEED):
    """Fit an LDA model with the shared settings."""
    lda = new_lda_model(num_topics, random_state)
    lda.fit(doc_term_matrix)
    return lda


def load_topic_names(path, top_words):
    """Topic names from a tab-separated names file, for topics whose top three words still match.

    Each line: the key columns (topic number, or period and topic number), the topic's three most
    probable words, the name. top_words maps a key tuple of strings to the model's three words.
    Chain names use the same format with the chain number as key and its topic numbers as words.
    A name is an interpretation of one fitted model; after a refit the topics differ, so a name
    whose words no longer match is left out (with a warning) rather than shown on the wrong topic.
    Returns {key tuple: name}.
    """
    if not path.exists():
        print(f"Note: {path} not found; topics are shown without names.")
        return {}
    names = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        *key, words, name = line.split('\t')
        key = tuple(key)
        if top_words.get(key) == words:
            names[key] = name
        else:
            print(f"Warning: name '{name}' for {' '.join(key)} skipped: its words '{words}' "
                  f"do not match the model ('{top_words.get(key)}')")
    return names


# Words shown in the explorers are ranked by relevance (Sievert & Shirley 2014, LDAvis):
#   relevance(w, k) = λ log P(w | k) + (1 − λ) log(P(w | k) / P(w))
# λ = 1 is plain probability; lower λ favours words specific to the topic over words frequent
# everywhere (lärare, elev, högskola). 0.6 is the value Sievert & Shirley found best for interpretation.
# Only the display uses it: names are matched on the most probable words (most_probable_words).
RELEVANCE_LAMBDA = 0.6


def topic_word_distributions(lda):
    """P(word | topic) for every topic: the model's components normalized per row."""
    return lda.components_ / lda.components_.sum(axis=1, keepdims=True)


def word_marginal(doc_term_matrix):
    """P(word) in the corpus: each word's count over all words (over the model's vocabulary)."""
    counts = np.asarray(doc_term_matrix.sum(axis=0)).ravel().astype(float)
    return counts / counts.sum()


def relevant_words(topic_word, marginal, n, lam=None):
    """Indices of the n most relevant words of one topic (topic_word: its P(word | topic))."""
    lam = RELEVANCE_LAMBDA if lam is None else lam
    with np.errstate(divide='ignore'):
        relevance = lam * np.log(topic_word) + (1 - lam) * np.log(topic_word / marginal)
    relevance[marginal == 0] = -np.inf
    return np.argsort(relevance)[::-1][:n]


def most_probable_words(topic_word, vocab, n=3):
    """The n most probable words of one topic, space-separated: the key of the names files."""
    return ' '.join(vocab[i] for i in np.argsort(topic_word)[::-1][:n])


# Seed stability in the explorers: a topic is shown as high (found again in every other seed's model),
# medium (in all but one) or low. Read from the per-topic CSVs of the stability tests (09, 16); their
# reference model is fitted with the reported seed, so its topics are the reported model's, which is
# checked on each topic's most probable words.
STABILITY_CHECK_WORDS = 8   # the words written to the CSV (TABLE_WORDS in analysis/seed_stability.py)


def load_seed_stability(csv_path, topic_word, vocab):
    """{topic index: {'found', 'of'}} from a per-topic stability CSV, or None if it is missing or
    describes another model (topic count or most probable words differ, e.g. after a refit)."""
    if not csv_path.exists():
        return None
    with open(csv_path, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    if len(rows) != len(topic_word):
        return None
    stability = {}
    for k, row in enumerate(rows):
        if row['top_words'] != most_probable_words(topic_word[k], vocab, STABILITY_CHECK_WORDS):
            return None
        stability[k] = {'found': int(row['found']), 'of': int(row['compared'])}
    return stability
