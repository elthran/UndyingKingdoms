if __name__ == "__main__":
    """Allow running just this test.

    Usage: python tests/some_folder/somefile.py
    v -> verbose
    s -> show prints
    """

    import os
    os.system("python3 -m pytest -vvs {}".format(__file__))
    exit(1)  # prevents code from trying to run file afterwards.

from undyingkingdoms import User
from undyingkingdoms.models import Diplomacy, Kingdom

def test_pending_alliances(app):
    with app.app_context():
        haldon = User.query.filter_by(username="haldon").one()

        county = haldon.county
        faenoth = haldon.county.kingdom
        ally = Kingdom.query.get(2)
        alliance = Diplomacy(faenoth.id, ally.id, ally.world.day, action="Alliance")
        alliance.save()

        assert len(faenoth._pending_alliances_you_started) == 1
        assert len(faenoth._pending_alliances_started_with_you) == 0
        assert len(faenoth.pending_alliances) == 1
        assert len(faenoth.kingdoms_who_we_offered_alliances_to) == 1
        assert len(faenoth.kingdoms_who_offered_us_alliances) == 0
