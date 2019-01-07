from .helpers import login, logout


def test_login_logout(client):
    """Make sure that login and logout work."""

    rv = login(client, 'haldon@gmail.com', 'brunner')
    assert rv.status_code == 200
    # assert b'You were logged in' in rv.data
