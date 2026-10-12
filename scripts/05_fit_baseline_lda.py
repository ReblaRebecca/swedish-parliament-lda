#!/usr/bin/env python3
"""
Fit baseline LDA model on full corpus and optimize number of topics.
Tests 6, 10, 14, 18, 22 topics and picks best by perplexity score.
Input: Normalized motion text (all 4 temporal bins combined).
Output: Best LDA model, vectorizer, perplexity scores.
"""

import json
from pathlib import Path
import sys
import pickle

try:
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    import numpy as np
except ImportError:
    print("Error: scikit-learn not installed. Install with: pip install scikit-learn")
    sys.exit(1)


def load_normalized_text(input_dir):
    """Load normalized text from all temporal bins."""
    print("Loading normalized text from all bins...")
    texts = []
    total_motions = 0

    for bin_file in sorted(input_dir.glob('group*.jsonl')):
        print(f"  Loading {bin_file.name}...")
        with open(bin_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    motion = json.loads(line.strip())
                    text = motion.get('text_normalized', '')
                    if text:
                        texts.append(text)
                        total_motions += 1
                except json.JSONDecodeError:
                    continue

    print(f"Loaded {total_motions} motions")
    return texts


def create_vectorizer_and_corpus(texts):
    """Create CountVectorizer and transform texts."""
    print("Creating document-term matrix...")

    # Create vectorizer
    vectorizer = CountVectorizer(
        max_df=0.5,      # Remove words in > 50% of docs
        min_df=5,        # Remove words in < 5 docs
        max_features=5000,
        stop_words=None,  # Already removed in preprocessing
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
        max_iter=20,
        learning_method='online',
        n_jobs=2,
        verbose=0,
    )
    lda.fit(doc_term_matrix)
    return lda


def calculate_perplexity(lda, doc_term_matrix):
    """Calculate perplexity score (lower is better)."""
    perplexity = lda.perplexity(doc_term_matrix)
    return perplexity


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent

    # Allow command-line arguments for input/output directories
    # Usage: python3 05_fit_baseline_lda.py [input_dir] [output_dir]
    # Default: normalized -> baseline_lda (backward compatible)
    if len(sys.argv) >= 3:
        INPUT_DIR = Path(sys.argv[1])
        OUTPUT_DIR = Path(sys.argv[2])
    else:
        INPUT_DIR = SCRIPT_DIR / 'normalized'
        OUTPUT_DIR = SCRIPT_DIR / 'baseline_lda'

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Topic counts to test
    TOPIC_COUNTS = [6, 10, 14, 18, 22]

    print("=" * 60)
    print("Fitting Baseline LDA Model (scikit-learn)")
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    # Load normalized text
    texts = load_normalized_text(INPUT_DIR)

    if not texts:
        print("Error: No texts loaded")
        sys.exit(1)

    # Create vectorizer and corpus
    vectorizer, doc_term_matrix = create_vectorizer_and_corpus(texts)

    # Test different topic counts
    print("\n" + "=" * 60)
    print(f"Testing topic counts: {TOPIC_COUNTS}")
    print("=" * 60)

    results = []
    best_score = float('inf')  # Lower perplexity is better
    best_model_info = None

    for num_topics in TOPIC_COUNTS:
        print(f"\nFitting LDA with {num_topics} topics...")
        lda = fit_lda_model(doc_term_matrix, num_topics)

        print(f"  Calculating perplexity...")
        perplexity_score = calculate_perplexity(lda, doc_term_matrix)

        print(f"  Perplexity: {perplexity_score:.4f}")

        results.append({
            'num_topics': num_topics,
            'perplexity': float(perplexity_score)
        })

        if perplexity_score < best_score:
            best_score = perplexity_score
            best_model_info = {
                'num_topics': num_topics,
                'perplexity': perplexity_score,
                'model': lda
            }

    # Display results
    print("\n" + "=" * 60)
    print("Results Summary")
    print("=" * 60)
    for result in results:
        marker = " <-- BEST" if result['num_topics'] == best_model_info['num_topics'] else ""
        print(f"Topics: {result['num_topics']:2d}  |  Perplexity: {result['perplexity']:8.4f}{marker}")

    # Save best model
    print("\n" + "=" * 60)
    print(f"Best model: {best_model_info['num_topics']} topics")
    print(f"Perplexity score: {best_model_info['perplexity']:.4f}")
    print("=" * 60)

    model_path = OUTPUT_DIR / f"baseline_lda_{best_model_info['num_topics']}_topics.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(best_model_info['model'], f)
    print(f"Model saved to: {model_path}")

    # Save vectorizer
    vectorizer_path = OUTPUT_DIR / "baseline_vectorizer.pkl"
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"Vectorizer saved to: {vectorizer_path}")

    # Save results to JSON
    results_file = OUTPUT_DIR / "baseline_perplexity_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            'results': results,
            'best_model': {
                'num_topics': best_model_info['num_topics'],
                'perplexity': float(best_model_info['perplexity'])
            }
        }, f, indent=2)
    print(f"Results saved to: {results_file}")

    print("\n" + "=" * 60)
    print("Baseline LDA fitting complete")
    print("=" * 60)


if __name__ == '__main__':
    main()
