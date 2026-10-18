#!/usr/bin/env python3
"""
Permutation-invariant topic matching between LDA models.

Uses Hungarian algorithm to optimally match topics across different random seeds
or model variants, accounting for the fact that topic indices are arbitrary.

Key insight: Topic ordering is random across LDA runs. Topic 5 in seed 42 might
correspond to Topic 23 in seed 123. Comparing by index (5 vs 5) is invalid.
This module finds the optimal one-to-one correspondence before computing stability metrics.

Vocabularies: models fitted with the same vectorizer (seed stability) are compared over their full,
identical vocabularies. Models with their own vocabularies (adjacent period models) are compared over the
words both vocabularies contain (shared_vocabulary=True), as Gordon (2026, 3.4).
"""

import numpy as np
from scipy.spatial.distance import cosine
from scipy.optimize import linear_sum_assignment
from scipy.stats import norm


def compute_topic_similarity_matrix(lda1, lda2, vocab1, vocab2, metric='cosine'):
    """
    Build a topic-to-topic similarity matrix between two LDA models.

    Args:
        lda1, lda2: Fitted sklearn LatentDirichletAllocation models
        vocab1, vocab2: Vocabulary arrays from vectorizer.get_feature_names_out()
        metric: 'cosine' (default) for complete distributions; other scipy.spatial.distance metrics supported

    Returns:
        similarity_matrix: (n_topics1 x n_topics2) array of similarities
            Values range [0, 1] where 1 = identical topics

    Raises:
        ValueError: If vocabularies differ or data is invalid
    """
    # Models are already validated as fitted by match_and_evaluate()
    topics1 = lda1.components_  # (n_topics1, n_features)
    topics2 = lda2.components_  # (n_topics2, n_features)

    # Validate topic arrays
    if not np.all(np.isfinite(topics1)) or not np.all(np.isfinite(topics2)):
        raise ValueError("Topic components contain non-finite values (NaN or inf)")

    if not np.all(topics1 >= 0) or not np.all(topics2 >= 0):
        raise ValueError("Topic components contain negative values")

    # Validate vocabulary
    vocab1 = np.asarray(vocab1)
    vocab2 = np.asarray(vocab2)

    if len(vocab1) != topics1.shape[1] or len(vocab2) != topics2.shape[1]:
        raise ValueError(
            f"Vocabulary length mismatch with components. "
            f"vocab1: {len(vocab1)} vs topics1 features: {topics1.shape[1]}, "
            f"vocab2: {len(vocab2)} vs topics2 features: {topics2.shape[1]}"
        )

    if not np.array_equal(vocab1, vocab2):
        raise ValueError(
            "Cosine topic matching requires identical vocabularies in identical column order. "
            f"vocab1 shape: {vocab1.shape}, vocab2 shape: {vocab2.shape}. "
            f"For seed-stability testing, use the same fitted vectorizer for all models."
        )

    # Normalize topic-word weights to probability distributions
    row_sums1 = topics1.sum(axis=1, keepdims=True)
    row_sums2 = topics2.sum(axis=1, keepdims=True)

    if np.any(row_sums1 == 0) or np.any(row_sums2 == 0):
        raise ValueError("Topic rows contain all-zero sums (degenerate topics)")

    topics1_normalized = topics1 / row_sums1
    topics2_normalized = topics2 / row_sums2

    n1, n2 = topics1_normalized.shape[0], topics2_normalized.shape[0]

    if metric == 'cosine':
        # Cosine similarity: 1 - cosine_distance
        # Compute pairwise cosine similarities
        similarity_matrix = np.zeros((n1, n2))
        for i in range(n1):
            for j in range(n2):
                # Cosine distance returns value in [0, 2]; convert to similarity [0, 1]
                dist = cosine(topics1_normalized[i], topics2_normalized[j])
                # Cosine distance is NaN if either vector is all zeros
                if np.isnan(dist):
                    similarity_matrix[i, j] = 0
                else:
                    similarity_matrix[i, j] = 1 - dist

        # Clip to [0, 1] to account for numerical precision edge cases
        similarity_matrix = np.clip(similarity_matrix, 0, 1)
    else:
        raise ValueError(f"Metric '{metric}' not yet supported")

    return similarity_matrix


class _SharedColumns:
    """A model's topic-word weights restricted to some of its columns (only components_ is used)."""

    def __init__(self, components):
        self.components_ = components


def restrict_to_shared_vocabulary(lda1, lda2, vocab1, vocab2):
    """Both models' topic-word weights over the words in both vocabularies, in the same order.

    Returns (restricted model 1, restricted model 2, shared vocabulary in vocab1's order).
    Cosine is scale-invariant, so normalizing over the shared words (to probabilities, as
    compute_topic_similarity_matrix does, or to unit length, as Gordon) gives the same similarity.
    """
    vocab1, vocab2 = np.asarray(vocab1), np.asarray(vocab2)
    if len(vocab1) != lda1.components_.shape[1] or len(vocab2) != lda2.components_.shape[1]:
        raise ValueError("Vocabulary length mismatch with components")
    if len(set(vocab1)) != len(vocab1) or len(set(vocab2)) != len(vocab2):
        raise ValueError("Vocabularies must not contain duplicate words")
    column2 = {word: j for j, word in enumerate(vocab2)}
    shared = [i for i, word in enumerate(vocab1) if word in column2]
    if not shared:
        raise ValueError("The two vocabularies have no words in common")
    columns2 = [column2[vocab1[i]] for i in shared]
    return (_SharedColumns(lda1.components_[:, shared]), _SharedColumns(lda2.components_[:, columns2]),
            vocab1[shared])


def permutation_null(similarity_matrix, n_permutations=1000, seed=0):
    """Matched mean similarity against random one-to-one matchings, as Gordon (2026, 3.4).

    The null distribution is the mean similarity of n_permutations random one-to-one matchings of the
    same topics (each a random permutation). z = (matched mean - null mean) / null SD; the p-value is
    one-sided (matched above the null) and taken from the standard normal distribution, as Gordon,
    not from the permutation counts.

    Args:
        similarity_matrix: square (n_topics x n_topics) array of similarities
    Returns:
        dict with matched_mean, null_mean, null_sd, z, p, n_permutations
    """
    similarity_matrix = np.asarray(similarity_matrix, dtype=float)
    n = similarity_matrix.shape[0]
    if similarity_matrix.shape != (n, n) or n < 2:
        raise ValueError("The permutation null needs a square similarity matrix with at least 2 topics")
    rows, cols = linear_sum_assignment(-similarity_matrix)
    matched_mean = float(similarity_matrix[rows, cols].mean())
    rng = np.random.default_rng(seed)
    null = np.array([similarity_matrix[np.arange(n), rng.permutation(n)].mean() for _ in range(n_permutations)])
    null_mean, null_sd = float(null.mean()), float(null.std(ddof=1))
    if null_sd > 1e-12:
        z = (matched_mean - null_mean) / null_sd
    else:
        # Every matching has the same mean (no structure): no signal, unless the matching is somehow higher
        z = 0.0 if np.isclose(matched_mean, null_mean) else float('inf')
    return {
        'matched_mean': matched_mean,
        'null_mean': null_mean,
        'null_sd': null_sd,
        'z': float(z),
        'p': float(norm.sf(z)),
        'n_permutations': n_permutations,
    }


def match_topics_hungarian(similarity_matrix):
    """
    Use Hungarian algorithm to find optimal one-to-one topic matching.

    Args:
        similarity_matrix: (n_topics1 x n_topics2) array of similarities

    Returns:
        matches: List of (topic_idx1, topic_idx2, similarity) tuples
    """
    # Hungarian algorithm minimizes cost, so negate similarities
    cost_matrix = -similarity_matrix

    # Find optimal assignment
    row_indices, col_indices = linear_sum_assignment(cost_matrix)

    matches = [
        (int(row), int(col), float(similarity_matrix[row, col]))
        for row, col in zip(row_indices, col_indices)
    ]

    return matches


def compute_topword_jaccard(lda1, lda2, vocab1, vocab2, matches, top_n=20):
    """
    Compute Jaccard similarity of top N words for matched topic pairs only.

    Args:
        lda1, lda2: Fitted LDA models
        vocab1, vocab2: Vocabulary arrays (from vectorizer.get_feature_names_out())
        matches: List of (topic_idx1, topic_idx2) tuples from Hungarian matching
        top_n: Number of top words to use for Jaccard calculation (default 20)

    Returns:
        jaccard_by_topic_pair: Dict mapping (topic_idx1, topic_idx2) -> jaccard_score
    """
    topics1 = lda1.components_
    topics2 = lda2.components_

    def get_top_word_indices(topic_weights, n=top_n):
        """Get indices of top N words for a topic."""
        return set(np.argsort(topic_weights)[-n:])

    def vocab_intersection_jaccard(indices1, indices2, words1, words2):
        """Compute Jaccard overlap of actual word strings (not indices)."""
        if len(indices1) == 0 or len(indices2) == 0:
            return 0.0

        words_set1 = set(words1[list(indices1)])
        words_set2 = set(words2[list(indices2)])

        intersection = len(words_set1 & words_set2)
        union = len(words_set1 | words_set2)

        return intersection / union if union > 0 else 0.0

    # Pre-compute top word indices for all topics (for efficiency)
    top_indices1 = {i: get_top_word_indices(topics1[i], top_n) for i in range(len(topics1))}
    top_indices2 = {i: get_top_word_indices(topics2[i], top_n) for i in range(len(topics2))}

    # Compute Jaccard only for matched pairs
    jaccard_scores = {}
    for t1_idx, t2_idx in matches:
        score = vocab_intersection_jaccard(
            top_indices1[t1_idx], top_indices2[t2_idx],
            vocab1, vocab2
        )
        jaccard_scores[(t1_idx, t2_idx)] = score

    return jaccard_scores


def match_and_evaluate(lda1, lda2, vocab1, vocab2, top_n=20, require_same_n_topics=True, shared_vocabulary=False):
    """
    Complete pipeline: match topics optimally and compute all metrics.

    Args:
        lda1, lda2: Fitted LDA models to compare
        vocab1, vocab2: Vocabulary arrays (identical, unless shared_vocabulary is True)
        top_n: Number of top words for Jaccard calculation (must be positive integer)
        require_same_n_topics: If True, raise error if models have different topic counts
                              (required for seed-stability tests; can be False for cross-model comparison)
        shared_vocabulary: If True, the models may have different vocabularies and cosine is computed over
                           the words both contain (Gordon's alignment of period models). Jaccard always
                           compares the top words of the full distributions.

    Returns:
        matches: List of (topic_idx1, topic_idx2, cosine_sim, jaccard_sim) tuples
        summary_stats: Dict with mean, median, min, max, std for both metrics
                      Uses population std (ddof=0) as these represent all matched pairs
        similarity_matrix: (n_topics1 x n_topics2) array of cosine similarities
                         Saved for reproducibility and debugging

    Raises:
        ValueError: If inputs are invalid or inconsistent
    """
    # Validate top_n first
    if not isinstance(top_n, int) or top_n <= 0:
        raise ValueError(f"top_n must be a positive integer, got {top_n}")

    # Validate models are fitted (check before accessing components_)
    if not hasattr(lda1, 'components_') or not hasattr(lda2, 'components_'):
        raise ValueError("Both models must be fitted LDA instances with components_ attribute")

    # Validate model consistency
    n_topics1 = lda1.components_.shape[0]
    n_topics2 = lda2.components_.shape[0]

    if require_same_n_topics and n_topics1 != n_topics2:
        raise ValueError(
            f"For seed-stability testing, models must have the same number of topics. "
            f"Got {n_topics1} vs {n_topics2}. "
            f"If cross-model comparison is intended, set require_same_n_topics=False."
        )

    # Step 1: Build similarity matrix using cosine similarity
    # This validates vocabulary consistency, finiteness, and non-negativity
    if shared_vocabulary:
        shared1, shared2, shared_vocab = restrict_to_shared_vocabulary(lda1, lda2, vocab1, vocab2)
        similarity_matrix = compute_topic_similarity_matrix(shared1, shared2, shared_vocab, shared_vocab, metric='cosine')
    else:
        similarity_matrix = compute_topic_similarity_matrix(lda1, lda2, vocab1, vocab2, metric='cosine')

    # Step 2: Find optimal matching
    matches = match_topics_hungarian(similarity_matrix)

    # Extract matched pairs (topic_idx1, topic_idx2) for efficiency
    matched_pairs = [(t1_idx, t2_idx) for t1_idx, t2_idx, _ in matches]

    # Step 3: Compute Jaccard for matched pairs only
    jaccard_scores = compute_topword_jaccard(lda1, lda2, vocab1, vocab2, matched_pairs, top_n=top_n)

    # Step 4: Enrich matches with Jaccard scores
    matches_with_jaccard = [
        (t1_idx, t2_idx, cosine_sim, jaccard_scores[(t1_idx, t2_idx)])
        for t1_idx, t2_idx, cosine_sim in matches
    ]

    # Step 5: Compute summary statistics
    cosine_sims = [m[2] for m in matches_with_jaccard]
    jaccard_sims = [m[3] for m in matches_with_jaccard]

    jaccard_key = f'jaccard_top{top_n}'

    # Note: np.std() uses population definition (ddof=0) because we are describing
    # all n_topics matched pairs, not a sample. This is consistent across all scripts.
    summary_stats = {
        'cosine': {
            'mean': float(np.mean(cosine_sims)),
            'median': float(np.median(cosine_sims)),
            'min': float(np.min(cosine_sims)),
            'max': float(np.max(cosine_sims)),
            'std': float(np.std(cosine_sims, ddof=0)),  # Population std
        },
        jaccard_key: {
            'mean': float(np.mean(jaccard_sims)),
            'median': float(np.median(jaccard_sims)),
            'min': float(np.min(jaccard_sims)),
            'max': float(np.max(jaccard_sims)),
            'std': float(np.std(jaccard_sims, ddof=0)),  # Population std
        }
    }

    return matches_with_jaccard, summary_stats, similarity_matrix
