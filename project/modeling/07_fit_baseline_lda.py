#!/usr/bin/env python3
"""
Fit the whole-corpus (baseline) LDA model with NUM_TOPICS topics (lda_common.py).
Input: Final preprocessed text (text_no_stopwords, all 4 temporal bins combined).
Output: LDA model, vectorizer (the global vocabulary, also used by the period models), perplexity score.

The topic count is 4 x PERIOD_TOPICS, so the whole-corpus model has the same total capacity as the
four period models together (as Gordon et al.); see docs/PIPELINE_DOCUMENTATION.md.
"""

import csv
from pathlib import Path
import sys
import pickle

try:
    from sklearn.feature_extraction.text import CountVectorizer
except ImportError:
    print("Error: scikit-learn not installed. Install with: pip install scikit-learn")
    sys.exit(1)

# Shared LDA settings and text loading (also used by the stability test)
from lda_common import BASELINE_MODEL_DIR, LDA_PARAMS, NUM_TOPICS, fit_lda_model, load_body_texts


def create_vectorizer_and_corpus(texts):
    """Create CountVectorizer and transform texts."""
    print("Creating document-term matrix...")

    # Create vectorizer
    vectorizer = CountVectorizer(
        max_df=0.5,        # Remove words in > 50% of docs
        min_df=5,          # Remove words in < 5 docs
        max_features=10000,  # Keep top 10,000 features (vocabulary truncation)
        stop_words=None,   # Already removed in preprocessing
    )

    # Transform texts
    doc_term_matrix = vectorizer.fit_transform(texts)

    print(f"Vocabulary size: {len(vectorizer.get_feature_names_out())} unique tokens")
    print(f"Document-term matrix shape: {doc_term_matrix.shape}")

    return vectorizer, doc_term_matrix


def calculate_perplexity(lda, doc_term_matrix):
    """Calculate training perplexity (diagnostic only, not evidence of generalization).

    Note: Perplexity computed on same data used to fit model.
    Training perplexity is optimistically biased and does NOT indicate generalization.
    """
    perplexity = lda.perplexity(doc_term_matrix)
    return perplexity


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    # Allow command-line arguments for input/output directories
    # Usage: python3 07_fit_baseline_lda.py [input_dir] [output_dir]
    # Default: data/output/stopword_removed -> models/<BASELINE_MODEL_DIR>
    if len(sys.argv) >= 3:
        INPUT_DIR = Path(sys.argv[1])
        OUTPUT_DIR = Path(sys.argv[2])
    else:
        INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
        OUTPUT_DIR = PROJECT_ROOT / 'models' / BASELINE_MODEL_DIR

    # Create output directory (with parents in case path doesn't exist)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print(f"Fitting Baseline LDA Model ({NUM_TOPICS} topics)")
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    # Load normalized text and metadata
    print("Loading final text from all bins...")
    texts, metadata, malformed = load_body_texts(INPUT_DIR)
    print(f"Loaded {len(texts)} motions")
    if malformed:
        print(f"⚠️  Warning: {malformed} malformed JSON lines skipped")

    if not texts:
        print("Error: No texts loaded")
        sys.exit(1)

    # Create vectorizer and corpus
    vectorizer, doc_term_matrix = create_vectorizer_and_corpus(texts)

    # Fit the LDA model
    print("\n" + "=" * 60)
    print(f"Fitting LDA with {NUM_TOPICS} topics...")
    print("=" * 60)

    lda = fit_lda_model(doc_term_matrix, NUM_TOPICS)

    print(f"Calculating perplexity...")
    perplexity_score = calculate_perplexity(lda, doc_term_matrix)

    print("\n" + "=" * 60)
    print(f"Model: {NUM_TOPICS} topics")
    print(f"Iterations: {lda.n_iter_} / {LDA_PARAMS['max_iter']} (max_iter)")
    print(f"Training Perplexity: {perplexity_score:.4f}")
    print("(Note: Training perplexity is diagnostic only, not evidence of generalization)")
    print("=" * 60)

    # Save model
    model_path = OUTPUT_DIR / f"baseline_lda_{NUM_TOPICS}_topics.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(lda, f)
    print(f"\n✅ Model saved to: {model_path}")

    # Save vectorizer
    vectorizer_path = OUTPUT_DIR / "baseline_vectorizer.pkl"
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"✅ Vectorizer saved to: {vectorizer_path}")

    # Infer document-topic distributions for each document
    print("\nInferring document-topic distributions...")
    doc_topics = lda.transform(doc_term_matrix)  # Shape: (n_docs, n_topics)

    # Create document-topic mapping with all probabilities
    results = []
    for doc_idx, (metadata_item, topic_dist) in enumerate(zip(metadata, doc_topics)):
        # Normalize probabilities (should sum to 1)
        topic_probs = topic_dist / topic_dist.sum()

        # Create row with all topic probabilities
        row = {
            'doc_id': metadata_item['doc_id'],
            'title': metadata_item['title'],
            'year': metadata_item['year'],
            'session': metadata_item['session'],
            'period': metadata_item['period'],
        }

        # Add all topic probabilities
        for topic_idx in range(NUM_TOPICS):
            row[f'topic_{topic_idx + 1}_prob'] = f'{topic_probs[topic_idx]:.6f}'

        results.append(row)

    # Write to CSV
    results_file = SCRIPT_DIR.parent / 'results' / 'document_topic_distribution.csv'
    results_file.parent.mkdir(exist_ok=True, parents=True)

    with open(results_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['doc_id', 'title', 'year', 'session', 'period'] + [f'topic_{i+1}_prob' for i in range(NUM_TOPICS)]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"✅ Document-topic distribution saved to: {results_file}")
    print(f"   Format: doc_id | title | year | session | period | topic_1_prob | topic_2_prob | ... | topic_{NUM_TOPICS}_prob")

    print("\n" + "=" * 60)
    print("Baseline LDA fitting complete")
    print("=" * 60)


if __name__ == '__main__':
    main()
