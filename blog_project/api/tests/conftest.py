import pytest
from collections import namedtuple
from faker import Faker
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from users.models import User

ANON_PASSWORD = Faker().password()
USER_PASSWORD = Faker().password()
ADMIN_PASSWORD = Faker().password()


class Client:
    def __init__(self, password, anon=False, is_staff=False, is_superuser=False):
        if not anon:
            self.properties = User.objects.create_user(
                email=Faker().email(),
                username=Faker().user_name(),
                password=password,
                name=Faker().name(),
                bio=Faker().paragraph(nb_sentences=2),
                is_staff=is_staff,
                is_superuser=is_superuser,
            )
            token = RefreshToken.for_user(self.properties).access_token
            self.client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        else:
            self.client = APIClient()
            Prop = namedtuple(
                'props', ('email', 'username', 'password', 'name', 'bio')
            )
            self.properties = Prop(
                Faker().email(),
                Faker().user_name(),
                password,
                Faker().name(),
                Faker().paragraph(nb_sentences=2)
            )

    def request(self, method, url, payload=None):
        request = {
            'GET': self.client.get(url, payload),
            'POST': self.client.post(url, payload),
            'PATCH': self.client.patch(url, payload),
            'DELETE': self.client.delete(url, payload),
        }
        response = request.get(method)
        return response


@pytest.fixture
def anon():
    anon = Client(ANON_PASSWORD, True)
    return anon


@pytest.fixture
def user():
    user = Client(USER_PASSWORD, False)
    return user


@pytest.fixture
def admin():
    admin = Client(ADMIN_PASSWORD, False, True, True)
    return admin
