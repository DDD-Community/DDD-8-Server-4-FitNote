from django.urls import path, include
from . import views

urlpatterns = [
    path('hypeboyTest/', views.hypeboy, name='hypeboy'),
    path('lessonAdd/', views.lessonAdd, name='lessonAdd'),
    path('add/', views.add, name='add'),
    path('delete/<int:lesson_id>', views.delete, name='delete'),
    path('completion/<int:lesson_id>', views.completion, name='completion'),
    path('hypeboy/<int:user_id>', views.lessonIng, name='lessonIng'),
    path('lessonNow/<int:user_id>/<int:start_date>', views.lessonNow, name='lessonNow'),
    path('lessonEnd/', views.lessonEnd, name='lessonEnd'),
]
