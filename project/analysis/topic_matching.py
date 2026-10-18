#!/usr/bin/env python3
"""
Topic matching between LDA models: Hungarian one-to-one matching on cosine similarity.

Topic numbers are arbitrary in each fitted model (topic 5 of one seed may be topic 23 of another), so
topics are matched optimally before they are compared.

Vocabularies: models fitted with the same vectorizer (seed stability) are compared over their full,
identical vocabularies. Models with their own vocabularies (adjacent period models) are compared over the
words both vocabularies contain (shared_vocabulary=True), as Gordon (2026, 3.4).
"""

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.stats import norm


def compute_topic_similarity_matrix(lda1, lda2, vocab1, vocab2):
    """Cosine similarity between every topic of lda1 and every topic of lda2, in [0, 1].

    The two models must have identical vocabularies in identical column order (else ValueError),
    so that cosine compares the same words.
    """
    topics1, topics2 = lda1.components_, lda2.components_
    if not np.all(np.isfinite(topics1)) or not np.all(np.isfinite(topics2)):
        raise ValueError("Topic components contain non-finite values (NaN or inf)")
    if not np.all(topics1 >= 0) or not np.all(topics2 >= 0):
        raise ValueError("Topic components contain negative values")

    vocab1, vocab2 = np.asarray(vocab1), np.asarray(vocab2)
    if len(vocab1) != topics1.shape[1] or len(vocab2) != topics2.shape[1]:
        raise ValueError(f"Vocabulary length mismatch with components: {len(vocab1)} vs {topics1.shape[1]}, "
                         f"{len(vocab2)} vs {topics2.shape[1]}")
    if not np.array_equal(vocab1, vocab2):
        raise ValueError("Cosine topic matching requires identical vocabularies in identical column order "
                         "(seed stability: one vectorizer for all models; periods: shared_vocabulary=True)")

    norms1 = np.linalg.norm(topics1, axis=1, keepdims=True)
    norms2 = np.linalg.norm(topics2, axis=1, keepdims=True)
    if np.any(norms1 == 0) or np.any(norms2 == 0):
        raise ValueError("Topic rows contain all-zero weights (degenerate topics)")
    # Cosine does not depend on scale, so the raw weights give the same value as normalized distributions
    return np.clip((topics1 / norms1) @ (topics2 / norms2).T, 0, 1)


class _SharedColumns:
    """A model's topic-word weights restricted to some of its columns (only components_ is used)."""

    def __init__(self, components):
        self.components_ = components


def restrict_to_shared_vocabulary(lda1, lda2, vocab1, vocab2):
    """Both models' topic-word weights over the words in both vocabularies, in the same order.

    Returns (restricted model 1, restricted model 2, shared vocabulary in vocab1's order).
    Cosine is scale-invariant, so this equals Gordon's cosine on L2-normalized distributions over
    the shared words.
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
    """Optimal one-to-one matching: [(topic index 1, topic index 2, similarity)], maximizing total similarity."""
    rows, cols = linear_sum_assignment(-similarity_matrix)
    return [(int(r), int(c), float(similarity_matrix[r, c])) for r, c in zip(rows, cols)]


def compute_topword_jaccard(lda1, lda2, vocab1, vocab2, matches, top_n=20):
    """Jaccard overlap of the top_n words (as strings) of each matched pair: {(t1, t2): score}."""
    vocab1, vocab2 = np.asarray(vocab1), np.asarray(vocab2)

    def top_words(lda, vocab, t):
        return set(vocab[np.argsort(lda.components_[t])[-top_n:]])

    scores = {}
    for t1, t2 in matches:
        words1, words2 = top_words(lda1, vocab1, t1), top_words(lda2, vocab2, t2)
        union = words1 | words2
        scores[(t1, t2)] = len(words1 & words2) / len(union) if union else 0.0
    return scores


def summary(values):
    # Population std (ddof=0): the values are all matched pairs, not a sample
    return {
        'mean': float(np.mean(values)),
        'median': float(np.median(values)),
        'min': float(np.min(values)),
        'max': float(np.max(values)),
        'std': float(np.std(values, ddof=0)),
    }


def match_and_evaluate(lda1, lda2, vocab1, vocab2, top_n=20, shared_vocabulary=False):
    """Match the topics of two models one-to-one and compare the matched pairs.

    Args:
        lda1, lda2: fitted LDA models with the same number of topics
        vocab1, vocab2: their vocabularies (identical, unless shared_vocabulary is True)
        top_n: number of top words for the Jaccard overlap
        shared_vocabulary: if True, the models may have different vocabularies and cosine is computed over
                           the words both contain (Gordon's alignment of period models). Jaccard always
                           compares the top words of the full distributions.

    Returns:
        matches: [(topic index 1, topic index 2, cosine, jaccard)]
        summary_stats: {'cosine': {...}, 'jaccard_top<n>': {...}} with mean, median, min, max, std
        similarity_matrix: (n_topics1 x n_topics2) cosine similarities
    """
    if not isinstance(top_n, int) or top_n <= 0:
        raise ValueError(f"top_n must be a positive integer, got {top_n}")
    if not hasattr(lda1, 'components_') or not hasattr(lda2, 'components_'):
        raise ValueError("Both models must be fitted LDA instances with components_ attribute")
    n_topics1, n_topics2 = lda1.components_.shape[0], lda2.components_.shape[0]
    if n_topics1 != n_topics2:
        raise ValueError(f"Models must have the same number of topics, got {n_topics1} vs {n_topics2}")

    if shared_vocabulary:
        shared1, shared2, shared_vocab = restrict_to_shared_vocabulary(lda1, lda2, vocab1, vocab2)
        similarity_matrix = compute_topic_similarity_matrix(shared1, shared2, shared_vocab, shared_vocab)
    else:
        similarity_matrix = compute_topic_similarity_matrix(lda1, lda2, vocab1, vocab2)

    pairs = match_topics_hungarian(similarity_matrix)
    jaccard = compute_topword_jaccard(lda1, lda2, vocab1, vocab2, [(t1, t2) for t1, t2, _ in pairs], top_n)
    matches = [(t1, t2, cosine, jaccard[(t1, t2)]) for t1, t2, cosine in pairs]
    summary_stats = {
        'cosine': summary([m[2] for m in matches]),
        f'jaccard_top{top_n}': summary([m[3] for m in matches]),
    }
    return matches, summary_stats, similarity_matrix
