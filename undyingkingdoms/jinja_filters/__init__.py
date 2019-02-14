from markupsafe import Markup

def vue_safe(value):
    """Convert all tuples to lists.

    This also marks the value as safe to prevent escaping.
    I may need to make this more complex over time.
    """

    new = []
    for item in value:
        if isinstance(item, tuple):
            new.append(list(item))
        else:
            new.append(item)

    return Markup(new)