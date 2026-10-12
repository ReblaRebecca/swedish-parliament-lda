#!/usr/bin/env python3
"""
Extract motion text from XML files following Bruinsma & Johansson (2024) methodology.
Parses XML structure, filters by organ (UbU), extracts body text between markers.
Input: XML files in data_xml/ organized by year
Output: JSONL files organized by temporal bin (1986-1993, 1994-2004, 2005-2014, 2015-2025)
"""

import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime
import xml.etree.ElementTree as ET


class HTMLToTextParser(HTMLParser):
    """Convert HTML to plain text, decoding entities."""
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return ' '.join(self.text)


def decode_html_entities(html_str):
    """Decode HTML entities and extract plain text."""
    if not html_str:
        return ""

    parser = HTMLToTextParser()
    try:
        parser.feed(html_str)
        return parser.get_text()
    except Exception:
        return ""


def extract_body_text(html_content):
    """
    Extract main body text between "Inledning" and signature block.
    Following Bruinsma & Johansson structure.
    """
    if not html_content:
        return ""

    text = decode_html_entities(html_content)

    # Find "Inledning" section (start of main content)
    inledning_match = re.search(r'Inledning\s+', text, re.IGNORECASE)
    start_idx = inledning_match.end() if inledning_match else 0

    # Find signature block (end of main content)
    # Pattern: "Stockholm den DATE" or similar signature markers
    signature_match = re.search(r'Stockholm\s+den\s+\d+\s+\w+\s+\d{4}', text[start_idx:])
    end_idx = start_idx + signature_match.start() if signature_match else len(text)

    body = text[start_idx:end_idx].strip()

    # Clean up extra whitespace
    body = re.sub(r'\s+', ' ', body)

    return body


def get_temporal_bin(date_str):
    """Assign date to temporal bin based on year."""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        year = date_obj.year

        if year <= 1993:
            return 'group1_1986-1993'
        elif year <= 2004:
            return 'group2_1994-2004'
        elif year <= 2014:
            return 'group3_2005-2014'
        else:
            return 'group4_2015-2025'
    except (ValueError, AttributeError):
        return None


def process_xml_file(xml_path):
    """
    Parse XML file and extract motion data if it's from UbU organ.
    Returns dict with extracted fields or None if not UbU.
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Extract metadata from <dokument> child element
        dokument = root.find('dokument')
        if dokument is None:
            return None

        dok_id = dokument.findtext('dok_id', '')
        organ = dokument.findtext('organ', '')
        datum = dokument.findtext('datum', '')
        titel = dokument.findtext('titel', '')
        html_content = dokument.findtext('html', '')

        # Filter by organ (UbU = Education Committee)
        if organ.strip() != 'UbU':
            return None

        # Extract body text
        body_text = extract_body_text(html_content)

        if not body_text:
            return None

        # Extract year from datum (format: YYYY-MM-DD HH:MM:SS)
        date_str = datum.strip().split()[0] if datum else ''

        return {
            'dok_id': dok_id.strip(),
            'date': date_str,
            'title': titel.strip(),
            'text': body_text
        }

    except Exception as e:
        print(f"  Error parsing {xml_path.name}: {e}", file=sys.stderr)
        return None


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    DATA_XML_DIR = SCRIPT_DIR.parent / 'data_xml'
    OUTPUT_DIR = SCRIPT_DIR / 'extracted_text_xml'

    if not DATA_XML_DIR.exists():
        print(f"Error: XML data directory not found: {DATA_XML_DIR}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)

    print("=" * 70)
    print("Extracting Motion Text from XML Files")
    print(f"Input: {DATA_XML_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 70)

    # Track statistics by temporal bin
    stats = {
        'group1_1986-1993': {'count': 0, 'skipped': 0},
        'group2_1994-2004': {'count': 0, 'skipped': 0},
        'group3_2005-2014': {'count': 0, 'skipped': 0},
        'group4_2015-2025': {'count': 0, 'skipped': 0},
    }

    # Output files (one per temporal bin)
    output_files = {}
    for bin_name in stats.keys():
        output_path = OUTPUT_DIR / f"{bin_name}.jsonl"
        output_files[bin_name] = open(output_path, 'w', encoding='utf-8')

    # Find all XML files in data_xml directory structure
    xml_files = list(DATA_XML_DIR.rglob('*.xml'))
    total_files = len(xml_files)

    print(f"\nFound {total_files} XML files")
    print("Processing by temporal bin...")
    print()

    # Process each XML file
    processed = 0
    for xml_path in sorted(xml_files):
        processed += 1
        if processed % 1000 == 0:
            print(f"  Processed {processed}/{total_files}...")

        motion = process_xml_file(xml_path)

        if not motion:
            continue

        # Determine temporal bin from date
        bin_name = get_temporal_bin(motion['date'])

        if not bin_name:
            continue

        # Write to appropriate bin file
        output_files[bin_name].write(json.dumps(motion) + '\n')
        stats[bin_name]['count'] += 1

    # Close all output files
    for f in output_files.values():
        f.close()

    # Print summary
    print("\n" + "=" * 70)
    print("Extraction Summary")
    print("=" * 70)

    total_extracted = 0
    for bin_name in sorted(stats.keys()):
        count = stats[bin_name]['count']
        total_extracted += count
        output_path = OUTPUT_DIR / f"{bin_name}.jsonl"
        size_mb = output_path.stat().st_size / (1024 * 1024) if output_path.exists() else 0
        print(f"{bin_name:20s}: {count:5d} motions ({size_mb:6.1f} MB)")

    print("-" * 70)
    print(f"{'Total':20s}: {total_extracted:5d} motions extracted")
    print("=" * 70)

    print(f"\nOutput files in: {OUTPUT_DIR}")
    print("Next step: Run 02_remove_stopwords.py on extracted_text_xml/")


if __name__ == '__main__':
    main()
