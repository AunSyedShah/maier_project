import pytest
from app import app, db, init_db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        init_db()
        yield app.test_client()


def test_register_login_logout(client):
    # Register
    resp = client.post('/register', data={
        'email': 'test@example.com',
        'password': 'secret123',
        'confirm': 'secret123'
    }, follow_redirects=True)
    assert b'Registration successful' in resp.data

    # Register duplicate should warn
    resp_dup = client.post('/register', data={
        'email': 'test@example.com',
        'password': 'secret123',
        'confirm': 'secret123'
    }, follow_redirects=True)
    assert b'Email already registered' in resp_dup.data

    # Index dashboard requires login (redirects to login) BEFORE logging in
    resp_index_redirect = client.get('/', follow_redirects=False)
    assert resp_index_redirect.status_code == 302
    assert '/login' in resp_index_redirect.headers.get('Location', '')

    # Follow redirect and check login page content for index
    resp_index_follow = client.get('/', follow_redirects=True)
    assert b'Login' in resp_index_follow.data

    # Profile requires login (redirects to login) BEFORE logging in
    resp_profile_redirect = client.get('/profile', follow_redirects=False)
    assert resp_profile_redirect.status_code == 302
    assert '/login' in resp_profile_redirect.headers.get('Location', '')

    # Follow redirect and check login page content
    resp_profile_follow = client.get('/profile', follow_redirects=True)
    assert b'Login' in resp_profile_follow.data

    # Login
    resp_login = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'secret123'
    }, follow_redirects=True)
    assert b'Logged in successfully' in resp_login.data

    # Check index shows logged-in user in navbar
    resp_index = client.get('/')
    assert b'Logged in as test@example.com' in resp_index.data

    # Profile accessible after login
    resp_profile = client.get('/profile')
    assert b'test@example.com' in resp_profile.data

    # Logout
    resp_logout = client.get('/logout', follow_redirects=True)
    assert b'Logged out' in resp_logout.data
