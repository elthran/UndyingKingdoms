from random import choice

from undyingkingdoms.models.exports import County


def test_forts_add_defence(ctx):
    county = County.query.get(1)
    forts = county.buildings['fort']
    forts.total = 0

    starting_defense = county.get_defensive_strength()

    forts.total = 10

    assert starting_defense < county.get_defensive_strength()

    forts.total = 0

    assert starting_defense == county.get_defensive_strength()
