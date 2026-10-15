#!/usr/bin/env python3
"""
⚠️  DEPRECATED: This script has methodological issues and should not be used.

Issues:
- Coherence metric lacks justification and is not validated
- Median calculation is incorrect for even-length arrays (uses floor instead of proper median)
- Category thresholds (high/medium/low) are defined but unsupported
- Title weighting specification ("3x") may not match actual model
- Does not use proper seed-stability evaluation (see topic_matching.py)

Use topic_matching.py with Hungarian algorithm-based stability testing instead.
"""

import csv
from pathlib import Path
import math


def calculate_coherence(top_words, word_probs):
    """Calculate entropy-based coherence for a topic.

    ⚠️  DEPRECATED: This metric lacks validation and peer-reviewed justification.
    Use proper coherence metrics from literature or stability testing instead.

    Coherence = 1 - (H / log(n))
    where H = Shannon entropy of top word probabilities
    """
    if len(top_words) < 2 or sum(word_probs) == 0:
        return 0.0

    # Normalize probabilities
    total_prob = sum(word_probs)
    probs = [p / total_prob for p in word_probs]

    # Calculate Shannon entropy
    entropy = 0.0
    for p in probs:
        if p > 0:
            entropy -= p * math.log(p)

    # Normalize by max possible entropy
    max_entropy = math.log(len(top_words))
    if max_entropy == 0:
        return 0.0

    # Coherence = 1 - normalized entropy
    coherence = 1.0 - (entropy / max_entropy)
    return max(0.0, coherence)


def load_lda_topics(topics_csv):
    """Load topics from CSV file (handles both baseline and weighted formats)."""
    topics = {}
    with open(topics_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Handle both "Topic 1" and "1" formats
            topic_str = row['topic'].replace('Topic ', '').strip()
            topic_id = int(topic_str)
            words = []
            probs = []
            for i in range(1, 21):
                word_col = f'word_{i}'
                prob_col = f'prob_{i}'
                if word_col in row and prob_col in row:
                    word = row[word_col].strip()
                    try:
                        prob = float(row[prob_col])
                    except (ValueError, TypeError):
                        continue
                    if word:
                        words.append(word)
                        probs.append(prob)
            topics[topic_id] = {'words': words, 'probs': probs}
    return topics


def calculate_coherence_scores(topics):
    """Calculate coherence for all topics."""
    scores = {}
    for topic_id, data in topics.items():
        coherence = calculate_coherence(data['words'], data['probs'])
        scores[topic_id] = coherence
    return scores


def analyze_coherence_distribution(scores):
    """Analyze coherence score distribution."""
    high = [score for score in scores.values() if score > 0.15]
    medium = [score for score in scores.values() if 0.08 <= score <= 0.15]
    low = [score for score in scores.values() if score < 0.08]

    avg = sum(scores.values()) / len(scores) if scores else 0
    sorted_scores = sorted(scores.values())
    if not sorted_scores:
        median = 0.0
    elif len(sorted_scores) % 2 == 1:
        # Odd number of elements
        median = sorted_scores[len(sorted_scores) // 2]
    else:
        # Even number of elements: average the two middle values
        mid1 = len(sorted_scores) // 2 - 1
        mid2 = len(sorted_scores) // 2
        median = (sorted_scores[mid1] + sorted_scores[mid2]) / 2.0
    min_score = min(scores.values()) if scores else 0
    max_score = max(scores.values()) if scores else 0

    return {
        'average': avg,
        'median': median,
        'min': min_score,
        'max': max_score,
        'high_count': len(high),
        'medium_count': len(medium),
        'low_count': len(low),
        'total': len(scores),
    }


def main():
    print("\n" + "=" * 70)
    print("❌ DEPRECATED: This script has methodological issues and is disabled.")
    print("=" * 70)
    print("\nIssues:")
    print("- Coherence metric lacks justification and is not validated")
    print("- Median calculation is incorrect for even-length arrays")
    print("- Category thresholds are unsupported")
    print("- Does not use proper seed-stability evaluation")
    print("\nUse instead:")
    print("  analysis/09_test_lda_stability.py       (baseline stability)")
    print("  analysis/13_seed_stability_5x_weighted.py (weighted stability)")
    print("  analysis/topic_matching.py              (Hungarian matching)")
    print("=" * 70 + "\n")
    import sys
    sys.exit(1)

    # Configuration (unreachable, preserved for reference)
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    BASELINE_TOPICS_CSV = PROJECT_ROOT / 'results' / '44_TOPICS_FINAL.csv'
    WEIGHTED_TOPICS_CSV = PROJECT_ROOT / 'results' / 'weighted_44_TOPICS_FINAL.csv'

    if not BASELINE_TOPICS_CSV.exists():
        print(f"Error: {BASELINE_TOPICS_CSV} not found")
        return

    print("=" * 70)
    print("COHERENCE COMPARISON: Baseline vs Title-Weighted LDA (44 topics)")
    print("=" * 70)

    # Load topics
    baseline_topics = load_lda_topics(BASELINE_TOPICS_CSV)
    baseline_scores = calculate_coherence_scores(baseline_topics)
    baseline_dist = analyze_coherence_distribution(baseline_scores)

    print("\n[BASELINE MODEL]")
    print(f"  Average Coherence: {baseline_dist['average']:.4f}")
    print(f"  Median Coherence:  {baseline_dist['median']:.4f}")
    print(f"  Min Coherence:     {baseline_dist['min']:.4f}")
    print(f"  Max Coherence:     {baseline_dist['max']:.4f}")
    print(f"  Distribution:")
    print(f"    High (>0.15):    {baseline_dist['high_count']} topics")
    print(f"    Medium (0.08-0.15): {baseline_dist['medium_count']} topics")
    print(f"    Low (<0.08):     {baseline_dist['low_count']} topics")

    # Check if weighted model exists
    if WEIGHTED_TOPICS_CSV.exists():
        weighted_topics = load_lda_topics(WEIGHTED_TOPICS_CSV)
        weighted_scores = calculate_coherence_scores(weighted_topics)
        weighted_dist = analyze_coherence_distribution(weighted_scores)

        print("\n[WEIGHTED MODEL (5x title replication)]")
        print(f"  Average Coherence: {weighted_dist['average']:.4f}")
        print(f"  Median Coherence:  {weighted_dist['median']:.4f}")
        print(f"  Min Coherence:     {weighted_dist['min']:.4f}")
        print(f"  Max Coherence:     {weighted_dist['max']:.4f}")
        print(f"  Distribution:")
        print(f"    High (>0.15):    {weighted_dist['high_count']} topics")
        print(f"    Medium (0.08-0.15): {weighted_dist['medium_count']} topics")
        print(f"    Low (<0.08):     {weighted_dist['low_count']} topics")

        # Comparison
        print("\n[COMPARISON: Weighted vs Baseline]")
        avg_change = weighted_dist['average'] - baseline_dist['average']
        avg_pct = 100 * avg_change / baseline_dist['average'] if baseline_dist['average'] > 0 else 0
        print(f"  Average Coherence: {avg_change:+.4f} ({avg_pct:+.1f}%)")

        median_change = weighted_dist['median'] - baseline_dist['median']
        median_pct = 100 * median_change / baseline_dist['median'] if baseline_dist['median'] > 0 else 0
        print(f"  Median Coherence:  {median_change:+.4f} ({median_pct:+.1f}%)")

        # High quality topics
        high_change = weighted_dist['high_count'] - baseline_dist['high_count']
        print(f"  High-Quality Topics: {high_change:+d} ({weighted_dist['high_count']}/{baseline_dist['total']})")

        print("\n✓ Comparison complete")
    else:
        print(f"\n⚠️  Weighted model topics not yet generated at {WEIGHTED_TOPICS_CSV}")

    print("=" * 70)


if __name__ == '__main__':
    main()
