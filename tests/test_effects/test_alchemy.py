from undyingkingdoms.models.counties.counties import County


def test_alchemy_technology_effects(ctx):
    county = County.query.filter_by(leader="Elthran").one()

    assert county.research_change == 0

    county.technologies['basic alchemy'].completed = True

    assert county.research_change == 10

    county.technologies['basic alchemy ii'].completed = True

    assert county.research_change == 20

    county.technologies['basic alchemy ii'].completed = False
    county.technologies['basic alchemy'].completed = False

    assert county.research_change == 0
