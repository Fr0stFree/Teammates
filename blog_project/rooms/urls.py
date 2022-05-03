from django.urls import path

from . import views


urlpatterns = [
    # Главная страница сайта
    path('', views.home, name='home'),
    # URL экземляра комнаты
    path('room/<str:pk>/', views.room, name='room'),
    # URL создания экземпляра комнаты
    path('create_room/', views.createRoom, name='create-room'),
    # URL изменения экземпляра комнаты
    path('update_room/<str:pk>/', views.updateRoom, name='update-room'),
    # URL удаления экземпляра комнаты
    path('delete_room/<str:pk>/', views.deleteRoom, name='delete-room'),
    # URL удаления экземпляра сообщения
    path('delete_msg/<str:pk>/', views.deleteMessage, name='delete-message'),
]
