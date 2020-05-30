"""
Tests for the _selectors module
"""

import pytest
import cssselect
from html.parser import HTMLParser
from gopher_render._parser import DocumentParser

from gopher_render._selectors import tag_matches


class MockTagParser(object):
    def __init__(self, tag, parent, attrs):
        self.tag = tag
        self.parent = parent
        self.children = []
        self.attrs = {}
        self.classes = []
        self.id = None
        if attrs is not None:
            self.attrs = dict(attrs)
            self.classes = self.__extract_classes()
            self.id = self.attrs.get('id', None)

    def tag_children(self):
        """
        Return only the children that represent tags (i.e. exclude any DataParsers)
        """
        return [t for t in self.children if t.tag is not None]

    def __extract_classes(self):
        if 'class' in self.attrs:
            self.attrs['class'] = self.attrs['class'].split()
            return self.attrs['class']
        return []


class MockDataParser(MockTagParser):
    def __init__(self, parent, data, **context):
        super().__init__(None, parent, None, **context)
        self.data = data


def test_basic_element_match():
    """
    Tests basic element selectors on their own
    """
    doc = DocumentParser()
    doc.append(MockTagParser('p', doc, ()))
    target = MockTagParser('p', doc, ())
    doc.append(target)

    match = cssselect.parse('p')
    match_ok, s = tag_matches(target, match)
    assert match_ok

    no_match = cssselect.parse('div')
    no_match_ok, s = tag_matches(target, no_match)
    assert not no_match_ok


def _perform_checks(elements, checks):
    for check_set in checks:
        selector = check_set[0]
        results = check_set[1]
        for index in range(0, len(elements)):
            match, specificity = tag_matches(
                elements[index],
                cssselect.parse(selector)
            )
            assert match == results[index], "Selector '{}' failed assertion index {}".format(selector, index)


def test_id_match():
    """
    Tests the id selector
    """
    doc = DocumentParser()
    elements = (
        MockTagParser('p', doc, ()),
        MockDataParser(doc, "\n"),
        MockTagParser('p', doc, (('id', 'para1'),)),
        MockTagParser('p', doc, (('id', 'para2'),)),
        MockTagParser('div', doc, (('id', 'div1'),)),
        MockTagParser('div', doc, ()),
    )
    for e in elements:
        doc.append(e)

    checks = (
        ('#nothing',    (False, False, False, False, False, False,)),
        ('#para1',      (False, False, True, False, False, False,)),
        ('p#para1',     (False, False, True, False, False, False,)),
        ('div#para1',   (False, False, False, False, False, False,)),
        ('#div1',       (False, False, False, False, True, False,)),
        ('div#div1',    (False, False, False, False, True, False,)),
        ('div',         (False, False, False, False, True, True,)),
    )
    for check_set in checks:
        selector = check_set[0]
        results = check_set[1]
        for index in range(0, len(elements)):
            match, specificity = tag_matches(
                elements[index],
                cssselect.parse(selector)
            )
            assert match == results[index], "Selector '{}' failed assertion index {}".format(selector, index)


def test_class_match():
    """
    Basic tests of the class selector
    """
    doc = DocumentParser()
    elements = (
        MockTagParser('p', doc, ()),
        MockDataParser(doc, "\n"),
        MockTagParser('p', doc, (('id', 'para1'),('class', 'c1'))),
        MockTagParser('p', doc, (('id', 'para2'),('class', 'c1 c2'))),
        MockTagParser('div', doc, (('id', 'div1'),)),
        MockTagParser('div', doc, (('class', 'c2'),)),
    )
    for e in elements:
        doc.append(e)

    checks = (
        ('.nothing',    (False, False, False, False, False, False,)),
        ('.c1',         (False, False, True, True, False, False,)),
        ('.c2#para2',   (False, False, False, True, False, False,)),
        ('div.c2',      (False, False, False, False, False, True,)),
        ('#div1.c1',    (False, False, False, False, False, False,)),
        ('.div1',       (False, False, False, False, False, False,)),
        ('div',         (False, False, False, False, True, True,)),
    )
    for check_set in checks:
        selector = check_set[0]
        results = check_set[1]
        for index in range(0, len(elements)):
            match, specificity = tag_matches(
                elements[index],
                cssselect.parse(selector)
            )
            assert match == results[index], "Selector '{}' failed assertion index {}".format(selector, index)


# Technically this is a pseudoclass, but cssselect does not treat it as such
def test_negation_match():
    """
    Basic tests of the negation selector (:not())
    """
    doc = DocumentParser()
    elements = (
        MockTagParser('p', doc, ()),
        MockDataParser(doc, "\n"),
        MockTagParser('p', doc, (('id', 'para1'),('class', 'c1'))),
        MockTagParser('p', doc, (('id', 'para2'),('class', 'c1 c2'))),
        MockTagParser('div', doc, (('id', 'div1'),)),
        MockTagParser('div', doc, (('class', 'c2'),)),
    )
    for e in elements:
        doc.append(e)

    checks = (
        (':not(span)',      (True, False, True, True, True, True,)),
        ('p:not(.c2)',      (True, False, True, False, False, False,)),
        ('p:not(#para1)',   (True, False, False, True, False, False,)),
        ('.c1:not(.c2)',    (False, False, True, False, False, False,)),
        (':not(p)',         (False, False, False, False, True, True,)),
    )
    _perform_checks(elements, checks)


def test_multiple_selectors_match():
    """
    Basic tests of multiple selectors in one specification
    """
    doc = DocumentParser()
    elements = (
        MockTagParser('p', doc, ()),
        MockDataParser(doc, "\n"),
        MockTagParser('p', doc, (('id', 'para1'),('class', 'c1'))),
        MockTagParser('p', doc, (('id', 'para2'),('class', 'c1 c2'))),
        MockTagParser('div', doc, (('id', 'div1'),)),
        MockTagParser('div', doc, (('class', 'c2'),)),
    )
    for e in elements:
        doc.append(e)

    # TODO: Should really be checking the specificity returned by these
    checks = (
        ('p, p#para1, #para2, .c1, div',      (True, False, True, True, True, True,)),
        ('p.c2, div#div1',                    (False, False, False, True, True, False,)),
        ('div, div#div1',                     (False, False, False, False, True, True,)),
    )
    _perform_checks(elements, checks)


class TestCombinators:
    """
    Tests for combinator selectors
    """

    def test_child(self):
        """
        Check child combinator (>)
        """
        doc = DocumentParser()
        toplevel = (
            MockTagParser('h1', doc, (('id', 'bigheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('section', doc, (('id', 'section1'),('class', 'docsec'))),
            MockTagParser('section', doc, (('id', 'section2'),('class', 'docsec'))),
        )
        for e in toplevel:
            doc.append(e)
        section1 = toplevel[2]
        section1.children.extend((
            MockTagParser('h2', section1, (('class', 'sectionheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('p', section1, ()),
            MockTagParser('p', section1, ()),
        ))
        section2 = toplevel[3]
        section2.children.extend((
            MockTagParser('h2', section2, (('class', 'sectionheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('p', section2, (('id', 'special'),)),
            MockTagParser('div', section2, ()),
        ))

        toplevel_checks = (
            ('section > h1',                (False, False, False, False)),
            ('section > p',                 (False, False, False, False)),
            ('div > p',                     (False, False, False, False)),
            ('section > .sectionheader',    (False, False, False, False)),
            ('section > div',               (False, False, False, False)),
            ('h1 > section',                (False, False, False, False)),
            ('#nothing > h1',               (False, False, False, False)),
            ('.sectionheader > h1',         (False, False, False, False)),
        )
        _perform_checks(toplevel, toplevel_checks)

        section1_checks = (
            ('section > h2',                (True, False, False, False)),
            ('section > p',                 (False, False, True, True)),
            ('div > p',                     (False, False, False, False)),
            ('section > .sectionheader',    (True, False, False, False)),
            ('section > div',               (False, False, False, False)),
        )
        _perform_checks(section1.children, section1_checks)

        section2_checks = (
            ('section > h2',                (True, False, False, False)),
            ('section > p',                 (False, False, True, False)),
            ('div > p',                     (False, False, False, False)),
            ('section > .sectionheader',    (True, False, False, False)),
            ('section > div',               (False, False, False, True)),
            ('section > #special',          (False, False, True, False)),
            ('section > p#special',         (False, False, True, False)),
        )
        _perform_checks(section2.children, section2_checks)


    def test_general_sibling(self):
        """
        Check general sibling combinator (~)
        """
        doc = DocumentParser()
        toplevel = (
            MockTagParser('h1', doc, (('id', 'bigheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('section', doc, (('id', 'section1'),('class', 'docsec'))),
            MockTagParser('section', doc, (('id', 'section2'),('class', 'docsec'))),
        )
        for e in toplevel:
            doc.append(e)
        section1 = toplevel[1]
        section1.children.extend((
            MockTagParser('h2', section1, (('class', 'sectionheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('p', section1, ()),
            MockTagParser('p', section1, (('class', 'last'),)),
        ))
        section2 = toplevel[2]
        section2.children.extend((
            MockTagParser('h2', section2, (('class', 'sectionheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('p', section2, (('id', 'special'),)),
            MockTagParser('div', section2, ()),
        ))

        toplevel_checks = (
            ('section ~ h1',                (False, False, False, False)),
            ('h1 ~ section',                (False, False, True, True)),
            ('div ~ p',                     (False, False, False, False)),
            ('#bigheader ~ #section1',      (False, False, True, False)),
            ('#bigheader ~ #section2',      (False, False, False, True)),
            ('#bigheader ~ .docsec',        (False, False, True, True)),
            ('h1 ~ .docsec',                (False, False, True, True)),
            ('.sectionheader ~ .docsec',    (False, False, False, False)),
        )
        _perform_checks(toplevel, toplevel_checks)

        section1_checks = (
            ('h2 ~ p',                      (False, False, True, True)),
            ('section ~ p',                 (False, False, False, False)),
            ('p ~ p',                       (False, False, False, True)),
            ('.sectionheader ~ p',          (False, False, True, True)),
            ('h2 ~ .last',                  (False, False, False, True)),
            ('.sectionheader ~ .last',      (False, False, False, True)),
            ('.sectionheader ~ p.last',     (False, False, False, True)),
        )
        _perform_checks(section1.children, section1_checks)

        section2_checks = (
            ('section ~ h2',                (False, False, False, False)),
            ('div ~ p',                     (False, False, False, False)),
            ('p ~ div',                     (False, False, False, True)),
            ('h2 ~ div',                    (False, False, False, True)),
            ('h2.sectionheader ~ #special', (False, False, True, False)),
        )
        _perform_checks(section2.children, section2_checks)


    def test_adjacent_sibling(self):
        """
        Check adjacent sibling combinator (+)
        """
        doc = DocumentParser()
        toplevel = (
            MockTagParser('h1', doc, (('id', 'bigheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('section', doc, (('id', 'section1'),('class', 'docsec'))),
            MockTagParser('section', doc, (('id', 'section2'),('class', 'docsec'))),
        )
        for e in toplevel:
            doc.append(e)
        section1 = toplevel[1]
        section1.children.extend((
            MockTagParser('h2', section1, (('class', 'sectionheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('p', section1, ()),
            MockTagParser('p', section1, (('class', 'last'),)),
        ))
        section2 = toplevel[2]
        section2.children.extend((
            MockTagParser('h2', section2, (('class', 'sectionheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('p', section2, (('id', 'special'),)),
            MockTagParser('div', section2, ()),
        ))

        toplevel_checks = (
            ('section + h1',                (False, False, False, False)),
            ('h1 + section',                (False, False, True, False)),
            ('#section1 + #section2',       (False, False, False, True)),
            ('#bigheader + section',        (False, False, True, False)),
            ('#section1 + section',         (False, False, False, True)),
            ('h1 + .docsec',                (False, False, True, False)),
        )
        _perform_checks(toplevel, toplevel_checks)

        section1_checks = (
            ('h2 + p',                      (False, False, True, False)),
            ('p + p',                       (False, False, False, True)),
            ('.sectionheader + #special',   (False, False, False, False)),
            ('h2 + .last',                  (False, False, False, False)),
        )
        _perform_checks(section1.children, section1_checks)

        section2_checks = (
            ('h2 + div',                    (False, False, False, False)),
            ('p + div',                     (False, False, False, True)),
            ('div + p',                     (False, False, False, False)),
            ('h2 + div',                    (False, False, False, False)),
            ('.sectionheader + #special',   (False, False, True, False)),
        )
        _perform_checks(section2.children, section2_checks)


    def test_descendant(self):
        """
        Check descendant combinator (' ')
        """
        doc = DocumentParser()
        toplevel = (
            MockTagParser('h1', doc, (('id', 'bigheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('section', doc, (('id', 'section1'),('class', 'docsec'))),
        )
        for e in toplevel:
            doc.append(e)
        section1 = toplevel[2]
        section1.children.extend((
            MockTagParser('h2', section1, (('class', 'sectionheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('p', section1, ()),
            MockDataParser(doc, "\n"),
            MockTagParser('div', section1, (('class', 'last'),)),
        ))
        section2 = section1.children[4]
        section2.children.extend((
            MockTagParser('h2', section2, (('class', 'sectionheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('p', section2, (('id', 'special'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('div', section2, ()),
        ))

        toplevel_checks = (
            ('section h1',                (False, False, False)),
            ('h1 section',                (False, False, False)),
        )
        _perform_checks(toplevel, toplevel_checks)

        section1_checks = (
            ('section p',                 (False, False, True, False, False)),
            ('.docsec p',                 (False, False, True, False, False)),
            ('#section1 p',               (False, False, True, False, False)),
            ('h1 p',                      (False, False, False, False, False)),
            ('.docsec .last',             (False, False, False, False, True)),
        )
        _perform_checks(section1.children, section1_checks)

        section2_checks = (
            ('section p',                 (False, False, True, False, False)),
            ('.docsec p',                 (False, False, True, False, False)),
            ('#section1 p',               (False, False, True, False, False)),
            ('#section1 h2',              (True, False, False, False, False)),
            ('#section1 p#special',       (False, False, True, False, False)),
            ('h1 p',                      (False, False, False, False, False)),
            ('.docsec .last',             (False, False, False, False, False)),
        )
        _perform_checks(section2.children, section2_checks)


class TestPseudoClasses:
    """
    Tests for pseudoclasses, both those with and those without arguments.
    """

    def test_first_child(self):
        """
        Check first child pseudoclass (:first-child)
        """
        doc = DocumentParser()
        toplevel = (
            MockDataParser(doc, "\n"),
            MockTagParser('h1', doc, (('id', 'bigheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('section', doc, (('id', 'section1'),('class', 'docsec'))),
        )
        for e in toplevel:
            doc.append(e)
        section1 = toplevel[3]
        section1.children.extend((
            MockDataParser(doc, "\n"),
            MockTagParser('h2', section1, (('class', 'sectionheader'),)),
            MockTagParser('p', section1, ()),
            MockTagParser('div', section1, (('class', 'last'),)),
        ))
        section2 = section1.children[3]
        section2.children.extend((
            MockDataParser(doc, "\n"),
            MockTagParser('h2', section2, (('class', 'sectionheader'),)),
            MockTagParser('p', section2, (('id', 'special'),)),
            MockTagParser('div', section2, ()),
        ))

        toplevel_checks = (
            ('h1:first-child',                (False, True, False, False)),
            ('section:first-child',           (False, False, False, False)),
            (':first-child',                  (False, True, False, False)),
            ('#bigheader:first-child',        (False, True, False, False)),
            ('.docsec:first-child',           (False, False, False, False)),
        )
        _perform_checks(toplevel, toplevel_checks)

        section1_checks = (
            (':first-child',                 (False, True, False, False)),
            ('h2:first-child',               (False, True, False, False)),
            ('p:first-child',                (False, False, False, False)),
            ('.last:first-child',            (False, False, False, False)),
        )
        _perform_checks(section1.children, section1_checks)

        section2_checks = (
            ('.last > .sectionheader:first-child',  (False, True, False, False)),
            ('.last > #special:first-child',        (False, False, False, False)),
            ('div > h2:first-child',                (False, True, False, False)),
        )
        _perform_checks(section2.children, section2_checks)


    def test_last_child(self):
        """
        Check last child pseudoclass (:last-child)
        """
        doc = DocumentParser()
        toplevel = (
            MockTagParser('h1', doc, (('id', 'bigheader'),)),
            MockTagParser('section', doc, (('id', 'section1'),('class', 'docsec'))),
            MockDataParser(doc, "\n"),
        )
        for e in toplevel:
            doc.append(e)
        section1 = toplevel[1]
        section1.children.extend((
            MockTagParser('h2', section1, (('class', 'sectionheader'),)),
            MockTagParser('p', section1, ()),
            MockTagParser('div', section1, (('class', 'last'),)),
            MockDataParser(doc, "\n"),
        ))
        section2 = section1.children[2]
        section2.children.extend((
            MockTagParser('h2', section2, (('class', 'sectionheader'),)),
            MockTagParser('p', section2, (('id', 'special'),)),
            MockTagParser('div', section2, ()),
            MockDataParser(doc, "\n"),
        ))

        toplevel_checks = (
            ('h1:last-child',                (False, False, False)),
            ('section:last-child',           (False, True, False)),
            (':last-child',                  (False, True, False)),
            ('.docsec:last-child',           (False, True, False)),
            ('#bigheader:last-child',        (False, False, False)),
        )
        _perform_checks(toplevel, toplevel_checks)

        section1_checks = (
            (':last-child',                 (False, False, True, False)),
            ('h2:last-child',               (False, False, False, False)),
            ('p:last-child',                (False, False, False, False)),
            ('div:last-child',              (False, False, True, False)),
            ('.last:last-child',            (False, False, True, False)),
        )
        _perform_checks(section1.children, section1_checks)

        section2_checks = (
            ('.last > .sectionheader:last-child',  (False, False, False, False)),
            ('.last > #special:last-child',        (False, False, False, False)),
            ('.last > div:last-child',             (False, False, True, False)),
        )
        _perform_checks(section2.children, section2_checks)


    def test_nth_child(self):
        """
        Check nth child pseudoclass (:nth-child())
        """
        doc = DocumentParser()
        toplevel = (
            MockTagParser('h1', doc, (('id', 'bigheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('section', doc, (('id', 'section1'),('class', 'docsec'))),
        )
        for e in toplevel:
            doc.append(e)
        section1 = toplevel[2]
        section1.children.extend((
            MockTagParser('h2', section1, (('class', 'sectionheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('p', section1, ()),
            MockTagParser('div', section1, (('class', 'last'),)),
        ))
        section2 = section1.children[3]
        section2.children.extend((
            MockTagParser('h2', section2, (('class', 'sectionheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('p', section2, (('id', 'special'),)),
            MockTagParser('div', section2, ()),
        ))

        toplevel_checks = (
            ('h1:nth-child(1)',              (True, False, False)),
            ('section:nth-child(1)',         (False, False, False)),
            ('section:nth-child(2)',         (False, False, True)),
            (':nth-child(2)',                (False, False, True)),
            ('.docsec:nth-child(2)',         (False, False, True)),
            ('#bigheader:nth-child(2)',      (False, False, False)),
        )
        _perform_checks(toplevel, toplevel_checks)

        section1_checks = (
            (':nth-child(3)',                 (False, False, False, True)),
            (':nth-child(2)',                 (False, False, True, False)),
            (':nth-child(2), :nth-child(3)',  (False, False, True, True)),
            ('h2:nth-child(1)',               (True, False, False, False)),
            ('p:nth-child(1)',                (False, False, False, False)),
            ('div:nth-child(3)',              (False, False, False, True)),
            ('.last:nth-child(3)',            (False, False, False, True)),
        )
        _perform_checks(section1.children, section1_checks)

        section2_checks = (
            ('.last > .sectionheader:nth-child(2)',  (False, False, False, False)),
            ('.last > #special:nth-child(2)',        (False, False, True, False)),
            ('.last > div:nth-child(3)',             (False, False, False, True)),
        )
        _perform_checks(section2.children, section2_checks)


    def test_nth_last_child(self):
        """
        Check nth last child pseudoclass (:nth-last-child())
        """
        doc = DocumentParser()
        toplevel = (
            MockTagParser('h1', doc, (('id', 'bigheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('section', doc, (('id', 'section1'),('class', 'docsec'))),
        )
        for e in toplevel:
            doc.append(e)
        section1 = toplevel[2]
        section1.children.extend((
            MockTagParser('h2', section1, (('class', 'sectionheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('p', section1, ()),
            MockTagParser('div', section1, (('class', 'last'),)),
        ))
        section2 = section1.children[3]
        section2.children.extend((
            MockTagParser('h2', section2, (('class', 'sectionheader'),)),
            MockDataParser(doc, "\n"),
            MockTagParser('p', section2, (('id', 'special'),)),
            MockTagParser('div', section2, ()),
        ))

        toplevel_checks = (
            ('h1:nth-last-child(2)',              (True, False, False)),
            ('section:nth-last-child(2)',         (False, False, False)),
            ('section:nth-last-child(1)',         (False, False, True)),
            (':nth-last-child(2)',                (True, False, False)),
            ('.docsec:nth-last-child(1)',         (False, False, True)),
            ('#bigheader:nth-last-child(2)',      (True, False, False)),
        )
        _perform_checks(toplevel, toplevel_checks)

        section1_checks = (
            (':nth-last-child(3)',                      (True, False, False, False)),
            (':nth-last-child(2)',                      (False, False, True, False)),
            (':nth-last-child(2), :nth-last-child(3)',  (True, False, True, False)),
            ('h2:nth-last-child(1)',                    (False, False, False, False)),
            ('p:nth-last-child(1)',                     (False, False, False, False)),
            ('div:nth-last-child(1)',                   (False, False, False, True)),
            ('.last:nth-last-child(3)',                 (False, False, False, False)),
        )
        _perform_checks(section1.children, section1_checks)

        section2_checks = (
            ('.last > .sectionheader:nth-last-child(3)',  (True, False, False, False)),
            ('.last > #special:nth-last-child(2)',        (False, False, True, False)),
            ('.last > div:nth-last-child(1)',             (False, False, False, True)),
        )
        _perform_checks(section2.children, section2_checks)
