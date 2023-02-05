from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('list/', views.getMemberList, name='getMemberList'),
    path('add/', views.addMember, name='addMember'),
    path('info/', views.selectMember, name='selectMember'),
    path('edit/', views.editMember, name='editMember'),
    path('delete/', views.deleteMember, name='deleteMember'),
]