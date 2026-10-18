#!/usr/bin/env python3
"""
Unit tests for analysis/topic_matching.py.
Verifies Hungarian algorithm-based topic matching on synthetic topic-word matrices.

Run from project/:
    python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'analysis'))
from topic_matching import match_and_evaluate, permutation_null  # noqa: E402


class MockLDA:
    """Mock LDA model for testing."""
    def __init__(self, components):
        self.components_ = components
        self.n_components = components.shape[0]


VOCAB = np.array([f"word_{i}" for i in range(10)])


def random_topics(n_topics=4, seed=0):
    """Random topic-word matrix (fixed seed, so the tests are reproducible)."""
    return np.random.default_rng(seed).dirichlet([1.0] * len(VOCAB), size=n_topics)


class TestTopicMatching(unittest.TestCase):

    def test_identical_models(self):
        """Identical models match perfectly (cosine = 1 for all topics)."""
        topics = random_topics()
        matches, _, _ = match_and_evaluate(MockLDA(topics.copy()), MockLDA(topics.copy()), VOCAB, VOCAB)
        for t1, t2, cosine, jaccard in matches:
            self.assertEqual(t1, t2)
            self.assertAlmostEqual(cosine, 1.0, places=6)
            self.assertAlmostEqual(jaccard, 1.0)

    def test_permuted_models(self):
        """A known permutation of the topics is recovered."""
        base_topics = random_topics()
        permutation = [2, 3, 0, 1]
        matches, _, _ = match_and_evaluate(MockLDA(base_topics), MockLDA(base_topics[permutation]), VOCAB, VOCAB)
        matched = {t2: t1 for t1, t2, _, _ in matches}
        for t2, expected_t1 in enumerate(permutation):
            self.assertEqual(matched[t2], expected_t1)

    def test_vocabulary_mismatch(self):
        """Different vocabularies raise ValueError."""
        topics = random_topics()
        with self.assertRaisesRegex(ValueError, '(?i)vocabular'):
            match_and_evaluate(MockLDA(topics), MockLDA(topics), VOCAB, VOCAB[:8])

    def test_reordered_vocabulary(self):
        """Same words in a different order raise ValueError (cosine would silently compare wrong words)."""
        topics = random_topics()
        with self.assertRaisesRegex(ValueError, '(?i)vocabular'):
            match_and_evaluate(MockLDA(topics), MockLDA(topics), VOCAB, VOCAB[::-1])

    def test_mismatched_topic_counts(self):
        """Different topic counts raise ValueError."""
        with self.assertRaisesRegex(ValueError, '(?i)topic'):
            match_and_evaluate(MockLDA(random_topics(4)), MockLDA(random_topics(5)), VOCAB, VOCAB,
                               require_same_n_topics=True)

    def test_invalid_top_n(self):
        """top_n must be a positive integer."""
        topics = random_topics()
        with self.assertRaisesRegex(ValueError, 'top_n'):
            match_and_evaluate(MockLDA(topics), MockLDA(topics), VOCAB, VOCAB, top_n=0)

    def test_unfitted_model(self):
        """A model without components_ raises ValueError."""
        class BadLDA:
            pass
        with self.assertRaisesRegex(ValueError, '(?i)fitted'):
            match_and_evaluate(MockLDA(random_topics()), BadLDA(), VOCAB, VOCAB)

    def test_summary_statistics(self):
        """Summary has both metrics with mean/median/min/max/std, matching the per-topic values."""
        matches, summary, _ = match_and_evaluate(MockLDA(random_topics(seed=1)), MockLDA(random_topics(seed=2)),
                                                 VOCAB, VOCAB)
        self.assertEqual(set(summary), {'cosine', 'jaccard_top20'})
        cosine = [m[2] for m in matches]
        jaccard = [m[3] for m in matches]
        for key, values in (('cosine', cosine), ('jaccard_top20', jaccard)):
            stats = summary[key]
            self.assertAlmostEqual(stats['mean'], np.mean(values))
            self.assertAlmostEqual(stats['median'], np.median(values))
            self.assertAlmostEqual(stats['min'], np.min(values))
            self.assertAlmostEqual(stats['max'], np.max(values))
            self.assertAlmostEqual(stats['std'], np.std(values))
            self.assertTrue(0 <= stats['min'] <= stats['max'] <= 1)



class TestSharedVocabulary(unittest.TestCase):
    """Period models with their own vocabularies are compared over the words both contain (Gordon)."""

    def test_same_topics_in_different_vocabularies(self):
        """Same weights on the shared words, other words and another column order: cosine 1."""
        topics = random_topics()
        # Model 2: the words in reverse order, plus two words model 1 does not have
        vocab2 = np.concatenate([VOCAB[::-1], ['new_a', 'new_b']])
        topics2 = np.hstack([topics[:, ::-1], np.full((len(topics), 2), 5.0)])
        matches, _, _ = match_and_evaluate(MockLDA(topics), MockLDA(topics2), VOCAB, vocab2, shared_vocabulary=True)
        for t1, t2, cosine, _ in matches:
            self.assertEqual(t1, t2)
            self.assertAlmostEqual(cosine, 1.0, places=6)

    def test_only_shared_words_count(self):
        """Weight on words outside the intersection does not change the cosine."""
        topics = random_topics()
        vocab1 = np.concatenate([VOCAB, ['only_in_1']])
        topics1 = np.hstack([topics, np.full((len(topics), 1), 100.0)])
        _, _, with_extra = match_and_evaluate(MockLDA(topics1), MockLDA(topics), vocab1, VOCAB, shared_vocabulary=True)
        _, _, without = match_and_evaluate(MockLDA(topics), MockLDA(topics), VOCAB, VOCAB)
        np.testing.assert_allclose(with_extra, without)

    def test_no_shared_words(self):
        topics = random_topics()
        other = np.array([f"other_{i}" for i in range(10)])
        with self.assertRaisesRegex(ValueError, '(?i)no words in common'):
            match_and_evaluate(MockLDA(topics), MockLDA(topics), VOCAB, other, shared_vocabulary=True)

    def test_default_still_requires_identical_vocabularies(self):
        """Seed stability compares models with one vectorizer: different vocabularies remain an error."""
        topics = random_topics()
        with self.assertRaisesRegex(ValueError, '(?i)vocabular'):
            match_and_evaluate(MockLDA(topics), MockLDA(topics), VOCAB, VOCAB[::-1])



class TestPermutationNull(unittest.TestCase):
    """Matched mean against random one-to-one matchings, as Gordon."""

    def test_clear_matching_is_far_above_the_null(self):
        # Diagonal 0.9, everything else 0.1: the matched mean is 0.9, random matchings are mostly near 0.1
        n = 8
        similarity = np.full((n, n), 0.1) + np.eye(n) * 0.8
        result = permutation_null(similarity, n_permutations=1000, seed=0)
        self.assertAlmostEqual(result['matched_mean'], 0.9)
        # A random permutation has on average one fixed point: null mean 0.1 + 0.8 / n
        self.assertAlmostEqual(result['null_mean'], 0.1 + 0.8 / n, delta=0.01)
        self.assertGreater(result['z'], 5)
        self.assertLess(result['p'], 1e-6)

    def test_matched_mean_uses_the_hungarian_matching(self):
        # Shuffled columns: the best matching is not the diagonal
        similarity = np.array([[0.1, 0.9, 0.2], [0.8, 0.1, 0.3], [0.2, 0.3, 0.7]])
        result = permutation_null(similarity, n_permutations=200, seed=1)
        self.assertAlmostEqual(result['matched_mean'], (0.9 + 0.8 + 0.7) / 3)

    def test_no_structure_gives_no_signal(self):
        # Every pair equally similar: every matching has the same mean, so z = 0 and p = 0.5
        result = permutation_null(np.full((5, 5), 0.4), n_permutations=100, seed=0)
        self.assertAlmostEqual(result['matched_mean'], result['null_mean'])
        self.assertEqual(result['z'], 0.0)
        self.assertAlmostEqual(result['p'], 0.5)

    def test_z_and_p_follow_the_formula(self):
        from scipy.stats import norm
        similarity = np.random.default_rng(3).random((6, 6))
        r = permutation_null(similarity, n_permutations=500, seed=2)
        self.assertAlmostEqual(r['z'], (r['matched_mean'] - r['null_mean']) / r['null_sd'])
        self.assertAlmostEqual(r['p'], norm.sf(r['z']))
        self.assertEqual(r['n_permutations'], 500)

    def test_reproducible_with_seed(self):
        similarity = np.random.default_rng(4).random((6, 6))
        self.assertEqual(permutation_null(similarity, 300, seed=7), permutation_null(similarity, 300, seed=7))

    def test_rejects_non_square(self):
        with self.assertRaises(ValueError):
            permutation_null(np.ones((3, 4)))


if __name__ == '__main__':
    unittest.main()
