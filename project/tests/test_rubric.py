#!/usr/bin/env python3
"""Tests for the rubric coding sheet and its summary (analysis/rubric_coding_sheet.py, rubric_summary.py)."""

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'modeling'))
sys.path.insert(0, str(PROJECT_ROOT / 'analysis'))

import rubric_coding_sheet as sheet  # noqa: E402
import rubric_summary as summary  # noqa: E402


def row(model='Whole corpus', period='', topic=1, coherent='', thematic='', concentration=0.4):
    return dict(zip(sheet.COLUMNS, [model, period, topic, 'ord', 'motion', concentration, 'S', coherent, thematic, '']))


class TestPartyConcentration(unittest.TestCase):
    def test_range(self):
        self.assertEqual(sheet.party_concentration(['S', 'M', 'C', 'L', 'V']), (0.2, 'V'))
        self.assertEqual(sheet.party_concentration(['S'] * 5), (1.0, 'S'))
        self.assertEqual(sheet.party_concentration(['S', 'S', 'M', 'S', 'C']), (0.6, 'S'))

    def test_no_party_counts_for_none(self):
        """Motions without a party are not one party: two unknowns do not make a concentration of 0.4."""
        self.assertEqual(sheet.party_concentration(['?', '?', 'S', 'M', 'C']), (0.2, 'S'))
        self.assertEqual(sheet.party_concentration(['?'] * 5), (0.2, ''))


class TestCodingChecks(unittest.TestCase):
    def test_valid(self):
        rows = [row(coherent='yes', thematic='no'), row(coherent='No'), row(coherent=' YES ', thematic='yes'), row()]
        self.assertEqual(summary.check(rows), [])

    def test_errors(self):
        self.assertEqual(len(summary.check([row(coherent='maybe')])), 1)
        self.assertEqual(len(summary.check([row(coherent='no', thematic='yes')])), 1)   # thematic needs coherent
        self.assertEqual(len(summary.check([row(coherent='yes')])), 1)                  # thematic missing


class TestSummary(unittest.TestCase):
    def test_shares(self):
        """Thematic share of all coded topics, as Gordon's Table 2, and of the coherent ones; uncoded left out."""
        rows = [row(coherent='yes', thematic='yes', concentration=1.0), row(coherent='yes', thematic='no'),
                row(coherent='yes', thematic='yes'), row(coherent='no'), row(concentration=0.2)]
        s = summary.summarize(rows)
        self.assertEqual((s['topics'], s['coded'], s['coherent'], s['thematic']), (5, 4, 3, 2))
        self.assertAlmostEqual(s['coherent_share'], 0.75)
        self.assertAlmostEqual(s['thematic_share'], 0.5)
        self.assertAlmostEqual(s['thematic_of_coherent'], 2 / 3)
        self.assertAlmostEqual(s['concentration'], (1.0 + 0.4 * 3 + 0.2) / 5)

    def test_groups(self):
        rows = [row(), row(model='Period', period='A'), row(model='Period', period='B'), row(model='Period', period='A')]
        self.assertEqual([(label, len(g)) for label, g in summary.groups(rows)],
                         [('Whole corpus', 1), ('A', 2), ('B', 1), ('Period models together', 3)])

    def test_sheet_round_trip(self):
        """A written sheet is read back with the same rows; the coding columns start empty."""
        rows = [['Whole corpus', '', 1, 'a, b', 'motion', 0.6, 'S', '', '', ''],
                ['Period', '1985/86–1993/94', 2, 'c, d', 'motion', 0.2, '', '', '', '']]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'sheet.xlsx'
            sheet.write_sheet(rows, path)
            read = summary.read_rows(path)
        self.assertEqual([(r['Model'], r['Topic'], r['Party concentration']) for r in read],
                         [('Whole corpus', 1, 0.6), ('Period', 2, 0.2)])
        self.assertEqual(summary.check(read), [])
        self.assertEqual(summary.summarize(read)['coded'], 0)


if __name__ == '__main__':
    unittest.main()
