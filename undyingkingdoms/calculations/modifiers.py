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
        if county.technologies.get('sharpened sticks') and county.technologies['sharpened sticks'].completed:
            if filter_key == 'peasant':
                mod_sum += 1

    return mod_sum
