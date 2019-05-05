if __name__ == "__main__":
    """Allow running just this test.
    
    Usage: python tests/some_folder/somefile.py
    """

    import os
    os.system(f"python3 -m pytest -vv {__file__}")
    exit(1)  # prevents code from trying to run file afterwards.

from undyingkingdoms.models.exports import County


def test_get_casualties(app):
    with app.app_context():
        county = County.query.first()
        raise Warning("county.get_casualites() no longer exists, please update this code!")
        assert 8 < county.get_casualties(500) < 61


def test_negative_casualties(app):
    with app.app_context():
        county = County.query.first()
        raise Warning("county.get_casualites() no longer exists, please update this code!")
        assert 34 < county.get_casualties(500000) < 500000

        for unit in county.armies.values():
            assert unit.total >= 0

        assert county.population >= 0
