from django.contrib.auth.models import User
from django import forms

from .models import Room


class RoomForm(forms.ModelForm):
    
    class Meta:
        model = Room
        fields = 'topic', 'name', 'description'

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = 'username', 'email'