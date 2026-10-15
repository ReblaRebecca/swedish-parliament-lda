#!/usr/bin/env python3
"""
Display and save top words for 44-topic baseline LDA model.
Loads baseline_lda_44 model and shows top 20 words per topic with normalized probabilities.

Note: Displays normalized word probabilities (topic distribution sums to 1),
not raw component weights. Each p-value is P(word | topic).
"""

import pickle
import csv
from pathlib import Path
import sys


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent

    # Allow command-line argument for model directory
    # Usage: python3 08_display_lda_topics.py [model_dir]
    # Default: models/baseline_lda_44
    if len(sys.argv) >= 2:
        MODEL_DIR = Path(sys.argv[1])
    else:
        MODEL_DIR = SCRIPT_DIR.parent / 'models' / 'baseline_lda_44'

    # Load 44-topic baseline LDA model
    # NOTE: 44 topics is FIXED (determined from topic concentration testing)
    model_file = MODEL_DIR / 'baseline_lda_44_topics.pkl'
    vectorizer_file = MODEL_DIR / 'baseline_vectorizer.pkl'

    if not model_file.exists() or not vectorizer_file.exists():
        print(f"Error: Model or vectorizer not found in {MODEL_DIR}")
        print(f"Looking for:")
        print(f"  {model_file}")
        print(f"  {vectorizer_file}")
        sys.exit(1)

    print("Loading LDA model and vectorizer...")
    with open(model_file, 'rb') as f:
        lda_model = pickle.load(f)

    with open(vectorizer_file, 'rb') as f:
        vectorizer = pickle.load(f)

    # Get feature names (words)
    feature_names = vectorizer.get_feature_names_out()
    num_topics = lda_model.n_components
    num_words = 20  # Top N words per topic

    print("\n" + "=" * 80)
    print(f"BASELINE LDA MODEL: {num_topics} Topics")
    print("=" * 80)

    # Extract all topics
    topics_data = []
    for topic_idx, topic in enumerate(lda_model.components_):
        # Normalize topic weights to probabilities (sum to 1)
        topic_probs = topic / topic.sum()

        # Get top word indices
        top_word_indices = topic_probs.argsort()[-num_words:][::-1]
        top_words = [feature_names[i] for i in top_word_indices]
        top_probs = topic_probs[top_word_indices]

        # Display to console
        print(f"\nTopic {topic_idx + 1}:")
        print("-" * 80)
        for rank, (word, prob) in enumerate(zip(top_words, top_probs), 1):
            print(f"  {rank:2d}. {word:25s} (p={prob:.4f})")

        # Store for CSV (include both word and probability)
        row = {'topic': f'Topic {topic_idx + 1}'}
        for i, (word, prob) in enumerate(zip(top_words, top_probs), 1):
            row[f'word_{i}'] = word
            row[f'prob_{i}'] = f'{prob:.4f}'
        topics_data.append(row)

    # Save to CSV
    output_file = SCRIPT_DIR.parent / 'results' / '44_TOPICS_FINAL.csv'
    output_file.parent.mkdir(exist_ok=True, parents=True)

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['topic']
        for i in range(num_words):
            fieldnames.extend([f'word_{i+1}', f'prob_{i+1}'])
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(topics_data)

    print(f"\n" + "=" * 80)
    print(f"✅ Results saved to: {output_file}")
    print("=" * 80)


if __name__ == '__main__':
    main()
