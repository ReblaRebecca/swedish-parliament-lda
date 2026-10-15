#!/usr/bin/env python3
"""
Lemmatize motion text with Stanza (STEP 3).
Runs on boilerplate-removed running text, so the tagger sees full sentences
(punctuation, function words and word order are still present).
Input: JSON lines with 'text_no_boilerplate' field.
Output: JSON lines with 'text_lemmatized' field (lemmas, one sentence per line).

Auxiliary verbs (UPOS AUX) are dropped: Stanza lemmatizes the modal 'ska/skall/skulle'
to 'skola', which would merge with the noun 'skola' (school). All auxiliaries are
stopwords anyway. Punctuation and symbols are dropped as well.

Resumable: motions already present in the output file are skipped, so an interrupted
run continues where it stopped.
"""

import json
import sys
import time
from pathlib import Path

try:
    import stanza
except ImportError:
    print("Error: Stanza not installed. Install with: pip install stanza")
    sys.exit(1)


# Parts of speech left out of the lemmatized text
SKIP_UPOS = {'AUX', 'PUNCT', 'SYM'}

# Number of motions sent to Stanza at once
BATCH_SIZE = 32


def load_pipeline():
    """Load the Swedish Stanza pipeline (downloads the model on first use)."""
    return stanza.Pipeline(
        'sv',
        processors='tokenize,pos,lemma',
        logging_level='WARN',
    )


def lemmatize_texts(nlp, texts):
    """Lemmatize a batch of texts. Returns one string per text, one sentence per line."""
    results = [''] * len(texts)
    non_empty = [i for i, t in enumerate(texts) if t and t.strip()]
    if not non_empty:
        return results

    docs = nlp([stanza.Document([], text=texts[i]) for i in non_empty])

    for i, doc in zip(non_empty, docs):
        lines = []
        for sentence in doc.sentences:
            lemmas = [word.lemma or word.text for word in sentence.words if word.upos not in SKIP_UPOS]
            if lemmas:
                lines.append(' '.join(lemmas))
        results[i] = '\n'.join(lines)

    return results


def load_completed(output_file):
    """Return dok_ids already written to output_file, dropping a truncated last line if present."""
    if not output_file.exists():
        return set()

    valid_lines = []
    with open(output_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                json.loads(line)
                valid_lines.append(line)
            except json.JSONDecodeError:
                continue

    # Rewrite without any partial line from an interrupted run
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(valid_lines)

    return {json.loads(line).get('dok_id') for line in valid_lines}


def process_temporal_bin(input_file, output_file, nlp):
    """Process one temporal bin: lemmatize boilerplate-removed text."""
    motion_count = 0
    skipped_count = 0
    malformed_count = 0

    print(f"Processing {input_file.name}...")

    completed = load_completed(output_file)
    if completed:
        print(f"  Resuming: {len(completed)} motions already lemmatized")

    pending = []
    with open(input_file, 'r', encoding='utf-8') as in_f:
        for line in in_f:
            try:
                motion = json.loads(line.strip())
            except json.JSONDecodeError:
                malformed_count += 1
                continue
            if motion.get('dok_id') in completed:
                skipped_count += 1
                continue
            pending.append(motion)

    start = time.time()
    with open(output_file, 'a', encoding='utf-8') as out_f:
        for batch_start in range(0, len(pending), BATCH_SIZE):
            batch = pending[batch_start:batch_start + BATCH_SIZE]
            lemmatized = lemmatize_texts(nlp, [m.get('text_no_boilerplate', '') for m in batch])

            for motion, text_lemmatized in zip(batch, lemmatized):
                motion['text_lemmatized'] = text_lemmatized
                out_f.write(json.dumps(motion, ensure_ascii=False) + '\n')
            out_f.flush()

            motion_count += len(batch)
            elapsed = time.time() - start
            remaining = (len(pending) - motion_count) * elapsed / motion_count
            print(f"  {motion_count}/{len(pending)} motions ({elapsed / 60:.1f} min elapsed, ~{remaining / 60:.0f} min left)")

    print(f"  Completed: {motion_count} motions lemmatized, {skipped_count} already done, {malformed_count} malformed JSON skipped")
    return motion_count, malformed_count


def main():
    # Configuration
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent

    # Allow command-line arguments for input/output directories
    # Usage: python3 03_lemmatize.py [input_dir] [output_dir]
    # Default: data/output/boilerplate_removed -> data/output/lemmatized
    if len(sys.argv) >= 3:
        INPUT_DIR = Path(sys.argv[1])
        OUTPUT_DIR = Path(sys.argv[2])
    else:
        INPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'boilerplate_removed'
        OUTPUT_DIR = PROJECT_ROOT / 'data' / 'output' / 'lemmatized'

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
    print("STEP 3: Lemmatizing text with Stanza")
    print(f"Stanza version: {stanza.__version__}")
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    nlp = load_pipeline()

    for input_filename, output_filename in bins:
        input_file = INPUT_DIR / input_filename
        output_file = OUTPUT_DIR / output_filename

        if not input_file.exists():
            print(f"Error: {input_file} not found")
            continue

        count, malformed = process_temporal_bin(input_file, output_file, nlp)
        total_motions += count
        total_malformed += malformed

    print("=" * 60)
    print(f"Total: {total_motions} motions lemmatized")
    if total_malformed > 0:
        print(f"⚠️  Warning: {total_malformed} malformed JSON lines skipped")
    print(f"Output saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
