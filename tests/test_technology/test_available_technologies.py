from tests.fakes.factories import UserFactory, CountyFactory
from undyingkingdoms.models.counties.specifics import merge_tech_requirements
from undyingkingdoms.models.exports import Preferences, Technology


def initialize_account():
    user = UserFactory()
    county = CountyFactory(user=user)
    Preferences(county, user)
    return county


def test_completed_technologies(ctx):
    # app.config['SQLALCHEMY_ECHO'] = True
    county = initialize_account()
    county.save()

    assert list(county.completed_technologies) == []
    assert set(county.technologies.values()) == set(county.incomplete_technologies)

    tech = county.technologies['basic agriculture']
    tech.completed = True

    assert list(county.completed_technologies) == [tech]
    assert len(list(county.incomplete_technologies)) == len(county.technologies) - 1


def test_available_technologies(ctx):
    county = initialize_account()
    all_requirements = merge_tech_requirements(county.race, county.background)
    Technology.establish_requirements(county.technologies, all_requirements)
    county.save()

    assert list(county.technologies) != []
    assert list(county.available_technologies) != []
    assert set(county.technologies.values()) != set(county.available_technologies)
