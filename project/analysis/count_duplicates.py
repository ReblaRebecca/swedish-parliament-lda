#!/usr/bin/env python3
"""
Count duplicate and near-duplicate motions on the final preprocessed text (for reporting).
The models skip the same duplicates (lda_common.read_bin_body_texts keeps the first copy, by text_key);
this script lists them. Counts all motions, including those under the models' length minimum.
Near-duplicates (lda_common.near_duplicates: revised resubmissions, also skipped by the models) are counted
among the motions left after the length minimum and exact duplicates, per period.
Re-run after changing boilerplate or stopwords, since the count depends on the final text.

Input: JSON lines with 'text_no_stopwords' field (output of 05_remove_stopwords.py).
Output: printed counts per temporal bin and a list of duplicate -> original dok_ids.
"""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from periods import PERIOD_FILES  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'modeling'))
from lda_common import NEAR_DUPLICATE_JACCARD, near_duplicates, read_bin_body_texts, text_key  # noqa: E402


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

            # The models' duplicate key: whitespace collapsed, so texts differing only in line wrapping match
            text = motion.get('text_no_stopwords', '')
            if not text.strip():
                continue
            text_hash = text_key(text)

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

    bins = PERIOD_FILES

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

    # Near-duplicates among the motions left after the length minimum and exact duplicates (the models' rule)
    texts, metadata, seen = [], [], set()
    for filename in bins:
        if (INPUT_DIR / filename).exists():
            bin_texts, bin_metadata, _ = read_bin_body_texts(INPUT_DIR / filename, seen)
            texts += bin_texts
            metadata += bin_metadata
    copies = near_duplicates(texts, [m['session'] for m in metadata])
    print("=" * 60)
    print(f"Near-duplicates (Jaccard of three-word sequences >= {NEAR_DUPLICATE_JACCARD} with an earlier motion), "
          f"among {len(texts)} motions after the length minimum and exact duplicates: {len(copies)}")
    for filename in bins:
        period = Path(filename).stem.split('_', 1)[-1]
        print(f"  {filename}: {sum(1 for i in copies if metadata[i]['period'] == period)}")
    print("=" * 60)


if __name__ == '__main__':
    main()
