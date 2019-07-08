import operator


def combine_dicts(a, b, op=operator.add):
    return dict(
        tuple(a.items()) + tuple(b.items()) +
        tuple((k, op(a[k], b[k])) for k in set(b) & set(a))
    )
