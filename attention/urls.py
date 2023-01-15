# user/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('memberList/<int:user_id>', views.memberList, name='memberList'),
    path('memberAdd/<int:user_id>', views.memberAdd, name='memberAdd'),
    path('memberEdit/<int:user_id>', views.memberEdit, name='memberEdit'),
    path('memberInfo/<int:member_id>', views.memberInfo, name='memberInfo'),
    path('memberSetting/<int:trainer_id>', views.memberSetting, name='memberSetting'),
    path('add2/<int:user_id>', views.add2, name='add2'),
    path('edit/<int:user_id>', views.edit, name='edit'),
    path('delete/<int:trainer_id>', views.delete, name='delete'),
    path('list/', views.getMemberList, name='getMemberList'),
]