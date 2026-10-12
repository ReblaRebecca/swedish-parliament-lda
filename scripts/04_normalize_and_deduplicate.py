#!/usr/bin/env python3
"""
Normalize motion text and detect duplicates.
Final preprocessing step before LDA.
Input: JSON lines with boilerplate-removed text.
Output: JSON lines with normalized text and duplicate flags.
"""

import json
import re
import hashlib
from pathlib import Path
import sys


def normalize_text(text):
    """Normalize text: lowercase, remove numbers/punctuation, clean whitespace."""
    if not text:
        return ""

    # Lowercase
    text = text.lower()

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Remove punctuation but keep spaces
    text = re.sub(r'[^\w\s]', ' ', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def compute_hash(text):
    """Compute MD5 hash of text for duplicate detection."""
    if not text:
        return None
    return hashlib.md5(text.encode()).hexdigest()


def process_temporal_bin(input_file, output_file):
    """Process one temporal bin: normalize and detect duplicates."""
    motion_count = 0
    duplicates = {}
    duplicate_count = 0

    print(f"Processing {input_file.name}...")

    with open(input_file, 'r', encoding='utf-8') as in_f:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for line in in_f:
                try:
                    motion = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue

                # Normalize text from boilerplate-removed version
                text = motion.get('text_no_boilerplate', '')
                text_normalized = normalize_text(text)

                # Compute hash for duplicate detection
                text_hash = compute_hash(text_normalized)

                # Check if duplicate
                is_duplicate = False
                if text_hash:
                    if text_hash in duplicates:
                        is_duplicate = True
                        duplicate_count += 1
                    else:
                        duplicates[text_hash] = motion.get('dok_id', 'unknown')

                # Add normalized text and duplicate flag to motion
                motion['text_normalized'] = text_normalized
                motion['is_duplicate'] = is_duplicate
                motion['text_hash'] = text_hash

                # Write to output
                out_f.write(json.dumps(motion, ensure_ascii=False) + '\n')
                motion_count += 1

                if motion_count % 1000 == 0:
                    print(f"  Processed {motion_count} motions...")

    print(f"  Completed: {motion_count} motions, {duplicate_count} duplicates found")
    return motion_count, duplicate_count


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    INPUT_DIR = SCRIPT_DIR / 'boilerplate_removed'
    OUTPUT_DIR = SCRIPT_DIR / 'normalized'

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Define temporal bins
    bins = [
        ('group1_1986-1993.jsonl', 'group1_1986-1993.jsonl'),
        ('group2_1994-2004.jsonl', 'group2_1994-2004.jsonl'),
        ('group3_2005-2014.jsonl', 'group3_2005-2014.jsonl'),
        ('group4_2015-2025.jsonl', 'group4_2015-2025.jsonl'),
    ]

    total_motions = 0
    total_duplicates = 0

    print("=" * 60)
    print("Normalizing text and detecting duplicates")
    print("=" * 60)

    for input_filename, output_filename in bins:
        input_file = INPUT_DIR / input_filename
        output_file = OUTPUT_DIR / output_filename

        if not input_file.exists():
            print(f"Error: {input_file} not found")
            continue

        count, dups = process_temporal_bin(input_file, output_file)
        total_motions += count
        total_duplicates += dups

    print("=" * 60)
    print(f"Total: {total_motions} motions processed")
    print(f"Total duplicates found: {total_duplicates} ({100*total_duplicates/total_motions:.2f}%)")
    print(f"Output saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
