#!/usr/bin/env python3
"""
Seed-stability test for the whole-corpus (baseline) LDA model (body text only).

Fits one model per seed with the baseline vocabulary, matches topics between every pair of
seeds with the Hungarian algorithm and writes a markdown report.
"""

import sys
from pathlib import Path

from seed_stability import (
    generate_report, per_topic_stability, run_seed_stability, save_report, save_topic_stability,
)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'modeling'))
from lda_common import BASELINE_MODEL_DIR, DEFAULT_SEED, NUM_TOPICS, STABILITY_SEEDS, load_baseline_vectorizer, load_body_texts  # noqa: E402


def main():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
    BASELINE_VECTORIZER_PATH = PROJECT_ROOT / 'models' / BASELINE_MODEL_DIR / 'baseline_vectorizer.pkl'
    OUTPUT_FILE = PROJECT_ROOT / 'docs' / 'reports' / f'BASELINE_STABILITY_{NUM_TOPICS}TOPICS_CORRECTED.md'

    print("=" * 80)
    print(f"Seed-Stability Test: {NUM_TOPICS}-Topic Baseline LDA")
    print(f"Seeds: {STABILITY_SEEDS}")
    print(f"Input: {INPUT_DIR}")
    print("=" * 80)

    print("\nLoading text...")
    texts, _, malformed = load_body_texts(INPUT_DIR)
    print(f"   Loaded {len(texts)} documents")
    if malformed:
        print(f"⚠️  {malformed} malformed JSON lines skipped")
    if not texts:
        print("Error: No texts loaded")
        sys.exit(1)

    print("\nLoading baseline vectorizer...")
    vectorizer = load_baseline_vectorizer(BASELINE_VECTORIZER_PATH)
    vocab = vectorizer.get_feature_names_out()
    print(f"   Vocabulary size: {len(vocab)} unique tokens")
    doc_term_matrix = vectorizer.transform(texts)

    seed_info, pairwise_results = run_seed_stability(doc_term_matrix, vocab, STABILITY_SEEDS, NUM_TOPICS)

    report = generate_report(
        f"Seed-Stability Analysis: {NUM_TOPICS}-Topic Baseline LDA",
        "Body text only (titles are not added)",
        NUM_TOPICS, seed_info, pairwise_results,
        closing_lines=[
            "## Key Change from Previous Analysis",
            "",
            "Previous reports compared Topic 1 to Topic 1, Topic 2 to Topic 2, etc. across seeds.",
            "This is methodologically invalid because topic indices are arbitrary.",
            "",
            "This corrected analysis uses the Hungarian algorithm to find optimal topic correspondences",
            "before computing similarities. The previous mean Jaccard value of ~0.02 reflected",
            "invalid index-by-index comparison. The values above reflect matched topics.",
        ],
    )
    save_report(report, OUTPUT_FILE)
    save_topic_stability(per_topic_stability(pairwise_results, DEFAULT_SEED, NUM_TOPICS), seed_info, DEFAULT_SEED,
                         PROJECT_ROOT / 'results' / f'BASELINE_STABILITY_{NUM_TOPICS}TOPICS_PER_TOPIC.csv')


if __name__ == '__main__':
    main()
