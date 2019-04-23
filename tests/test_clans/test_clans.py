import pytest

if __name__ == "__main__":
    """Allow running just this test.

    Usage: python tests/some_folder/somefile.py
    """

    import os

    os.system(f"python3 -m pytest -vvsx {__file__}")
    exit(1)  # prevents code from trying to run file afterwards.


from undyingkingdoms.models.users import User
from undyingkingdoms.models.clans import Clan
from undyingkingdoms.models.kingdoms import Kingdom

def test_clan_creation(app):
    with app.app_context():
        user = User.query.get(1)
        clan = Clan(1, user.id, is_owner=True)
        clan.save()
        assert user.clan == clan is not None
        assert clan.members == [user]

        kingdom = Kingdom.query.get(1)
        assert clan.kingdom == kingdom
        assert clan.is_owner == True
        assert clan.owner == user is not None


def test_clan_invites(app):
    with app.app_context():
        user = User.query.get(1)
        clan = Clan(1, user.id, is_owner=True)
        clan.save()
        # invited
        user2 = User.query.get(2)
        clan2 = Clan(1, user2.id)
        clan2.save()
        assert user.clan == clan is not None
        assert user2.clan is None
        assert user.clan.invited == [user2]


def test_clan_membership(app):
    with app.app_context():
        user = User.query.get(1)
        user2 = User.query.get(2)
        clan = Clan(1, user.id, is_owner=True)
        clan2 = Clan(1, user2.id, status="Member")
        clan.save()
        clan2.save()
        kingdom = Kingdom.query.get(1)
        # member
        assert user2.clan == clan2
        assert user.clan != user2.clan
        assert user2.clan.owner == user
        assert user2.clan.is_owner == False
        assert user2.clan.kingdom == kingdom
        assert user2 in clan.members
        assert user in clan2.members
        assert clan2.members == clan.members

def test_clan_validators(app):
    with app.app_context():
        user = User.query.get(1)
        user2 = User.query.get(2)
        clan = Clan(1, user.id, is_owner=True)
        clan2 = Clan(1, user2.id, status="Member")
        clan.save()
        clan2.save()
        # test ownership validator
        with pytest.raises(AttributeError, match='This clan already as an owner*') as ex:
            print(ex)
            clan2.is_owner = True

        # test status validator
        with pytest.raises(AttributeError, match='Status must be one of*'):
            clan.status = "Leader"
