#!/usr/bin/env python3
"""
Extract top 20 words from weighted LDA model and regenerate wordcloud.
"""

import csv
import pickle
from pathlib import Path
import sys

try:
    import importlib.util
except ImportError:
    print("Error: importlib not available")
    sys.exit(1)


def extract_topics(lda_model, vectorizer, num_topics=44, num_words=20):
    """Extract top N words for each topic from LDA model, with normalized probabilities."""
    topics = []
    feature_names = vectorizer.get_feature_names_out()

    for topic_idx in range(num_topics):
        # Normalize topic weights to probabilities (sum to 1)
        topic_weights = lda_model.components_[topic_idx]
        topic_probs = topic_weights / topic_weights.sum()

        # Get top word indices
        top_indices = topic_probs.argsort()[-num_words:][::-1]

        top_words = [
            {
                'word': feature_names[i],
                'prob': float(topic_probs[i])
            }
            for i in top_indices
        ]
        topics.append({
            'topic_num': topic_idx + 1,
            'top_words': top_words
        })

    return topics


def save_topics_csv(topics, output_path):
    """Save topics in CSV format for wordcloud generation."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['topic'] + [f'word_{i}' for i in range(1, 21)] + [f'prob_{i}' for i in range(1, 21)]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for topic in topics:
            row = {'topic': f"Topic {topic['topic_num']}"}
            for i, word_data in enumerate(topic['top_words'], 1):
                row[f'word_{i}'] = word_data['word']
                # Format as normalized probability (0.0000 to 1.0000)
                row[f'prob_{i}'] = f"{word_data['prob']:.4f}"
            writer.writerow(row)

    print(f"✅ Topics CSV saved to: {output_path}")


def main():
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    WEIGHTED_MODEL_PATH = PROJECT_ROOT / 'models' / 'weighted_lda_44_shared_vocab' / 'weighted_lda_44_topics.pkl'
    VECTORIZER_PATH = PROJECT_ROOT / 'models' / 'weighted_lda_44_shared_vocab' / 'shared_vectorizer.pkl'
    WEIGHTED_DOCTOPICS_PATH = PROJECT_ROOT / 'results' / 'weighted_document_topic_distribution.csv'
    OUTPUT_TOPICS_CSV = PROJECT_ROOT / 'results' / 'weighted_44_TOPICS_SHARED_VOCAB.csv'
    OUTPUT_HTML = PROJECT_ROOT / 'results' / 'weighted_topics_wordclouds_shared_vocab.html'
    BASELINE_HTML = PROJECT_ROOT / 'results' / 'topics_wordclouds.html'

    print("=" * 70)
    print("Extract Topics from Weighted Model & Regenerate Wordcloud")
    print("=" * 70)

    if not WEIGHTED_MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
        print(f"Error: Model or vectorizer not found")
        sys.exit(1)

    # Load model and vectorizer
    print("Loading weighted LDA model...")
    with open(WEIGHTED_MODEL_PATH, 'rb') as f:
        weighted_lda = pickle.load(f)
    print(f"  ✓ Model: {weighted_lda.n_components} topics")

    print("Loading shared vocabulary...")
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
    vocab_size = len(vectorizer.get_feature_names_out())
    print(f"  ✓ Vocabulary: {vocab_size} features")

    feature_names = vectorizer.get_feature_names_out()
    if 'morgonsamling' in feature_names:
        print(f"  ✓ 'morgonsamling' in vocabulary")

    # Extract topics
    print("\nExtracting top 20 words per topic...")
    topics = extract_topics(weighted_lda, vectorizer, num_topics=44, num_words=20)
    save_topics_csv(topics, OUTPUT_TOPICS_CSV)

    # Regenerate wordcloud using existing script functions
    print(f"\nRegenerating wordcloud visualization...")

    # Load the wordcloud generation module
    spec = importlib.util.spec_from_file_location("wordcloud_gen", SCRIPT_DIR / '12_generate_weighted_wordclouds.py')
    gen_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen_module)

    # Use the functions
    prevalence = gen_module.calculate_topic_prevalence(str(WEIGHTED_DOCTOPICS_PATH), 44)
    topics_with_data = gen_module.load_topics_with_concentration(str(OUTPUT_TOPICS_CSV), prevalence)
    all_motions, top_motions_by_topic = gen_module.load_motions(str(WEIGHTED_DOCTOPICS_PATH))
    motions_by_topic = gen_module.filter_motions_by_dominant_topic(all_motions, 44, 15)

    output_path = gen_module.generate_html(
        topics_with_data,
        all_motions,
        BASELINE_HTML,
        OUTPUT_HTML,
        motions_by_topic,
        top_motions_by_topic
    )

    if output_path:
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"✅ Wordcloud saved: {output_path}")
        print(f"   Size: {file_size_mb:.1f} MB")
    else:
        print("Error: Could not generate wordcloud")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("Complete! Wordcloud updated with new shared vocabulary model.")
    print("=" * 70)
    print(f"Open: file:///{OUTPUT_HTML}")
    print("=" * 70)


if __name__ == '__main__':
    main()
