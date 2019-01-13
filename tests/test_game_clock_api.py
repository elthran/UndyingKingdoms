import json

from undyingkingdoms.models import World
from .helpers import register, initialize, login


def test_get_token(client):
    with client:
        rv_login = login(client, 'haldon@gmail.com', 'brunner')
        assert "Public Info" in rv_login.data.decode()
        assert rv_login.status_code == 200

        rv = client.get('/game_clock/token')
        data = json.loads(rv.data.decode())
        assert data['status'] == 'success'
        assert data['message']


def test_advance_data(client):
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
        day = world.day
        rv = client.get(
            '/game_clock/advance',
            headers=dict(
                Authorization='Bearer ' + data_token['auth_token']
            )
        )

        data = json.loads(rv.data.decode())
        assert data['status'] == 'success'
        assert data['message']
        assert World.query.first().day > day
