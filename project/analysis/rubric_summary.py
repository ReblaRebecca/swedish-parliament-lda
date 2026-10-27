#!/usr/bin/env python3
"""
Rubric summary: reads the coded sheet of analysis/rubric_coding_sheet.py and computes, per model, the
share of coherent topics, the share of thematic topics (of all topics, as Gordon's Table 2, and of the
coherent ones) and the mean party concentration, next to Gordon's (2026) values.

Coding rules checked: Coherent is yes or no; Thematic is yes or no for coherent topics and empty for
incoherent ones. Rows not yet coded are counted and left out of the shares.

Usage: python analysis/rubric_summary.py [sheet]
Output: docs/reports/RUBRIC_SUMMARY.md
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'analysis'))

from rubric_coding_sheet import COLUMNS, PERIOD_MODEL, SHEET_PATH, TOP_MOTIONS, WHOLE_CORPUS  # noqa: E402

REPORT_PATH = PROJECT_ROOT / 'docs' / 'reports' / 'RUBRIC_SUMMARY.md'
GORDON = ('Gordon (2026, Table 2): coherent 80–85%; thematic 47% (whole corpus, 15 topics), 62% (whole corpus, '
          '60 topics), 60–65% (binned models, MALLET and Authorless); mean author concentration 0.68–0.81.')


def read_rows(path):
    """The coding sheet's rows as dicts keyed by COLUMNS."""
    from openpyxl import load_workbook
    rows = list(load_workbook(path, read_only=True)['Coding'].values)
    if list(rows[0][:len(COLUMNS)]) != COLUMNS:
        sys.exit(f'{path}: unexpected columns {rows[0]}')
    return [dict(zip(COLUMNS, row)) for row in rows[1:] if any(v is not None for v in row)]


def answer(value):
    """'yes', 'no' or '' for one coded cell (case and spaces ignored)."""
    return (value or '').strip().lower() if isinstance(value, str) else ''


def check(rows):
    """Coding errors as messages: invalid answers, or Thematic set for an incoherent topic."""
    errors = []
    for row in rows:
        where = f"{row['Model']} {row['Period'] or ''} topic {row['Topic']}".replace('  ', ' ')
        coherent, thematic = answer(row['Coherent']), answer(row['Thematic'])
        if coherent not in ('', 'yes', 'no') or thematic not in ('', 'yes', 'no'):
            errors.append(f'{where}: answers must be yes or no')
        elif coherent == 'no' and thematic:
            errors.append(f'{where}: Thematic is coded only for coherent topics')
        elif coherent == 'yes' and not thematic:
            errors.append(f'{where}: coherent but Thematic not coded')
    return errors


def summarize(rows):
    """Counts and shares of one group of rows."""
    coded = [r for r in rows if answer(r['Coherent'])]
    coherent = [r for r in coded if answer(r['Coherent']) == 'yes']
    thematic = [r for r in coherent if answer(r['Thematic']) == 'yes']
    concentration = [float(r['Party concentration']) for r in rows]
    return {
        'topics': len(rows),
        'coded': len(coded),
        'coherent': len(coherent),
        'thematic': len(thematic),
        'coherent_share': len(coherent) / len(coded) if coded else None,
        'thematic_share': len(thematic) / len(coded) if coded else None,
        'thematic_of_coherent': len(thematic) / len(coherent) if coherent else None,
        'concentration': sum(concentration) / len(concentration) if concentration else None,
    }


def groups(rows):
    """(label, rows) for the whole-corpus model, each period model and the period models together."""
    whole = [r for r in rows if r['Model'] == WHOLE_CORPUS]
    period_rows = [r for r in rows if r['Model'] == PERIOD_MODEL]
    labels = list(dict.fromkeys(r['Period'] for r in period_rows))
    return ([('Whole corpus', whole)] + [(label, [r for r in period_rows if r['Period'] == label]) for label in labels]
            + [('Period models together', period_rows)])


def pct(value):
    return '–' if value is None else f'{value * 100:.0f}%'


def report(rows):
    lines = ['# Rubric Coding Summary', '',
             f'Coded sheet: `docs/rubric/{SHEET_PATH.name}` (`analysis/rubric_coding_sheet.py`), coded by hand as '
             'Gordon (2026, 3.3) by a single annotator. *Coherent*: the top words form a recognizable semantic '
             'field. *Thematic*: coherent and recurring subject matter, not a register, procedure or paratext; '
             'the share is of all coded topics (as Gordon) and of the coherent ones. *Party concentration*: '
             f'share of the top {TOP_MOTIONS} motions from the most frequent party among them (the counterpart '
             'of Gordon\'s author concentration).', '',
             '| Model | Topics | Coded | Coherent | Thematic | Thematic of coherent | Mean party concentration |',
             '|---|---|---|---|---|---|---|']
    for label, group in groups(rows):
        s = summarize(group)
        lines.append(f"| {label} | {s['topics']} | {s['coded']} | {pct(s['coherent_share'])} "
                     f"| {pct(s['thematic_share'])} | {pct(s['thematic_of_coherent'])} "
                     f"| {s['concentration']:.2f} |")
    lines += ['', GORDON, '']
    return '\n'.join(lines)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else SHEET_PATH
    rows = read_rows(path)
    errors = check(rows)
    if errors:
        sys.exit('Coding errors:\n' + '\n'.join(errors))
    uncoded = sum(1 for r in rows if not answer(r['Coherent']))
    if uncoded:
        print(f'Note: {uncoded} of {len(rows)} topics not yet coded; left out of the shares.')
    REPORT_PATH.write_text(report(rows), encoding='utf-8')
    print(f'✅ Report saved to: {REPORT_PATH}')


if __name__ == '__main__':
    main()
