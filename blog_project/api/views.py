from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from rooms.models import Room
from users.models import User
from .serializers import (
    SignUpSerializer,
    SignInSerializer,
)


class APISignUp(APIView):
    """
    Вью-фукнция для получения запроса для отправки на почту кода подтверждения.
    Для получения требуется предоставить валидные email и username. Права
    доступа: неавторизованный пользователь. Пример запроса:
    POST /v1/auth/signup/ HTTP/1.1
    Content-Type: application/json
    {
        "email": "str",
        "password": "str",
        "username": "str"
    }
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        try:
            validate_password(password)
        except Exception as e:
            return Response({'password': e}, status=status.HTTP_403_FORBIDDEN)
        User.objects.create(
            email=serializer.validated_data.get('email'),
            username=serializer.validated_data.get('username'),
            password=make_password(password)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APISignIn(APIView):
    """
    Вью-фукнция для получения JWT-токена. Для получения требуется
    предоставить электронную почту и пароль. Права доступа:
    неавторизованный пользователь. Пример  запроса:

    POST /v1/auth/token/ HTTP/1.1
    Content-Type: application/json
    {
        "email": "str",
        "password": "str"
    }
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )

        password = serializer.validated_data.get('password')
        if not user.check_password(password):
            return Response(
                {'password': 'Некорректный пароль'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)}, status=status.HTTP_201_CREATED)
