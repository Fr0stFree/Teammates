from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import User, Room, Topic, Message
from .forms import RoomForm, UserForm, CustomUserCreationForm


def loginPage(request):
    """
    Вью-функция для авторизации пользователя.
    """
    # Если авторизованный пользователь пытается попасть на логин-страницу
    # через адресную строку - редиректим его на домашнюю страницу
    if request.user.is_authenticated:
        return redirect('home')

    template = 'login&register.html'
    context = {
        'page': 'login',
    }
    if request.method == 'GET':
        return render(request, template, context)

    elif request.method == 'POST':
        # Валидация полученных из формы параметров и поиск на соответстие в БД
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Пользователь не найден')

        # В случае успешной аутентификации залогиним пользователя
        # и редиректим на домашнюю страницу
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Некорректный пароль')
        return render(request, template, context)


def registerPage(request):
    """
    Вью-функция для создания экземпляра пользователя.
    """
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
            messages.error(request, 'Невозможно создать пользователя с '
                                    'данными параметрами')
            return render(request, template, context)


def logoutUser(request):
    """
    Вью-функция удаление сессии пользователя.
    """
    logout(request)
    return redirect('home')


def home(request):
    """
    Вью-функция домашней страницы с фильтрацией контента в серчбаре.
    """
    template = 'rooms/home.html'
    # Получение параметров из адресной строки
    q = request.GET.get('q') if request.GET.get('q') else ''
    # Поиск полученныз параметров среди всех тематик, комнат и описаний комнат
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    context = {
        'rooms': rooms,
        'topics': Topic.objects.all(),
        'room_count': rooms.count(),
        'room_messages': Message.objects.filter(
            Q(room__topic__name__icontains=q)
        )[:5]

    }
    return render(request, template, context)


def room(request, pk):
    """
    Вью-функция страницы экземпляра комнаты.
    """
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'GET':
        template = 'rooms/room.html'
        context = {
            'room': room,
            'participants': room.participants.all(),
            'room_messages': room.messages.all(),
        }
        return render(request, template, context)

    # На данной странице возможно добавление комментария через POST-запрос
    elif request.method == 'POST':
        room.messages.create(
            user=request.user,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.pk)


def userProfile(request, pk):
    """
    Вью-функция страницы профиля  пользователя.
    """
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
    """
    Вью-функция создания экземпляра комнаты.
    """
    if request.method == 'GET':
        template = 'rooms/room_form.html'
        context = {
            'form': RoomForm(),
            'topics': Topic.objects.all(),
        }
        return render(request, template, context)

    elif request.method == 'POST':
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
    """
    Вью-функция изменения экземпляра комнаты.
    """
    room = Room.objects.get(pk=pk)

    # Если пользователь, не являющийся владельцем комнаты пытается изменить
    # комнату перейдя по url через адресную строку - запрещаем ему доступ
    if request.user != room.host and not request.user.is_superuser:
        return HttpResponseForbidden('Отказано в доступе')

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
    """
    Вью-функция удаления экземпляра комнаты.
    """
    room = Room.objects.get(pk=pk)

    # Если пользователь, не являющийся владельцем комнаты пытается удалить
    # комнату перейдя по url через адресную строку - запрещаем ему доступ
    if request.user != room.host and not request.user.is_superuser:
        return HttpResponseForbidden('Отказано в доступе')

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
def deleteMessage(request, pk):
    """
    Вью-функция удаления экземпляра комментария.
    """
    message = Message.objects.get(pk=pk)

    # Если пользователь, не являющийся владельцем комментария пытается удалить
    # комментарий перейдя по url через адресную строку - запрещаем ему доступ
    if request.user != message.user and not request.user.is_superuser:
        return HttpResponseForbidden('Отказано в доступе')

    if request.method == 'GET':
        template = 'delete.html'
        context = {
            'obj': message,
        }
        return render(request, template, context)

    elif request.method == 'POST':
        message.delete()
        return redirect('room', message.room.pk)


@login_required(login_url='login')
def updateUser(request):
    """
    Вью-функция изменения параметров экземпляра пользователя.
    """
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
