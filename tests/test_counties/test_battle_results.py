if __name__ == "__main__":
    """Allow running just this test.
    
    Usage: python tests/some_folder/somefile.py
    """

    import os
    os.system("python3 -m pytest -vv {}".format(__file__))
    exit(1)  # prevents code from trying to run file afterwards.

from undyingkingdoms.models.counties import County
from undyingkingdoms.models.users import User


def test_battle_results(app, client):
    with app.app_context():
        user1 = User('user1', 'user1@gmail.com', 'password')
        user1.save()
        county1 = County("County1", "Leader1", user1.id, "Human", "Male")
        county1.save()
        army1 = dict(
            peasant=50,
            soldier=100,
            archer=0,
            elite=10
        )

        user2 = User('user2', 'user2@gmail.com', 'password')
        user2.save()
        county2 = County("County2", "Leader2", user2.id, "Human", "Male")
        county2.save()
        # create user 1
        # create user 2
        # simulate attack.
        assert 'You claimed a massive victory and gained 15 acres, but lost' in county1.battle_results(army1, county2)
