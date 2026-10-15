#!/usr/bin/env python3
"""
Preprocess motion titles using the same pipeline as body text.
Apply boilerplate removal, Stanza lemmatization, normalization and stopword removal,
reusing the functions from preprocessing steps 02-05 so titles and bodies are treated identically.
Store processed titles separately for weighting experiment.

Input: Raw titles from deduplicated/ JSONL files
Output: Processed titles in deduplicated/ files (new 'title_processed' field)
"""

import importlib.util
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def load_step(module_name, filename):
    """Import a pipeline step module (filenames start with digits, so plain import is not possible)."""
    spec = importlib.util.spec_from_file_location(module_name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


boilerplate_step = load_step('remove_boilerplate', '02_remove_boilerplate.py')
lemmatize_step = load_step('lemmatize', '03_lemmatize.py')
normalize_step = load_step('normalize_text', '04_normalize_text.py')
stopword_step = load_step('remove_stopwords', '05_remove_stopwords.py')


def process_titles(titles, boilerplate_patterns, nlp, stopwords):
    """Process a batch of titles through the full body-text pipeline."""
    without_boilerplate = [boilerplate_step.remove_boilerplate(t, boilerplate_patterns) for t in titles]
    lemmatized = lemmatize_step.lemmatize_texts(nlp, without_boilerplate)

    processed = []
    for text in lemmatized:
        text = normalize_step.normalize_text(text)
        text = stopword_step.remove_stopwords(text, stopwords)
        processed.append(' '.join(text.split()))
    return processed


def process_temporal_bin(input_file, output_file, boilerplate_patterns, nlp, stopwords):
    """Process titles for one temporal bin. Read entire file first to avoid truncation."""
    empty_titles = 0

    print(f"Processing {input_file.name}...")

    # Read all lines first (avoid truncation when output_file == input_file)
    motions = []
    with open(input_file, 'r', encoding='utf-8') as in_f:
        for line in in_f:
            try:
                motions.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue

    titles = [motion.get('title', '') or '' for motion in motions]
    processed = []
    for start in range(0, len(titles), lemmatize_step.BATCH_SIZE * 8):
        processed.extend(process_titles(titles[start:start + lemmatize_step.BATCH_SIZE * 8], boilerplate_patterns, nlp, stopwords))
        print(f"  Processed {len(processed)}/{len(titles)} titles...")

    # Write all motions with processed titles
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for motion, title_processed in zip(motions, processed):
            if not title_processed:
                empty_titles += 1
            motion['title_processed'] = title_processed
            out_f.write(json.dumps(motion, ensure_ascii=False) + '\n')

    print(f"  Completed: {len(motions)} motions, {empty_titles} empty titles")
    return len(motions), empty_titles


def main():
    # Configuration
    PROJECT_ROOT = SCRIPT_DIR.parent

    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'deduplicated'
    OUTPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'deduplicated'

    # Load preprocessing resources (same as body pipeline)
    print("Loading boilerplate, Stanza pipeline and stopwords...")
    boilerplate_patterns = boilerplate_step.load_boilerplate_phrases(PROJECT_ROOT / 'config' / 'boilerplate_phrases.txt')
    nlp = lemmatize_step.load_pipeline()
    stopwords = stopword_step.get_swedish_stopwords()

    print(f"  Boilerplate: {len(boilerplate_patterns)} phrases")
    print(f"  Stopwords: {len(stopwords)} words")

    # Define temporal bins
    bins = [
        'group1_1986-1993.jsonl',
        'group2_1994-2004.jsonl',
        'group3_2005-2014.jsonl',
        'group4_2015-2025.jsonl',
    ]

    total_motions = 0
    total_empty = 0

    print("\n" + "=" * 60)
    print("PREPROCESSING MOTION TITLES")
    print(f"Input: {INPUT_DIR}")
    print("=" * 60)

    for bin_file in bins:
        input_file = INPUT_DIR / bin_file
        output_file = OUTPUT_DIR / bin_file

        if not input_file.exists():
            print(f"Error: {input_file} not found")
            continue

        count, empty = process_temporal_bin(input_file, output_file, boilerplate_patterns, nlp, stopwords)
        total_motions += count
        total_empty += empty

    print("=" * 60)
    print(f"Total: {total_motions} motions processed")
    if total_motions > 0:
        print(f"Empty titles after processing: {total_empty} ({100*total_empty/total_motions:.2f}%)")
    else:
        print(f"⚠️  Warning: No motions processed")
    print(f"Output saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
