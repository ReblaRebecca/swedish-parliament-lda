#!/usr/bin/env python3
"""
Count duplicate motions on the final preprocessed text (for reporting).
Not part of the pipeline: models use all motions, duplicates are not removed.
Re-run after changing boilerplate or stopwords, since the count depends on the final text.

Input: JSON lines with 'text_no_stopwords' field (output of 05_remove_stopwords.py).
Output: printed counts per temporal bin and a list of duplicate -> original dok_ids.
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


def count_temporal_bin(input_file, duplicates, pairs):
    """Count duplicates in one temporal bin (global dict persists across bins).

    Args:
        input_file: Input JSON file
        duplicates: Dict[text_hash -> dok_id] shared across all bins for cross-bin detection
        pairs: List of (duplicate dok_id, original dok_id), appended to
    """
    motion_count = 0
    duplicate_count = 0
    malformed_count = 0

    with open(input_file, 'r', encoding='utf-8') as in_f:
        for line in in_f:
            try:
                motion = json.loads(line.strip())
            except json.JSONDecodeError:
                malformed_count += 1
                continue
            motion_count += 1

            # Normalize whitespace (collapse newlines, multiple spaces) to catch
            # duplicates that differ only in line wrapping
            text = motion.get('text_no_stopwords', '')
            text_hash = compute_hash(' '.join(text.split()))
            if not text_hash:
                continue

            dok_id = motion.get('dok_id', 'unknown')
            if text_hash in duplicates:
                duplicate_count += 1
                pairs.append((dok_id, duplicates[text_hash]))
            else:
                duplicates[text_hash] = dok_id

    print(f"  {input_file.name}: {motion_count} motions, {duplicate_count} duplicates, {malformed_count} malformed JSON skipped")
    return motion_count, duplicate_count


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    # Usage: python3 count_duplicates.py [input_dir]
    # Default: data/output/stopword_removed
    if len(sys.argv) >= 2:
        INPUT_DIR = Path(sys.argv[1])
    else:
        INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'

    bins = [
        'group1_1986-1993.jsonl',
        'group2_1994-2004.jsonl',
        'group3_2005-2014.jsonl',
        'group4_2015-2025.jsonl',
    ]

    # Global duplicates dict (persists across all bins for cross-bin detection)
    duplicates = {}
    pairs = []

    total_motions = 0
    total_duplicates = 0

    print("=" * 60)
    print("Counting duplicate motions (cross-bin)")
    print(f"Input: {INPUT_DIR}")
    print("=" * 60)

    for filename in bins:
        input_file = INPUT_DIR / filename
        if not input_file.exists():
            print(f"Error: {input_file} not found")
            continue

        count, dups = count_temporal_bin(input_file, duplicates, pairs)
        total_motions += count
        total_duplicates += dups

    print("=" * 60)
    duplicate_percentage = 100 * total_duplicates / total_motions if total_motions else 0
    print(f"Total: {total_duplicates} duplicates of {total_motions} motions ({duplicate_percentage:.2f}%)")
    print("=" * 60)
    for dup, original in pairs:
        print(f"{dup} duplicates {original}")


if __name__ == '__main__':
    main()
