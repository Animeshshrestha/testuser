from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, UserProfileViewSet

router = routers.DefaultRouter()
router.register('user-signup', UserViewSet)
router.register('user-profile',UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]