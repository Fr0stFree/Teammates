from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Room, Topic
from .forms import RoomForm


def home(request):
    template = 'rooms/home.html'
    q = request.GET.get('q') if request.GET.get('q') else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    context = {
        'rooms': rooms,
        'topics': Topic.objects.all(),
        'room_count': rooms.count()
    }
    return render(request, template, context)


def room(request, pk):
    template = 'rooms/room.html'
    context = {
        'room': get_object_or_404(Room, pk=pk),
    }
    return render(request, template, context)


def createRoom(request):
    if request.method == 'GET':
        template = 'rooms/room_form.html'
        context = {
            'form': RoomForm(),
        }
        return render(request, template, context)

    elif request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


def updateRoom(request, pk):
    room = Room.objects.get(pk=pk)

    if request.method == 'GET':
        template = 'rooms/room_form.html'
        context = {
            'room': room,
            'form': RoomForm(instance=room),
        }
        return render(request, template, context)

    elif request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')


def deleteRoom(request, pk):
    room = Room.objects.get(pk=pk)

    if request.method == 'GET':
        template = 'delete.html'
        context = {
            'obj': room,
        }
        return render(request, template, context)

    elif request.method == 'POST':
        room.delete()
        return redirect('home')
