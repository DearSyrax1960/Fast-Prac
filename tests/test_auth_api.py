import pytest


@pytest.fixture()
def new_user():
    """Generate a user."""
    return {
        "name": "John",
        "email": "example@gmail.com",
        "password": "password@98",
    }


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == "server is running"


def test_signup(test_client, new_user):
    response = test_client.post('/auth/signup', json=new_user)
    assert response.status_code == 201
    assert response.json()['token_type'] == "bearer"
    assert response.json()['access_token'] is not None


def test_signup_fails_if_email_had_been_registered(test_client, new_user):
    same_user = new_user
    test_client.post('/auth/signup', json=new_user)
    response = test_client.post('/auth/signup', json=same_user)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered."}


def test_signup_fails_if_email_was_not_correct(test_client, new_user):
    new_user['email'] = 'an incorrect email'
    response = test_client.post('/auth/signup', json=new_user)
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == "value_error"
    assert "email" in response.json()['detail'][0]['loc']


def test_signup_fails_if_password_is_short(test_client, new_user):
    new_user['password'] = 'short'
    response = test_client.post('/auth/signup', json=new_user)
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == "string_too_short"
    assert "password" in response.json()['detail'][0]['loc']
