#!/usr/bin/env python3
"""
Extract motion text from XML files following Bruinsma & Johansson (2024) methodology.
Parses XML structure, filters by organ (UbU), extracts body text between markers.
Removes document metadata from the text: signatures, headers, the title heading,
motion numbers and the motion's own author names (body and title).
Input: XML files, searched recursively (default: ../swedish-parliament-data next to the repository,
       with one folder per period such as mot-1980-1989.xml/; override with [xml_dir] [output_dir])
Output: JSONL files, one per period (periods.py: four periods of complete electoral terms, sessions
        1985/86-2025/26), assigned by parliamentary session (riksmöte), not by date
"""

import json
import re
import sys
import unicodedata
from pathlib import Path
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from periods import PERIODS, period_of_session  # noqa: E402


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


# The title heading appears near the start of the body ("Motion till riksdagen ... av NAME (PARTY) TITLE").
# Only an occurrence starting within this many characters is treated as the heading.
TITLE_HEADING_MAX_START = 400


def remove_title_heading(body, title):
    """Remove the title heading from the start of the body text.

    The title is kept as a separate field (for later use), so the body holds only the motion's
    own text and title words are not counted in it twice. Matching is word by word, ignoring case and punctuation
    differences ("Sfi - uttalets" vs "Sfi – uttalets"). Later repetitions of the title phrase
    belong to the motion's argument and are kept.
    """
    words = re.findall(r'\w+', title)
    if not body or not words:
        return body

    pattern = re.compile(r'\b' + r'\W+'.join(re.escape(w) for w in words) + r'\b', re.IGNORECASE)
    match = pattern.search(body)
    if not match or match.start() > TITLE_HEADING_MAX_START:
        return body

    return re.sub(r'\s+', ' ', body[:match.start()] + ' ' + body[match.end():]).strip()


# Motion numbers (e.g., 1986/87:1001, GE02A1)
MOTION_NUMBER_PATTERN = re.compile(r'\d{4}/\d{2}:\w+|[A-Z]{1,2}\d+[A-Z]*\d*')


def remove_motion_numbers(text):
    """Remove motion identification numbers."""
    return MOTION_NUMBER_PATTERN.sub('', text)


def remove_author_names(text, author_names):
    """Remove author names from text using per-document metadata.

    Only removes exact word matches to avoid removing legitimate content.
    Author names are case-insensitive but matched as whole words only.
    """
    escaped_names = [re.escape(name) for name in author_names if name]
    if not text or not escaped_names:
        return text

    pattern = r'\b(' + '|'.join(escaped_names) + r')\b'
    return re.sub(pattern, '', text, flags=re.IGNORECASE)


def remove_metadata(text, author_names):
    """Remove motion numbers and author names, then collapse whitespace."""
    text = remove_motion_numbers(text)
    text = remove_author_names(text, author_names)
    return re.sub(r'\s+', ' ', text).strip()


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


def get_temporal_bin(session):
    """Period (file stem) of a parliamentary session ('1985/86' -> 'group1_1985-1994'); None if outside
    1985/86-2025/26 or not a valid session. The date is not used: some motions carry a placeholder date."""
    return period_of_session(session)


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
        session = dokument.findtext('rm', '')
        titel = repair_characters(dokument.findtext('titel', ''))
        html_content = dokument.findtext('html', '')

        # Filter by organ (UbU = Education Committee)
        # Note: organ tag can be "UbU" or "ubu" depending on XML source
        if organ.strip().upper() != 'UBU':
            return None

        # Extract body text
        body_text = extract_body_text(html_content)

        if not body_text:
            return None

        # Remove the title heading: the title is kept separately, the body holds only the motion's own text
        body_text = remove_title_heading(body_text, titel)

        # Date without time (format: YYYY-MM-DD HH:MM:SS), kept as metadata
        date_str = datum.strip().split()[0] if datum else ''

        # Extract author information from root-level <dokintressent>
        authors = extract_authors(root)
        author_names = [a['name'] for a in authors]

        # Remove motion numbers and author names from body and title
        body_text = remove_metadata(body_text, author_names)
        title_text = remove_metadata(titel, author_names)

        return {
            'dok_id': dok_id.strip(),
            'date': date_str,
            'session': session.strip(),     # parliamentary session (riksmöte), decides the period
            'title': titel.strip(),          # original title, for display
            'title_text': title_text,        # title with metadata removed, for processing
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
    # Default: ../swedish-parliament-data (next to the repository) -> data/input/extracted_text_xml
    DATA_XML_DIR = Path(sys.argv[1]) if len(sys.argv) >= 2 else PARENT_DIR.parent / 'swedish-parliament-data'
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
    stats = {stem: {'count': 0, 'skipped': 0} for stem, _, _ in PERIODS}

    # Output files (one per temporal bin)
    output_files = {}
    for bin_name in stats.keys():
        output_path = OUTPUT_DIR / f"{bin_name}.jsonl"
        output_files[bin_name] = open(output_path, 'w', encoding='utf-8')

    # Find all XML files in the data directory structure
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

        # Period from the parliamentary session
        bin_name = get_temporal_bin(motion['session'])

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
    print("Next step: Run preprocessing/02_lemmatize.py")


if __name__ == '__main__':
    main()
