if __name__ == "__main__":
    """Allow running just this test.

    Usage: python tests/some_folder/somefile.py
    """

    import os

    os.system(f"python3 -m pytest -vvsx {__file__}")
    exit(1)  # prevents code from trying to run file afterwards.

import pytest

from undyingkingdoms.models import County


def test_completed_techs(app):
    with app.app_context():
        county = County.query.get(1)
        assert county.completed_techs == []
