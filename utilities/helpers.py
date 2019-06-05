import operator
import re

import roman

from tests import bp


def to_class_name(name):
    """Convert spaced or underscored word to title case word.

    e.g.
        foo bar -> FooBar
        foo_bar -> FooBar
        foo bar_bag -> FooBarBag
    """
    return ''.join(name.title().replace(" ", "_").split('_'))


def to_var_name(name):
    """Convert a upper case class name to a variable name.
    e.g.
        FooBar -> foo_bar
        FooBAR -> foo_b_a_r
    TODO: make FooBAR => foo_bar ...
    """

    words = re.sub(r"([A-Z])", r" \1", name).split()

    return '_'.join(words).lower()


def romanize(word, n):
    """Attach a Roman numeral to the given word.

    Do nothing if n is 0.
    """
    numeral = roman.toRoman(n)
    return f'{word} {numeral}' if n > 1 else word


def strip_leading_underscore(s):
    return s[1:] if s[0] == '_' else s


def combine_dicts(a, b, op=operator.add):
    return dict(
        tuple(a.items()) + tuple(b.items()) +
        tuple((k, op(a[k], b[k])) for k in set(b) & set(a))
    )
