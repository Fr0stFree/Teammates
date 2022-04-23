from django.shortcuts import render, get_object_or_404

from .models import Room

def home(request):
    context = {
        'rooms': Room.objects.all(),
    }
    return render(request, 'rooms/home.html', context)

def room(request, pk):
    context = {
        'room': get_object_or_404(Room, pk=pk),
    }
    return render(request, 'rooms/room.html', context)