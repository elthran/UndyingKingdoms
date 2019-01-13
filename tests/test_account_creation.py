from .helpers import register, initialize


def test_account_creation(client):
    rv_register = register(client, 'test', 'test@gmail.com', 'test')
    assert "Establish county" in rv_register.data.decode()
    assert rv_register.status_code == 200

    rv_initialize = initialize(client, "TestLand", "TheTester", 2, 2)
    assert "Public Info" in rv_initialize.data.decode()
    assert rv_initialize.status_code == 200
