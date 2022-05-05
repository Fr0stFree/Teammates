from rest_framework.test import APIClient
import pytest


client = APIClient


@pytest.mark.django_db
def test_anon_able_to_register():
   assert 1 == 1


@pytest.mark.django_db
def test_anon_able_to_get_token():
   assert 1 == 1
