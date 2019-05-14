from copy import deepcopy

from tests import bp
from undyingkingdoms.metadata.research.metadata_research_alchemist import alchemist_technology
from undyingkingdoms.models.exports import County


def test_technology_effects(app):
    with app.app_context():
        county = County.query.filter_by(leader="Haldon").one()
        output = county.grain_produced

        county.technologies['basic agriculture'].completed = True

        assert output < county.grain_produced

        county.technologies['basic agriculture'].completed = False

        assert county.grain_produced == output


def test_health_tech(app):
    with app.app_context():

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


def test_fort_multiplier(app):
    with app.app_context():
        county = County.query.filter_by(leader="Haldon").one()
        infrastructure = county.infrastructure

        fort_output = county.buildings['fort'].output
        infrastructure.fort_multiplier = 2

        assert county.buildings['fort'].output == fort_output * 2

        infrastructure.fort_multiplier = 1.6

        assert county.buildings['fort'].output == fort_output * 1.6

        infrastructure.fort_multiplier = 0.2

        assert county.buildings['fort'].output == fort_output * 0.2
