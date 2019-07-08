import re

import roman


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


def to_mixed_case(name):
    """Convert a lower_case_with_underscores to mixedCase naming.

    foo_barCAPS == fooBarCAPS
    Assumes any grouping of capitals is an acronym and should
    be left as is.
    """
    first_char = (
        name[0].lower()
        if len(name) > 1 and not name[1].isupper()
        else name[0]
    )
    mixed_case = (
        first_char +
        ''.join([
            '' if char == '_' else
            (char.upper() if name[i] == '_' else char)
            for i, char in enumerate(name[1:])
        ])
    )
    return mixed_case


def romanize(word, n):
    """Attach a Roman numeral to the given word.

    Do nothing if n is 0.
    """
    numeral = roman.toRoman(n)
    return f'{word} {numeral}' if n > 1 else word


def strip_leading_underscore(s):
    return s[1:] if s[0] == '_' else s
