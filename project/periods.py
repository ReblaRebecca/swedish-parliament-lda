"""
The four periods of the study, defined once for the whole pipeline.

The periods follow complete electoral terms (mandatperioder), as equal in size as the terms allow.
Motions are assigned by parliamentary session (riksmöte, the XML field 'rm'), not by date: the session
is the unit of parliamentary work, and some motions carry a placeholder date (1985/86 motions dated
1985-01-01).

    Period   Sessions           Electoral terms beginning
    1        1985/86-1993/94    1985, 1988, 1991
    2        1994/95-2005/06    1994, 1998, 2002
    3        2006/07-2013/14    2006, 2010
    4        2014/15-2025/26    2014, 2018, 2022

Each period is stored as one JSONL file per data stage, named after the calendar years its sessions
span (group1_1985-1994.jsonl, ...). The part after 'group<n>_' is the period's key, used in file and
model names; pages and reports show the sessions instead (1985/86–1993/94, ...).
"""

import re

# (file stem, first session's start year, last session's start year)
PERIODS = [
    ('group1_1985-1994', 1985, 1993),
    ('group2_1994-2006', 1994, 2005),
    ('group3_2006-2014', 2006, 2013),
    ('group4_2014-2026', 2014, 2025),
]

PERIOD_FILES = [f'{stem}.jsonl' for stem, _, _ in PERIODS]


def session_start_year(session):
    """Start year of a session: '1985/86' -> 1985, '1999/2000' -> 1999; None unless two consecutive years."""
    match = re.fullmatch(r'(\d{4})/(\d{2}|\d{4})', (session or '').strip())
    if not match:
        return None
    start, end = int(match.group(1)), match.group(2)
    expected = str(start + 1) if len(end) == 4 else f'{(start + 1) % 100:02d}'
    return start if end == expected else None


def period_of_session(session):
    """File stem of the period a session belongs to ('1985/86' -> 'group1_1985-1994'); None if outside."""
    year = session_start_year(session)
    if year is None:
        return None
    for stem, first, last in PERIODS:
        if first <= year <= last:
            return stem
    return None


def session_name(start_year):
    """1985 -> '1985/86', 1999 -> '1999/2000'."""
    end = start_year + 1
    return f'{start_year}/{end}' if end % 100 == 0 else f'{start_year}/{end % 100:02d}'


def period_key(stem):
    """'group1_1985-1994' -> '1985-1994'."""
    return stem.split('_', 1)[-1]


# Period key -> name shown on pages and in reports: '1985-1994' -> '1985/86–1993/94'
DISPLAY_NAMES = {period_key(stem): f'{session_name(first)}–{session_name(last)}' for stem, first, last in PERIODS}
