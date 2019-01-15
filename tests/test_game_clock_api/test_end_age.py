import json

from tests.helpers import login
from undyingkingdoms.models import World


def test_end_age(client):
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
            '/game_clock/end_age',
            headers=dict(
                Authorization='Bearer ' + data_token['auth_token']
            )
        )

        data = json.loads(rv.data.decode())
        assert data['status'] == 'success'
        assert data['message']
        world2 = World.query.first()
        assert world2.age > age
        assert world2.day > day
