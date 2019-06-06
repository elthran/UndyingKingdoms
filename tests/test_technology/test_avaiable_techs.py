from tests.fakes.factories import UserFactory, CountyFactory
from undyingkingdoms.models.counties.specifics import merge_tech_requirements
from undyingkingdoms.models.exports import Preferences, Technology


def initialize_account():
    user = UserFactory()
    county = CountyFactory(user=user)
    Preferences(county, user)
    return county


def test_completed_techs(ctx):
    # app.config['SQLALCHEMY_ECHO'] = True
    county = initialize_account()
    county.save()

    assert list(county.completed_techs) == []
    assert set(county.technologies.values()) == set(county.incomplete_techs)

    tech = county.technologies['basic agriculture']
    tech.completed = True

    assert list(county.completed_techs) == [tech]
    assert len(list(county.incomplete_techs)) == len(county.technologies) - 1


def test_available_techs(ctx):
    county = initialize_account()
    all_requirements = merge_tech_requirements(county.race, county.background)
    Technology.establish_requirements(county.technologies, all_requirements)
    county.save()

    assert list(county.technologies) != []
    assert list(county.available_techs) != []
    assert set(county.technologies.values()) != set(county.available_techs)
