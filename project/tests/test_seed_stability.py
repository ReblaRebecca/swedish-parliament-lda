#!/usr/bin/env python3
"""
Tests for the seed-stability tests and the shared LDA code they rely on
(modeling/lda_common.py, analysis/seed_stability.py, the 09/13 scripts and the 07/10/06 models).
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
from collections import Counter
from pathlib import Path
from unittest import mock

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
weighted_model = load_script('modeling/10_fit_title_weighted_lda.py')
shared_vocab_models = load_script('modeling/06_build_shared_vocabulary_and_fit_models.py')
baseline_stability = load_script('analysis/09_test_lda_stability.py')
stability_5x = load_script('analysis/13_seed_stability_5x_weighted.py')
stability_3x = load_script('analysis/13_seed_stability_3x_weighted.py')


def quiet(function, *args, **kwargs):
    """Call function with its progress printing suppressed."""
    with contextlib.redirect_stdout(io.StringIO()):
        return function(*args, **kwargs)


def write_bin(directory, motions, extra_lines=()):
    """Write motions as one temporal-bin JSONL file."""
    with open(Path(directory) / 'group1_1986-1993.jsonl', 'w', encoding='utf-8') as f:
        for motion in motions:
            f.write(json.dumps(motion, ensure_ascii=False) + '\n')
        for line in extra_lines:
            f.write(line + '\n')


class TestTitleWeighting(unittest.TestCase):
    """Title words are appended exactly TITLE_WEIGHT times; documents without a title are body only."""

    def test_reported_model_weight_is_five(self):
        self.assertEqual(lda_common.TITLE_WEIGHT, 5)

    def test_title_words_appended_title_weight_times(self):
        counts = Counter(lda_common.weight_document('skola lärare', 'skola betyg').split())
        self.assertEqual(counts, {'skola': 1 + 5, 'lärare': 1, 'betyg': 5})

    def test_other_weight(self):
        counts = Counter(lda_common.weight_document('elev', 'betyg', title_weight=3).split())
        self.assertEqual(counts, {'elev': 1, 'betyg': 3})

    def test_title_whitespace_normalized(self):
        self.assertEqual(lda_common.weight_document('elev', '  betyg \n  skola ', 2).split(),
                         ['elev', 'betyg', 'skola', 'betyg', 'skola'])

    def test_empty_title_gives_body_only(self):
        self.assertEqual(lda_common.weight_document('skola lärare', ''), 'skola lärare')
        self.assertEqual(lda_common.weight_document('skola lärare', '   '), 'skola lärare')

    def test_load_weighted_texts(self):
        motions = [
            {'dok_id': 'A', 'date': '1990-01-01', 'title': 'Lärarna', 'text_no_stopwords': 'skola lärare', 'title_processed': 'lärare'},
            {'dok_id': 'B', 'date': '1991-01-01', 'title': '', 'text_no_stopwords': 'elev', 'title_processed': ''},
            {'dok_id': 'C', 'date': '1992-01-01', 'title': 'Betyg', 'text_no_stopwords': '', 'title_processed': 'betyg'},
            {'dok_id': 'D', 'date': '1993-01-01', 'title': '', 'text_no_stopwords': '', 'title_processed': ''},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            write_bin(tmp, motions, extra_lines=['{not json'])
            texts, metadata, stats = lda_common.load_weighted_texts(Path(tmp), title_weight=5)

        self.assertEqual([m['doc_id'] for m in metadata], ['A', 'B', 'C'])  # D is empty and skipped
        self.assertEqual(Counter(texts[0].split()), {'skola': 1, 'lärare': 1 + 5})
        self.assertEqual(texts[1], 'elev')
        self.assertEqual(Counter(texts[2].split()), {'betyg': 5})
        self.assertEqual(metadata[0], {'doc_id': 'A', 'title': 'Lärarna', 'year': '1990'})
        self.assertEqual(stats, {'empty': 2, 'weighted': 2, 'total': 4, 'malformed': 1})

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


class TestSharedSettings(unittest.TestCase):
    """The models and the stability tests use the same code, so they cannot drift apart."""

    def test_models_and_tests_use_the_shared_functions(self):
        for module in (baseline_model, weighted_model, shared_vocab_models, seed_stability):
            self.assertIs(module.fit_lda_model, lda_common.fit_lda_model, module.__name__)
        for module in (weighted_model, stability_5x, stability_3x):
            self.assertIs(module.load_weighted_texts, lda_common.load_weighted_texts, module.__name__)
        for module in (baseline_model, baseline_stability):
            self.assertIs(module.load_body_texts, lda_common.load_body_texts, module.__name__)
        self.assertIs(shared_vocab_models.weight_document, lda_common.weight_document)

    def test_no_script_builds_its_own_lda_or_weighting(self):
        """Only lda_common.py creates LDA models or repeats titles (the quick matching check excepted)."""
        allowed = {'lda_common.py', '11_validate_matching_quick.py'}
        offenders = []
        for path in sorted((PROJECT_ROOT / 'modeling').glob('*.py')) + sorted((PROJECT_ROOT / 'analysis').glob('*.py')):
            if path.name in allowed:
                continue
            source = path.read_text(encoding='utf-8')
            if 'LatentDirichletAllocation(' in source or re.search(r"\+ ' '\) \* \d", source):
                offenders.append(path.name)
        self.assertEqual(offenders, [])

    def test_fit_uses_shared_settings(self):
        X = CountVectorizer().fit_transform(['skola lärare elev', 'universitet student forskning'] * 5)
        lda = lda_common.fit_lda_model(X, num_topics=2, random_state=7)
        params = lda.get_params()
        self.assertEqual(params['n_components'], 2)
        self.assertEqual(params['random_state'], 7)
        for key, value in lda_common.LDA_PARAMS.items():
            self.assertEqual(params[key], value, key)

    def test_defaults(self):
        self.assertEqual(lda_common.NUM_TOPICS, 44)
        self.assertEqual(lda_common.DEFAULT_SEED, 42)
        self.assertEqual(lda_common.LDA_PARAMS['max_iter'], 50)
        self.assertEqual(len(set(lda_common.STABILITY_SEEDS)), len(lda_common.STABILITY_SEEDS))
        # The reported model's seed is one of the seeds tested
        self.assertIn(lda_common.DEFAULT_SEED, lda_common.STABILITY_SEEDS)

    def test_stability_scripts_load_with_their_weight(self):
        """Each 13 script asks for its own title weight (5 for the reported model, 3 for the comparison)."""
        for module, expected_weight in ((stability_5x, lda_common.TITLE_WEIGHT), (stability_3x, 3)):
            calls = []

            def fake_load(input_dir, title_weight=lda_common.TITLE_WEIGHT):
                calls.append(title_weight)
                return [], [], {'empty': 0, 'weighted': 0, 'total': 0, 'malformed': 0}

            # With no texts loaded, main() stops before fitting anything
            with mock.patch.object(module, 'load_weighted_texts', fake_load):
                with self.assertRaises(SystemExit):
                    quiet(module.main)
            self.assertEqual(calls, [expected_weight], module.__name__)

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
        self.seed_info = {seed: {'perplexity': 1000.0 + seed, 'n_iter': 50} for seed in self.seeds}
        self.report = seed_stability.generate_report(
            'Test report', 'Title words are appended five times', self.num_topics,
            self.seed_info, self.pairwise, closing_lines=['## Closing'])

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

    def test_seed_table_and_notes(self):
        for seed in self.seeds:
            self.assertIn(f"| {seed} | {1000.0 + seed:.2f} | 50 |", self.report)
        self.assertIn('appears in 4 of the 10 pairs', self.report)
        self.assertIn('does not test for convergence', self.report)
        self.assertIn('Title words are appended five times', self.report)
        self.assertTrue(self.report.endswith('## Closing'))


if __name__ == '__main__':
    unittest.main()
