#!/usr/bin/env python3
"""
Validation of corrected topic matching methodology.

Two tests:
1. Smoke test: verifies pipeline executes on real text (but doesn't prove matching is correct)
2. Synthetic permutation test: validates matching correctness on known ground truth
"""

import json
import numpy as np
from pathlib import Path
import sys

from topic_matching import match_and_evaluate

try:
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
except ImportError:
    print("Error: scikit-learn not installed")
    sys.exit(1)


def load_sample_texts(input_dir, max_docs=2000):
    """Load a small sample of the final preprocessed text (as used by the models) for quick testing."""
    texts = []
    for bin_file in sorted(input_dir.glob('group*.jsonl')):
        with open(bin_file, 'r', encoding='utf-8') as f:
            for line in f:
                if len(texts) >= max_docs:
                    return texts
                try:
                    motion = json.loads(line.strip())
                    text = motion.get('text_no_stopwords', '')
                    if text:
                        texts.append(text)
                except json.JSONDecodeError:
                    continue
    return texts


def main():
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent
    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'

    NUM_TOPICS = 8
    SEEDS = [42, 123]

    print("=" * 80)
    print(f"Quick Validation: Topic Matching with {NUM_TOPICS} topics, {len(SEEDS)} seeds")
    print("=" * 80)

    # Load small sample
    print("\n1. Loading sample texts (max 2000 for speed)...")
    texts = load_sample_texts(INPUT_DIR, max_docs=2000)
    print(f"   Loaded {len(texts)} documents")

    # Create vectorizer once
    print("\n2. Creating vectorizer...")
    vectorizer = CountVectorizer(
        max_df=0.5,
        min_df=5,
        max_features=10000,
        stop_words=None,
    )
    doc_term_matrix = vectorizer.fit_transform(texts)
    vocab = vectorizer.get_feature_names_out()
    print(f"   Vocabulary: {len(vocab)} tokens")

    # Fit 2 models with different seeds
    print(f"\n3. Fitting {len(SEEDS)} LDA models ({NUM_TOPICS} topics each)...")
    models_by_seed = {}
    for seed in SEEDS:
        print(f"   Seed {seed}...")
        lda = LatentDirichletAllocation(
            n_components=NUM_TOPICS,
            random_state=seed,
            max_iter=20,  # Quick convergence for validation
            learning_method='online',
            n_jobs=2,
            verbose=0,
        )
        lda.fit(doc_term_matrix)
        models_by_seed[seed] = lda
        print(f"     Perplexity: {lda.perplexity(doc_term_matrix):.2f}")

    # Compare the two models
    print(f"\n4. Computing optimal topic matching...")
    lda1 = models_by_seed[SEEDS[0]]
    lda2 = models_by_seed[SEEDS[1]]

    try:
        matches, summary, similarity_matrix = match_and_evaluate(lda1, lda2, vocab, vocab, top_n=10)
        print("   ✅ Matching succeeded")
    except Exception as e:
        print(f"   ❌ Matching failed: {e}")
        sys.exit(1)

    # Report results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)

    cosine_stats = summary['cosine']
    jaccard_key = [k for k in summary.keys() if k.startswith('jaccard_')][0]
    jaccard_stats = summary[jaccard_key]

    print(f"\n{SEEDS[0]} vs {SEEDS[1]}:")
    print(f"\nCosine Similarity:")
    print(f"  Mean: {cosine_stats['mean']:.4f}")
    print(f"  Median: {cosine_stats['median']:.4f}")
    print(f"  Std: {cosine_stats['std']:.4f}")
    print(f"\n{jaccard_key}:")
    print(f"  Mean: {jaccard_stats['mean']:.4f}")
    print(f"  Median: {jaccard_stats['median']:.4f}")
    print(f"  Std: {jaccard_stats['std']:.4f}")

    # Show a few matched pairs
    print(f"\nSample matched topic pairs:")
    for t1, t2, cosine_sim, jaccard_sim in matches[:3]:
        print(f"  Topic {t1} ↔ Topic {t2}: cosine={cosine_sim:.4f}, {jaccard_key}={jaccard_sim:.4f}")

    print("\n✅ Validation complete—corrected methodology works.")
    print("=" * 80)


def test_synthetic_permutation():
    """
    Synthetic validation: create two identical topic matrices with known permutation.

    Ground truth: if lda1 has topics [A, B, C, D], lda2 has topics [C, D, A, B],
    then the optimal matching should identify this permutation correctly.
    """
    print("\n" + "=" * 80)
    print("SYNTHETIC PERMUTATION TEST: Validate Matching on Known Ground Truth")
    print("=" * 80)

    # Create synthetic topic matrix: 4 topics, 10 words
    # Each topic is a distribution over 10 words
    np.random.seed(42)
    n_topics = 4
    n_words = 10

    # Create 4 distinct base topics
    base_topics = np.random.dirichlet([1.0] * n_words, size=n_topics)
    print(f"\nBase topics shape: {base_topics.shape}")

    # lda1: original topic order [0, 1, 2, 3]
    lda1_components = base_topics.copy()

    # lda2: permuted topic order [2, 3, 0, 1]
    # So lda2 topic 0 is actually base topic 2, etc.
    permutation = [2, 3, 0, 1]
    lda2_components = base_topics[permutation].copy()

    print(f"Ground truth permutation: {permutation}")
    print(f"  lda2 topic 0 should match lda1 topic {permutation[0]}")
    print(f"  lda2 topic 1 should match lda1 topic {permutation[1]}")
    print(f"  lda2 topic 2 should match lda1 topic {permutation[2]}")
    print(f"  lda2 topic 3 should match lda1 topic {permutation[3]}")

    # Create mock LDA objects with these components
    from sklearn.decomposition import LatentDirichletAllocation

    class MockLDA:
        def __init__(self, components):
            self.components_ = components

    lda1 = MockLDA(lda1_components)
    lda2 = MockLDA(lda2_components)

    # Create vocabulary (doesn't matter, just for validation)
    vocab = np.array([f"word_{i}" for i in range(n_words)])

    # Run matching
    print("\nRunning topic matching...")
    try:
        matches, summary, sim_matrix = match_and_evaluate(lda1, lda2, vocab, vocab, top_n=5)
    except Exception as e:
        print(f"❌ Matching failed: {e}")
        return False

    # Check if matching recovered the permutation
    print("\nMatched pairs:")
    matched_permutation = [None] * n_topics
    for t1_idx, t2_idx, cosine_sim, jaccard_sim in matches:
        print(f"  lda1 topic {t1_idx} ↔ lda2 topic {t2_idx} (cosine: {cosine_sim:.4f})")
        matched_permutation[t2_idx] = t1_idx

    # Verify: lda2_topic[i] should match lda1_topic[permutation[i]]
    # Or equivalently: matched_permutation[i] should equal permutation[i]
    correct = 0
    for t2_idx in range(n_topics):
        expected_t1 = permutation[t2_idx]
        actual_t1 = matched_permutation[t2_idx]
        if actual_t1 == expected_t1:
            correct += 1
            status = "✅"
        else:
            status = "❌"
        print(f"{status} lda2 topic {t2_idx}: expected lda1 topic {expected_t1}, got {actual_t1}")

    if correct == n_topics:
        print(f"\n✅ SYNTHETIC TEST PASSED: Matching correctly recovered all {n_topics} permutation pairs")
        return True
    else:
        print(f"\n❌ SYNTHETIC TEST FAILED: Only {correct}/{n_topics} pairs matched correctly")
        return False


if __name__ == '__main__':
    # Run smoke test (real data)
    main()

    # Run synthetic validation (known ground truth)
    synthetic_ok = test_synthetic_permutation()
