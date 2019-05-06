from undyingkingdoms.models.technologies import Technology

# from undyingkingdoms.metadata.metadata import birth_rate_modifier, food_consumed_modifier, death_rate_modifier, \
#     income_modifier, production_per_worker_modifier, offensive_power_modifier, defense_per_citizen_modifier, \
#     happiness_modifier, buildings_built_per_day_modifier
#
# all_mods = dict(
#     birth=birth_rate_modifier,
#     food=food_consumed_modifier,
#     death=death_rate_modifier,
#     income=income_modifier,
#     production=production_per_worker_modifier,
#     offensive=offensive_power_modifier,
#     defense=defense_per_citizen_modifier,
#     happiness=happiness_modifier,
#     buildings=buildings_built_per_day_modifier
# )

all_mods = dict(
    defence=[]
)


def get_modifiers(county, mod_type, filter_key):
    """Get any and all modifiers of a particular type.

    This should include racial, background and tech modifiers.
    Note: This is kind of slow and should probably be cached somehow.

    Example usage:
    def get_happiness(self)
        return 7 + get_modifiers(county, 'happiness')

    Should return any relevant modifiers to happiness give this county object.

    Should look like this:
    return sum([mod.value for mod in county.modifiers[mod_type].values()])

    or use some kind of dictionary or database filter query ...
    """

    mod_sum = 0

    # This is absolutely the wrong way to do it. :P
    # But I'm too lazy to build a table of all modifiers right now.
    # If you built one in would need to be queryable on at least
    # 2 (possibly 3 or 3) properties.
    # e.g. Modifiers.query.filter_by(race, background, type, type2).all()
    # Then you could run a simple for loop and sum all the values.
    # We should have a master modifier table listing all modifiers.

    if mod_type == 'unit_attack':
        if county.technologies.get('tactician') and county.technologies['tactician'].completed:
            mod_sum += 1
        if county.technologies.get('sacrifice') and county.technologies['sacrifice'].completed:
            mod_sum += 2
        if county.technologies.get('cross-breeding') and county.technologies['cross-breeding'].completed:
            if filter_key == 'elite':
                mod_sum += 3
        if county.technologies.get('dragon-fire') and county.technologies['dragon-fire'].completed:
            if filter_key == 'elite':
                mod_sum += 3
        if county.technologies.get('knights templar') and county.technologies['knights templar'].completed:
            if filter_key == 'elite':
                mod_sum += 3
        if county.technologies.get('deathwish') and county.technologies['deathwish'].completed:
            if filter_key == 'soldier':
                mod_sum += 1
        if county.technologies.get('ranger training') and county.technologies['ranger training'].completed:
            if filter_key == 'soldier':
                mod_sum += 2
        if county.technologies.get('sharpened sticks') and county.technologies['sharpened sticks'].completed:
            if filter_key == 'peasant':
                mod_sum += 1

    if mod_type == 'unit_defence':
        if county.technologies.get('dwarven muskets') and county.technologies['dwarven muskets'].completed:
            if filter_key == 'archer':
                mod_sum += 1
        if county.technologies.get('barbed arrows') and county.technologies['barbed arrows'].completed:
            if filter_key == 'archer':
                mod_sum += 1
        if county.technologies.get('throwing axes') and county.technologies['throwing axes'].completed:
            if filter_key == 'soldier':
                mod_sum += 2

    if mod_type == 'unit_health':
        if county.technologies.get('mithril armour') and county.technologies['mithril armour'].completed:
            if filter_key != 'monster' and filter_key != 'besieger':
                mod_sum += 1
        if county.technologies.get('sacrifice') and county.technologies['sacrifice'].completed:
            mod_sum -= 1
        if county.technologies.get('blessings') and county.technologies['blessings'].completed:
            mod_sum += 1

    if mod_type == 'unit_upkeep':
        if county.technologies.get('civic duty') and county.technologies['civic duty'].completed:
            if filter_key == 'peasant':
                mod_sum -= 10

    if mod_type == 'unit_gold':
        if county.technologies.get('slavery') and county.technologies['slavery'].completed:
            if filter_key == 'peasant':
                mod_sum -= 5
        if county.technologies.get('trading') and county.technologies['trading'].completed:
            if filter_key == 'peasant' or filter_key == 'soldier' or filter_key == 'archer' \
                    or filter_key == 'elite' or filter_key == 'monster':
                mod_sum -= 5

    if mod_type == 'unit_wood':
        if county.technologies.get('slavery') and county.technologies['slavery'].completed:
            if filter_key == 'peasant':
                mod_sum -= -1

    if mod_type == 'unit_iron':
        if county.technologies.get('slavery') and county.technologies['slavery'].completed:
            if filter_key == 'peasant':
                mod_sum = -1

    return mod_sum
