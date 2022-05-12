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
        required=True,
        write_only=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='user')
    room = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        required=False
    )
    body = serializers.CharField()
    pk = serializers.PrimaryKeyRelatedField(
        queryset=Message.objects.all(),
        required=False
    )

    class Meta:
        model = Message
        fields = ('pk', 'author', 'body', 'room')


class UserSerializer(SignUpSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'name', 'is_staff', 'bio',
                  'last_login', 'date_joined', 'messages')


class UserSelfUpdateSerializer(UserSerializer):
    email = serializers.CharField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)


class UserAdminUpdateSerializer(UserSerializer):
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)


class RoomDetailSerializer(serializers.ModelSerializer):
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


class RoomListSerializer(serializers.ModelSerializer):
    topic = serializers.StringRelatedField()
    host = serializers.StringRelatedField()
    participants_count = serializers.SerializerMethodField()
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('topic', 'name', 'host', 'updated', 'created',
                  'participants_count', 'message_count')

    def get_participants_count(self, obj):
        return obj.participants.count()

    def get_message_count(self, obj):
        return obj.messages.count()
