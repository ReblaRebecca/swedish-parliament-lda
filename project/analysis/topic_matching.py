#!/usr/bin/env python3
"""
Permutation-invariant topic matching between LDA models.

Uses Hungarian algorithm to optimally match topics across different random seeds
or model variants, accounting for the fact that topic indices are arbitrary.

Key insight: Topic ordering is random across LDA runs. Topic 5 in seed 42 might
correspond to Topic 23 in seed 123. Comparing by index (5 vs 5) is invalid.
This module finds the optimal one-to-one correspondence before computing stability metrics.
"""

import numpy as np
from scipy.spatial.distance import cosine
from scipy.optimize import linear_sum_assignment


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


def match_and_evaluate(lda1, lda2, vocab1, vocab2, top_n=20, require_same_n_topics=True):
    """
    Complete pipeline: match topics optimally and compute all metrics.

    Args:
        lda1, lda2: Fitted LDA models to compare
        vocab1, vocab2: Vocabulary arrays (must be identical for valid cosine comparison)
        top_n: Number of top words for Jaccard calculation (must be positive integer)
        require_same_n_topics: If True, raise error if models have different topic counts
                              (required for seed-stability tests; can be False for cross-model comparison)

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


def format_match_details(lda1, lda2, vocab1, vocab2, matches, top_n=5, sort_by='cosine'):
    """
    Format matched topic pairs with top words for human inspection.

    Args:
        lda1, lda2: Fitted LDA models
        vocab1, vocab2: Vocabulary arrays
        matches: Output from match_and_evaluate() (list of (t1, t2, cosine, jaccard) tuples)
        top_n: Number of top words to display (default 5)
        sort_by: Sort matches by 'cosine', 'jaccard', 'topic1', or None (default 'cosine')

    Returns:
        formatted_string: Human-readable text representation
    """
    topics1 = lda1.components_
    topics2 = lda2.components_

    # Sort matches if requested
    if sort_by == 'cosine':
        sorted_matches = sorted(matches, key=lambda m: m[2], reverse=True)
    elif sort_by == 'jaccard':
        sorted_matches = sorted(matches, key=lambda m: m[3], reverse=True)
    elif sort_by == 'topic1':
        sorted_matches = sorted(matches, key=lambda m: m[0])
    elif sort_by is None:
        sorted_matches = matches
    else:
        raise ValueError(f"sort_by must be 'cosine', 'jaccard', 'topic1', or None, got '{sort_by}'")

    lines = []
    for t1_idx, t2_idx, cosine_sim, jaccard_sim in sorted_matches:
        # Get top words for each topic
        top_indices1 = np.argsort(topics1[t1_idx])[-top_n:][::-1]
        top_indices2 = np.argsort(topics2[t2_idx])[-top_n:][::-1]

        words1 = ', '.join(vocab1[i] for i in top_indices1)
        words2 = ', '.join(vocab2[i] for i in top_indices2)

        lines.append(
            f"Topic {t1_idx:2d} ↔ Topic {t2_idx:2d}  "
            f"[cosine: {cosine_sim:.4f}, jaccard: {jaccard_sim:.4f}]\n"
            f"  Model 1: {words1}\n"
            f"  Model 2: {words2}"
        )

    return '\n'.join(lines)
