from copy import deepcopy

from utilities.helpers import romanize


def generate_tech_levels(techs, requirements):
    """Generate each level up tech up to max level.

    You should now be able to create
    Technology(
       ...
       tier=2
       max_level=2
    )
    and have no extra tech generated.
    """
    all_techs = []
    all_reqs = requirements
    for tech in techs:
        all_techs.append(tech)
        for level in range(tech.tier, tech.max_level):
            next_level_tech = deepcopy(tech)
            next_level_tech.tier = tech.tier + level
            next_level_tech.name = romanize(tech.name, next_level_tech.tier)
            # try:
            #     next_level_tech.output = tech.output * (level + 1)
            # except TypeError:
            #     pass
            all_techs.append(next_level_tech)

            # merge custom and generated requirements
            try:
                all_reqs[next_level_tech.key] = set(requirements[next_level_tech.key]) | {all_techs[-2].key}
            except KeyError:
                all_reqs[next_level_tech.key] = {all_techs[-2].key}

    return {
        tech.key: tech
        for tech in all_techs
    }, all_reqs
