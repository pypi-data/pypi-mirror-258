"""Bible classes."""

__version__ = '1.1.0'

import copy
import json
import os
from dataclasses import dataclass
from typing import Final, Union

import requests
from bs4 import BeautifulSoup, NavigableString
from bs4.element import Tag

from .data import BOOKS, CHAPTERS
from .utils import read_file, write_file

# Replace [EMAIL] with your own - let's be nice to The Lockman Foundation :)
USERAGENT: Final = "Python LSB Reader - [EMAIL]"

CLASS_TO_ATTR_MAPPING: Final = {
    'single-quote': 'quote#{}#1',
    'double-quote': 'quote#{}#2',
    'block-quote': 'indent#{}#1',
    'indented-block-quote': 'indent#{}#2',
    'poetry': 'poetry#{}#1',
}


@dataclass
class BibleMarker:
    """A specific verse in the Bible."""

    book: str
    chapter: int
    verse: int


@dataclass
class BibleRange:
    """A range of verse."""

    start: BibleMarker
    end: BibleMarker


def expand_book(book: str):
    """Attempt to get a Bible book based on the starting characters.

    For example, if you passed MAT it would return matthew. However, if you
    passed m, since that matches micah, malachi, matthew, and mark, we cannot
    determine the correct book, so an empty string will be returned. If the
    string passed doesn't match the start of ANY book, None is returned.
    """
    book = book.lower()
    if book in BOOKS:
        return book
    candidates = [_b for _b in BOOKS if _b.startswith(book)]
    if not candidates:
        return None
    if len(candidates) > 1:
        return ''
    return candidates[0]


class BibleGetter():
    """Manages a collection of Bible verses, downloading them when needed."""

    URL: Final = "https://read.lsbible.org/"

    def __init__(self, file):
        """Initialize Bible data."""
        self.file = file
        self.data = (json.loads(read_file(file)) if os.path.exists(file) else {
            book: {'chapters': CHAPTERS[idx]}
            for idx, book in enumerate(BOOKS)})
        self.changed = False

    def __get_chapter(self, book: str, chapter: int) -> dict:
        """Download a chapter of the Bible."""
        # print(f"Caching {book} {chapter}...")
        _r = requests.get(
            self.URL,
            params={'q': f'{book}{chapter}'},
            headers={'user-agent': USERAGENT},
            timeout=30)
        _bs = BeautifulSoup(_r.text, 'lxml')
        verses = _bs.find_all('span', class_='verse')
        self.data[book][str(chapter)] = {
            str(int(verse.attrs['data-key'][-3:])):
                BibleGetter.__jsonify_verse(
                    verse,
                    _bs,
                    int(verse.attrs['data-key'][-3:]))
            for verse in verses
        }
        self.data[book][str(chapter)]['verses'] = max({
            int(span.attrs['data-key'][-3:])
            for span in verses})
        self.changed = True
        if chapter == 1 or book == 'psalm':
            self.data[
                book][str(chapter)]['1']['attributes'].append('paragraph')
        return self.data[book][str(chapter)]

    @classmethod
    def __jsonify_verse(
        cls,
        verse: Tag,
        _bs: BeautifulSoup,
        verse_num: int
    ) -> dict:
        """Create a database entry for an HTML verse tag."""
        lines = [
            _c
            for _c in verse.contents
            if (_c.strip() if isinstance(_c, NavigableString) else (
                _c.get('class', '')
                and {
                    'prose',
                    'block-quote',
                    'poetry',
                    'indented-block-quote'
                }.intersection(set(_c['class']))))]
        attrs = []
        for idx, line in enumerate(lines):
            # Turn non-tagged strings into paragraphs
            if isinstance(line, str):
                _p = _bs.new_tag('p', attrs={'class': ''})
                _p.string = line
                line = _p
                lines[idx] = line
            for class_name, attr_template in CLASS_TO_ATTR_MAPPING.items():
                if class_name in line['class']:
                    attrs.append(attr_template.format(idx))
            if line.text.strip().endswith(' Higgaion Selah.'):
                attrs.append(f'higgaion-selah#{idx}#1')
                string = list(line.strings)[-1]
                string.replace_with(string.strip()[:-16])
            if line.text.strip().endswith(' Selah.'):
                attrs.append(f'selah#{idx}#1')
                string = list(line.strings)[-1]
                string.replace_with(string.strip()[:-7])
        # I wonder if these can be replaced with just find instead of find_all
        if verse.find_all('span', class_='start-pericope', recursive=False):
            attrs.append('paragraph')
        if verse.find_all('br'):
            attrs.append('break')
        search = verse.find_all('h3', class_='hebrew-letter')
        if search:
            attrs.append('acrostic')
            attrs.append(f'acrostic#{search[0].text}')
        heading = ''
        search = verse.find_all('h3', class_='subhead')
        if search:
            heading = search[0].text
            if verse_num == 1:
                attrs.append('paragraph')
        subheading = ''
        search = verse.find_all('div', class_='included-subhead')
        if search:
            subheading = search[0].text
        return {
            'attributes': attrs,
            'heading': heading,
            'subheading': subheading,
            'text': [BibleGetter.__stringify_line(_v).text for _v in lines]
        }

    def __list(
        self,
        selection: BibleRange,
        redownload: bool
    ) -> list[BibleMarker]:
        """Generate a list of each verse referenced in a BibleRange."""
        ret = []
        # Get book range (since these are non-numeric)
        books = list(self.data.keys())
        for book in books[
            books.index(selection.start.book):
            books.index(selection.end.book) + 1
        ]:
            for chapter in range(
                1 if selection.start.book != book else selection.start.chapter,
                (
                    self.data[book]['chapters']
                    if selection.end.book != book
                    else selection.end.chapter
                ) + 1
            ):
                if redownload or str(chapter) not in self.data[book]:
                    self.__get_chapter(book, chapter)
                ret.extend([
                    BibleMarker(book, chapter, verse)
                    for verse in range(
                        (
                            1
                            if selection.start.book != book
                            or selection.start.chapter != chapter
                            else selection.start.verse
                        ),
                        (
                            self.data[book][str(chapter)]['verses']
                            if selection.end.book != book
                            or selection.end.chapter != chapter
                            else selection.end.verse
                        ) + 1
                    )])
        # print(f"Returning: {ret}")
        return ret

    @classmethod
    def __stringify_line(cls, line: Tag) -> str:
        """Stringifies certain elements of an HTML verse tag."""
        for caps in line.find_all('span', class_='small-caps'):
            for _s in list(caps.strings):
                _s.replace_with(_s.upper())
        for red in line.find_all('span', class_='red-letter'):
            for _s in list(red.strings):
                _s.replace_with(f'\033[31m{_s.text}\033[39m')
        for italic in line.select('i'):
            italic.replace_with(f'\033[3m{italic.text}\033[23m')
        return line

    def find_attribute_backwards(
        self,
        start: BibleMarker,
        attr: str,
        inclusive: bool = False,
        redownload: bool = False
    ) -> BibleMarker:
        """Search for the first verse with attr, towards Genesis 1."""
        prev_ = start
        next_ = copy.copy(start)
        if redownload:
            self.data[next_.book].pop(str(next_.chapter))
        while True:
            if str(next_.chapter) not in self.data[next_.book]:
                self.__get_chapter(next_.book, next_.chapter)
            if (
                attr in self.data
                    [next_.book][str(next_.chapter)][str(next_.verse)]
                    ['attributes']
            ):
                break
            if next_.verse == 1:
                if next_.chapter == 1:
                    if next_.book == 'genesis':
                        break
                    prev_ = copy.copy(next_)
                    idx = BOOKS.index(next_.book)
                    next_.book = BOOKS[idx - 1]
                    next_.chapter = CHAPTERS[idx - 1]
                else:
                    prev_ = copy.copy(next_)
                    next_.chapter -= 1
                if (
                    redownload
                    or str(next_.chapter) not in self.data[next_.book]
                ):
                    self.__get_chapter(next_.book, next_.chapter)
                next_.verse = self.data[
                    next_.book][str(next_.chapter)]['verses']
            else:
                prev_ = copy.copy(next_)
                next_.verse -= 1
        return next_ if inclusive else prev_

    def find_attribute_forwards(
        self,
        start: BibleMarker,
        attr: str,
        inclusive: bool = False,
        redownload: bool = False
    ) -> BibleMarker:
        """Search for the first verse with attr, towards Revelation 22."""
        prev_ = start
        next_ = copy.copy(start)
        if redownload:
            self.data[next_.book].pop(str(next_.chapter))
        while True:
            if str(next_.chapter) not in self.data[next_.book]:
                self.__get_chapter(next_.book, next_.chapter)
            if (
                next_ != start
                and attr in self.data
                    [next_.book][str(next_.chapter)][str(next_.verse)]
                    ['attributes']
            ):
                break
            if (
                next_.verse == self.data[
                    next_.book][str(next_.chapter)]['verses']
            ):
                if next_.chapter == self.data[next_.book]['chapters']:
                    if next_.book == 'revelation':
                        break
                    prev_ = copy.copy(next_)
                    idx = BOOKS.index(next_.book)
                    next_.book = BOOKS[idx + 1]
                    next_.chapter = 0
                else:
                    prev_ = copy.copy(next_)
                next_.chapter += 1
                next_.verse = 0
            else:
                prev_ = copy.copy(next_)
            next_.verse += 1
        return next_ if inclusive else prev_

    def get(
        self,
        selection: Union[BibleMarker, BibleRange],
        redownload: bool
    ) -> dict:
        """Retrieve a specified verse, or range of verses."""
        if not self.valid(selection):
            return {}
        if isinstance(selection, BibleMarker):
            selection = BibleRange(selection, selection)
        ret = {}
        for marker in self.__list(selection, redownload):
            if marker.book not in ret:
                ret[marker.book] = {}
            if marker.chapter not in ret[marker.book]:
                ret[marker.book][marker.chapter] = {}
            ret[marker.book][marker.chapter][marker.verse] = (
                self.data[marker.book][str(marker.chapter)][str(marker.verse)])
        return ret

    def get_chapters(self, book: str) -> int:
        """Get the chapter count for a particular book of the Bible."""
        return self.data[book]['chapters'] if book in self.data else 0

    def get_verses(self, book: str, chapter: int) -> int:
        """Get the verse count for a particular chapter of the Bible."""
        if (
            book not in self.data
            or chapter < 1
            or chapter > self.data[book]['chapters']
        ):
            return 0
        if str(chapter) not in self.data[book]:
            self.__get_chapter(book, chapter)
        return self.data[book][str(chapter)]['verses']

    def highlight(self, book: str, chapter: int, verse: int, color: int):
        """Highlight a verse.

        If color is 0, the highlight is removed.
        """
        attrs = self.data[book][str(chapter)][str(verse)]['attributes']
        attrs = [
            _a
            for _a in attrs
            if not _a.startswith('highlight#')]
        if color != 0:
            attrs.append(f'highlight#{color}')
        self.changed = True
        self.data[book][str(chapter)][str(verse)]['attributes'] = attrs

    def save(self):
        """Write back data if changed."""
        if self.changed:
            write_file(self.file, json.dumps(self.data))
            self.changed = False

    def valid(self, selection: Union[BibleMarker, BibleRange]) -> bool:
        """Check if a Scripture reference is valid.

        If a chapter is valid, and is not downloaded yet, it gets downloaded
        before this function returns.
        """
        if isinstance(selection, BibleMarker):
            return (
                selection.book in self.data
                and selection.chapter > 0
                and selection.chapter <= self.data[selection.book]['chapters']
                and selection.verse > 0
                and (
                    str(selection.chapter) in self.data[selection.book]
                    or self.__get_chapter(
                        selection.book,
                        selection.chapter)
                )
                and selection.verse <= self.data[
                    selection.book][str(selection.chapter)]['verses'])
        # Is range
        return self.valid(selection.start) and self.valid(selection.end)
