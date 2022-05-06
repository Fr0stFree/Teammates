from http import HTTPStatus

import pytest
from django.urls import reverse


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
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
def test_admin_able_to_see_user_list(admin):
    response = admin.client.post('/api/users/')
    print(admin.client.credentials())
    print(response.data)
    assert response.status_code == HTTPStatus.OK
