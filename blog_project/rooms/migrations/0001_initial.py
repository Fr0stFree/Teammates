# Generated by Django 4.0.4 on 2022-05-04 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Тематика')),
            ],
            options={
                'verbose_name_plural': 'Тематики',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rooms', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('participants', models.ManyToManyField(blank=True, null=True, related_name='participants', to=settings.AUTH_USER_MODEL, verbose_name='Участники')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='rooms.topic', verbose_name='Тематика')),
            ],
            options={
                'verbose_name_plural': 'Комнаты',
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='Текст')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='rooms.room', verbose_name='Комната')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name_plural': 'Сообщения',
                'ordering': ['updated', 'created'],
            },
        ),
    ]
