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
    prefix='rooms',
    viewset=views.RoomViewSet,
    basename='rooms',
)

urlpatterns = [
    path('auth/signup/', views.APISignUp.as_view(), name='signup'),
    path('auth/signin/', views.APISignIn.as_view(), name='signin'),
    path('', include(router.urls)),
]
