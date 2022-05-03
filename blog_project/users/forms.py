from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Кастомная форма для регистрации пользователя.
    Наследуется от стандартной UserCreationForm.
    """
    class Meta:
        model = User
        fields = 'name', 'username', 'email', 'password1', 'password2'


class UserForm(ModelForm):
    """
    Форма для авторизации пользователя.
    """
    class Meta:
        model = User
        fields = 'avatar', 'name', 'username', 'email', 'bio'
