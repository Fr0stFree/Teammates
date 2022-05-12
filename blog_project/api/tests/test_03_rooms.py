from http import HTTPStatus
import pytest

DETAIL_METHODS = ['GET', 'PATCH', 'DELETE']
LIST_METHODS = ['GET', 'POST']


@pytest.mark.django_db(transaction=True)
def test_room_list_fields_correctness(room, user):
    url = '/api/rooms/1/'
    method = 'GET'
    response = user.request(method, url)
    assert response.status_code == HTTPStatus.OK
    assert response.data.get('topic') == room.topic.name
    assert response.data.get('name') == room.name
    assert response.data.get('host') == room.host.username
    assert response.data.get('description') == room.description
    # Подфиксить позже
    assert response.data.get('updated') is not None
    assert response.data.get('created') is not None
    assert response.data.get('description') == room.description
    assert response.data.get('participants') == [participant.username for participant in room.participants.all()]
    # Постараться разобраться с messages
