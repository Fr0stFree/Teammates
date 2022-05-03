from rest_framework.viewsets import ReadOnlyModelViewSet

from rooms.models import Room
from users.models import User
from .serializers import (
    RoomSerializer,
    UserListSerializer,
    UserDetailSerializer,
)


class RoomViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет для работы с моделями комнат. Только для чтения.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class UserViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет для работы с пользователями. Только для чтения.
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
