import functools


@functools.lru_cache(maxsize=80)
def check_for_filter(filters, s):
    for filter_ in filters:
        if s.startswith(filter_):
            return filter_, s[len(filter_)+1:]
    return False


def check_filter_match(filter, unit):
    valid_target = False
    if filter in 'unit':
        valid_target = True
    elif filter == 'non_siege':
        if unit.type != unit.BESIEGER:
            valid_target = True
    elif filter == 'non_monster_non_siege':
        if unit.type not in {unit.BESIEGER, unit.MONSTER}:
            valid_target = True
    elif unit.type == unit.TYPES[filter]:
        valid_target = True
    return valid_target
