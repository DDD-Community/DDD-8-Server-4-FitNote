from django.urls import path, include
from . import views

urlpatterns = [
    path('hypeboyTest/', views.hypeboy, name='hypeboy'),
    path('lessonAdd/<int:user_id>', views.lessonAdd, name='lessonAdd'),
    path('add/<int:user_id>/<int:today>', views.add, name='add'),
    path('delete/<int:user_id>/<int:lesson_id>', views.delete, name='delete'),
    path('completion/<int:user_id>/<int:lesson_id>', views.completion, name='completion'),
    path('hypeboy/<int:user_id>', views.lessonIng, name='lessonIng'),
    path('lessonNow/<int:user_id>/<int:today>', views.lessonNow, name='lessonNow'),
    path('lessonEnd/', views.lessonEnd, name='lessonEnd'),

    # Json Return
    path('add/', views.addLesson, name='addLesson'),
    path('ing/', views.ingLesson, name='ingLesson'),
    path('delete/', views.deleteLesson, name='deleteLesson'),
    path('end/', views.endLesson, name='endLesson'),
    path('info/', views.getLesson, name='getLesson'),
    path('complet/', views.completionLesson, name='completionLesson'),
    
]