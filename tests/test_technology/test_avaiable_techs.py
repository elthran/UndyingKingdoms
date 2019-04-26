if __name__ == "__main__":
    """Allow running just this test.

    Usage: python tests/some_folder/somefile.py
    """

    import os

    os.system(f"python3 -m pytest -vvsx {__file__}")
    exit(1)  # prevents code from trying to run file afterwards.

from tests import bp

from tests.fakes import UserFactory
from undyingkingdoms.controler.initialize import initialize_county, pick_kingdom


def initialize_account():
    user = UserFactory()
    user.save()
    kingdom = pick_kingdom(user, False)
    county = initialize_county(user, kingdom, 'county', 'leader', 'Merchant', 'Dwarf', 'Baron')
    return county


def test_completed_techs(app):
    with app.app_context():
        county = initialize_account()
        assert county.completed_techs == []

        tech1 = county.technologies['agriculture']
        tech1.completed = True

        assert county.completed_techs == [tech1]
