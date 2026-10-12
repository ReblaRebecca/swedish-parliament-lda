#!/usr/bin/env python3
"""
Remove Swedish parliamentary boilerplate from motion text.
Hybrid approach: regex patterns + hardcoded phrase removal.
Input: JSON lines with stopword-removed text.
Output: JSON lines with boilerplate-removed text.
"""

import json
import re
from pathlib import Path
import sys


def load_boilerplate_phrases(phrases_file):
    """Load boilerplate phrases from file and convert to regex patterns."""
    patterns = []

    if not phrases_file.exists():
        print(f"Warning: {phrases_file} not found, using minimal boilerplate removal")
        return []

    with open(phrases_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Convert wildcard patterns to regex
            # "hemställ*" becomes r"\bhemställ\w*\b" (word boundary aware)
            if '*' in line:
                # Escape special regex chars except *
                pattern = re.escape(line).replace(r'\*', r'\w*')
                pattern = r'\b' + pattern + r'\b'
            else:
                # For exact phrases, use word boundaries
                pattern = r'\b' + re.escape(line) + r'\b'

            try:
                compiled = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
                patterns.append(compiled)
            except re.error as e:
                print(f"Warning: Invalid regex pattern '{line}': {e}")

    return patterns


# Load boilerplate phrases from file
SCRIPT_DIR = Path(__file__).parent
PHRASES_FILE = SCRIPT_DIR / 'boilerplate_phrases.txt'
BOILERPLATE_PATTERNS = load_boilerplate_phrases(PHRASES_FILE)

# Regex for motion numbers (e.g., 1986/87:1001, GE02A1)
MOTION_NUMBER_PATTERN = re.compile(r'\d{4}/\d{2}:\w+|[A-Z]{1,2}\d+[A-Z]*\d*')

# Regex for author signatures (Name followed by party code)
AUTHOR_PATTERN = re.compile(r'^[A-Z][a-z\s\-]+\([@\w]\)', re.MULTILINE)


def remove_motion_numbers(text):
    """Remove motion identification numbers."""
    return MOTION_NUMBER_PATTERN.sub('', text)


def remove_author_signatures(text):
    """Remove author/undersignature lines."""
    # Remove lines that look like "Name (party)"
    lines = text.split('\n')
    filtered_lines = []

    for line in lines:
        # Skip lines that are just names and party codes
        if re.match(r'^[A-Z][a-z\s\-\.\,]+\([a-z]\)\s*$', line):
            continue
        filtered_lines.append(line)

    return '\n'.join(filtered_lines)


def remove_boilerplate_phrases(text):
    """Remove known boilerplate phrases."""
    for pattern in BOILERPLATE_PATTERNS:
        text = pattern.sub('', text)
    return text


def clean_text(text):
    """Remove extra whitespace and empty lines."""
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def remove_boilerplate(text):
    """Apply all boilerplate removal techniques."""
    if not text:
        return ""

    # Apply removals in sequence
    text = remove_motion_numbers(text)
    text = remove_boilerplate_phrases(text)
    text = remove_author_signatures(text)
    text = clean_text(text)

    return text


def process_temporal_bin(input_file, output_file):
    """Process one temporal bin: remove boilerplate."""
    motion_count = 0

    print(f"Processing {input_file.name}...")

    with open(input_file, 'r', encoding='utf-8') as in_f:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for line in in_f:
                try:
                    motion = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue

                # Remove boilerplate from stopword-removed text
                text = motion.get('text_no_stopwords', '')
                text_cleaned = remove_boilerplate(text)

                # Add cleaned text to motion
                motion['text_no_boilerplate'] = text_cleaned

                # Write to output
                out_f.write(json.dumps(motion, ensure_ascii=False) + '\n')
                motion_count += 1

                if motion_count % 1000 == 0:
                    print(f"  Processed {motion_count} motions...")

    print(f"  Completed: {motion_count} motions processed")
    return motion_count


def main():
    # Configuration
    INPUT_DIR = SCRIPT_DIR / 'stopword_removed'
    OUTPUT_DIR = SCRIPT_DIR / 'boilerplate_removed'

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

    print("=" * 60)
    print("Removing parliamentary boilerplate")
    print(f"Boilerplate patterns loaded: {len(BOILERPLATE_PATTERNS)}")
    print("=" * 60)

    for input_filename, output_filename in bins:
        input_file = INPUT_DIR / input_filename
        output_file = OUTPUT_DIR / output_filename

        if not input_file.exists():
            print(f"Error: {input_file} not found")
            continue

        count = process_temporal_bin(input_file, output_file)
        total_motions += count

    print("=" * 60)
    print(f"Total: {total_motions} motions processed")
    print(f"Output saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
