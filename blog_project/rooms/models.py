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
        unique=True
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


class Topic(models.Model):
    """
    Модель тематики комнаты.
    """
    name = models.CharField(verbose_name='Тематика', max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Тематики'


class Room(models.Model):
    """
    Модель комнаты.
    """
    name = models.CharField(verbose_name='Название', max_length=150)
    host = models.ForeignKey(
        verbose_name='Автор',
        to=User,
        related_name='rooms',
        on_delete=models.SET_NULL,
        null=True,
    )
    topic = models.ForeignKey(
        verbose_name='Тематика',
        to=Topic,
        related_name='rooms',
        on_delete=models.SET_NULL,
        null=True,
    )
    participants = models.ManyToManyField(
        verbose_name='Участники',
        to=User,
        related_name='participants',
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return self.name


class Message(models.Model):
    """
    Модель пользовательского комментария.
    """
    user = models.ForeignKey(
        verbose_name='Автор',
        to=User,
        related_name='messages',
        on_delete=models.SET_NULL,
        null=True,
    )
    room = models.ForeignKey(
        verbose_name='Комната',
        to=Room,
        related_name='messages',
        on_delete=models.CASCADE,
    )
    body = models.TextField(verbose_name='Текст')
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)

    class Meta:
        ordering = ['updated', 'created']

    def __str__(self):
        return self.body[:20] + '...'
