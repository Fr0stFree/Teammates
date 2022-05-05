import pytest
from faker import Faker

from users.models import User


USER_PASSWORD = Faker().password()


@pytest.fixture
def user():
    user_instance = User.objects.create_user(
        email=Faker().email(),
        username=Faker().user_name(),
        password=USER_PASSWORD,
        name=Faker().name(),
        bio=Faker().paragraph(nb_sentences=2),
    )
    return user_instance


""" @pytest.fixture
def anon():
    anon_data = {
        'email': Faker().email(),
        'username': Faker().user_name(),
        'password': Faker().password(),
    }
    return anon_data """
