#!/usr/bin/env python3
"""
Remove Swedish stop words from normalized motion text (STEP 3).
Works on already-normalized text (lowercase, punctuation removed).
Input: JSON lines with 'text_normalized' field.
Output: JSON lines with 'text_no_stopwords' field.
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
    """Get Swedish stop words from NLTK with supplementary common words."""
    try:
        stop_words = set(stopwords.words('swedish'))
    except LookupError:
        print("Downloading NLTK stopwords...")
        import nltk
        nltk.download('stopwords', quiet=True)
        stop_words = set(stopwords.words('swedish'))

    # Add Swedish general words missing from NLTK
    # Parliamentary document abbreviations (metadata)
    supplementary_stops = {'ub', 'dvs', 'etc', 'osv', 'resp', 'eg', 'ca', 'frn', 'ky', 'et', 'tt', 'ib', 'ds', 'qz', 'iq', 'uö', 'fn', 'of', 'mr', 'ar'}
    # Spatial/directional words (structural, not content) - NOTE: many duplicated with boilerplate
    # Auxiliary verbs
    supplementary_stops.update({'ska', 'skall', 'blir', 'varit', 'blivit'})
    # Prepositions and connectors (too generic for content)
    supplementary_stops.update({'kommer', 'enligt', 'genom', 'dock', 'fall', 'ge', 'ta', 'del', 'fler'})
    # Generic adjectives and verbs (too vague for education policy content)
    supplementary_stops.update({'olika', 'mer', 'behöver', 'vill', 'nya'})
    # Generic action verbs and helpers (identified from LDA analysis)
    supplementary_stops.update({'göra', 'gör', 'gjort', 'gjorts', 'håll', 'håller', 'rör'})
    # Generic prepositions/adverbs
    supplementary_stops.update({'inför', 'all', 'alls'})
    # Generic manner/state/existence verbs and adjectives (sätt in boilerplate)
    supplementary_stops.update({'sätts', 'visar', 'visat', 'viss', 'dels', 'finna', 'finnas', 'är'})
    # Additional generic adjectives, verbs, adverbs, conjunctions
    supplementary_stops.update({'stora', 'rätt', 'bra', 'hos', 'se', 'går', 'bara', 'ser', 'både', 'samt'})
    # More filler words and generic discourse markers (some in boilerplate)
    supplementary_stops.update({'trots', 'hela', 'komma', 'flera', 'första', 'flesta', 'själva', 'heller', 'bland', 'exempel', 'såväl', 'kring', 'även', 'mycket'})
    # Two-letter word artifacts from preprocessing (boilerplate removal, tokenization errors)
    supplementary_stops.update({'br', 'de', 'dg', 'di', 'fj', 'fr', 'ga', 'gg', 'gr', 'hb', 'hj', 'jd', 'ka', 'ld', 'lt', 'mf', 'nd', 'ne', 'ng', 'nk', 'ns', 'nt', 'oh', 'po', 'rb', 'rd', 'rk', 'rl', 'rn', 'rr', 'rs', 'rt', 'sa', 'sf', 'sj', 'sk', 'sl', 'sm', 'te', 'tg', 'tj', 'tr', 'tt', 'ut', 'vs'})
    stop_words.update(supplementary_stops)

    return stop_words


def remove_stopwords(text, stop_words):
    """Remove stop words from normalized text.

    Text is already lowercase and punctuation-free, so simple word matching works.
    Preserves line structure for reference/debugging.
    """
    if not text:
        return ""

    # Process line-by-line to preserve structure
    lines = text.split('\n')
    filtered_lines = []

    for line in lines:
        words = line.split()
        filtered_words = [word for word in words if word not in stop_words]
        filtered_lines.append(' '.join(filtered_words))

    return '\n'.join(filtered_lines)


def process_temporal_bin(input_file, output_file, stop_words):
    """Process one temporal bin: remove stop words."""
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

                # Remove stop words from normalized text
                text_cleaned = remove_stopwords(motion.get('text_normalized', ''), stop_words)

                # Update motion with cleaned text
                motion['text_no_stopwords'] = text_cleaned

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
    # Usage: python3 04_remove_stopwords.py [input_dir] [output_dir]
    # Default: data/output/normalized -> data/output/stopword_removed
    if len(sys.argv) >= 3:
        INPUT_DIR = Path(sys.argv[1])
        OUTPUT_DIR = Path(sys.argv[2])
    else:
        INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'normalized'
        OUTPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'stopword_removed'

    # Create output directory (with parents in case path doesn't exist)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
    total_malformed = 0

    print("=" * 60)
    print("STEP 3: Removing Swedish stop words")
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    for input_filename, output_filename in bins:
        input_file = INPUT_DIR / input_filename
        output_file = OUTPUT_DIR / output_filename

        if not input_file.exists():
            print(f"Error: {input_file} not found")
            continue

        count, malformed = process_temporal_bin(input_file, output_file, stop_words)
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
