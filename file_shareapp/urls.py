from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'file_shareapp'

urlpatterns = [
    path('public-view/', views.public_view, name="public_view"),
    path('file/<uuid:file_id>', views.success_view, name="file_detail_view"),
    path('auth-view/',views.auth_view , name="auth_view"),
    # path('files/', views.file_list, name='file_list', ),
]
