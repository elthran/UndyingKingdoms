def register(client, username, email, password):
    """Register a user."""
    return client.post('/register/', data=dict(
        username=username,
        email=email,
        password=password,
        confirmation=password
    ), follow_redirects=True)


def initialize(client, county, leader, gender, race):
    """Initialize a user."""
    return client.post('/initialize/', data=dict(
        county=county,
        leader=leader,
        gender=gender,
        race=race
    ), follow_redirects=True)


def login(client, email, password):
    """Log user in to client."""
    return client.post('/login/', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    """Log current user out."""
    return client.get('/logout/', follow_redirects=True)

