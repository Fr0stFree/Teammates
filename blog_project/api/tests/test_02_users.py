from http import HTTPStatus

import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User

from .conftest import USER_PASSWORD



@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
def test_anon_unable_to_see_user_list(anon):
    response = anon.client.post('/api/users/')
    print(response.data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
def test_user_unable_to_see_user_list(user):
    response = user.client.post('/api/users/')
    print(response.data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
def test_user_unable_to_see_user_list(user):
    response = user.client.post('/api/users/')
    print(response.data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

