#!/usr/bin/env python3
"""
Tests for the seed-stability tests and the shared LDA code they rely on
(modeling/lda_common.py, analysis/seed_stability.py, 09_test_lda_stability.py and the 07 model).
Small synthetic data only: no corpus or fitted models needed, runs in about half a minute.

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
from sklearn.feature_extraction.text import CountVectorizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'modeling'))
sys.path.insert(0, str(PROJECT_ROOT / 'analysis'))

import lda_common  # noqa: E402
import seed_stability  # noqa: E402


def load_script(relative_path):
    """Import a script as a module (file names start with digits, so plain import fails)."""
    path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(re.sub(r'\W', '_', path.stem), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


baseline_model = load_script('modeling/07_fit_baseline_lda.py')
baseline_stability = load_script('analysis/09_test_lda_stability.py')


def quiet(function, *args, **kwargs):
    """Call function with its progress printing suppressed."""
    with contextlib.redirect_stdout(io.StringIO()):
        return function(*args, **kwargs)


def write_bin(directory, motions, extra_lines=()):
    """Write motions as one temporal-bin JSONL file."""
    with open(Path(directory) / 'group1_1985-1994.jsonl', 'w', encoding='utf-8') as f:
        for motion in motions:
            f.write(json.dumps(motion, ensure_ascii=False) + '\n')
        for line in extra_lines:
            f.write(line + '\n')


class TestLoadBodyTexts(unittest.TestCase):
    """The models are fitted on body text only; motions without body text are skipped."""

    def setUp(self):
        # Short synthetic texts: the length minimum is tested in TestMinimumLength
        patcher = mock.patch.object(lda_common, 'MIN_WORDS', 1)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_empty_bodies_skipped(self):
        motions = [
            {'dok_id': 'A', 'text_no_stopwords': 'skola', 'title_processed': 'lärare'},
            {'dok_id': 'B', 'text_no_stopwords': '', 'title_processed': 'betyg'},
            {'dok_id': 'C', 'text_no_stopwords': 'elev', 'title_processed': ''},
            # Withdrawn motion: no words left, only a line break
            {'dok_id': 'E', 'text_no_stopwords': '\n', 'title_processed': 'utgå'},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            write_bin(tmp, motions)
            texts, metadata, _ = lda_common.load_body_texts(Path(tmp))
        self.assertEqual([m['doc_id'] for m in metadata], ['A', 'C'])
        self.assertEqual(texts, ['skola', 'elev'])  # titles are not added

    def test_load_body_texts(self):
        motions = [
            {'dok_id': 'A', 'date': '1990-01-01', 'text_no_stopwords': 'skola lärare', 'title_processed': 'lärare'},
            {'dok_id': 'C', 'date': '1992-01-01', 'text_no_stopwords': '', 'title_processed': 'betyg'},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            write_bin(tmp, motions, extra_lines=['{not json'])
            texts, metadata, malformed = lda_common.load_body_texts(Path(tmp))

        self.assertEqual(texts, ['skola lärare'])  # no title added, empty body skipped
        self.assertEqual([m['doc_id'] for m in metadata], ['A'])
        self.assertEqual(malformed, 1)


class TestMinimumLength(unittest.TestCase):
    """Motions with fewer than MIN_WORDS words in the final text are not modelled."""

    def test_short_motions_skipped(self):
        self.assertEqual(lda_common.MIN_WORDS, 20)
        motions = [
            {'dok_id': 'A', 'text_no_stopwords': ' '.join(['skola'] * 20)},
            {'dok_id': 'B', 'text_no_stopwords': ' '.join(['skola'] * 19)},
            {'dok_id': 'C', 'text_no_stopwords': '\n'},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            write_bin(tmp, motions)
            _, metadata, _ = lda_common.load_body_texts(Path(tmp))
        self.assertEqual([m['doc_id'] for m in metadata], ['A'])

    def test_is_modelled(self):
        self.assertTrue(lda_common.is_modelled(' '.join(['elev'] * 25)))
        self.assertFalse(lda_common.is_modelled('hemställa riksdag regering'))
        self.assertFalse(lda_common.is_modelled(None))


class TestNearDuplicates(unittest.TestCase):
    """A revised resubmission (three-word sequences overlapping at least NEAR_DUPLICATE_JACCARD with an
    earlier motion) is not modelled; a motion revised more than that is."""

    WORDS = [f'ord{i}' for i in range(40)]

    def revised(self, changed):
        """The 40-word text with its last `changed` words replaced (new words unique to this revision)."""
        return ' '.join(self.WORDS[:40 - changed] + [f'nytt{changed}_{i}' for i in range(changed)])

    def test_threshold(self):
        self.assertEqual(lda_common.NEAR_DUPLICATE_JACCARD, 0.6)
        original = ' '.join(self.WORDS)
        # 1 word changed: 37 sequences shared of 39 (Jaccard 0.95); 6 changed: 32 of 44 (0.73);
        # 10 changed: 28 of 48 (0.58)
        texts = [original, self.revised(1), self.revised(6), self.revised(10)]
        self.assertEqual(lda_common.near_duplicates(texts, ['1990/91', '1991/92', '1992/93', '1993/94']), {1, 2})

    def test_earlier_session_is_the_original(self):
        # The copy listed first but submitted later is the one dropped
        texts = [self.revised(1), ' '.join(self.WORDS)]
        self.assertEqual(lda_common.near_duplicates(texts, ['1995/96', '1990/91']), {0})

    def test_unrelated_texts_kept(self):
        texts = [' '.join(self.WORDS), ' '.join(f'annat{i}' for i in range(40))]
        self.assertEqual(lda_common.near_duplicates(texts, ['1990/91', '1991/92']), set())

    def test_loaders_skip_near_copies_in_both_models(self):
        motions = [
            {'dok_id': 'A', 'session': '1990/91', 'text_no_stopwords': ' '.join(self.WORDS)},
            {'dok_id': 'B', 'session': '1991/92', 'text_no_stopwords': self.revised(1)},
            {'dok_id': 'C', 'session': '1992/93', 'text_no_stopwords': self.revised(10)},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            write_bin(tmp, motions)
            _, metadata, _ = lda_common.load_body_texts(Path(tmp))
            periods, _ = lda_common.load_period_body_texts(Path(tmp))
        self.assertEqual([m['doc_id'] for m in metadata], ['A', 'C'])
        self.assertEqual([m['doc_id'] for m in periods['1985-1994'][1]], ['A', 'C'])

    def test_near_copy_in_a_later_period_kept(self):
        bins = {
            'group1_1985-1994.jsonl': [{'dok_id': 'A', 'session': '1993/94', 'text_no_stopwords': ' '.join(self.WORDS)}],
            'group2_1994-2006.jsonl': [{'dok_id': 'B', 'session': '1994/95', 'text_no_stopwords': self.revised(1)}],
        }
        with tempfile.TemporaryDirectory() as tmp:
            for name, motions in bins.items():
                (Path(tmp) / name).write_text(''.join(json.dumps(m) + '\n' for m in motions), encoding='utf-8')
            _, metadata, _ = lda_common.load_body_texts(Path(tmp))
            periods, _ = lda_common.load_period_body_texts(Path(tmp))
        self.assertEqual([m['doc_id'] for m in metadata], ['A', 'B'])
        self.assertEqual([m['doc_id'] for m in periods['1994-2006'][1]], ['B'])


class TestDedupLevels(unittest.TestCase):
    """The deduplication comparison's selections: none, over all periods (earlier setting), within each period."""

    WORDS = TestNearDuplicates.WORDS
    revised = TestNearDuplicates.revised

    def test_levels(self):
        bins = {
            'group1_1985-1994.jsonl': [
                {'dok_id': 'A', 'session': '1990/91', 'text_no_stopwords': ' '.join(self.WORDS)},
                {'dok_id': 'B', 'session': '1991/92', 'text_no_stopwords': ' '.join(self.WORDS)},  # exact copy
                {'dok_id': 'C', 'session': '1992/93', 'text_no_stopwords': self.revised(1)},       # near copy
            ],
            'group2_1994-2006.jsonl': [
                {'dok_id': 'D', 'session': '1994/95', 'text_no_stopwords': ' '.join(self.WORDS)},  # exact, later period
                {'dok_id': 'E', 'session': '1995/96', 'text_no_stopwords': self.revised(6)},       # near, same period as D
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            for name, motions in bins.items():
                (Path(tmp) / name).write_text(''.join(json.dumps(m) + '\n' for m in motions), encoding='utf-8')
            kept = {level: [m['doc_id'] for m in lda_common.load_body_texts(Path(tmp), dedup=level)[1]]
                    for level in lda_common.DEDUP_LEVELS}
            with self.assertRaises(ValueError):
                lda_common.load_body_texts(Path(tmp), dedup='near')
        self.assertEqual(kept, {'none': ['A', 'B', 'C', 'D', 'E'], 'global': ['A'], 'period': ['A', 'D']})

    def test_default_is_within_each_period(self):
        self.assertEqual(lda_common.load_body_texts.__defaults__, ('period',))
        self.assertEqual(lda_common.load_period_body_texts.__defaults__, ('period',))


class TestSharedSettings(unittest.TestCase):
    """The models and the stability tests use the same code, so they cannot drift apart."""

    def test_models_and_tests_use_the_shared_functions(self):
        for module in (baseline_model, seed_stability):
            self.assertIs(module.fit_lda_model, lda_common.fit_lda_model, module.__name__)
        for module in (baseline_model, baseline_stability):
            self.assertIs(module.load_body_texts, lda_common.load_body_texts, module.__name__)

    def test_no_script_builds_its_own_lda(self):
        """Only lda_common.py creates LDA models."""
        allowed = {'lda_common.py'}
        offenders = []
        for path in sorted((PROJECT_ROOT / 'modeling').glob('*.py')) + sorted((PROJECT_ROOT / 'analysis').glob('*.py')):
            if path.name in allowed:
                continue
            source = path.read_text(encoding='utf-8')
            if 'LatentDirichletAllocation(' in source:
                offenders.append(path.name)
        self.assertEqual(offenders, [])

    def test_whole_corpus_vocabulary_uses_the_period_rule(self):
        """The whole-corpus model's vocabulary follows the same rule as the period models' (no size cap)."""
        with contextlib.redirect_stdout(io.StringIO()):
            vectorizer, _ = baseline_model.create_vectorizer_and_corpus(['skola lärare', 'universitet student'] * 10)
        params = vectorizer.get_params()
        for key, value in lda_common.VECTORIZER_PARAMS.items():
            self.assertEqual(params[key], value, key)
        self.assertIsNone(params['max_features'])

    def test_fit_uses_shared_settings(self):
        X = CountVectorizer().fit_transform(['skola lärare elev', 'universitet student forskning'] * 5)
        lda = lda_common.fit_lda_model(X, num_topics=2, random_state=7)
        params = lda.get_params()
        self.assertEqual(params['n_components'], 2)
        self.assertEqual(params['random_state'], 7)
        for key, value in lda_common.LDA_PARAMS.items():
            self.assertEqual(params[key], value, key)

    def test_defaults(self):
        self.assertEqual(lda_common.NUM_TOPICS, 4 * lda_common.PERIOD_TOPICS)
        self.assertEqual(lda_common.DEFAULT_SEED, 42)
        self.assertEqual(lda_common.LDA_PARAMS['max_iter'], 50)
        self.assertEqual(len(set(lda_common.STABILITY_SEEDS)), len(lda_common.STABILITY_SEEDS))
        # The reported model's seed is one of the seeds tested
        self.assertIn(lda_common.DEFAULT_SEED, lda_common.STABILITY_SEEDS)

    def test_missing_vectorizer_gives_clear_message(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), self.assertRaises(SystemExit):
            lda_common.load_baseline_vectorizer(PROJECT_ROOT / 'models' / 'does_not_exist.pkl')
        self.assertIn('07_fit_baseline_lda.py', output.getvalue())


def random_corpus(n_docs=60, seed=0):
    """Unstructured corpus: words drawn at random from one shared vocabulary."""
    rng = np.random.default_rng(seed)
    vocab = [f'ord{i}' for i in range(40)]
    return [' '.join(rng.choice(vocab, 30)) for _ in range(n_docs)]


# Three clearly separated planted topics
PLANTED_TOPICS = [
    ['skola', 'lärare', 'elev', 'klass', 'betyg', 'rektor', 'läxa', 'undervisning'],
    ['universitet', 'forskning', 'student', 'doktorand', 'professor', 'examen', 'högskola', 'avhandling'],
    ['förskola', 'barn', 'pedagog', 'lek', 'föräldrar', 'barngrupp', 'omsorg', 'småbarn'],
]


def planted_corpus(docs_per_topic=60, seed=0):
    """Each document draws 40 words from one planted topic."""
    rng = np.random.default_rng(seed)
    return [' '.join(rng.choice(words, 40)) for words in PLANTED_TOPICS for _ in range(docs_per_topic)]


class TestSeeds(unittest.TestCase):
    """The seed is what varies between runs: same seed reproduces the model, a different seed changes it."""

    @classmethod
    def setUpClass(cls):
        cls.X = CountVectorizer().fit_transform(random_corpus())

    def test_same_seed_gives_same_model(self):
        first = lda_common.fit_lda_model(self.X, num_topics=4, random_state=42)
        second = lda_common.fit_lda_model(self.X, num_topics=4, random_state=42)
        np.testing.assert_allclose(first.components_, second.components_)

    def test_different_seeds_give_different_models(self):
        first = lda_common.fit_lda_model(self.X, num_topics=4, random_state=42)
        second = lda_common.fit_lda_model(self.X, num_topics=4, random_state=123)
        self.assertFalse(np.allclose(first.components_, second.components_))


class TestPlantedTopics(unittest.TestCase):
    """End to end: on a corpus with clearly separated topics, the procedure reports them as stable."""

    def test_planted_topics_are_stable_across_seeds(self):
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(planted_corpus())
        seeds = [42, 123, 456]
        seed_info, pairwise = quiet(seed_stability.run_seed_stability,
                                    X, vectorizer.get_feature_names_out(), seeds, len(PLANTED_TOPICS))

        self.assertEqual(list(pairwise), [(42, 123), (42, 456), (123, 456)])
        for pair, result in pairwise.items():
            self.assertGreater(result['summary']['cosine']['min'], 0.99, pair)
            # Every topic is matched exactly once
            self.assertEqual(sorted(m[1] for m in result['matches']), [0, 1, 2], pair)
        self.assertEqual(set(seed_info), set(seeds))
        for info in seed_info.values():
            self.assertEqual(info['n_iter'], lda_common.LDA_PARAMS['max_iter'])
            self.assertEqual(len(info['top_words']), len(PLANTED_TOPICS))
        # Every planted topic of the reference model is found again in both other models
        rows = seed_stability.per_topic_stability(pairwise, 42, len(PLANTED_TOPICS))
        self.assertEqual([r['found'] for r in rows], [2, 2, 2])


class TestPerTopicStability(unittest.TestCase):
    """Each reference topic collects its matches from every pair that includes the reference seed."""

    def setUp(self):
        # Reference seed 42 appears both as first and as second seed of a pair
        self.pairwise = {
            (123, 42): {'matches': [(0, 1, 0.95, 0.8), (1, 0, 0.40, 0.1)]},   # ref topic 1 <-> 123's topic 0
            (123, 456): {'matches': [(0, 0, 0.10, 0.0), (1, 1, 0.10, 0.0)]},  # does not involve 42: ignored
            (42, 456): {'matches': [(0, 1, 0.50, 0.2), (1, 0, 0.90, 0.6)]},
        }

    def test_matches_collected_for_both_pair_orientations(self):
        rows = seed_stability.per_topic_stability(self.pairwise, 42, 2)
        self.assertEqual(rows[0]['cosines'], [0.40, 0.50])  # topic 1 of seed 42
        self.assertEqual(rows[1]['cosines'], [0.95, 0.90])  # topic 2 of seed 42
        self.assertAlmostEqual(rows[1]['mean_cosine'], 0.925)
        self.assertAlmostEqual(rows[0]['min_cosine'], 0.40)
        self.assertAlmostEqual(rows[1]['mean_jaccard'], 0.7)

    def test_found_uses_threshold(self):
        rows = seed_stability.per_topic_stability(self.pairwise, 42, 2)
        self.assertEqual([r['found'] for r in rows], [0, 2])
        self.assertEqual(seed_stability.FOUND_COSINE, 0.70)

    def test_unknown_reference_seed(self):
        with self.assertRaises(ValueError):
            seed_stability.per_topic_stability(self.pairwise, 999, 2)

    def test_csv_output(self):
        rows = seed_stability.per_topic_stability(self.pairwise, 42, 2)
        seed_info = {42: {'top_words': [['skola', 'lärare'], ['barn', 'förskola']]}}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'per_topic.csv'
            quiet(seed_stability.save_topic_stability, rows, seed_info, 42, path)
            lines = path.read_text(encoding='utf-8').splitlines()
        self.assertEqual(lines[0], 'topic,found,compared,mean_cosine,min_cosine,mean_jaccard,top_words')
        self.assertEqual(lines[2], '2,2,2,0.9250,0.9000,0.7000,barn förskola')


class TestReport(unittest.TestCase):
    """Report counts and pooled statistics are computed from all matched pairs."""

    def setUp(self):
        rng = np.random.default_rng(0)
        self.seeds = [42, 123, 456, 789, 999]
        self.num_topics = 44
        self.pairwise = {}
        self.all_cosine, self.all_jaccard = [], []
        for i, seed1 in enumerate(self.seeds):
            for seed2 in self.seeds[i + 1:]:
                cosine = rng.uniform(0.3, 1.0, self.num_topics)
                jaccard = rng.uniform(0.0, 1.0, self.num_topics)
                self.all_cosine.extend(cosine)
                self.all_jaccard.extend(jaccard)
                matches = [(t, t, float(c), float(j)) for t, (c, j) in enumerate(zip(cosine, jaccard))]
                self.pairwise[(seed1, seed2)] = {'matches': matches, 'summary': {}, 'similarity_matrix': None}
        self.seed_info = {seed: {'perplexity': 1000.0 + seed, 'n_iter': 50,
                                 'top_words': [[f'ord{k}_{i}' for i in range(8)] for k in range(self.num_topics)]}
                          for seed in self.seeds}
        self.report = seed_stability.generate_report(
            'Test report', 'Body text only', self.num_topics,
            self.seed_info, self.pairwise)

    def section(self, heading):
        """Text of one '### heading' section in the overall summary."""
        start = self.report.index(heading)
        end = self.report.find('\n###', start + 1)
        return self.report[start:end if end != -1 else None]

    def test_counts(self):
        self.assertIn('**Total seed pairs tested:** 10', self.report)
        self.assertIn('**Total matched topic pairs:** 440', self.report)
        self.assertEqual(self.report.count('### Seed '), 10)

    def test_pooled_statistics(self):
        cosine = self.section('### Cosine Similarity (across all matches)')
        self.assertIn(f"- Mean: {np.mean(self.all_cosine):.4f}", cosine)
        self.assertIn(f"- Median: {np.median(self.all_cosine):.4f}", cosine)
        self.assertIn(f"- Std Dev: {np.std(self.all_cosine):.4f}", cosine)
        jaccard = self.section('### Jaccard Similarity (across all matches)')
        self.assertIn(f"- Mean: {np.mean(self.all_jaccard):.4f}", jaccard)
        self.assertIn(f"- Max: {np.max(self.all_jaccard):.4f}", jaccard)

    def test_per_pair_statistics(self):
        cosine = [m[2] for m in self.pairwise[(42, 123)]['matches']]
        start = self.report.index('### Seed 42 vs Seed 123')
        pair_section = self.report[start:self.report.index('### Seed 42 vs Seed 456')]
        self.assertIn(f"- Mean: {np.mean(cosine):.4f}", pair_section)

    def test_per_topic_section(self):
        self.assertIn('## Stability per Topic (reference model: seed 42)', self.report)
        rows = seed_stability.per_topic_stability(self.pairwise, 42, self.num_topics)
        # Distribution table covers every topic exactly once
        counts = [int(m) for m in re.findall(r'^\| \d of 4 \| (\d+) \|$', self.report, re.M)]
        self.assertEqual(sum(counts), self.num_topics)
        first = rows[0]
        self.assertIn(f"| 1 | ord0_0, ord0_1, ord0_2, ord0_3, ord0_4, ord0_5, ord0_6, ord0_7 | {first['found']}/4 | "
                      f"{first['mean_cosine']:.3f} |", self.report)

    def test_seed_table_and_notes(self):
        for seed in self.seeds:
            self.assertIn(f"| {seed} | {1000.0 + seed:.2f} | 50 |", self.report)
        self.assertIn('appears in 4 of the 10 pairs', self.report)
        self.assertIn('does not test for convergence', self.report)
        self.assertIn('**Text:** Body text only', self.report)
        self.assertTrue(self.report.rstrip().endswith(f"- Std Dev: {np.std(self.all_jaccard):.4f}"))  # pooled Jaccard last


if __name__ == '__main__':
    unittest.main()
