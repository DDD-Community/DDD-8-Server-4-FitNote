from django.urls import path, include
from rest_framework import routers
from accounts.views import UserViewSet
from . import views

router = routers.DefaultRouter()
router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
