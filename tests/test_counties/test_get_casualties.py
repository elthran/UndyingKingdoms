if __name__ == "__main__":
    """Allow running just this test.
    
    Usage: python tests/some_folder/somefile.py
    """

    import os
    os.system("python3 -m pytest -vv {}".format(__file__))
    exit(1)  # prevents code from trying to run file afterwards.

from undyingkingdoms.models.counties import County


def test_get_casualties(app):
    with app.app_context():
        county = County.query.first()
        assert 17 < county.get_casualties(500) < 61


def test_negative_casualties(app):
    with app.app_context():
        county = County.query.first()
        assert 34 < county.get_casualties(500000) < 500000

        for unit in county.armies.values():
            assert unit.total >= 0

        assert county.population >= 0
