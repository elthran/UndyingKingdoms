import math


def bell_curvish(size):
    """Produce a bell curve-ish distribution of groups.

    [[round(y / sum(bell_curvish(x)) * 100)
      for y in bell_curvish(x)]
      for x in range(1, 16)] ->
    [[100],
     [50, 50],
     [29, 42, 29],
     [19, 31, 31, 19],
     [13, 23, 27, 23, 13],
     [9, 18, 22, 22, 18, 9],
     [7, 14, 19, 20, 19, 14, 7],
     [5, 11, 16, 18, 18, 16, 11, 5],
     [4, 9, 13, 15, 16, 15, 13, 9, 4],
     [3, 8, 11, 13, 14, 14, 13, 11, 8, 3],
     [3, 7, 10, 12, 13, 13, 13, 12, 10, 7, 3],
     [2, 6, 8, 10, 12, 12, 12, 12, 10, 8, 6, 2],
     [2, 5, 7, 9, 10, 11, 11, 11, 10, 9, 7, 5, 2],
     [2, 4, 6, 8, 9, 10, 11, 11, 10, 9, 8, 6, 4, 2],
     [1, 4, 6, 7, 8, 9, 10, 10, 10, 9, 8, 7, 6, 4, 1]]

     Note: doesn't work above 21 steps.
    """
    std = size / 3 + 0.3
    mean = sum([x for x in range(size)]) / size
    curve = [
        (1 - (x - mean) ** 2 / (2 * std ** 2))
        / (std * math.sqrt(2 * math.pi)) * math.e
        for x in range(size)
    ]

    return curve


def normalize(values, bounds):
    """Normalize some data between given bounds."""
    return [
        bounds['desired']['lower'] + (x - bounds['actual']['lower'])
        * (bounds['desired']['upper'] - bounds['desired']['lower'])
        / (bounds['actual']['upper'] - bounds['actual']['lower'])
        for x in values
    ]


def curve_bounds(curve, data, lower=4):
    """Return the bounds of a curve given data"""
    bounds = dict(
        desired=dict(
            lower=lower,
            upper=len(data),
        ),
        actual=dict(
            lower=curve[0],
            upper=curve[len(curve) // 2],
        )
    )
    return bounds


def get_int_between_0_and_100(n):
    return int(max(min(100, n), 0))


def get_int_between_n_and_m(p, n=1, m=100):
    return int(max(min(m, p), n))
