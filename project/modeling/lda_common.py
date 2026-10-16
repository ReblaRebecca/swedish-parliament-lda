#!/usr/bin/env python3
"""
Shared LDA configuration and helpers.

Every script that fits an LDA model imports from here, so the fitted model and the stability
test cannot drift apart:
    modeling/07_fit_baseline_lda.py, analysis/09_test_lda_stability.py,
    modeling/14_generate_topic_explorer.py, modeling/15_fit_period_lda.py,
    analysis/16_seed_stability_periods.py

The model uses body text only. Titles are kept as a separate field (title_processed) in the
data for later use; title weighting was tested and dropped (2026-10-16, see PIPELINE_DOCUMENTATION.md).
"""

import json
import pickle
import sys
from pathlib import Path

try:
    from sklearn.decomposition import LatentDirichletAllocation
except ImportError:
    print("Error: scikit-learn not installed. Install with: pip install scikit-learn")
    sys.exit(1)


# Number of topics in the whole-corpus models
NUM_TOPICS = 44

# Number of topics in each period model (44 = 4 periods x 11, as Gordon's 60 = 4 x 15).
# Provisional: to be chosen with the seed-stability test per period (16_seed_stability_periods.py).
PERIOD_TOPICS = 11

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


def motion_metadata(motion):
    """Fields kept next to each document for the document-topic output."""
    return {
        'doc_id': motion.get('dok_id', 'unknown'),
        'title': motion.get('title', ''),
        'year': motion.get('date', '')[:4] if motion.get('date') else 'unknown',
    }


def read_bin_body_texts(bin_file):
    """Load final body text (titles not added) from one temporal-bin file.

    Input field: text_no_stopwords (output of 05_remove_stopwords.py). Texts with no words are skipped
    (e.g. withdrawn motions titled 'Utgår', whose body is only a line break after preprocessing).
    Returns: texts (list), metadata (list, same order), malformed_count (int)
    """
    texts = []
    metadata = []
    malformed_count = 0
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


def period_label(bin_file):
    """Period of a temporal-bin file: 'group2_1994-2004.jsonl' -> '1994-2004'."""
    return Path(bin_file).stem.split('_', 1)[-1]


def load_body_texts(input_dir):
    """Load final body text from all temporal bins combined, for the whole-corpus model.

    Same selection rule as the period models (read_bin_body_texts), so both use the same motions.
    Returns: texts (list), metadata (list, same order), malformed_count (int)
    """
    texts = []
    metadata = []
    malformed_count = 0
    for bin_file in sorted(input_dir.glob('group*.jsonl')):
        bin_texts, bin_metadata, bin_malformed = read_bin_body_texts(bin_file)
        texts += bin_texts
        metadata += bin_metadata
        malformed_count += bin_malformed
    return texts, metadata, malformed_count


def load_period_body_texts(input_dir):
    """Load final body text per period, for the period models.

    Returns: {period label: (texts, metadata)} in period order, and the total malformed count.
    """
    periods = {}
    malformed_count = 0
    for bin_file in sorted(input_dir.glob('group*.jsonl')):
        texts, metadata, malformed = read_bin_body_texts(bin_file)
        periods[period_label(bin_file)] = (texts, metadata)
        malformed_count += malformed
    return periods, malformed_count


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
