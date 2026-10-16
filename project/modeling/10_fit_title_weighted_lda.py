#!/usr/bin/env python3
"""
Fit title-weighted LDA model for comparison with baseline.
Strategy: Append processed title words TITLE_WEIGHT (5) times to body text (modeling/lda_common.py).
The title heading is removed from the body at extraction, so title words count exactly 5x
(plus any genuine mentions in the body text).
This weights document-topic inference toward title content without changing vocabulary.

Input: Preprocessed motions (stopword_removed) with text_no_stopwords and title_processed fields
Output: Title-weighted LDA model, document-topic distribution, title weighting statistics
(the baseline vectorizer is reused, so both models share one vocabulary)
Configuration: 44 topics, same settings as baseline for fair comparison
"""

import csv
from pathlib import Path
import pickle
import sys

# Shared LDA settings, title weighting and text loading (also used by the stability tests)
from lda_common import (
    LDA_PARAMS, NUM_TOPICS, TITLE_WEIGHT, fit_lda_model, load_baseline_vectorizer, load_weighted_texts,
)


def transform_weighted_texts(texts, vectorizer):
    """Transform weighted texts using baseline vectorizer."""
    print("Transforming weighted documents with baseline vectorizer...")
    doc_term_matrix = vectorizer.transform(texts)
    print(f"Document-term matrix shape: {doc_term_matrix.shape}")
    return doc_term_matrix


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
    BASELINE_VECTORIZER_PATH = PROJECT_ROOT / 'models' / 'baseline_lda_44' / 'baseline_vectorizer.pkl'
    OUTPUT_DIR = PROJECT_ROOT / 'models' / 'title_weighted_lda_44'
    RESULTS_DIR = PROJECT_ROOT / 'results'
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print(f"Fitting Title-Weighted LDA Model ({NUM_TOPICS} topics, titles {TITLE_WEIGHT}x)")
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    # Load baseline vectorizer for consistent vocabulary
    vectorizer = load_baseline_vectorizer(BASELINE_VECTORIZER_PATH)
    print(f"Loaded baseline vectorizer with vocabulary size: {len(vectorizer.get_feature_names_out())}")

    # Load texts with title weighting
    print(f"Loading texts with titles appended {TITLE_WEIGHT} times...")
    texts, metadata, title_stats = load_weighted_texts(INPUT_DIR, TITLE_WEIGHT)
    print(f"  Loaded {len(texts)} documents")
    print(f"  Documents with titles: {title_stats['weighted']} / {title_stats['total']}")
    print(f"  Empty titles: {title_stats['empty']}")
    if title_stats['malformed']:
        print(f"⚠️  Warning: {title_stats['malformed']} malformed JSON lines skipped")

    if not texts:
        print("Error: No texts loaded")
        sys.exit(1)

    # Transform weighted texts using baseline vectorizer
    doc_term_matrix = transform_weighted_texts(texts, vectorizer)

    # Fit LDA model
    print("\n" + "=" * 60)
    print(f"Fitting {NUM_TOPICS}-topic LDA model with title weighting...")
    print("=" * 60)

    lda = fit_lda_model(doc_term_matrix, NUM_TOPICS)

    perplexity_score = lda.perplexity(doc_term_matrix)

    print("\n" + "=" * 60)
    print(f"Model: {NUM_TOPICS} topics")
    print(f"Iterations: {lda.n_iter_} / {LDA_PARAMS['max_iter']} (max_iter)")
    print(f"Training Perplexity: {perplexity_score:.4f}")
    print("(Note: Training perplexity is diagnostic only)")
    print("=" * 60)

    # Save model
    model_path = OUTPUT_DIR / f"title_weighted_lda_{NUM_TOPICS}_topics.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(lda, f)
    print(f"\n✅ Model saved to: {model_path}")

    print(f"✅ Using baseline vectorizer (shared with unweighted model)")

    # Infer document-topic distributions
    print("\nInferring document-topic distributions...")
    doc_topics = lda.transform(doc_term_matrix)

    # Save document-topic distribution
    results = []
    for doc_idx, (metadata_item, topic_dist) in enumerate(zip(metadata, doc_topics)):
        topic_probs = topic_dist / topic_dist.sum()

        row = {
            'doc_id': metadata_item['doc_id'],
            'title': metadata_item['title'],
            'year': metadata_item['year'],
        }

        for topic_idx in range(NUM_TOPICS):
            row[f'topic_{topic_idx + 1}_prob'] = f'{topic_probs[topic_idx]:.6f}'

        results.append(row)

    results_file = RESULTS_DIR / 'document_topic_distribution.csv'
    with open(results_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['doc_id', 'title', 'year'] + [f'topic_{i+1}_prob' for i in range(NUM_TOPICS)]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"✅ Document-topic distribution saved to: {results_file}")
    print(f"   Format: doc_id | title | year | topic_1_prob | ... | topic_44_prob")

    # Save title stats
    stats_file = OUTPUT_DIR / 'title_weighting_stats.txt'
    with open(stats_file, 'w') as f:
        f.write("Title Weighting Statistics\n")
        f.write("=" * 60 + "\n")
        f.write(f"Total documents: {title_stats['total']}\n")
        f.write(f"Documents with processed titles: {title_stats['weighted']}\n")
        f.write(f"Documents with empty titles: {title_stats['empty']}\n")
        f.write(f"Title coverage: {100*title_stats['weighted']/title_stats['total']:.2f}%\n")
        f.write(f"\nTitle weighting strategy: processed title words appended {TITLE_WEIGHT} times after body text\n")
        f.write(f"Note: Title heading removed from body at extraction; title counts exactly {TITLE_WEIGHT}x\n")

    print(f"✅ Title statistics saved to: {stats_file}")

    print("\n" + "=" * 60)
    print("Title-weighted LDA fitting complete")
    print("=" * 60)


if __name__ == '__main__':
    main()
