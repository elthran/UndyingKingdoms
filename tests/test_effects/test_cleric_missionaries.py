from copy import deepcopy

from undyingkingdoms.metadata.research.metadata_research_cleric import cleric_technology
from undyingkingdoms.models.exports import County


def test_cleric_missionaries(ctx):
    county = County.query.filter_by(leader="Haldon").one()
    economy = county.economy
    county.technologies.update(deepcopy(cleric_technology))

    initial_rate = county.immigration_rate
    county.technologies['missionaries'].completed = True

    assert county.immigration_rate == initial_rate * (1 + economy.immigration_modifier)
