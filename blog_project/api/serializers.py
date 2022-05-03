from rest_framework import serializers

from rooms.models import Room
from users.models import User


class UserListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы со списком пользователей.
    """
    class Meta:
        model = User
        fields = 'username', 'name'


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы экземпляром пользователя.
    """

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'email',
            'is_superuser',
            'bio',
        )


class RoomSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с моделями комнат.
    """    
    host = serializers.StringRelatedField()
    topic = serializers.StringRelatedField()
    participants = UserListSerializer(many=True)

    class Meta:
        model = Room
        fields = (
            "name",
            "description",
            "host",
            "topic",
            "participants",
        )
