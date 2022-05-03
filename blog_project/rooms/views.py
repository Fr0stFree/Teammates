from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import User, Room, Topic, Message
from .forms import RoomForm, UserForm, CustomUserCreationForm


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
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Incorrect data')
        return render(request, template, context)


def registerPage(request):
    template = 'login&register.html'
    context = {
        'page': 'register',
        'form': CustomUserCreationForm(),
    }
    if request.method == 'GET':
        return render(request, template, context)

    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
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
            user=request.user,
            body=request.POST.get('body'),
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
            'topics': Topic.objects.all(),
        }
        return render(request, template, context)

    elif request.method == 'POST':
        form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room = Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
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
            'topics': Topic.objects.all(),
        }
        return render(request, template, context)

    elif request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('room', pk=room.pk)


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


@login_required(login_url='login')
def updateUser(request):
    if request.method == 'GET':
        template = 'update_user.html'
        context = {
            'form': UserForm(instance=request.user),
        }
        return render(request, template, context)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', request.user.pk)
