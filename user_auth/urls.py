from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

from django.contrib.auth import views as auth_views

app_name = 'user_auth'

urlpatterns = [
    # Signup
    path('register/', views.register, name='register'),
    # Login/Logout
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]