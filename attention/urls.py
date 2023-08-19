from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('list/', views.getMemberList, name='getMemberList'),
    path('add/', views.addMember, name='addMember'),
    path('info/', views.selectMember, name='selectMember'),
    path('edit/', views.editMember, name='editMember'),
    path('delete/', views.deleteMember, name='deleteMember'),
    path('sample/', views.sample, name='sample'),
    ## 비밀번호 초기화
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('password_reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/', views.UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('send_email/', views.send_email, name='send_email'),
]