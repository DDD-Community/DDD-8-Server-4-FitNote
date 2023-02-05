from django.urls import path, include
from . import views

urlpatterns = [
    path('share/<int:user_id>/<int:today>', views.share, name='share'),
    path('add/', views.addLesson, name='addLesson'),
    path('ing/', views.ingLesson, name='ingLesson'),
    path('delete/', views.deleteLesson, name='deleteLesson'),
    path('end/', views.endLesson, name='endLesson'),
    path('info/', views.getLesson, name='getLesson'),
    path('complet/', views.completionLesson, name='completionLesson'),
]