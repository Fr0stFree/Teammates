from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm):
    """
    Форма для создания экземпляра комнаты.
    """
    class Meta:
        model = Room
        fields = 'topic', 'name', 'description'
