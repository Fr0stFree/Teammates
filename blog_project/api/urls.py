from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router = SimpleRouter()
router.register(
    prefix='users',
    viewset=views.UserViewSet,
    basename='users',
)

router.register(
    prefix=r'rooms/(?P<room_pk>\d+)/messages',
    viewset=views.MessageViewSet,
    basename='messages',
)

router.register(
    prefix='rooms',
    viewset=views.RoomViewSet,
    basename='rooms',
)

urlpatterns = [
    path('auth/signup/', views.APISignUp.as_view(), name='signup'),
    path('auth/signin/', views.APISignIn.as_view(), name='signin'),
    #path('rooms/<int:room_pk>/messages/<int:message_pk/', views.APIMessage.as_view(), name='message'),
    path('', include(router.urls)),
]
