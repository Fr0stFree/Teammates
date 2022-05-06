from http import HTTPStatus

import pytest
from faker import Faker
from django.urls import reverse
from users.models import User

from .conftest import USER_PASSWORD


@pytest.mark.APIauth
@pytest.mark.django_db(transaction=True)
def test_anon_able_to_register(anon):
    count_users = User.objects.count()
    payload = {
        'email': anon.email,
        'username': anon.username,
        'password': anon.password,
    }
    response = anon.client.post(reverse('api:signup'), payload)
    registered_anon = User.objects.filter(
        username=payload['username'],
        email=payload['email'],
    )
    print(response.data)
    assert response.status_code == HTTPStatus.CREATED
    assert registered_anon.exists()
    assert count_users + 1 == User.objects.count()


@pytest.mark.APIauth
@pytest.mark.django_db(transaction=True)
def test_user_able_to_get_token(user):
    payload = {
        'password': user.password,
        'email': user.email,
    }
    response = user.client.post(reverse('api:signin'), payload)
    print(response.data)
    assert response.status_code == HTTPStatus.CREATED
    assert 'token' in response.data


@pytest.mark.APIauth
@pytest.mark.django_db(transaction=True)
def test_non_existent_user_unable_to_get_token(anon):
    payload = {
        'email': anon.email,
        'password': anon.password,
    }
    response = anon.client.post(reverse('api:signin'), payload)
    print(response.data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'token' not in response.data


@pytest.mark.APIauth
@pytest.mark.django_db(transaction=True)
def test_user_unable_to_get_token_with_wrong_password(user):
    payload = {
        'email': user.email,
        'password': Faker().password(),
    }
    response = user.client.post(reverse('api:signin'), payload)
    print(response.data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert 'token' not in response.data
