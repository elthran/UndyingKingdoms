# import pytest


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'Redirecting...' in rv.data
    assert rv.status_code == 302
    assert 'login' in rv.location
