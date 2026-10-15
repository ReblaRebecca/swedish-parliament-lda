#!/usr/bin/env python3
"""
Extract motion text from XML files following Bruinsma & Johansson (2024) methodology.
Parses XML structure, filters by organ (UbU), extracts body text between markers.
Input: XML files organized by year (default: data_xml/ at repo root; override with [xml_dir] [output_dir])
Output: JSONL files organized by temporal bin (1986-1993, 1994-2004, 2005-2014, 2015-2025)
"""

import json
import re
import sys
import unicodedata
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime
import xml.etree.ElementTree as ET


# Tags that separate words. Inline tags (<span>, <b>, <a>, ...) do NOT: the source HTML
# often splits single words across spans ("uppföljni</span><span>ng", "f</span><span>ö</span><span>r").
BLOCK_TAGS = {
    'p', 'br', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ul', 'ol',
    'table', 'tr', 'td', 'th', 'hr', 'section', 'blockquote', 'pre',
}

# Some source texts write å/ä/ö as a base letter followed by a spacing ring/diaeresis ("ma°ste", "sa¨tt")
SPACING_DIACRITICS = {
    'a°': 'å', 'A°': 'Å', 'a¨': 'ä', 'A¨': 'Ä', 'o¨': 'ö', 'O¨': 'Ö',
}
SPACING_DIACRITICS_PATTERN = re.compile('|'.join(SPACING_DIACRITICS))


class HTMLToTextParser(HTMLParser):
    """Convert HTML to plain text, decoding entities.

    Text pieces are joined without separators; whitespace is inserted only at block-level tags.
    """
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag in BLOCK_TAGS:
            self.text.append('\n')

    def handle_endtag(self, tag):
        if tag in BLOCK_TAGS:
            self.text.append('\n')

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return ''.join(self.text)


def repair_characters(text):
    """Repair character-level encoding problems in the source text.

    - Remove soft hyphens (U+00AD), which otherwise become word breaks in normalization
    - Compose combining diacritics (NFC), e.g. 'a' + U+030A -> 'å'
    - Replace spacing diacritics after a base letter, e.g. 'a°' -> 'å', 'o¨' -> 'ö'
    """
    text = text.replace('\xad', '')
    text = unicodedata.normalize('NFC', text)
    return SPACING_DIACRITICS_PATTERN.sub(lambda m: SPACING_DIACRITICS[m.group()], text)


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
    Extract motion body text from HTML, removing author-related and formatting elements.
    Removes <div> and <p> elements with author/header classes, plus style/script tags.
    Returns cleaned, stripped text with normalized whitespace.
    """
    if not html_content:
        return ""

    # Remove style, script, and other non-content HTML elements
    # These contain CSS/JavaScript code that should not appear in text
    non_content_patterns = [
        r'<style[^>]*>.*?</style>',           # CSS styles
        r'<script[^>]*>.*?</script>',         # JavaScript
        r'<link[^>]*>',                       # Link tags
        r'<meta[^>]*>',                       # Meta tags
        r'<!--.*?-->',                        # HTML comments
        r'<noscript[^>]*>.*?</noscript>'     # NoScript content
    ]

    cleaned_html = html_content
    for pattern in non_content_patterns:
        cleaned_html = re.sub(pattern, '', cleaned_html, flags=re.IGNORECASE | re.DOTALL)

    # Remove HTML elements with author-related classes
    # These classes mark author signatures, dates, headers, etc.
    author_classes = [
        'MotionarLista',        # Author list
        'Underskrifter',        # Signatures
        'UnderskriftDatum',     # Signature date
        'sidhuvud_publikation', # Publication header
        'sidhuvud_beteckning'   # Document reference header
    ]

    for class_name in author_classes:
        # Remove <div class="ClassName">...</div> and <p class="ClassName">...</p>
        # Using non-greedy matching to avoid removing too much
        cleaned_html = re.sub(
            rf'<(div|p)[^>]*class="[^"]*{class_name}[^"]*"[^>]*>.*?</\1>',
            '',
            cleaned_html,
            flags=re.IGNORECASE | re.DOTALL
        )

    text = decode_html_entities(cleaned_html)

    # After structural removal of headers and signatures, use full cleaned body.
    # The "Stockholm den DATE" pattern is now a fallback edge case rather than
    # a primary boundary, since Underskrifter and UnderskriftDatum are already removed.
    body = repair_characters(text).strip()

    # Clean up extra whitespace
    body = re.sub(r'\s+', ' ', body)

    return body


def extract_authors(root):
    """Extract author names and metadata from <dokintressent> section.

    Only includes intressents with role='undertecknare' (signatories).
    Returns list of dicts with author info: {name, party, role, order}
    """
    authors = []
    dokintressent = root.find('dokintressent')

    if dokintressent is None:
        return authors

    for intressent in dokintressent.findall('intressent'):
        namn = intressent.findtext('namn', '')
        partibet = intressent.findtext('partibet', '')
        ordning = intressent.findtext('ordning', '')
        roll = intressent.findtext('roll', '')

        # Only include if name exists and role is 'undertecknare' (signatory)
        if namn and roll.strip().lower() == 'undertecknare':
            authors.append({
                'name': namn.strip(),
                'party': partibet.strip() if partibet else '',
                'role': roll.strip(),
                'order': int(ordning) if ordning and ordning.isdigit() else 0
            })

    # Sort by order
    authors.sort(key=lambda x: x['order'])
    return authors


def get_temporal_bin(date_str):
    """Assign date to temporal bin based on year (1986-2025 range)."""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        year = date_obj.year

        if 1986 <= year <= 1993:
            return 'group1_1986-1993'
        elif 1994 <= year <= 2004:
            return 'group2_1994-2004'
        elif 2005 <= year <= 2014:
            return 'group3_2005-2014'
        elif 2015 <= year <= 2025:
            return 'group4_2015-2025'
        else:
            return None  # Outside 1986-2025 range
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
        # Note: organ tag can be "UbU" or "ubu" depending on XML source
        if organ.strip().upper() != 'UBU':
            return None

        # Extract body text
        body_text = extract_body_text(html_content)

        if not body_text:
            return None

        # Extract year from datum (format: YYYY-MM-DD HH:MM:SS)
        date_str = datum.strip().split()[0] if datum else ''

        # Extract author information from root-level <dokintressent>
        authors = extract_authors(root)
        author_names = [a['name'] for a in authors]

        return {
            'dok_id': dok_id.strip(),
            'date': date_str,
            'title': titel.strip(),
            'text': body_text,
            'authors': authors,
            'author_names': author_names
        }

    except Exception as e:
        print(f"  Error parsing {xml_path.name}: {e}", file=sys.stderr)
        return None


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent
    PARENT_DIR = PROJECT_ROOT.parent

    # Allow command-line arguments: [xml_dir] [output_dir]
    # Default: data_xml/ (repo root) -> data/input/extracted_text_xml
    DATA_XML_DIR = Path(sys.argv[1]) if len(sys.argv) >= 2 else PARENT_DIR / 'data_xml'
    OUTPUT_DIR = Path(sys.argv[2]) if len(sys.argv) >= 3 else PROJECT_ROOT / 'data' / 'input' / 'extracted_text_xml'

    if not DATA_XML_DIR.exists():
        print(f"Error: XML data directory not found: {DATA_XML_DIR}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
    # Only files: the riksdag downloads unpack into directories that are themselves named *.xml
    xml_files = [p for p in DATA_XML_DIR.rglob('*.xml') if p.is_file()]
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
        output_files[bin_name].write(json.dumps(motion, ensure_ascii=False) + '\n')
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
    print("Next step: Run 02_remove_boilerplate.py on extracted_text_xml/")


if __name__ == '__main__':
    main()
