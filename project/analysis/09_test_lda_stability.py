#!/usr/bin/env python3
"""
Corrected seed-stability test for 44-topic baseline LDA model.

Uses Hungarian algorithm to optimally match topics between models before
computing stability metrics, accounting for arbitrary topic indices.
"""

import json
import numpy as np
from pathlib import Path
import sys
from itertools import combinations

from topic_matching import match_and_evaluate

try:
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    import pickle
except ImportError:
    print("Error: scikit-learn not installed. Install with: pip install scikit-learn")
    sys.exit(1)


def load_text(input_dir, text_field='text_no_stopwords'):
    """Load text from all temporal bins.

    Args:
        input_dir: Directory containing group*.jsonl files
        text_field: Which text field to load. Must match the field used to fit baseline model.
                   (default 'text_no_stopwords' for 44-topic baseline)
    """
    print(f"Loading {text_field} from all bins...")
    texts = []
    total_motions = 0
    malformed_count = 0

    for bin_file in sorted(input_dir.glob('group*.jsonl')):
        print(f"  Loading {bin_file.name}...")
        with open(bin_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    motion = json.loads(line.strip())
                    text = motion.get(text_field, '')
                    if text:
                        texts.append(text)
                        total_motions += 1
                except json.JSONDecodeError:
                    malformed_count += 1
                    continue

    print(f"Loaded {total_motions} motions")
    if malformed_count > 0:
        print(f"⚠️  Warning: {malformed_count} malformed JSON lines skipped")
    return texts


def load_vectorizer_and_transform(vectorizer_path, texts):
    """Load baseline vectorizer and transform texts (exact reproduction pipeline).

    Loading the saved baseline vectorizer ensures exact vocabulary match with
    trained baseline model.
    """
    print("Loading baseline vectorizer...")
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    vocab = vectorizer.get_feature_names_out()
    print(f"Vocabulary size: {len(vocab)} unique tokens")

    print("Transforming texts with baseline vectorizer...")
    doc_term_matrix = vectorizer.transform(texts)
    print(f"Document-term matrix shape: {doc_term_matrix.shape}")
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
    # ========== CONFIGURATION ==========
    NUM_TOPICS = 44  # Change this to match the baseline model
    SEEDS = [42, 123, 456, 789, 999]
    # ==================================

    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'deduplicated'
    BASELINE_VECTORIZER_PATH = PROJECT_ROOT / 'models' / 'baseline_lda_44' / 'baseline_vectorizer.pkl'
    RESULTS_DIR = PROJECT_ROOT / 'results'
    OUTPUT_FILE = RESULTS_DIR / f'BASELINE_STABILITY_{NUM_TOPICS}TOPICS_CORRECTED.md'

    print("=" * 80)
    print(f"Corrected Seed-Stability Test: {NUM_TOPICS}-Topic Baseline LDA")
    print(f"Seeds: {SEEDS}")
    print(f"Input: {INPUT_DIR}")
    print("=" * 80)

    # Load data once (using text_no_stopwords to match 44-topic baseline model)
    print("\n1. Loading text...")
    texts = load_text(INPUT_DIR, text_field='text_no_stopwords')
    if not texts:
        print("Error: No texts loaded")
        sys.exit(1)
    print(f"   Loaded {len(texts)} documents")

    # Load baseline vectorizer
    print("\n2. Loading baseline vectorizer (exact reproduction)...")
    if not BASELINE_VECTORIZER_PATH.exists():
        print(f"Error: Baseline vectorizer not found at {BASELINE_VECTORIZER_PATH}")
        sys.exit(1)
    vectorizer, doc_term_matrix = load_vectorizer_and_transform(BASELINE_VECTORIZER_PATH, texts)
    vocab = vectorizer.get_feature_names_out()

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
        f"# Corrected Seed-Stability Analysis: {num_topics}-Topic Baseline LDA",
        "",
        "## Methodology",
        "",
        "**Key fix:** Topics are optimally matched across models using the Hungarian algorithm,",
        "accounting for the fact that topic indices are arbitrary across LDA runs.",
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
        "## Key Change from Previous Analysis",
        "",
        "Previous reports compared Topic 1 to Topic 1, Topic 2 to Topic 2, etc. across seeds.",
        "This is methodologically invalid because topic indices are arbitrary.",
        "",
        "This corrected analysis uses the Hungarian algorithm to find optimal topic correspondences",
        "before computing similarities. The previous mean Jaccard value of ~0.02 reflected",
        "invalid index-by-index comparison. The values above reflect matched topics.",
    ])

    return '\n'.join(report_lines)


if __name__ == '__main__':
    main()
