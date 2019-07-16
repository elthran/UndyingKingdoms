from copy import deepcopy

from app.metadata.research.metadata_research_alchemist import alchemist_technology
from app.models.counties.counties import County


def test_health_tech(ctx):
    # I would like to generate a fake county of alchemist
    # county = fakes.CountyFaker(background="alchemist")
    # or figure out how to add any tech to an account without breaking
    # everything.
    county = County.query.filter_by(leader="Haldon").one()

    county.technologies.update(deepcopy(alchemist_technology))

    non_besieger_health = county.armies['archer'].health
    besieger_health = county.armies['besieger'].health

    county.technologies['elixir of life'].completed = True

    assert non_besieger_health < county.armies['archer'].health
    assert besieger_health == county.armies['besieger'].health

    county.technologies['elixir of life'].completed = False

    assert non_besieger_health == county.armies['archer'].health
    assert besieger_health == county.armies['besieger'].health
