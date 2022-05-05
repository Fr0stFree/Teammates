import pytest
from http import HTTPStatus
from faker import Faker
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User

from .conftest import USER_PASSWORD

client = APIClient()
fake = Faker()


@pytest.mark.django_db
def test_anon_able_to_register():
    count_users = User.objects.count()
    payload = {
        'email': Faker().email(),
        'username': Faker().user_name(),
        'password': Faker().password(),
    }
    response = client.post(reverse('api:signup'), payload)
    registered_anon = User.objects.filter(
        username=payload['username'],
        email=payload['email'],
    )
    assert response.status_code == HTTPStatus.CREATED
    assert registered_anon.exists()
    assert count_users + 1 == User.objects.count()


@pytest.mark.django_db
def test_user_able_to_get_token(user):
    payload = {
        'password': USER_PASSWORD,
        'email': user.email,
    }
    response = client.post(reverse('api:signin'), payload)
    assert response.status_code == HTTPStatus.OK
    assert 'token' in response.data


@pytest.mark.django_db
def test_non_existent_user_unable_to_get_token():
    payload = {
        'email': Faker().email(),
        'password': Faker().password(),
    }
    response = client.post(reverse('api:signin'), payload)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'token' not in response.data


@pytest.mark.django_db
def test_user_unable_to_get_token_with_wrong_password(user):
    payload = {
        'email': user.email,
        'password': Faker().password(),
    }
    response = client.post(reverse('api:signin'), payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert 'token' not in response.data
