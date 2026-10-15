#!/usr/bin/env python3
"""
Corrected seed-stability test for 3x title-weighted LDA model.

Uses Hungarian algorithm to optimally match topics between models before
computing stability metrics, accounting for arbitrary topic indices.
"""

import json
import pickle
import numpy as np
from pathlib import Path
import sys
from itertools import combinations

from topic_matching import match_and_evaluate

try:
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
except ImportError:
    print("Error: scikit-learn not installed")
    sys.exit(1)


def load_text_with_titles_3x(input_dir):
    """Load text with 3x title weighting - matches weighted LDA fitting pipeline.

    Reproduces the exact preprocessing from 10_fit_title_weighted_lda.py:
    - Uses text_lemmatized (same as baseline)
    - Uses title_processed (preprocessed titles)
    - Appends title three additional times (3x replication)
    """
    texts = []
    metadata = []
    malformed_count = 0

    for bin_file in sorted(input_dir.glob('group*.jsonl')):
        with open(bin_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    motion = json.loads(line.strip())
                    text = motion.get('text_lemmatized', '')
                    title = motion.get('title_processed', '')

                    # Create weighted document: body + (title * 3 additional copies)
                    if title and title.strip():
                        weighted_text = text + ' ' + (' '.join(title.split()) + ' ') * 3
                    else:
                        weighted_text = text

                    if weighted_text.strip():
                        texts.append(weighted_text)
                        metadata.append({
                            'doc_id': motion.get('dok_id', 'unknown'),
                            'title': motion.get('title', ''),
                            'year': motion.get('date', '')[:4] if motion.get('date') else 'unknown'
                        })
                except json.JSONDecodeError:
                    malformed_count += 1
                    continue

    if malformed_count > 0:
        print(f"⚠️  {malformed_count} malformed JSON lines skipped")

    return texts, metadata


def create_vectorizer_and_corpus(texts):
    """Create CountVectorizer and fit once."""
    vectorizer = CountVectorizer(
        max_df=0.5,
        min_df=5,
        max_features=10000,
        stop_words=None,
    )
    doc_term_matrix = vectorizer.fit_transform(texts)
    return vectorizer, doc_term_matrix


def fit_lda_model(doc_term_matrix, num_topics, random_seed, max_iter=50):
    """Fit LDA model with given random seed."""
    lda = LatentDirichletAllocation(
        n_components=num_topics,
        random_state=random_seed,
        max_iter=max_iter,
        learning_method='online',
        n_jobs=2,
        verbose=0,
    )
    lda.fit(doc_term_matrix)
    return lda


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'deduplicated'
    BASELINE_VECTORIZER_PATH = PROJECT_ROOT / 'models' / 'baseline_lda_44' / 'baseline_vectorizer.pkl'
    RESULTS_DIR = PROJECT_ROOT / 'results'
    OUTPUT_FILE = RESULTS_DIR / 'SEED_STABILITY_3X_WEIGHTED_CORRECTED.md'

    NUM_TOPICS = 44
    SEEDS = [42, 123, 456, 789, 999]

    print("=" * 80)
    print(f"Corrected Seed-Stability Test: 3x Title-Weighted LDA (44 topics)")
    print(f"Seeds: {SEEDS}")
    print("=" * 80)

    # Load data with 3x title weighting (exact pipeline: deduplicated + text_lemmatized + title_processed 3x)
    print("\n1. Loading text with 3x title weighting...")
    texts, metadata = load_text_with_titles_3x(INPUT_DIR)
    print(f"   Loaded {len(texts)} documents")

    if not texts:
        print("Error: No texts loaded")
        sys.exit(1)

    # Load baseline vectorizer (ensures weighted model uses exact same vocabulary as baseline)
    print("\n2. Loading baseline vectorizer (shared vocabulary)...")
    import pickle
    with open(BASELINE_VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
    vocab = vectorizer.get_feature_names_out()
    print(f"   Vocabulary size: {len(vocab)} unique tokens")

    # Transform texts using baseline vectorizer
    print("   Transforming documents...")
    doc_term_matrix = vectorizer.transform(texts)

    # Fit models with different seeds
    print(f"\n3. Fitting {len(SEEDS)} LDA models with different seeds...")
    models_by_seed = {}
    for seed in SEEDS:
        print(f"   Seed {seed}...")
        lda = fit_lda_model(doc_term_matrix, NUM_TOPICS, seed)
        models_by_seed[seed] = lda
        perplexity = lda.perplexity(doc_term_matrix)
        print(f"     Perplexity: {perplexity:.2f}, Iterations: {lda.n_iter_}")

    # Compute all pairwise matches
    print(f"\n4. Computing pairwise topic matching ({len(list(combinations(SEEDS, 2)))} pairs)...")
    seed_pairs = list(combinations(SEEDS, 2))
    pairwise_results = {}

    for seed1, seed2 in seed_pairs:
        print(f"   Seeds {seed1} vs {seed2}...")
        lda1 = models_by_seed[seed1]
        lda2 = models_by_seed[seed2]

        matches, summary, similarity_matrix = match_and_evaluate(lda1, lda2, vocab, vocab, top_n=20)
        pairwise_results[(seed1, seed2)] = {
            'matches': matches,
            'summary': summary,
            'similarity_matrix': similarity_matrix
        }

    # Generate report
    print(f"\n5. Generating report...")
    report = generate_report(pairwise_results, seed_pairs, NUM_TOPICS)

    # Save report
    RESULTS_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✅ Report saved to: {OUTPUT_FILE}")
    print("=" * 80)


def generate_report(pairwise_results, seed_pairs, num_topics):
    """Generate comprehensive markdown report."""
    report_lines = [
        "# Corrected Seed-Stability Analysis: 3x Title-Weighted LDA (44 topics)",
        "",
        "## Methodology",
        "",
        "**Key fix:** Topics are optimally matched across models using the Hungarian algorithm,",
        "accounting for the fact that topic indices are arbitrary across LDA runs.",
        "",
        "**Weighting:** Title words are appended three additional times to body text",
        "",
        "**Matching criterion:** Cosine similarity over normalized topic-word distributions",
        "",
        "**Secondary metric:** Jaccard overlap of top 20 words (for interpretability)",
        "",
        "## Pairwise Comparisons",
        "",
    ]

    # Collect all cosine and jaccard values for overall stats
    all_cosine_sims = []
    all_jaccard_sims = []

    for seed1, seed2 in seed_pairs:
        result = pairwise_results[(seed1, seed2)]
        matches = result['matches']
        summary = result['summary']

        cosine_stats = summary['cosine']
        # Find the Jaccard key (jaccard_top20, etc.)
        jaccard_key = [k for k in summary.keys() if k.startswith('jaccard_')][0]
        jaccard_stats = summary[jaccard_key]

        # Collect for overall stats
        all_cosine_sims.extend([m[2] for m in matches])
        all_jaccard_sims.extend([m[3] for m in matches])

        # Extract top_n from key (e.g., 'jaccard_top20' -> 20)
        top_n = int(jaccard_key.split('top')[1])

        report_lines.extend([
            f"### Seed {seed1} vs Seed {seed2}",
            "",
            f"**Cosine Similarity (full topic distributions):**",
            f"- Mean: {cosine_stats['mean']:.4f}",
            f"- Median: {cosine_stats['median']:.4f}",
            f"- Min: {cosine_stats['min']:.4f}",
            f"- Max: {cosine_stats['max']:.4f}",
            f"- Std Dev: {cosine_stats['std']:.4f}",
            "",
            f"**Jaccard Similarity (top {top_n} words):**",
            f"- Mean: {jaccard_stats['mean']:.4f}",
            f"- Median: {jaccard_stats['median']:.4f}",
            f"- Min: {jaccard_stats['min']:.4f}",
            f"- Max: {jaccard_stats['max']:.4f}",
            f"- Std Dev: {jaccard_stats['std']:.4f}",
            "",
        ])

    # Overall summary statistics
    report_lines.extend([
        "## Overall Summary Statistics",
        "",
        f"**Total seed pairs tested:** {len(seed_pairs)}",
        f"**Total matched topic pairs:** {len(all_cosine_sims)}",
        "",
        "### Cosine Similarity (across all matches)",
        f"- Mean: {np.mean(all_cosine_sims):.4f}",
        f"- Median: {np.median(all_cosine_sims):.4f}",
        f"- Min: {np.min(all_cosine_sims):.4f}",
        f"- Max: {np.max(all_cosine_sims):.4f}",
        f"- Std Dev: {np.std(all_cosine_sims):.4f}",
        "",
        "### Jaccard Similarity (across all matches)",
        f"- Mean: {np.mean(all_jaccard_sims):.4f}",
        f"- Median: {np.median(all_jaccard_sims):.4f}",
        f"- Min: {np.min(all_jaccard_sims):.4f}",
        f"- Max: {np.max(all_jaccard_sims):.4f}",
        f"- Std Dev: {np.std(all_jaccard_sims):.4f}",
        "",
        "## Comparison to Baseline",
        "",
        "Compare these values to the baseline 44-topic model to assess",
        "whether title weighting (three additional copies) improves topic stability across random seeds.",
    ])

    return '\n'.join(report_lines)


if __name__ == '__main__':
    main()
