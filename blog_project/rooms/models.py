from django.db import models
from users.models import User


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
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.body[:20] + '...'
