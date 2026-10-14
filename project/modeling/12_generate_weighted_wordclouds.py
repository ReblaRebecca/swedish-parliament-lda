#!/usr/bin/env python3
"""
Generate weighted LDA word cloud visualization using baseline HTML template.
Reuses exact structure, CSS, and JavaScript from baseline with updated data.
"""

import csv
import json
import math
from pathlib import Path
import sys



def calculate_topic_prevalence(doctopics_csv, num_topics):
    """Calculate mean prevalence (average document probability) for each topic."""
    prevalence = {i: [] for i in range(num_topics)}

    with open(doctopics_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for topic_num in range(1, num_topics + 1):
                col = f'topic_{topic_num}_prob'
                if col in row:
                    try:
                        prob = float(row[col])
                        prevalence[topic_num - 1].append(prob)
                    except (ValueError, TypeError):
                        pass

    # Calculate mean for each topic
    mean_prevalence = {}
    for topic_num, probs in prevalence.items():
        if probs:
            mean_prevalence[topic_num] = sum(probs) / len(probs)
        else:
            mean_prevalence[topic_num] = 0.0

    return mean_prevalence


def load_topics_with_concentration(csv_path, prevalence_dict=None):
    """Load weighted topics and calculate top-20 probability concentration.

    Concentration measures how probability mass is distributed among the top 20 words.
    High concentration (near 1.0) = a few words dominate the topic.
    Low concentration (near 0.0) = probability distributed evenly among top 20.
    This is NOT full-topic entropy (which would include all vocabulary).

    prevalence_dict: optional dict mapping topic_num to mean prevalence value
    """
    topics = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            topic_str = row['topic'].replace('Topic ', '').strip()
            topic_id = int(topic_str)
            words = []

            # Load top 20 words (or until empty)
            for i in range(1, 21):
                word = row[f'word_{i}'].strip()
                prob_str = row[f'prob_{i}']
                if word:
                    try:
                        # Probabilities are already P(word|topic), properly normalized in the CSV
                        prob = float(prob_str)
                        words.append({"text": word, "p": prob})
                    except (ValueError, TypeError):
                        pass

            if not words:
                continue

            # Use probabilities as-is (already P(word|topic), sum ≈ 1.0 within full vocabulary)
            # Do NOT re-normalize to top-20 only, as that changes their meaning
            normalized_words = words

            # Calculate entropy concentration (NOT semantic coherence)
            # Top-20 probability concentration: entropy of top-20 words relative to each other
            # Measures how concentrated probability is among the top 20 (vs uniform distribution)
            # NOT semantic coherence; NOT full-topic entropy (which would need all vocabulary)
            probs_only = [w['p'] for w in normalized_words]

            if probs_only and len(probs_only) > 1:
                # Normalize top-20 probabilities to sum to 1 for valid entropy calculation
                top20_total = sum(probs_only)
                if top20_total > 0:
                    relative_probs = [p / top20_total for p in probs_only]
                    # Shannon entropy on the normalized top-20 distribution
                    entropy = -sum([p * math.log(p) for p in relative_probs if p > 0])
                    max_entropy = math.log(len(relative_probs))
                    concentration = 1.0 - (entropy / max_entropy) if max_entropy > 0 else 0
                    concentration = max(0, concentration)
                else:
                    concentration = 0.0
            else:
                concentration = 0.0

            prevalence = prevalence_dict.get(topic_id - 1, 0) if prevalence_dict else 0
            topics.append({
                "num": topic_id,
                "title": f"Topic {topic_id}",
                "prevalence": f"{prevalence * 100:.2f}%",  # For display: "5.07%"
                "words": normalized_words,
                "concentration": concentration  # Renamed from "coherence" to be accurate
            })

    return topics


def load_motions(csv_path):
    """Load document-topic distributions and compute top 15 for each topic from complete corpus."""
    # First pass: load all data and compute top 15 for each topic
    all_data = []
    motions = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            topics_array = []
            topics_dict = {}
            for i in range(1, 45):
                col = f'topic_{i}_prob'
                if col in row:
                    try:
                        prob = float(row[col])
                    except (ValueError, TypeError):
                        prob = 0
                    topics_array.append(prob)
                    topics_dict[i-1] = prob
                else:
                    topics_array.append(0)

            # Find dominant topic
            dominant_topic = max(range(44), key=lambda i: topics_dict.get(i, 0)) + 1

            motion = {
                "doc_id": row['doc_id'],
                "title": row['title'],
                "year": row['year'],
                "topics": topics_array,
                "dominant_topic": dominant_topic
            }
            motions.append(motion)
            all_data.append((motion, topics_array))

    # Second pass: compute top 15 for each topic from complete corpus
    top_motions_by_topic = {}
    for topic_num in range(1, 45):
        # Sort all documents by probability for this topic
        sorted_docs = sorted(
            all_data,
            key=lambda x: x[1][topic_num - 1],  # Index into topics_array
            reverse=True
        )
        # Take top 15, include probability
        top_motions_by_topic[topic_num] = [
            {
                "doc_id": doc[0]["doc_id"],
                "title": doc[0]["title"],
                "year": doc[0]["year"],
                "prob": round(doc[1][topic_num - 1], 4)  # Probability for this topic
            }
            for doc in sorted_docs[:15]
        ]

    return motions, top_motions_by_topic


def filter_motions_by_dominant_topic(motions, num_topics=44, max_per_topic=15):
    """Filter motions to show only those where each topic is dominant.

    Returns a dict mapping topic_num -> list of up to max_per_topic motions
    where that topic is dominant.
    """
    # Group motions by dominant topic
    motions_by_topic = {i: [] for i in range(1, num_topics + 1)}
    for motion in motions:
        dominant = motion['dominant_topic']
        if dominant in motions_by_topic:
            motions_by_topic[dominant].append(motion)

    # Limit each topic to max_per_topic motions
    for topic_num in motions_by_topic:
        motions_by_topic[topic_num] = motions_by_topic[topic_num][:max_per_topic]

    return motions_by_topic


def generate_html(topics, motions, baseline_html_path, output_path, motions_by_dominant_topic=None, top_motions_by_topic=None):
    """Generate weighted HTML by injecting data into template."""

    # Always load from baseline template (not from any existing output)
    if not baseline_html_path.exists():
        print(f"Error: {baseline_html_path} not found (template)")
        return None
    with open(baseline_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find where to inject topMotionsByTopic (after motionData)
    inject_pos = html_content.find('const container = document.getElementById')
    if inject_pos == -1:
        print(f"Error: Could not find injection point in HTML")
        return None

    # Generate JSON for all data
    topics_json = json.dumps(topics, ensure_ascii=False, separators=(',', ': '))

    # Use filtered motions if provided, otherwise use all motions
    if motions_by_dominant_topic:
        flat_filtered = []
        for topic_num, topic_motions in motions_by_dominant_topic.items():
            flat_filtered.extend(topic_motions)
        motions_json = json.dumps(flat_filtered, ensure_ascii=False, separators=(',', ': '))
    else:
        motions_json = json.dumps(motions, ensure_ascii=False, separators=(',', ': '))

    # Generate topMotionsByTopic JSON
    if top_motions_by_topic:
        top_motions_json = json.dumps(top_motions_by_topic, ensure_ascii=True, separators=(',', ': '))
    else:
        top_motions_json = '{}'

    # Replace topicsData and motionData arrays in HTML
    new_html = html_content.replace(
        'const topicsData = [];',
        f'const topicsData = {topics_json};'
    ).replace(
        'let motionData = [];',
        f'let motionData = {motions_json};'
    ).replace(
        'const topMotionsByTopic = {};',
        f'const topMotionsByTopic = {top_motions_json};'
    )

    # Replace the sorting logic with precomputed top 15 from topMotionsByTopic
    # Also update the motion display to show title (year) — probability
    old_sort = '''const topMotionsList = motionData
    .map(m => ({...m, topicProb: m.topics[topic.num - 1] || 0}))
    .sort((a, b) => b.topicProb - a.topicProb)
    .filter((m, idx, arr) => arr.findIndex(x => x.title === m.title) === idx)
    .slice(0, 15);'''

    new_sort = '''const topMotionsList = topMotionsByTopic[topic.num] || [];'''

    new_html = new_html.replace(old_sort, new_sort)

    # Update motion display to show: Title (Year) — Probability
    old_display = 'li.textContent = m.title || \'(untitled)\';'
    new_display = 'li.textContent = (m.title || \'(untitled)\') + \' (\' + m.year + \') — \' + (m.prob || 0).toFixed(4);'
    new_html = new_html.replace(old_display, new_display)

    # Update badge to use "concentration" field instead of "coherence"
    new_html = new_html.replace(
        'badge.className = `coherence-badge ${getCoherenceClass(topic.coherence)}`;',
        'badge.className = `concentration-badge ${getConcentrationClass(topic.concentration)}`;'
    )
    new_html = new_html.replace(
        'badge.textContent = `${topic.coherence.toFixed(3)}`;',
        'badge.textContent = `${topic.concentration.toFixed(3)}`;'
    )
    new_html = new_html.replace(
        'function getCoherenceClass(score)',
        'function getConcentrationClass(score)'
    )

    # Remove duplicate .rotate() call in d3 wordcloud chain
    new_html = new_html.replace(
        '.rotate(d => d.rotate)\n    .rotate(d => d.rotate)',
        '.rotate(d => d.rotate)'
    )

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    return output_path


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    TOPICS_CSV = PROJECT_ROOT / 'results' / 'weighted_44_TOPICS_FINAL.csv'
    DOCTOPICS_CSV = PROJECT_ROOT / 'results' / 'document_topic_distribution.csv'
    BASELINE_HTML = PROJECT_ROOT / 'results' / 'topics_wordclouds.html'
    OUTPUT_HTML = PROJECT_ROOT / 'results' / 'weighted_topics_wordclouds.html'
    TOPIC_STATS_CSV = PROJECT_ROOT / 'results' / 'topic_statistics.csv'

    print("=" * 70)
    print("Generating Weighted LDA Word Cloud Visualization")
    print("=" * 70)

    if not TOPICS_CSV.exists():
        print(f"Error: {TOPICS_CSV} not found")
        sys.exit(1)

    if not DOCTOPICS_CSV.exists():
        print(f"Error: {DOCTOPICS_CSV} not found")
        sys.exit(1)

    if not BASELINE_HTML.exists():
        print(f"Error: {BASELINE_HTML} not found (template)")
        sys.exit(1)

    print("Calculating topic prevalence...")
    prevalence = calculate_topic_prevalence(DOCTOPICS_CSV, 44)
    print(f"  ✓ Calculated prevalence for 44 topics")

    print("Loading and normalizing topics...")
    topics = load_topics_with_concentration(TOPICS_CSV, prevalence)
    print(f"  ✓ Loaded {len(topics)} topics")

    print("Loading document-topic distributions...")
    all_motions, top_motions_by_topic = load_motions(DOCTOPICS_CSV)
    print(f"  ✓ Loaded {len(all_motions)} documents")
    print(f"  ✓ Computed top 15 motions for 44 topics (from complete corpus)")

    print("Filtering motions to show only dominant topics...")
    motions_by_topic = filter_motions_by_dominant_topic(all_motions, 44, 15)
    dominant_count = sum(len(m) for m in motions_by_topic.values())
    print(f"  ✓ Filtered to {dominant_count} dominant topic instances across {len([t for t in motions_by_topic.values() if t])} topics")

    # Flatten for HTML generation (motions are grouped per topic in the viz)
    motions = all_motions

    print("Generating HTML visualization from baseline template...")
    output_path = generate_html(topics, motions, BASELINE_HTML, OUTPUT_HTML, motions_by_topic, top_motions_by_topic)

    if output_path:
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"\n✅ Visualization saved to: {output_path}")
        print(f"   Size: {file_size_mb:.1f} MB")
        print(f"   Structure: Identical to baseline")
        print(f"   Topics: {len(topics)} weighted LDA with entropy concentration badges")
        print(f"   Motions: All {len(motions)} documents")
    else:
        print("Error: Could not generate HTML")
        sys.exit(1)

    # Save topic statistics CSV
    print(f"\nSaving topic statistics...")
    with open(TOPIC_STATS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['topic', 'mean_prevalence', 'concentration'])
        writer.writeheader()
        for topic in topics:
            writer.writerow({
                'topic': topic['num'],
                'mean_prevalence': topic['prevalence'],  # Already formatted as percentage
                'concentration': f"{topic['concentration']:.6f}"
            })
    print(f"✅ Topic statistics saved to: {TOPIC_STATS_CSV}")

    print("=" * 70)


if __name__ == '__main__':
    main()
