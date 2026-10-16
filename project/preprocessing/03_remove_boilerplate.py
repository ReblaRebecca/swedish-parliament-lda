#!/usr/bin/env python3
"""
Remove Swedish parliamentary boilerplate from tagged motion text and titles (STEP 3).
Phrases from config/boilerplate_phrases.txt are matched against the ORIGINAL word forms
saved by the Stanza step, so the phrase list keeps its surface forms ("riksdagen",
"med anledning av"). The output is the LEMMAS of the remaining words.
Auxiliary verbs (UPOS AUX), punctuation and symbols are dropped from the output: Stanza
lemmatizes the modal 'ska/skall/skulle' to 'skola', which would merge with the noun
'skola' (school), and all auxiliaries are stopwords anyway.
Words whose lemma contains an underscore are dropped too: Stanza expands abbreviations into
multi-word lemmas ('t.ex.' -> 'till_exempel', 'bl.a.' -> 'bland_annat'), which would otherwise
become single tokens in the model. They are counted, with their word forms, in
underscore_lemmas.json in the output directory, so the most frequent ones can be reviewed.

Cheap to re-run: edit the phrase list and run this step again, no need to re-run Stanza.

Input: JSON lines with 'tokens' and 'title_tokens' fields (sentences of [word, lemma, upos]).
Output: JSON lines with 'text_no_boilerplate' and 'title_no_boilerplate' fields
        (lemmas, one sentence per line).
"""

import bisect
import json
import re
from collections import Counter, defaultdict
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


# Parts of speech left out of the output
SKIP_UPOS = {'AUX', 'PUNCT', 'SYM'}


def remove_boilerplate(sentences, boilerplate_patterns, underscore_counts=None):
    """Remove boilerplate phrases (matched on word forms) and return the remaining lemmas.

    sentences: list of sentences, each a list of [word, lemma, upos] triples.
    A word is removed only if a phrase match covers the whole word.
    Words with an underscore lemma are dropped; if underscore_counts (lemma -> Counter of
    word forms) is given, each dropped word is counted there.
    Returns lemmas as text, one sentence per line.
    """
    if not sentences:
        return ""

    # Word forms joined by spaces, sentences by newlines (phrases never match across sentences)
    words = [token for sentence in sentences for token in sentence]
    starts, ends, parts, pos = [], [], [], 0
    for s_idx, sentence in enumerate(sentences):
        for w_idx, (form, _, _) in enumerate(sentence):
            starts.append(pos)
            ends.append(pos + len(form))
            parts.append(form)
            pos += len(form)
            parts.append(' ' if w_idx < len(sentence) - 1 else '\n')
            pos += 1
    text = ''.join(parts)

    removed = [False] * len(words)
    for pattern in boilerplate_patterns:
        for match in pattern.finditer(text):
            i = bisect.bisect_left(starts, match.start())
            while i < len(words) and starts[i] < match.end():
                if ends[i] <= match.end():
                    removed[i] = True
                i += 1

    lines, i = [], 0
    for sentence in sentences:
        lemmas = []
        for form, lemma, upos in sentence:
            if removed[i] or upos in SKIP_UPOS:
                pass
            elif '_' in lemma:
                if underscore_counts is not None:
                    underscore_counts[lemma][form] += 1
            else:
                lemmas.append(lemma)
            i += 1
        if lemmas:
            lines.append(' '.join(lemmas))

    return '\n'.join(lines)


def save_underscore_counts(underscore_counts, output_file):
    """Write dropped underscore lemmas, most frequent first, with their word forms."""
    rows = sorted(underscore_counts.items(), key=lambda item: -sum(item[1].values()))
    summary = {
        lemma: {'count': sum(forms.values()), 'forms': dict(forms.most_common())}
        for lemma, forms in rows
    }
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


def process_temporal_bin(input_file, output_file, boilerplate_patterns, underscore_counts):
    """Process one temporal bin: remove boilerplate from body and title."""
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

                motion['text_no_boilerplate'] = remove_boilerplate(motion.pop('tokens', []), boilerplate_patterns, underscore_counts)
                motion['title_no_boilerplate'] = remove_boilerplate(motion.pop('title_tokens', []), boilerplate_patterns, underscore_counts)
                # The per-word Stanza output stays in data/output/lemmatized/; later steps only need the lemmas

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
    # Default: data/output/lemmatized -> data/output/boilerplate_removed with config/boilerplate_phrases.txt
    if len(sys.argv) >= 3:
        INPUT_DIR = Path(sys.argv[1])
        OUTPUT_DIR = Path(sys.argv[2])
        PHRASES_FILE = Path(sys.argv[3]) if len(sys.argv) >= 4 else PROJECT_ROOT / 'config' / 'boilerplate_phrases.txt'
    else:
        INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'lemmatized'
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
    # Dropped underscore lemmas across all bins: lemma -> Counter of word forms
    underscore_counts = defaultdict(Counter)

    print("=" * 60)
    print("STEP 3: Removing parliamentary boilerplate (body and title)")
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

        count, malformed = process_temporal_bin(input_file, output_file, BOILERPLATE_PATTERNS, underscore_counts)
        total_motions += count
        total_malformed += malformed

    print("=" * 60)
    print(f"Total: {total_motions} motions processed")
    underscore_file = OUTPUT_DIR / 'underscore_lemmas.json'
    save_underscore_counts(underscore_counts, underscore_file)
    dropped = sum(sum(forms.values()) for forms in underscore_counts.values())
    print(f"Underscore lemmas dropped: {dropped} words, {len(underscore_counts)} distinct -> {underscore_file.name}")
    if total_malformed > 0:
        print(f"⚠️  Warning: {total_malformed} malformed JSON lines skipped")
    print(f"Output saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
