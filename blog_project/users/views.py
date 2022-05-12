from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

from rooms.models import Topic
from .models import User
from .forms import UserForm, CustomUserCreationForm


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
        email = request.POST.get('email').lower()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Пользователь не найден')
        # В случае успешной аутентификации залогиним пользователя
        # и редиректим на домашнюю страницу
        password = request.POST.get('password')
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
            user = form.save()
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
