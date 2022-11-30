from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.list, name='list'),
    path('detail/', views.detail, name='detail'),
]
