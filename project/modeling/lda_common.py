#!/usr/bin/env python3
"""
Shared LDA configuration and helpers.

Every script that fits an LDA model or builds title-weighted documents imports from here,
so the fitted models and the stability tests cannot drift apart:
    modeling/07_fit_baseline_lda.py, modeling/10_fit_title_weighted_lda.py,
    modeling/06_build_shared_vocabulary_and_fit_models.py,
    analysis/09_test_lda_stability.py, analysis/13_seed_stability_{3x,5x}_weighted.py
"""

import json
import pickle
import sys

try:
    from sklearn.decomposition import LatentDirichletAllocation
except ImportError:
    print("Error: scikit-learn not installed. Install with: pip install scikit-learn")
    sys.exit(1)


# Number of topics in the whole-corpus models
NUM_TOPICS = 44

# Title words are appended this many times to the body text in the weighted model.
# The title heading is removed from the body at extraction, so the title counts exactly this many times.
TITLE_WEIGHT = 5

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


def weight_document(text, title, title_weight=TITLE_WEIGHT):
    """Body text followed by the title words title_weight times (body only if the title is empty)."""
    if title and title.strip():
        return text + ' ' + (' '.join(title.split()) + ' ') * title_weight
    return text


def motion_metadata(motion):
    """Fields kept next to each document for the document-topic output."""
    return {
        'doc_id': motion.get('dok_id', 'unknown'),
        'title': motion.get('title', ''),
        'year': motion.get('date', '')[:4] if motion.get('date') else 'unknown',
    }


def load_body_texts(input_dir):
    """Load final body text (no title weighting) from all temporal bins, for the baseline model.

    Input field: text_no_stopwords (output of 05_remove_stopwords.py). Texts with no words are skipped
    (e.g. withdrawn motions titled 'Utgår', whose body is only a line break after preprocessing).
    Returns: texts (list), metadata (list, same order), malformed_count (int)
    """
    texts = []
    metadata = []
    malformed_count = 0

    for bin_file in sorted(input_dir.glob('group*.jsonl')):
        with open(bin_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    motion = json.loads(line.strip())
                except json.JSONDecodeError:
                    malformed_count += 1
                    continue
                text = motion.get('text_no_stopwords', '')
                # strip(): a text with no words left can still hold line breaks
                if text.strip():
                    texts.append(text)
                    metadata.append(motion_metadata(motion))

    return texts, metadata, malformed_count


def load_weighted_texts(input_dir, title_weight=TITLE_WEIGHT):
    """Load final text and titles from all temporal bins and build title-weighted documents.

    Input fields: text_no_stopwords, title_processed (output of 05_remove_stopwords.py).
    Motions with empty body text are skipped, as in load_body_texts, so the baseline and the
    weighted model are fitted on exactly the same motions.
    Returns: texts (list), metadata (list, same order), title_stats (dict; 'total', 'weighted'
             and 'empty' count the kept motions, 'empty_body' the skipped ones)
    """
    texts = []
    metadata = []
    title_stats = {'empty': 0, 'weighted': 0, 'total': 0, 'empty_body': 0, 'malformed': 0}

    for bin_file in sorted(input_dir.glob('group*.jsonl')):
        with open(bin_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    motion = json.loads(line.strip())
                except json.JSONDecodeError:
                    title_stats['malformed'] += 1
                    continue

                text = motion.get('text_no_stopwords', '')
                title = motion.get('title_processed', '')
                # Same rule as load_body_texts: a motion without body text is not used
                if not text.strip():
                    title_stats['empty_body'] += 1
                    continue

                title_stats['total'] += 1
                if title and title.strip():
                    title_stats['weighted'] += 1
                else:
                    title_stats['empty'] += 1

                texts.append(weight_document(text, title, title_weight))
                metadata.append(motion_metadata(motion))

    return texts, metadata, title_stats


def load_baseline_vectorizer(vectorizer_path):
    """Load the vectorizer saved by 07_fit_baseline_lda.py, or exit with a clear message if it is missing."""
    if not vectorizer_path.exists():
        print(f"Error: baseline vectorizer not found at {vectorizer_path}")
        print("Run modeling/07_fit_baseline_lda.py first: every model shares its vocabulary.")
        sys.exit(1)
    with open(vectorizer_path, 'rb') as f:
        return pickle.load(f)


def fit_lda_model(doc_term_matrix, num_topics=NUM_TOPICS, random_state=DEFAULT_SEED):
    """Fit an LDA model with the shared settings."""
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=random_state, **LDA_PARAMS)
    lda.fit(doc_term_matrix)
    return lda
