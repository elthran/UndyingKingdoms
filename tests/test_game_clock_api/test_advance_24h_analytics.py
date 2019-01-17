import json

from tests.helpers import login
from undyingkingdoms.models import World


def test_advance_24h_analytics(client):
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
        analytic_cycles = world.analytic_cycles
        rv = client.get(
            '/game_clock/advance_24h_analytics',
            headers=dict(
                Authorization='Bearer ' + data_token['auth_token']
            )
        )

        data = json.loads(rv.data.decode())
        assert data['status'] == 'success'
        assert data['message']
        world2 = World.query.first()
        assert world2.analytic_cycles > analytic_cycles
