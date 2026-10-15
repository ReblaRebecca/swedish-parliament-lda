#!/usr/bin/env python3
"""
Remove Swedish parliamentary boilerplate from motion text (STEP 1).
Works on raw extracted text with original structure (newlines, punctuation).
Input: JSON lines with raw 'text' field from extraction.
Output: JSON lines with 'text_no_boilerplate' field.
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


# Regex for motion numbers (e.g., 1986/87:1001, GE02A1)
MOTION_NUMBER_PATTERN = re.compile(r'\d{4}/\d{2}:\w+|[A-Z]{1,2}\d+[A-Z]*\d*')


def remove_motion_numbers(text):
    """Remove motion identification numbers."""
    return MOTION_NUMBER_PATTERN.sub('', text)


def remove_author_signatures(text):
    """Remove author/undersignature lines.

    Matches: Name (PARTY_CODE) format with Swedish characters.
    Handles both single and multi-author lines.
    Examples: "John Smith (s)", "Maria von Berg (kd) Åsa Bergström (mp)"
    """
    # Remove lines that contain only names and party codes
    lines = text.split('\n')
    filtered_lines = []

    for line in lines:
        # Signature pattern: one or more instances of Name (PARTY_CODE)
        # Optional leading whitespace, then capital letter (Swedish Å, Ä, Ö),
        # followed by name-like chars, party code in parens
        # Party codes can be 1-4 chars (s, m, kds, vpk, etc.), upper or lower case
        # Catches:
        #   - "John Smith (s)"
        #   - "  John Smith (s)" (indented)
        #   - "John Smith (s) Maria Berg (mp) Åsa Bergström (fp)" (multi-author)
        if re.match(r'^\s*([A-ZÅÄÖ][A-Za-zåäö\s\-\.\,]+\([A-Za-zåäö]{1,4}\)\s*)+$', line):
            continue
        filtered_lines.append(line)

    return '\n'.join(filtered_lines)


def remove_boilerplate_phrases(text, boilerplate_patterns):
    """Remove known boilerplate phrases."""
    for pattern in boilerplate_patterns:
        text = pattern.sub('', text)
    return text


def clean_text(text):
    """Remove extra whitespace but preserve line structure."""
    if not text:
        return ""

    # Remove extra whitespace on each line but preserve line breaks
    lines = text.split('\n')
    cleaned_lines = [re.sub(r'\s+', ' ', line).strip() for line in lines]
    # Remove empty lines
    cleaned_lines = [line for line in cleaned_lines if line]

    return '\n'.join(cleaned_lines)


def remove_boilerplate(text, boilerplate_patterns):
    """Apply all boilerplate removal techniques."""
    if not text:
        return ""

    # Apply removals in sequence (order matters - structural first)
    text = remove_motion_numbers(text)
    text = remove_author_signatures(text)
    text = remove_boilerplate_phrases(text, boilerplate_patterns)
    text = clean_text(text)

    return text


def process_temporal_bin(input_file, output_file, boilerplate_patterns):
    """Process one temporal bin: remove boilerplate from raw text."""
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

                # Remove boilerplate from raw extracted text
                text = motion.get('text', '')
                text_cleaned = remove_boilerplate(text, boilerplate_patterns)

                # Add cleaned text to motion
                motion['text_no_boilerplate'] = text_cleaned

                # Write to output
                out_f.write(json.dumps(motion, ensure_ascii=False) + '\n')
                motion_count += 1

                if motion_count % 1000 == 0:
                    print(f"  Processed {motion_count} motions...")

    print(f"  Completed: {motion_count} motions, {malformed_count} malformed JSON skipped")
    return motion_count, malformed_count


def main():
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    # Allow command-line arguments: [input_dir] [output_dir] [boilerplate_file]
    # Default: data/input/extracted_text_xml -> data/output/boilerplate_removed with config/boilerplate_phrases.txt
    if len(sys.argv) >= 3:
        INPUT_DIR = Path(sys.argv[1])
        OUTPUT_DIR = Path(sys.argv[2])
        PHRASES_FILE = Path(sys.argv[3]) if len(sys.argv) >= 4 else PROJECT_ROOT / 'config' / 'boilerplate_phrases.txt'
    else:
        INPUT_DIR = PROJECT_ROOT / 'data' / 'input' / 'extracted_text_xml'
        OUTPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'boilerplate_removed'
        PHRASES_FILE = PROJECT_ROOT / 'config' / 'boilerplate_phrases.txt'

    # Load boilerplate patterns
    BOILERPLATE_PATTERNS = load_boilerplate_phrases(PHRASES_FILE)

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
    print("STEP 1: Removing parliamentary boilerplate (structural)")
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Boilerplate patterns loaded: {len(BOILERPLATE_PATTERNS)}")
    print("=" * 60)

    for input_filename, output_filename in bins:
        input_file = INPUT_DIR / input_filename
        output_file = OUTPUT_DIR / output_filename

        if not input_file.exists():
            print(f"Error: {input_file} not found")
            continue

        count, malformed = process_temporal_bin(input_file, output_file, BOILERPLATE_PATTERNS)
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
