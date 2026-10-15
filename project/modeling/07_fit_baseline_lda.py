#!/usr/bin/env python3
"""
Fit baseline LDA model with 44 topics (FIXED).
Input: Normalized motion text (all 4 temporal bins combined).
Output: 44-topic LDA model, vectorizer, perplexity score.

Note: 44 topics selected as providing good balance between vocabulary coverage
and interpretability (based on topic concentration testing, not semantic coherence).
This script fits ONLY 44 topics (no optimization). For temporal analysis,
separate models will be fit with 11 topics per temporal bin.
"""

import json
import csv
from pathlib import Path
import sys
import pickle

try:
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
except ImportError:
    print("Error: scikit-learn not installed. Install with: pip install scikit-learn")
    sys.exit(1)


def load_normalized_text(input_dir):
    """Load final preprocessed text (lemmatized) and metadata from all temporal bins.

    Input field: text_no_stopwords (output of complete preprocessing pipeline)

    Returns:
        texts: List of text strings
        metadata: List of dicts with doc_id, title, year (same order as texts)
    """
    print("Loading normalized text from all bins...")
    texts = []
    metadata = []
    total_motions = 0
    malformed_count = 0

    for bin_file in sorted(input_dir.glob('group*.jsonl')):
        print(f"  Loading {bin_file.name}...")
        with open(bin_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    motion = json.loads(line.strip())
                    text = motion.get('text_no_stopwords', '')
                    if text:
                        texts.append(text)
                        # Preserve metadata in same order
                        metadata.append({
                            'doc_id': motion.get('dok_id', 'unknown'),
                            'title': motion.get('title', ''),
                            'year': motion.get('date', '')[:4] if motion.get('date') else 'unknown'
                        })
                        total_motions += 1
                except json.JSONDecodeError:
                    malformed_count += 1
                    continue

    print(f"Loaded {total_motions} motions")
    if malformed_count > 0:
        print(f"⚠️  Warning: {malformed_count} malformed JSON lines skipped")
    return texts, metadata


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


def fit_lda_model(doc_term_matrix, num_topics, random_state=42):
    """Fit LDA model with given number of topics."""
    lda = LatentDirichletAllocation(
        n_components=num_topics,
        random_state=random_state,
        max_iter=50,  # Increased from 20 for better convergence on 13k+ documents
        learning_method='online',
        n_jobs=2,
        verbose=0,
    )
    lda.fit(doc_term_matrix)
    return lda


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
    # Default: data/output/deduplicated -> models/baseline_lda_44
    # (deduplicated contains all docs; is_duplicate flags indicate flagged duplicates, not removed)
    if len(sys.argv) >= 3:
        INPUT_DIR = Path(sys.argv[1])
        OUTPUT_DIR = Path(sys.argv[2])
    else:
        INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'deduplicated'
        OUTPUT_DIR = PROJECT_ROOT / 'models' / 'baseline_lda_44'

    # Create output directory (with parents in case path doesn't exist)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Fixed topic count (selected from topic concentration testing, not semantic coherence)
    NUM_TOPICS = 44

    print("=" * 60)
    print("Fitting Baseline LDA Model (44 topics)")
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    # Load normalized text and metadata
    texts, metadata = load_normalized_text(INPUT_DIR)

    if not texts:
        print("Error: No texts loaded")
        sys.exit(1)

    # Create vectorizer and corpus
    vectorizer, doc_term_matrix = create_vectorizer_and_corpus(texts)

    # Fit 44-topic LDA model
    print("\n" + "=" * 60)
    print(f"Fitting 44-topic LDA model...")
    print("=" * 60)

    print(f"\nFitting LDA with {NUM_TOPICS} topics...")
    lda = fit_lda_model(doc_term_matrix, NUM_TOPICS)

    print(f"Calculating perplexity...")
    perplexity_score = calculate_perplexity(lda, doc_term_matrix)

    print("\n" + "=" * 60)
    print(f"Model: {NUM_TOPICS} topics")
    print(f"Iterations: {lda.n_iter_} / 50 (max_iter)")
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

        # Create row with all 44 topic probabilities
        row = {
            'doc_id': metadata_item['doc_id'],
            'title': metadata_item['title'],
            'year': metadata_item['year'],
        }

        # Add all 44 topic probabilities
        for topic_idx in range(NUM_TOPICS):
            row[f'topic_{topic_idx + 1}_prob'] = f'{topic_probs[topic_idx]:.6f}'

        results.append(row)

    # Write to CSV
    results_file = SCRIPT_DIR.parent / 'results' / 'document_topic_distribution.csv'
    results_file.parent.mkdir(exist_ok=True, parents=True)

    with open(results_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['doc_id', 'title', 'year'] + [f'topic_{i+1}_prob' for i in range(NUM_TOPICS)]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"✅ Document-topic distribution saved to: {results_file}")
    print(f"   Format: doc_id | title | year | topic_1_prob | topic_2_prob | ... | topic_44_prob")

    print("\n" + "=" * 60)
    print("Baseline LDA fitting complete")
    print("=" * 60)


if __name__ == '__main__':
    main()
