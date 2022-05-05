from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(write_only=True)

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_email(self, email):
        validate_email(email)
        return email

    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')
