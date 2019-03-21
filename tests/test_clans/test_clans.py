import pytest

if __name__ == "__main__":
    """Allow running just this test.

    Usage: python tests/some_folder/somefile.py
    """

    import os

    os.system("python3 -m pytest -vvs {}".format(__file__))
    exit(1)  # prevents code from trying to run file afterwards.


from undyingkingdoms.models.users import User
from undyingkingdoms.models.clans import Clan
from undyingkingdoms.models.kingdoms import Kingdom

def test_pending_alliances(app):
    with app.app_context():
        user = User.query.get(1)
        clan = Clan(1, user.id, True)
        clan.save()
        assert user.clan == clan
        assert list(clan.users) == [user]

        kingdom = Kingdom.query.get(1)
        assert user.clan.kingdom == kingdom
        assert user.clan.is_owner == True
        assert user.clan.owner == user

        user2 = User.query.get(2)
        clan2 = Clan(1, user2.id)
        clan2.save()
        assert user.clan == clan
        assert user2.clan == clan2
        assert user.clan != user2.clan
        assert user2.clan.owner == user
        assert user2.clan.is_owner == False
        assert user2.clan.kingdom == kingdom
        assert user2 in clan.users
        assert user in clan2.users
        assert list(clan2.users) == list(clan.users)

        # test ownership
        with pytest.raises(AttributeError):
            user.clan.is_owner = True
