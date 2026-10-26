#!/usr/bin/env python3
"""
Unit tests for the extraction and preprocessing functions (steps 01, 03, 04, 05).
Small hand-written examples only: no corpus data and no Stanza model needed, runs in seconds.

Run from project/:
    python -m unittest discover -s tests -v
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_script(relative_path):
    """Import a pipeline script as a module (file names start with digits, so plain import fails)."""
    path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


extract = load_script('extraction/01_extract_from_xml.py')
boilerplate = load_script('preprocessing/03_remove_boilerplate.py')
normalize = load_script('preprocessing/04_normalize_text.py')
stopwords = load_script('preprocessing/05_remove_stopwords.py')


class TestHTMLParsing(unittest.TestCase):
    """01: inline tags must not split words, block tags must separate them."""

    def test_word_split_across_spans_is_joined(self):
        html = '<p><span>uppföljni</span><span>ng</span></p>'
        self.assertEqual(extract.decode_html_entities(html).strip(), 'uppföljning')

    def test_every_letter_in_its_own_span(self):
        html = '<p><span>f</span><span>ö</span><span>r</span> skolan</p>'
        self.assertEqual(extract.decode_html_entities(html).split(), ['för', 'skolan'])

    def test_block_tags_separate_words(self):
        html = '<p>skolan</p><p>eleverna</p><div>lärare</div>x<br>y'
        self.assertEqual(extract.decode_html_entities(html).split(), ['skolan', 'eleverna', 'lärare', 'x', 'y'])

    def test_entities_are_decoded(self):
        self.assertEqual(extract.decode_html_entities('<p>skola &amp; f&ouml;rskola</p>').strip(), 'skola & förskola')

    def test_empty_input(self):
        self.assertEqual(extract.decode_html_entities(''), '')
        self.assertEqual(extract.extract_body_text(''), '')


class TestExtractBodyText(unittest.TestCase):
    """01: metadata sections and non-content tags are removed, whitespace collapsed."""

    def test_signatures_and_styles_removed(self):
        html = (
            '<style>p { color: red; }</style>'
            '<div class="sidhuvud_beteckning">Motion 1999/2000:Ub201</div>'
            '<p>Skolan behöver fler lärare.</p>'
            '<div class="Underskrifter">Anna Svensson (s)</div>'
            '<p class="UnderskriftDatum">Stockholm den 5 oktober 1999</p>'
        )
        self.assertEqual(extract.extract_body_text(html), 'Skolan behöver fler lärare.')

    def test_soft_hyphen_inside_split_word(self):
        html = '<p><span>ansva</span><span>\xad</span><span>ret</span> ligger hos kommunen</p>'
        self.assertEqual(extract.extract_body_text(html), 'ansvaret ligger hos kommunen')

    def test_whitespace_collapsed(self):
        self.assertEqual(extract.extract_body_text('<p>  en\n\n  skola </p><p>två</p>'), 'en skola två')


class TestRepairCharacters(unittest.TestCase):
    """01: character-level encoding repairs."""

    def test_soft_hyphen_removed(self):
        self.assertEqual(extract.repair_characters('ansva\xadret'), 'ansvaret')

    def test_combining_diacritics_composed(self):
        self.assertEqual(extract.repair_characters('många'), 'många')
        self.assertEqual(extract.repair_characters('skörd'), 'skörd')

    def test_spacing_diacritics_replaced(self):
        self.assertEqual(extract.repair_characters('ma°ste'), 'måste')
        self.assertEqual(extract.repair_characters('sa¨tt'), 'sätt')
        self.assertEqual(extract.repair_characters('o¨ka'), 'öka')
        self.assertEqual(extract.repair_characters('A°lder O¨vrigt A¨ven'), 'Ålder Övrigt Även')

    def test_normal_text_unchanged(self):
        text = 'Riksdagen ställer sig bakom det som anförs i motionen.'
        self.assertEqual(extract.repair_characters(text), text)


class TestRemoveTitleHeading(unittest.TestCase):
    """01: the title heading at the start of the body is removed once; later mentions are kept."""

    def test_heading_removed(self):
        body = 'Motion till riksdagen av Anna Svensson (s) Sfi – uttalets betydelse Vi föreslår mer undervisning.'
        result = extract.remove_title_heading(body, 'Sfi - uttalets betydelse')
        self.assertEqual(result, 'Motion till riksdagen av Anna Svensson (s) Vi föreslår mer undervisning.')

    def test_case_insensitive(self):
        body = 'Motion till riksdagen LÄRARNAS LÖNER Lärare ska ha högre lön.'
        self.assertEqual(extract.remove_title_heading(body, 'Lärarnas löner'), 'Motion till riksdagen Lärare ska ha högre lön.')

    def test_only_first_occurrence_removed(self):
        body = 'Lärarnas löner Bakgrund. Frågan om lärarnas löner är viktig.'
        self.assertEqual(extract.remove_title_heading(body, 'Lärarnas löner'), 'Bakgrund. Frågan om lärarnas löner är viktig.')

    def test_occurrence_far_into_text_kept(self):
        body = 'x ' * 250 + 'Lärarnas löner är viktiga.'
        self.assertEqual(extract.remove_title_heading(body, 'Lärarnas löner'), body)

    def test_title_must_match_whole_words(self):
        body = 'Skolans lärare ska ha mer tid.'
        self.assertEqual(extract.remove_title_heading(body, 'Skola'), body)

    def test_empty_title(self):
        self.assertEqual(extract.remove_title_heading('Någon text.', ''), 'Någon text.')


class TestPlaceholders(unittest.TestCase):
    """01: motions with no text of their own are skipped; real motions are kept."""

    def test_placeholder_texts_are_skipped(self):
        self.assertTrue(extract.is_placeholder('Dokument saknas', 'Ansvaret för skolan'))
        self.assertTrue(extract.is_placeholder('Motion till riksdagen av (M) [~ konvertering pågår ~]', 'Bygg testreaktorn Electra'))
        self.assertTrue(extract.is_placeholder(
            'Observera att dokumentet är inskannat och fel kan förekomma. Motion till riksdagen (fp) Motionen återtagen', 'Kostkunskap'))

    def test_withdrawal_in_title_only(self):
        text = 'Observera att dokumentet är inskannat och fel kan förekomma. Motion till riksdagen 1986/87 :Ub305 Svenskt Tryck Stockholm 1987'
        self.assertTrue(extract.is_placeholder(text, 'Motionen utgår'))

    def test_real_motions_are_kept(self):
        # Short but real: a formal request referring to another motion
        self.assertFalse(extract.is_placeholder(
            'Hemställan Med hänvisning till vad som anförts i motion hemställs att riksdagen som sin mening ger regeringen till känna', 'Lärarutbildning'))
        # Long motion that mentions a withdrawn motion
        self.assertFalse(extract.is_placeholder('Motionen utgår ur ett större förslag. ' + 'skola ' * 40, 'Studiemedel'))


class TestRemoveMetadata(unittest.TestCase):
    """01: motion numbers and the motion's own author names are removed."""

    def test_motion_numbers_removed(self):
        self.assertEqual(extract.remove_metadata('Motion 1986/87:Ub801 om skolan', []), 'Motion om skolan')
        self.assertEqual(extract.remove_metadata('Se motion GE02A1 om skolan', []), 'Se motion om skolan')

    def test_author_names_removed_case_insensitive(self):
        text = 'Förslag av ANNA SVENSSON och Per Olsson om skolan'
        self.assertEqual(extract.remove_metadata(text, ['Anna Svensson', 'Per Olsson']), 'Förslag av och om skolan')

    def test_author_name_only_as_whole_words(self):
        text = 'Bertil Ohlins väg och skolan'
        self.assertEqual(extract.remove_metadata(text, ['Bertil Ohlin']), text)

    def test_no_authors(self):
        self.assertEqual(extract.remove_metadata('Om skolan', []), 'Om skolan')


class TestPeriodBySession(unittest.TestCase):
    """01: motions are assigned to the four periods by parliamentary session (riksmöte), not by date.
    The periods follow complete electoral terms: 1985/86-1993/94, 1994/95-2005/06, 2006/07-2013/14, 2014/15-2025/26."""

    def test_period_boundaries(self):
        self.assertEqual(extract.get_temporal_bin('1985/86'), 'group1_1985-1994')
        self.assertEqual(extract.get_temporal_bin('1993/94'), 'group1_1985-1994')
        self.assertEqual(extract.get_temporal_bin('1994/95'), 'group2_1994-2006')
        self.assertEqual(extract.get_temporal_bin('2005/06'), 'group2_1994-2006')
        self.assertEqual(extract.get_temporal_bin('2006/07'), 'group3_2006-2014')
        self.assertEqual(extract.get_temporal_bin('2013/14'), 'group3_2006-2014')
        self.assertEqual(extract.get_temporal_bin('2014/15'), 'group4_2014-2026')
        self.assertEqual(extract.get_temporal_bin('2025/26'), 'group4_2014-2026')

    def test_four_digit_session(self):
        # The riksdag writes the session spanning the millennium as 1999/2000
        self.assertEqual(extract.get_temporal_bin('1999/2000'), 'group2_1994-2006')

    def test_outside_range_or_invalid(self):
        self.assertIsNone(extract.get_temporal_bin('1984/85'))
        self.assertIsNone(extract.get_temporal_bin('2026/27'))
        self.assertIsNone(extract.get_temporal_bin(''))
        self.assertIsNone(extract.get_temporal_bin('1990'))
        self.assertIsNone(extract.get_temporal_bin('1990/92'))  # not two consecutive years
        self.assertIsNone(extract.get_temporal_bin('inte ett riksmöte'))

    def test_motion_keeps_session_and_is_binned_by_it(self):
        # A 1985/86 motion whose date field holds the placeholder 1985-01-01 belongs to the first period
        xml = (
            '<dokumentstatus><dokument>'
            '<dok_id>G902ub211</dok_id><rm>1985/86</rm><organ>UbU</organ>'
            '<datum>1985-01-01 00:00:00</datum><titel>Medieundervisningen i skolan</titel>'
            '<html>&lt;p&gt;Skolan behöver mer undervisning om medier.&lt;/p&gt;</html>'
            '</dokument></dokumentstatus>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'g902ub211.xml'
            path.write_text(xml, encoding='utf-8')
            motion = extract.process_xml_file(path)
        self.assertEqual(motion['session'], '1985/86')
        self.assertEqual(motion['date'], '1985-01-01')
        self.assertEqual(extract.get_temporal_bin(motion['session']), 'group1_1985-1994')


def tokens(*triples):
    """One sentence of [word, lemma, upos] triples."""
    return [list(t) for t in triples]


class TestRemoveBoilerplate(unittest.TestCase):
    """03: phrases match on word forms; output is lemmas without AUX/PUNCT/SYM."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        phrases_file = Path(self.tmp.name) / 'phrases.txt'
        phrases_file.write_text('# comment\n\nmed anledning av\nriksdagen\nav motionen\n', encoding='utf-8')
        self.patterns = boilerplate.load_boilerplate_phrases(phrases_file)

    def tearDown(self):
        self.tmp.cleanup()

    def test_comments_and_blank_lines_skipped(self):
        self.assertEqual(len(self.patterns), 3)

    def test_phrase_removed_and_lemmas_returned(self):
        sentence = tokens(
            ('Med', 'med', 'ADP'), ('anledning', 'anledning', 'NOUN'), ('av', 'av', 'ADP'),
            ('skolorna', 'skola', 'NOUN'), ('behöver', 'behöva', 'VERB'), ('lärare', 'lärare', 'NOUN'),
            ('.', '.', 'PUNCT'),
        )
        self.assertEqual(boilerplate.remove_boilerplate([sentence], self.patterns), 'skola behöva lärare')

    def test_phrase_matched_on_word_form_not_lemma(self):
        # 'riksdagens' is a different word form from the phrase 'riksdagen', even though the lemma is 'riksdag'
        sentence = tokens(('riksdagens', 'riksdag', 'NOUN'), ('beslut', 'beslut', 'NOUN'))
        self.assertEqual(boilerplate.remove_boilerplate([sentence], self.patterns), 'riksdag beslut')
        sentence = tokens(('riksdagen', 'riksdag', 'NOUN'), ('beslutar', 'besluta', 'VERB'))
        self.assertEqual(boilerplate.remove_boilerplate([sentence], self.patterns), 'besluta')

    def test_modal_ska_dropped_but_noun_skola_kept(self):
        sentence = tokens(('Eleverna', 'elev', 'NOUN'), ('ska', 'skola', 'AUX'), ('gå', 'gå', 'VERB'),
                          ('i', 'i', 'ADP'), ('skolan', 'skola', 'NOUN'))
        self.assertEqual(boilerplate.remove_boilerplate([sentence], self.patterns), 'elev gå i skola')

    def test_symbols_and_punctuation_dropped(self):
        sentence = tokens(('50', '50', 'NUM'), ('%', '%', 'SYM'), ('av', 'av', 'ADP'), ('eleverna', 'elev', 'NOUN'), ('.', '.', 'PUNCT'))
        self.assertEqual(boilerplate.remove_boilerplate([sentence], self.patterns), '50 av elev')

    def test_phrase_does_not_match_across_sentences(self):
        first = tokens(('Vi', 'vi', 'PRON'), ('avstår', 'avstå', 'VERB'), ('av', 'av', 'ADP'))
        second = tokens(('Motionen', 'motion', 'NOUN'), ('avslås', 'avslå', 'VERB'))
        self.assertEqual(boilerplate.remove_boilerplate([first, second], self.patterns), 'vi avstå av\nmotion avslå')

    def test_one_line_per_sentence_and_empty_sentences_dropped(self):
        first = tokens(('Skolan', 'skola', 'NOUN'))
        only_boilerplate = tokens(('Riksdagen', 'riksdag', 'NOUN'), ('.', '.', 'PUNCT'))
        last = tokens(('Lärare', 'lärare', 'NOUN'))
        self.assertEqual(boilerplate.remove_boilerplate([first, only_boilerplate, last], self.patterns), 'skola\nlärare')

    def test_empty_input(self):
        self.assertEqual(boilerplate.remove_boilerplate([], self.patterns), '')

    def test_underscore_lemmas_dropped_and_counted(self):
        # Stanza expands abbreviations into multi-word lemmas ('t.ex.' -> 'till_exempel')
        sentence = tokens(('t.ex.', 'till_exempel', 'ADV'), ('lärare', 'lärare', 'NOUN'),
                          ('bl.a.', 'bland_annat', 'ADV'), ('T.ex.', 'till_exempel', 'ADV'))
        counts = boilerplate.defaultdict(boilerplate.Counter)
        self.assertEqual(boilerplate.remove_boilerplate([sentence], self.patterns, counts), 'lärare')
        self.assertEqual(counts['till_exempel'], {'t.ex.': 1, 'T.ex.': 1})
        self.assertEqual(counts['bland_annat'], {'bl.a.': 1})

    def test_underscore_lemma_inside_boilerplate_not_counted(self):
        sentence = tokens(('Riksdagen', 'riks_dag', 'NOUN'), ('skolan', 'skola', 'NOUN'))
        counts = boilerplate.defaultdict(boilerplate.Counter)
        self.assertEqual(boilerplate.remove_boilerplate([sentence], self.patterns, counts), 'skola')
        self.assertEqual(dict(counts), {})

    def test_underscore_counts_saved_most_frequent_first(self):
        counts = boilerplate.defaultdict(boilerplate.Counter)
        counts['med_flera']['m.fl.'] += 1
        counts['till_exempel']['t.ex.'] += 3
        counts['till_exempel']['T.ex.'] += 1
        output_file = Path(self.tmp.name) / 'underscore_lemmas.json'
        boilerplate.save_underscore_counts(counts, output_file)
        saved = boilerplate.json.loads(output_file.read_text(encoding='utf-8'))
        self.assertEqual(list(saved), ['till_exempel', 'med_flera'])
        self.assertEqual(saved['till_exempel'], {'count': 4, 'forms': {'t.ex.': 3, 'T.ex.': 1}})

    def test_trailing_punctuation_does_not_block_removal(self):
        # Stanza keeps the full stop in abbreviations ('mot.', 'prop.'); the phrase still removes the word
        sentence = tokens(('riksdagen.', 'riksdag', 'NOUN'), ('skolan', 'skola', 'NOUN'))
        self.assertEqual(boilerplate.remove_boilerplate([sentence], self.patterns), 'skola')

    def test_trailing_punctuation_rule_keeps_longer_words(self):
        sentence = tokens(('riksdagens.', 'riksdag', 'NOUN'), ('skolan', 'skola', 'NOUN'))
        self.assertEqual(boilerplate.remove_boilerplate([sentence], self.patterns), 'riksdag skola')

    def test_abbreviation_with_inner_and_trailing_full_stops(self):
        # 'milj.kr.' (miljoner kronor) is removed by the phrase 'milj.kr'
        patterns = boilerplate.load_boilerplate_phrases(PROJECT_ROOT / 'config' / 'boilerplate_phrases.txt')
        sentence = tokens(('500', '500', 'NUM'), ('milj.kr.', 'milj.kru', 'NOUN'), ('till', 'till', 'ADP'),
                          ('skolan', 'skola', 'NOUN'))
        self.assertNotIn('milj', boilerplate.remove_boilerplate([sentence], patterns))

    def test_lemma_corrections_applied(self):
        sentence = tokens(('kompetensen', 'kompet', 'NOUN'), ('lärarna', 'lärare', 'NOUN'))
        corrections = {'kompet': 'kompetens'}
        self.assertEqual(boilerplate.remove_boilerplate([sentence], self.patterns, lemma_corrections=corrections),
                         'kompetens lärare')

    def test_lemma_corrections_ignore_case(self):
        # A sentence-initial word keeps its capital in the lemma ('Kompetens' -> 'Kompet')
        sentence = tokens(('Kompetensen', 'Kompet', 'NOUN'), ('saknas', 'sakna', 'VERB'))
        self.assertEqual(boilerplate.remove_boilerplate([sentence], self.patterns, lemma_corrections={'kompet': 'kompetens'}),
                         'kompetens sakna')

    def test_lemma_corrections_in_compounds(self):
        corrections = {'*kompet': 'kompetens', 'anslagen': 'anslag'}
        self.assertEqual(boilerplate.correct_lemma('kompet', corrections), 'kompetens')
        self.assertEqual(boilerplate.correct_lemma('gymnasiekompet', corrections), 'gymnasiekompetens')
        self.assertEqual(boilerplate.correct_lemma('IT-kompet', corrections), 'it-kompetens')
        self.assertEqual(boilerplate.correct_lemma('anslagen', corrections), 'anslag')
        # Without '*' only the whole lemma is corrected
        self.assertEqual(boilerplate.correct_lemma('sammanslagen', corrections), 'sammanslagen')
        self.assertEqual(boilerplate.correct_lemma('lärare', corrections), 'lärare')

    def test_real_corrections_on_compounds(self):
        corrections = boilerplate.load_lemma_corrections(PROJECT_ROOT / 'config' / 'lemma_corrections.txt')
        self.assertEqual(boilerplate.correct_lemma('lärarkompet', corrections), 'lärarkompetens')
        self.assertEqual(boilerplate.correct_lemma('skolbibliotekarium', corrections), 'skolbibliotekarie')
        self.assertEqual(boilerplate.correct_lemma('sammanslagen', corrections), 'sammanslagen')

    def test_lemma_corrections_file(self):
        corrections_file = Path(self.tmp.name) / 'corrections.txt'
        corrections_file.write_text('# comment\n\nkompet  kompetens  # kompetens\nkåre kår\n', encoding='utf-8')
        self.assertEqual(boilerplate.load_lemma_corrections(corrections_file), {'kompet': 'kompetens', 'kåre': 'kår'})

    def test_real_lemma_corrections_file_loads(self):
        corrections = boilerplate.load_lemma_corrections(PROJECT_ROOT / 'config' / 'lemma_corrections.txt')
        self.assertEqual(corrections['*kompet'], 'kompetens')
        self.assertEqual(corrections['anslagen'], 'anslag')
        self.assertNotIn('*anslagen', corrections)  # would turn 'sammanslagen' into 'sammanslag'

    def test_real_phrase_file_loads(self):
        patterns = boilerplate.load_boilerplate_phrases(PROJECT_ROOT / 'config' / 'boilerplate_phrases.txt')
        self.assertGreater(len(patterns), 0)


class TestNormalizeText(unittest.TestCase):
    """04: lowercase, no digits or punctuation, no single-character words, line breaks kept."""

    def test_lowercase_digits_punctuation(self):
        self.assertEqual(normalize.normalize_text('Skolan 2024, bra!'), 'skolan bra')

    def test_single_character_words_removed(self):
        self.assertEqual(normalize.normalize_text('elev i skola å x'), 'elev skola')

    def test_line_breaks_kept_and_empty_lines_dropped(self):
        self.assertEqual(normalize.normalize_text('Skola\n123 .\nLärare'), 'skola\nlärare')

    def test_swedish_letters_kept(self):
        self.assertEqual(normalize.normalize_text('Lärare Över Åren'), 'lärare över åren')

    def test_empty_input(self):
        self.assertEqual(normalize.normalize_text(''), '')


class TestStopwords(unittest.TestCase):
    """05: stopword list (needs NLTK stopwords in SU/nltk_data) and removal."""

    @classmethod
    def setUpClass(cls):
        cls.stop_words = stopwords.get_swedish_stopwords()

    def test_common_words_are_stopwords(self):
        for word in ['och', 'att', 'som', 'det', 'ska', 'kommer', 'enligt']:
            self.assertIn(word, self.stop_words)

    def test_lemma_forms_are_stopwords(self):
        for word in ['behöva', 'vilja', 'kunna', 'ny', 'stor', 'olik', 'hel', 'mången']:
            self.assertIn(word, self.stop_words)

    def test_content_words_are_not_stopwords(self):
        # 'skola' is the lemma of both the noun (school) and the modal ska; it must stay
        for word in ['skola', 'lärare', 'elev', 'utbildning', 'förskola', 'högskola', 'sfi', 'csn', 'fn', 'eg', 'ky', 'ib']:
            self.assertNotIn(word, self.stop_words)

    def test_remove_stopwords_keeps_lines(self):
        text = 'skola och lärare\nvi vilja ha fler elev'
        self.assertEqual(stopwords.remove_stopwords(text, self.stop_words), 'skola lärare\nelev')

    def test_empty_input(self):
        self.assertEqual(stopwords.remove_stopwords('', self.stop_words), '')


if __name__ == '__main__':
    unittest.main()
