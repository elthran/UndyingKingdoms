import json

from tests.helpers import login
from undyingkingdoms.models import DAU


def test_advance_24h_analytics(client):
    with client:
        rv_login = login(client, 'haldon@gmail.com', 'brunner')
        assert "Calendar" in rv_login.data.decode()
        assert rv_login.status_code == 200

        rv_token = client.get('/game_clock/token')
        data_token = json.loads(rv_token.data.decode())
        assert data_token['status'] == 'success'
        assert data_token['auth_token']
        assert rv_token.status_code == 200

        # I might need to logout here just to be safe?

        dau_events = DAU.query.count()
        rv = client.get(
            '/game_clock/advance_24h_analytics',
            headers=dict(
                Authorization='Bearer ' + data_token['auth_token']
            )
        )

        data = json.loads(rv.data.decode())
        assert data['status'] == 'success'
        assert data['message']
        dau_events2 = DAU.query.count()
        assert dau_events2 > dau_events
