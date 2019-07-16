from copy import deepcopy

from app.metadata.research.metadata_research_warlord import warlord_technology
from app.models.counties.counties import County


def test_call_to_arms(ctx):
    county = County.query.get(1)

    county.technologies.update(deepcopy(warlord_technology))

    train_count = county.armies['peasant'].trainable_per_day
    county.technologies['call to arms'].completed = True

    assert county.armies['peasant'].trainable_per_day > train_count

    county.technologies['call to arms'].completed = False
    assert county.armies['peasant'].trainable_per_day == train_count
