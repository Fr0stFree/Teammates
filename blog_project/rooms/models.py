from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(
        to=User,
        related_name='rooms',
        on_delete=models.SET_NULL,
        null=True,
    )
    topic = models.ForeignKey(
        to=Topic,
        related_name='rooms',
        on_delete=models.SET_NULL,
        null=True,
    )
    participants = models.ManyToManyField(
        to=User,
        related_name='participants',
        blank=True,
    )
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name='messages',
        on_delete=models.SET_NULL,
        null=True
    )
    room = models.ForeignKey(
        to=Room,
        related_name='messages',
        on_delete=models.CASCADE
    )
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[:20] + '...'
