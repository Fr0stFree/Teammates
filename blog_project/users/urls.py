from django.urls import path

from . import views


urlpatterns = [
    # Авторизация пользователя
    path('login/', views.loginPage, name='login'),
    # Регистрация пользователя
    path('register/', views.registerPage, name='register'),
    # Удаление собственной пользовательской сессии из кукис
    path('logout/', views.logoutUser, name='logout'),
    # URL изменения персональных пользовательских данных
    path('update/', views.updateUser, name='update-user'),
    # URL страницы пользователя
    path('<str:pk>/', views.userProfile, name='user-profile'),
]
