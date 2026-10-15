#!/usr/bin/env python3
"""
Normalize lemmatized motion text: lowercase, remove numbers and punctuation (STEP 4).
Works on lemmatized text (one sentence per line), preserves line structure.
Input: JSON lines with 'text_lemmatized' field.
Output: JSON lines with 'text_normalized' field.
"""

import json
import re
from pathlib import Path
import sys


def normalize_text(text):
    """Normalize text: lowercase, remove numbers/punctuation, clean whitespace.

    Preserves line breaks for structure.
    Removes single-character words (OCR artifacts).
    """
    if not text:
        return ""

    # Lowercase
    text = text.lower()

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Remove punctuation but keep spaces and newlines
    text = re.sub(r'[^\w\s\n]', ' ', text)

    # Remove extra whitespace on each line but preserve line breaks
    lines = text.split('\n')
    normalized_lines = []
    for line in lines:
        # Clean whitespace
        line = re.sub(r'\s+', ' ', line).strip()
        # Remove single-character words (OCR artifacts, encoding errors)
        words = [w for w in line.split() if len(w) > 1]
        cleaned_line = ' '.join(words)
        if cleaned_line:
            normalized_lines.append(cleaned_line)

    return '\n'.join(normalized_lines)


def process_temporal_bin(input_file, output_file):
    """Process one temporal bin: normalize text."""
    motion_count = 0
    malformed_count = 0

    print(f"Processing {input_file.name}...")

    with open(input_file, 'r', encoding='utf-8') as in_f:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for line in in_f:
                try:
                    motion = json.loads(line.strip())
                except json.JSONDecodeError:
                    malformed_count += 1
                    continue

                # Normalize lemmatized text
                text_normalized = normalize_text(motion.get('text_lemmatized', ''))

                # Add normalized text to motion
                motion['text_normalized'] = text_normalized

                # Write to output
                out_f.write(json.dumps(motion, ensure_ascii=False) + '\n')
                motion_count += 1

                if motion_count % 1000 == 0:
                    print(f"  Processed {motion_count} motions...")

    print(f"  Completed: {motion_count} motions, {malformed_count} malformed JSON skipped")
    return motion_count, malformed_count


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    # Allow command-line arguments for input/output directories
    # Usage: python3 04_normalize_text.py [input_dir] [output_dir]
    # Default: data/output/lemmatized -> data/output/normalized
    if len(sys.argv) >= 3:
        INPUT_DIR = Path(sys.argv[1])
        OUTPUT_DIR = Path(sys.argv[2])
    else:
        INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'lemmatized'
        OUTPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'normalized'

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

    print("=" * 60)
    print("STEP 4: Normalizing lemmatized text")
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    for input_filename, output_filename in bins:
        input_file = INPUT_DIR / input_filename
        output_file = OUTPUT_DIR / output_filename

        if not input_file.exists():
            print(f"Error: {input_file} not found")
            continue

        count, malformed = process_temporal_bin(input_file, output_file)
        total_motions += count
        total_malformed += malformed

    print("=" * 60)
    print(f"Total: {total_motions} motions processed")
    if total_malformed > 0:
        print(f"⚠️  Warning: {total_malformed} malformed JSON lines skipped")
    print(f"Output saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
