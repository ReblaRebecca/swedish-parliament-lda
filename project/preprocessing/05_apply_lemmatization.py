#!/usr/bin/env python3
"""
Apply controlled lemmatization to stopword-removed text (STEP 4).
Uses manual lemmatization lookup table for Swedish education terminology.
Input: JSON lines with 'text_no_stopwords' field.
Output: JSON lines with 'text_lemmatized' field.
"""

import json
import csv
from pathlib import Path
import sys


def load_lemmatization_table(csv_file):
    """Load variant->lemma mappings from CSV file."""
    lemma_dict = {}

    if not csv_file.exists():
        print(f"Error: {csv_file} not found")
        sys.exit(1)

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            variant = row['variant'].strip()
            lemma = row['lemma'].strip()
            if variant and lemma:
                lemma_dict[variant] = lemma

    print(f"Loaded {len(lemma_dict)} lemmatization mappings")
    return lemma_dict


def apply_lemmatization(text, lemma_dict):
    """Apply lemmatization to text using controlled lookup table.

    Preserves line structure for reference/debugging.
    Returns: (lemmatized_text, token_count, replacement_count)
    """
    if not text or not lemma_dict:
        return text, 0, 0

    # Process line-by-line to preserve structure
    lines = text.split('\n')
    lemmatized_lines = []
    token_count = 0
    replacement_count = 0

    for line in lines:
        words = line.split()
        lemmatized_words = []
        for word in words:
            token_count += 1
            if word in lemma_dict:
                lemmatized_words.append(lemma_dict[word])
                replacement_count += 1
            else:
                lemmatized_words.append(word)
        lemmatized_lines.append(' '.join(lemmatized_words))

    return '\n'.join(lemmatized_lines), token_count, replacement_count


def process_temporal_bin(input_file, output_file, lemma_dict):
    """Process one temporal bin: apply lemmatization."""
    motion_count = 0
    malformed_count = 0
    total_tokens = 0
    total_replacements = 0

    print(f"Processing {input_file.name}...")

    with open(input_file, 'r', encoding='utf-8') as in_f:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for line in in_f:
                try:
                    motion = json.loads(line.strip())
                except json.JSONDecodeError:
                    malformed_count += 1
                    continue

                # Apply lemmatization to stopword-removed text
                text = motion.get('text_no_stopwords', '')
                text_lemmatized, token_count, replacement_count = apply_lemmatization(text, lemma_dict)
                total_tokens += token_count
                total_replacements += replacement_count

                # Add lemmatized text to motion
                motion['text_lemmatized'] = text_lemmatized

                # Write to output
                out_f.write(json.dumps(motion, ensure_ascii=False) + '\n')
                motion_count += 1

                if motion_count % 1000 == 0:
                    print(f"  Processed {motion_count} motions...")

    print(f"  Completed: {motion_count} motions, {malformed_count} malformed JSON skipped")
    return motion_count, malformed_count, total_tokens, total_replacements


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    # Allow command-line arguments for input/output directories and lemmatization file
    # Usage: python3 05_apply_lemmatization.py [input_dir] [output_dir] [lemmatization_csv]
    # Default: data/output/stopword_removed -> data/output/lemmatized with config/controlled_lemmatization.csv
    if len(sys.argv) >= 3:
        INPUT_DIR = Path(sys.argv[1])
        OUTPUT_DIR = Path(sys.argv[2])
        LEMMATIZATION_FILE = Path(sys.argv[3]) if len(sys.argv) >= 4 else PROJECT_ROOT / 'config' / 'controlled_lemmatization.csv'
    else:
        INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'
        OUTPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'lemmatized'
        LEMMATIZATION_FILE = PROJECT_ROOT / 'config' / 'controlled_lemmatization.csv'

    # Load lemmatization table
    print("Loading controlled lemmatization table...")
    lemma_dict = load_lemmatization_table(LEMMATIZATION_FILE)

    # Create output directory (with parents in case path doesn't exist)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Define temporal bins
    bins = [
        ('group1_1986-1993.jsonl', 'group1_1986-1993.jsonl'),
        ('group2_1994-2004.jsonl', 'group2_1994-2004.jsonl'),
        ('group3_2005-2014.jsonl', 'group3_2005-2014.jsonl'),
        ('group4_2015-2025.jsonl', 'group4_2015-2025.jsonl'),
    ]

    total_motions = 0
    total_malformed = 0
    total_tokens = 0
    total_replacements = 0

    print("=" * 60)
    print("STEP 4: Applying controlled lemmatization")
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Lemmatization file: {LEMMATIZATION_FILE}")
    print("=" * 60)

    for input_filename, output_filename in bins:
        input_file = INPUT_DIR / input_filename
        output_file = OUTPUT_DIR / output_filename

        if not input_file.exists():
            print(f"Error: {input_file} not found")
            continue

        count, malformed, tokens, replacements = process_temporal_bin(input_file, output_file, lemma_dict)
        total_motions += count
        total_malformed += malformed
        total_tokens += tokens
        total_replacements += replacements

    print("=" * 60)
    print(f"Total: {total_motions} motions processed")
    if total_malformed > 0:
        print(f"⚠️  Warning: {total_malformed} malformed JSON lines skipped")

    # Report lemmatization statistics
    replacement_rate = (100 * total_replacements / total_tokens) if total_tokens > 0 else 0
    print(f"Lemmatization: {total_replacements:,} replacements / {total_tokens:,} tokens ({replacement_rate:.2f}%)")

    print(f"Output saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
