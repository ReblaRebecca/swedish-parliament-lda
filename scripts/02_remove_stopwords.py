#!/usr/bin/env python3
"""
Remove Swedish stop words from extracted motion text.
Processes JSON lines files organized by temporal bins.
Output: JSON lines with stopword-removed text.
"""

import json
from pathlib import Path
import sys

try:
    from nltk.corpus import stopwords
except ImportError:
    print("Error: NLTK not installed. Install with: pip install nltk")
    sys.exit(1)


def get_swedish_stopwords():
    """Get Swedish stop words from NLTK."""
    try:
        stop_words = set(stopwords.words('swedish'))
    except LookupError:
        print("Downloading NLTK stopwords...")
        import nltk
        nltk.download('stopwords', quiet=True)
        stop_words = set(stopwords.words('swedish'))

    return stop_words


def remove_stopwords(text, stop_words):
    """Remove stop words from text."""
    if not text:
        return ""

    # Split into words and filter out stop words (case-insensitive)
    words = text.lower().split()
    filtered_words = [word for word in words if word not in stop_words]

    return ' '.join(filtered_words)


def process_temporal_bin(input_file, output_file, stop_words):
    """Process one temporal bin: remove stop words."""
    motion_count = 0

    print(f"Processing {input_file.name}...")

    with open(input_file, 'r', encoding='utf-8') as in_f:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for line in in_f:
                try:
                    motion = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue

                # Remove stop words from text
                text_cleaned = remove_stopwords(motion.get('text', ''), stop_words)

                # Update motion with cleaned text
                motion['text_no_stopwords'] = text_cleaned

                # Write to output
                out_f.write(json.dumps(motion, ensure_ascii=False) + '\n')
                motion_count += 1

                if motion_count % 1000 == 0:
                    print(f"  Processed {motion_count} motions...")

    print(f"  Completed: {motion_count} motions processed")
    return motion_count


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent

    # Allow command-line arguments for input/output directories (for XML or other sources)
    # Usage: python3 02_remove_stopwords.py [input_dir] [output_dir]
    # Default: extracted_text -> stopword_removed (backward compatible)
    if len(sys.argv) >= 3:
        INPUT_DIR = Path(sys.argv[1])
        OUTPUT_DIR = Path(sys.argv[2])
    else:
        INPUT_DIR = SCRIPT_DIR / 'extracted_text'
        OUTPUT_DIR = SCRIPT_DIR / 'stopword_removed'

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Get stop words
    print("Loading Swedish stop words...")
    stop_words = get_swedish_stopwords()
    print(f"Loaded {len(stop_words)} stop words")

    # Define temporal bins
    bins = [
        ('group1_1986-1993.jsonl', 'group1_1986-1993.jsonl'),
        ('group2_1994-2004.jsonl', 'group2_1994-2004.jsonl'),
        ('group3_2005-2014.jsonl', 'group3_2005-2014.jsonl'),
        ('group4_2015-2025.jsonl', 'group4_2015-2025.jsonl'),
    ]

    total_motions = 0

    print("=" * 60)
    print("Removing Swedish stop words")
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    for input_filename, output_filename in bins:
        input_file = INPUT_DIR / input_filename
        output_file = OUTPUT_DIR / output_filename

        if not input_file.exists():
            print(f"Error: {input_file} not found")
            continue

        count = process_temporal_bin(input_file, output_file, stop_words)
        total_motions += count

    print("=" * 60)
    print(f"Total: {total_motions} motions processed")
    print(f"Output saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
