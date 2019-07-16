from copy import deepcopy

from lib.namers import romanize


def generate_tech_levels(technologies, requirements):
    """Generate each level of tech up to max level.

    You should now be able to create
    Technology(
       ...
       tier=2
       max_level=2
    )
    and have no extra tech generated.
    """
    all_technologies = []
    all_reqs = requirements
    for tech in technologies:
        all_technologies.append(tech)
        for level in range(tech.tier, tech.max_level):
            next_level_tech = deepcopy(tech)
            next_level_tech.tier = tech.tier + level
            next_level_tech.name = romanize(tech.name, next_level_tech.tier)
            # try:
            #     next_level_tech.output = tech.output * (level + 1)
            # except TypeError:
            #     pass
            all_technologies.append(next_level_tech)

            # merge custom and generated requirements
            try:
                all_reqs[next_level_tech.key] = set(requirements[next_level_tech.key]) | {all_technologies[-2].key}
            except KeyError:
                all_reqs[next_level_tech.key] = {all_technologies[-2].key}

    return {
        tech.key: tech
        for tech in all_technologies
    }, all_reqs
