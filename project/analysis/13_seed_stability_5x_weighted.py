#!/usr/bin/env python3
"""
Seed-stability test for the 5x title-weighted LDA model (matches the reported model).

Title words are appended 5 times to the body text (weighting from modeling/lda_common.py).
Fits one model per seed with the baseline vocabulary, matches topics between every pair of
seeds with the Hungarian algorithm and writes a markdown report.
"""

import sys
from pathlib import Path

from seed_stability import (
    generate_report, per_topic_stability, run_seed_stability, save_report, save_topic_stability,
)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'modeling'))
from lda_common import (  # noqa: E402
    DEFAULT_SEED, NUM_TOPICS, STABILITY_SEEDS, TITLE_WEIGHT, load_baseline_vectorizer, load_weighted_texts,
)

# TITLE_WEIGHT (5) is the weight of the reported model in 10_fit_title_weighted_lda.py
assert TITLE_WEIGHT == 5, "lda_common.TITLE_WEIGHT changed: rename this script and its report"


def main():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
    BASELINE_VECTORIZER_PATH = PROJECT_ROOT / 'models' / 'baseline_lda_44' / 'baseline_vectorizer.pkl'
    OUTPUT_FILE = PROJECT_ROOT / 'results' / 'SEED_STABILITY_5X_WEIGHTED_CORRECTED.md'

    print("=" * 80)
    print(f"Seed-Stability Test: {TITLE_WEIGHT}x Title-Weighted LDA ({NUM_TOPICS} topics)")
    print(f"Seeds: {STABILITY_SEEDS}")
    print("=" * 80)

    print(f"\nLoading text with {TITLE_WEIGHT}x title weighting...")
    texts, _, title_stats = load_weighted_texts(INPUT_DIR, TITLE_WEIGHT)
    print(f"   Loaded {len(texts)} documents ({title_stats['weighted']} with titles)")
    if title_stats['malformed']:
        print(f"⚠️  {title_stats['malformed']} malformed JSON lines skipped")
    if not texts:
        print("Error: No texts loaded")
        sys.exit(1)

    print("\nLoading baseline vectorizer (shared vocabulary)...")
    vectorizer = load_baseline_vectorizer(BASELINE_VECTORIZER_PATH)
    vocab = vectorizer.get_feature_names_out()
    print(f"   Vocabulary size: {len(vocab)} unique tokens")
    doc_term_matrix = vectorizer.transform(texts)

    seed_info, pairwise_results = run_seed_stability(doc_term_matrix, vocab, STABILITY_SEEDS, NUM_TOPICS)

    report = generate_report(
        f"Seed-Stability Analysis: {TITLE_WEIGHT}x Title-Weighted LDA ({NUM_TOPICS} topics)",
        f"Title words are appended five times to the body text",
        NUM_TOPICS, seed_info, pairwise_results,
        closing_lines=[
            "## Comparison to Baseline",
            "",
            "Compare these values to the baseline 44-topic model (BASELINE_STABILITY_44TOPICS_CORRECTED.md)",
            "to assess whether title weighting improves topic stability across random seeds.",
        ],
    )
    save_report(report, OUTPUT_FILE)
    save_topic_stability(per_topic_stability(pairwise_results, DEFAULT_SEED, NUM_TOPICS), seed_info, DEFAULT_SEED,
                         PROJECT_ROOT / 'results' / 'SEED_STABILITY_5X_WEIGHTED_PER_TOPIC.csv')


if __name__ == '__main__':
    main()
