from django.urls import path, include
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('docs/', views.docs, name='docs'),
    path('memberDocs/', views.memberDocs, name='memberDocs'),
    path('data/', views.getApi, name='data'),
]
