import pytest
from faker import Faker
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APIClient

from users.models import User


USER_PASSWORD = Faker().password()
ADMIN_PASSWORD = Faker().password()


@pytest.fixture
def anon():
    class AnonUser:
        email = Faker().email()
        username = Faker().user_name()
        password = Faker().password()
        client = APIClient()
    return AnonUser


@pytest.fixture
def user():
    USER_PASSWORD = Faker().password()
    instance = User.objects.create_user(
        email=Faker().email(),
        username=Faker().user_name(),
        password=USER_PASSWORD,
        name=Faker().name(),
        bio=Faker().paragraph(nb_sentences=2),
    )
    refresh = RefreshToken.for_user(instance)

    class AuthUser:
        email = instance.email
        username = instance.username
        password = USER_PASSWORD
        name = instance.name
        bio = instance.bio
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return AuthUser


@pytest.fixture
def admin():
    ADMIN_PASSWORD = Faker().password()
    instance = User.objects.create_superuser(
        email=Faker().email(),
        username=Faker().user_name(),
        password=ADMIN_PASSWORD,
        name=Faker().name(),
        bio=Faker().paragraph(nb_sentences=2),
    )
    
    refresh = RefreshToken.for_user(instance)

    class AdminUser:
        email = instance.email
        username = instance.username
        password = ADMIN_PASSWORD
        name = instance.name
        bio = instance.bio
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return AdminUser
