def login(client, username, password):
    """Log user in to client."""
    return client.post('/login/', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    """Log current user out."""
    return client.get('/logout/', follow_redirects=True)

