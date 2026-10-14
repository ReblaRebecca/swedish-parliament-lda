#!/usr/bin/env python3
"""
Preprocess motion titles using same pipeline as body text.
Apply normalization, boilerplate removal, stopword removal, and lemmatization.
Store processed titles separately for weighting experiment.

Input: Raw titles from deduplicated/ JSONL files
Output: Processed titles in deduplicated/ files (new 'title_processed' field)
"""

import json
import re
from pathlib import Path
from collections import defaultdict

try:
    from nltk.corpus import stopwords
except ImportError:
    print("Error: NLTK not installed. Install with: pip install nltk")
    import sys
    sys.exit(1)


def load_boilerplate():
    """Load boilerplate phrases."""
    boilerplate_file = Path(__file__).parent.parent / 'config' / 'boilerplate_phrases.txt'
    phrases = []
    with open(boilerplate_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                phrases.append(line)
    return phrases


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
    supplementary_stops = {'ub', 'dvs', 'etc', 'osv', 'resp', 'eg', 'ca', 'frn', 'ky', 'et', 'tt', 'ib', 'ds', 'qz', 'iq', 'uö'}
    supplementary_stops.update({'uppåt', 'uppe', 'uppifrån', 'nedåt', 'nere', 'nedifrån', 'framåt', 'framme', 'framifrån', 'bakåt', 'bakom', 'bakifrån', 'inåt', 'inne', 'inifrån', 'utåt', 'ute', 'utifrån', 'ovanpå', 'ovanför', 'underifrån', 'undertill', 'bredvid', 'bortåt', 'borta', 'hit', 'dit', 'här', 'där', 'hemma', 'hemåt', 'varifrån', 'någonstans', 'överallt', 'ingenstans'})
    supplementary_stops.update({'ska', 'skall', 'blir', 'varit', 'blivit'})
    supplementary_stops.update({'kommer', 'enligt', 'genom', 'dock', 'fall', 'ge', 'ta', 'del', 'fler'})
    supplementary_stops.update({'olika', 'mer', 'behöver', 'vill', 'nya'})
    supplementary_stops.update({'göra', 'gör', 'gjort', 'gjorts', 'håll', 'håller', 'rör'})
    supplementary_stops.update({'inför', 'all', 'alls'})
    supplementary_stops.update({'sätt', 'sätts', 'visar', 'visat', 'viss', 'dels', 'finna', 'finnas'})
    supplementary_stops.update({'stora', 'rätt', 'bra', 'hos', 'se', 'går', 'bara', 'ser', 'både', 'samt'})
    # Two-letter word artifacts from preprocessing (boilerplate removal, tokenization errors)
    supplementary_stops.update({'br', 'de', 'dg', 'di', 'fj', 'fr', 'ga', 'gg', 'gr', 'hb', 'hj', 'jd', 'ka', 'ld', 'lt', 'mf', 'nd', 'ne', 'ng', 'nk', 'ns', 'nt', 'oh', 'po', 'rb', 'rd', 'rk', 'rl', 'rn', 'rr', 'rs', 'rt', 'sa', 'sf', 'sj', 'sk', 'sl', 'sm', 'te', 'tg', 'tj', 'tr', 'tt', 'ut', 'vs'})
    stop_words.update(supplementary_stops)

    return stop_words


def load_lemmatization():
    """Load lemmatization dictionary."""
    lem_file = Path(__file__).parent.parent / 'config' / 'controlled_lemmatization.csv'
    lemmas = {}
    with open(lem_file, 'r', encoding='utf-8') as f:
        f.readline()  # Skip header
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2:
                variant, lemma = parts
                lemmas[variant.lower()] = lemma.lower()
    return lemmas


def remove_boilerplate(text, boilerplate_phrases):
    """Remove boilerplate phrases from text."""
    text = text.lower()
    for phrase in boilerplate_phrases:
        if '*' in phrase:
            pattern = phrase.replace('*', r'\w*')
            text = re.sub(r'\b' + pattern + r'\b', '', text, flags=re.IGNORECASE)
        else:
            text = re.sub(r'\b' + re.escape(phrase) + r'\b', '', text, flags=re.IGNORECASE)
    return text


def normalize_text(text):
    """Normalize: lowercase, remove numbers/punctuation."""
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def remove_stopwords(text, stopwords):
    """Remove stopwords."""
    words = text.split()
    return ' '.join([w for w in words if w not in stopwords and len(w) > 1])


def apply_lemmatization(text, lemmas):
    """Apply lemmatization."""
    words = text.split()
    lemmatized = []
    for word in words:
        lemmatized.append(lemmas.get(word, word))
    return ' '.join(lemmatized)


def process_title(title, boilerplate_phrases, stopwords, lemmas):
    """Process title through full pipeline."""
    if not title or not title.strip():
        return ""

    # Remove boilerplate
    title = remove_boilerplate(title, boilerplate_phrases)

    # Normalize
    title = normalize_text(title)

    # Remove stopwords
    title = remove_stopwords(title, stopwords)

    # Lemmatize
    title = apply_lemmatization(title, lemmas)

    return title.strip()


def process_temporal_bin(input_file, output_file, boilerplate_phrases, stopwords, lemmas):
    """Process titles for one temporal bin. Read entire file first to avoid truncation."""
    motion_count = 0
    empty_titles = 0

    print(f"Processing {input_file.name}...")

    # Read all lines first (avoid truncation when output_file == input_file)
    motions = []
    with open(input_file, 'r', encoding='utf-8') as in_f:
        for line in in_f:
            try:
                motion = json.loads(line.strip())
                motions.append(motion)
            except json.JSONDecodeError:
                continue

    # Process and write
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for motion in motions:
            # Process title
            raw_title = motion.get('title', '')
            title_processed = process_title(raw_title, boilerplate_phrases, stopwords, lemmas)

            if not title_processed:
                empty_titles += 1

            # Add processed title to motion
            motion['title_processed'] = title_processed

            # Write to output with flush
            out_f.write(json.dumps(motion, ensure_ascii=False) + '\n')
            out_f.flush()
            motion_count += 1

            if motion_count % 1000 == 0:
                print(f"  Processed {motion_count} motions...")

    print(f"  Completed: {motion_count} motions, {empty_titles} empty titles")
    return motion_count, empty_titles


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'deduplicated'
    OUTPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'deduplicated'

    # Load preprocessing resources
    print("Loading boilerplate, stopwords, and lemmatization dictionary...")
    boilerplate_phrases = load_boilerplate()
    stopwords = get_swedish_stopwords()
    lemmas = load_lemmatization()

    print(f"  Boilerplate: {len(boilerplate_phrases)} phrases")
    print(f"  Stopwords: {len(stopwords)} words")
    print(f"  Lemmatization: {len(lemmas)} mappings")

    # Define temporal bins
    bins = [
        'group1_1986-1993.jsonl',
        'group2_1994-2004.jsonl',
        'group3_2005-2014.jsonl',
        'group4_2015-2025.jsonl',
    ]

    total_motions = 0
    total_empty = 0

    print("\n" + "=" * 60)
    print("PREPROCESSING MOTION TITLES")
    print(f"Input: {INPUT_DIR}")
    print("=" * 60)

    for bin_file in bins:
        input_file = INPUT_DIR / bin_file
        output_file = OUTPUT_DIR / bin_file

        if not input_file.exists():
            print(f"Error: {input_file} not found")
            continue

        count, empty = process_temporal_bin(input_file, output_file, boilerplate_phrases, stopwords, lemmas)
        total_motions += count
        total_empty += empty

    print("=" * 60)
    print(f"Total: {total_motions} motions processed")
    if total_motions > 0:
        print(f"Empty titles after processing: {total_empty} ({100*total_empty/total_motions:.2f}%)")
    else:
        print(f"⚠️  Warning: No motions processed")
    print(f"Output saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
