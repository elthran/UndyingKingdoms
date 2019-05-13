if __name__ == "__main__":
    """Allow running just this test.

    Usage: python tests/some_folder/somefile.py
    """

    import os

    os.system(f"python3 -m pytest -vvsx {__file__}")
    exit(1)  # prevents code from trying to run file afterwards.

from tests import bp, pp

from tests.fakes.factories import UserFactory, CountyFactory
from tests.fakes.providers import fake
from undyingkingdoms.models.exports import Preferences, Technology


def initialize_account():
    user = UserFactory()
    county = CountyFactory(user=user)
    Preferences(county, user)
    return county


def test_completed_techs(app):
    with app.app_context():
        # app.config['SQLALCHEMY_ECHO'] = True
        county = initialize_account()
        county.save()

        assert list(county.completed_techs) == []
        assert set(county.technologies.values()) == set(county.incomplete_techs)

        tech = county.technologies['basic agriculture']
        tech.completed = True

        assert list(county.completed_techs) == [tech]
        assert len(list(county.incomplete_techs)) == len(county.technologies) - 1


def test_available_techs(app):
    with app.app_context():
        county = initialize_account()
        level_1s = 4
        requirements = fake.requirements(county.technologies.keys(), level_1s=level_1s)
        # pp(requirements)
        Technology.establish_requirements(county.technologies, requirements)
        county.save()

        assert list(county.technologies) != []
        assert list(county.available_techs) != []
        assert set(county.technologies.values()) != set(county.available_techs)
