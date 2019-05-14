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
