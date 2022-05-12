from http import HTTPStatus
from faker import Faker
import pytest

from users.models import User

DETAIL_METHODS = ['GET', 'PATCH', 'DELETE']
LIST_METHODS = ['GET', 'POST']


# Permissions

@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('method', LIST_METHODS)
def test_anon_permissions_for_user_list(method, anon):
    url = '/api/users/'
    response = anon.request(method, url)
    expected_status_code = {
        'GET': HTTPStatus.UNAUTHORIZED,
        'POST': HTTPStatus.UNAUTHORIZED,
    }
    assert response.status_code == expected_status_code.get(method)


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('method', DETAIL_METHODS)
def test_anon_permissions_for_user_detail(method, anon, user):
    url = f'/api/users/{user.properties.username}/'
    response = anon.request(method, url)
    expected_status_code = {
        'GET': HTTPStatus.OK,
        'PATCH': HTTPStatus.UNAUTHORIZED,
        'DELETE': HTTPStatus.UNAUTHORIZED,
    }
    assert response.status_code == expected_status_code.get(method)


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('method', LIST_METHODS)
def test_user_permissions_for_user_list(method, user):
    url = '/api/users/'
    response = user.request(method, url)
    expected_status_code = {
        'GET': HTTPStatus.FORBIDDEN,
        'POST': HTTPStatus.FORBIDDEN,
    }
    assert response.status_code == expected_status_code.get(method)


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('method', DETAIL_METHODS)
def test_user_permissions_for_user_detail(method, user, admin):
    url = f'/api/users/{user.properties.username}/'
    response = user.request(method, url)
    expected_status_code = {
        'GET': HTTPStatus.OK,
        'PATCH': HTTPStatus.FORBIDDEN,
        'DELETE': HTTPStatus.FORBIDDEN,
    }
    assert response.status_code == expected_status_code.get(method)


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('method', LIST_METHODS)
def test_admin_permissions_for_user_list(method, admin):
    url = '/api/users/'
    response = admin.request(method, url)
    expected_status_code = {
        'GET': HTTPStatus.OK,
        # Запрос без данных для создания пользователя вернет 400
        'POST': HTTPStatus.BAD_REQUEST,
    }
    assert response.status_code == expected_status_code.get(method)


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('method', DETAIL_METHODS)
def test_admin_permissions_for_user_detail(method, user, admin):
    url = f'/api/users/{user.properties.username}/'
    response = admin.request(method, url)
    expected_status_code = {
        'GET': HTTPStatus.OK,
        'PATCH': HTTPStatus.OK,
        'DELETE': HTTPStatus.NO_CONTENT,
    }
    assert response.status_code == expected_status_code.get(method)


# Serializers

@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
def test_other_user_detail_fields_correctness(user, admin):
    url = f'/api/users/{admin.properties.username}/'
    method = 'GET'
    response = user.request(method, url)
    assert response.status_code == HTTPStatus.OK
    assert response.data.get('name') == admin.properties.name
    assert response.data.get('username') == admin.properties.username
    assert response.data.get('bio') == admin.properties.bio
    assert response.data.get('email') == admin.properties.email
    assert response.data.get('name') == admin.properties.name
    assert response.data.get('is_staff') == admin.properties.is_staff
    assert response.data.get('password') is None


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
def test_self_user_detail_fields_correctness(user):
    url = '/api/users/me/'
    method = 'GET'
    response = user.request(method, url)
    assert response.status_code == HTTPStatus.OK
    assert response.data.get('name') == user.properties.name
    assert response.data.get('username') == user.properties.username
    assert response.data.get('bio') == user.properties.bio
    assert response.data.get('email') == user.properties.email
    assert response.data.get('name') == user.properties.name
    assert response.data.get('is_staff') == user.properties.is_staff
    assert response.data.get('password') is None


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
def test_user_list_fields_correctness(admin):
    url = '/api/users/'
    method = 'GET'
    response = admin.request(method, url)
    assert response.status_code == HTTPStatus.OK
    assert len(response.data) == User.objects.count()
    assert response.data[0].get('name') == admin.properties.name
    assert response.data[0].get('username') == admin.properties.username
    assert response.data[0].get('bio') == admin.properties.bio
    assert response.data[0].get('email') == admin.properties.email
    assert response.data[0].get('name') == admin.properties.name
    assert response.data[0].get('is_staff') == admin.properties.is_staff
    assert response.data[0].get('password') is None


# Views

@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
def test_anon_unable_to_get_self_profile(anon):
    url = '/api/users/me/'
    method = 'GET'
    response = anon.request(method, url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
def test_user_able_to_update_self_profile(user):
    url = '/api/users/me/'
    method = 'PATCH'
    payload = {
        'username': Faker().user_name(),
        'password': Faker().password(),
        'bio': Faker().paragraph(nb_sentences=1),
        'name': Faker().name()
    }
    response = user.request(method, url, payload)
    updated_user = User.objects.filter(
        username=payload.get('username'),
        password=payload.get('password'),
        bio=payload.get('bio'),
        name=payload.get('name'),
    )
    assert response.status_code == HTTPStatus.OK
    assert updated_user.exists()
    assert updated_user.count() == 1
    assert user.properties.id == updated_user.first().id


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
def test_user_unable_to_change_self_email_and_status(user):
    url = '/api/users/me/'
    method = 'PATCH'
    payload = {
        'email': Faker().email(),
        'is_staff': True,
        'is_superuser': True
    }
    response = user.request(method, url, payload)
    assert response.status_code == HTTPStatus.OK
    assert user.properties.email != payload.get('email')
    assert user.properties.is_staff != payload.get('is_staff')
    assert user.properties.is_superuser != payload.get('is_superuser')


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
def test_admin_able_to_create_a_user_instance(admin):
    url = '/api/users/'
    method = 'POST'
    payload = {
        'email': Faker().email(),
        'username': Faker().user_name(),
        'password': Faker().password(),
        'bio': Faker().paragraph(nb_sentences=1),
        'is_staff': True,
        'name': Faker().name()
    }
    user_count = User.objects.count()
    response = admin.request(method, url, payload)
    created_user = User.objects.filter(
        email=payload.get('email'),
        username=payload.get('username'),
        password=payload.get('password'),
        is_staff=payload.get('is_staff'),
        bio=payload.get('bio'),
        name=payload.get('name'),
    )
    assert response.status_code == HTTPStatus.CREATED
    assert created_user.exists()
    assert user_count + 1 == User.objects.count()


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
def test_admin_able_to_update_a_user_instance(admin, user):
    url = f'/api/users/{user.properties.username}/'
    method = 'PATCH'
    payload = {
        'email': Faker().email(),
        'username': Faker().user_name(),
        'password': Faker().password(),
        'bio': Faker().paragraph(nb_sentences=1),
        'is_staff': True,
        'name': Faker().name()
    }
    response = admin.request(method, url, payload)
    updated_user = User.objects.filter(
        email=payload.get('email'),
        username=payload.get('username'),
        password=payload.get('password'),
        is_staff=payload.get('is_staff'),
        bio=payload.get('bio'),
        name=payload.get('name')
    )
    assert response.status_code == HTTPStatus.OK
    assert updated_user.exists()
    assert updated_user.count() == 1
    assert user.properties.id == updated_user.first().id


@pytest.mark.APIusers
@pytest.mark.django_db(transaction=True)
def test_admin_able_to_delete_a_user_instance(admin, user):
    url = f'/api/users/{user.properties.username}/'
    method = 'DELETE'
    user_count = User.objects.count()
    user_id = user.properties.id
    response = admin.request(method, url)
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert user_count - 1 == User.objects.count()
    assert not User.objects.filter(id=user_id).exists()
