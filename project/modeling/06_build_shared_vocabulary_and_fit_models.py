#!/usr/bin/env python3
"""
Build shared vocabulary (max_features=20000) from processed body + one title copy.
Train both baseline and weighted LDA models using this shared vocabulary.

This ensures fair comparison: both models use the same feature space,
only the document weighting differs (baseline: body only; weighted: body + 5× titles).
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


def load_texts_and_titles(input_dir):
    """Load processed body text and titles from all temporal bins."""
    print("Loading texts and titles...")
    texts = []
    metadata = []

    for bin_file in sorted(input_dir.glob('group*.jsonl')):
        print(f"  Loading {bin_file.name}...")
        with open(bin_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    motion = json.loads(line.strip())
                    body = motion.get('text_no_stopwords', '').strip()
                    title = motion.get('title_processed', '').strip()

                    if body:
                        texts.append(body)
                        metadata.append({
                            'doc_id': motion.get('dok_id', 'unknown'),
                            'title': motion.get('title', ''),
                            'year': motion.get('date', '')[:4] if motion.get('date') else 'unknown',
                            'body': body,
                            'title_processed': title
                        })
                except json.JSONDecodeError:
                    continue

    print(f"  Loaded {len(texts)} documents")
    return texts, metadata


def build_shared_vocabulary(texts, metadata, max_features=20000):
    """
    Build shared vocabulary from body text + one copy of processed titles.
    This vocabulary will be reused for both baseline and weighted models.
    """
    print(f"\nBuilding shared vocabulary (max_features={max_features})...")
    print("  Combining: processed body + one copy of processed title")

    # Create vocabulary corpus: body + one title copy
    vocab_corpus = []
    for meta in metadata:
        body = meta['body']
        title = meta['title_processed']
        # One copy of title (not five)
        combined = body + ' ' + title if title else body
        vocab_corpus.append(combined)

    # Fit vectorizer on combined corpus
    vectorizer = CountVectorizer(
        max_df=0.5,
        min_df=5,
        max_features=max_features,
        lowercase=True,
        # Match sklearn default: require 2+ word characters, filters single letters
    )
    vectorizer.fit(vocab_corpus)

    vocab = vectorizer.get_feature_names_out()
    print(f"  ✓ Vocabulary size: {len(vocab)}")

    # Check key words
    for word in ['morgonsamling', 'skolverket', 'högskola', 'lärare']:
        if word in vocab:
            print(f"  ✓ '{word}' is in vocabulary")
        else:
            print(f"  ✗ '{word}' is NOT in vocabulary")

    return vectorizer


def create_baseline_corpus(metadata):
    """Create corpus for baseline model: body text only."""
    print("\nCreating baseline corpus (body only)...")
    texts = [meta['body'] for meta in metadata]
    print(f"  {len(texts)} documents")
    return texts


def create_weighted_corpus(metadata):
    """Create corpus for weighted model: body + five title copies."""
    print("\nCreating weighted corpus (body + 5× titles)...")
    texts = []
    for meta in metadata:
        body = meta['body']
        title = meta['title_processed']
        # Five additional copies of title
        if title and title.strip():
            weighted_text = body + ' ' + (' '.join(title.split()) + ' ') * 5
        else:
            weighted_text = body
        texts.append(weighted_text)
    print(f"  {len(texts)} documents")
    return texts


def fit_lda_model(doc_term_matrix, num_topics, model_name, random_state=42):
    """Fit LDA model."""
    print(f"Fitting {model_name} LDA model ({num_topics} topics)...")
    lda = LatentDirichletAllocation(
        n_components=num_topics,
        random_state=random_state,
        max_iter=50,
        learning_method='online',
        n_jobs=2,
        verbose=0,
    )
    lda.fit(doc_term_matrix)
    perplexity = lda.perplexity(doc_term_matrix)
    print(f"  Iterations: {lda.n_iter_} / 50 (max)")
    print(f"  Perplexity: {perplexity:.4f}")
    return lda


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
    BASELINE_OUTPUT_DIR = PROJECT_ROOT / 'models' / 'baseline_lda_44_shared_vocab'
    WEIGHTED_OUTPUT_DIR = PROJECT_ROOT / 'models' / 'weighted_lda_44_shared_vocab'
    RESULTS_DIR = PROJECT_ROOT / 'results'

    BASELINE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    WEIGHTED_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    NUM_TOPICS = 44

    print("=" * 70)
    print("Build Shared Vocabulary and Fit Baseline + Weighted LDA Models")
    print("=" * 70)

    if not INPUT_DIR.exists():
        print(f"Error: {INPUT_DIR} not found")
        sys.exit(1)

    # Load texts and metadata
    texts, metadata = load_texts_and_titles(INPUT_DIR)

    if not texts:
        print("Error: No texts loaded")
        sys.exit(1)

    # Build shared vocabulary
    vectorizer = build_shared_vocabulary(texts, metadata, max_features=20000)

    # Save shared vectorizer
    vectorizer_path = BASELINE_OUTPUT_DIR / 'shared_vectorizer.pkl'
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"\n✅ Shared vectorizer saved to: {vectorizer_path}")

    # Copy to weighted model directory
    weighted_vectorizer_path = WEIGHTED_OUTPUT_DIR / 'shared_vectorizer.pkl'
    with open(weighted_vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"✅ Shared vectorizer also saved to: {weighted_vectorizer_path}")

    # ============ BASELINE MODEL ============
    print("\n" + "=" * 70)
    print("BASELINE MODEL (body only)")
    print("=" * 70)

    baseline_texts = create_baseline_corpus(metadata)
    baseline_matrix = vectorizer.transform(baseline_texts)
    print(f"Document-term matrix shape: {baseline_matrix.shape}")

    baseline_lda = fit_lda_model(baseline_matrix, NUM_TOPICS, "Baseline", random_state=42)

    # Save baseline model
    baseline_model_path = BASELINE_OUTPUT_DIR / f'baseline_lda_{NUM_TOPICS}_topics.pkl'
    with open(baseline_model_path, 'wb') as f:
        pickle.dump(baseline_lda, f)
    print(f"✅ Baseline model saved to: {baseline_model_path}")

    # Infer baseline document-topic distributions
    baseline_doc_topics = baseline_lda.transform(baseline_matrix)

    # ============ WEIGHTED MODEL ============
    print("\n" + "=" * 70)
    print("WEIGHTED MODEL (body + 5× titles)")
    print("=" * 70)

    weighted_texts = create_weighted_corpus(metadata)
    weighted_matrix = vectorizer.transform(weighted_texts)
    print(f"Document-term matrix shape: {weighted_matrix.shape}")

    weighted_lda = fit_lda_model(weighted_matrix, NUM_TOPICS, "Weighted", random_state=42)

    # Save weighted model
    weighted_model_path = WEIGHTED_OUTPUT_DIR / f'weighted_lda_{NUM_TOPICS}_topics.pkl'
    with open(weighted_model_path, 'wb') as f:
        pickle.dump(weighted_lda, f)
    print(f"✅ Weighted model saved to: {weighted_model_path}")

    # Infer weighted document-topic distributions
    weighted_doc_topics = weighted_lda.transform(weighted_matrix)

    # ============ SAVE DOCUMENT-TOPIC DISTRIBUTIONS ============
    print("\n" + "=" * 70)
    print("Saving document-topic distributions")
    print("=" * 70)

    # Baseline
    baseline_results_file = RESULTS_DIR / 'baseline_document_topic_distribution.csv'
    with open(baseline_results_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['doc_id', 'title', 'year'] + [f'topic_{i+1}_prob' for i in range(NUM_TOPICS)]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for doc_idx, (meta, topic_dist) in enumerate(zip(metadata, baseline_doc_topics)):
            topic_probs = topic_dist / topic_dist.sum()
            row = {
                'doc_id': meta['doc_id'],
                'title': meta['title'],
                'year': meta['year'],
            }
            for topic_idx in range(NUM_TOPICS):
                row[f'topic_{topic_idx + 1}_prob'] = f'{topic_probs[topic_idx]:.6f}'
            writer.writerow(row)

    print(f"✅ Baseline distribution saved to: {baseline_results_file}")

    # Weighted
    weighted_results_file = RESULTS_DIR / 'weighted_document_topic_distribution.csv'
    with open(weighted_results_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['doc_id', 'title', 'year'] + [f'topic_{i+1}_prob' for i in range(NUM_TOPICS)]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for doc_idx, (meta, topic_dist) in enumerate(zip(metadata, weighted_doc_topics)):
            topic_probs = topic_dist / topic_dist.sum()
            row = {
                'doc_id': meta['doc_id'],
                'title': meta['title'],
                'year': meta['year'],
            }
            for topic_idx in range(NUM_TOPICS):
                row[f'topic_{topic_idx + 1}_prob'] = f'{topic_probs[topic_idx]:.6f}'
            writer.writerow(row)

    print(f"✅ Weighted distribution saved to: {weighted_results_file}")

    print("\n" + "=" * 70)
    print("Complete! Both models trained with shared vocabulary.")
    print("=" * 70)
    print(f"Baseline: {baseline_model_path}")
    print(f"Weighted: {weighted_model_path}")
    print(f"Shared vectorizer: {vectorizer_path}")
    print("=" * 70)


if __name__ == '__main__':
    main()
