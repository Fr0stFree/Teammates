from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register(
    prefix='rooms',
    viewset=views.RoomViewSet,
    basename='rooms',
)
router.register(
    prefix='users',
    viewset=views.UserViewSet,
    basename='users',
)

urlpatterns = [
    path('', include(router.urls)),
]
