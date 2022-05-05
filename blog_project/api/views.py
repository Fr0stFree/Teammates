from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, permissions

from users.models import User
from .permissions import IsAdmin
from .serializers import (
    SignUpSerializer,
    SignInSerializer,
    UserSerializer,
    UserAdminUpdateInfoSerializer,
    UserSelfUpdateInfoSerializer,
)


class APISignUp(APIView):
    """
    Вью-фукнция для регистрации нового пользователя. Для получения требуется
    предоставить валидные email, username и пароль. Права доступа:
    неавторизованный пользователь. Пример запроса:
    POST /v1/auth/signup/
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
        hashed_password = make_password(serializer.validated_data['password'])
        serializer.save(password=hashed_password)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APISignIn(APIView):
    """
    Вью-фукнция для получения JWT-токена. Для получения требуется
    предоставить электронную почту и пароль. Права доступа:
    неавторизованный пользователь. Пример  запроса:
    POST /api/auth/signin/
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
        email = serializer.validated_data.get('email').lower()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'email': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )

        password = serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            return Response(
                {'password': 'Некорректный пароль'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)}, status=status.HTTP_201_CREATED)


class UserViewSet(ModelViewSet):
    """
    Вьюсет для CRUD-операций с моделями пользователей.
    Права доступа: администратор. Пример запроса:
    DELETE /api/users/<username>/ HTTP/1.1
    По url /api/users/me/ доступно на чтение и изменение
    собственных пользовательских атрибутов. Права доступа:
    авторизованный пользователь. Пример запроса:
    PATCH /api/users/me/ HTTP/1.1
    Content-Type: application/json
    {
        "bio": "str",
        "name": "str",
        "username": "str"
    }
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserAdminUpdateInfoSerializer
    permission_classes = (IsAdmin, )

    def get_permissions(self):
        if self.action == 'retrieve':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    @action(methods=['GET', 'PATCH'], detail=False, url_path='me',
            permission_classes=(permissions.IsAuthenticated, ))
    def user_self_retrieve_update(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = UserSelfUpdateInfoSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
