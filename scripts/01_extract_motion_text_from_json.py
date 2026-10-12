#!/usr/bin/env python3
"""
Extract text from Swedish parliamentary motion JSON files.
Process UbU (Education Committee) motions organized by temporal bins.
Output: JSON lines format with motion metadata and extracted text.
"""

import json
import csv
from pathlib import Path
from html.parser import HTMLParser
import sys


class HTMLToText(HTMLParser):
    """Convert HTML to plain text."""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_content = False

    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style']:
            self.skip_content = True

    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.skip_content = False
        elif tag in ['p', 'div', 'br', 'li']:
            self.text.append('\n')

    def handle_data(self, data):
        if not self.skip_content:
            text = data.strip()
            if text:
                self.text.append(text)

    def get_text(self):
        return ' '.join(self.text).strip()


def load_json_file(filepath):
    """Load JSON file, handling UTF-8 BOM."""
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}", file=sys.stderr)
        return None


def extract_text_from_html(html_content):
    """Convert HTML to plain text."""
    if not html_content:
        return ""
    parser = HTMLToText()
    try:
        parser.feed(html_content)
        return parser.get_text()
    except Exception as e:
        print(f"Error parsing HTML: {e}", file=sys.stderr)
        return ""


def remove_author_signatures(text):
    """Remove author/signatory block from end of motion text."""
    if not text:
        return text

    lines = text.split('\n')

    # Remove lines that are author signatures (Name + party code or similar)
    # Signatures typically appear at the end and match patterns like:
    # "FIRSTNAME LASTNAME (s)"
    # "Stockholm den 23 januari 1981"
    filtered_lines = []
    in_signature_block = False

    for line in reversed(lines):
        stripped = line.strip()

        # Detect signature patterns (Name with party code in parentheses)
        if stripped and '(' in stripped and ')' in stripped:
            # Likely a signature line (NAME (party))
            in_signature_block = True
            continue

        # Skip date lines (Stockholm den X Y Z)
        if stripped.startswith('Stockholm den') or stripped.startswith('stockholm den'):
            in_signature_block = True
            continue

        # Once we're past the signature block, keep all remaining lines
        if in_signature_block and not stripped:
            # Empty lines at end of signature block
            continue
        elif in_signature_block and stripped:
            # We've reached actual content, stop removing
            in_signature_block = False

        filtered_lines.append(line)

    # Reverse back to original order
    cleaned_text = '\n'.join(reversed(filtered_lines)).strip()
    return cleaned_text


def extract_motion_text(json_data):
    """Extract title and text from motion JSON, removing author signatures."""
    if 'dokumentstatus' not in json_data:
        return None

    doc = json_data['dokumentstatus'].get('dokument', {})
    title = doc.get('titel', '')
    html = doc.get('html', '')
    datum = doc.get('datum', '')
    dok_id = doc.get('dok_id', '')

    text = extract_text_from_html(html)

    # Remove author/signatory block
    text = remove_author_signatures(text)

    # Combine title and body text
    full_text = f"{title}\n\n{text}".strip()

    return {
        'dok_id': dok_id,
        'date': datum,
        'title': title,
        'text': full_text
    }


def process_temporal_bin(csv_file, data_dir, output_file):
    """Process one temporal bin: read CSV, extract text from JSON, write output."""
    data_path = Path(data_dir)
    motion_count = 0
    error_count = 0

    print(f"Processing {csv_file.name}...")

    with open(output_file, 'w', encoding='utf-8') as out_f:
        with open(csv_file, 'r', encoding='utf-8') as csv_f:
            reader = csv.DictReader(csv_f)
            for row in reader:
                filename = row['filename']

                # Find the JSON file in data directories
                json_path = None
                for folder in data_path.glob('mot-*'):
                    candidate = folder / filename
                    if candidate.exists():
                        json_path = candidate
                        break

                if json_path is None:
                    print(f"  Warning: Could not find {filename}", file=sys.stderr)
                    error_count += 1
                    continue

                json_data = load_json_file(str(json_path))
                if json_data is None:
                    error_count += 1
                    continue

                motion = extract_motion_text(json_data)
                if motion is None:
                    error_count += 1
                    continue

                # Write as JSON line
                out_f.write(json.dumps(motion, ensure_ascii=False) + '\n')
                motion_count += 1

                if motion_count % 1000 == 0:
                    print(f"  Processed {motion_count} motions...")

    print(f"  Completed: {motion_count} motions extracted, {error_count} errors")
    return motion_count, error_count


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    DATA_DIR = Path('/Users/rebecca/Dev/SU/Proj_course/data')
    OUTPUT_DIR = SCRIPT_DIR / 'extracted_text'

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Define temporal bins
    bins = [
        ('filtered_motions_UbU_group1_1986-1993.csv', 'group1_1986-1993.jsonl'),
        ('filtered_motions_UbU_group2_1994-2004.csv', 'group2_1994-2004.jsonl'),
        ('filtered_motions_UbU_group3_2005-2014.csv', 'group3_2005-2014.jsonl'),
        ('filtered_motions_UbU_group4_2015-2025.csv', 'group4_2015-2025.jsonl'),
    ]

    total_motions = 0
    total_errors = 0

    print("=" * 60)
    print("Extracting motion text from JSON files")
    print("=" * 60)

    for csv_filename, output_filename in bins:
        csv_file = SCRIPT_DIR / csv_filename
        output_file = OUTPUT_DIR / output_filename

        if not csv_file.exists():
            print(f"Error: {csv_file} not found")
            continue

        count, errors = process_temporal_bin(csv_file, DATA_DIR, output_file)
        total_motions += count
        total_errors += errors

    print("=" * 60)
    print(f"Total: {total_motions} motions extracted, {total_errors} errors")
    print(f"Output saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
