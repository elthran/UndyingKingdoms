from undyingkingdoms import User
from undyingkingdoms.controler.initialize import initialize_county, pick_kingdom

if __name__ == "__main__":
    """Allow running just this test.

    Usage: python tests/some_folder/somefile.py
    """

    import os

    os.system(f"python3 -m pytest -vvsx {__file__}")
    exit(1)  # prevents code from trying to run file afterwards.

import pytest

from undyingkingdoms.models import County


def initialize_account():
    user = User('username', 'email@gmail.com', 'password')
    user.save()
    kingdom = pick_kingdom(user, False)
    county = initialize_county(user, kingdom, 'county', 'leader', 'Merchant', 'Dwarf', 'Baron')


def test_completed_techs(app):
    with app.app_context():
        county = County.query.get(1)
        assert county.completed_techs == []

        tech1 = county.technologies[0]
        tech1.completed = True

        assert county.completed_techs == [tech1]
