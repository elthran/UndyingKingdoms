from random import choice

from undyingkingdoms.models.exports import County


def test_forts_add_defence(ctx):
    county = County.query.get(1)
    forts = county.buildings['fort']

    forts.total = 0
    low_defense = county.get_defensive_strength()

    forts.total = 10
    medium_defense = county.get_defensive_strength()

    forts.total = 20
    high_defense = county.get_defensive_strength()

    assert low_defense < medium_defense
    assert medium_defense < high_defense

