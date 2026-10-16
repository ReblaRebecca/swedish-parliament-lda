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
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

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
    'group1_1986-1993.jsonl': [
        {'dok_id': 'A', 'date': '1990-01-01', 'text_no_stopwords': 'skola lärare elev'},
        {'dok_id': 'B', 'date': '1991-01-01', 'text_no_stopwords': '\n'},  # withdrawn: no words
    ],
    'group2_1994-2004.jsonl': [
        {'dok_id': 'C', 'date': '1995-01-01', 'text_no_stopwords': 'universitet forskning'},
        {'dok_id': 'D', 'date': '1996-01-01', 'text_no_stopwords': ''},
    ],
    'group3_2005-2014.jsonl': [{'dok_id': 'E', 'date': '2010-01-01', 'text_no_stopwords': 'förskola barn'}],
    'group4_2015-2025.jsonl': [{'dok_id': 'F', 'date': '2020-01-01', 'text_no_stopwords': 'digitalisering elev'}],
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

    def test_periods_in_order_with_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_bins(tmp)
            periods, _ = lda_common.load_period_body_texts(Path(tmp))
        self.assertEqual(list(periods), ['1986-1993', '1994-2004', '2005-2014', '2015-2025'])
        self.assertEqual([m['doc_id'] for m in periods['1986-1993'][1]], ['A'])
        self.assertEqual(periods['1994-2004'][0], ['universitet forskning'])

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
        self.assertEqual(lda_common.period_label(Path('x/group2_1994-2004.jsonl')), '1994-2004')


class TestPeriodModels(unittest.TestCase):
    """All period models share one vocabulary, so their topics can be compared directly."""

    @classmethod
    def setUpClass(cls):
        rng = np.random.default_rng(0)
        words = ['skola', 'lärare', 'elev', 'universitet', 'forskning', 'student', 'förskola', 'barn',
                 'digitalisering', 'betyg']
        cls.periods = {
            period: ([' '.join(rng.choice(words[2 * i:2 * i + 4], 20)) for _ in range(30)], [{}] * 30)
            for i, period in enumerate(['1986-1993', '1994-2004', '2005-2014', '2015-2025'])
        }
        # Global vocabulary, as 07 builds it from all periods
        cls.vectorizer = CountVectorizer().fit([t for texts, _ in cls.periods.values() for t in texts])
        cls.models = quiet(period_models.fit_period_models, cls.periods,
                           period_models.period_vectorizers(cls.periods, cls.vectorizer), num_topics=3)

    def test_one_model_per_period_with_shared_settings(self):
        self.assertEqual(list(self.models), list(self.periods))
        for lda, _ in self.models.values():
            params = lda.get_params()
            self.assertEqual(params['n_components'], 3)
            self.assertEqual(params['random_state'], lda_common.DEFAULT_SEED)
            for key, value in lda_common.LDA_PARAMS.items():
                self.assertEqual(params[key], value, key)

    def test_same_vocabulary_same_order(self):
        reference = self.vectorizer.get_feature_names_out()
        for period, (lda, vocab) in self.models.items():
            np.testing.assert_array_equal(vocab, reference, period)
            self.assertEqual(lda.components_.shape, (3, len(reference)), period)
        period_models.check_same_vocabulary(self.models)  # does not raise

    def test_words_absent_from_a_period_still_have_a_column(self):
        # 'betyg' occurs only in the last period: a column everywhere, near-zero weight in the first
        vocab = list(self.vectorizer.get_feature_names_out())
        betyg = vocab.index('betyg')
        first, _ = self.models['1986-1993']
        last, _ = self.models['2015-2025']
        # Only the prior: far below a word that occurs in the period
        skola = vocab.index('skola')
        self.assertLess(first.components_[:, betyg].sum(), 0.05 * first.components_[:, skola].sum())
        self.assertGreater(last.components_[:, betyg].max(), first.components_[:, betyg].max())

    def test_check_rejects_different_vocabulary(self):
        lda, vocab = self.models['1986-1993']
        changed = dict(self.models)
        changed['2015-2025'] = (lda, vocab[::-1])
        with self.assertRaises(ValueError):
            period_models.check_same_vocabulary(changed)

    def test_adjacent_periods_can_be_matched(self):
        (lda1, vocab1), (lda2, vocab2) = self.models['1986-1993'], self.models['1994-2004']
        matches, summary, _ = match_and_evaluate(lda1, lda2, vocab1, vocab2)
        self.assertEqual(len(matches), 3)

    def test_top_words_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'period_topics.csv'
            quiet(period_models.save_top_words, self.models, 3, output)
            lines = output.read_text(encoding='utf-8').splitlines()
        self.assertEqual(len(lines), 1 + 4 * 3)  # header + 3 topics x 4 periods
        self.assertTrue(lines[1].startswith('1986-1993,1,'))

    def test_period_scripts_use_shared_functions(self):
        self.assertIs(period_models.fit_lda_model, lda_common.fit_lda_model)
        self.assertIs(period_models.load_period_body_texts, lda_common.load_period_body_texts)
        self.assertIs(period_stability.load_period_body_texts, lda_common.load_period_body_texts)
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
        report = period_stability.summary_report({('1986-1993', 3): s, ('1994-2004', 3): s})
        self.assertIn('| 1986-1993 | 3 |', report)
        self.assertIn('| 1994-2004 | 3 |', report)


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
        chains, links = period_explorer.build_chains(models, vocab)
        # Row 0 is topic a in every period: index 0, then 1, then 2
        self.assertEqual(chains, [[0, 1, 2], [1, 2, 0], [2, 0, 1]])
        for row_links in links:
            self.assertEqual(len(row_links), 2)
            for c in row_links:
                self.assertAlmostEqual(c, 1.0, places=3)

    def test_weak_link_is_reported(self):
        vocab = np.array(['a', 'b', 'c', 'd'])
        models = [FakeModel([[10, 1, 1, 1], [1, 10, 1, 1]]), FakeModel([[10, 1, 1, 1], [1, 1, 10, 10]])]
        chains, links = period_explorer.build_chains(models, vocab)
        self.assertEqual(chains, [[0, 0], [1, 1]])
        self.assertGreater(links[0][0], 0.99)
        self.assertLess(links[1][0], period_explorer.CHAIN_COSINE)

    def test_stability_only_used_for_the_same_model(self):
        vocab = np.array([f'w{i}' for i in range(10)])
        model = FakeModel([list(range(10, 0, -1)), list(range(1, 11))])
        top = [' '.join(f'w{i}' for i in range(8)), ' '.join(f'w{i}' for i in range(9, 1, -1))]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'stability.csv'
            path.write_text('topic,found,compared,mean_cosine,min_cosine,mean_jaccard,top_words\n'
                            f'1,4,4,0.9,0.8,0.5,{top[0]}\n2,1,4,0.5,0.3,0.2,{top[1]}\n', encoding='utf-8')
            self.assertEqual(period_explorer.load_stability(path, model, vocab),
                             {0: {'found': 4, 'of': 4}, 1: {'found': 1, 'of': 4}})
            # Different top words: the CSV describes another model and is not used
            other = FakeModel([list(range(1, 11)), list(range(10, 0, -1))])
            self.assertIsNone(period_explorer.load_stability(path, other, vocab))
            self.assertIsNone(period_explorer.load_stability(Path(tmp) / 'missing.csv', model, vocab))


if __name__ == '__main__':
    unittest.main()
