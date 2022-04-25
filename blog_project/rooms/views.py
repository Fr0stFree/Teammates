from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Room, Topic, Message
from .forms import RoomForm

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    template = 'login&register.html'
    context = {
        'page': 'login',
    }
    if request.method == 'GET':
        return render(request, template, context)

    elif request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Incorrect data')
        return render(request, template, context)


def registerPage(request):
    template = 'login&register.html'
    context = {
        'page': 'register',
        'form': UserCreationForm(),
    }
    if request.method == 'GET':
        return render(request, template, context)

    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
            return render(request, template, context)

def logoutUser(request):
    logout(request)
    return redirect('home')


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
        'room_count': rooms.count(),
        'room_messages': Message.objects.filter(Q(room__topic__name__icontains=q))[:5]

    }
    return render(request, template, context)


def room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'GET':
        template = 'rooms/room.html'
        context = {
            'room': room,
            'participants': room.participants.all(),
            'room_messages': room.messages.all(),
        }
        return render(request, template, context)

    elif request.method == 'POST':
        room.messages.create(
            user = request.user,
            body = request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.pk)


def userProfile(request, pk):
    template = 'profile.html'
    user = User.objects.get(pk=pk)
    context = {
        'user': user,
        'rooms': user.rooms.all(),
        'room_messages': user.messages.all(),
        'topics': Topic.objects.all(),
    }
    return render(request, template, context)


@login_required(login_url='login')
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
            form = form.save(commit=False)
            form.host = request.user
            form.save()
            room = Room.objects.filter(host=request.user).first()
            room.participants.add(request.user)
            return redirect('room', pk=room.pk)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(pk=pk)

    if request.user != room.host and not request.user.is_superuser:
        return HttpResponse('Permission denied')

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


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(pk=pk)

    if request.user != room.host and not request.user.is_superuser:
        return HttpResponse('Permission denied')

    if request.method == 'GET':
        template = 'delete.html'
        context = {
            'obj': room,
        }
        return render(request, template, context)

    elif request.method == 'POST':
        room.delete()
        return redirect('home')


@login_required(login_url='login')
def deleteMessage(request, room_pk, message_pk):
    message = Message.objects.get(pk=message_pk)

    if request.user != message.user and not request.user.is_superuser:
        return HttpResponse('Permission denied')

    if request.method == 'GET':
        template = 'delete.html'
        context = {
            'obj': message,
        }
        return render(request, template, context)

    elif request.method == 'POST':
        message.delete()
        return redirect('room', room_pk)