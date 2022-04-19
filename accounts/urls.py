from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path('member_register', views.member_register, name='member_register'),
    path('member_idcheck', views.member_idcheck, name='member_idcheck'),
    path('member_insert', views.member_insert, name='member_insert'),
    path('signin', views.signin_view, name='signin'),
    path('member_login', views.member_login, name='member_login'),
    path('member_logout', views.member_logout, name='member_logout'),
]