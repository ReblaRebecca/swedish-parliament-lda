#!/usr/bin/env python3
"""
Detect duplicate motions on final lemmatized text (STEP 5).
Input: JSON lines with 'text_lemmatized' field.
Output: JSON lines with 'is_duplicate' flag and 'text_hash' field.
Fixed version with explicit file flushing.
"""

import json
import hashlib
from pathlib import Path
import sys


def compute_hash(text):
    """Compute MD5 hash of text for duplicate detection."""
    if not text:
        return None
    return hashlib.md5(text.encode()).hexdigest()


def process_temporal_bin(input_file, output_file, duplicates):
    """Process one temporal bin: detect duplicates (global dict persists across bins)."""
    motion_count = 0
    duplicate_count = 0
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

                # Compute hash on final lemmatized text
                text = motion.get('text_lemmatized', '')
                text_for_hash = ' '.join(text.split())
                text_hash = compute_hash(text_for_hash)

                # Check if duplicate
                is_duplicate = False
                duplicate_of = None
                if text_hash:
                    if text_hash in duplicates:
                        is_duplicate = True
                        duplicate_count += 1
                        duplicate_of = duplicates[text_hash]
                    else:
                        duplicates[text_hash] = motion.get('dok_id', 'unknown')

                # Add duplicate info to motion
                motion['is_duplicate'] = is_duplicate
                motion['duplicate_of'] = duplicate_of
                motion['text_hash'] = text_hash

                # Write to output with explicit flush
                out_f.write(json.dumps(motion, ensure_ascii=False) + '\n')
                out_f.flush()
                motion_count += 1

                if motion_count % 1000 == 0:
                    print(f"  Processed {motion_count} motions...")

    print(f"  Completed: {motion_count} motions written, {duplicate_count} duplicates found, {malformed_count} malformed JSON skipped")
    return motion_count, duplicate_count, malformed_count


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'lemmatized'
    OUTPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'deduplicated'

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Define temporal bins
    bins = [
        ('group1_1986-1993.jsonl', 'group1_1986-1993.jsonl'),
        ('group2_1994-2004.jsonl', 'group2_1994-2004.jsonl'),
        ('group3_2005-2014.jsonl', 'group3_2005-2014.jsonl'),
        ('group4_2015-2025.jsonl', 'group4_2015-2025.jsonl'),
    ]

    # Global duplicates dict
    duplicates = {}

    total_motions = 0
    total_duplicates = 0
    total_malformed = 0

    print("=" * 60)
    print("STEP 5: Detecting duplicate motions (cross-bin deduplication)")
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    for input_filename, output_filename in bins:
        input_file = INPUT_DIR / input_filename
        output_file = OUTPUT_DIR / output_filename

        if not input_file.exists():
            print(f"Error: {input_file} not found")
            continue

        count, dups, malformed = process_temporal_bin(input_file, output_file, duplicates)
        total_motions += count
        total_duplicates += dups
        total_malformed += malformed

    print("=" * 60)
    print(f"Total: {total_motions} motions processed")

    duplicate_percentage = (
        100 * total_duplicates / total_motions
        if total_motions
        else 0
    )
    print(f"Total duplicates found: {total_duplicates} ({duplicate_percentage:.2f}%)")

    if total_malformed > 0:
        print(f"⚠️  Warning: {total_malformed} malformed JSON lines skipped")
    print(f"Output saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
