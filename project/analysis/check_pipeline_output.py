#!/usr/bin/env python3
"""
Sanity checks on the pipeline output (steps 01-05). Read-only: writes nothing.
Run after the pipeline (or after re-running steps 03-05) to catch broken or incomplete output.

FAIL = the output is wrong (missing motions, missing fields, stopwords or punctuation left, ...)
WARN = worth a look, may be legitimate (empty texts, known extraction fragments in the vocabulary)

Stages that have not been run yet are skipped, so the script can be used part-way through.

Usage: python3 check_pipeline_output.py [data_dir]
Default data_dir: data/ (expects input/extracted_text_xml/ and output/<stage>/ under it)
Exit code 1 if any check fails.
"""

import importlib.util
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from periods import PERIOD_FILES, period_of_session  # noqa: E402

BINS = PERIOD_FILES

# Stage directory (relative to data_dir) -> fields every motion must have after that stage
STAGES = [
    ('input/extracted_text_xml', ['dok_id', 'date', 'session', 'title', 'title_text', 'text', 'authors', 'author_names']),
    ('output/lemmatized', ['tokens', 'title_tokens']),
    ('output/boilerplate_removed', ['text_no_boilerplate', 'title_no_boilerplate']),
    ('output/normalized', ['text_normalized', 'title_normalized']),
    ('output/stopword_removed', ['text_no_stopwords', 'title_processed']),
]

# Fragments created by the old extraction bug (see docs/PREPROCESSING_ARTIFACTS.md); should now be (nearly) gone
KNOWN_FRAGMENTS = {'ning', 'ningen', 'ningar', 'skol', 'arbets', 'utbild', 'beh', 'nda', 'lder', 'ldre', 'mne', 'arbetsl', 'nyanl'}

# A fragment found in more than this share of motions is reported
FRAGMENT_WARN_SHARE = 0.001

SPACING_DIACRITICS = re.compile('[aAoO][°¨]')
# Final text: lowercase letters only, words separated by single spaces, one sentence per line
FINAL_TEXT_ALLOWED = re.compile(r'^[^\W\d_A-ZÅÄÖ]+(?: [^\W\d_A-ZÅÄÖ]+)*$')


class Report:
    def __init__(self):
        self.failures = 0
        self.warnings = 0

    def ok(self, message):
        print(f"  ok    {message}")

    def fail(self, message, examples=()):
        self.failures += 1
        print(f"  FAIL  {message}")
        for example in list(examples)[:5]:
            print(f"          e.g. {example}")

    def warn(self, message, examples=()):
        self.warnings += 1
        print(f"  WARN  {message}")
        for example in list(examples)[:5]:
            print(f"          e.g. {example}")

    def check(self, failing, message, examples=()):
        """Report ok if nothing is failing, else FAIL with examples."""
        if failing:
            self.fail(f"{message}: {len(failing)}", examples or failing)
        else:
            self.ok(message)


def read_motions(path):
    """Yield (line number, motion or None if malformed) for a JSONL file."""
    with open(path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            try:
                yield line_number, json.loads(line)
            except json.JSONDecodeError:
                yield line_number, None


def check_structure(report, stage_dir, required_fields, reference_ids):
    """Every bin present, no malformed lines, no duplicate dok_ids, same motions as extraction, fields present.

    Returns {bin: [dok_id, ...]} for this stage.
    """
    ids_by_bin = {}
    malformed, missing_fields, missing_bins = [], [], []

    for bin_name in BINS:
        path = stage_dir / bin_name
        if not path.exists():
            missing_bins.append(bin_name)
            continue
        ids = []
        for line_number, motion in read_motions(path):
            if motion is None:
                malformed.append(f"{bin_name} line {line_number}")
                continue
            ids.append(motion.get('dok_id'))
            absent = [field for field in required_fields if field not in motion]
            if absent:
                missing_fields.append(f"{motion.get('dok_id')} missing {absent}")
        ids_by_bin[bin_name] = ids

    report.check(missing_bins, "all four period files present")
    report.check(malformed, "no malformed JSON lines")
    report.check(missing_fields, f"fields present: {', '.join(required_fields)}")

    duplicates = [f"{bin_name}: {dok_id}" for bin_name, ids in ids_by_bin.items()
                  for dok_id, n in Counter(ids).items() if n > 1]
    report.check(duplicates, "no dok_id written twice")

    total = sum(len(ids) for ids in ids_by_bin.values())
    if reference_ids is None:
        report.ok(f"{total} motions")
    else:
        differences = []
        for bin_name, ids in ids_by_bin.items():
            missing = set(reference_ids.get(bin_name, [])) - set(ids)
            extra = set(ids) - set(reference_ids.get(bin_name, []))
            if missing or extra:
                differences.append(f"{bin_name}: {len(missing)} missing, {len(extra)} extra "
                                   f"(e.g. {sorted(missing or extra)[:3]})")
        expected = sum(len(ids) for ids in reference_ids.values())
        report.check(differences, f"same motions as extraction ({total} of {expected})")

    return ids_by_bin


def check_extracted(report, stage_dir):
    """Extraction repairs applied: no soft hyphens, no spacing diacritics, NFC text; titles present;
    every motion in the file of its session's period."""
    bad_chars, empty_text, empty_title, wrong_period = [], [], [], []
    for bin_name in BINS:
        path = stage_dir / bin_name
        if not path.exists():
            continue
        for _, motion in read_motions(path):
            if motion is None:
                continue
            dok_id = motion.get('dok_id')
            if period_of_session(motion.get('session')) != Path(bin_name).stem:
                wrong_period.append(f"{dok_id} ({motion.get('session')!r} in {bin_name})")
            for field in ('text', 'title_text'):
                value = motion.get(field) or ''
                if '\xad' in value or SPACING_DIACRITICS.search(value) or not unicodedata.is_normalized('NFC', value):
                    bad_chars.append(f"{dok_id} ({field})")
            if not (motion.get('text') or '').strip():
                empty_text.append(dok_id)
            if not (motion.get('title_text') or '').strip():
                empty_title.append(dok_id)

    report.check(wrong_period, "every motion in the period of its session")
    report.check(bad_chars, "no soft hyphens, spacing diacritics or non-NFC text")
    report.check(empty_text, "no empty body text")
    if empty_title:
        report.warn(f"motions with empty title: {len(empty_title)}", empty_title)
    else:
        report.ok("no empty titles")


def is_token_list(value):
    """A list of sentences, each a list of [word, lemma, upos] string triples."""
    return isinstance(value, list) and all(
        isinstance(sentence, list) and all(
            isinstance(token, list) and len(token) == 3 and all(isinstance(x, str) for x in token)
            for token in sentence)
        for sentence in value)


def check_lemmatized(report, stage_dir):
    """Stanza output has the right shape and every non-empty text was tagged."""
    bad_shape, untagged = [], []
    for bin_name in BINS:
        path = stage_dir / bin_name
        if not path.exists():
            continue
        for _, motion in read_motions(path):
            if motion is None:
                continue
            dok_id = motion.get('dok_id')
            for text_field, token_field in (('text', 'tokens'), ('title_text', 'title_tokens')):
                value = motion.get(token_field)
                if not is_token_list(value):
                    bad_shape.append(f"{dok_id} ({token_field})")
                elif (motion.get(text_field) or '').strip() and not value:
                    untagged.append(f"{dok_id} ({token_field})")

    report.check(bad_shape, "tokens are sentences of [word, lemma, upos]")
    report.check(untagged, "every non-empty text and title was tagged")


def load_stopwords():
    path = PROJECT_ROOT / 'preprocessing' / '05_remove_stopwords.py'
    spec = importlib.util.spec_from_file_location('remove_stopwords', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_swedish_stopwords()


def check_final(report, stage_dir):
    """Final model text: clean format, no stopwords left; report empty texts and known fragments."""
    stop_words = load_stopwords()
    bad_format, stopwords_left, short_words = [], [], []
    empty_text, empty_title = [], []
    fragment_docs = Counter()
    total = 0

    for bin_name in BINS:
        path = stage_dir / bin_name
        if not path.exists():
            continue
        for _, motion in read_motions(path):
            if motion is None:
                continue
            total += 1
            dok_id = motion.get('dok_id')
            text = motion.get('text_no_stopwords') or ''
            title = motion.get('title_processed') or ''

            if not text.strip():
                empty_text.append(dok_id)
            if not title.strip():
                empty_title.append(dok_id)

            # Empty lines are allowed in the body (lines left empty after stopword removal)
            lines = [line for line in text.split('\n') if line] + ([title] if title else [])
            if any(not FINAL_TEXT_ALLOWED.match(line) for line in lines):
                bad_format.append(dok_id)

            words = set(text.split()) | set(title.split())
            left = words & stop_words
            if left:
                stopwords_left.append(f"{dok_id}: {sorted(left)[:5]}")
            if any(len(w) < 2 for w in words):
                short_words.append(dok_id)
            for fragment in words & KNOWN_FRAGMENTS:
                fragment_docs[fragment] += 1

    report.check(bad_format, "final text is lowercase letters only, single spaces, no digits or punctuation")
    report.check(short_words, "no single-character words")
    report.check(stopwords_left, "no stopwords left in text or title")

    if empty_text:
        report.warn(f"motions with empty final text: {len(empty_text)}", empty_text)
    else:
        report.ok("no empty final texts")
    if empty_title:
        report.warn(f"motions with empty final title (titles are kept for later use; the model uses body text only): {len(empty_title)}", empty_title)
    else:
        report.ok("no empty final titles")

    frequent = {f: n for f, n in fragment_docs.items() if total and n / total > FRAGMENT_WARN_SHARE}
    if frequent:
        report.warn("known extraction fragments still frequent (motions containing them)",
                    [f"{f}: {n}" for f, n in sorted(frequent.items(), key=lambda x: -x[1])])
    else:
        report.ok("known extraction fragments rare or absent")


def main():
    data_dir = Path(sys.argv[1]) if len(sys.argv) >= 2 else PROJECT_ROOT / 'data'
    report = Report()
    reference_ids = None

    print("=" * 70)
    print(f"Checking pipeline output in {data_dir}")
    print("=" * 70)

    for relative_dir, fields in STAGES:
        stage_dir = data_dir / relative_dir
        print(f"\n{relative_dir}")
        if not stage_dir.exists():
            print("  skip  not run yet")
            continue

        ids_by_bin = check_structure(report, stage_dir, fields, reference_ids)
        if reference_ids is None:
            reference_ids = ids_by_bin

        if relative_dir == 'input/extracted_text_xml':
            check_extracted(report, stage_dir)
        elif relative_dir == 'output/lemmatized':
            check_lemmatized(report, stage_dir)
        elif relative_dir == 'output/stopword_removed':
            check_final(report, stage_dir)

    print("\n" + "=" * 70)
    print(f"{report.failures} failed, {report.warnings} warnings")
    print("=" * 70)
    sys.exit(1 if report.failures else 0)


if __name__ == '__main__':
    main()
