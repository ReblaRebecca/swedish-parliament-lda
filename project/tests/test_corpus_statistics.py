#!/usr/bin/env python3
"""
Tests for analysis/corpus_statistics.py: words and different words per pipeline step.
Small synthetic motions with known answers; no corpus or fitted models needed.

Run from project/:
    python -m unittest discover -s tests -v
"""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from sklearn.feature_extraction.text import CountVectorizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from periods import PERIOD_FILES  # noqa: E402

spec = importlib.util.spec_from_file_location('corpus_statistics', PROJECT_ROOT / 'analysis' / 'corpus_statistics.py')
stats = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stats)


class TestWords(unittest.TestCase):
    """What counts as a word."""

    def test_stanza_forms_and_lemmas_are_the_same_tokens(self):
        tokens = [[['Skolorna', 'skola', 'NOUN'], ['6:e', '6:', 'ADJ'], ['.', '.', 'PUNCT'], ['2007', '2007', 'NUM']]]
        forms, lemmas = stats.stanza_words(tokens)
        self.assertEqual(forms, ['Skolorna', '6:e'])
        # The lemma of '6:e' has no letter but is still counted: one lemma per word form
        self.assertEqual(lemmas, ['skola', '6:'])

    def test_lemma_text(self):
        self.assertEqual(stats.lemma_text_words('skola 2007 elev\nlärare'), ['skola', 'elev', 'lärare'])

    def test_different_words_ignore_case(self):
        count = stats.Count()
        count.add(['Skola', 'skola', 'SKOLA', 'elev'])
        count.add(['elev'])
        row = count.row('test')
        self.assertEqual((row['words'], row['different']), (5, 2))
        self.assertEqual((row['median'], row['mean']), (2.5, 2.5))


def write_stage(data_dir, stage, motions):
    """Write motions to the first period file of a stage; the other period files are empty."""
    directory = data_dir / stage
    directory.mkdir(parents=True)
    for i, name in enumerate(PERIOD_FILES):
        with open(directory / name, 'w', encoding='utf-8') as f:
            for motion in (motions if i == 0 else []):
                f.write(json.dumps(motion, ensure_ascii=False) + '\n')


class TestStepCounts(unittest.TestCase):
    """Two motions through every step; the expected counts are worked out by hand."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        data = Path(cls.tmp.name)
        write_stage(data, 'output/lemmatized', [
            {'tokens': [[['Skolan', 'skola', 'NOUN'], ['och', 'och', 'CCONJ'], ['skolorna', 'skola', 'NOUN'],
                         ['.', '.', 'PUNCT']], [['Skolan', 'skola', 'NOUN'], ['!', '!', 'PUNCT']]]},
            {'tokens': [[['Lärare', 'lärare', 'NOUN'], ['2025', '2025', 'NUM']]]},
        ])
        write_stage(data, 'output/boilerplate_removed', [
            {'text_no_boilerplate': 'skola och skola\nskola'}, {'text_no_boilerplate': 'lärare 2025'}])
        write_stage(data, 'output/normalized', [
            {'text_normalized': 'skola och skola\nskola'}, {'text_normalized': 'lärare'}])
        write_stage(data, 'output/stopword_removed', [
            {'text_no_stopwords': 'skola skola\nskola'}, {'text_no_stopwords': 'lärare'}])
        # Stanza's tokens of the extracted text 'Skolan och skolorna. Skolan! Lärare 2025'
        cls.rows = dict(zip(['01', '02', '03', '04', '05'], stats.step_counts(data)))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def counts(self, step):
        r = self.rows[step]
        return r['words'], r['different']

    def test_extraction_counted_as_stanza_tokens(self):
        # Skolan, och, skolorna, Skolan, Lärare (no '.', '!', '2025'): 5 words; skolan, och, skolorna, lärare: 4 different
        self.assertEqual(self.counts('01'), (5, 4))
        self.assertEqual(self.rows['01']['median'], 2.5)

    def test_lemmatization_keeps_the_words_and_merges_forms(self):
        # Each word is replaced by its lemma: same number of words, fewer different words
        self.assertEqual(self.counts('02'), (5, 3))  # skolan, skolorna -> skola
        self.assertEqual(self.rows['02']['median'], self.rows['01']['median'])

    def test_later_steps(self):
        self.assertEqual(self.counts('03'), (5, 3))  # '2025' is not a word
        self.assertEqual(self.counts('04'), (5, 3))
        self.assertEqual(self.counts('05'), (4, 2))  # stopword 'och' removed

    def test_one_row_per_step_in_order(self):
        self.assertEqual([r['step'][:2] for r in self.rows.values()], ['01', '02', '03', '04', '05'])
        self.assertIn('lemmas', self.rows['02']['step'])


class TestVocabularyCounts(unittest.TestCase):

    def test_words_inside_the_vocabularies(self):
        final = {PERIOD_FILES[0]: ['skola elev skola', 'lärare'], PERIOD_FILES[1]: ['student elev']}
        whole = CountVectorizer(vocabulary=['skola', 'elev'])
        period = {PERIOD_FILES[0]: CountVectorizer().fit(['skola lärare']),
                  PERIOD_FILES[1]: CountVectorizer().fit(['student'])}
        whole_row, periods_row, per_period = stats.vocabulary_counts(final, whole, period)
        # Whole corpus: skola, elev, skola + elev = 4 words in a 2-word vocabulary; per motion 3, 0, 1
        self.assertEqual((whole_row['words'], whole_row['different']), (4, 2))
        self.assertEqual(whole_row['median'], 1)
        # Periods: skola, skola, lärare (3) + student (1); vocabularies {skola, lärare} and {student}
        self.assertEqual(per_period, [(PERIOD_FILES[0], 2, 3, 2), (PERIOD_FILES[1], 1, 1, 1)])
        self.assertEqual((periods_row['words'], periods_row['different']), (4, 3))


if __name__ == '__main__':
    unittest.main()
