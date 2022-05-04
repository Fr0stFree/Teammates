from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Расширенная кастомная модель пользователя. Поддерживает картинку (avatar)
    пользователя и биографию (bio). Вместо имени и фамилии введено общее поле
    "Имя" (name). Авторизация производится по электронной почте и паролю.
    """
    name = models.CharField(
        verbose_name='Имя и фамилия',
        max_length=40,
        null=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        null=True,
        unique=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        null=True,
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        null=True,
        default='avatar.svg'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = 'Пользователи'
