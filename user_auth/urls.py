from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Signup
    path('signup/', views.signup, name='signup'),
    # Login
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]