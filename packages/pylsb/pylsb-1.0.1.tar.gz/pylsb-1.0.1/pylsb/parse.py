"""Argument parsing for PyLSB."""

__version__ = '1.0.0'

import argparse
import random
import re
import sys
from typing import Union

from .bible import BibleGetter, BibleMarker, BibleRange, expand_book
from .data import BOOKS

VERSE = r"(\d?)\s*([a-zA-Z]+)\s*(\d+)(?::(\d+))?"
VERSE_OPT = r"(\d??)\s*([a-zA-Z]+)?\s*(\d+)(?::(\d+))?"
BIBLE_REGEX = re.compile(rf"^\s*{VERSE}\s*(?:-\s*{VERSE_OPT}\s*)?$")


def parse_scripture(arg: str, bible: BibleGetter) -> BibleRange:
    """Parse a verse string into a BibleRange.

    Returns None if it fails to parse.
    """
    # Read a verse or range of verses
    match = BIBLE_REGEX.match(arg)
    if not match:
        raise ValueError(f'Unable to parse {arg} as a Bible verse or range.')
    start = BibleMarker(
        f"{match.group(1) or ''}{match.group(2)}",
        int(match.group(3)),
        -1 if not match.group(4) else int(match.group(4)))
    end = BibleMarker(
        f"{match.group(5) or ''}"
        f"{match.group(6) or ''}",
        -1 if not match.group(7) else int(match.group(7)),
        -1 if not match.group(8) else int(match.group(8)))
    # Expand shortened name
    _sb = expand_book(start.book)
    if _sb is None:
        raise ValueError(
            f'{start.book} '
            'does not match the start of any book of the Bible.')
    if not _sb:
        raise ValueError(
            f'{start.book} matches more than one book of the Bible.')
    start.book = _sb
    # Make sure chapter is valid
    if start.chapter > bible.get_chapters(start.book):
        raise ValueError(
            f"{start.book.title()} doesn't have that many chapters!")
    return BibleRange(start, end)


def get_scripture(
    arg: str,
    bible: BibleGetter
) -> Union[BibleMarker, BibleRange]:
    """Get the appropriate BibleMarker or BibleRange for a string.

    Returns None if it fails to parse, or if invalid values are given.
    """
    # Custom arguments
    if arg == 'random':
        book = random.choice(BOOKS)
        chapter = random.choice(range(0, bible.get_chapters(book))) + 1
        return BibleMarker(
            book,
            chapter,
            random.choice(range(0, bible.get_verses(book, chapter))) + 1)
    # Standard argument
    range_ = parse_scripture(arg, bible)
    # No range explicitly given
    if range_.end.chapter == -1:
        # Single verse
        if range_.start.verse != -1:
            return range_.start
        # No starting verse specified, so give the whole chapter
        range_.start.verse = 1
        range_.end = BibleMarker(
            range_.start.book,
            range_.start.chapter,
            bible.get_verses(range_.start.book, range_.start.chapter))
    # Explicit range
    else:
        # Different book
        if range_.end.book:
            # Expand shortened name
            _eb = expand_book(range_.end.book)
            if _eb is None:
                raise argparse.ArgumentTypeError(
                    f'{range_.end.book} '
                    'does not match the start of any book of the Bible.')
            if not _eb:
                raise argparse.ArgumentTypeError(
                    f'{range_.end.book} '
                    'matches more than one book of the Bible.')
            range_.end.book = _eb
        # No book specified (same book)
        else:
            # Make sure chapter isn't actually a verse
            if range_.end.verse == -1 and range_.start.verse != -1:
                range_.end.verse = range_.end.chapter
                range_.end.chapter = range_.start.chapter
            range_.end.book = range_.start.book
        # Make sure chapter is valid
        if range_.end.chapter > bible.get_chapters(range_.end.book):
            raise argparse.ArgumentTypeError(
                f'{range_.end.book.title()} '
                "doesn't have that many chapters!")
        # Fill in missing data where applicable
        if range_.start.verse == -1:
            range_.start.verse = 1
        if range_.end.verse == -1:
            range_.end.verse = bible.get_verses(
                range_.end.book,
                range_.end.chapter)
    return range_


def get_highlight(val: str) -> int:
    """Parse a string as either a 1-3 digit integer, or a 6 digit hex value."""
    val = val.strip()
    if val.startswith('-'):
        raise argparse.ArgumentTypeError('color must be a positive value')
    if len(val) < 4:
        return int(val)
    if len(val[2:] if val.startswith('0x') else val) != 6:
        raise argparse.ArgumentTypeError('color should be 1, 2, 3 or 6 digits')
    return -int(val, 16)


def args(bible: BibleGetter) -> list[Union[BibleMarker, BibleRange]]:
    """Parse sys.argv into Scripture and options."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options] scripture [scripture ...]',
        description=(
            'Downloads, displays, and caches verses '
            'from the Legacy Standard Bible'),
        epilog=(
            'The scripture references and options '
            'may be passed in any order.'))
    parser.add_argument(
        'scripture',
        action='store',
        help=(
            'chapter, verse, range of chapters or verses, '
            'or "random" for a random verse'),
        nargs='+',
        type=lambda _s: get_scripture(_s.lower(), bible))
    parser.add_argument(
        '-p',
        '--paragraph',
        action='store_true',
        help='expand a verse or range to include the whole paragraph')
    parser.add_argument(
        '-r',
        '--redownload',
        action='store_true',
        help='force a cache update even if the verses are already downloaded')
    parser.add_argument(
        '-n',
        '--nored',
        action='store_true',
        help='disable red text quotes')
    parser.add_argument(
        '-8',
        '--80columns',
        action='store_true',
        help='force width to 80 columns (ignore terminal settings)',
        dest='columns80')
    parser.add_argument(
        '-w',
        '--web',
        action='store_true',
        help='format text like the web version instead of the print version')
    parser.add_argument(
        '-b',
        '--browser',
        action='store_true',
        help='open scripture in web browser')
    parser.add_argument(
        '-f',
        '--preface',
        action='store_true',
        help='display preface before scripture')
    parser.add_argument(
        '-m',
        '--highlight',
        action='store',
        help=(
            'highlight all selected verses with specified color num '
            '(0 to remove)'),
        metavar='color',
        type=get_highlight)
    parser.add_argument(
        '-2',
        '--split',
        action='store_true',
        help='print verses in 2 columns, one screen at a time')
    return parser.parse_args(sys.argv[1:])
