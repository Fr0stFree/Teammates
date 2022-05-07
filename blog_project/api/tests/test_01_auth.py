from http import HTTPStatus

import pytest
from django.urls import reverse
from .conftest import ANON_PASSWORD, USER_PASSWORD
from users.models import User


@pytest.mark.APIauth
@pytest.mark.django_db(transaction=True)
def test_anon_able_to_register(anon):
    count_users = User.objects.count()
    method = 'POST'
    url = reverse('api:signup')
    payload = {
        'email': anon.properties.email,
        'username': anon.properties.username,
        'password': ANON_PASSWORD,
    }
    response = anon.request(method, url, payload)
    registered_anon = User.objects.filter(
        username=payload['username'],
        email=payload['email'],
    )
    assert response.status_code == HTTPStatus.CREATED
    assert registered_anon.exists()
    assert count_users + 1 == User.objects.count()


@pytest.mark.APIauth
@pytest.mark.django_db(transaction=True)
def test_user_able_to_get_token(user):
    method = 'POST'
    url = reverse('api:signin')
    payload = {
        'password': USER_PASSWORD,
        'email': user.properties.email,
    }
    response = user.request(method, url, payload)
    assert response.status_code == HTTPStatus.CREATED
    assert 'token' in response.data


@pytest.mark.APIauth
@pytest.mark.django_db(transaction=True)
def test_non_existent_user_unable_to_get_token(anon):
    method = 'POST'
    url = reverse('api:signin')
    payload = {
        'email': anon.properties.email,
        'password': ANON_PASSWORD,
    }
    response = anon.request(method, url, payload)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'token' not in response.data


@pytest.mark.APIauth
@pytest.mark.django_db(transaction=True)
def test_user_unable_to_get_token_with_wrong_password(user):
    method = 'POST'
    url = reverse('api:signin')
    payload = {
        'email': user.properties.email,
        'password': USER_PASSWORD + 'foobar',
    }
    response = user.request(method, url, payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert 'token' not in response.data
