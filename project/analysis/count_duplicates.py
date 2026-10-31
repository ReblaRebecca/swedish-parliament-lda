#!/usr/bin/env python3
"""
Count duplicate and near-duplicate motions on the final preprocessed text (for reporting).
The models skip duplicates within each period (lda_common.load_body_texts, dedup='period': the first copy in
each period is kept, by text_key); this script lists them. Counts all motions, including those under the
models' length minimum. Copies of a motion in an earlier period are kept by the models and counted separately.
Near-duplicates (lda_common.near_duplicates: revised resubmissions, also skipped within each period) are counted
among the motions left after the length minimum and exact duplicates, per period.
Finally the modelled motions per period with the current rule and with the earlier global rule (dedup='global').
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
from lda_common import (  # noqa: E402
    NEAR_DUPLICATE_JACCARD, load_body_texts, near_duplicates, period_label, read_bin_body_texts, text_key,
)


def count_temporal_bin(input_file, earlier, pairs):
    """Count duplicates in one temporal bin.

    Args:
        input_file: Input JSON file
        earlier: Dict[text_hash -> dok_id] of the earlier bins; this bin's texts are added at the end
        pairs: List of (duplicate dok_id, original dok_id) within the bin, appended to
    Returns: motions, duplicates within the bin (skipped), copies of a motion in an earlier bin (kept)
    """
    motion_count = 0
    duplicate_count = 0
    earlier_count = 0
    malformed_count = 0
    in_bin = {}

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
            if text_hash in in_bin:
                duplicate_count += 1
                pairs.append((dok_id, in_bin[text_hash]))
            else:
                in_bin[text_hash] = dok_id
                if text_hash in earlier:
                    earlier_count += 1

    for text_hash, dok_id in in_bin.items():
        earlier.setdefault(text_hash, dok_id)
    print(f"  {input_file.name}: {motion_count} motions, {duplicate_count} duplicates in the period (skipped), "
          f"{earlier_count} copies of an earlier period's motion (kept), {malformed_count} malformed JSON skipped")
    return motion_count, duplicate_count, earlier_count


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

    bins = [filename for filename in PERIOD_FILES if (INPUT_DIR / filename).exists()]
    for filename in PERIOD_FILES:
        if filename not in bins:
            print(f"Error: {INPUT_DIR / filename} not found")

    earlier = {}
    pairs = []

    total_motions = 0
    total_duplicates = 0
    total_earlier = 0

    print("=" * 60)
    print("Counting duplicate motions (within each period)")
    print(f"Input: {INPUT_DIR}")
    print("=" * 60)

    for filename in bins:
        count, dups, earlier_copies = count_temporal_bin(INPUT_DIR / filename, earlier, pairs)
        total_motions += count
        total_duplicates += dups
        total_earlier += earlier_copies

    print("=" * 60)
    duplicate_percentage = 100 * total_duplicates / total_motions if total_motions else 0
    print(f"Total: {total_duplicates} duplicates within a period of {total_motions} motions ({duplicate_percentage:.2f}%); "
          f"{total_earlier} copies of an earlier period's motion, kept")
    print("=" * 60)
    for dup, original in pairs:
        print(f"{dup} duplicates {original}")

    # Near-duplicates within each period, among the motions left after the length minimum and exact duplicates
    print("=" * 60)
    print(f"Near-duplicates within each period (Jaccard of three-word sequences >= {NEAR_DUPLICATE_JACCARD} "
          "with an earlier motion of the period), after the length minimum and exact duplicates:")
    total_near = 0
    for filename in bins:
        texts, metadata, _ = read_bin_body_texts(INPUT_DIR / filename)
        copies = near_duplicates(texts, [m['session'] for m in metadata])
        total_near += len(copies)
        print(f"  {filename}: {len(copies)} of {len(texts)}")
    print(f"  Total: {total_near}")

    # Modelled motions per period: the current rule against the earlier global one
    print("=" * 60)
    print("Modelled motions per period, within each period (the models) and over all periods (earlier rule):")
    counts = {}
    for dedup in ('period', 'global'):
        _, metadata, _ = load_body_texts(INPUT_DIR, dedup=dedup)
        counts[dedup] = [sum(1 for m in metadata if m['period'] == period_label(f)) for f in bins]
    for filename, now, before in zip(bins, counts['period'], counts['global']):
        print(f"  {filename}: {now} (global: {before}; +{now - before})")
    print(f"  Total: {sum(counts['period'])} (global: {sum(counts['global'])}; "
          f"+{sum(counts['period']) - sum(counts['global'])})")
    print("=" * 60)


if __name__ == '__main__':
    main()
