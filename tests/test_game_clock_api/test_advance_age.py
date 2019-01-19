if __name__ == "__main__":
    """Allow running just this test.

    Usage: python tests/some_folder/somefile.py
    """

    import os

    os.system("python3 -m pytest -vvs {}".format(__file__))
    exit(1)  # prevents code from trying to run file afterwards.

import json

from tests.helpers import login
from undyingkingdoms.models import World, County


def test_advance_age(client):
    with client:
        rv_login = login(client, 'haldon@gmail.com', 'brunner')
        assert "Public Info" in rv_login.data.decode()
        assert rv_login.status_code == 200

        rv_token = client.get('/game_clock/token')
        data_token = json.loads(rv_token.data.decode())
        assert data_token['status'] == 'success'
        assert data_token['auth_token']
        assert rv_token.status_code == 200

        # I might need to logout here just to be safe?

        world = World.query.first()
        age, day = world.age, world.day
        rv = client.get(
            '/game_clock/advance_age',
            headers=dict(
                Authorization='Bearer ' + data_token['auth_token']
            )
        )

        data = json.loads(rv.data.decode())
        assert data['status'] == 'success'
        assert data['message']
        world2 = World.query.first()
        assert County.query.all() == []
        assert world2.age == age + 1
        assert world2.day == 0
