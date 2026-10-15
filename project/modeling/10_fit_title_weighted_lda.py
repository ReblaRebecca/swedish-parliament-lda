#!/usr/bin/env python3
"""
Fit title-weighted LDA model for comparison with baseline.
Strategy: Append processed title words five additional times to body text.
If title is already in body, effective count could be higher (up to 6x original).
This weights document-topic inference toward title content without changing vocabulary.

Input: Deduplicated motions with title_processed field
Output: Title-weighted LDA model, weighted vectorizer, document-topic distribution
Configuration: 44 topics, same settings as baseline for fair comparison
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
    print("Error: scikit-learn not installed")
    sys.exit(1)


def load_texts_with_titles(input_dir):
    """Load final preprocessed text and processed titles from all temporal bins.

    Creates weighted documents by appending processed title words five additional times.
    Note: If title words already appear in body, effective count could reach 6x original.
    Returns: texts (list), metadata (list), title_stats (dict)
    """
    print("Loading texts with title processing...")
    texts = []
    metadata = []
    title_stats = {'empty': 0, 'weighted': 0, 'total': 0}

    for bin_file in sorted(input_dir.glob('group*.jsonl')):
        print(f"  Loading {bin_file.name}...")
        with open(bin_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    motion = json.loads(line.strip())
                    text = motion.get('text_lemmatized', '')
                    title = motion.get('title_processed', '')

                    title_stats['total'] += 1

                    # Create weighted document: body + (title * 5)
                    if title and title.strip():
                        weighted_text = text + ' ' + (' '.join(title.split()) + ' ') * 5
                        title_stats['weighted'] += 1
                    else:
                        weighted_text = text
                        title_stats['empty'] += 1

                    if weighted_text.strip():
                        texts.append(weighted_text)
                        metadata.append({
                            'doc_id': motion.get('dok_id', 'unknown'),
                            'title': motion.get('title', ''),
                            'year': motion.get('date', '')[:4] if motion.get('date') else 'unknown'
                        })
                except json.JSONDecodeError:
                    continue

    print(f"  Loaded {len(texts)} documents")
    print(f"  Documents with titles: {title_stats['weighted']} / {title_stats['total']}")
    print(f"  Empty titles: {title_stats['empty']}")

    return texts, metadata, title_stats


def load_baseline_vectorizer(vectorizer_path):
    """Load the baseline vectorizer for consistent vocabulary."""
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)
    print(f"Loaded baseline vectorizer with vocabulary size: {len(vectorizer.get_feature_names_out())}")
    return vectorizer


def transform_weighted_texts(texts, vectorizer):
    """Transform weighted texts using baseline vectorizer."""
    print("Transforming weighted documents with baseline vectorizer...")
    doc_term_matrix = vectorizer.transform(texts)
    print(f"Document-term matrix shape: {doc_term_matrix.shape}")
    return doc_term_matrix


def fit_lda_model(doc_term_matrix, num_topics, random_state=42):
    """Fit LDA model with given number of topics."""
    lda = LatentDirichletAllocation(
        n_components=num_topics,
        random_state=random_state,
        max_iter=50,
        learning_method='online',
        n_jobs=2,
        verbose=0,
    )
    lda.fit(doc_term_matrix)
    return lda


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'deduplicated'
    BASELINE_VECTORIZER_PATH = PROJECT_ROOT / 'models' / 'baseline_lda_44' / 'baseline_vectorizer.pkl'
    OUTPUT_DIR = PROJECT_ROOT / 'models' / 'title_weighted_lda_44'
    RESULTS_DIR = PROJECT_ROOT / 'results'
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    NUM_TOPICS = 44

    print("=" * 60)
    print("Fitting Title-Weighted LDA Model (44 topics)")
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    # Load baseline vectorizer for consistent vocabulary
    if not BASELINE_VECTORIZER_PATH.exists():
        print(f"Error: Baseline vectorizer not found at {BASELINE_VECTORIZER_PATH}")
        sys.exit(1)

    vectorizer = load_baseline_vectorizer(BASELINE_VECTORIZER_PATH)

    # Load texts with title weighting
    texts, metadata, title_stats = load_texts_with_titles(INPUT_DIR)

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
    print(f"Iterations: {lda.n_iter_} / 50 (max_iter)")
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
        f.write(f"\nTitle weighting strategy: Five additional copies appended\n")
        f.write(f"(Processed title words appended 5 more times after body text)\n")
        f.write(f"Note: If title words already appear in body, effective count up to 6x\n")

    print(f"✅ Title statistics saved to: {stats_file}")

    print("\n" + "=" * 60)
    print("Title-weighted LDA fitting complete")
    print("=" * 60)


if __name__ == '__main__':
    main()
