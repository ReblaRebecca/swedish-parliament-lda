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

import json
import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from periods import DISPLAY_NAMES  # noqa: E402

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

# Vocabulary of each period model, as Gordon (2026, 3.3): built within the period, keeping words in at least
# 10 and at most 50% of the period's motions, with no cap on its size. Adjacent periods are compared over the
# words both vocabularies contain (topic_matching.match_and_evaluate with shared_vocabulary=True).
PERIOD_VECTORIZER_PARAMS = {
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


def read_bin_body_texts(bin_file):
    """Load final body text (titles not added) from one temporal-bin file.

    Input field: text_no_stopwords (output of 05_remove_stopwords.py). Texts with no words are skipped
    (e.g. withdrawn motions titled 'Utgår', whose body is only a line break after preprocessing).
    Returns: texts (list), metadata (list, same order), malformed_count (int)
    """
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
            # strip(): a text with no words left can still hold line breaks
            if text.strip():
                texts.append(text)
                metadata.append(motion_metadata(motion, period))
    return texts, metadata, malformed_count


def period_label(bin_file):
    """Period key of a period file: 'group2_1994-2006.jsonl' -> '1994-2006' (used in file and model names)."""
    return Path(bin_file).stem.split('_', 1)[-1]


def period_display(period):
    """Name of a period on pages and in reports, by its sessions: '1985-1994' -> '1985/86–1993/94'."""
    return DISPLAY_NAMES.get(period, period)


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


def fit_period_vectorizer(texts):
    """The vocabulary of one period model, built on that period's motions only."""
    return CountVectorizer(**PERIOD_VECTORIZER_PARAMS).fit(texts)


def load_baseline_vectorizer(vectorizer_path):
    """Load the vectorizer saved by 07_fit_baseline_lda.py, or exit with a clear message if it is missing."""
    if not vectorizer_path.exists():
        print(f"Error: baseline vectorizer not found at {vectorizer_path}")
        print("Run modeling/07_fit_baseline_lda.py first.")
        sys.exit(1)
    with open(vectorizer_path, 'rb') as f:
        return pickle.load(f)


def fit_lda_model(doc_term_matrix, num_topics=NUM_TOPICS, random_state=DEFAULT_SEED):
    """Fit an LDA model with the shared settings."""
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=random_state, **LDA_PARAMS)
    lda.fit(doc_term_matrix)
    return lda
