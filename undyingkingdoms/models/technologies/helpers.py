from copy import deepcopy

from sqlalchemy.ext.hybrid import hybrid_property

from tests import bp
from utilities.helpers import romanize, strip_leading_underscore


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


# def hoist_cols_macro(cls, sub_cls, sub_table_alias=None):
#     sub_table_alias = sub_table_alias or sub_cls.__table__.name
#
#     cols_to_hoist = set([
#         strip_leading_underscore(c.name)
#         for c in sub_cls.__table__.c
#     ]) - set([
#         strip_leading_underscore(c.name)
#         for c in cls.__table__.c
#     ])
#
#     for name in cols_to_hoist:
#         func = hybrid_property(
#             lambda self, key=name: getattr(
#                 getattr(self, sub_table_alias),
#                 key
#             )
#         )
#         setattr(
#             cls,
#             name,
#             func
#         )
#         setattr(
#             cls,
#             name,
#             func.setter(
#                 lambda self, value, key=name: setattr(
#                     getattr(self, sub_table_alias),
#                     key,
#                     value
#                 )
#             )
#         )
