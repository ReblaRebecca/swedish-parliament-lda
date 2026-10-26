#!/usr/bin/env python3
"""
Tests for the period models (modeling/15_fit_period_lda.py), their seed-stability test
(analysis/16_seed_stability_periods.py) and the per-period text loading in lda_common.py.
Small synthetic data only: no corpus or fitted models needed.

Run from project/:
    python -m unittest discover -s tests -v
"""

import contextlib
import importlib.util
import io
import json
import re
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'modeling'))
sys.path.insert(0, str(PROJECT_ROOT / 'analysis'))

import lda_common  # noqa: E402
import seed_stability  # noqa: E402
from topic_matching import match_and_evaluate  # noqa: E402


def load_script(relative_path):
    """Import a script as a module (file names start with digits, so plain import fails)."""
    path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(re.sub(r'\W', '_', path.stem), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


period_models = load_script('modeling/15_fit_period_lda.py')
period_stability = load_script('analysis/16_seed_stability_periods.py')
period_explorer = load_script('modeling/17_generate_period_explorer.py')


def quiet(function, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return function(*args, **kwargs)


BINS = {
    'group1_1985-1994.jsonl': [
        {'dok_id': 'A', 'date': '1985-01-01', 'session': '1985/86', 'text_no_stopwords': 'skola lärare elev'},
        {'dok_id': 'B', 'date': '1991-01-01', 'session': '1990/91', 'text_no_stopwords': '\n'},  # withdrawn: no words
    ],
    'group2_1994-2006.jsonl': [
        {'dok_id': 'C', 'date': '1995-01-01', 'session': '1994/95', 'text_no_stopwords': 'universitet forskning'},
        {'dok_id': 'D', 'date': '1996-01-01', 'session': '1995/96', 'text_no_stopwords': ''},
    ],
    'group3_2006-2014.jsonl': [{'dok_id': 'E', 'date': '2010-01-01', 'session': '2009/10', 'text_no_stopwords': 'förskola barn'}],
    'group4_2014-2026.jsonl': [{'dok_id': 'F', 'date': '2026-04-01', 'session': '2025/26', 'text_no_stopwords': 'digitalisering elev'}],
}


def write_bins(directory, extra_line_in_first=None):
    for name, motions in BINS.items():
        with open(Path(directory) / name, 'w', encoding='utf-8') as f:
            for motion in motions:
                f.write(json.dumps(motion, ensure_ascii=False) + '\n')
            if extra_line_in_first and name.startswith('group1'):
                f.write(extra_line_in_first + '\n')


class TestPeriodLoading(unittest.TestCase):
    """The period models use exactly the motions of the whole-corpus model, split by period."""

    def setUp(self):
        # Short synthetic texts: the length minimum is tested in TestMinimumLength
        patcher = mock.patch.object(lda_common, 'MIN_WORDS', 1)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_periods_in_order_with_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_bins(tmp)
            periods, _ = lda_common.load_period_body_texts(Path(tmp))
        self.assertEqual(list(periods), ['1985-1994', '1994-2006', '2006-2014', '2014-2026'])
        self.assertEqual([m['doc_id'] for m in periods['1985-1994'][1]], ['A'])
        self.assertEqual(periods['1994-2006'][0], ['universitet forskning'])

    def test_same_motions_as_whole_corpus(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_bins(tmp, extra_line_in_first='{not json')
            periods, period_malformed = lda_common.load_period_body_texts(Path(tmp))
            texts, metadata, malformed = lda_common.load_body_texts(Path(tmp))
        self.assertEqual([t for p_texts, _ in periods.values() for t in p_texts], texts)
        self.assertEqual([m for _, p_meta in periods.values() for m in p_meta], metadata)
        self.assertEqual([m['doc_id'] for m in metadata], ['A', 'C', 'E', 'F'])  # empty bodies skipped
        self.assertEqual(period_malformed, malformed)
        self.assertEqual(malformed, 1)

    def test_period_label(self):
        self.assertEqual(lda_common.period_label(Path('x/group2_1994-2006.jsonl')), '1994-2006')

    def test_period_display_names(self):
        # Pages and reports name the periods by their parliamentary sessions
        self.assertEqual([lda_common.period_display(p) for p in ['1985-1994', '1994-2006', '2006-2014', '2014-2026']],
                         ['1985/86–1993/94', '1994/95–2005/06', '2006/07–2013/14', '2014/15–2025/26'])

    def test_metadata_carries_session_and_period(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_bins(tmp)
            _, metadata, _ = lda_common.load_body_texts(Path(tmp))
        self.assertEqual([(m['session'], m['period']) for m in metadata],
                         [('1985/86', '1985-1994'), ('1994/95', '1994-2006'), ('2009/10', '2006-2014'), ('2025/26', '2014-2026')])


class TestPeriodModels(unittest.TestCase):
    """Each period model has its own vocabulary (Gordon); adjacent periods are compared over shared words."""

    @classmethod
    def setUpClass(cls):
        words = ['skola', 'lärare', 'elev', 'universitet', 'forskning', 'student', 'förskola', 'barn',
                 'digitalisering', 'betyg']
        # 40 motions per period; period i uses words 2i..2i+3, each in 10 motions (the minimum kept),
        # 'common' in 12 motions of every period and 'rare' in one (below the minimum)
        cls.periods = {}
        for i, period in enumerate(['1985-1994', '1994-2006', '2006-2014', '2014-2026']):
            texts = [' '.join([words[2 * i + j % 4]] * 10) for j in range(40)]
            for j in range(12):
                texts[j] += ' common'
            texts[0] += ' rare'
            cls.periods[period] = (texts, [{}] * 40)
        cls.vectorizers = period_models.period_vectorizers(cls.periods)
        cls.models = quiet(period_models.fit_period_models, cls.periods, cls.vectorizers, num_topics=3)

    def test_one_model_per_period_with_shared_settings(self):
        self.assertEqual(list(self.models), list(self.periods))
        for lda, _ in self.models.values():
            params = lda.get_params()
            self.assertEqual(params['n_components'], 3)
            self.assertEqual(params['random_state'], lda_common.DEFAULT_SEED)
            for key, value in lda_common.LDA_PARAMS.items():
                self.assertEqual(params[key], value, key)

    def test_vocabulary_built_within_each_period(self):
        # Period i uses words 2i..2i+3 only; its vocabulary holds those words that pass the limits
        for i, (period, (lda, vocab)) in enumerate(self.models.items()):
            texts = self.periods[period][0]
            self.assertEqual(lda.components_.shape[1], len(vocab), period)
            self.assertEqual(set(vocab) - {'common'}, set(w for t in texts for w in t.split()) - {'common', 'rare'}, period)
        self.assertNotIn('digitalisering', self.models['1985-1994'][1])
        self.assertIn('digitalisering', self.models['2014-2026'][1])

    def test_gordon_document_frequency_limits(self):
        self.assertEqual(lda_common.VECTORIZER_PARAMS, {'min_df': 10, 'max_df': 0.5})
        for period, (_, vocab) in self.models.items():
            self.assertIn('common', vocab, period)   # in 12 of 40 motions: kept
            self.assertNotIn('rare', vocab, period)  # in 1 motion: below 10
        # A word in more than half of a period's motions is dropped in that period
        texts = ['skola elev'] * 10 + ['skola lärare'] * 10 + ['skola'] * 5  # skola in all, elev and lärare in 10 of 25
        vocab = lda_common.fit_period_vectorizer(texts).get_feature_names_out()
        self.assertEqual(list(vocab), ['elev', 'lärare'])

    def test_adjacent_periods_matched_over_shared_words(self):
        (lda1, vocab1), (lda2, vocab2) = self.models['1985-1994'], self.models['1994-2006']
        self.assertFalse(np.array_equal(vocab1, vocab2))
        matches, _, _ = match_and_evaluate(lda1, lda2, vocab1, vocab2, shared_vocabulary=True)
        self.assertEqual(len(matches), 3)
        with self.assertRaises(ValueError):  # without the shared-vocabulary step, a mismatch is an error
            match_and_evaluate(lda1, lda2, vocab1, vocab2)

    def test_top_words_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'period_topics.csv'
            quiet(period_models.save_top_words, self.models, 3, output)
            lines = output.read_text(encoding='utf-8').splitlines()
        self.assertEqual(len(lines), 1 + 4 * 3)  # header + 3 topics x 4 periods
        self.assertTrue(lines[1].startswith('1985-1994,1,'))

    def test_period_scripts_use_shared_functions(self):
        self.assertIs(period_models.fit_lda_model, lda_common.fit_lda_model)
        self.assertIs(period_models.load_period_body_texts, lda_common.load_period_body_texts)
        self.assertIs(period_stability.load_period_body_texts, lda_common.load_period_body_texts)
        self.assertIs(period_stability.fit_period_vectorizer, lda_common.fit_period_vectorizer)
        self.assertIs(period_stability.run_seed_stability, seed_stability.run_seed_stability)


class TestPeriodStabilitySummary(unittest.TestCase):

    def setUp(self):
        # 3 topics, seeds 42/123/456; topic 1 found in both, topic 2 in one, topic 3 in none
        cosines = {(42, 123): [0.9, 0.8, 0.2], (42, 456): [0.95, 0.3, 0.1], (123, 456): [0.5, 0.5, 0.5]}
        self.pairwise = {pair: {'matches': [(t, t, c, 0.5) for t, c in enumerate(values)]}
                         for pair, values in cosines.items()}
        self.rows = seed_stability.per_topic_stability(self.pairwise, 42, 3)

    def test_summarize(self):
        s = period_stability.summarize(self.pairwise, self.rows)
        self.assertEqual(s['num_topics'], 3)
        self.assertEqual(s['others'], 2)
        self.assertEqual((s['found_all'], s['found_none']), (1, 1))
        self.assertEqual(s['stable'], 2)  # found in at least 1 of 2 other models
        self.assertAlmostEqual(s['mean_cosine'], np.mean([np.mean([0.9, 0.8, 0.2]), np.mean([0.95, 0.3, 0.1]), 0.5]))
        self.assertAlmostEqual(s['min_pair'], 0.45)
        self.assertAlmostEqual(s['max_pair'], np.mean([0.9, 0.8, 0.2]))

    def test_summary_report_has_one_row_per_period_and_count(self):
        s = period_stability.summarize(self.pairwise, self.rows)
        report = period_stability.summary_report({('1985-1994', 3): s, ('1994-2006', 3): s})
        self.assertIn('| 1985/86–1993/94 | 3 |', report)
        self.assertIn('| 1994/95–2005/06 | 3 |', report)


class FakeModel:
    """Stands in for a fitted LDA model: only components_ and n_components are used."""

    def __init__(self, components):
        self.components_ = np.asarray(components, dtype=float)
        self.n_components = self.components_.shape[0]


class TestPeriodExplorerChains(unittest.TestCase):
    """Rows follow the Hungarian matches between adjacent periods."""

    def test_chains_follow_matches(self):
        vocab = np.array(['a', 'b', 'c'])
        topic_a, topic_b, topic_c = [10, 1, 1], [1, 10, 1], [1, 1, 10]
        models = [
            FakeModel([topic_a, topic_b, topic_c]),
            FakeModel([topic_c, topic_a, topic_b]),   # same topics, shuffled
            FakeModel([topic_b, topic_c, topic_a]),
        ]
        chains, links = period_explorer.build_chains(models, [vocab] * len(models))
        # Row 0 is topic a in every period: index 0, then 1, then 2
        self.assertEqual(chains, [[0, 1, 2], [1, 2, 0], [2, 0, 1]])
        for row_links in links:
            self.assertEqual(len(row_links), 2)
            for c in row_links:
                self.assertAlmostEqual(c, 1.0, places=3)

    def test_weak_link_is_reported(self):
        vocab = np.array(['a', 'b', 'c', 'd'])
        models = [FakeModel([[10, 1, 1, 1], [1, 10, 1, 1]]), FakeModel([[10, 1, 1, 1], [1, 1, 10, 10]])]
        chains, links = period_explorer.build_chains(models, [vocab] * len(models))
        self.assertEqual(chains, [[0, 0], [1, 1]])
        self.assertGreater(links[0][0], 0.99)
        self.assertLess(links[1][0], period_explorer.CHAIN_COSINE)



if __name__ == '__main__':
    unittest.main()



class TestTopicNames(unittest.TestCase):
    def test_name_shown_only_when_top_words_match(self):
        top3 = {('1',): 'skola elev lärare', ('2',): 'forskning högskola universitet'}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'names.tsv'
            path.write_text('# comment\n1\tskola elev lärare\tSkolan\n2\tforskning student högskola\tForskning\n',
                            encoding='utf-8')
            self.assertEqual(quiet(lda_common.load_topic_names, path, top3), {('1',): 'Skolan'})
            self.assertEqual(quiet(lda_common.load_topic_names, Path(tmp) / 'missing.tsv', top3), {})

    def test_period_names_keyed_by_period_and_topic(self):
        top3 = {('1985-1994', '1'): 'skola elev lärare', ('1994-2006', '1'): 'skola elev lärare'}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'names.tsv'
            path.write_text('1994-2006\t1\tskola elev lärare\tSkolan\n', encoding='utf-8')
            self.assertEqual(quiet(lda_common.load_topic_names, path, top3), {('1994-2006', '1'): 'Skolan'})
