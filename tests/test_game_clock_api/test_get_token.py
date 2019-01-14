import json

from tests.helpers import login


def test_get_token(client):
    with client:
        rv_login = login(client, 'haldon@gmail.com', 'brunner')
        assert "Public Info" in rv_login.data.decode()
        assert rv_login.status_code == 200

        rv = client.get('/game_clock/token')
        data = json.loads(rv.data.decode())
        assert data['status'] == 'success'
        assert data['message']
