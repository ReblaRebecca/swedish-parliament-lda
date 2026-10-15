#!/usr/bin/env python3
"""
Unit tests for topic_matching module.
Verifies Hungarian algorithm-based topic matching on synthetic and real data.
"""

import numpy as np
import sys
from pathlib import Path

# Import the matching module
from topic_matching import (
    compute_topic_similarity_matrix,
    match_topics_hungarian,
    match_and_evaluate,
)


class MockLDA:
    """Mock LDA model for testing."""
    def __init__(self, components):
        self.components_ = components
        self.n_components = components.shape[0]


def test_identical_models():
    """Test: Identical models should match perfectly (cosine=1.0 for all)."""
    print("Test 1: Identical models...")

    # Create identical topic matrix
    topics = np.random.dirichlet([1.0] * 10, size=4)

    lda1 = MockLDA(topics.copy())
    lda2 = MockLDA(topics.copy())
    vocab = np.array([f"word_{i}" for i in range(10)])

    matches, summary, sim_matrix = match_and_evaluate(lda1, lda2, vocab, vocab)

    # All matches should have cosine=1.0
    cosine_sims = [m[2] for m in matches]
    assert all(abs(s - 1.0) < 0.001 for s in cosine_sims), f"Expected all 1.0, got {cosine_sims}"
    print("  ✓ Passed: All matches have cosine=1.0")


def test_permuted_models():
    """Test: Permuted models should recover the permutation."""
    print("Test 2: Permuted models...")

    # Create base topics
    base_topics = np.random.dirichlet([1.0] * 10, size=4)

    # Apply known permutation
    permutation = [2, 3, 0, 1]
    permuted_topics = base_topics[permutation]

    lda1 = MockLDA(base_topics)
    lda2 = MockLDA(permuted_topics)
    vocab = np.array([f"word_{i}" for i in range(10)])

    matches, summary, sim_matrix = match_and_evaluate(lda1, lda2, vocab, vocab)

    # Check that matching recovered the permutation
    matched_pairs = {t2: t1 for t1, t2, _, _ in matches}
    for t2_idx in range(4):
        expected_t1 = permutation[t2_idx]
        actual_t1 = matched_pairs[t2_idx]
        assert actual_t1 == expected_t1, f"Permutation not recovered: t2[{t2_idx}] should match t1[{expected_t1}], got t1[{actual_t1}]"

    print("  ✓ Passed: Permutation correctly recovered")


def test_vocabulary_mismatch():
    """Test: Different vocabularies should raise ValueError."""
    print("Test 3: Vocabulary mismatch detection...")

    topics = np.random.dirichlet([1.0] * 10, size=4)
    lda1 = MockLDA(topics)
    lda2 = MockLDA(topics)

    vocab1 = np.array([f"word_{i}" for i in range(10)])
    vocab2 = np.array([f"word_{i}" for i in range(8)])  # Different size

    try:
        match_and_evaluate(lda1, lda2, vocab1, vocab2)
        assert False, "Should have raised ValueError for vocabulary mismatch"
    except ValueError as e:
        assert "vocabular" in str(e).lower()
        print("  ✓ Passed: ValueError raised for vocabulary mismatch")


def test_reordered_vocabulary():
    """Test: Reordered vocabulary (same words, different order) should raise ValueError.

    This is a critical safety check: cosine similarity silently fails if vocabularies
    are reordered because indices no longer correspond to the same words.
    """
    print("Test 3b: Reordered vocabulary detection (silent failure prevention)...")

    topics = np.random.dirichlet([1.0] * 10, size=4)
    lda1 = MockLDA(topics)
    lda2 = MockLDA(topics)

    vocab1 = np.array([f"word_{i}" for i in range(10)])
    vocab2 = vocab1[::-1]  # Same words, reversed order

    try:
        match_and_evaluate(lda1, lda2, vocab1, vocab2)
        assert False, "Should have raised ValueError for reordered vocabulary"
    except ValueError as e:
        assert "vocabular" in str(e).lower()
        print("  ✓ Passed: ValueError raised for reordered vocabulary")


def test_mismatched_topic_counts():
    """Test: Different topic counts should raise ValueError."""
    print("Test 4: Mismatched topic counts...")

    topics1 = np.random.dirichlet([1.0] * 10, size=4)
    topics2 = np.random.dirichlet([1.0] * 10, size=5)  # Different count

    lda1 = MockLDA(topics1)
    lda2 = MockLDA(topics2)
    vocab = np.array([f"word_{i}" for i in range(10)])

    try:
        match_and_evaluate(lda1, lda2, vocab, vocab, require_same_n_topics=True)
        assert False, "Should have raised ValueError for mismatched topic counts"
    except ValueError as e:
        assert "topic" in str(e).lower()
        print("  ✓ Passed: ValueError raised for mismatched topic counts")


def test_invalid_top_n():
    """Test: Invalid top_n parameter should raise ValueError."""
    print("Test 5: Invalid top_n parameter...")

    topics = np.random.dirichlet([1.0] * 10, size=4)
    lda1 = MockLDA(topics)
    lda2 = MockLDA(topics)
    vocab = np.array([f"word_{i}" for i in range(10)])

    try:
        match_and_evaluate(lda1, lda2, vocab, vocab, top_n=0)  # Invalid
        assert False, "Should have raised ValueError for invalid top_n"
    except ValueError as e:
        assert "top_n" in str(e).lower()
        print("  ✓ Passed: ValueError raised for invalid top_n")


def test_unfitted_model():
    """Test: Unfitted model should raise ValueError."""
    print("Test 6: Unfitted model detection...")

    # Create a mock object without components_
    class BadLDA:
        pass

    topics = np.random.dirichlet([1.0] * 10, size=4)
    lda1 = MockLDA(topics)
    lda2 = BadLDA()  # No components_
    vocab = np.array([f"word_{i}" for i in range(10)])

    try:
        match_and_evaluate(lda1, lda2, vocab, vocab)
        assert False, "Should have raised ValueError for unfitted model"
    except ValueError as e:
        assert "fitted" in str(e).lower()
        print("  ✓ Passed: ValueError raised for unfitted model")


def test_summary_statistics():
    """Test: Summary statistics are computed correctly."""
    print("Test 7: Summary statistics...")

    topics = np.random.dirichlet([1.0] * 10, size=4)
    lda1 = MockLDA(topics)
    lda2 = MockLDA(topics)
    vocab = np.array([f"word_{i}" for i in range(10)])

    matches, summary, sim_matrix = match_and_evaluate(lda1, lda2, vocab, vocab)

    # Verify summary structure
    assert 'cosine' in summary
    assert 'jaccard_top20' in summary

    cosine_stats = summary['cosine']
    assert all(k in cosine_stats for k in ['mean', 'median', 'min', 'max', 'std'])

    # Verify values are in valid ranges
    assert 0 <= cosine_stats['mean'] <= 1.0
    assert 0 <= cosine_stats['median'] <= 1.0
    assert 0 <= cosine_stats['min'] <= 1.0
    assert 0 <= cosine_stats['max'] <= 1.0
    assert cosine_stats['std'] >= 0

    print("  ✓ Passed: Summary statistics computed correctly")


def main():
    print("=" * 60)
    print("Testing topic_matching module")
    print("=" * 60)
    print()

    try:
        test_identical_models()
        test_permuted_models()
        test_vocabulary_mismatch()
        test_reordered_vocabulary()
        test_mismatched_topic_counts()
        test_invalid_top_n()
        test_unfitted_model()
        test_summary_statistics()

        print()
        print("=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"❌ Test failed: {e}")
        print("=" * 60)
        return 1
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
