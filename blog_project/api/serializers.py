from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from users.models import User
from rooms.models import Room, Message, Topic


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            validate_email,
        ],
    )
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'name', 'is_staff', 'bio', 'last_login',
                  'date_joined')


class UserSelfUpdateSerializer(UserSerializer):
    email = serializers.CharField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)


class UserAdminUpdateSerializer(UserSerializer):
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ('user', 'body')


class RoomSerializer(serializers.ModelSerializer):
    topic = serializers.CharField()
    host = serializers.StringRelatedField()
    name = serializers.CharField(
        validators=[
            UniqueValidator(queryset=Room.objects.all()),
        ],
    )
    messages = MessageSerializer(many=True, required=False)
    participants = serializers.StringRelatedField(many=True, required=False)

    def create(self, validated_data):
        """
        Переопределенный метод создания комнаты.
        """
        # При получении сериализованных данных, вытаскиваем строковое
        # представление объекта класса Topic
        topic = validated_data.pop('topic')
        # Создаем или возвращаем Topic с таким названием
        current_topic, status = Topic.objects.get_or_create(name=topic)
        host = self.context.get('request').user
        # Создаем экземпляр комнаты связав комнату с объектами Host и Topic
        room = Room.objects.create(
            topic=current_topic,
            host=host,
            **validated_data
        )
        # Добавим создателя комнаты как первого участника
        room.participants.add(host)
        return room

    class Meta:
        model = Room
        fields = ('topic', 'name', 'host', 'description',
                  'updated', 'created', 'participants', 'messages')
