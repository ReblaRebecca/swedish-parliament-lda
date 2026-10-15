#!/usr/bin/env python3
"""
Normalize motion text: lowercase, remove numbers and punctuation (STEP 2).
Works on boilerplate-removed text, preserves line structure.
Removes document-specific author names using extracted metadata.
Input: JSON lines with 'text_no_boilerplate' and 'author_names' fields.
Output: JSON lines with 'text_normalized' field.
"""

import json
import re
from pathlib import Path
import sys


def remove_author_names(text, author_names):
    """Remove author names from text using per-document metadata.

    Only removes exact word matches to avoid removing legitimate content.
    Author names are case-insensitive but matched as whole words only.
    """
    if not text or not author_names:
        return text

    # Build regex pattern for author names (case-insensitive, word boundaries)
    # Escape special regex characters in names
    escaped_names = [re.escape(name.lower()) for name in author_names if name]
    if not escaped_names:
        return text

    # Pattern: word boundary + author name + word boundary
    pattern = r'\b(' + '|'.join(escaped_names) + r')\b'

    # Remove author names (case-insensitive)
    text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    return text


def normalize_text(text, author_names=None):
    """Normalize text: lowercase, remove numbers/punctuation, clean whitespace.

    Removes document-specific author names, preserves line breaks for structure.
    Removes single-character words (OCR artifacts).
    """
    if not text:
        return ""

    # Remove author names first (before lowercasing, for better matching)
    text = remove_author_names(text, author_names)

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

                # Normalize text from boilerplate-removed version
                text = motion.get('text_no_boilerplate', '')
                author_names = motion.get('author_names', [])
                text_normalized = normalize_text(text, author_names)

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
    # Usage: python3 03_normalize_text.py [input_dir] [output_dir]
    # Default: data/output/boilerplate_removed -> data/output/normalized
    if len(sys.argv) >= 3:
        INPUT_DIR = Path(sys.argv[1])
        OUTPUT_DIR = Path(sys.argv[2])
    else:
        INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'boilerplate_removed'
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
    print("STEP 3: Normalizing text and removing per-document author names")
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
