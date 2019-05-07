import roman


def to_class_name(name):
    """Convert spaced or underscored word to title case word.

    e.g.
        foo bar -> FooBar
        foo_bar -> FooBar
        foo bar_bag -> FooBarBag
    """
    return ''.join(name.title().replace(" ", "_").split('_'))


def romanize(word, n):
    """Attach a Roman numeral to the given word.

    Do nothing if n is 0.
    """
    numeral = roman.toRoman(n)
    return f'{word} {numeral}' if n > 1 else word


def strip_leading_underscore(s):
    return s[1:] if s[0] == '_' else s
