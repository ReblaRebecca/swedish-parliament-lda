#!/usr/bin/env python3
"""
Display topics from the title-weighted LDA model.
Extracts top words and probabilities for each topic.
Output: CSV file with 44 topics × 20 words per topic
"""

import csv
import pickle
from pathlib import Path
import sys


def display_topics(lda_model, vectorizer, num_words=20):
    """Extract and display top words for each topic.

    Normalizes topic weights to probabilities (sum to 1) to match baseline display.

    Args:
        lda_model: Fitted LDA model (num_topics derived from n_components)
        vectorizer: Fitted CountVectorizer
        num_words: Number of top words per topic (default 20)
    """
    topics_data = []
    num_topics = lda_model.n_components
    feature_names = vectorizer.get_feature_names_out()

    for topic_idx in range(num_topics):
        # Normalize topic weights to probabilities (sum to 1)
        topic_weights = lda_model.components_[topic_idx]
        topic_probs = topic_weights / topic_weights.sum()

        # Get top word indices for this topic
        top_indices = topic_probs.argsort()[-num_words:][::-1]

        row = {'topic': topic_idx + 1}

        for rank, word_idx in enumerate(top_indices, 1):
            word = feature_names[word_idx]
            prob = topic_probs[word_idx]
            row[f'word_{rank}'] = word
            row[f'prob_{rank}'] = f'{prob:.4f}'

        topics_data.append(row)

    return topics_data


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    MODEL_PATH = PROJECT_ROOT / 'models' / 'title_weighted_lda_44' / 'title_weighted_lda_44_topics.pkl'
    VECTORIZER_PATH = PROJECT_ROOT / 'models' / 'baseline_lda_44' / 'baseline_vectorizer.pkl'
    OUTPUT_CSV = PROJECT_ROOT / 'results' / 'weighted_44_TOPICS_FINAL.csv'

    NUM_WORDS = 20

    # Load model
    if not MODEL_PATH.exists():
        print(f"Error: Model not found at {MODEL_PATH}")
        sys.exit(1)

    print(f"Loading model from {MODEL_PATH}...")
    with open(MODEL_PATH, 'rb') as f:
        lda_model = pickle.load(f)

    # Load vectorizer
    if not VECTORIZER_PATH.exists():
        print(f"Error: Vectorizer not found at {VECTORIZER_PATH}")
        sys.exit(1)

    print(f"Loading vectorizer from {VECTORIZER_PATH}...")
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)

    # Validate model and vectorizer compatibility
    num_topics = lda_model.n_components
    vocab_size = len(vectorizer.get_feature_names_out())
    model_features = lda_model.components_.shape[1]

    if model_features != vocab_size:
        print(f"Error: Model features ({model_features}) != Vectorizer vocabulary ({vocab_size})")
        sys.exit(1)

    print("=" * 60)
    print(f"Displaying Title-Weighted LDA Topics ({num_topics} topics)")
    print("=" * 60)

    # Display topics
    print(f"Extracting top {NUM_WORDS} words for each of {num_topics} topics...")
    topics_data = display_topics(lda_model, vectorizer, NUM_WORDS)

    # Save to CSV
    output_csv_path = OUTPUT_CSV
    output_csv_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['topic'] + [f'word_{i}' for i in range(1, NUM_WORDS + 1)] + [f'prob_{i}' for i in range(1, NUM_WORDS + 1)]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(topics_data)

    print(f"\n✅ Topics saved to: {output_csv_path}")
    print(f"   Format: topic, word_1-20, prob_1-20")
    print(f"   Size: {output_csv_path.stat().st_size / 1024:.1f} KB")

    # Display sample (derived from topic count for flexibility)
    print(f"\nSample topics:")
    sample_indices = [0, num_topics // 4, num_topics // 2, num_topics - 1]
    for i in sample_indices:
        row = topics_data[i]
        print(f"\n  Topic {row['topic']}:")
        for j in range(1, 6):
            word = row[f'word_{j}']
            prob = row[f'prob_{j}']
            print(f"    {j}. {word:15s} ({prob})")

    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()
