import cssselect
from cssselect.parser import (
    Selector,
    Element,
    Class,
    FunctionalPseudoElement,
    Function,
    Pseudo,
    Negation,
    Attrib,
    Hash,
    CombinedSelector,
)


def _element_matches(tag, element):
    return tag.tag == element.element or element.element == "*"


def _hash_matches(tag, hash):
    if tag.id is None:
        return False
    return tag.id == hash.id


def _class_matches(tag, klass):
    return klass.class_name in tag.classes


def _negation_matches(tag, selector):
    return (
        _selector_matches(tag, selector.selector) and
        not _selector_matches(tag, selector.subselector)
    )


def _any_ancestor_matches(tag, selector):
    if not hasattr(tag, 'parent') or tag.parent is None:
        return False
    if _selector_matches(tag.parent, selector):
        return True
    return _any_ancestor_matches(tag.parent, selector)


def _descendant_matches(tag, selector):
    # The tag must match the subselector, while some ancestor element must match
    # the main selector.
    primary_match = _selector_matches(tag, selector.subselector)
    if not primary_match:
        return False

    # Need to walk back up the tree checking the selector
    return _any_ancestor_matches(tag, selector.selector)


def _child_matches(tag, selector):
    # The tag cannot match as a child if it does not have a parent.
    if not hasattr(tag, 'parent') or tag.parent is None:
        return False
    primary_match = _selector_matches(tag, selector.subselector)
    if not primary_match:
        return False
    return _selector_matches(tag.parent, selector.selector)


def _general_sibling_matches(tag, selector):
    # The tag must match the subselector, while some sibling before this tag in
    # the parent must match the selector.
    if not hasattr(tag, 'parent') or tag.parent is None:
        return False

    primary_match = _selector_matches(tag, selector.subselector)
    if not primary_match:
        return False

    for sibling in tag.parent.children:
        if sibling == tag:
            return False
        if _selector_matches(sibling, selector.selector):
            return True
    return False


def _adjacent_sibling_matches(tag, selector):
    # The tag must match the subselector, while the sibling immediately before
    # this tag in the parent must match the selector.
    if not hasattr(tag, 'parent') or tag.parent is None:
        return False

    primary_match = _selector_matches(tag, selector.subselector)
    if not primary_match:
        return False

    tag_index = tag.parent.children.index(tag)
    # If the tag is the first within the parent then
    # it can't have a previous sibling.
    if tag_index == 0:
        return False
    sibling = tag.parent.children[tag_index]
    return _selector_matches(sibling, selector.selector)


def _column_matches(tag, selector):
    # I don't know how to check this one.
    return False


def _attribute_matches(tag, selector):
    # This selector allows a namespace to be specified as well, but that is
    # not handled here.
    # There are also options related to how to compare the values case-wise
    # but that is apparently not handled by cssselect.
    if selector.attrib in tag.attrs:
        if selector.operator == 'exists':
            return True
        attr_val = tag.attrs[selector.attrib]
        if selector.attrib == 'class':
            # The class attribute is split during parsing, so have to rejoin
            # it for ease of comparison
            attr_val = " ".join(attr_val)
        if selector.operator == '=':
            return attr_val == selector.value
        if selector.operator == '~=':
            split_val = attr_val.split()
            return selector.value in split_val
        if selector.operator == '|=':
            return attr_val == selector.value or attr_val.startswith("{}-".format(selector.value))
        if selector.operator == '^=':
            return attr_val.startswith(selector.value)
        if selector.operator == '$=':
            return attr_val.endswith(selector.value)
        if selector.operator == '*=':
            return selector.value in attr_val
    return False


def _combination_matches(tag, selector):
    if selector.combinator == ' ':
        return _descendant_matches(tag, selector)
    elif selector.combinator == '>':
        return _child_matches(tag, selector)
    elif selector.combinator == '~':
        return _general_sibling_matches(tag, selector)
    elif selector.combinator == '+':
        return _adjacent_sibling_matches(tag, selector)
    elif selector.combinator == '||':
        return _column_matches(tag, selector)


def _pseudoclass_matches(tag, selector):
    # This is a pseudo-class that does not take arguments
    # Candidates to support:
    #   :any-link
    #   :empty
    #   :first-child
    #   :first-of-type
    #   :last-child
    #   :last-of-type
    #   :only-child
    #   :only-of-type
    #   :root (equivalent of 'html' i.e. specify a renderer for the whole document)
    #   :target
    return False


def _pseudofunction_matches(tag, selector):
    # This is a pseudo-class that takes arguments
    # Candidates to support:
    #   :dir()
    #   :has()
    #   :is()
    #   :lang()
    #   :nth-child()
    #   :nth-col()
    #   :nth-last-child()
    #   :nth-last-col()
    #   :nth-last-of-type()
    #   :nth-of-type()
    #   :where()
    return False


def _pseudoelement_matches(tag, selector):
    # It is unclear if cssselect supports all peudo-elements or only ones that
    # take arguments, but we are not supporting any of them anyway.
    return False


def _selector_matches(tag, selector):
    if isinstance(selector, Element):
        return _element_matches(tag, selector)
    elif isinstance(selector, Class):
        return _class_matches(tag, selector)
    elif isinstance(selector, Hash):
        return _hash_matches(tag, selector)
    elif isinstance(selector, Negation):
        return _negation_matches(tag, selector)
    elif isinstance(selector, Attrib):
        return _attribute_matches(tag, selector)
    elif isinstance(selector, Pseudo):
        return _pseudoclass_matches(tag, selector)
    elif isinstance(selector, Function):
        return _pseudofunction_matches(tag, selector)
    elif isinstance(selector, FunctionalPseudoElement):
        return _pseudoelement_matches(tag, selector)

    # oh no
    return False


def tag_matches(tag, selector):
    """
    Determine if a given tag matches a given selector.

    Returns a boolean indicating a match or not, and a value indicating the
    specificity of the matched selector.
    """
    # The selector will actually be a list, though perhaps one with only one
    # element. If multiple elements match then we need to determine the most
    # specific one.
    matched = False
    best_specificity = None
    for s in selector:
        is_match = _selector_matches(tag, s.parsed_tree)
        if is_match:
            if more_specific(s.specificity(), best_specificity):
                matched = True
                best_specificity = s.specificity()

    return matched, best_specificity


def more_specific(specificity1, specificity2):
    """
    Returns True if the first argument is more specific than the second,
    otherwise False.

    Specificity is a concept defined for CSS selectors:
    https://www.w3.org/TR/selectors/#specificity

    For our purposes, each specificity will be a tuple with three elements.
    """
    if specificity1 is None:
        raise ArgumentError("specificity1 cannot be None")
    if specificity2 is None:
        return True
    if specificity1[0] == specificity2[0]:
        if specificity1[1] == specificity2[1]:
            # TODO: If these are equal, should the return be True or False?
            # If we return True, later entries in the map with equal specificity
            # will override earlier entries. But will the map order even be
            # meaningful?
            return specificity1[2] > specificity2[2]
        else:
            return specificity1[1] > specificity2[1]
    else:
        return specificity1[0] > specificity2[0]
